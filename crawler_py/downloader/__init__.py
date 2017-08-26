from urllib.parse import urlparse
import requests

from .fetcher import Fetcher
from ..database import Database as db
from ..analyzer import RobotsParser
from ..utils import print_log, fill_http_prefix
from ..errors import PageNotFound


class Downloader:
    def __init__(self, url):
        self.url = url
        self.hostname = urlparse(url).netloc

    def start(self):
        if not self.check_host_info_exist():
            self.get_robots()

        fetcher = Fetcher(self.url)
        return fetcher.get_content()

    def check_host_info_exist(self):
        url_parse = urlparse(self.url)

        result = db.host_info.find_one({
            'hostname': self.hostname
        }).count()

        return result > 0

    def get_robots(self):
        url = fill_http_prefix(self.hostname)
        url = f'{url}/robots.txt'
        res = requests.get(url)
        has_robots = self.has_robots(res)

        db.host_info.update_one(
            {'hostname': self.hostname},
            {'has_robots': has_robots, 'downloaded_robots': True}
        )

        if has_robots:
            rp = RobotsParser(self.hostname, res.content)
            rp.extract_link()
            rp.save()

    def has_robots(self, res):
        return res.status_code >= 200 or res.status_code < 300
