# _*_ coding: utf-8 _*_

"""
file api of admin
"""

from ..base import *
from ..file.utils import RespFileList

# define router
router = APIRouter()


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          session: Session = Depends(get_session)):
    """
    get file schema list, support pagination
    """
    # get file model list and schema list
    file_model_list = session.query(File).offset(skip).limit(limit).all()
    file_schema_list = [FileSchema(**fm.dict()) for fm in file_model_list]

    # return total count and file schema list
    file_total = session.query(File).count()
    return RespFileList(data_file_total=file_total, data_file_list=file_schema_list)


@router.get("/user/{user_id}", response_model=RespFileList)
def _get_file_schema_list(user_id: str = Path(..., description="user id"),
                          skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          session: Session = Depends(get_session)):
    """
    get file schema list by user_id, support pagination
    """
    filter0 = File.user_id == user_id

    # get file model list and schema list
    file_model_list = session.query(File).filter(filter0).offset(skip).limit(limit).all()
    file_schema_list = [FileSchema(**file_model.dict()) for file_model in file_model_list]

    # return total count and file schema list
    file_total = session.query(File).filter(filter0).count()
    return RespFileList(data_file_total=file_total, data_file_list=file_schema_list)
