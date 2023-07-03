# _*_ coding: utf-8 _*_

"""
file schema (FileTag and File)
"""

from typing import Optional

from pydantic import BaseModel


# used for response_model
class FileTagSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    # _type: Optional[str] = None
    # user_id: Optional[int] = None


# used for request body
class FileTagCreate(BaseModel):
    name: str  # required
    icon: Optional[str] = None
    color: Optional[str] = None


# used for request body
class FileTagUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

# file schema ignored
