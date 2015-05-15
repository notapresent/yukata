# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import urlparse
from collections import OrderedDict

from google.appengine.ext import ndb

from models import BaseModel
from models.datafield import DataField
from models.dataset import DataSet


URLSOURCE_TYPES = OrderedDict([
    (u'single', u'Single URL'),
    (u'chained', u'Chained'),
    (u'dataset', u'Dataset'),
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


class BaseURLSource(BaseModel):
    kind = ndb.StringProperty(required=True, choices=URLSOURCE_TYPES.keys(),
                              verbose_name='URL source type')

    def num_jobs(self):
        raise NotImplementedError

    def get_urls(self):
        raise NotImplementedError

    @staticmethod
    def factory(urlsource_dict):
        kind = urlsource_dict['kind']
        class_name = "{}URLSource".format(kind.title())
        class_obj = getattr(sys.modules[__name__], class_name)
        instance = class_obj(kind=kind)
        instance.populate(**urlsource_dict)
        return instance


class SingleURLSource(BaseURLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='URL to crawl')

    def num_jobs(self):
        return 1

    def get_urls(self):
        return self.url


class ChainedURLSource(BaseURLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='Start URL')
    nextpage = ndb.LocalStructuredProperty(DataField, required=True)
    page_limit = ndb.IntegerProperty(default=1000)

    def num_jobs(self):
        return None


class DatasetURLSource(BaseURLSource):
    dataset = ndb.KeyProperty(kind=DataSet, required=True)
    field_name = ndb.StringProperty(required=True, indexed=False)
    only_new = ndb.BooleanProperty(required=True, default=True)
    update_before_use = ndb.BooleanProperty(required=True, default=True)
