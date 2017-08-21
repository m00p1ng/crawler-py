from .database import connect as db_connect, DB_CONFIG_PATH

def print_header():
    print("===================================")
    print("=           m00ping130t           =")
    print("=                                 =")
    print("=       By. mooping eiei  :)      =")
    print("===================================")
    print()

def main():
    print_header()
    db_connect()
