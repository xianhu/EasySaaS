# _*_ coding: utf-8 _*_

"""
filetag api
"""

import time
from typing import List

from fastapi import APIRouter, Depends
from fastapi import Body, Path, Query
from pydantic import Field
from sqlalchemy.orm import Session

from core.utils import get_id_string
from data import get_session
from data.models import FILETAG_SYSTEM_SET, FileTag, User
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


@router.post("/", response_model=RespFileTag)
def _post(filetag_schema: FileTagCreate = Body(..., description="create schema"),
          current_user: User = Depends(get_current_user),
          session: Session = Depends(get_session)):
    """
    create filetag model based on create schema, return filetag schema
    - **status=-1**: filetag name invalid or existed
    """
    # check if filetag name is valid
    if filetag_schema.name in FILETAG_SYSTEM_SET:
        return RespFileTag(status=-1, msg="filetag name invalid")
    filetag_name = filetag_schema.name

    # check if filetag name not existed
    for filetag_model in current_user.filetags:
        if filetag_name != filetag_model.name:
            continue
        return RespFileTag(status=-1, msg="filetag name existed")
    user_id = current_user.id

    # create filetag variables
    filetag_id = get_id_string(f"{user_id}-{filetag_name}-{time.time()}")
    filetag_kwargs = filetag_schema.model_dump(exclude_unset=True)

    # create filetag model and save to database
    filetag_model = FileTag(id=filetag_id, user_id=current_user.id, **filetag_kwargs)
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
    update filetag model based on update schema, return filetag schema
    - **status=-1**: filetag name invalid or existed
    - **status=-2**: filetag not existed in current_user
    """
    # check if filetag name is valid
    if filetag_schema.name in FILETAG_SYSTEM_SET:
        return RespFileTag(status=-1, msg="filetag name invalid")
    filetag_name = filetag_schema.name

    # check if filetag name not existed
    for filetag_model in current_user.filetags:
        if filetag_name != filetag_model.name:
            continue
        return RespFileTag(status=-1, msg="filetag name existed")
    user_id = current_user.id

    # check if filetag existed in current_user
    filetag_model = session.query(FileTag).get(filetag_id)
    if (not filetag_model) or (filetag_model.user_id != user_id):
        return RespFileTag(status=-2, msg="filetag not existed")
    if filetag_model.ttype != "custom":
        return RespFileTag(status=-2, msg="filetag not existed")

    # update filetag model based on update schema
    for field in filetag_schema.model_dump(exclude_unset=True):
        setattr(filetag_model, field, getattr(filetag_schema, field))
    session.merge(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data=FileTagSchema(**filetag_model.dict()))


@router.get("/", response_model=RespFileTagList)
def _get_list(skip: int = Query(0, description="skip count"),
              limit: int = Query(10, description="limit count"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    get filetag schema list and return
    """
    # get filetag model list
    filetag_model_list = session.query(FileTag).filter(
        FileTag.user_id == current_user.id,
    ).offset(skip).limit(limit).all()

    # get filetag schema list
    filetag_schema_list = []
    for filetag_model in filetag_model_list:
        filetag_schema = FileTagSchema(**filetag_model.dict())
        filetag_schema_list.append(filetag_schema)

    # return filetag schema list
    return RespFileTagList(data=filetag_schema_list)


@router.get("/{filetag_id}", response_model=RespFileTag)
def _get_one(filetag_id: str = Path(..., description="id of filetag"),
             current_user: User = Depends(get_current_user),
             session: Session = Depends(get_session)):
    """
    get filetag schema by id and return
    - **status=-2**: filetag not existed in current_user
    """
    user_id = current_user.id

    # check if filetag existed in current_user
    filetag_model = session.query(FileTag).get(filetag_id)
    if (not filetag_model) or (filetag_model.user_id != user_id):
        return RespFileTag(status=-2, msg="filetag not existed")
    if filetag_model.ttype != "custom":
        return RespFileTag(status=-2, msg="filetag not existed")

    # return filetag schema
    return RespFileTag(data=FileTagSchema(**filetag_model.dict()))


@router.delete("/{filetag_id}", response_model=RespFileTag)
def _delete(filetag_id: str = Path(..., description="id of filetag"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    delete filetag model by id and return
    - **status=-2**: filetag not existed in current_user
    - **status=-3**: filetag not empty with file
    """
    user_id = current_user.id

    # check if filetag existed in current_user
    filetag_model = session.query(FileTag).get(filetag_id)
    if (not filetag_model) or (filetag_model.user_id != user_id):
        return RespFileTag(status=-2, msg="filetag not existed")
    if filetag_model.ttype != "custom":
        return RespFileTag(status=-2, msg="filetag not existed")

    # check if filetag not empty
    if filetag_model.filetagfiles:
        return RespFileTag(status=-3, msg="filetag not empty with file")

    # delete filetag model
    session.delete(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data=FileTagSchema(**filetag_model.dict()))
