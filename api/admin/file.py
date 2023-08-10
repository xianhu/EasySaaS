# _*_ coding: utf-8 _*_

"""
admin api (file)
"""

from ..base import *
from ..utils import get_current_user_admin

# define router
router = APIRouter()


# response model
class RespFile(Resp):
    data_file: Optional[FileSchema] = Field(None)


# response model
class RespFileList(Resp):
    data_file_list: List[FileSchema] = Field([])


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          current_user: User = Depends(get_current_user_admin),
                          session: Session = Depends(get_session)):
    """
    get file schema list
    """
    # get file model list and schema list
    file_model_list = session.query(File).offset(skip).limit(limit).all()
    file_schema_list = [FileSchema(**fm.dict()) for fm in file_model_list]

    # return file schema list
    return RespFileList(data_file_list=file_schema_list)
