# _*_ coding: utf-8 _*_

"""
project schema
"""

from typing import Optional

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None


class ProjectCreate(ProjectSchema):
    name: str  # required
    user_id: int  # required


class ProjectUpdate(BaseModel):
    desc: Optional[str] = None


class ProjectUpdatePri(ProjectUpdate):
    pass
