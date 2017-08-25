import os
from collections import namedtuple

from .settings import SAVE_ROOT, EXTRACT_EXTENSIONS
from .utils import join_modifier_url


def save(url_parse, content):
    filepath = _parse_to_path(url_parse)
    save_path = os.path.join(SAVE_ROOT, url_parse.netloc, filepath.path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_save_path = os.path.join(save_path, filepath.filename)

    if _check_extension(filepath.filename):
        mode = 'w'
    else:
        mode = 'wb'

    with open(file_save_path, mode) as file:
        file.write(content)


def _parse_to_path(url_parse):
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

def _check_extension(filename):
    extension = os.path.splitext(filename)[1]
    if extension in EXTRACT_EXTENSIONS or extension is '':
        return True
    else:
        return False