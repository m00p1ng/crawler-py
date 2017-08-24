import unittest
from datetime import datetime

from crawler_py.utils import *


class TestUtils(unittest.TestCase):
    def test_fill_http_prefix(self):
        url = 'example.com'
        url_with_http = fill_http_prefix(url)
        self.assertEqual(url_with_http, 'http://example.com')

    def test_is_relative_path(self):
        self.assertIsNone(True)

    def test_split_url(self):
        self.assertIsNone(True)

    def test_join_modifier_url(self):
        self.assertIsNone(True)


if __name__ == '__main__':
    unittest.main()
