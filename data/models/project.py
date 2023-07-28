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

    # relationship -- userprojects (project.userprojects, userproject.project)
    userprojects = sqlalchemy.orm.relationship("UserProject", back_populates="project")


class UserProject(AbstractModel):
    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="unique_user_project"),
    )

    # relationship -- foreign_key to user (userproject.user, user.userprojects)
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)
    user = sqlalchemy.orm.relationship("User", back_populates="userprojects")

    # relationship -- foreign_key to project (userproject.project, project.userprojects)
    project_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("projects.id"), index=True)
    project = sqlalchemy.orm.relationship("Project", back_populates="userprojects")

    # information -- permission of user and project
    permission = sqlalchemy.Column(sqlalchemy.Integer, default=0, doc="0(owner), 1(member)")
