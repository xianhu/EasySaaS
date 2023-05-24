# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

from .project import ProjectCreate, ProjectCreatePri
from .project import ProjectSchema
from .project import ProjectUpdate, ProjectUpdatePri
from .user import UserCreate, UserCreatePri
from .user import UserSchema
from .user import UserUpdate, UserUpdatePri


class AccessToken(BaseModel):
    access_token: str  # required
    token_type: str = "bearer"


class Resp(BaseModel):
    status: int = 0
    msg: str = "success"
