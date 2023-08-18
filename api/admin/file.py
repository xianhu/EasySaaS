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
    filter0 = File.is_trash == False

    # get file model list and schema list
    file_model_list = (session.query(File).filter(filter0)
                       .order_by(File.created_at.desc())
                       .offset(skip).limit(limit).all())
    file_schema_list = [FileSchema(**fm.dict()) for fm in file_model_list]

    # return total count and file schema list
    file_total = session.query(File).count()
    return RespFileList(data_file_total=file_total, data_file_list=file_schema_list)
