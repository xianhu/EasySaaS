# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy.orm
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import AbstractModel


class Project(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), doc="Description")

    # information -- expire datetime
    expire_time = sqlalchemy.Column(sqlalchemy.DateTime, doc="Expire DateTime")


class UserProject(AbstractModel):
    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="unique_user_project"),
    )
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # relationship -- foreign_key to user and project
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)
    project_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("projects.id"), index=True)

    # information -- permission of user and project
    permission = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="0(owner), 1(member)")
