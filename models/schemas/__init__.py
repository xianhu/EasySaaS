# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

from .project import ProjectCreate, ProjectSchema, ProjectUpdate, ProjectUpdatePri
from .user import UserCreate, UserSchema, UserUpdate, UserUpdatePri


class Token(BaseModel):
    token: str
    token_type: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Result(BaseModel):
    status: int = 1
    msg: str
