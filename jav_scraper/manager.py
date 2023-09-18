import threading
from time import sleep
from sqlalchemy import select

from . import scrapers
from . import models
from . import utils

class Manager(threading.Thread):
    _logger = None

    def __init__(self):
        threading.Thread.__init__(self)
        self._logger = utils.Log().setup_logging(__name__)

    def run(self):
        while True:
            pending_movies = select(models.JAVMovie).where(models.JAVMovie.status == 'pending')
            for movie in pending_movies:
                for scraper in scrapers.Scraper.__subclasses__():
                    grab = scraper().search(movie.code)
                    if grab:
                        self._logger.info(f'Found movie {movie.code}')
                        movie.grabs += grab
                        movie.status = 'done'
                        # TODO JDownloader add
                        break

            self._logger.debug("All movies processed, sleeping...")
            sleep(60)
