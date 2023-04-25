# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

from .project import (ProjectCreate, ProjectInDB, ProjectSchema, ProjectUpdate)
from .user import (UserCreate, UserInDB, UserSchema, UserUpdate)


class Token(BaseModel):
    access_token: str
    token_type: str


class Msg(BaseModel):
    msg: str
