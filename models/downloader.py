from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from models import BaseModel


class Downloader(BaseModel):
    # requests per second
    rps = ndb.FloatProperty(required=True, default=0.2)     # FIXME move this
    timeout = ndb.IntegerProperty(required=True, default=5)    # seconds

    # TODO: Retry parameters, auth, reuest method, headers, cookies etc

    def html(self, url):
        result = urlfetch.fetch(url=url, deadline=self.timeout)
        return result.content
