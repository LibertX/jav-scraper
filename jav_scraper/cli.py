#!/usr/bin/python3

from . import log, scrapers
import sys
import argparse

logger = log.setup_logging(__name__)

def main():
    parser = argparse.ArgumentParser(description='JAV Scraper')
    parser.add_argument('--search', dest='search', action='store', help='Search single JAV Movie download link')
    args = parser.parse_args()

    if args.search:
        for scraper in scrapers.Scraper.__subclasses__():
            print(scraper().search(args.search))

if __name__ == "__main__":
    main()
