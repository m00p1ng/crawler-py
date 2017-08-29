import requests

from ..settings import HEADERS, REQUEST_TIMEOUT

exceptions = requests.exceptions


def get(url):
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    return response


def is_found_page(status_code):
    return status_code >= 200 and status_code < 300
