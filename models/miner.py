from __future__ import absolute_import
import logging
import datetime
from collections import OrderedDict

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from models import BaseModel
from models.dataset import DataSet
from models.urlsource import BaseURLSource, build_urlsource
from models.downloader import Downloader
import models.crawl


SCHEDULES = OrderedDict([
    (u'm', u'Manual'),
    (u'1m', u'Once a minute'),
    (u'15m', u'Every 15 minutes'),
    (u'1h', u'Every hour'),
    (u'1d', u'Once a day'),
])


class Miner(BaseModel):
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    name = ndb.StringProperty(required=True, default='Anonymous miner')
    schedule = ndb.StringProperty(choices=SCHEDULES.keys(),
                                  required=True,
                                  default=SCHEDULES.items()[0][0])

    # Submodels
    # urlsource = ndb.LocalStructuredProperty(BaseURLSource)
    urlsource = ndb.StructuredProperty(BaseURLSource)
    downloader = ndb.StructuredProperty(Downloader)
    datasets = ndb.LocalStructuredProperty(DataSet, repeated=True)

    @classmethod
    def list(cls, ancestor=None):
        return cls.query(ancestor=ancestor).fetch()

    @classmethod
    def get_scheduled_miners(cls, schedule):
        # TODO limit and cursor
        miners = cls.query(cls.schedule == schedule).fetch()
        for miner in miners:
            yield miner

    def mine(self):
        """ Creates and starts a crawl
        """
        self.urlsource = build_urlsource(self.urlsource.kind,
                                         self.urlsource.to_dict(exclude=['kind']))
        if not self.downloader:
            self.downloader = Downloader()

        logging.info("Miner {} started mining".format(self.name))
        crawl = models.crawl.make_crawl(self.urlsource.kind, self.key)
        crawl.miner = self
        crawl.run()

    def process_datasets(self, html):
        result = dict()
        for ds in self.datasets:
            result[ds.name] = ds.process(html)
        return result

    def dictify(self):
        """
        Returns all data necessary to run miner
        """
        dictified = self.to_dict(exclude=['created_at', 'name', 'schedule'])
        dictified['id'] = self.key.id()
        return dictified
