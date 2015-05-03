from __future__ import absolute_import
import urlparse

from google.appengine.ext import ndb

from models import BaseModel
from models.datafield import DataField
from models.dataset import DataSet


def validate_http_url(url):
    normalized = normalize_http_url(url)
    if len(normalized) > 1500:
        raise ValueError('URL cannot exceed 1500 bytes')
    return normalized


def normalize_http_url(url):
    url = url.strip()
    if not url.lower().startswith('http'):
        url = 'http://{}'.format(url)
    return urlparse.urlsplit(url).geturl()


class BaseURLSource(ndb.Expando):
    pass


class SingleURLSource(BaseURLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='URL to crawl')


class ChainedURLSource(BaseURLSource):
    url = ndb.StringProperty(required=True, validator=validate_http_url,
                             verbose_name='Start URL')
    nextpage = ndb.LocalStructuredProperty(DataField, required=True)
    page_limit = ndb.IntegerProperty(default=1000)


class DataSetURLSource(BaseURLSource):
    target_key = ndb.KeyProperty(kind=DataSet, required=True)
    field_name = ndb.StringProperty(required=True, indexed=False)
    only_new = ndb.BooleanProperty(required=True, default=True)
    update_before_use = ndb.BooleanProperty(required=True, default=True)
