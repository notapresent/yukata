from __future__ import absolute_import
import urlparse
from collections import OrderedDict

from google.appengine.ext import ndb

import lxml



SELECTOR_TYPES = OrderedDict([
    (u'css', u'CSS'),
    (u'xpath', u'XPath'),
    (u'rx', u'RegExp')
])


class DataField(ndb.Model):
    selector = ndb.StringProperty()
    selector_type = ndb.StringProperty(choices=SELECTOR_TYPES.keys())
    rx = ndb.StringProperty()

    def process(self, html):
        if self.selector_type == 'xpath':
            return self.process_xpath(html)
        else:
            raise NotImplementedError

    def process_xpath(self, html):
        tree = lxml.etree.HTML(html)
        results = list()
        for elem in tree.xpath(self.selector):
            if isinstance(elem, basestring):
                results.append(elem)
            elif isinstance(elem, lxml.etree._Element):
                results.append(elem.text)
            else:
                raise ValueError('Not string and not etree.Element')

        return results[0] if len(results) == 1 else results


class NamedDataField(DataField):
    name = ndb.StringProperty()
