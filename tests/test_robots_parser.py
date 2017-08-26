import os
import unittest

from crawler_py.database import Database as db
from crawler_py.analyzer import RobotsParser


class TestRobotsParser(unittest.TestCase):
    DATABASE_NAME = 'crawler_test'

    def setUp(self):
        db.connect(self.DATABASE_NAME)

    def test_extract_link(self):
        current_path = os.getcwd()
        test_data_path = os.path.join(
            current_path, 'tests', 'testdata', 'robots.txt'
        )
        with open(test_data_path) as file:
            content = file.read()

        hostname = 'example.com'

        rp = RobotsParser(hostname, content)
        disallow_link = rp.extract_link()

        expect_resources = [
            '/search'
        ]

        self.assertEqual(len(disallow_link), 1)
        self.assertListEqual(expect_resources, disallow_link)

    def test_save(self):
        current_path = os.getcwd()
        test_data_path = os.path.join(
            current_path, 'tests', 'testdata', 'robots.txt'
        )
        with open(test_data_path) as file:
            content = file.read()

        hostname = 'example.com'

        rp = RobotsParser(hostname, content)
        rp.extract_link()
        rp.save()

        count_disallow_links = db.disallow_links.find().count()
        self.assertEqual(count_disallow_links, 1)


    def tearDown(self):
        db._client.drop_database(self.DATABASE_NAME)


if __name__ == '__main__':
    unittest.main(buffer=True)
