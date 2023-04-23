# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy
from sqlalchemy import orm

from . import BaseModel


class Project(BaseModel):
    # basic
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), index=False, nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String(512), index=False, nullable=True)

    # relationship: project.user_projects
    user_projects = orm.relationship("UserProject", back_populates="project")


class UserProject(BaseModel):
    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    project_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("projects.id"), primary_key=True)

    # role and role_json of project
    role = sqlalchemy.Column(sqlalchemy.String(255), index=False, default="admin", doc="Role: admin, member")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, index=False, nullable=True, doc="Role Json")

    # relationships: up.user, up.project
    user = orm.relationship("User", back_populates="user_projects")
    project = orm.relationship("Project", back_populates="user_projects")
