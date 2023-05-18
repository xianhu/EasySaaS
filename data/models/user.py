# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy.orm

from .base import AbstractModel


class User(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255))
    avatar = sqlalchemy.Column(sqlalchemy.String(255))

    # information -- email
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    email_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # information -- others (model -> schema -> crud)
    # ts_expires = sqlalchemy.Column(sqlalchemy.Integer, doc="Timestamp Expires")

    # information -- permission
    password = sqlalchemy.Column(sqlalchemy.String(512), doc="Password")
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is Admin")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Role Json")

    # relationship: projects
    projects = sqlalchemy.orm.relationship("Project", back_populates="user")
