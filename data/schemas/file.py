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
    # ttype: Optional[str] = None
    # user_id: Optional[int] = None


# used for request body
class FileTagCreate(BaseModel):
    name: str  # required
    icon: Optional[str] = None
    color: Optional[str] = None


# used for request body
class FileTagUpdate(BaseModel):
    id: int  # required
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


# used for response_model
class FileSchema(BaseModel):
    id: Optional[int] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None


# used for request body
class FileCreate(BaseModel):
    filename: str  # required


# used for request body
class FileUpdate(BaseModel):
    id: int  # required
    filename: Optional[str] = None
