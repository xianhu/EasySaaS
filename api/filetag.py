# _*_ coding: utf-8 _*_

"""
filetag api
"""
import hashlib
import time
from typing import List

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
    - **status=-1**: filetag name invalid
    """
    # check if filetag name is valid
    if filetag_schema.name == "default":
        return Resp(status=-1, msg="filetag name invalid")

    # check if filetag name not existed
    for filetag_model in current_user.filetags:
        if filetag_schema.name == filetag_model.name:
            return Resp(status=-1, msg="filetag name invalid")
    user_id = current_user.id
    _id = hashlib.md5(f"{user_id}-{time.time()}".encode()).hexdigest()
    filetag_params = filetag_schema.model_dump(exclude_unset=True)

    # create custom filetag model and save to database
    filetag_model = FileTag(id=_id, user_id=user_id, **filetag_params)
    session.add(filetag_model)
    session.commit()

    # return RespFileTag
    return RespFileTag(data=FileTagSchema(**filetag_model.dict()))


@router.post("/update", response_model=RespFileTag)
def _update(filetag_schema: FileTagUpdate = Body(..., description="update schema"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    update filetag based on update schema
    - **status=0**: update success
    - **status=-1**: filetag name invalid
    - **status=-2**: filetag not existed
    """
    # check if filetag name is valid
    if filetag_schema.name == "default":
        return Resp(status=-1, msg="filetag name invalid")

    # check if filetag name not existed
    for filetag_model in current_user.filetags:
        if filetag_schema.name == filetag_model.name:
            return Resp(status=-1, msg="filetag name invalid")

    # check if filetag id existed
    for filetag_model in current_user.filetags:
        if filetag_model.ttype != "custom":
            continue
        if filetag_schema.id == filetag_model.id:
            # update filetag model based on FileTagUpdate
            for field in filetag_schema.model_dump(exclude_unset=True):
                setattr(filetag_model, field, getattr(filetag_schema, field))
            session.merge(filetag_model)
            session.commit()
            return RespFileTag(data=FileTagSchema(**filetag_model.dict()))

    # return -2 (filetag not existed)
    return RespFileTag(status=-2, msg="filetag not existed")


@router.post("/delete", response_model=RespFileTag)
def _delete(filetag_id: int = Body(..., embed=True, description="id of filetag"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    delete filetag based on filetag id
    - **status=0**: delete success
    - **status=-2**: filetag not existed
    """
    # check if filetag id existed
    for filetag_model in current_user.filetags:
        if filetag_model.ttype != "custom":
            continue
        if filetag_id == filetag_model.id:
            # delete filetag model
            session.delete(filetag_model)
            session.commit()
            return RespFileTag(data=FileTagSchema(**filetag_model.dict()))

    # return -2 (filetag not existed)
    return RespFileTag(status=-2, msg="filetag not existed")


# response model
class RespFileTagList(Resp):
    data: List[FileTagSchema] = Field(None)


@router.get("/list", response_model=RespFileTagList)
def _list(current_user: User = Depends(get_current_user)):
    """
    get filetag schema list
    - **status=0**: get success
    """
    filetag_schema_list = []
    for filetag_model in current_user.filetags:
        filetag_schema = FileTagSchema(**filetag_model.dict())
        filetag_schema_list.append(filetag_schema)

    # return RespFileTagList
    return RespFileTagList(data=filetag_schema_list)
