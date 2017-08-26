import os
import shutil
import unittest
from urllib.parse import urlparse

from crawler_py import storage
from crawler_py.settings import SAVE_ROOT


class TestStorage(unittest.TestCase):
    def test_save_html(self):
        current_path = os.getcwd()
        test_data_path = os.path.join(
            current_path, 'tests', 'testdata', 'index.html'
        )

        with open(test_data_path, 'r') as file:
            test_data = file.read()

        url = 'http://example.com/hello/world'
        url_parse = urlparse(url)

        storage.save(url, test_data)

        test_save_path = os.path.join(SAVE_ROOT, url_parse.netloc, 'hello', 'world')
        self.assertTrue(os.path.exists(test_save_path))

        with open(test_save_path) as file:
            save_data = file.read()
        self.assertEqual(save_data, test_data)
        shutil.rmtree(SAVE_ROOT)

if __name__ == '__main__':
    unittest.main()
