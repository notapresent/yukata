# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import webapp2
from webapp2_extras.routes import PathPrefixRoute

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

config = {}

routes = [
    PathPrefixRoute('/task', [
        webapp2.Route('/runminer/<miner_key:[\w\-]+>',
                      'backend.handlers.TaskHandler:runminer',
                      'task-runminer'),
        webapp2.Route('/runjob/<job_key:[\w\-]+>',
                      'backend.handlers.TaskHandler:runjob', 'task-runjob'),
    ]),
    PathPrefixRoute('/cron', [
        webapp2.Route('/runminers/<schedule:\w+>',
                      'backend.handlers.CronHandler:runminers',
                      'cron-runminers'),
    ]),
]

application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
