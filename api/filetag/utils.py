# _*_ coding: utf-8 _*_

"""
filetag api
"""

from ..base import *





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
