from __future__ import absolute_import

import logging

from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import BaseModel, SCHEDULES
from models.dataset import DataSet
from models.urlsource import BaseURLSource
from models.downloader import Downloader


class Miner(BaseModel):
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    name = ndb.StringProperty(required=True, default='Anonymous miner')
    schedule = ndb.StringProperty(choices=SCHEDULES.keys(), required=True,
                                  default='m')

    # Submodels
    urlsource = ndb.LocalStructuredProperty(BaseURLSource)
#    downloader = ndb.LocalStructuredProperty(Downloader)
#    datasets = ndb.LocalStructuredProperty(DataSet, repeated=True)

    @classmethod
    def list(cls, ancestor=None):
        return cls.query(ancestor=ancestor).fetch()

    @classmethod
    def get_scheduled_miners(cls, schedule):
        # TODO limit and cursor
        miners = cls.query(cls.schedule == schedule).fetch()
        for miner in miners:
            yield miner

    def start(self):
        """ Starts a miner
        """
        pass

    def dictify(self):
        """
        Returns all data necessary to run miner
        """
        dictified = self.to_dict(exclude=['created_at', 'name', 'schedule'])
        dictified['id'] = self.key.id()
        return dictified

