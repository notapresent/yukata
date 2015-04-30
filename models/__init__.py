from __future__ import absolute_import

from google.appengine.ext import ndb

SCHEDULES = {
    '15m': 'Every 15 minutes',
    '1h': 'Every hour',
    '1d': 'Once a day',
    'm': 'Manual'
}


class BaseModel(ndb.Model):
    @classmethod
    def from_urlsafe(cls, urlsafe_key, **ctx_options):
        key = ndb.Key(urlsafe=urlsafe_key)
        return key.get(**ctx_options)
