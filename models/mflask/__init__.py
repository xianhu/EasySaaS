# _*_ coding: utf-8 _*_

"""
models in flask
"""

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm

from models import BaseModel

# create SQLAlchemy
app_db = SQLAlchemy(app=None)


class UserProject(BaseModel, app_db.Model):
    # relationships
    user_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("user.id"), primary_key=True)
    project_id = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey("project.id"), primary_key=True)

    # role and role_json of project
    role = sqlalchemy.Column(sqlalchemy.String(255), default="admin", doc="admin/writer/reader")
    role_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, doc="json of role")

    # relationships: up.user, up.project
    user = orm.relationship("User", back_populates="user_projects")
    project = orm.relationship("Project", back_populates="user_projects")
