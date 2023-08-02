# _*_ coding: utf-8 _*_

"""
file api
"""

from fastapi import APIRouter
from fastapi import Body, Depends, Path, Query
from sqlalchemy.orm import Session

from data import get_session
from data.models import File, User
from data.schemas import FileSchema, FileUpdate
from .utils import RespFile, RespFileList
from .utils import check_file_permission, get_filetag_id_list
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

    # get file model list
    file_model_list = session.query(File).filter(
        File.user_id == user_id,
    ).offset(skip).limit(limit).all()

    # file schema list and filetag_id list list
    file_schema_list, filetag_id_list_list = [], []
    for file_model in file_model_list:
        # define file schema and append to list
        file_schema = FileSchema(**file_model.dict())
        file_schema_list.append(file_schema)

        # define filetag_id list and append to list
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


@router.delete("/{file_id}", response_model=RespFile)
def _delete_file_model(file_id: str = Path(..., description="id of file"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    delete file model by id, return file schema
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    # delete file from disk and delete filetagfile model if necessary

    # delete file model
    session.delete(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])
