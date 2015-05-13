# -*- coding: utf-8 -*-
import webapp2

from models import taskmanager
# from models.miner import Miner


class TaskHandler(webapp2.RequestHandler):
    def run_miner(self):
        """
        Reconstructs miner from POST data and runs it
        """
        pass
        # miner = Miner()
        # miner.populate(self.request.POST)
        # miner.mine()

    def run_job(self):
        """
        Reconstructs mining job from POST data and runs it
        """
        pass


class CronHandler(webapp2.RequestHandler):
    def run_scheduled_miners(self, schedule):
        taskmanager.enqueue_scheduled_miners(schedule)
