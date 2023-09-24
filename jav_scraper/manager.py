import threading

from . import scrapers
from . import downloaders
from . import models
from . import utils
from . import app
from . import db
from .config import Config

class Manager(threading.Thread):
    _logger = None
    _downloader = None


    def __init__(self):
        threading.Thread.__init__(self)
        self._logger = utils.Log().setup_logging(__name__)

        if Config().DEBUG_MODE:
            utils.Log().enable_debug()
            self._logger.debug('Debug mode enabled')

        self.setup_downloader()


    def run(self):
        while True:
            self._logger.info('Processing movies...')
            with app.app_context():
                pending_movies = models.JAVMovie.query.all()
                for movie in pending_movies:
                    for scraper in scrapers.Scraper.__subclasses__():
                        self._logger.info(f'Searching for movie {movie.code}')
                        grab = scraper().search(movie.code)
                        if grab:
                            self._logger.info(f'Found movie {movie.code}')
                            movie.grabs += [grab]
                            db.session.add(movie)
                            db.session.commit()

                            try:
                                self._downloader.add_url(grab.download_links)
                                grab.state = 'done'
                                self._logger.info(f'Added {movie.code} to downloader')
                            except Exception:
                                grab.state = 'error'
                                self._logger.warning(f'Could not add {movie.code} to downloader')

                            db.session.add(movie)
                            db.session.commit()
                            break

            self._logger.info("All movies processed, sleeping...")
            e = threading.Event()
            e.wait(timeout=60)


    def setup_downloader(self):
        conf_downloader = Config().DOWNLOADER
        if not conf_downloader:
            self._logger.warning('Missing DOWNLOADER parameter, defaulting to JDownloader')
            conf_downloader = 'JDownloader'

        self._downloader = getattr(downloaders, conf_downloader)()
        return self._downloader
