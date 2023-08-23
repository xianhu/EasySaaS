# _*_ coding: utf-8 _*_

"""
file api
"""

from .utils import *
from ..base import *
from ..filetag.utils import check_filetag
from ..utils import get_current_user

# define router
router = APIRouter()


@router.post("/link/", response_model=RespFile)
def _link_file_filetag(file_id: str = Body(..., description="file id"),
                       filetag_id: str = Body(..., description="filetag id"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    link file model to a filetag model, return file schema
    - **status_code=404**: file not found or filetag not found
    """
    # check file_id/filetag_id and get file/filetag model
    file_model = check_file(file_id, current_user.id, session)
    filetag_model = check_filetag(filetag_id, current_user.id, session)

    # check if filetagfile existed in database
    filter1 = FileTagFile.file_id == file_id
    filter2 = FileTagFile.filetag_id == filetag_id
    if not session.query(FileTagFile).filter(filter1, filter2).first():
        # create filetagfile model by file_id and filetag_id
        filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
        session.add(filetagfile_model)
        session.commit()

    # create file schema
    file_schema = FileSchema(**file_model.dict())
    file_schema.filetag_id_list = get_filetag_id_list(file_id, session)

    # return file schema
    return RespFile(data_file=file_schema)


@router.post("/unlink/", response_model=RespFile)
def _unlink_file_filetag(file_id: str = Body(..., description="file id"),
                         filetag_id: str = Body(..., description="filetag id"),
                         current_user: User = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    """
    unlink file model to a filetag model, return file schema
    - **status_code=404**: file not found or filetag not found
    """
    # check file_id/filetag_id and get file/filetag model
    file_model = check_file(file_id, current_user.id, session)
    filetag_model = check_filetag(filetag_id, current_user.id, session)

    # delete filetagfile model by file_id and filetag_id
    filter1 = FileTagFile.file_id == file_id
    filter2 = FileTagFile.filetag_id == filetag_id
    session.query(FileTagFile).filter(filter1, filter2).delete()
    session.commit()

    # create file schema
    file_schema = FileSchema(**file_model.dict())
    file_schema.filetag_id_list = get_filetag_id_list(file_id, session)

    # return file schema
    return RespFile(data_file=file_schema)
