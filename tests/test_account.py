import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from . import GAETestCase

from models.account import Account


class AccountTestCase(GAETestCase):
    def setUp(self):
        super(AccountTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def test_account_apikey_generation(self):
        acc_key = Account().put()
        self.assertIsNot(acc_key.get().apikey, None)
