import os
import unittest
from urllib.parse import urlparse

from crawler_py.analyzer import ContentFilter
from crawler_py.database import Database as db


class TestContentFilter(unittest.TestCase):
    DATABASE_NAME = 'creawler_test'

    def setUp(self):
        db.connect(self.DATABASE_NAME)

        url = 'http://example.com/content'
        self.addContent(url)

    def addContent(self, url):
        current_path = os.getcwd()
        test_data_path = os.path.join(
            current_path, 'tests', 'testdata', 'robots.txt'
        )
        with open(test_data_path) as file:
            content = file.read()

        url_parse = urlparse(url)
        cf = ContentFilter(url_parse, content)
        cf.filter_duplicated()

    def test_add_content_success(self):
        count_content = db.content.find().count()
        self.assertEqual(count_content, 1)

    def test_filter_duplicated(self):
        url = 'http://example.com/duplicate'
        self.addContent(url)

        count_content = db.content.find().count()
        self.assertEqual(count_content, 2)

        duplicated_content = db.content.find_one({
            'hostname': 'example.com',
            'resource': '/duplicate',
        })

        self.assertTrue(duplicated_content['is_duplicated'])

    def tearDown(self):
        db._client.drop_database(self.DATABASE_NAME)


if __name__ == '__main__':
    unittest.main()
