import unittest

from google.appengine.ext import testbed
import webapp2

import backend


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
