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


# used for internal call
class ProjectCreate(ProjectSchema):
    name: str  # required
    user_id: int  # required
    is_current: bool = False  # default


# used for request body
class ProjectUpdate(BaseModel):
    desc: Optional[str] = None


# used for internal call
class ProjectUpdatePri(ProjectUpdate):
    pass
