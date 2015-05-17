
from google.appengine.api import taskqueue

from models import ndb_serialize
from models.crawler import Crawler
from models.robot import Robot


def enqueue_robot(url, robot):
    urlsource = robot.urlsource
    taskqueue.add(url=url, payload=ndb_serialize.dumps(robot))


def enqueue_scheduled_robots(schedule, url):
    for robot in Robot.get_scheduled_robots(schedule):
        # TODO batch add
        taskqueue.add(url=url, payload=ndb_serialize.dumps(robot))


def run_robot(request_body, job_url):
    robot = ndb_serialize.loads(request_body)
    crawler = Crawler(robot)
    crawl = crawler.crawl
    for job in crawler.get_jobs():
        # TODO batch add
        taskqueue.add(url=job_url, payload=ndb_serialize.dumps((robot, crawl, job)))


def run_job(request_body):
    robot, crawl, job = ndb_serialize.loads(request_body)
    crawler = Crawler(robot=robot, crawl=crawl)
    crawler.run_job(job)
