from __future__ import absolute_import

import hashlib
import random

from google.appengine.ext import ndb

from models import BaseModel


def make_apikey():
    m = hashlib.sha1()
    m.update(str(random.random()))
    return m.hexdigest()


class Account(BaseModel):
    created = ndb.DateTimeProperty(auto_now_add=True)
    apikey = ndb.StringProperty(required=True)

    def _pre_put_hook(self):
        if self.apikey is None:
            self.apikey = make_apikey()
