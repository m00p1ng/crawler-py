import json
from pymongo import MongoClient, errors

from .utils import print_log, split_url
from .settings import DATABASE_CONFIG_PATH


class Database:
    '''
    --------------------
     Collection: queue
     :attribute
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
            with open(DATABASE_CONFIG_PATH, 'r') as file:
                MONGO = json.loads(file.read())

            print_log("Connecting to database...")
            cls._client = MongoClient(MONGO['HOST'], MONGO['PORT'])
            cls._client.server_info()

            db = cls._client[db_name]
            if 'USERNAME' in MONGO and 'PASSWORD' in MONGO:
                db.authenticate(MONGO['USERNAME'], MONGO['PASSWORD'])

            print_log("Connection successful")
            cls._create_collection(db)

            return db

        except FileNotFoundError:
            print_log(
                f"Database config not exists on `{DATABASE_CONFIG_PATH}`", 'red')
            exit(1)
        except errors.ServerSelectionTimeoutError:
            print_log("Connection Timeout. Please Try again", 'red')
            exit(1)

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
        return self.collection.insert_one(data)

    def insert_many(self, data):
        return self.collection.insert_many(data)

    def find(self, find_params=None, return_field=None, limit=0):
        return self.collection.find(find_params, return_field).limit(limit)

    def find_one(self, find_params=None, return_field=None):
        return self.collection.find_one(find_params, return_field)

    def update_one(self, find_params, update):
        return self.collection.update_one(find_params, update)

    def count(self):
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
        return self.collection.find_one()['link_counter']

    @property
    def link_counter_id(self):
        return self.collection.find_one()['_id']


class _Queue(_Collection):
    def __init__(self, db, collection_name):
        super().__init__(db, collection_name)

    def update_visited_link(self, url):
        url_split = split_url(url)

        self.collection.update_one(
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
        })