from abc import ABC, abstractmethod
from typing import List

from ..utils import Log

class Downloader(ABC):
    _logger = None

    def __init__(self):
        self._logger = Log().setup_logging(__name__)


    @abstractmethod
    def add_url(self, url: str):
        pass


    @abstractmethod # type: ignore[no-redef]
    def add_url(self, url: List[str]):
        pass

