# -*- coding: utf-8 -*-
import datetime
import logging

from google.appengine.api import taskqueue
import webapp2

from models import SCHEDULES
from models.miner import Miner


class TaskHandler(webapp2.RequestHandler):
    def runminer(self, miner_key):
        miner = Miner.from_urlsafe(miner_key)
        message = "Running miner {}".format(miner.name)
        logging.info(message)
        self.response.write(message)
        miner.run()

    def runjob(self, job_key):
        raise NotImplementedError()


class CronHandler(webapp2.RequestHandler):
    def runminers(self, schedule):
        task_url = self.uri_for('task-runminer')
        num_tasks = Miner.enqueue_scheduled_miners(schedule, task_url)
        self.response.write("Started {} for {}".format(num_tasks, schedule))
