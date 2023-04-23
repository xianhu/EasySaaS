# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy

from models import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"
    __table_args__ = (
        sqlalchemy.Index("index_p_1", "name"),
    )

    # basic
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # information
    ts_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ts_expired = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    # relationship: project.user_projects
    user_projects = orm.relationship("UserProject", back_populates="project")


class UserProject(BaseModel):
    __tablename__ = "user_projects"

    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("users.id"), primary_key=True)
    project_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("projects.id"), primary_key=True)

    # role and role_json of project
    role = sqlalchemy.Column(sqlalchemy.String(255), default="admin", doc="admin/writer/reader")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, doc="json of role")

    # relationships: up.user, up.project
    user = orm.relationship("User", back_populates="user_projects")
    project = orm.relationship("Project", back_populates="user_projects")
