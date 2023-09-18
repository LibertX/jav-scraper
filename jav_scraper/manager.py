import threading
from time import sleep

from . import scrapers
from . import models
from . import utils
from . import app
from . import db

class Manager(threading.Thread):
    _logger = None

    def __init__(self):
        threading.Thread.__init__(self)
        self._logger = utils.Log().setup_logging(__name__)

    def run(self):
        while True:
            with app.app_context():
                pending_movies = models.JAVMovie.query.filter_by(status='pending').all()
                for movie in pending_movies:
                    for scraper in scrapers.Scraper.__subclasses__():
                        grab = scraper().search(movie.code)
                        if grab:
                            self._logger.info(f'Found movie {movie.code}')
                            movie.grabs += [grab]
                            movie.status = 'done'
                            db.session.add(movie)
                            db.session.commit()
                            # TODO JDownloader add
                            break

            self._logger.info("All movies processed, sleeping...")
            e = threading.Event()
            e.wait(timeout=60)
