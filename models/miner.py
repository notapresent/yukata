from __future__ import absolute_import

import logging

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

from lxml import etree

from models import BaseModel


class Miner(BaseModel):
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    name = ndb.StringProperty(indexed=False)
    schedule = ndb.StringProperty()

    def run(self):
        pass
