from .database import connect as db_connect
from .utils import print_log

def print_header():
    print_log("===================================")
    print_log("=           m00p1ng130t           =")
    print_log("=                                 =")
    print_log("=       By. mooping eiei  :)      =")
    print_log("===================================")
    print()

def main():
    print_header()
    db_connect()
