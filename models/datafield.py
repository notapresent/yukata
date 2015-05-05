from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb

from lxml import etree


class DataField(ndb.Model):
    name = ndb.StringProperty()
    selector = ndb.StringProperty()
    selector_type = ndb.StringProperty(choices=['css', 'xpath'])
    rx = ndb.StringProperty()

    def extract(self, html):
        pass

    def extract_list(self, html):
        pass
