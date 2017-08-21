from ..database import db
from ..utils import print_log
from urllib.parse import urljoin


class Scheduler:
    def __init__(self):
        self.queue = []

    def update(self, limit=100):
        self._get_queue(limit)

    def _get_queue(self, limit):
        COLLECTION = 'queue_links'

        urls = db[COLLECTION].find(
            {"visited": False},
            {'hostname': 1, 'resource': 1, '_id': 0}
        ).limit(limit)

        self.queue = [urljoin(url.hostname, url.resource) for url in urls]
