# _*_ coding: utf-8 _*_

"""
file schema
"""

from typing import Optional

from pydantic import BaseModel, Field


# used for response_model
class FileSchema(BaseModel):
    id: Optional[str] = None
    filename: Optional[str] = None
    filesize: Optional[int] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None
    # user_id: Optional[str] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    filesize: int = Field(..., ge=0, description="File Size")


# used for request body
class FileUpdate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    # filesize: int = Field(..., ge=0, description="File Size")
