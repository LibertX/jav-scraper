import threading
from sqlalchemy import func

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
                pending_movies = db.session.query(models.JAVMovie).filter(~models.JAVMovie.id.in_(db.session.query(models.Grab.javmovie_id))).all()
                pending_movies_upgrades = db.session.query(models.JAVMovie, models.JAVQuality, models.Grab).filter(models.Grab.javmovie_id == models.JAVMovie.id, models.JAVQuality.id == models.Grab.quality_id).group_by(models.JAVMovie).having(func.max(models.JAVQuality.priority) < 100).all()
                pending_movies += [item[0] for item in pending_movies_upgrades]

                for movie in pending_movies:
                    self._logger.info(f'Searching for movie {movie.code}')
                    for scraper in scrapers.Scraper.__subclasses__():
                        grab = scraper().search(movie.code)
                        if grab:
                            # Check if existing quality is better
                            existing_priority = db.session.query(func.max(models.JAVQuality.priority)).filter(models.Grab.javmovie_id == movie.id).filter(models.Grab.quality_id == models.JAVQuality.id).scalar()
                            if existing_priority and grab.quality.priority <= existing_priority:
                                self._logger.debug(f'Existing quality has equal or lower priority ({existing_priority}) than existing ({grab.quality.priority}), skipping.')
                                continue

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
