from urllib.parse import urlparse

from . import http
from ..database import Database as db
from ..analyzer import RobotsParser
from ..utils import print_log
from ..urls import fill_http_prefix


class RobotFetcher:
    def __init__(self, url):
        self.hostname = urlparse(url).netloc
        self.scheme = urlparse(url).scheme
        if not self.scheme in ['http', 'https']:
            self.scheme = 'http'
        self.robot_url = fill_http_prefix(self.scheme, self.hostname) 
        self.robot_url = f'{self.robot_url}/robots.txt'

    def get(self):
        try:
            print_log(f"GET robots.txt from {self.scheme}://{self.hostname}")
            res = http.get(self.robot_url)
            has_robots = http.is_found_page(res.status_code)

            db.host_info.update_one(
                {'hostname': self.hostname},
                {'$set': {'has_robots': has_robots, 'downloaded_robots': True}}
            )

            if has_robots:
                rp = RobotsParser(self.hostname, res.text)
                rp.extract_link()
                rp.save()
                print_log(f"Saved disallow links from {self.scheme}://{self.hostname}")
            else:
                print_log(
                    f"Not found robots.txt from {self.scheme}://{self.hostname}", 'yellow')

        except http.exceptions.ConnectionError:
            print_log(f"Cannot GET {self.scheme}://{self.hostname}/robots.txt", 'red')

        except http.exceptions.ReadTimeout:
            print_log("Request Timeout", 'red')
            db.error_log.add_log(self.robot_url, "request_timeout")
