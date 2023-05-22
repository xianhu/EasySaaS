# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy.orm

from .base import AbstractModel


class Project(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # information -- others (model -> schema -> crud)
    # ts_expires = sqlalchemy.Column(sqlalchemy.Integer, doc="Timestamp Expires")

    # information -- foreign_key
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    # relationship: user
    user = sqlalchemy.orm.relationship("User", back_populates="projects")
