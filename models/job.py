from __future__ import absolute_import

from google.appengine.ext import ndb

from webapp2_extras import json

from models import BaseModel
from models.miner import Miner


class Job(BaseModel):
    crawl_key = ndb.KeyProperty('c', kind=Crawl, required=True)
    url = ndb.StringProperty('u', required=True)
    enqueued = ndb.DateTimeProperty('e', required=True)
    saved = ndb.DateTimeProperty('s', auto_now=True)
    request_id = ndb.StringProperty()
    payload = ndb.JsonProperty('p')    # Should use either this or gzipped one
    gzipped_payload = ndb.JsonProperty('zp', compressed=True)
