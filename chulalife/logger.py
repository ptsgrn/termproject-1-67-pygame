import logging
from .setting import logging_level


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s] %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
