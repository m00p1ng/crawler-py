from urllib.parse import urljoin

from ..database import Database as db
from ..utils import print_log, fill_http_prefix, split_url


class Scheduler:
    def __init__(self):
        self.queue = []

    def update(self, limit=100):
        self.queue = self._get_queue(limit)

    def _get_queue(self, limit):
        urls = db.queue.find(
            find_params={"visited": False},
            return_field={'hostname': 1, 'resource': 1, '_id': 0},
            limit=limit
        )

        urls_join = []
        for url in urls:
            hostname = fill_http_prefix(url['hostname'])
            resource = url['resource']
            urls_join.append(urljoin(hostname, resource))

        return urls_join

    def get_url(self):
        if self.size_queue() > 0:
            return self.queue[0]
        else:
            return None

    def size_queue(self):
        self.update()
        return len(self.queue)

    def count(self):
        return db.queue.count()

    def add(self, urls):
        url_list = []
        for url in urls:
            url_split = split_url(url)
            if not self._find_url(url_split):
                url_list.append({
                    'hostname': url_split.hostname,
                    'resource': url_split.resource,
                    'visited': False,
                })

        if url_list:
            db.queue.insert_many(url_list)
            self.update()

    def _find_url(self, url_split):
        result = db.queue.find_one({
            'hostname': url_split.hostname,
            'resource': url_split.resource,
        })

        if result:
            return True
        else:
            return False
