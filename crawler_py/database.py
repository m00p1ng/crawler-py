import os
import json
from pymongo import MongoClient, errors

from .utils import print_log
from .settings import DB_CONFIG_PATH


class Database:
    queue = None
    content = None
    disallow_links = None
    _client = None

    @classmethod
    def connect(cls):
        try:
            with open(DB_CONFIG_PATH, 'r') as file:
                MONGO = json.loads(file.read())

            print_log("Connecting to database...")
            cls._client = MongoClient(MONGO['HOST'], MONGO['PORT'])
            cls._client.server_info()

            db = cls._client[MONGO['DATABASE']]
            if 'USERNAME' in MONGO and 'PASSWORD' in MONGO:
                db.authenticate(MONGO['USERNAME'], MONGO['PASSWORD'])

            print_log("Connection successful")
            cls._create_collection(db)

            return db

        except FileNotFoundError:
            print_log(
                f"Database config not exists on `{DB_CONFIG_PATH}`", 'red')
            exit(1)
        except errors.ServerSelectionTimeoutError:
            print_log("Connection Timeout. Please Try again", 'red')
            exit(1)

    @classmethod
    def _create_collection(cls, db):
        cls.queue = _Collection(db, 'queue_links')
        cls.content = _Collection(db, 'content_info')
        cls.disallow_links = _Collection(db, 'disallow_links')

    @classmethod
    def disconnect(cls):
        if cls._client is not None:
            return cls._client.close()
        else:
            return None


class _Collection:
    def __init__(self, db, name):
        self.db = db[name]

    def insert(self, data):
        return self.db.insert(data)

    def find(self, find_params={}, return_field=None, limit=0):
        return self.db.find(find_params, return_field).limit(limit)

    def find_one(self, find_params={}, return_field=None):
        return self.db.find_one(find_params, return_field)
