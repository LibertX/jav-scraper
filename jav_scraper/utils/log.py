import logging
import sys
from typing import Optional

from .singleton import Singleton

class Log(metaclass = Singleton):
    _level: int = logging.INFO


    def setup_logging(self, name: Optional[str]=None) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level=self._level)

        if not logger.hasHandlers():
            stream = logging.StreamHandler(sys.stdout)
            stream.setFormatter(self.CustomFormatter())
            logger.addHandler(stream)

        return logger


    def enable_debug(self) -> None:
        self._level = logging.DEBUG
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).setLevel(self._level)


    class CustomFormatter(logging.Formatter):
        grey: str = "\x1b[38;20m"
        yellow: str = "\x1b[33;20m"
        red: str = "\x1b[31;20m"
        bold_red: str = "\x1b[31;1m"
        reset: str = "\x1b[0m"
        log_format: str = "[%(name)s] %(levelname)s - %(message)s"

        FORMATS = {
            logging.DEBUG: grey + log_format + reset,
            logging.INFO: grey + log_format + reset,
            logging.WARNING: yellow + log_format + reset,
            logging.ERROR: red + log_format + reset,
            logging.CRITICAL: bold_red + log_format + reset
        }

        def format(self, record: logging.LogRecord) -> str:
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)
