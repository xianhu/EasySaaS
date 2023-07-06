# _*_ coding: utf-8 _*_

"""
file model (FileTag and File)
"""

import sqlalchemy.orm

from .base import AbstractModel


class FileTag(AbstractModel):
    # information -- basic
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    icon = sqlalchemy.Column(sqlalchemy.String(255), doc="Icon Value")
    color = sqlalchemy.Column(sqlalchemy.String(255), doc="Color Code")
    ttype = sqlalchemy.Column(sqlalchemy.String(255), default="custom", doc="system, custom")

    # relationship -- foreign_key to user (filetag.user, user.filetags)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship("User", back_populates="filetags")

    # relationship -- filetagfiles (filetag.filetagfiles, filetagfile.filetag)
    filetagfiles = sqlalchemy.orm.relationship("FileTagFile", back_populates="filetag")


class File(AbstractModel):
    # information -- basic
    filename = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    # information -- fullname and location
    fullname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, doc="uid-time-filename")
    location = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, doc="save_path + fullname")

    # relationship -- filetagfiles (file.filetagfiles, filetagfile.file)
    filetagfiles = sqlalchemy.orm.relationship("FileTagFile", back_populates="file")


class FileTagFile(AbstractModel):
    __table_args__ = (
        sqlalchemy.UniqueConstraint("filetag_id", "file_id", name="unique_filetag_file"),
    )

    # information -- permission
    permission = sqlalchemy.Column(sqlalchemy.Integer, default=1, doc="0(read), 1(write)")

    # relationship -- foreign_key to filetag (filetagfile.filetag, filetag.filetagfiles)
    filetag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("filetags.id"))
    filetag = sqlalchemy.orm.relationship("FileTag", back_populates="filetagfiles")

    # relationship -- foreign_key to file (filetagfile.file, file.filetagfiles)
    file_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("files.id"))
    file = sqlalchemy.orm.relationship("File", back_populates="filetagfiles")
