from __future__ import absolute_import

from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    @classmethod
    def get_by_urlsafe(cls, urlsafe_key, **ctx_options):
        return ndb.Key(urlsafe=urlsafe_key).get(**ctx_options)

    def populate_existing(self, values):
        """
        Set attributes from keyword arguments, ignoring non-existing keys

        :param values: dict
        :return: None
        """
        for k, v in values.items():
            if k in self._properties:
                print "Setting {} to {} ".format(k, v)
                setattr(self, k, v)