import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from . import GAETestCase

from models import BaseModel


class BaseModelTestCase(GAETestCase):

    def setUp(self):
        super(BaseModelTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_by_urlsafe_finds_entity(self):
        model = BaseModel()
        model_key = model.put()
        urlsafe = model_key.urlsafe()
        self.assertIs(model, BaseModel.get_by_urlsafe(urlsafe))
