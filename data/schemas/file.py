# _*_ coding: utf-8 _*_

"""
file schema (FileTag and File)
"""

from typing import Optional

from pydantic import BaseModel, Field


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
    name: str = Field(..., min_length=2, max_length=10)
    icon: Optional[str] = Field(description="Icon Value")
    color: Optional[str] = Field(description="Color Code")


# used for request body
class FileTagUpdate(BaseModel):
    id: int = Field(...)
    name: Optional[str] = Field(min_length=2, max_length=10)
    icon: Optional[str] = Field(description="Icon Value")
    color: Optional[str] = Field(description="Color Code")


# used for response_model
class FileSchema(BaseModel):
    id: Optional[int] = None
    filename: Optional[str] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None
    permission: Optional[int] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)


# used for request body
class FileUpdate(BaseModel):
    id: int = Field(...)
    filename: Optional[str] = Field(min_length=4, max_length=100)
