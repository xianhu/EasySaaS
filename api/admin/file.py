# _*_ coding: utf-8 _*_

"""
admin api of file
"""

from ..base import *
from ..file.utils import RespFileList, get_filetag_id_list

# define router
router = APIRouter()


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          session: Session = Depends(get_session)):
    """
    get file schema list, support pagination
    """
    # get file schema list
    file_schema_list = []
    for file_model in (session.query(File)
            .order_by(File.created_at.desc())
            .offset(skip).limit(limit).all()):
        file_schema = FileSchema(**file_model.dict())
        file_schema.filetag_id_list = get_filetag_id_list(file_model.id, session)
        file_schema_list.append(file_schema)

    # return total count and file schema list
    file_total = session.query(File).count()
    return RespFileList(data_file_total=file_total, data_file_list=file_schema_list)
