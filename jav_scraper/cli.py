#!/usr/bin/python3

import argparse

from . import scrapers
from . import utils
from . import app

logger = utils.Log().setup_logging(__name__)

def main():
    parser = argparse.ArgumentParser(description='JAV Scraper')
    parser.add_argument('--search', dest='search', action='store', help='Search single JAV Movie download link')
    args = parser.parse_args()

    if args.search:
        with app.app_context():
            for scraper in scrapers.Scraper.__subclasses__():
                if scraper().__class__.__name__ == 'AkibaOnline':
                    print(scraper().search(args.search).download_links)

if __name__ == "__main__":
    main()
