from abc import ABC, abstractmethod

class Scraper(ABC):
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

