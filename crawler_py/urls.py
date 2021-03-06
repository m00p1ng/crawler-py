'''
URL management module
'''

import os
import re
from collections import namedtuple
from urllib.parse import urlparse, quote, unquote
from .settings import IGNORE_WORD_LIST, SEED_HOSTNAME


SplitResult = namedtuple('SplitResult', ['hostname', 'resource'])
FilePath = namedtuple('FilePath', ['path', 'filename'])


def fill_http_prefix(scheme, url):
    '''
    Fill http prefix if doesn't exist

    Parameter:
        url (string): raw URL
    Return:
        (string): URL with http prefix
    '''
    if not re.match(r'^https?://', url):
        return f'{scheme}://{url}'
    return url


def remove_www_prefix(url):
    '''
    Remove www prefix from URL

    Parameter:
        url (string): raw URL
    Return:
        (string): URL with no www prefix
    '''
    result = re.match(r'(www\.)(.*)', url)
    if result:
        return result.group(2)
    return url


def is_relative_path(url):
    '''
    Check URL is relative path

    Parameter:
        url (string) : raw URL
    Return:
        (bool) : if relative path return True
    '''
    url_parse = urlparse(url)
    return not bool(url_parse.netloc)


def split_url(url):
    '''
    http://<hostname>/<resource>

    Parameter:
        url (string): raw URL
    Return:
        (SplitResult): tuple with hostname and resource
        example:
            SplitResult(hostname="example.com", resource="/dir1")
    '''
    url_parse = urlparse(url)
    hostname = url_parse.netloc

    resource = url_parse.path
    resource = join_modifier_url(resource, url_parse)

    return SplitResult(hostname=hostname, resource=resource)


def join_modifier_url(source, url_parse):
    '''
    Join modifier URL into filename

    Parameters:
        source (string): source filename
        url_parse (ParseResult): URL that is parse
    Return:
        (string): filename with modifier
    '''
    result = source
    if url_parse.params:
        result += f';{url_parse.params}'
    if url_parse.query:
        result += f'?{url_parse.query}'
    if url_parse.fragment:
        result += f'#{url_parse.fragment}'
    return result


def url_to_path(url):
    '''
    Convert URL to filepath

    Parameter:
        url (string): raw URL
    Return:
        (FilePath) : tuple of FilePath
        example:
            FilePath(path="/root/path/dir", finename="index.html")
    '''
    url_parse = urlparse(url)

    if url_parse.path in ['/', '']:
        # if resource is root path
        filename = join_modifier_url('index.html', url_parse)
        path = ''
    elif url_parse.path and url_parse.path[-1] == '/':
        # if resouce end with '/'
        filename = join_modifier_url('index.html', url_parse)
        path = url_parse.path.rstrip('/').split('/')
        path = os.path.join(*path)
    else:
        filename = url_parse.path.split('/')[-1]
        filename = join_modifier_url(filename, url_parse)
        path = url_parse.path.split('/')[:-1]
        path = os.path.join(*path)

    return FilePath(path=path, filename=filename)


def is_ignore_link(url):
    pattern = '(' + '|'.join(IGNORE_WORD_LIST) + ')'
    result = re.search(pattern, split_url(url).resource, re.IGNORECASE)
    if result:
        return True, result.group(1)
    return False, None


def is_under_seed_root(url):
    hostname = urlparse(url).netloc
    pattern = f'(.*[.]{SEED_HOSTNAME}$)|(^{SEED_HOSTNAME}$)'
    result = re.match(pattern, hostname)
    return result


def url_encode(url):
    return quote(url, safe=":=&?/'\"")


def is_redirect(req_url, res_url):
    req_split = split_url(req_url.strip('/'))
    res_split = split_url(res_url.strip('/'))

    req_hostname = remove_www_prefix(req_split.hostname)
    res_hostname = remove_www_prefix(res_split.hostname)

    req_resource = unquote(req_split.resource)
    res_resource = unquote(res_split.resource)

    return req_hostname != res_hostname or req_resource != res_resource
