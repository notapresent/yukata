from __future__ import absolute_import

from google.appengine.api import urlfetch


class Downloader(object):
    def html(self, url, timeout=5):
        result = urlfetch.fetch(url=url, deadline=timeout)
        return result.content
