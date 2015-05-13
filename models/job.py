from __future__ import absolute_import
import os
import logging
from google.appengine.ext import ndb

from webapp2_extras import json

from models import BaseModel


class Job(BaseModel):
    crawl_key = ndb.KeyProperty(kind='Crawl', required=True)
    seq_num = ndb.IntegerProperty(indexed=False, required=True)
    url = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(required=True)
    saved_at = ndb.DateTimeProperty(auto_now=True)
    request_id = ndb.StringProperty()
    status = ndb.StringProperty()
    result = ndb.JsonProperty()    # Should use either this or gzipped one

    def run(self, miner, crawl):
        logging.info('Running job {} from crawl {}'.format(self, self.crawl_key))

        self.status = 'failure'
        try:
            self.request_id = os.environ.get('REQUEST_LOG_ID')
            html = miner.downloader.html(self.url)
            if miner.datasets:
                self.result = miner.process_datasets(html)
            self.status = 'success'
        finally:
            # FIXME: If no more tries - suppress exception and set status=failed
            self.put()
            logging.info('Finished job {} from crawl {}'.format(self, self.crawl_key))
            self.crawl_key.get().finish(self.status, self.result)

