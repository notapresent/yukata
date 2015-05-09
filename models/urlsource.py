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


def build_urlsource(urlsource_type, params):
    class_name = "{}URLSource".format(urlsource_type.title())
    class_ = getattr(sys.modules[__name__], class_name)
    obj = class_(kind=urlsource_type, **params)
    return obj


class BaseURLSource(ndb.Model):
    kind = ndb.StringProperty(required=True, choices=URLSOURCE_TYPES.keys(),
                              verbose_name='URL source type')


class SingleURLSource(BaseURLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='URL to crawl')


class ChainedURLSource(BaseURLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='Start URL')
    nextpage = ndb.LocalStructuredProperty(DataField, required=True)
    page_limit = ndb.IntegerProperty(default=1000)


class DatasetURLSource(BaseURLSource):
    dataset = ndb.KeyProperty(kind=DataSet, required=True)
    field_name = ndb.StringProperty(required=True, indexed=False)
    only_new = ndb.BooleanProperty(required=True, default=True)
    update_before_use = ndb.BooleanProperty(required=True, default=True)
