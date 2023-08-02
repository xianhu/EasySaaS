# _*_ coding: utf-8 _*_

"""
filetag model
"""

import sqlalchemy.orm
from sqlalchemy import ForeignKey

from .base import AbstractModel


class FileTag(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    icon = sqlalchemy.Column(sqlalchemy.String(255), doc="Icon Value")
    color = sqlalchemy.Column(sqlalchemy.String(255), doc="Color Code")

    # information -- type, system or custom
    ttype = sqlalchemy.Column(sqlalchemy.String(255), default="custom", doc="system, custom")

    # relationship -- foreign_key to user
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)
