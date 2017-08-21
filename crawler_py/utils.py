import re
from datetime import datetime
from urllib.parse import urlparse
from termcolor import colored
from collections import namedtuple

# dictionary for map hostname to ip address
hostname_ip = {}

# counter for downloaded link
link_counter = 0

# user agent for bot crawler
USER_AGENT = {
    "User-agent": "m00p1ng130t",
}

EXTENSIONS = {
    "application": [
        ".bin", ".bz", ".bz2", ".jar", ".js",
        ".json", ".rar", ".rtf", ".tar", ".ts",
        ".xhtml", ".xml", "zip", ".7z", ".pdf"
    ],
    "audio": [
        ".aac", "midi", ".wav",
    ],
    "image": [
        ".gif", ".ico", ".png", ".svg",
    ],
    "video": [
        ".avi", ".mpeg", ".mp4", "3gp",
    ],
    "text": [
        ".css", ".csv", ".htm", ".html",
    ],
    "font": [
        ".ttf", ".woff", ".woff2",
    ],
}

EXTRACT_EXTENSIONS = [
    ".htm", ".html", ".xml"
]


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

    if url_parse.params:
        resource += f';{url_parse.params}'
    if url_parse.query:
        resource += f'?{url_parse.query}'
    if url_parse.fragment:
        resource += f'#{url_parse.fragment}'

    split_result = namedtuple('SplitResult', ['hostname', 'resource'])
    return split_result(hostname=hostname, resource=resource)
