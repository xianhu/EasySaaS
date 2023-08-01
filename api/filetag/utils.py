# _*_ coding: utf-8 _*_

"""
utility functions and variables
"""

from typing import List

from fastapi import HTTPException, status
from pydantic import Field
from sqlalchemy.orm import Session

from data.models import FileTag
from data.schemas import FileTagSchema, Resp


# response model
class RespFileTag(Resp):
    data_filetag: FileTagSchema = Field(None)


# response model
class RespFileTagList(Resp):
    data_filetag_list: List[FileTagSchema] = Field(None)


def check_filetag_permission(filetag_id: str, user_id: str, session: Session) -> FileTag:
    """
    check if filetag_id is valid and user_id has permission to access filetag
    """
    filetag_model = session.query(FileTag).get(filetag_id)
    if (not filetag_model) or (filetag_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no permission to access filetag",
        )
    return filetag_model
