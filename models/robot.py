from __future__ import absolute_import
import logging
import datetime
from collections import OrderedDict

from google.appengine.ext import ndb

from models import BaseModel
from models.dataset import DataSet
from models.urlsource import URLSource


SCHEDULES = OrderedDict([
    (u'm', u'Manual'),
    (u'1m', u'Once a minute'),
    (u'15m', u'Every 15 minutes'),
    (u'1h', u'Every hour'),
    (u'1d', u'Once a day'),
])


class Robot(BaseModel):
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    name = ndb.StringProperty(required=False)
    schedule = ndb.StringProperty(choices=SCHEDULES.keys(),
                                  required=True,
                                  default=SCHEDULES.items()[0][0])
    # Download settings
    rps = ndb.FloatProperty(required=True, default=0.2)  # requests per second
    timeout = ndb.IntegerProperty(required=True, default=5)    # seconds

    # Submodels
    # urlsource = ndb.LocalStructuredProperty(URLSource)
    urlsource = ndb.StructuredProperty(URLSource)

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


    def process_datasets(self, html):
        result = dict()
        for ds in self.datasets:
            result[ds.name] = ds.process(html)
        return result

    def dictify(self):
        """
        Returns all data necessary to run robot
        """
        dictified = self.to_dict(exclude=['created_at', 'name', 'schedule'])
        dictified['id'] = self.key.id()
        return dictified
