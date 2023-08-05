# _*_ coding: utf-8 _*_

"""
data module
"""

from .dmysql import SessionMaker, get_session
from .dredis import RedisPool, get_redis
from .utils import FILETAG_SYSTEM_SET, PhoneStr
