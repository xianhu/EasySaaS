# _*_ coding: utf-8 _*_

"""
utility functions
"""

import hashlib
import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name: str, interval: int = 1, backup: int = 60, level=logging.WARNING) -> logging.Logger:
    """
    get logger instance of TimedRotatingFileHandler
    """
    # define handler
    handler = TimedRotatingFileHandler(name, when="MIDNIGHT", interval=interval, backupCount=backup)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(filename)s: %(message)s"))

    # define logger
    logger = logging.getLogger(name)

    # set logger
    logger.setLevel(level)
    logger.addHandler(handler)

    # return
    return logger


def get_id_string(raw_string: str) -> str:
    """
    get id of string from raw string
    """
    encode = raw_string.encode()
    return hashlib.md5(encode).hexdigest()


def iter_file(file_path: str, chunk_size: int = 1024 * 1024) -> iter:
    """
    iter file, yield chunk
    """
    with open(file_path, "rb") as file_in:
        while chunk := file_in.read(chunk_size):
            yield chunk
