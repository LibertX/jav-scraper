import myjdapi
import os
from multipledispatch import dispatch

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


    @dispatch(str)
    def add_url(self, url):
        self._logger.debug(f'Adding {url} to JDownloader...')
        self._jdownloader.linkgrabber.add_links([{'autostart': True, 'links': url}])
        return True


    @dispatch(list)
    def add_url(self, url):
        self._logger.debug(f'Adding {url} in list mode')
        return self.add_url(','.join(url))
