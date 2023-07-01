# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy.orm

from .base import AbstractModel


class User(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), doc="Avatar Url")

    # information -- email
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    email_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Verified?")

    # information -- permission
    password = sqlalchemy.Column(sqlalchemy.String(512), doc="Hash Value of Password")
    system_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is System Admin")
    system_role = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="System Role Json")

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")

    # relationship -- userprojects (user.userprojects, userproject.user)
    userprojects = sqlalchemy.orm.relationship("UserProject", back_populates="user")

    # relationship -- filetags (user.filetags, filetag.user)
    filetags = sqlalchemy.orm.relationship("FileTag", back_populates="user")
