# -*- coding: utf-8 -*-
import webapp2

from models import taskmanager
from models.miner import Miner


class TaskHandler(webapp2.RequestHandler):
    def run_miner(self):
        """
        Reconstructs miner from POST data and runs it
        """
        miner = taskmanager.unpack(self.request.body)
        job_url = self.uri_for('task-runjob')
        miner.run(job_url)

    def run_job(self):
        """
        Reconstructs job, crawl and miner from POST data and runs job
        """
        miner, crawl, job = taskmanager.unpack(self.request.body)

        print 'Request length: ', len(self.request.body)

        job.run(miner, crawl)


class CronHandler(webapp2.RequestHandler):
    def run_scheduled_miners(self, schedule):
        url = self.uri_for('task-runminer')
        miners = Miner.get_scheduled_miners(schedule)
        for miner in miners:
            taskmanager.run_miner('task-runminer', miner)
