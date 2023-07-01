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

    # relationship -- userprojects (project.userprojects, userproject.project)
    userprojects = sqlalchemy.orm.relationship("UserProject", back_populates="project")


class UserProject(AbstractModel):
    __table_args__ = (
        sqlalchemy.UniqueConstraint("user_id", "project_id", name="unique_user_project"),
    )

    # information -- permission
    permission = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0(read), 1(write)")

    # relationship -- foreign_key to user (user.userprojects, userproject.user)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship("User", back_populates="userprojects")

    # relationship -- foreign_key to project (project.userprojects, userproject.project)
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("projects.id"))
    project = sqlalchemy.orm.relationship("Project", back_populates="userprojects")
