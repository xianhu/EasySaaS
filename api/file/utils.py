# _*_ coding: utf-8 _*_

"""
file api
"""

from ..base import *


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
    # get filetagfile model list
    filter1 = FileTagFile.file_id == file_id
    ftf_model_list = session.query(FileTagFile).filter(filter1).all()

    # return filetag_id list
    return [ftf_model.filetag_id for ftf_model in ftf_model_list]
