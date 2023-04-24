# _*_ coding: utf-8 _*_

"""
project schema
"""

from .base import ProjectBase


class ProjectSchema(ProjectBase):
    pass


class ProjectCreate(ProjectBase):
    name: str
    user_id: int


class ProjectUpdate(ProjectBase):
    # user_id: int
    pass


class ProjectInDB(ProjectBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
