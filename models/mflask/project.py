# _*_ coding: utf-8 _*_

"""
project model
"""

import sqlalchemy
from sqlalchemy import orm

from models import BaseModel
from models.mflask import app_db


class Project(BaseModel, app_db.Model):
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)

    # information
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)

    # information
    ts_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ts_expired = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    # relationship: project.user_projects
    user_projects = orm.relationship("UserProject", back_populates="project")
