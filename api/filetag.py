# _*_ coding: utf-8 _*_

"""
filetag api
"""

from fastapi import APIRouter, Body, Depends
from pydantic import Field
from sqlalchemy.orm import Session

from data import get_session
from data.models import FileTag, User
from data.schemas import FileTagCreate, FileTagSchema, FileTagUpdate, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFileTag(Resp):
    data: FileTagSchema = Field(None)


@router.post("/create", response_model=RespFileTag)
def _create(filetag_schema: FileTagCreate = Body(..., description="create schema"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    create filetag based on create schema
    - **status=0**: create success
    - **status=-1**: filetag existed
    """
    # check if filetag existed
    for filetag_model in current_user.filetags:
        if filetag_model.name == filetag_schema.name:
            return Resp(status=-1, msg="filetag existed")
    filetag_params = filetag_schema.dict(exclude_unset=True)

    # create filetag model and save to database
    filetag_model = FileTag(user_id=current_user.id, **filetag_params)
    session.add(filetag_model)
    session.commit()

    # return RespFileTag
    return FileTagSchema(**filetag_model.to_dict())


@router.post("/delete", response_model=Resp)
def _delete(filetag_id: int = Body(..., description="id of filetag"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    delete filetag
    - **status=0**: data=None
    """

    # return Resp
    return Resp()


@router.post("/update", response_model=Resp)
def _update(filetag_schema: FileTagUpdate = Body(..., description="update schema"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    update filetag
    - **status=0**: data=None
    """
    # return Resp
    return Resp()


@router.get("/list", response_model=RespFileTag)
def _list(current_user: User = Depends(get_current_user),
          session: Session = Depends(get_session)):
    """
    get filetag
    - **status=0**: data=FiletagSchema
    """

    # data of response
    filetag_schema_list = []
    session.refresh(current_user)
    for filetag_model in current_user.filetags:
        filetag_schema = FileTagSchema(**filetag_model.to_dict())
        filetag_schema_list.append(filetag_schema)

    # return FiletagSchema

    return RespFileTag()
