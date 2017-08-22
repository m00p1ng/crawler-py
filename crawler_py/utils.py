import re
from datetime import datetime
from urllib.parse import urlparse
from termcolor import colored
from collections import namedtuple

# dictionary for map hostname to ip address
hostname_ip = {}

# counter for downloaded link
link_counter = 0


def time_stamp():
    return datetime.now().strftime('%d-%m-%yT%H:%M:%S')


def print_log(text, color='white'):
    return print(colored(f"[{time_stamp()}]  {text}", color))


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
