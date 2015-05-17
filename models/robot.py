from __future__ import absolute_import
from collections import OrderedDict

from google.appengine.ext import ndb

from models.dataset import DataSet
from models.urlsource import URLSource


SCHEDULES = OrderedDict([
    (u'm', u'Manual'),
    (u'1m', u'Once a minute'),
    (u'15m', u'Every 15 minutes'),
    (u'1h', u'Every hour'),
    (u'1d', u'Once a day'),
])


class Robot(ndb.Model):
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    name = ndb.StringProperty(required=False)
    schedule = ndb.StringProperty(choices=SCHEDULES.keys(),
                                  required=True,
                                  default=SCHEDULES.items()[0][0])
    # Download settings
    rps = ndb.FloatProperty(required=True, default=0.2)  # requests per second
    timeout = ndb.IntegerProperty(required=True, default=5)  # seconds

    # Submodels
    # urlsource = ndb.LocalStructuredProperty(URLSource)
    urlsource = ndb.StructuredProperty(URLSource, indexed=False)

    @classmethod
    def list(cls, ancestor=None):
        return cls.query(ancestor=ancestor).fetch()

    @classmethod
    def get_scheduled_robots(cls, schedule):
        # TODO limit and cursor
        robots = cls.query(cls.schedule == schedule).fetch()
        for robot in robots:
            yield robot

    @property
    def datasets(self):
        try:
            return self._datasets
        except AttributeError:
            self._datasets = DataSet.query(ancestor=self.key).fetch()
            return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = value

    @classmethod
    def _post_get_hook(cls, key, future):
        obj = future.get_result()
        obj.urlsource = URLSource.factory(obj.urlsource.to_dict())
