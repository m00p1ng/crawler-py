from ..database import db
from ..utils import print_log

class Scheduler:
    def __init__(self):
        self.queue = []
    
    def add_links(self, urls):
        self.queue += urls

    def _get_queue(self):
        COLLECTION = 'queue_links'

        queues = db[COLLECTION].find({"visited": False})