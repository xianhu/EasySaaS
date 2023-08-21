# _*_ coding: utf-8 _*_

"""
file schema
"""

from .base import *


# used for response_model
class FileSchema(BaseModel):
    id: Optional[str] = None
    filename: Optional[str] = None
    keywords: Optional[List[str]] = None
    edit_time: Optional[datetime] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    keywords: Optional[List[str]] = Field(None, description="Keywords")


# used for request body
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, min_length=4, max_length=100)
    keywords: Optional[List[str]] = Field(None, description="Keywords")
