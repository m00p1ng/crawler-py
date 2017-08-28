import os
from urllib.parse import urlparse

from .settings import SAVE_ROOT
from .utils import url_to_path, check_extension, join_modifier_url, remove_www_prefix


def save(url, content):
    url_parse = urlparse(url)
    filepath = url_to_path(url)
    hostname = remove_www_prefix(url_parse.netloc)
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


def _check_filepath_exist(save_path, pure_filename, url_parse):
    save_filename = join_modifier_url(pure_filename, url_parse)
    save_filename = save_filename.replace('/', '-')

    file_save_path = os.path.join(save_path, save_filename)
    if os.path.exists(file_save_path) and os.path.isdir(file_save_path):
        return os.path.join(file_save_path, 'index.html')
    return file_save_path


def _create_dir_name(save_path):
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        elif not os.path.isdir(save_path):
            # dirname = os.path.dirname(save_path)
            # _move_index_to_folder(dirname)
            _move_index_to_folder(save_path)
    except NotADirectoryError:
        paths = save_path.replace(SAVE_ROOT, '')
        paths = paths.split('/')[1:]
        _check_filename_dir(paths, -1)


def _check_filename_dir(paths, i):
    if i < -1:
        path = os.path.join(SAVE_ROOT, *paths[0: i + 1])
    else:
        path = os.path.join(SAVE_ROOT, *paths)

    if os.path.exists(path) and not os.path.isdir(path):
        _move_index_to_folder(path)
        os.makedirs(os.path.join(SAVE_ROOT, *path))
    else:
        _check_filename_dir(paths, i - 1)


def _move_index_to_folder(path):
    temp_index_file = os.path.join(os.path.dirname(path), 'temp.index.html')
    os.rename(path, temp_index_file)
    os.makedirs(path)

    dest = os.path.join(path, 'index.html')
    os.rename(temp_index_file, dest)
