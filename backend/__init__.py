# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import webapp2
from webapp2_extras.routes import PathPrefixRoute


DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

config = {}

routes = [

    # Task routes
    PathPrefixRoute('/task', [
        webapp2.Route('/runrobot', 'backend.handlers.TaskHandler:run_robot',
                      'task-runrobot'),
        webapp2.Route('/runjob', 'backend.handlers.TaskHandler:run_job',
                      'task-runjob'),
    ]),

    # Cron routes
    PathPrefixRoute('/cron', [
        webapp2.Route('/runrobots/<:\w+>',
                      'backend.handlers.CronHandler:run_scheduled_robots',
                      'cron-run-scheduled-robots'),
    ]),
]

application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
