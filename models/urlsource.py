# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import urlparse
from collections import OrderedDict

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from models import BaseModel
from models.datafield import DataField


URLSOURCE_TYPES = OrderedDict([
    (u'SingleURLSource', u'Single URL'),
    (u'ChainedURLSource', u'Chained'),
])


def validate_http_url(prop, url):
    normalized = normalize_http_url(url)
    if len(normalized) > 1500:
        raise ValueError('URL cannot exceed 1500 bytes')
    return normalized


def normalize_http_url(url):
    url = url.strip()
    if not url.lower().startswith('http'):
        url = 'http://{}'.format(url)
    return urlparse.urlsplit(url).geturl()


class URLSource(polymodel.PolyModel):
    def num_jobs(self):
        raise NotImplementedError

    def get_urls(self):
        raise NotImplementedError

    @property
    def class_name(self):
        return self.class_[-1]

    @staticmethod
    def factory(data):
        class_obj = getattr(sys.modules[__name__], data['class_name'])
        obj = class_obj()

        values = data.copy()
        del values['class_name']
        obj.populate(**values)
        return obj


class SingleURLSource(URLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='URL to crawl')

    def num_jobs(self):
        return 1

    def get_urls(self):
        return self.url


class ChainedURLSource(URLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='Start URL')
    nextpage = ndb.LocalStructuredProperty(DataField, required=True)
    page_limit = ndb.IntegerProperty(default=1000)

    def num_jobs(self):
        return None



