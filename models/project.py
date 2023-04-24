# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy
from sqlalchemy import ForeignKey, orm

from .base import AbstractModel


class Project(AbstractModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), index=False)

    # relationship: user
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("users.id"), nullable=False)
    user = orm.relationship("User", back_populates="projects")
