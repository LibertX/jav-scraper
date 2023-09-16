import collections
import re
from abc import abstractmethod
from .flaresolverr import Flaresolverr
from bs4 import BeautifulSoup

class Scraper(object):
    def __init__(self):
        raise TypeError("Cannot instantiate Scraper classes")

    @abstractmethod
    def search(self, jav_code):
        pass

    @abstractmethod
    def get_download_link(self, url):
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

    def __init__(self):
        pass

    def search(self, jav_code):
        url = self.search_url(jav_code)
        if not url:
            return False

        return self.get_download_link(url)

    def search_url(self, jav_code):
        jav_code = jav_code.upper()
        flaresolverr = Flaresolverr()
        research = flaresolverr.read_url_and_retry(self.SEARCH_URL.replace('%s', jav_code))
        soup = BeautifulSoup(research, 'html.parser')


        url = False
        for result in soup.select('div#wrapper h2.title a'):
            # Exclude invalid items
            if not re.search('^(\[.*\] )?' + jav_code + '\ ', result.text):
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

    def get_download_link(self, dl_url):
        return_url = []
        flaresolverr = Flaresolverr()
        research = flaresolverr.read_url_and_retry(dl_url)
        soup = BeautifulSoup(research, 'html.parser')
        entries = soup.select('div#content div.post div.entry p')
        for url in entries[1].select('a'):
            if '.8K.' in url.text:
                return_url += [url.get('href')]

        if len(return_url):
            return return_url

        for i in range(len(entries)):
            for url in entries[-i].select('a'):
                return_url += [url.get('href')]

            if len(return_url):
                return return_url

        return False
