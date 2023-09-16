import logging
import sys

log_level = logging.INFO


def setup_logging(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(level=log_level)

    if not logger.hasHandlers():
        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(CustomFormatter())
        logger.addHandler(stream)

    return logger


def enable_debug():
    global log_level
    log_level = logging.DEBUG

    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).setLevel(log_level)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(name)s] %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
