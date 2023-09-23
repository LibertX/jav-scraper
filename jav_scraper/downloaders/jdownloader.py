import myjdapi
import os

from . import Downloader
from ..utils import MissingEnvironmentException

class JDownloader(Downloader):
    _jdownloader = None

    def __init__(self):
        username = os.environ.get('JD_USERNAME')
        password = os.environ.get('JD_PASSWORD')
        device = os.environ.get('JD_DEVICE')

        if not (username and password and device):
            raise MissingEnvironmentException("Missing JDownloader configuration")

        jd = myjdapi.jdapi()
        jd.connect(username, password)
        self._jdownloader = jd.getDevice(name=device)

        return True

    def add_url(self, url):
        pass
