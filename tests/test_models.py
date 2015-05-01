import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from models import BaseModel

class BaseModelTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_from_urlsafe_finds_entity(self):
        model = BaseModel()
        model_key = model.put()
        urlsafe = model_key.urlsafe()
        self.assertIs(model, BaseModel.from_urlsafe(urlsafe))
