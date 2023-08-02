# _*_ coding: utf-8 _*_

"""
file api
"""

from typing import List, Optional

from fastapi import HTTPException, status
from pydantic import Field
from sqlalchemy.orm import Session

from data.models import File, FileTagFile
from data.schemas import FileSchema, Resp


# response model
class RespFile(Resp):
    data_file: Optional[FileSchema] = Field(None)
    data_filetag_id_list: List[str] = Field([])


# response model
class RespFileList(Resp):
    data_file_list: List[FileSchema] = Field([])
    data_filetag_id_list_list: List[List[str]] = Field([])


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


def get_filetag_id_list(file_id: str, session: Session) -> List[str]:
    """
    get filetag_id list of file from filetagfiles table
    """
    return [item[0] for item in session.query(FileTagFile.filetag_id, ).filter(
        FileTagFile.file_id == file_id,
    ).all()]
