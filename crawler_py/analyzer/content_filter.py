import hashlib
from urllib.parse import urlunparse
from datetime import datetime

from .. import storage
from ..utils import print_log, split_url
from ..database import Database as db


class ContentFilter:
    def __init__(self, url_parse, content):
        self.url_parse = url_parse
        self.content = content

    def filter_duplicated(self):
        hash_ = hashlib.sha224(self.content.encode('utf-8')).hexdigest()
        url = urlunparse(self.url_parse)

        if not db.content.find_one({"hash": hash_}):
            self._save_hash(hash_, False)
            storage.save(self.url_parse, self.content)
            print_log(f"Added hash of '{url}' to database")
        else:
            self._save_hash(hash_, True)
            print_log(f"Content of '{url}' is duplicated", 'yellow')

    def _save_hash(self, hash_, is_duplicated):
        url = split_url(self.url_parse.geturl())
        result = db.content.insert_one({
            "hostname": url.hostname,
            "resource": url.resource,
            "is_duplicated": is_duplicated,
            "timestamp": datetime.now(),
            "hash": hash_,
        })
        return result
