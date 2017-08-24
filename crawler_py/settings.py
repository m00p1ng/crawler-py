import os

# user agent for bot crawler
SAVE_ROOT = ''

DB_CONFIG_PATH = os.path.realpath('db.json')

HEADER = {
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
    ".htm", ".html", ".xml", ".php", ".asp"
]

if 'SAVE_PATH' not in globals() or SAVE_ROOT == '':
    SAVE_ROOT = os.path.join(os.path.expanduser('~'), 'Documents', 'html')
else:
    SAVE_ROOT = os.path.join(SAVE_ROOT, 'html')

if not os.path.exists(SAVE_ROOT):
    os.makedirs(SAVE_ROOT)