from .database import connect as db_connect

def print_header():
    print("===================================")
    print("=           m00p1ng130t           =")
    print("=                                 =")
    print("=       By. mooping eiei  :)      =")
    print("===================================")
    print()

def main():
    print_header()
    db_connect()
