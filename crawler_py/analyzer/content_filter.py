import hashlib
from urllib.parse import urlunparse
from datetime import datetime

from ..utils import print_log, split_url
from ..database import db


class ContentFilter:
    COLLECTION = 'contents_info'

    def __init__(self, url, content):
        self.url = url
        self.content = content

    def filter_duplicated(self):
        hash_ = hashlib.sha224(self.content.encode('utf-8')).hexdigest()
        if not db[self.COLLECTION].find_one({"hash": hash_}):
            self._save_hash(hash_, False)
            print_log(f"Added content of `{urlunparse(self.url)}` to database")
        else:
            self._save_hash(hash_, True)
            print_log(
                f"Content of `{urlunparse(self.url)}` is duplicated", 'yellow')

    def _save_hash(self, hash_, is_duplicated):
        url = split_url(self.url.geturl())
        result = db[self.COLLECTION].insert({
            "hostname": url.hostname,
            "resource": url.resource,
            "is_duplicated": is_duplicated,
            "timestamp": datetime.now(),
            "hash": hash_,
        })
        return result
