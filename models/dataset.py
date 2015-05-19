from __future__ import absolute_import

from google.appengine.ext import ndb

from models.datafield import NamedDataField


class DataSet(ndb.Model):
    """ Collection of NamedDataField objects
    """
    name = ndb.StringProperty(indexed=False)
    datafields = ndb.LocalStructuredProperty(NamedDataField, repeated=True)
