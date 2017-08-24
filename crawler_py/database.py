import sys
import os
import json
from pymongo import MongoClient, errors
from .utils import print_log

DB_CONFIG_PATH = os.path.realpath('db.json')

try:
    with open(DB_CONFIG_PATH, 'r') as file:
        MONGO = json.loads(file.read())

    print_log("Connecting to database...")
    client = MongoClient(MONGO['HOST'], MONGO['PORT'])

    client.server_info()

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


class _DB:
    def __init__(self, collection):
        self.db = db[collection]

    def insert(self, data):
        return self.db.insert(data)

    def find(self, find_params={}, return_field=None, limit=0):
        return self.db.find(find_params, return_field).limit(limit)

    def find_one(self, find_params={}, return_field=None):
        return self.db.find_one(find_params, return_field)


queue = _DB('queue_links')
content = _DB('content_info')
disallow_links = _DB('disallow_links')
