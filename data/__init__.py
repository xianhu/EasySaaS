# _*_ coding: utf-8 _*_

"""
data module
"""

from .db_mysql import SessionLocal, get_session
from .db_redis import redis_pool
