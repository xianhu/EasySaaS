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

    duration: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: Optional[int] = None

    filesize: Optional[int] = None
    filetype: Optional[str] = None
    # fullname: Optional[str] = None
    # location: Optional[str] = None

    is_trash: Optional[bool] = None  # use trash api
    trash_time: Optional[datetime] = None  # use trash api


# used for request body
class FileCreate(BaseModel):
    filename: str = Field(..., min_length=4, max_length=100)
    # keywords: Optional[List[str]] = Field(None, description="Keyword List")

    duration: Optional[int] = Field(None, description="Duration")
    start_time: Optional[datetime] = Field(None, description="Start DateTime")
    end_time: Optional[datetime] = Field(None, description="End DateTime")
    timezone: Optional[int] = Field(None, description="Timezone")


# used for request body
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, min_length=4, max_length=100)
    keywords: Optional[List[str]] = Field(None, description="Keyword List")
