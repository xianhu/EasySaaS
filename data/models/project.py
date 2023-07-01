# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy.orm

from .base import AbstractModel


class Project(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String(255), doc="Description")

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")


class UserProject(AbstractModel):
    __table_args__ = (
        sqlalchemy.UniqueConstraint("user_id", "project_id", name="unique_project_user"),
    )

    # information -- permission
    project_role = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Project Role Json")

    # relationship: foreign_key to user
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship("User", back_populates="userprojects")

    # relationship: foreign_key to project
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("projects.id"))
    project = sqlalchemy.orm.relationship("Project", back_populates="userprojects")
