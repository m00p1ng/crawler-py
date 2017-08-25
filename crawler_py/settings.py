import os

SAVE_ROOT = ''

DATABASE_CONFIG_PATH = os.path.realpath('db.json')

DATABASE_NAME = 'crawler-py'

HEADER = {
    "User-agent": "m00p1ng130t",
}

EXTRACT_EXTENSIONS = [
    ".htm", ".html", ".xml", ".php", ".asp"
]

if 'SAVE_ROOT' not in globals() or SAVE_ROOT == '':
    SAVE_ROOT = os.path.join(os.path.expanduser('~'), 'Documents', 'html')
else:
    SAVE_ROOT = os.path.join(SAVE_ROOT, 'html')

if not os.path.exists(SAVE_ROOT):
    os.makedirs(SAVE_ROOT)
