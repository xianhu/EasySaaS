# _*_ coding: utf-8 _*_

"""
filetag schema
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from .file import FileSchema


# used for response_model
class FileTagSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    ttype: Optional[str] = None
    # user_id: Optional[str] = None
    # ---- link to file list ----
    file_list: List[FileSchema] = []


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
