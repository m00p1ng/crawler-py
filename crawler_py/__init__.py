import sys

from .utils import print_log, fill_http_prefix
from .database import Database
from .settings import DATABASE_NAME, SEED_URL

from .analyzer import Analyzer
from .downloader import Downloader
from .scheduler import Scheduler


def print_header():
    print_log("===================================")
    print_log("=           m00p1ng130t           =")
    print_log("=                                 =")
    print_log("=        By mooping eiei :)       =")
    print_log("===================================")
    print()


def main():
    if sys.version_info >= (3, 6):
        print_header()
    else:
        print_log("Please upgrade python to version 3.6 or greater", 'red')
        exit(1)

    db = Database()
    db.connect(DATABASE_NAME)
    crawler()

def crawler():
    pass
