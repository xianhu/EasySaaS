# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy
from sqlalchemy import orm

from models.mflask import BaseModel


class Project(BaseModel):
    __name__ = "project"

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String(512), index=False, nullable=True)

    # information
    ts_start = sqlalchemy.Column(sqlalchemy.Integer, index=False, nullable=True)
    ts_expired = sqlalchemy.Column(sqlalchemy.Integer, index=False, nullable=True)

    # relationship: project.user_projects
    user_projects = orm.relationship("UserProject", back_populates="project")


class UserProject(BaseModel):
    __name__ = "user_project"

    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("user.id"), primary_key=True)
    project_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("project.id"), primary_key=True)

    # role and role_json of project
    role = sqlalchemy.Column(sqlalchemy.String(255), index=False, default="admin")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, index=False, nullable=True)

    # relationships: up.user, up.project
    user = orm.relationship("User", back_populates="user_projects")
    project = orm.relationship("Project", back_populates="user_projects")
