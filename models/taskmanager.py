import pickle
from google.appengine.api import taskqueue


def pack(value):
    return pickle.dumps(value, pickle.HIGHEST_PROTOCOL)


def unpack(value):
    return pickle.loads(value)


def run_miner(url, miner):
    """
    Add miner to task queue
    """
    taskqueue.add(url=url, payload=pack(miner))


def run_job(url, miner, crawl, job):
    """
    Add job to task queue
    """
    taskqueue.add(url=url, payload=pack((miner, crawl, job)))
