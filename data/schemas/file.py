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

    filesize: Optional[int] = None
    filetype: Optional[str] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None

    edit_time: Optional[datetime] = None
    filetag_id_list: Optional[List[str]] = None


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    keywords: List[str] = Field([], description="Keywords")
    # edit_time: datetime = Field(..., description="Edit DateTime")
    filetag_id_list: List[str] = Field([], description="FileTag ID List")


# used for request body
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, min_length=4, max_length=100)
    keywords: List[str] = Field([], description="Keywords")
    # edit_time: datetime = Field(..., description="Edit DateTime")
    filetag_id_list: List[str] = Field([], description="FileTag ID List")
