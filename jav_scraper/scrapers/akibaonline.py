import re
from bs4 import BeautifulSoup
from typing import List, Tuple
from urllib import request

from ..models import Grab
from ..models import JAVQuality
from . import Scraper
from . import QualityMapper

class AkibaOnlineQualityMapper(QualityMapper):
    _regex_vr = r'.*(4096x2048|7680x3840|8192x4096).*'
    _regex_uncensored = r'^$'
    _regex_1080p = r'.*(1920x1080|1080p).*'
    _regex_4k = r'.*4096x2048.*'
    _regex_8k = r'.*(7680x3840|8192x4096).*'

class AkibaOnline(Scraper):
    name = "Akiba Online"
    _baseurl = "https://www.akiba-online.com"
    searchurl = _baseurl + "/search/1/?q=%s"
    _quality_mapper = AkibaOnlineQualityMapper

    def __init__(self):
        super(AkibaOnline, self).__init__()


    def search(self, jav_code: str) -> Grab:
        url = self.search_url(jav_code)
        if not url:
            return False

        grab = Grab()
        grab.download_page = url[0]
        grab.quality = url[1]
        grab.download_links = url[2]
        grab.state = 'pending'
        return grab


    def search_url(self, jav_code: str) -> Tuple[str, JAVQuality, list[str]]:
        self._logger.debug(f'Searching for {jav_code} with {self.name}')
        jav_code = jav_code.upper()

        url = self.searchurl.replace('%s', jav_code)
        research = request.urlopen(url).read()
        if not research:
            self._logger.debug(f'Could not read url: {url}')
            return
        soup = BeautifulSoup(research, 'html.parser')

        url = False
        dl_urls = []
        priority = 0
        for result in soup.select('h3.contentRow-title a'):
            if not '[' + jav_code + ']' in result.text:
                continue

            # Read posts to gather quality
            post = request.urlopen(self._baseurl + result.get('href')).read()
            for dl_url in BeautifulSoup(post, 'html.parser').select('div.bbWrapper a.link'):
                if not dl_url.text.startswith(jav_code):
                    continue

                quality = self.get_quality(dl_url.text)
                if not quality:
                    continue

                # Check if URL is alive
                if 'filejoker' in dl_url.get('href'):
                    filejoker_http = request.urlopen(request.Request(dl_url.get('href'), headers={'User-Agent': ''})).read()
                    if BeautifulSoup(filejoker_http, 'html.parser').select('div.not_found'):
                        self._logger.info(f'Found expired Filejoker link: {dl_url.get("href")}')
                        continue

                # Handling multipart files
                if re.match(r'.*\-([A-Z]|[1-9]+)\.(mp4|mkv)\ .*', dl_url.text):
                    if quality.priority > priority:
                        priority = quality.priority
                        dl_urls = [dl_url.get('href')]
                    elif quality.priority == priority:
                        dl_urls.append(dl_url.get('href'))
                # If release has better quality, retain it
                elif quality.priority > priority:
                    priority = quality.priority
                    dl_urls = [dl_url.get('href')]
                # Blacklist bad releases
                elif quality.priority < 0:
                    continue

            return url, quality, dl_urls

