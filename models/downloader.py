from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb

from models import BaseModel


class Downloader(BaseModel):
    # requests per minute
    rpm = ndb.FloatProperty(required=True, default=1.0)
    timeout = ndb.IntegerProperty(required=True, default=5)    # seconds

    # TODO: Retry parameters, auth, reuest method, headers, cookies etc
