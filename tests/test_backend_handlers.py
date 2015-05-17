import unittest

from google.appengine.api import memcache
from google.appengine.ext import testbed

import webapp2
from mock import patch, MagicMock

from models.robot import SCHEDULES
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
