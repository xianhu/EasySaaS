# _*_ coding: utf-8 _*_

"""
test redis
"""

import logging

import redis

from data import RedisPool

# init redis
rd = redis.Redis(connection_pool=RedisPool)

# test redis
rd.set("test", "test")
logging.warning("test: %s", rd.get("test"))
