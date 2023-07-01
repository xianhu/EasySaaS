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

    # relationship: foreign_key to user (project.user, user.projects)
    # user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    # user = sqlalchemy.orm.relationship("User", back_populates="projects")


class UserProject(AbstractModel):
    __table_args__ = (
        sqlalchemy.UniqueConstraint("user_id", "project_id", name="unique_project_user"),
    )

    # relationship: foreign_key to user and project
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("projects.id"))

    # information -- permission
    project_role = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Project Role Json")
