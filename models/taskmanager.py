import pickle
from google.appengine.api import taskqueue


def pack(value):
    return pickle.dumps(value, pickle.HIGHEST_PROTOCOL)


def unpack(value):
    return pickle.loads(value)


def enqueue_robot(url, robot):
    """
    Add robot to task queue
    """
    taskqueue.add(url=url, payload=pack(robot))


def enqueue_job(url, crawl, job):
    """
    Add job to task queue
    """
    taskqueue.add(url=url, payload=pack((crawl, job)))
