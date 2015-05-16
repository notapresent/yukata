# -*- coding: utf-8 -*-
import webapp2

from models import taskmanager
from models.robot import Robot


class TaskHandler(webapp2.RequestHandler):
    def run_robot(self):
        """
        Reconstructs robot from POST data and runs it
        """
        robot = taskmanager.unpack(self.request.body)
        job_url = self.uri_for('task-runjob')
        robot.run(job_url)

    def run_job(self):
        """
        Reconstructs job and crawl from POST data and runs job
        """
        crawl, job = taskmanager.unpack(self.request.body)
        if crawl.robot is None:
            raise RuntimeError
        job.run(crawl)


class CronHandler(webapp2.RequestHandler):
    def run_scheduled_robots(self, schedule):
        url = self.uri_for('task-runrobot')
        robots = Robot.get_scheduled_robots(schedule)
        for robot in robots:
            taskmanager.enqueue_robot('task-runrobot', robot)
