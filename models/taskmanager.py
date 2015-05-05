from google.appengine.api import taskqueue


class TaskManager(object):
    @classmethod
    def enqueue_scheduled(cls, schedule, task_url):
        """ 
        Enqueue scheduled miners 
        """
        # TODO: process in batches
        for miner in Miner.get_scheduled_miners(schedule):
            taskqueue.add(url=task_url, payload=miner.dictify())
        
        
        