import unittest
from urllib.parse import urlparse, urlunparse

from crawler_py.urls import *


class TestUtils(unittest.TestCase):
    def test_fill_http_prefix(self):
        url = 'example.com'
        url_with_http = fill_http_prefix(url)
        self.assertEqual(url_with_http, 'http://example.com')

    def test_is_relative_path(self):
        self.assertFalse(is_relative_path('http://example.com'))
        self.assertTrue(is_relative_path('example.com'))
        self.assertTrue(is_relative_path('../helloworld'))

    def test_split_url(self):
        url = 'http://example.com/path?name=john#segment'
        result = split_url(url)
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.resource, '/path?name=john#segment')

    def test_join_modifier_url(self):
        url = 'http://example.com/path?name=john#segment'
        url_parse = urlparse(url)
        joined_url = join_modifier_url(url_parse.path, url_parse)
        self.assertEqual(joined_url, '/path?name=john#segment')


if __name__ == '__main__':
    unittest.main()
