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
        # self.request_id = os.environ.get('REQUEST_LOG_ID')
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
