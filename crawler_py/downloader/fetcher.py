import requests

from ..utils import print_log, split_url
from ..database import Database as db
from ..errors import PageNotFound


class Fetcher:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        print_log(f"Getting... '{self.url}'")
        res = requests.get(self.url)

        url_split = split_url(self.url)

        db.queue.update_one(
            {'hostname': url_split.hostname, 'resource': url_split.resource},
            {'visited': True}
        )

        if res.status_code == 404:
            print_log(f"'{self.url}' not found", 'red')
            raise PageNotFound

        print_log(f"'{self.url}' was stored")
        return res.content
