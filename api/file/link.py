# _*_ coding: utf-8 _*_

"""
link of file api
"""

from fastapi import APIRouter
from fastapi import Body, Depends
from sqlalchemy.orm import Session

from data import get_session
from data.models import FileTagFile, User
from data.schemas import FileSchema
from .utils import RespFile, check_file_permission
from ..filetag.utils import check_filetag_permission
from ..utils import get_current_user

# define router
router = APIRouter()


@router.post("/link/", response_model=RespFile)
def _link_file_filetag(file_id: str = Body(..., description="id of file"),
                       filetag_id: str = Body(..., description="id of filetag"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    link file model to a filetag model, return file schema and filetag_id list
    - **status_code=403**: no permission to access file or filetag
    """
    # check file_id and get file model, filetag_id and get filetag model
    file_model = check_file_permission(file_id, current_user.id, session)
    _ = check_filetag_permission(filetag_id, current_user.id, session)

    # check if filetagfile existed in database
    filetagfile_model = session.query(FileTagFile).filter(
        FileTagFile.file_id == file_id,
        FileTagFile.filetag_id == filetag_id,
    ).first()
    if not filetagfile_model:
        # create filetagfile model and save to database
        filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
        session.add(filetagfile_model)
        session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = [ftfm.filetag_id for ftfm in file_model.filetagfiles]
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)


@router.post("/unlink/", response_model=RespFile)
def _unlink_file_filetag(file_id: str = Body(..., description="id of file"),
                         filetag_id: str = Body(..., description="id of filetag"),
                         current_user: User = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    """
    unlink file model to a filetag model, return file schema and filetag_id list
    - **status_code=403**: no permission to access file or filetag
    """
    # check file_id and get file model, filetag_id and get filetag model
    file_model = check_file_permission(file_id, current_user.id, session)
    _ = check_filetag_permission(filetag_id, current_user.id, session)

    # delete filetagfile model by ids
    session.query(FileTagFile).filter(
        FileTagFile.file_id == file_id,
        FileTagFile.filetag_id == filetag_id,
    ).delete()
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = [ftfm.filetag_id for ftfm in file_model.filetagfiles]
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)
