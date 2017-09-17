DEBUG = False

SEED_URL = 'http://ku.ac.th'

LIMIT_SITE = 10000
MAX_LEVEL = 10
REQUEST_TIMEOUT = 10
DELAY_FETCH = 10

DATABASE_NAME = 'crawler-py'

HEADERS = {
    "User-agent": "m00p1ng130t",
}

ACCEPTED_CONTENT_TYPES = [
    'text/html',
    'application/xml',
    'application/xhtml+xml',
]

EXTRACT_EXTENSIONS = [
    ".htm", ".html", ".xml", ".php", ".asp"
]

IGNORE_WORD_LIST = [
    "image",
    "photo",
    "picture",
    "gallery",
    "album",
    "mailto",
    "download",
    "login",
    "logout",
    "#",
]

import os
from urllib.parse import urlparse

DATABASE_CONFIG_PATH = os.path.realpath('db.json')

# set default value
if 'SAVE_ROOT' not in globals():
    SAVE_ROOT = os.path.join(os.path.expanduser('~'), 'Documents', 'html')
elif SAVE_ROOT == '':
    SAVE_ROOT = os.path.join(os.path.expanduser('~'), 'Documents', 'html')
else:
    SAVE_ROOT = os.path.join(SAVE_ROOT, 'html')

if not os.path.exists(SAVE_ROOT):
    os.makedirs(SAVE_ROOT)

SEED_HOSTNAME = urlparse(SEED_URL).netloc
