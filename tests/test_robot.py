from google.appengine.ext import ndb
from google.appengine.ext import testbed

from . import GAETestCase
from models.robot import Robot, SCHEDULES


class RobotTestCase(GAETestCase):
    def setUp(self):
        super(RobotTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.taskqueue = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def test_list_returns_empty_list(self):
        groupkey = ndb.Key('_', '_')
        self.assertEqual(Robot.list(ancestor=groupkey), [])

    def test_list_returns_one(self):
        groupkey = ndb.Key('_', '_')
        robot = Robot(parent=groupkey, name='_', schedule=SCHEDULES.keys()[0])
        robot.put()
        self.assertEqual(Robot.list(ancestor=groupkey), [robot])
