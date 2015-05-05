from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from . import GAETestCase

from models import SCHEDULES
from models.miner import Miner


class MinerTestCase(GAETestCase):
    def setUp(self):
        super(MinerTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.taskqueue = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def test_list_returns_empty_list(self):
        groupkey = ndb.Key('_', '_')
        self.assertEqual(Miner.list(ancestor=groupkey), [])

    def test_list_returns_one(self):
        groupkey = ndb.Key('_', '_')
        miner = Miner(parent=groupkey, name='_', schedule=SCHEDULES.keys()[0])
        miner.put()
        self.assertEqual(Miner.list(ancestor=groupkey), [miner])
