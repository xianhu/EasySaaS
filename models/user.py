# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy
from sqlalchemy import orm

from .base import AbstractModel


class User(AbstractModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), index=False)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), index=False)

    # relationship: projects
    projects = orm.relationship("Project", back_populates="user")
