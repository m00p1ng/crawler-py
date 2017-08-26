import os

from .content_filter import ContentFilter
from .robots_parser import RobotsParser
from .url_extractor import URLExtractor
from .url_filter import URLFilter
from ..utils import url_to_path, check_extension
from ..settings import SEED_HOSTNAME


class Analyzer:
    def __init__(self, url_parse, content):
        self.url_parse = url_parse
        self.content = content

    def start(self):
        self._content_analyzer()
        return self._url_analyzer()

    def _content_analyzer(self):
        cf = ContentFilter(self.url_parse, self.content)
        cf.filter_duplicated()

    def _url_analyzer(self):
        ue = URLExtractor(self.url_parse, self.content, SEED_HOSTNAME)
        urls = ue.extract_link()

        urls = [url for url in urls if self._filter_extension(url)]

        uf = URLFilter(urls)
        urls = uf.filter_links()
        return urls

    def _filter_extension(self, url):
        filepath = url_to_path(url)
        filename = filepath.filename

        return check_extension(filename)
