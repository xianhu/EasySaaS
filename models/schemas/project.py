# _*_ coding: utf-8 _*_

"""
schemas of project
"""

from typing import Optional

from .base import ProjectBase


class ProjectSchema(ProjectBase):
    pass


class ProjectCreate(ProjectBase):
    name: str


class ProjectUpdate(ProjectBase):
    pass


class ProjectInDB(ProjectBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
