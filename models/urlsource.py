# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import urlparse
from collections import OrderedDict

from google.appengine.ext import ndb

from models.datafield import DataField


URLSOURCE_TYPES = OrderedDict([
    ('single', 'Single URL'),
    ('chained', 'Chained'),
])


def validate_http_url(_, url):
    normalized = normalize_http_url(url)
    if len(normalized) > 1500:
        raise ValueError('URL cannot exceed 1500 bytes')
    return normalized


def normalize_http_url(url):
    url = url.strip()
    if not url.lower().startswith('http'):
        url = 'http://{}'.format(url)
    return urlparse.urlsplit(url).geturl()


class URLSource(ndb.Expando):
    @classmethod
    def _get_kind(cls):
        return 'URLSource'

    kind = ndb.StringProperty(required=True, choices=URLSOURCE_TYPES.keys())

    @classmethod
    def _post_get_hook(cls, key, future):
        obj = future.get_result()
        if obj is not None:
            # test needed because post_get_hook is called even if get() fails!
            pass


class SingleURLSource(URLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='URL to crawl')


class ChainedURLSource(URLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='Start URL')
    next_page = ndb.StructuredProperty(DataField, required=True, indexed=False)
    page_limit = ndb.IntegerProperty(default=100)
