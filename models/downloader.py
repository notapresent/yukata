from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from models import BaseModel


class Downloader(object):
    def html(self, url, timeout=5):
        result = urlfetch.fetch(url=url, deadline=timeout)
        return result.content
