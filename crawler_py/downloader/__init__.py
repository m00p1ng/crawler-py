from urllib.parse import urlparse

from . import http
from .fetcher import Fetcher
from ..database import Database as db
from ..analyzer import RobotsParser
from ..utils import print_log
from ..urls import fill_http_prefix
from ..exceptions import PageNotFound


class Downloader:
    def __init__(self, url):
        self.url = url
        self.hostname = urlparse(url).netloc

    def start(self):
        fetcher = Fetcher(self.url)
        content = fetcher.get_content()

        if not self.check_host_info_exist():
            db.host_info.insert_one({'hostname': self.hostname})
            self.get_robots()

        return content

    def check_host_info_exist(self):
        result = db.host_info.find_one({
            'hostname': self.hostname
        })

        return result

    def get_robots(self):
        try:
            url = fill_http_prefix(self.hostname)
            url = f'{url}/robots.txt'

            print_log(f"GET robots.txt from {self.hostname}")
            res = http.get(url)
            has_robots = http.is_found_page(res.status_code)

            db.host_info.update_one(
                {'hostname': self.hostname},
                {'$set': {'has_robots': has_robots, 'downloaded_robots': True}}
            )

            if has_robots:
                rp = RobotsParser(self.hostname, res.text)
                rp.extract_link()
                rp.save()
                print_log(f"Saved disallow links from {self.hostname}")
            else:
                print_log(
                    f"Not found robots.txt from {self.hostname}", 'yellow')
        except http.exceptions.ConnectionError:
            print_log(f"Cannot GET {self.hostname}/robots.txt", 'red')
