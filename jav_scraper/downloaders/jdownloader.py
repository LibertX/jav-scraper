import myjdapi # type: ignore
import os
from multimethod import multimethod
from typing import List

from . import Downloader
from ..utils import MissingEnvironmentException

class JDownloader(Downloader):
    _jdownloader = None

    def __init__(self):
        super(JDownloader, self).__init__()
        try:
            username = os.environ['JD_USERNAME']
            password = os.environ['JD_PASSWORD']
            device = os.environ['JD_DEVICE']
        except Exception:
            self._logger.error('Missing JDownloader environment configuration')
            raise MissingEnvironmentException("Missing JDownloader configuration")

        jd = myjdapi.Myjdapi()
        jd.connect(username, password)
        self._jdownloader = jd.get_device(device)
        self._logger.debug('JDownloader downloader initialized')


    @multimethod
    def add_url(self, url: str) -> bool:
        self._logger.debug(f'Adding {url} to JDownloader...')
        self._jdownloader.linkgrabber.add_links([{'autostart': True, 'links': url}])
        return True


    @multimethod
    def add_url(self, url: List[str]) -> bool:
        return self.add_url(','.join(url))
