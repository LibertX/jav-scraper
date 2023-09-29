import re
from abc import ABC, abstractmethod

from ..utils import Log
from ..models import JAVQuality

class Scraper(ABC):
    _logger = None

    @property
    @abstractmethod
    def _quality_mapper(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def searchurl(self):
        pass

    def __init__(self):
        self._logger = Log().setup_logging(__name__)

    @abstractmethod
    def search(self, jav_code):
        pass

    @abstractmethod
    def get_download_link(self, url):
        pass

    def get_quality(self, title):
        quality = self._quality_mapper().get_quality_from_title(title)
        if not quality:
            self._logger.warning(f'Could not get quality for title: {title}')
            return
        return quality


class QualityMapper(ABC):
    _logger = None

    @property
    @abstractmethod
    def _regex_vr(self):
        pass

    @property
    @abstractmethod
    def _regex_uncensored(self):
        pass

    @property
    @abstractmethod
    def _regex_1080p(self):
        pass

    @property
    @abstractmethod
    def _regex_4k(self):
        pass

    @property
    @abstractmethod
    def _regex_8k(self):
        pass

    def __init__(self):
        self._logger = Log().setup_logging(__name__)

    def get_quality_from_title(self, title):
        self._logger.debug(f'Evaluate quality for title: {title}')
        return JAVQuality.query.filter_by(
            vr = re.match(self._regex_vr, title) != None,
            uncensored = re.match(self._regex_uncensored, title) != None,
            def_1080p = re.match(self._regex_1080p, title) != None,
            def_4k = re.match(self._regex_4k, title) != None,
            def_8k = re.match(self._regex_8k, title) != None
        ).first()
