import requests

from ..utils import print_log, split_url
from ..database import Database as db
from ..errors import PageNotFound
from ..settings import LIMIT_SITE, REQUEST_TIMEOUT


class Fetcher:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            link_counter = self._get_counter() + 1
            link_counter_id = self._get_counter_id()
            print()
            print_log(f"[{link_counter}/{LIMIT_SITE}] GET '{self.url}'")
            res = requests.get(self.url, timeout=REQUEST_TIMEOUT)

            self._update_visited_link()

            if res.status_code == 404:
                raise PageNotFound

            self._update_link_counter(link_counter_id)
            print_log(f"GET content successful")
            return res.text
        except requests.ConnectionError:
            print_log(f"Cannot GET content from {self.url}", 'red')
            self._update_visited_link()
            return None
        except PageNotFound:
            print_log(f"Not Found Page '{self.url}'", 'red')
            return None

    def _update_visited_link(self):
        url_split = split_url(self.url)

        db.queue.update_one(
            {'hostname': url_split.hostname, 'resource': url_split.resource},
            {'$set': {'visited': True}}
        )

    def _update_link_counter(self, _id):
        db.crawler_state.update_one(
            {'_id': _id},
            {'$inc': {'link_counter': 1}}
        )

    def _get_counter(self):
        return db.crawler_state.find_one()['link_counter']

    def _get_counter_id(self):
        return db.crawler_state.find_one()['_id']
