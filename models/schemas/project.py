# _*_ coding: utf-8 _*_

"""
project schema
"""

from .base import ProjectBase


class ProjectSchema(ProjectBase):
    pass


class ProjectCreate(ProjectBase):
    name: str


class ProjectUpdate(ProjectBase):
    pass


class ProjectInDB(ProjectBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
