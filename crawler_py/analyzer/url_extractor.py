import re
from urllib.parse import urljoin, urlunparse, urlparse
from bs4 import BeautifulSoup

from ..utils import is_relative_path, print_log


class URLExtractor:
    def __init__(self, url_parse, content, root):
        self.url_parse = url_parse
        self.content = content
        self.root = root

    def extract_link(self):
        print_log("Extracting URLs...")
        urls = []
        soup = BeautifulSoup(self.content, 'html.parser')

        urls += self._find_tag(soup, 'a', 'href')
        # urls += self._find_tag(soup, 'img', 'src')
        # urls += self._find_tag(soup, 'frame', 'src')

        return urls

    def _find_tag(self, soup, tagname, attribute):
        results = soup.find_all(tagname)
        urls = []

        for tag in results:
            url = tag[attribute]
            if is_relative_path(url):
                url = urljoin(urlunparse(self.url_parse), url)
            if self._is_under_seed_root(url):
                urls.append(url)

        return urls

    def _is_under_seed_root(self, url):
        url_parse = urlparse(url)
        return re.match(self.root, url_parse.netloc)
