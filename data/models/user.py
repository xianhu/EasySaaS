# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy.orm

from .base import AbstractModel


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

    # information -- permissions of system
    system_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is System Admin")
    system_role = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="System Role Json")

    # relationship -- userprojects (user.userprojects, userproject.user)
    userprojects = sqlalchemy.orm.relationship("UserProject", back_populates="user")

    # relationship -- filetags (user.filetags, filetag.user)
    filetags = sqlalchemy.orm.relationship("FileTag", back_populates="user")

    # relationship -- files (user.files, file.user)
    files = sqlalchemy.orm.relationship("File", back_populates="user")
