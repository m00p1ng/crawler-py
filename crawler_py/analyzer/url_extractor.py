import re
from urllib.parse import urljoin, urlunparse, unquote
from bs4 import BeautifulSoup

from ..utils import print_log
from ..urls import is_relative_path, split_url, is_under_seed_root
from ..settings import DEBUG, MAX_LEVEL


class URLExtractor:
    def __init__(self, url_parse, content):
        self.url_parse = url_parse
        self.content = content

    def extract_link(self):
        print_log("Extracting URLs...")
        urls = []
        soup = BeautifulSoup(self.content, 'html.parser')

        redi_url = self._redirect_match(soup)
        meta_url = self._meta_redirect(soup)
        if redi_url:
            urls.append(redi_url)
        if meta_url:
            urls.append(meta_url)
        urls += self._find_tag(soup, 'a', 'href')

        if urls:
            print_log(f"Found {len(urls)} URLs", 'cyan')
        else:
            print_log(f"Not Found URLs", 'yellow')

        return urls

    def _find_tag(self, soup, tagname, attribute):
        results = soup.find_all(tagname)
        urls = []

        for tag in results:
            if tag.has_attr(attribute):
                url = unquote(tag[attribute])
                if is_relative_path(url):
                    url = urljoin(urlunparse(self.url_parse), url)
                if is_under_seed_root(url) and self._is_lower_max_level(url):
                    urls.append(url)
                    if DEBUG:
                        print_log(f"Found '{url}'", 'cyan')

        return urls

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

    def _meta_redirect(self, soup):
        result = soup.find("meta", attrs={"http-equiv": "Refresh"})
        if result and hasattr(result, 'content'):
            if result['content'].find(';') == -1:
                return None
            _, text = result["content"].split(";")
            if text.strip().lower().startswith("url="):
                url = text[4:]
                if DEBUG:
                    print_log(f"Found '{url}'", 'cyan')
                return url
        return None

    def _is_lower_max_level(self, url):
        url_split = split_url(url)
        level = url_split.resource.split('/')

        return len(level) < MAX_LEVEL
