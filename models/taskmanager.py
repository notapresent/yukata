from google.appengine.ext import deferred

import models.miner


def enqueue_scheduled_miners(schedule):
    """
    Enqueue scheduled miners
    """
    # TODO: process in batches
    for miner in models.miner.Miner.get_scheduled_miners(schedule):
        deferred.defer(miner.mine)


def schedule_job(method, *args):
    deferred.defer(method, *args)


def run_miner(miner):
    deferred.defer(miner.mine)
