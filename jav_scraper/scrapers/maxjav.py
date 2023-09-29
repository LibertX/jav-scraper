import re
from bs4 import BeautifulSoup

from ..utils import Flaresolverr
from ..models import Grab
from . import Scraper
from . import QualityMapper


class MaxJAVQualityMapper(QualityMapper):
    _regex_vr = r'.*[–-](\ Uncensored)?\ VR$'
    _regex_uncensored = r'.*([–-] ?UMR$|\ Uncensored\ ).*'
    _regex_1080p = r'.*[–-] ?(UMR|HD)$'
    _regex_4k = r'.*\b4K$'
    _regex_8k = r'^\[8K\]\ .*'


class MaxJAV(Scraper):
    name = "MaxJAV"
    searchurl = "https://maxjav.com/?s=%s"
    _quality_mapper = MaxJAVQualityMapper

    def __init__(self):
        super(MaxJAV, self).__init__()


    def search(self, jav_code):
        url = self.search_url(jav_code)
        if not url:
            return False

        grab = Grab()
        grab.download_page = url[0]
        grab.quality = url[1]
        grab.download_links = self.get_download_link(url[0])
        grab.state = 'pending'
        return grab


    def search_url(self, jav_code):
        self._logger.debug(f'Searching for {jav_code} with MaxJAV')
        jav_code = jav_code.upper()
        flaresolverr = Flaresolverr()

        url = self.searchurl.replace('%s', jav_code)
        research = flaresolverr.read_url_and_retry(url)
        if not research:
            self._logger.debug(f'Could not read url: {url}')
            return
        soup = BeautifulSoup(research, 'html.parser')


        url = False
        priority = 0
        for result in soup.select('div#wrapper h2.title a'):
            # Exclude invalid items
            if not re.match('^(\[.*\] )?' + jav_code + '\ ', result.text):
                continue

            quality = self.get_quality(result.text)
            if not quality:
                continue

            # If release has better quality, retain it
            if quality.priority > priority:
                priority = quality.priority
                url = result.get('href')
            # Blacklist bad releases
            elif quality.priority < 0:
                continue

            # If release is top quality, return immediatly
            if priority >= 100:
                break

        return url, quality


    def get_download_link(self, dl_url):
        return_url = []
        flaresolverr = Flaresolverr()
        research = flaresolverr.read_url_and_retry(dl_url)
        if not research:
            self._logger.debug(f'Could not read url: {dl_url}')
            return
        soup = BeautifulSoup(research, 'html.parser')
        entries = soup.select('div#content div.post div.entry p')

        for i in range(1,len(entries)):
            for url in entries[i].select('a'):
                return_url += [url.get('href')]

            if return_url:
                return return_url

        return False

