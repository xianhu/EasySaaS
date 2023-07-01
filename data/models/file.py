# _*_ coding: utf-8 _*_

"""
file model
"""

import sqlalchemy.orm

from .base import AbstractModel


class FileTag(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    icon = sqlalchemy.Column(sqlalchemy.String(255), doc="Icon Value")
    color = sqlalchemy.Column(sqlalchemy.String(255), doc="Color Code")

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")

    # relationship: foreign_key to user (filetag.user, user.filetags)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship("User", back_populates="filetags")

    # relationship: files (filetag.files, file.filetags)
    files = sqlalchemy.orm.relationship("File", secondary="filetagfiles", back_populates="filetags")


class File(AbstractModel):
    # information -- basic
    fullname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")

    # relationship: filetags (file.filetags, filetag.files)
    filetags = sqlalchemy.orm.relationship("FileTag", secondary="filetagfiles", back_populates="files")


class FileTagFile(AbstractModel):
    __table_args__ = (
        sqlalchemy.UniqueConstraint("filetag_id", "file_id", name="unique_filetag_file"),
    )

    # relationship: foreign_key to filetag and file
    filetag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("filetags.id"))
    file_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("files.id"))

    # information -- others (model -> schema -> crud)
    # xxx_xxxx = sqlalchemy.Column(sqlalchemy.String(255), doc="xxx xxxxx")
