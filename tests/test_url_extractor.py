import os
import unittest
from urllib.parse import urlparse

from crawler_py.analyzer import URLExtractor


class TestURLExtractor(unittest.TestCase):
    def test_extract_link(self):
        current_path = os.getcwd()
        test_data_path = os.path.join(
            current_path, 'tests', 'testdata', 'index.html'
        )

        with open(test_data_path) as file:
            content = file.read()

        url_parse = urlparse('http://example.com/test/path/content')
        ue = URLExtractor(url_parse, content)
        links = ue.extract_link()

        expect_links = [
            'http://example.com/search',
            'http://example.com/eiei',
            'http://example.com/test/helloworld',
        ]

        self.assertEqual(len(links), 3)
        for i, link in enumerate(links):
            self.assertEqual(link, expect_links[i])

if __name__ == '__main__':
    unittest.main()