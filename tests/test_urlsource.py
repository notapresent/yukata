from . import GAETestCase

from models.urlsource import SingleURLSource


class URLSourceTestCase(GAETestCase):
    def setUp(self):
        super(URLSourceTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()


class SingleURLSourceTestCase(GAETestCase):
    def setUp(self):
        super(SingleURLSourceTestCase, self).setUp()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_urls_return_url(self):
        test_url = 'http://random-valid-url.com/'
        urlsource = SingleURLSource(url=test_url)
        self.assertEqual([test_url], list(urlsource.get_urls()))
