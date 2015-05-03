from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb

from models.datafield import DataField


class DataSet(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    datafields = ndb.LocalStructuredProperty(DataField, repeated=True)
