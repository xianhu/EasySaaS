# _*_ coding: utf-8 _*_

"""
file model
"""

import sqlalchemy.orm

from .base import AbstractModel


class File(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    format = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    # relationship: foreign_key and user
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship("User", back_populates="files")

    # relationship: foreign_key and category
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categorys.id"))
    category = sqlalchemy.orm.relationship("Category", back_populates="files")




class Category(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)


class Tag(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String(512), nullable=True)
