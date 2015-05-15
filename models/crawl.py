from __future__ import absolute_import
import logging
import datetime

from google.appengine.ext import ndb

from models import BaseModel
from models.job import Job
from models import taskmanager


def make_crawl(urlsource_kind, parent_key):
    if urlsource_kind == 'single':
        return SingleCrawl(parent=parent_key)
    else:
        raise NotImplementedError


class BaseCrawl(BaseModel):
    started_at = ndb.DateTimeProperty()
    num_jobs = ndb.IntegerProperty()    # Planned number of jobs or None if unknown
    finished_at = ndb.DateTimeProperty()
    status = ndb.StringProperty(choices=['success', 'warning', 'failure'])
    result = ndb.JsonProperty('r')    # Should use either this or gzipped one

    @classmethod
    def _get_kind(cls):
        return 'Crawl'

    @property
    def jobs(self):
        return Job.query(Job.crawl_key == self.key).order(Job.created_at).fetch()

    def run(self):
        raise NotImplementedError("Must be implemented in subclass")


class SingleCrawl(BaseCrawl):
    def run(self, miner):
        self.started_at = datetime.datetime.utcnow()
        self.num_jobs = 1
        self.put()
        self.start(miner)

    def start(self, miner):
        logging.info('Started crawl {}'.format(self))
        url = miner.urlsource.url
        job = Job(crawl_key=self.key, url=url, created_at=datetime.datetime.utcnow(),
                  seq_num=0)
        job.on_complete = self.finish
        taskmanager.run_job('/task/runjob', miner, self, job)

    def finish(self, status, result):
        self.finished_at = datetime.datetime.utcnow()
        self.status = status
        self.result = result
        self.put()
        logging.info('Finished crawl {}'.format(self))
