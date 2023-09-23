from abc import ABC, abstractmethod

class Downloader(ABC):
    @abstractmethod
    def add_url(self, url):
        pass
