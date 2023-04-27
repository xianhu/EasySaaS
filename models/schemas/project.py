# _*_ coding: utf-8 _*_

"""
project schema
"""

from typing import Optional

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None


class ProjectCreate(ProjectSchema):
    name: str  # required
    user_id: int  # required
    id: Optional[int] = None


class ProjectUpdate(ProjectSchema):
    pass
