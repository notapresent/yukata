from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb

from models.datafield import NamedDataField


class DataSet(ndb.Model):
    """ Collection of NamedDataField objects
    """
    name = ndb.StringProperty(indexed=False)
    fields = ndb.LocalStructuredProperty(NamedDataField, repeated=True)

    def process(self, html):
        results = {}
        for field in self.fields:
            results[field.name] = field.process(html)
        return results
