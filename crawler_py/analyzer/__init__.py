import os
from urllib.parse import urlparse

from .content_filter import ContentFilter
from .robots_parser import RobotsParser
from .url_extractor import URLExtractor
from .url_filter import URLFilter
from ..settings import SEED_HOSTNAME, DEBUG
from ..urls import is_ignore_link
from ..utils import check_extension, print_log


class Analyzer:
    def __init__(self, url, content):
        self.url = url
        self.url_parse = urlparse(url)
        self.content = content

    def start(self):
        is_duplicated = self._content_analyzer()
        if is_duplicated:
            return [], is_duplicated
        else:
            return self._url_analyzer(), is_duplicated

    def _content_analyzer(self):
        cf = ContentFilter(self.url_parse, self.content)
        return cf.filter_duplicated()

    def _url_analyzer(self):
        ue = URLExtractor(self.url_parse, self.content, SEED_HOSTNAME)
        urls = ue.extract_link()

        if urls:

            uf = URLFilter(urls)
            urls = uf.filter_links()

            before_link = len(urls)
            urls = [url for url in urls if self._filter_extension(url)]
            urls = [url for url in urls if self._filter_ignore_link(url)]

            uniq_link = len(urls)
            skip_link = before_link - uniq_link
            if skip_link > 0 and not DEBUG:
                print_log(f"Skiped {skip_link} URLs", 'yellow')
            print_log(f"Passed {uniq_link} URLs", 'green')

        return urls

    def _filter_extension(self, url):
        filename = urlparse(url).path
        extension = os.path.splitext(filename)[1]
        result = check_extension(filename)
        if not result and DEBUG:
            message = f"Skip file extension {extension}"
            message += f" [{url}]"
            print_log(message, 'yellow')

        return result

    def _filter_ignore_link(self, url):
        result, ignore_word = is_ignore_link(url)
        if result and DEBUG:
            message = f"Skip URL because contain '{ignore_word}'"
            message += f" [{url}]"
            print_log(message, 'yellow')

        return not result
