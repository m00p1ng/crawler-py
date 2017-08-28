import sys
import time

from .utils import print_log, fill_http_prefix
from .database import Database as db
from .settings import DATABASE_NAME, LIMIT_SITE, DELAY_FETCH

from .analyzer import Analyzer
from .downloader import Downloader
from .scheduler import Scheduler


def print_header():
    print_log("===================================")
    print_log("=           m00p1ng130t           =")
    print_log("=                                 =")
    print_log("=        By mooping eiei :)       =")
    print_log("===================================")
    print()


def main():
    if sys.version_info >= (3, 6):
        print_header()
    else:
        print_log("Please upgrade python to version 3.6 or greater", 'red')
        exit(1)

    db.connect(DATABASE_NAME)
    crawler()


def crawler():
    schedule = Scheduler()
    link_counter = db.crawler_state.link_counter

    while link_counter < LIMIT_SITE - 1 or schedule.size_queue() == 0:
        link_counter = db.crawler_state.link_counter
        url = schedule.get_url()

        if url is None:
            break

        downloader = Downloader(url)
        content = downloader.start()

        if content is not None:
            analyzer = Analyzer(url, content)
            urls = analyzer.start()

            schedule.add(urls)

        db.crawler_state.update_link_counter()
        db.queue.update_visited_link(url)

        time.sleep(DELAY_FETCH)
        print()

    print_log("Finish crawler", 'green')

