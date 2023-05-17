# _*_ coding: utf-8 _*_

"""
data module
"""

from .dmysql import SessionLocal, get_session
from .dredis import RedisPool, get_redis
