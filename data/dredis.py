# _*_ coding: utf-8 _*_

"""
database of redis
"""

import redis
from redis import ConnectionPool

from core.settings import settings

# create connection pool
url = f"{settings.REDIS_URI}/{0 if not settings.DEBUG else 1}"
RedisPool = ConnectionPool.from_url(url, decode_responses=True)


def get_redis() -> redis.Redis:
    """
    get redis connection
    """
    return redis.Redis(connection_pool=RedisPool)
