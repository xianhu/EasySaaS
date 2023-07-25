# _*_ coding: utf-8 _*_

"""
file api
"""

from fastapi import APIRouter
from fastapi import Body, Depends, Path
from pydantic import Field
from sqlalchemy.orm import Session

from data import get_session
from data.models import File, User
from data.schemas import FileSchema, FileUpdate, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFile(Resp):
    data: FileSchema = Field(None)


@router.patch("/{file_id}", response_model=RespFile)
def _patch(file_id: str = Path(..., description="id of file"),
           file_schema: FileUpdate = Body(..., description="update schema"),
           current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    """
    update file model based on update schema, return file schema
    - **status=-1**: file not existed
    """
    # check if file existed
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != current_user.id):
        return Resp(status=-1, msg="file not existed")

    # update file model
    for field in file_schema.model_dump(exclude_unset=True):
        setattr(file_model, field, getattr(file_schema, field))
    session.merge(file_model)
    session.commit()

    # return file schema with permission
    return RespFile(data=FileSchema(**file_model.dict()))
