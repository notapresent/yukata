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
        self.testbed.init_taskqueue_stub()
        self.taskqueue = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)


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

    def test_enqueue_scheduled_miners_enqueues(self):
        schedule = '1d'
        miner = Miner(name='testminer', schedule=schedule)
        miner_key = miner.put()
        baseurl = '/'
        n = Miner.enqueue_scheduled_miners(schedule, baseurl)
        self.assertEqual(1, n)

        tasks = self.taskqueue.get_filtered_tasks()
        self.assertEqual(1, len(tasks))
        self.assertIn(miner_key.urlsafe(), tasks[0].url)

