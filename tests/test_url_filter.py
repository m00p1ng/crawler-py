import unittest

from crawler_py.analyzer.url_filter import URLFilter
from crawler_py.database import Database as db


class TestURLFilter(unittest.TestCase):
    DATABASE_NAME = 'crawler_test'

    def setUp(self):
        db.connect(self.DATABASE_NAME)
        self.add_queue()
        self.add_disallow()

    def add_queue(self):
        queue = [{
            'hostname': 'example.com',
            'resource': '/test',
            'visited': False,
        }, {
            'hostname': 'test.com',
            'resource': '/test',
            'visited': False,
        }]

        for link in queue:
            db.queue.insert_one(link)
    
    def add_disallow(self):
        db.disallow_links.insert_one({
            'hostname': 'example.com',
            'resource': '/disallow'
        })

    def test_filter_links(self):
        urls = [
            'http://example.com/test',
            'http://example.com/haha',
            'http://example.com/disallow',
        ]

        uf = URLFilter(urls)
        links = uf.filter_links()
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], urls[1])
    
    def tearDown(self):
        db._client.drop_database(self.DATABASE_NAME)


if __name__ == '__main__':
    unittest.main()
