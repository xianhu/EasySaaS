# _*_ coding: utf-8 _*_

"""
file schema
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# used for response_model
class FileSchema(BaseModel):
    id: Optional[str] = None
    filename: Optional[str] = None
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None
    filesize: Optional[int] = None
    filetype: Optional[str] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None
    # user_id: Optional[str] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    created_time: Optional[datetime] = Field(None, description="Created Time")
    updated_time: Optional[datetime] = Field(None, description="Updated Time")


# used for request body
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, min_length=4, max_length=100)
    created_time: Optional[datetime] = Field(None, description="Created Time")
    updated_time: Optional[datetime] = Field(None, description="Updated Time")
