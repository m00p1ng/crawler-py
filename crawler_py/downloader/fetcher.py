import re

from . import http
from ..utils import print_log
from ..database import Database as db
from ..exceptions import PageNotFound, ContentTypeNotFound, ContentTypeNotAccepted
from ..settings import LIMIT_SITE, ACCEPTED_CONTENT_TYPES


class Fetcher:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            link_counter = db.crawler_state.link_counter + 1
            print_log(f"[{link_counter}/{LIMIT_SITE}] GET '{self.url}'")
            res = http.get(self.url)

            if res.status_code == 404:
                db.queue.update_visited_link(self.url)
                raise PageNotFound

            print_log(f"GET content successful")

            return self.check_content_type(res)

        except http.exceptions.ConnectionError:
            print_log("Cannot GET content", 'red')
            db.error_log.add_log(self.url, "cant_get_content")

        except http.exceptions.ReadTimeout:
            print_log("Request Timeout", 'red')
            db.error_log.add_log(self.url, "request_timeout")

        except http.exceptions.TooManyRedirects:
            print_log("Too Many Redirect", 'red')
            db.error_log.add_log(self.url, "many_redirect")

        except PageNotFound:
            print_log("Not Found Page", 'red')

        except ContentTypeNotFound:
            print_log("Content-type Not Found", 'red')

        except ContentTypeNotAccepted as e:
            print_log(f"Content-type '{e.content_type}' Not Accepted", 'red')

    def check_content_type(self, response):
        if 'content-type' not in response.headers:
            raise ContentTypeNotFound

        for content_type in ACCEPTED_CONTENT_TYPES:
            if re.match(content_type, response.headers['content-type']):
                return response.text
        raise ContentTypeNotAccepted(response.headers['content-type'])
