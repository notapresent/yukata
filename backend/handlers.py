# -*- coding: utf-8 -*-
import os

import webapp2

from models import taskmanager


class CronHandler(webapp2.RequestHandler):
    def run_scheduled_robots(self, schedule):
        """
        Add all robots with specified schedule to execution queue
        """
        url = self.uri_for('task-runrobot')
        taskmanager.enqueue_scheduled_robots(schedule, url)


class TaskHandler(webapp2.RequestHandler):
    def run_robot(self):
        """
        Reconstructs robot from POST data and runs it
        """
        job_url = self.uri_for('task-runjob')
        taskmanager.run_robot(self.request.body, job_url)

    def run_job(self):
        """
        Reconstructs job from POST data and runs it
        """
        request_id = os.environ.get('REQUEST_LOG_ID')
        taskmanager.run_job(self.request.body)
