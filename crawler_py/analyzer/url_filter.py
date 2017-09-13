import re

from ..utils import print_log
from ..urls import split_url
from ..database import Database as db
from ..settings import DEBUG


class URLFilter:
    def __init__(self, urls):
        self.urls = urls

    def filter_links(self):
        print_log("Filtering URL disallowed links...")
        disallowed_links = self.filter_disallow()
        if disallowed_links == 0:
            print_log("URLs not found in robots.txt")
        else:
            print_log(f"Disallowed {disallowed_links} URLs", 'red')


        print_log("Filtering duplicated URLs...")
        duplicated_links = self.filter_duplicated()
        if duplicated_links == 0:
            print_log("URLs not duplicated")
        else:
            print_log(f"Duplicated {duplicated_links} URLs", 'yellow')

        return self.urls

    def filter_disallow(self):
        urls = []
        for url in self.urls:
            if not self._is_disallowed(url):
                urls.append(url)

        disallow_link = len(self.urls) - len(urls)
        self.urls = urls

        return disallow_link

    def _is_disallowed(self, url):
        url_split = split_url(url)
        disallow_links = db.disallow_links.find(
            {"hostname": url_split.hostname},
            {"resource": 1, "_id": 0}
        )

        for link in disallow_links:
            pattern = r'^' + re.escape(link['resource'])
            if re.match(pattern, url_split.resource):
                if DEBUG:
                    print_log(f"Disallowed '{url}'", 'red')
                return True
        return False

    def filter_duplicated(self):
        urls = []
        for url in self.urls:
            url_split = split_url(url)
            result = db.queue.find_one({
                "hostname": url_split.hostname,
                "resource": '/' + url_split.resource.strip('/'),
            })

            if not result and url not in urls:
                urls.append(url)
            else:
                if DEBUG:
                    print_log(f"Duplicated '{url}'", 'yellow')

        duplicated_links = len(self.urls) - len(urls)
        self.urls = urls

        return duplicated_links
