# _*_ coding: utf-8 _*_

"""
file schema
"""

from .base import *


# used for response_model
class FileSchema(BaseModel):
    id: Optional[str] = None
    filename: Optional[str] = None
    duration: Optional[int] = None
    start_time: Optional[datetime] = None
    filesize: Optional[int] = None  # can't be changed
    filetype: Optional[str] = None  # can't be changed
    is_trash: Optional[bool] = None  # use trash api
    trash_time: Optional[datetime] = None  # use trash api


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    duration: Optional[int] = Field(None, description="Duration")
    start_time: Optional[datetime] = Field(None, description="Start DateTime")


# used for request body
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, min_length=4, max_length=100)
    duration: Optional[int] = Field(None, description="Duration")
    start_time: Optional[datetime] = Field(None, description="Start DateTime")
