'''
Database module

Database schema
--------------------
 Collection: queue
 :attribute
    * scheme
    * hostname
    * resource
    * visited

--------------------
 Collection: content
 :attribute
    * hostname
    * resource
    * is_duplicated
    * timestamp
    * hash

--------------------
 Collection: disallow_link
 :attribute
    * hostname
    * resource

--------------------
 Collection: host_info
 :attribute
    * hostname
    * ip_addr
    * has_robots
    * downloaded_robots

--------------------
 Collection: crawler_state
 :attribute
    * link_count

--------------------
'''
import os
import json
from datetime import datetime
from pymongo import MongoClient, errors

from .utils import print_log
from .urls import split_url
from .settings import DATABASE_CONFIG_PATH


class Database:
    ''' Database model '''
    queue = None
    content = None
    disallow_links = None
    host_info = None
    crawler_state = None
    error_log = None
    _client = None

    @classmethod
    def connect(cls, db_name):
        try:
            print_log("Connecting to database...")
            db = cls._connect(db_name)

            print_log("Connection successful")
            cls._create_collection(db)

            return db

        except errors.ServerSelectionTimeoutError:
            print_log("Connection Timeout. Please Try again", 'red')
            exit(1)

    @classmethod
    def _connect(cls, db_name):
        if not os.path.exists(DATABASE_CONFIG_PATH):
            mongo = {}
            mongo['HOST'] = 'localhost'
            mongo['PORT'] = 27017
        else:
            with open(DATABASE_CONFIG_PATH, 'r') as file:
                mongo = json.loads(file.read())

        cls._client = MongoClient(mongo['HOST'], mongo['PORT'])
        cls._client.server_info()

        db = cls._client[db_name]
        if 'USERNAME' in mongo and 'PASSWORD' in mongo:
            db.authenticate(mongo['USERNAME'], mongo['PASSWORD'])

        return db

    @classmethod
    def _create_collection(cls, db):
        cls.queue = _Queue(db, 'queue_links')
        cls.content = _Collection(db, 'content_info')
        cls.disallow_links = _Collection(db, 'disallow_links')
        cls.host_info = _Collection(db, 'host_info')
        cls.error_log = _ErrorLog(db, 'error_log')
        cls.crawler_state = _CrawlerState(db, 'crawler_state')

    @classmethod
    def disconnect(cls):
        if cls._client is not None:
            return cls._client.close()
        else:
            return None


class _Collection:
    def __init__(self, db, collection_name):
        self.collection = db[collection_name]

    def insert_one(self, data):
        '''Override insert_one method from pymongo'''
        return self.collection.insert_one(data)

    def insert_many(self, data):
        '''Override insert_manyy method from pymongo'''
        return self.collection.insert_many(data)

    def find(self, find_params=None, return_field=None, limit=0):
        '''Override find method from pymongo'''
        return self.collection.find(find_params, return_field).limit(limit)

    def find_one(self, find_params=None, return_field=None):
        '''Override find_one method from pymongo'''
        return self.collection.find_one(find_params, return_field)

    def update_one(self, find_params, update):
        '''Override update_one method from pymongo'''
        return self.collection.update_one(find_params, update)

    def count(self):
        '''Override count method from pymongo'''
        return self.collection.count()


class _CrawlerState(_Collection):
    def __init__(self, db, collection_name):
        super().__init__(db, collection_name)
        self.init_link_counter()

    def init_link_counter(self):
        if self.collection.count() == 0:
            self.collection.insert_one({
                "link_counter": 0
            })

    def update_link_counter(self):
        self.collection.update_one(
            {'_id': self.link_counter_id},
            {'$inc': {'link_counter': 1}}
        )

    @property
    def link_counter(self):
        return int(self.collection.find_one()['link_counter'])

    @property
    def link_counter_id(self):
        return self.collection.find_one()['_id']


class _Queue(_Collection):
    def __init__(self, db, collection_name):
        super().__init__(db, collection_name)

    def update_visited_link(self, url):
        url_split = split_url(url)

        self.collection.update_many(
            {'hostname': url_split.hostname, 'resource': url_split.resource},
            {'$set': {'visited': True}}
        )


class _ErrorLog(_Collection):
    def __init__(self, db, collection_name):
        super().__init__(db, collection_name)

    def add_log(self, url, reason):
        url_split = split_url(url)
        self.collection.insert_one({
            "hostname": url_split.hostname,
            "resource": url_split.resource,
            "reason": reason,
            "timestamp": datetime.now(),
        })
