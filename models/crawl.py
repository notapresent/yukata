from __future__ import absolute_import

from google.appengine.ext import ndb

from models import BaseModel
from models.miner import Miner


class Crawl(BaseModel):
    enqueued = ndb.DateTimeProperty('e')
    num_jobs = timeout = ndb.IntegerProperty()
