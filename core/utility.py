# _*_ coding: utf-8 _*_

"""
utility functions
"""

import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name, interval=1, backup=60, level=logging.WARNING):
    """
    get logger instance of TimedRotatingFileHandler
    """
    # define handler
    handler = TimedRotatingFileHandler(name, when="MIDNIGHT", interval=interval, backupCount=backup)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(filename)s: %(message)s"))

    # define logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # return
    return logger
