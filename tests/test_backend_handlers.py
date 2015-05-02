import unittest

from google.appengine.api import memcache
from google.appengine.ext import testbed

import webapp2
import webtest
from mock import patch, MagicMock

from backend import config, routes
from backend.handlers import TaskHandler, CronHandler


class CronHandlerTestCase(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(routes, debug=True, config=config)
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
        self.testbed.deactivate()

    @patch('models.miner.Miner.enqueue_scheduled_miners')
    def test_runminers(self, mock_esm):
        schedule = '1d'
        response = self.testapp.get('/cron/runminers/' + schedule)
        self.assertEqual(response.status_int, 200)
#         mock_credentials.set_store.assert_called_once_with(mock_store)
        mock_esm.assert_called_once_with(schedule, '/task/runminer/')



    def disabledtestCacheHandler(self):
        # First define a key and value to be cached.
        key = 'answer'
        value = '42'
        self.testbed.init_memcache_stub()
        params = {'key': key, 'value': value}
        # Then pass those values to the handler.
        response = self.testapp.post('/cache/', params)
        # Finally verify that the passed-in values are actually stored in Memcache.
        self.assertEqual(value, memcache.get(key))

