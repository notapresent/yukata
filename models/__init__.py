from __future__ import absolute_import

from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    @classmethod
    def get_by_urlsafe(cls, urlsafe_key, **ctx_options):
        return ndb.Key(urlsafe=urlsafe_key).get(**ctx_options)
