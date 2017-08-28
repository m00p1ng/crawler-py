import requests

from ..utils import print_log
from ..database import Database as db
from ..errors import PageNotFound
from ..settings import LIMIT_SITE, REQUEST_TIMEOUT


class Fetcher:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            link_counter = db.crawler_state.link_counter + 1
            print_log(f"[{link_counter}/{LIMIT_SITE}] GET '{self.url}'")
            res = requests.get(self.url, timeout=REQUEST_TIMEOUT)

            if res.status_code == 404:
                db.queue.update_visited_link(self.url)
                raise PageNotFound

            print_log(f"GET content successful")
            return res.text
        except requests.ConnectionError:
            print_log(f"Cannot GET content from {self.url}", 'red')
            db.queue.update_visited_link(self.url)
            db.error_log.add_log(self.url, "cant_get_content")
            return None
        except PageNotFound:
            print_log(f"Not Found Page", 'red')
            return None
