'''Scheduler Module'''
from urllib.parse import urljoin, urlparse

from ..database import Database as db
from ..urls import fill_http_prefix, split_url
from ..settings import SEED_HOSTNAME, SEED_SCHEME


class Scheduler:
    def __init__(self):
        self.queue = []
        self.init_schedule()

    def init_schedule(self):
        self.update()

        if self.count() == 0:
            db.queue.insert_one({
                'scheme': SEED_SCHEME,
                'hostname': SEED_HOSTNAME,
                'resource': '/',
                'visited': False
            })
            self.update()

    def update(self, limit=100):
        if not self.queue:
            self.queue = self._get_queue(limit)

    def _get_queue(self, limit):
        urls = db.queue.find(
            find_params={"visited": False},
            return_field={
                "scheme": 1,
                'hostname': 1,
                'resource': 1,
                '_id': 0
            },
            limit=limit
        )

        urls_join = []
        for url in urls:
            hostname = fill_http_prefix(url['scheme'], url['hostname'])
            resource = url['resource']
            urls_join.append(urljoin(hostname, resource))

        return urls_join

    def get_url(self):
        if self.queue_size > 0:
            url = self.queue[0]
            self.queue.pop(0)
            return url
        else:
            return None

    @property
    def queue_size(self):
        self.update()
        return len(self.queue)

    def count(self):
        return db.queue.count()

    def add(self, urls):
        url_list = []
        for url in urls:
            url_split = split_url(url)
            scheme = urlparse(url).scheme
            if not scheme or scheme not in ['http', 'https']:
                scheme = "http"
            hostname = url_split.hostname
            resource = '/' + url_split.resource.strip('/')
            url_list.append({
                'scheme': scheme,
                'hostname': hostname,
                'resource': resource,
                'visited': False,
            })

        if url_list:
            db.queue.insert_many(url_list)
            self.update()
