#!/usr/bin/python3

from . import log, scrapers
import argparse

logger = log.setup_logging(__name__)

def main():
    parser = argparse.ArgumentParser(description='JAV Scraper')
    parser.add_argument('--search', dest='search', action='store', help='Search single JAV Movie download link')
    args = parser.parse_args()

    if args.search:
        for scraper_class in scrapers.Scraper.get_scrapers():
            scraper = scraper_class()
            print(scraper.search(args.search))

if __name__ == "__main__":
    main()
