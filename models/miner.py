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
    name = ndb.StringProperty(indexed=False, required=True)
    schedule = ndb.StringProperty(choices=SCHEDULES.keys(), required=True)

    # Submodels
    urlsource = ndb.LocalStructuredProperty(BaseURLSource)
    downloader = ndb.LocalStructuredProperty(Downloader)
    datasets = ndb.LocalStructuredProperty(DataSet, repeated=True)

    @classmethod
    def list(cls, ancestor=None):
        return cls.query(ancestor=ancestor).fetch()

    @classmethod
    def enqueue_scheduled_miners(cls, schedule, task_url):
        # TODO Add tasks in batches
        miners = cls.query(cls.schedule == schedule).fetch()
        for m in miners:
            taskqueue.add(url=task_url + m.key.urlsafe())
        msg = "Start {} miners with {} schedule".format(len(miners), schedule)
        logging.info(msg)
        return len(miners)

    def run(self):
        pass
