from __future__ import absolute_import

from google.appengine.ext import ndb

SCHEDULES = {
    '1m': 'Onca a minute',
    '15m': 'Every 15 minutes',
    '1h': 'Every hour',
    '1d': 'Once a day',
    'm': 'Manual'
}


class BaseModel(ndb.Model):
    @classmethod
    def get_by_urlsafe(cls, urlsafe_key, **ctx_options):
        return ndb.Key(urlsafe=urlsafe_key).get(**ctx_options)
