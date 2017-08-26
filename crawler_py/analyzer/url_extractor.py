import re
from urllib.parse import urljoin, urlunparse, urlparse
from bs4 import BeautifulSoup

from ..utils import is_relative_path, print_log, split_url
from ..settings import DEBUG, MAX_LEVEL


class URLExtractor:
    def __init__(self, url_parse, content, root):
        self.url_parse = url_parse
        self.content = content
        self.root = root

    def extract_link(self):
        print_log("Extracting URLs...")
        urls = []
        soup = BeautifulSoup(self.content, 'html.parser')

        redi_url = self._redirect_match(soup)
        if redi_url:
            urls.append(redi_url)
        urls += self._find_tag(soup, 'a', 'href')

        return urls

    def _find_tag(self, soup, tagname, attribute):
        results = soup.find_all(tagname)
        urls = []

        for tag in results:
            if tag.has_attr(attribute):
                url = tag[attribute]
                if is_relative_path(url):
                    url = urljoin(urlunparse(self.url_parse), url)
                if (self._is_under_seed_root(url) and self._is_lower_max_level(url) and
                        not self._is_long_filename(url)):
                    urls.append(url)
                    if DEBUG:
                        print_log(f"Found '{url}'", 'cyan')

        return urls

    def _is_under_seed_root(self, url):
        url_parse = urlparse(url)
        return self.root in url_parse.netloc

    def _redirect_match(self, soup):
        pattern = r'.*?window\.location\s*=\s*\"([^"]+)\"'
        redirMatch = re.match(pattern, str(soup), re.M | re.S)

        if redirMatch and "http" in redirMatch.group(1):
            url = redirMatch.group(1)
            if DEBUG:
                print_log(f"Found '{url}'", 'cyan')
            return url
        else:
            return None

    def _is_lower_max_level(self, url):
        url_split = split_url(url)
        level = url_split.resource.split('/')

        return len(level) < MAX_LEVEL

    def _is_long_filename(self, url):
        url_split = split_url(url)
        if len(url_split.resource) > 255:
            print_log(f"Skip URL {url}", 'yellow')
            return True
        return False
