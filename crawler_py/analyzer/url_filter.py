import re
from urllib.parse import urljoin

from ..utils import print_log, split_url
from .. import database as db


class URLFilter:
    def __init__(self, urls):
        self.urls = urls

    def filter_links(self):
        print_log("Filtering URL disallowed links...")
        self.filter_disallow()
        print_log("Filtering successful")

        print_log("Filtering URL duplicated links...")
        self.filter_duplicated()
        print_log("Filtering successful")

    def filter_disallow(self):
        urls = []
        for url in self.urls:
            if not self._is_disallowed(url):
                urls.append(url)
        self.urls = urls
        return urls

    def _is_disallowed(self, url):
        url_split = split_url(url)
        disallow_links = db.disallow_links.find(
            {"hostname": url_split.hostname},
            {"resource": 1, "_id": 0}
        )

        for link in disallow_links:
            pattern = r'^' + re.escape(link['resource'])
            if re.match(pattern, url_split.resource):
                print_log(f"{url} is disallowed", 'red')
                return True
        return False

    def filter_duplicated(self):
        urls = []
        for url in self.urls:
            url_split = split_url(url)
            result = db.queue.find_one({
                "hostname": url_split.hostname,
                "resource": url_split.resource,
            })

            if not result:
                urls.append(url)
            else:
                print_log(f"`{url}` is duplicated", 'yellow')

        self.urls = urls
        return urls
