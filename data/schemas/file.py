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
    user_id: Optional[int] = None


# used for request body
class FileTagCreate(BaseModel):
    name: str  # required
    icon: Optional[str] = None
    color: Optional[str] = None


# used for internal call
class FileTagCreatePri(FileTagCreate):
    id: Optional[int] = None
    user_id: int  # required


# used for request body
class FileTagUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


# used for internal call
class FileTagUpdatePri(FileTagUpdate):
    # id: Optional[int] = None
    # user_id: Optional[int] = None
    pass


# used for response_model
class FileSchema(BaseModel):
    id: Optional[int] = None
    fullname: Optional[str] = None
    location: Optional[str] = None


# used for request body
class FileCreate(BaseModel):
    fullname: str  # required
    location: str  # required


# used for internal call
class FileCreatePri(FileCreate):
    id: Optional[int] = None


# used for request body
class FileUpdate(BaseModel):
    fullname: Optional[str] = None
    location: Optional[str] = None


# used for internal call
class FileUpdatePri(FileUpdate):
    # id: Optional[int] = None
    pass
