from __future__ import absolute_import
import logging
import datetime

from google.appengine.ext import ndb

from models import BaseModel
from models.job import Job
from models import taskmanager


class BaseCrawl(BaseModel):
    started_at = ndb.DateTimeProperty()
    num_jobs = ndb.IntegerProperty()    # Planned number of jobs or None if unknown
    finished_at = ndb.DateTimeProperty()
    status = ndb.StringProperty(choices=['success', 'warning', 'failure'])
    result = ndb.JsonProperty('r')    # Should use either this or gzipped one

    def __init__(self, *args, **kwargs):
        super(BaseCrawl, self).__init__(*args, **kwargs)
        self.robot = kwargs.get('robot')
        self.job_url = kwargs.get('job_url')

    @classmethod
    def _get_kind(cls):
        return 'Crawl'

    @property
    def jobs(self):
        return Job.query(Job.crawl_key == self.key).order(Job.created_at).fetch()

    def run(self):
        raise NotImplementedError("Must be implemented in subclass")

    @staticmethod
    def factory(robot, job_url):
        if robot.urlsource.class_name == 'SingleURLSource':
            crawl = SingleCrawl(parent=robot.key)
        else:
            raise NotImplementedError

        crawl.robot = robot
        crawl.job_url = job_url
        return crawl


class SingleCrawl(BaseCrawl):
    def run(self):
        self.started_at = datetime.datetime.utcnow()
        self.num_jobs = 1
        self.put()
        self.start()

    def start(self):
        logging.info('Started crawl {}'.format(self))
        url = self.robot.urlsource.url
        job = Job(crawl_key=self.key, url=url, created_at=datetime.datetime.utcnow(),
                  seq_num=0)
        job.on_complete = self.finish
        taskmanager.enqueue_job(self.job_url, self, job)

    def finish(self, status, result):
        self.finished_at = datetime.datetime.utcnow()
        self.status = status
        self.result = result
        self.put()
        logging.info('Finished crawl {}'.format(self))
