import re
from bs4 import BeautifulSoup

from ..utils import Flaresolverr
from ..models import Grab
from . import Scraper

class MaxJAV(Scraper):
    name = "MaxJAV"
    searchurl = "https://maxjav.com/?s=%s"

    def __init__(self):
        super(MaxJAV, self).__init__()


    def search(self, jav_code):
        url = self.search_url(jav_code)
        if not url:
            return False

        grab = Grab()
        grab.download_page = url
        grab.download_links = self.get_download_link(url)
        grab.state = 'pending'
        return grab


    def search_url(self, jav_code):
        self._logger.debug(f'Searching for {jav_code} with MaxJAV')
        jav_code = jav_code.upper()
        flaresolverr = Flaresolverr()
        research = flaresolverr.read_url_and_retry(self.searchurl.replace('%s', jav_code))
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

        for i in range(1,len(entries)):
            for url in entries[i].select('a'):
                return_url += [url.get('href')]

            if return_url:
                return return_url

        return False
