# Crawler-py
The web crawler with python

## Requirements
* [Python](https://www.python.org) v3.6 or greater
* [MongoDB](https://www.mongodb.com) v3.4 or greater

## Python Dependencies
* [Beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) v4.6.0
* [Pymongo](https://api.mongodb.com/python/current/) v3.5.0
* [Requests](http://docs.python-requests.org/en/master/) v2.18.4
* Termcolor v1.1.0

## Installation

1. Clone repository
```
$ git clone https://github.com/m00p1ng/crawler-py
```

2. Install python dependencies
```
$ cd crawler-py
$ pip install -r requirements.py
```

## How to run
```
$ cd crawler-py
$ python crawler_py
```

## Database Configuration

1. Create `db.json` in `crawler-py` folder and setting config

**Example**
```json
{
    "HOST": "localhost",
    "PORT": 27017
}
```

If your database has authentication add **`USERNAME`** and **`PASSWORD`**

**Example**
```json
{
    "HOST": "localhost",
    "PORT": 27017,
    "USERNAME": "admin",
    "PASSWORD": "admin"
}
```

## Crawler Settings

* **`DEBUG`** Il `True` will show more information on console
* **`SEED_URL`** root url for crawler
* **`LIMIT_SITE`** limit size of crawler site
* **`MAX_LEVEL`** limit level site for crawler (prevent crawler traps`)
* **`REQUEST_TIMEOUT`** request timeout for http request (second)
* **`SAVE_ROOT`** save crawler data path
* **`DATABASE_NAME`** name of database for store crawler infomation
