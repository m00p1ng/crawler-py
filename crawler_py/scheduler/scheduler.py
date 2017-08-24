from urllib.parse import urljoin

from .. import database as db
from ..utils import print_log


class Scheduler:
    def __init__(self):
        self.queue = []

    def update(self, limit=100):
        self.queue = self._get_queue(limit)

    def _get_queue(self, limit):
        urls = db.queue.find(
            find_val={"visited": False},
            return_field={'hostname': 1, 'resource': 1, '_id': 0},
            limit=limit
        )

        return [urljoin(url.hostname, url.resource) for url in urls]
