from __future__ import absolute_import

from google.appengine.ext import ndb

from models import BaseModel


class Crawl(BaseModel):
    started = ndb.DateTimeProperty(auto_now_add=True)
