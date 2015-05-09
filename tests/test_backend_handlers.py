import unittest

from google.appengine.api import memcache
from google.appengine.ext import testbed

import webapp2
from mock import patch, MagicMock

from models.miner import SCHEDULES
import backend
from backend.handlers import TaskHandler, CronHandler


class CronHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = backend.application
        # Set a dummy request just to be able to use uri_for().
        dummy_req = webapp2.Request.blank('/')
        dummy_req.app = self.app
        self.app.set_globals(app=self.app, request=dummy_req)

        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
        self.testbed.deactivate()

    def uri_for(self, route_name, *args, **kwargs):
        return webapp2.uri_for(route_name, None, *args, **kwargs)

    @patch('backend.handlers.TaskManager.enqueue_scheduled')
    def test_cron_runminers_calls_enque(self, mock_enqueue_scheduled):
        schedule = SCHEDULES.keys()[0]
        uri = self.uri_for('cron-run-scheduled-miners', schedule)
        runminer_uri = self.uri_for('task-runminer')
        response = self.app.get_response(uri)
        self.assertEqual(200, response.status_int)
        mock_enqueue_scheduled.assert_called_once_with(schedule, runminer_uri)
