# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy.orm

from .base import AbstractModel


class Project(AbstractModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), index=False)

    # relationship: user
    user = sqlalchemy.orm.relationship("User", back_populates="projects")
