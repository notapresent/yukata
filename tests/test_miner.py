from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from . import GAETestCase

from models.account import Account
from models.miner import Miner


class MinerTestCase(GAETestCase):
    def setUp(self):
        super(MinerTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_list_returns_empty_list(self):
        acckey = Account(apikey='dummy').put()
        self.assertEqual(Miner.list(ancestor=acckey), [])

    def test_list_returns_one(self):
        acckey = Account(apikey='dummy').put()
        miner = Miner(parent=acckey, name='dummy')
        miner.put()
        self.assertEqual(Miner.list(ancestor=acckey), [miner])

