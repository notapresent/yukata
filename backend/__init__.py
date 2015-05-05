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
        webapp2.Route('/runminer', 'backend.handlers.TaskHandler:run_miner',
                      'task-runminer'),
        webapp2.Route('/runjob', 'backend.handlers.TaskHandler:run_job', 
                      'task-runjob'),
    ]),
    
    # Cron routes
    PathPrefixRoute('/cron', [
        webapp2.Route('/runminers/<:\w+>',
                      'backend.handlers.CronHandler:run_scheduled_miners',
                      'cron-run-scheduled-miners'),
    ]),
]

application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
