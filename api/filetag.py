# _*_ coding: utf-8 _*_

"""
filetag api
"""

import hashlib
import time
from typing import List

from fastapi import APIRouter, Body, Depends, Path
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


# response model
class RespFileTagList(Resp):
    data: List[FileTagSchema] = Field(None)


# global variable of default filetag name set
FILETAG_DEFAULT_SET = {"default", "all", "untagged", "favorite"}


@router.post("/", response_model=RespFileTag)
def _post(filetag_schema: FileTagCreate = Body(..., description="create schema"),
          current_user: User = Depends(get_current_user),
          session: Session = Depends(get_session)):
    """
    create filetag based on create schema, return filetag schema
    - **status=0**: create success
    - **status=-1**: filetag name invalid or existed
    """
    # check if filetag name is valid
    if filetag_schema.name in FILETAG_DEFAULT_SET:
        return Resp(status=-1, msg="filetag name invalid")

    # check if filetag name not existed
    for filetag_model in current_user.filetags:
        if filetag_schema.name != filetag_model.name:
            continue
        return Resp(status=-1, msg="filetag name existed")
    user_id = current_user.id
    filetag_id = hashlib.md5(f"{user_id}-{time.time()}".encode()).hexdigest()

    # create custom filetag model and save to database
    filetag_params = filetag_schema.model_dump(exclude_unset=True)
    filetag_model = FileTag(id=filetag_id, user_id=user_id, **filetag_params)
    session.add(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data=FileTagSchema(**filetag_model.dict()))


@router.patch("/{filetag_id}", response_model=RespFileTag)
def _patch(filetag_id: str = Path(..., description="id of filetag"),
           filetag_schema: FileTagUpdate = Body(..., description="update schema"),
           current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    """
    update filetag based on update schema, return filetag schema
    - **status=0**: update success
    - **status=-1**: filetag name invalid or existed
    - **status=-2**: filetag not existed in current_user
    """
    # check if filetag name is valid
    if filetag_schema.name in FILETAG_DEFAULT_SET:
        return Resp(status=-1, msg="filetag name invalid")

    # check if filetag name not existed
    for filetag_model in current_user.filetags:
        if filetag_schema.name != filetag_model.name:
            continue
        return Resp(status=-1, msg="filetag name existed")

    # check if filetag existed
    for filetag_model in current_user.filetags:
        if filetag_model.ttype != "custom":
            continue
        if filetag_id == filetag_model.id:
            # update filetag model based on FileTagUpdate
            for field in filetag_schema.model_dump(exclude_unset=True):
                setattr(filetag_model, field, getattr(filetag_schema, field))
            session.merge(filetag_model)
            session.commit()

            # return filetag schema
            return RespFileTag(data=FileTagSchema(**filetag_model.dict()))

    # return -2 (filetag not existed)
    return RespFileTag(status=-2, msg="filetag not existed")


@router.delete("/{filetag_id}", response_model=RespFileTag)
def _delete(filetag_id: str = Path(..., description="id of filetag"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    delete filetag based on filetag id, return filetag schema
    - **status=0**: delete success
    - **status=-2**: filetag not existed in current_user
    """
    # check if filetag existed
    for filetag_model in current_user.filetags:
        if filetag_model.ttype != "custom":
            continue
        if filetag_id == filetag_model.id:
            # delete filetag model
            session.delete(filetag_model)
            session.commit()

            # return filetag schema
            return RespFileTag(data=FileTagSchema(**filetag_model.dict()))

    # return -2 (filetag not existed)
    return RespFileTag(status=-2, msg="filetag not existed")


@router.get("/", response_model=RespFileTagList)
def _get(current_user: User = Depends(get_current_user)):
    """
    get filetag schema list, return filetag schema list
    - **status=0**: get success
    """
    # get filetag list
    filetag_schema_list = []
    for filetag_model in current_user.filetags:
        filetag_schema = FileTagSchema(**filetag_model.dict())
        filetag_schema_list.append(filetag_schema)

    # return filetag schema list
    return RespFileTagList(data=filetag_schema_list)


@router.get("/{filetag_id}", response_model=RespFileTag)
def _get(filetag_id: str = Path(..., description="id of filetag"),
         current_user: User = Depends(get_current_user)):
    """
    get filetag schema based on filetag id, return filetag schema
    - **status=0**: get success
    - **status=-2**: filetag not existed in current_user
    """
    # get filetag schema
    for filetag_model in current_user.filetags:
        if filetag_id == filetag_model.id:
            filetag_schema = FileTagSchema(**filetag_model.dict())
            return RespFileTag(data=filetag_schema)

    # return -2 (filetag not existed)
    return RespFileTag(status=-2, msg="filetag not existed")
