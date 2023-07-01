# _*_ coding: utf-8 _*_

"""
schemas module
"""

from pydantic import BaseModel

# schemas of File
from .file import FileCreate, FileCreatePri
from .file import FileSchema
from .file import FileTagCreate, FileTagCreatePri
# schemas of FileTag
from .file import FileTagSchema
from .file import FileTagUpdate, FileTagUpdatePri
from .file import FileUpdate, FileUpdatePri
# schemas of Project
from .project import ProjectCreate, ProjectCreatePri
from .project import ProjectSchema
from .project import ProjectUpdate, ProjectUpdatePri
# schemas of User
from .user import UserCreate, UserCreatePri
from .user import UserSchema
from .user import UserUpdate, UserUpdatePri


class AccessToken(BaseModel):
    access_token: str  # required
    token_type: str = "bearer"


class Resp(BaseModel):
    status: int = 0
    msg: str = "success"
