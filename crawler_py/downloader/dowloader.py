import socket
import requests
import re
from urllib.parse import urlparse

from ..database import db
from ..utils import (
    print_log,
    fill_http_prefix,
    hostname_ip,
)


class Downloader:
    def __init__(self, url):
        pass

    def insert_hostname(self):
        pass

    def get_robots(self):
        pass

    def get_hostname(self):
        pass

    def hostname_to_ip(self, hostname):
        pass
