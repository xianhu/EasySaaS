# _*_ coding: utf-8 _*_

"""
data module
"""

from .dmysql import SessionLocal, get_session
from .dredis import get_redis, redis_pool
