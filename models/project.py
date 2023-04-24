# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy
from sqlalchemy import ForeignKey, orm

from .base import AbstractModel


class Project(AbstractModel):
    __tablename__ = "projects"

    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("users.id"), nullable=False)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), index=False)

    # relationship: user
    user = orm.relationship("User", back_populates="projects")
