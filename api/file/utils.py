# _*_ coding: utf-8 _*_

"""
utility functions and variables
"""

from typing import List

from fastapi import HTTPException, status
from pydantic import Field
from sqlalchemy.orm import Session

from data.models import File
from data.schemas import FileSchema, Resp


# response model
class RespFile(Resp):
    data_file: FileSchema = Field(None)
    data_filetag_id_list: List[str] = Field(None)


# response model
class RespFileList(Resp):
    data_file_list: List[FileSchema] = Field(None)
    data_filetag_id_list_list: List[List[str]] = Field(None)


def check_file_permission(file_id: str, user_id: str, session: Session) -> File:
    """
    check if file_id is valid and user_id has permission to access file
    """
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no permission to access file",
        )
    return file_model
