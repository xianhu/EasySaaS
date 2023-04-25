# _*_ coding: utf-8 _*_

"""
project schema
"""

from typing import Optional

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    status: Optional[int] = 1


class ProjectCreate(ProjectSchema):
    name: str
    user_id: int


class ProjectUpdate(ProjectSchema):
    # user_id: int
    pass
