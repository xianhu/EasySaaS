# _*_ coding: utf-8 _*_

"""
project schema
"""

from typing import Optional

from pydantic import BaseModel


# used for response_model
class ProjectSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None


# used for request body
class ProjectCreate(BaseModel):
    name: str  # required
    desc: Optional[str] = None


# used for internal call
class ProjectCreatePri(ProjectCreate):
    id: Optional[int] = None


# used for request body
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None


# used for internal call
class ProjectUpdatePri(ProjectUpdate):
    # id: Optional[int] = None
    pass
