# _*_ coding: utf-8 _*_

"""
file api
"""

from ..base import *


# response model
class RespFile(Resp):
    data_file: Optional[FileSchema] = Field(None)
    data_filetag_id_list: Optional[List[str]] = Field(None)


# response model
class RespFileList(Resp):
    data_file_total: int = Field(0)
    data_file_list: List[FileSchema] = Field([])
    data_filetag_id_list_list: List[List[str]] = Field([])


def check_file_type_size(filetype: str, filesize: int) -> bool:
    """
    check file type and size, return True or raise exception
    - **status_code=500**: file type not supported
    - **status_code=500**: file size too large
    """
    if filetype not in ["audio/mpeg", "audio/wav", "audio/x-wav",
                        "audio/mp4", "audio/webm", "audio/x-m4a"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file type not supported"
        )
    if filesize > 1024 * 1024 * 25:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    return True


def check_file(file_id: str, user_id: str, session: Session) -> File:
    """
    check if file_id is valid to user_id, return file model
    - **status_code=404**: file not found
    """
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="file not found",
        )
    return file_model


def get_filetag_id_list(file_id: str, session: Session) -> List[str]:
    """
    get filetag_id list by file_id from filetagfiles table
    """
    # get filetagfile model list
    filter1 = FileTagFile.file_id == file_id
    ftf_model_list = session.query(FileTagFile).filter(filter1).all()

    # return filetag_id list related to file_id
    return [ftf_model.filetag_id for ftf_model in ftf_model_list]


def delete_file_filetagfile(file_id_list: List[str], session: Session) -> bool:
    """
    delete file models and filetagfile models by file_id list, return True
    - **status_code=500**: delete file filetagfile error
    """
    # delete files from disk or cloud  # TODO
    try:
        # delete filetagfile models and file models
        session.query(FileTagFile).filter(FileTagFile.file_id.in_(file_id_list)).delete()
        session.query(File).filter(File.id.in_(file_id_list)).delete()
        session.commit()
        return True
    except Exception as excep:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="delete file filetagfile error",
        )
