import re
from datetime import datetime
from collections import namedtuple
from urllib.parse import urlparse
from termcolor import colored


def print_log(text, color='white'):
    timestamp = datetime.now().strftime('%d-%m-%yT%H:%M:%S')
    print(colored(f"[{timestamp}]  {text}", color))


def fill_http_prefix(url):
    if not re.match(r'^https?://', url):
        return f'http://{url}'
    return url


def is_relative_path(url):
    url_parse = urlparse(url)
    return not bool(url_parse.netloc)


def split_url(url):
    url_parse = urlparse(url)
    hostname = url_parse.netloc

    resource = url_parse.path
    resource = join_modifier_url(resource, url_parse)

    split_result = namedtuple('SplitResult', ['hostname', 'resource'])
    return split_result(hostname=hostname, resource=resource)


def join_modifier_url(source, url_parse):
    result = source
    if url_parse.params:
        result += f';{url_parse.params}'
    if url_parse.query:
        result += f'?{url_parse.query}'
    if url_parse.fragment:
        result += f'#{url_parse.fragment}'
    return result
