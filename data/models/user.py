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
    birthday = sqlalchemy.Column(sqlalchemy.Date, doc="Date of Birthday")
    gender = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="1-Male, 2-Female")

    # information -- country and address
    country = sqlalchemy.Column(sqlalchemy.String(255), doc="Country")
    address = sqlalchemy.Column(sqlalchemy.String(512), doc="Address")

    # information -- email / phone and password
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True, index=True)
    email_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Verified?")
    phone = sqlalchemy.Column(sqlalchemy.String(255), unique=True, index=True)
    phone_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Verified?")
    password = sqlalchemy.Column(sqlalchemy.String(512), doc="Hash Value of Password")

    # information -- expire datetime
    expire_time = sqlalchemy.Column(sqlalchemy.DateTime, doc="Expire DateTime")

    # information -- points and history
    points_left = sqlalchemy.Column(sqlalchemy.Integer, doc="Left Points")
    points_total = sqlalchemy.Column(sqlalchemy.Integer, doc="Total Points")
    points_history = sqlalchemy.Column(sqlalchemy.JSON, default=[], doc="Points History")

    # information -- space and history (bytes with biginteger)
    space_used = sqlalchemy.Column(sqlalchemy.BigInteger, doc="Used Space")
    space_total = sqlalchemy.Column(sqlalchemy.BigInteger, doc="Total Space")
    space_history = sqlalchemy.Column(sqlalchemy.JSON, default=[], doc="Space History")

    # information -- permissions of system
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is Admin")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Role Json")


class UserLog(AbstractModel):
    # information -- id and user_id
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)

    # information -- basic
    host = sqlalchemy.Column(sqlalchemy.String(255), doc="Host")
    ua = sqlalchemy.Column(sqlalchemy.String(255), doc="User Agent")
    headers = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Headers")

    # information -- others
    path = sqlalchemy.Column(sqlalchemy.String(255), doc="Request Path")
