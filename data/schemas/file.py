# _*_ coding: utf-8 _*_

"""
file schema (FileTag and File)
"""

from typing import Optional

from pydantic import BaseModel, Field


# used for response_model
class FileTagSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    # ttype: Optional[str] = None
    # user_id: Optional[str] = None


# used for request body
class FileTagCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    icon: Optional[str] = Field(None, description="Icon Value")
    color: Optional[str] = Field(None, description="Color Code")


# used for request body
class FileTagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=20)
    icon: Optional[str] = Field(None, description="Icon Value")
    color: Optional[str] = Field(None, description="Color Code")


# used for response_model
class FileSchema(BaseModel):
    id: Optional[str] = None
    filename: Optional[str] = None
    filesize: Optional[int] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None
    permission: Optional[int] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    filesize: int = Field(..., ge=0, description="File Size")


# used for request body
class FileUpdate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    # filesize: int = Field(..., ge=0, description="File Size")
