# _*_ coding: utf-8 _*_

"""
file model
"""

from .base import *


class File(AbstractModel):
    # information -- basic
    filename = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    keywords = sqlalchemy.Column(sqlalchemy.JSON, default=[], doc="Keywords")

    # information -- size, type, fullname and location
    filesize = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, doc="File Size")
    filetype = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, doc="File Type")
    fullname = sqlalchemy.Column(sqlalchemy.String(512), nullable=False, doc="uid-sid-filename")
    location = sqlalchemy.Column(sqlalchemy.String(512), nullable=False, doc="save_path/fullname")

    # information -- edit datetime
    edit_time = sqlalchemy.Column(sqlalchemy.DateTime, doc="Edit DateTime")

    # information -- trash and trash datetime
    is_trash = sqlalchemy.Column(sqlalchemy.Boolean, default=False, doc="Is Trash")
    trash_time = sqlalchemy.Column(sqlalchemy.DateTime, doc="Trash DateTime")

    # relationship -- foreign_key to user
    user_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("users.id"), index=True)


class FileTagFile(AbstractModel):
    __table_args__ = (
        UniqueConstraint("filetag_id", "file_id", name="unique_filetag_file"),
    )
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # relationship -- foreign_key to filetag and file
    filetag_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("filetags.id"), index=True)
    file_id = sqlalchemy.Column(sqlalchemy.String(128), ForeignKey("files.id"), index=True)
