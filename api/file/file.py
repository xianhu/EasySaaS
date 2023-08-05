# _*_ coding: utf-8 _*_

"""
file api
"""

from .utils import RespFile, RespFileList, check_file_permission, get_filetag_id_list
from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    get file schema list and filetag_id list list of current_user
    """
    user_id = current_user.id
    _filter = File.user_id == user_id

    # get file model list and schema list
    file_model_list = session.query(File).filter(_filter).offset(skip).limit(limit).all()
    file_schema_list = [FileSchema(**file_model.dict()) for file_model in file_model_list]

    # filetag_id list list
    filetag_id_list_list = []
    for file_model in file_model_list:
        filetag_id_list = get_filetag_id_list(file_model.id, session)
        filetag_id_list_list.append(filetag_id_list)

    # return file schema list and filetag_id list list
    return RespFileList(data_file_list=file_schema_list, data_filetag_id_list_list=filetag_id_list_list)


@router.patch("/{file_id}", response_model=RespFile)
def _update_file_model(file_id: str = Path(..., description="id of file"),
                       file_schema: FileUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update file model based on update schema, return file schema
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # update file model based on update schema
    for field in file_schema.model_dump(exclude_unset=True):
        setattr(file_model, field, getattr(file_schema, field))
    session.merge(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.post("/trash/{file_id}", response_model=RespFile)
def _trash_file_model(file_id: str = Path(..., description="id of file"),
                      current_user: User = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    """
    trash file model by id, return file schema
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # update file model
    file_model.is_trash = True
    file_model.trash_time = datetime.utcnow()
    session.merge(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.post("/untrash/{file_id}", response_model=RespFile)
def _untrash_file_model(file_id: str = Path(..., description="id of file"),
                        current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    """
    untrash file model by id, return file schema
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # update file model
    file_model.is_trash = False
    file_model.trash_time = None
    session.merge(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.delete("/", response_model=Resp)
def _delete_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                            current_user: User = Depends(get_current_user),
                            session: Session = Depends(get_session)):
    """
    delete file model list by id list
    """
    session.query(File).filter(
        File.id.in_(file_id_list),
        File.user_id == current_user.id,
        File.is_trash == True,
    ).delete()
    session.commit()
    return Resp(msg="delete success")
