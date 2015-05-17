from __future__ import absolute_import

from google.appengine.ext import ndb

from models.job import Job


class Crawl(ndb.Model):
    started_at = ndb.DateTimeProperty()
    num_jobs = ndb.IntegerProperty()  # Planned number of jobs or None if unknown
    finished_at = ndb.DateTimeProperty()
    status = ndb.StringProperty(choices=['success', 'warning', 'failure', 'canceled'])
    result = ndb.JsonProperty()

    @property
    def jobs(self):
        return Job.query(Job.crawl_key == self.key).order(Job.created_at).fetch()
