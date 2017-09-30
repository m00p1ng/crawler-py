import hashlib
from urllib.parse import urlunparse
from datetime import datetime

from .. import storage
from ..utils import print_log
from ..urls import split_url
from ..database import Database as db

content_cached = set()


class ContentFilter:
    def __init__(self, url_parse, content):
        self.url_parse = url_parse
        self.content = content

    def filter_duplicated(self):
        hash_ = hashlib.sha224(self.content.encode('utf-8')).hexdigest()
        url = urlunparse(self.url_parse)

        if not hash_ in content_cached and \
                not db.content.find_one({"hash": hash_}):
            self._save_hash(hash_, False)
            print_log("Added hash to database")

            storage.save(url, self.content)
            print_log("Stored content to disk")
            content_cached.add(hash_)
            return False
        else:
            self._save_hash(hash_, True)
            db.error_log.add_log(url, "duplicated_content")
            print_log(f"Duplicated Content", 'yellow')
            return True

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

    def _find_host(self):
        url = split_url(self.url_parse.geturl())
        return db.content.find_one({
            'hostname': url.hostname,
            'resource': url.resource,
        })
