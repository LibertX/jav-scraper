import collections
import undetected_chromedriver as uc
from abc import abstractmethod

class Scraper(object):
    def __init__(self):
        raise TypeError("Cannot instantiate Scraper classes")

    @abstractmethod
    def search(self, jav_code):
        pass

    @property
    @abstractmethod
    def NAME():
        pass

    @property
    @abstractmethod
    def SEARCH_URL():
        pass

    def get_name(self):
        return self.NAME

    def get_scrapers():
        return Scraper.__subclasses__()

    def init_driver(self):
        if not self.driver:
            self.driver = uc.Chrome(headless=True, use_subprocess=False)

class MaxJAV(Scraper):
    NAME="MaxJAV"
    SEARCH_URL="https://maxjav.com/?s=%s"
    driver = None

    def __init__(self):
        pass

    def search(self, jav_code):
        self.init_driver()
        self.driver.get(self.SEARCH_URL.replace('%s', jav_code))
        print(self.driver.page_source)
