from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlunparse

from ..utils import is_relative_path, print_log


class URLExtractor:
    def __init__(self, url, content):
        self.url = url
        self.content = content

    def extract_link(self):
        print_log("Extracting URL...")
        links = []
        soup = BeautifulSoup(self.content, 'html.parser')

        links += self._find_tag(soup, 'a', 'href')
        links += self._find_tag(soup, 'img', 'src')
        links += self._find_tag(soup, 'frame', 'src')

        return links

    def _find_tag(self, soup, tagname, attribute):
        results = soup.find_all(tagname)
        links = []

        for tag in results:
            link = tag[attribute]
            if is_relative_path(link):
                link = urljoin(urlunparse(self.url), link)
            links.append(link)

        return links        