# _*_ coding: utf-8 _*_

"""
filetag api
"""

from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from data import get_session
from data.models import FileTag, User
from data.schemas import FileTagCreate, FileTagSchema, FileTagUpdate, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFileTag(Resp):
    data: List[FileTagSchema] = []


@router.post("/create", response_model=RespFileTag)
def _create(filetag_schema: FileTagCreate = Body(..., description="create schema"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    create filetag based on create schema
    - **status=0**: create success
    - **status=-1**: filetag existed
    """
    # get filetags of current_user
    filetag_model_list = session.query(FileTag).filter(
        FileTag.user_id == current_user.id,
    ).all()

    # check if filetag existed
    for filetag_model in filetag_model_list:
        if filetag_model.name == filetag_schema.name:
            return Resp(status=-1, msg="filetag existed")

    # create filetag model
    filetag_model = FileTag(user_id=current_user.id, **filetag_schema.dict(exclude_unset=True))
    session.add(filetag_model)
    session.commit()

    # return
    return Resp()


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
    # return FiletagSchema
    return RespFileTag()
