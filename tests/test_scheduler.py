import unittest

from crawler_py.database import Database
from crawler_py.scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    DATABASE_NAME = 'crawler_test'

    def setUp(self):
        Database.connect(self.DATABASE_NAME)
        self.add_data()

    def add_data(self):
        queue = [{
            'hostname': 'example.com',
            'resource': '/hello/world',
            'visited': False,
        }, {
            'hostname': 'example.com',
            'resource': '/search',
            'visited': False,
        }]

        for i in queue:
            Database.queue.insert_one(i)

    def test_update(self):
        s = Scheduler()
        s.update()
        self.assertEqual(len(s.queue), 2)

    def tearDown(self):
        Database._client.drop_database(self.DATABASE_NAME)


if __name__ == '__main__':
    unittest.main(buffer=True)
