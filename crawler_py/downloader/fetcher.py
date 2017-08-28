import re
import requests

from ..utils import print_log
from ..database import Database as db
from ..exceptions import PageNotFound
from ..settings import LIMIT_SITE, REQUEST_TIMEOUT, ACCEPTED_CONTENT_TYPES


class Fetcher:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            link_counter = db.crawler_state.link_counter + 1
            print_log(f"[{link_counter}/{LIMIT_SITE}] GET '{self.url}'")
            res = requests.get(self.url, timeout=REQUEST_TIMEOUT)

            if res.status_code == 404:
                db.queue.update_visited_link(self.url)
                raise PageNotFound

            print_log(f"GET content successful")

            for content_type in ACCEPTED_CONTENT_TYPES:
                if re.match(content_type, res.headers['Content-Type']):
                    return res.text
            return None

        except requests.ConnectionError:
            print_log("Cannot GET content", 'red')
            db.error_log.add_log(self.url, "cant_get_content")
            return None

        except requests.ReadTimeout:
            print_log("Request Timeout", 'red')
            db.error_log.add_log(self.url, "request_timeout")

        except PageNotFound:
            print_log("Not Found Page", 'red')
            return None
