import sys
import time

from .utils import print_log
from .urls import fill_http_prefix, is_redirect, url_encode
from .database import Database as db
from .settings import DATABASE_NAME, LIMIT_SITE, DELAY_FETCH

from .analyzer import Analyzer
from .downloader import Fetcher
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
    try:
        schedule = Scheduler()
        link_counter = db.crawler_state.link_counter

        while link_counter < LIMIT_SITE - 1 and schedule.queue_size > 0:
            link_counter = db.crawler_state.link_counter
            url = schedule.get_url()

            content = None
            real_url = None
            fetch = Fetcher(url).get_content()
            if fetch:
                content, real_url = fetch

            if real_url and is_redirect(url, real_url):
                print_log(f"==> Redirect to {real_url}", 'yellow')

            if content is not None:
                analyzer = Analyzer(url, content)
                urls, is_duplicated = analyzer.start()

                if not is_duplicated:
                    schedule.add(urls)
                    db.crawler_state.update_link_counter()

            db.queue.update_visited_link(url)

            time.sleep(DELAY_FETCH)
            print()

        print_log("Finish crawler", 'green')

    except PermissionError:
        print()
        print_log("PermissionError: will try again", 'red')
        print()
        crawler()
