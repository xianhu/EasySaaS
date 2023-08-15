# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

from .file import FileCreate, FileSchema, FileUpdate
from .filetag import FileTagCreate, FileTagSchema, FileTagUpdate
from .project import ProjectCreate, ProjectSchema, ProjectUpdate
from .user import UserCreate, UserCreateEmail, UserCreatePhone, UserSchema, UserUpdate


# base response
class Resp(BaseModel):
    status: int = 0
    msg: str = "success"


# response model
class RespSend(Resp):
    token: str = "no token"
