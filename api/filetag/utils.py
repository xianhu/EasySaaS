# _*_ coding: utf-8 _*_

"""
filetag api
"""

from ..base import *


# response model
class RespFileTag(Resp):
    data_filetag: Optional[FileTagSchema] = Field(None)


# response model
class RespFileTagList(Resp):
    data_filetag_total: int = Field(...)
    data_filetag_list: List[FileTagSchema] = Field([])


def check_filetag_permission(filetag_id: str, user_id: str, session: Session) -> FileTag:
    """
    check if filetag_id is valid and user_id has permission to access filetag
    """
    filetag_model = session.query(FileTag).get(filetag_id)
    if (not filetag_model) or (filetag_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404 not found",
        )
    return filetag_model
