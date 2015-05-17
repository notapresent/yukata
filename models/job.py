from __future__ import absolute_import
from google.appengine.ext import ndb

from models import BaseModel


class Job(BaseModel):
    crawl_key = ndb.KeyProperty(kind='Crawl', required=True)
    seq_num = ndb.IntegerProperty(indexed=False, required=True)
    url = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(required=True)
    saved_at = ndb.DateTimeProperty(auto_now=True)
    request_id = ndb.StringProperty()
    status = ndb.StringProperty()
    result = ndb.JsonProperty()
