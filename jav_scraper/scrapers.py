import collections
from abc import abstractmethod
from .flaresolverr import Flaresolverr
from bs4 import BeautifulSoup

class Scraper(object):
    def __init__(self):
        raise TypeError("Cannot instantiate Scraper classes")

    @abstractmethod
    def search(self, jav_code):
        pass

    @property
    @abstractmethod
    def NAME():
        pass

    @property
    @abstractmethod
    def SEARCH_URL():
        pass

    def get_name(self):
        return self.NAME

    def get_scrapers():
        return Scraper.__subclasses__()

class MaxJAV(Scraper):
    NAME="MaxJAV"
    SEARCH_URL="https://maxjav.com/?s=%s"
    driver = None

    def __init__(self):
        pass

    def search(self, jav_code):
        flaresolverr = Flaresolverr()
        research = flaresolverr.read_url_and_retry(self.SEARCH_URL.replace('%s', jav_code))
        soup = BeautifulSoup(research, 'html.parser')

        priority = None
        url = False
        for result in soup.select('div#wrapper h2.title a'):
            # Exclude invalid items
            if not (result.text.startswith(jav_code) or ' ' + jav_code in result.text):
                continue

            # Prioritize 8K in VR
            if result.text.endswith(' – VR'):
                if result.text.startswith('[8K] '):
                    return result.get('href')
                else:
                    url = result.get('href')

            # Exclude 4K releases
            if result.text.endswith(' – 4K'):
                continue

            if result.text.endswith(' – UMR'):
                return result.get('href')

            url = result.get('href')

        return url
