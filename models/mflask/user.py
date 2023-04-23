# _*_ coding: utf-8 _*_

"""
user model
"""

from sqlalchemy import orm

from models import UserBase
from models.mflask import app_db


class User(UserBase, app_db.Model):
    # relationship: user.user_projects
    user_projects = orm.relationship("UserProject", back_populates="user")
