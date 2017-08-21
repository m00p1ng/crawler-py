import sys
import os
import json
from pymongo import MongoClient, errors
from .utils import print_log

DB_CONFIG_PATH = os.path.realpath('db.json')
db = None

def connect():
    try:
        with open(DB_CONFIG_PATH, 'r') as file:
            MONGO = json.loads(file.read())

        print_log("Connecting to database...")
        client = MongoClient(MONGO['HOST'], MONGO['PORT'])

        client.server_info()

        global db
        db = client[MONGO['DATABASE']]

        if 'USERNAME' in MONGO and 'PASSWORD' in MONGO:
            db.authenticate(MONGO['USERNAME'], MONGO['PASSWORD'])

        print_log("Connection successful")

    except FileNotFoundError:
        print_log(f"Database config not exists on `{DB_CONFIG_PATH}`", 'red')
        exit(1)
    except errors.ServerSelectionTimeoutError:
        print_log("Connection Timeout. Please Try again", 'red')
        exit(1)
