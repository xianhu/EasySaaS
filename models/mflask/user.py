# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy
from sqlalchemy import orm

from models.mflask import BaseModel


class User(BaseModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    pwd = sqlalchemy.Column(sqlalchemy.String(512), index=False, nullable=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255), index=True, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)

    # relationship: user.user_projects
    user_projects = orm.relationship("UserProject", back_populates="user")
