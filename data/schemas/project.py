# _*_ coding: utf-8 _*_

"""
project schema
"""

from .base import *


# used for response_model
class ProjectSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None


# used for request body
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=100)
    desc: Optional[str] = Field(None, description="Description")


# used for request body
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=4, max_length=100)
    desc: Optional[str] = Field(None, description="Description")
