import sys
from .utils import print_log


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
        from . import database
    else:
        print_log("Please upgrade your python to version 3.6 or greater", 'red')
