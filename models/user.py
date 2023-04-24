# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy.orm

from .base import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), index=False)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), index=False)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), index=False)

    # relationship: projects
    projects = sqlalchemy.orm.relationship("Project", back_populates="user")
