from __future__ import absolute_import
import urlparse
from collections import OrderedDict

from google.appengine.ext import ndb

from lxml import etree


SELECTOR_TYPES = OrderedDict([
    (u'css', u'CSS'),
    (u'xpath', u'XPath'),
    (u'rx', u'RegExp')
])


class DataField(ndb.Model):
    selector = ndb.StringProperty()
    selector_type = ndb.StringProperty(choices=SELECTOR_TYPES.keys())
    rx = ndb.StringProperty()

    def extract(self, html):
        pass

    def extract_list(self, html):
        pass


class NamedDataField(DataField):
    name = ndb.StringProperty()
