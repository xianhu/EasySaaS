# _*_ coding: utf-8 _*_

"""
test redis
"""

import logging

from data import get_redis

rd = get_redis()
rd.set("test", "test")
logging.warning("test: %s", rd.get("test"))
