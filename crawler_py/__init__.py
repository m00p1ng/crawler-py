from .database import connect as db_connect, DB_CONFIG_PATH

def print_header():
    print("=================================")
    print("=                               =")
    print("=          m00p1ng130t          =")
    print("=                               =")
    print("=================================")
    print()

def main():
    print_header()
    db_connect()
