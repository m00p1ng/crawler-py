import unittest

from crawler_py.database import Database


class TestDatabase(unittest.TestCase):
    def test_connection(self):
        db = Database.connect()
        self.assertIsNotNone(db)


if __name__ == '__main__':
    unittest.main(buffer=True)
