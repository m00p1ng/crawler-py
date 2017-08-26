import os
import re
from urllib.parse import urlparse

from .settings import SAVE_ROOT
from .utils import url_to_path, check_extension, join_modifier_url


def save(url, content):
    url_parse = urlparse(url)
    filepath = url_to_path(url)
    hostname = _remove_www(url_parse.netloc)
    save_path = os.path.join(SAVE_ROOT, hostname, filepath.path)

    _create_dir_name(save_path)

    pure_filename = url_parse.path.split('/')[-1]
    file_save_path = _check_filepath_exist(save_path, pure_filename, url_parse)

    if check_extension(pure_filename):
        mode = 'w'
    else:
        mode = 'wb'

    with open(file_save_path, mode) as file:
        file.write(content)


def _remove_www(url):
    result = re.match(r'(www\.)(.*)', url)
    if result:
        return result.group(2)
    return url

def _check_filepath_exist(save_path, pure_filename, url_parse):
    save_filename = join_modifier_url(pure_filename, url_parse)
    save_filename = save_filename.replace('/', '-')

    file_save_path = os.path.join(save_path, save_filename)
    if os.path.exists(file_save_path):
        return os.path.join(file_save_path, 'index.html')
    return file_save_path

def _create_dir_name(save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    elif not os.path.isdir(save_path):
        dirname = os.path.dirname(save_path)
        temp_index_file = os.path.join(dirname, 'temp.index.html')
        os.rename(save_path, temp_index_file)
        os.makedirs(save_path)

        dest = os.path.join(save_path, 'index.html')
        os.rename(temp_index_file, dest)