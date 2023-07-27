# _*_ coding: utf-8 _*_

"""
file model
"""

import sqlalchemy.orm
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import AbstractModel


class File(AbstractModel):
    # information -- basic
    filename = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    filesize = sqlalchemy.Column(sqlalchemy.BigInteger, default=0, doc="File Size")

    # information -- fullname and location
    fullname = sqlalchemy.Column(sqlalchemy.String(512), nullable=False, doc="uid-time-filename")
    location = sqlalchemy.Column(sqlalchemy.String(512), nullable=False, doc="save_path/fullname")

    # relationship -- foreign_key to user (file.user, user.files)
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)
    user = sqlalchemy.orm.relationship("User", back_populates="files")

    # relationship -- filetagfiles (file.filetagfiles, filetagfile.file)
    filetagfiles = sqlalchemy.orm.relationship("FileTagFile", back_populates="file")


class FileTagFile(AbstractModel):
    __table_args__ = (
        UniqueConstraint("filetag_id", "file_id", name="unique_filetag_file"),
    )

    # relationship -- foreign_key to filetag (filetagfile.filetag, filetag.filetagfiles)
    filetag_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("filetags.id"), index=True)
    filetag = sqlalchemy.orm.relationship("FileTag", back_populates="filetagfiles")

    # relationship -- foreign_key to file (filetagfile.file, file.filetagfiles)
    file_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("files.id"), index=True)
    file = sqlalchemy.orm.relationship("File", back_populates="filetagfiles")
