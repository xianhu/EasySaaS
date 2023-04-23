# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy
from sqlalchemy import orm

from . import BaseModel


class User(BaseModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), index=False, nullable=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, nullable=True, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), index=True, nullable=True, unique=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)

    # relationship: user.user_projects
    user_projects = orm.relationship("UserProject", back_populates="user")
