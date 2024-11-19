import logging
from logging.handlers import RotatingFileHandler
from .setting import logging_level


def get_logger(name):
    logging.basicConfig(level=logging_level, handlers=[
        # RotatingFileHandler(filename="chulalife.log",
        #                     maxBytes=1000000, backupCount=5)
    ])
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s] %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
