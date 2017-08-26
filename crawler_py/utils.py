import re
import os
from datetime import datetime
from collections import namedtuple
from urllib.parse import urlparse
from termcolor import colored

from .settings import EXTRACT_EXTENSIONS


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


def url_to_path(url_parse):
    filepath = namedtuple('FilePath', ['path', 'filename'])
    if url_parse.path in ['/', '']:
        filename = join_modifier_url('index.html', url_parse)
        path = ''
    else:
        filename = url_parse.path.split('/')[-1]
        filename = join_modifier_url(filename, url_parse)
        path = url_parse.path.split('/')[:-1]
        path = os.path.join(*path)

    return filepath(path=path, filename=filename)


def check_extension(filename):
    extension = os.path.splitext(filename)[1]
    if extension in EXTRACT_EXTENSIONS or extension is '':
        return True
    else:
        return False
