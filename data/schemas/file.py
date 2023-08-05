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
    filesize: Optional[int] = None  # can't be changed
    filetype: Optional[str] = None  # can't be changed
    is_trash: Optional[bool] = None
    trash_time: Optional[datetime] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    created_time: Optional[datetime] = Field(None, description="Created DateTime")
    updated_time: Optional[datetime] = Field(None, description="Updated DateTime")


# used for request body
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, min_length=4, max_length=100)
    created_time: Optional[datetime] = Field(None, description="Created DateTime")
    updated_time: Optional[datetime] = Field(None, description="Updated DateTime")
