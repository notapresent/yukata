# -*- coding: utf-8 -*-
import datetime
import logging

from google.appengine.api import taskqueue
import webapp2

from models.taskmanager import TaskManager
from models import SCHEDULES
from models.miner import Miner


class TaskHandler(webapp2.RequestHandler):
    def run_miner(self):
        """
        Reconstructs miner from POST data and runs it
        """
        miner = Miner()
        miner.populate(self.request.POST)
        miner.start()

    def run_job(self):
        """
        Reconstructs mining job from POST data and runs it
        """
        pass


class CronHandler(webapp2.RequestHandler):
    def run_scheduled_miners(self, schedule):
        TaskManager.enqueue_scheduled(schedule, self.uri_for('task-runminer'))
