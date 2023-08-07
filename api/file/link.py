# _*_ coding: utf-8 _*_

"""
file api
"""

from .utils import RespFile, check_file_permission, get_filetag_id_list
from ..base import *
from ..filetag.utils import check_filetag_permission
from ..utils import get_current_user

# define router
router = APIRouter()


@router.post("/link/", response_model=RespFile)
def _link_file_filetag(file_id: str = Body(..., description="file id"),
                       filetag_id: str = Body(..., description="filetag id"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    link file model to a filetag model, return file schema and filetag_id list
    - **status_code=403**: no permission to access file or filetag
    """
    # check file_id and get file model, filetag_id and get filetag model
    file_model = check_file_permission(file_id, current_user.id, session)
    filetag_model = check_filetag_permission(filetag_id, current_user.id, session)

    # check if filetagfile existed in database
    filter1 = FileTagFile.file_id == file_id
    filter2 = FileTagFile.filetag_id == filetag_id
    if not session.query(FileTagFile).filter(filter1, filter2).first():
        # create filetagfile model and save to database
        filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
        session.add(filetagfile_model)
        session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = get_filetag_id_list(file_id, session)
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)


@router.post("/unlink/", response_model=RespFile)
def _unlink_file_filetag(file_id: str = Body(..., description="file id"),
                         filetag_id: str = Body(..., description="filetag id"),
                         current_user: User = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    """
    unlink file model to a filetag model, return file schema and filetag_id list
    - **status_code=403**: no permission to access file or filetag
    """
    # check file_id and get file model, filetag_id and get filetag model
    file_model = check_file_permission(file_id, current_user.id, session)
    filetag_model = check_filetag_permission(filetag_id, current_user.id, session)

    # delete filetagfile model by file_id and filetag_id
    filter1 = FileTagFile.file_id == file_id
    filter2 = FileTagFile.filetag_id == filetag_id
    session.query(FileTagFile).filter(filter1, filter2).delete()
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = get_filetag_id_list(file_id, session)
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)
