from __future__ import absolute_import
from collections import OrderedDict

from google.appengine.ext import ndb
from lxml import etree, cssselect


SELECTOR_TYPES = OrderedDict([
    (u'xpath', u'XPath'),
    (u'css', u'CSS'),
    # (u'rx', u'RegExp')
])


class DataField(ndb.Model):
    selector = ndb.StringProperty()
    selector_type = ndb.StringProperty(choices=SELECTOR_TYPES.keys(),
                                       default=SELECTOR_TYPES.keys()[0])
    rx = ndb.StringProperty()

    def process(self, html):
        if self.selector_type == 'xpath':
            return self.process_xpath(html)
        elif self.selector_type == 'css':
            return self.process_css(html)
        else:
            raise NotImplementedError

    def process_xpath(self, html):
        tree = etree.HTML(html)
        results = list()
        for elem in tree.xpath(self.selector):
            if isinstance(elem, basestring):
                results.append(elem)
            elif isinstance(elem, etree._Element):
                results.append(elem.text)
            else:
                raise ValueError('Not string and not etree.Element')

        return results[0] if len(results) == 1 else results

    def process_css(self, html):
        sel = cssselect.CSSSelector(self.selector)
        tree = tree = etree.HTML(html)
        results = list()
        for elem in sel(tree):
            if isinstance(elem, basestring):
                results.append(elem)
            elif isinstance(elem, etree._Element):
                results.append(elem.text)
            else:
                raise ValueError('Not string and not etree.Element')

        return results[0] if len(results) == 1 else results


class NamedDataField(DataField):
    name = ndb.StringProperty()
