from abc import ABC, abstractmethod

from ..utils import Log

class Downloader(ABC):
    _logger = None

    def __init__(self):
        self._logger = Log().setup_logging(__name__)


    @abstractmethod
    def add_url(self, url):
        pass
