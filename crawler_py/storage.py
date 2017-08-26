import os
from collections import namedtuple

from .settings import SAVE_ROOT, EXTRACT_EXTENSIONS
from .utils import join_modifier_url, url_to_path, check_extension


def save(url_parse, content):
    filepath = url_to_path(url_parse)
    save_path = os.path.join(SAVE_ROOT, url_parse.netloc, filepath.path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_save_path = os.path.join(save_path, filepath.filename)

    if check_extension(filepath.filename):
        mode = 'w'
    else:
        mode = 'wb'

    with open(file_save_path, mode) as file:
        file.write(content)
