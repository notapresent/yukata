# -*- coding: utf-8 -*-
from datetime import datetime
import logging

from models.crawl import Crawl
from models.job import Job


class Crawler(object):
    def __init__(self, robot, crawl=None):
        self.robot = robot
        urlsource = robot.urlsource
        self._crawl = crawl

    def get_jobs(self):
        seq = 0
        for url in self.robot.urlsource.get_urls():
            job = Job(
                crawl_key=self.crawl.key,
                url=url,
                seq_num=seq, created_at=datetime.utcnow,
                status='new'
            )
            yield job

    def run_job(self, job, request_id):
        ck = self.crawl.key
        logging.info('Running job #{} from crawl #{}'.format(job.seq_num, ck.id()))
        job.request_id = request_id
        # self.status = 'failure'
        # try:
        #     self.request_id = os.environ.get('REQUEST_LOG_ID')
        #     dldr = Downloader()
        #     html = dldr.html(self.url)
        #     if crawl.robot.datasets:
        #         self.result = crawl.robot.process_datasets(html)
        #     self.status = 'success'
        # finally:
        #     # FIXME: If no more tries - suppress exception and set status=failed
        #     self.put()
        #     logging.info('Finished job {} from crawl {}'.format(self, self.crawl_key))
        #     self.crawl_key.get().finish(self.status, self.result)



    @property
    def crawl(self):
        if not self._crawl:
            self._crawl = Crawl(parent=self.robot.key)
            self._crawl.put()
        return self._crawl

# class SingleCrawl(BaseCrawl):
#     def run(self):
#         self.started_at = datetime.datetime.utcnow()
#         self.num_jobs = 1
#         self.put()
#         self.start()
#
#     def start(self):
#         logging.info('Started crawl {}'.format(self))
#         url = self.robot.urlsource.url
#         job = Job(crawl_key=self.key, url=url, created_at=datetime.datetime.utcnow(),
#                   seq_num=0)
#         job.on_complete = self.finish
#         taskmanager.enqueue_job(self.job_url, self, job)
#
#     def finish(self, status, result):
#         self.finished_at = datetime.datetime.utcnow()
#         self.status = status
#         self.result = result
#         self.put()
#         logging.info('Finished crawl {}'.format(self))

    # def run(self, job_url):
    #     """ Creates and starts a crawl
    #     """
    #     logging.info("Robot {} started mining".format(self.name))
    #     self.urlsource = URLSource.factory(self.urlsource.to_dict())
    #
    #     crawl = BaseCrawl.factory(self, job_url)
    #     crawl.run()
