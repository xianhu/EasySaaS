# _*_ coding: utf-8 _*_

"""
user model
"""

import sqlalchemy.orm

from .base import AbstractModel


class Company(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255))
    avatar = sqlalchemy.Column(sqlalchemy.String(255), doc="Avatar Url")
    location = sqlalchemy.Column(sqlalchemy.String(255), doc="Location")

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")

    # relationship: users (company.users, user.company)
    # users = sqlalchemy.orm.relationship("User", back_populates="company")


class User(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255))
    avatar = sqlalchemy.Column(sqlalchemy.String(255), doc="Avatar Url")

    # information -- email
    email = sqlalchemy.Column(sqlalchemy.String(255), index=True, unique=True)
    email_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Verified?")

    # information -- permission
    password = sqlalchemy.Column(sqlalchemy.String(512), doc="Hash Value of Password")
    system_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is System Admin")
    system_role = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="System Role Json")

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")

    # relationship: foreign_key and company
    # company_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id"))
    # company = sqlalchemy.orm.relationship("Company", back_populates="users")
    company_name = sqlalchemy.Column(sqlalchemy.String(255), doc="Company Name")

    # information -- permission of company
    company_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=True, doc="Is Company Admin")
    company_role = sqlalchemy.Column(sqlalchemy.JSON, default={}, doc="Company Role Json")

    # relationship: projects (user.projects, project.user)
    projects = sqlalchemy.orm.relationship("Project", back_populates="user")

    # relationship: filetags (user.filetags, filetag.user)
    filetags = sqlalchemy.orm.relationship("FileTag", back_populates="user")
