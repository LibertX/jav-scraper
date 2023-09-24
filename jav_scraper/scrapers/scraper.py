from abc import ABC, abstractmethod

from ..utils import Log

class Scraper(ABC):
    _logger = None

    @abstractmethod
    def search(self, jav_code):
        pass

    @abstractmethod
    def get_download_link(self, url):
        pass

    @property
    @abstractmethod
    def name():
        pass

    @property
    @abstractmethod
    def searchurl(self):
        pass

    def __init__(self):
        self._logger = Log().setup_logging(__name__)

