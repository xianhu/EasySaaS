# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy.orm

from .base import AbstractModel


class User(AbstractModel):
    # hash password
    pwd = sqlalchemy.Column(sqlalchemy.String(512))

    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255))
    avatar = sqlalchemy.Column(sqlalchemy.String(255))

    # information -- email
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    email_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # relationship: projects
    projects = sqlalchemy.orm.relationship("Project", back_populates="user")
