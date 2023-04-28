# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

from .project import ProjectCreate, ProjectSchema, ProjectUpdate
from .user import UserCreate, UserSchema, UserUpdate


class Token(BaseModel):
    token: str
    token_type: str


class Result(BaseModel):
    status: int = 1
    msg: str
