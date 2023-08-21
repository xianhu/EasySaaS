# _*_ coding: utf-8 _*_

"""
user model
"""

from .base import *


class User(AbstractModel):
    # information -- basic
    avatar = sqlalchemy.Column(sqlalchemy.String(255), doc="Avatar Url")
    nickname = sqlalchemy.Column(sqlalchemy.String(255), doc="Nickname")

    # information -- personal information
    birthday = sqlalchemy.Column(sqlalchemy.DateTime, doc="Birthday Datetime")
    gender = sqlalchemy.Column(sqlalchemy.Integer, doc="1-Male, 2-Female")

    # information -- country and address
    country = sqlalchemy.Column(sqlalchemy.String(255), doc="Country")
    address = sqlalchemy.Column(sqlalchemy.String(512), doc="Address")

    # information -- email / phone and password
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True, index=True)
    email_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Verified?")
    phone = sqlalchemy.Column(sqlalchemy.String(255), unique=True, index=True)
    phone_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Verified?")
    password = sqlalchemy.Column(sqlalchemy.String(512), doc="Hash Value of Password")

    # information -- expire datetime and reset datetime
    expire_time = sqlalchemy.Column(sqlalchemy.DateTime, doc="Expire DateTime")
    reset_time = sqlalchemy.Column(sqlalchemy.DateTime, doc="Reset DateTime")

    # information -- points and history
    points_left = sqlalchemy.Column(sqlalchemy.Integer, doc="Left Points")
    points_total = sqlalchemy.Column(sqlalchemy.Integer, doc="Total Points")
    points_history = sqlalchemy.Column(sqlalchemy.JSON, default=[], doc="Points History")

    # information -- seconds and history
    seconds_left = sqlalchemy.Column(sqlalchemy.Integer, doc="Left Seconds")
    seconds_total = sqlalchemy.Column(sqlalchemy.Integer, doc="Total Seconds")
    seconds_history = sqlalchemy.Column(sqlalchemy.JSON, default=[], doc="Seconds History")

    # information -- space and history (bytes with biginteger)
    space_used = sqlalchemy.Column(sqlalchemy.BigInteger, doc="Used Space")
    space_total = sqlalchemy.Column(sqlalchemy.BigInteger, doc="Total Space")
    space_history = sqlalchemy.Column(sqlalchemy.JSON, default=[], doc="Space History")

    # information -- permissions of system
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is Admin")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Role Json")


class UserLog(AbstractModel):
    # information -- id, user_id and path
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)
    path = sqlalchemy.Column(sqlalchemy.String(255), doc="Request Path")

    # information -- basic
    host = sqlalchemy.Column(sqlalchemy.String(255), doc="Host")
    ua = sqlalchemy.Column(sqlalchemy.String(255), doc="User Agent")
    headers = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Headers")
