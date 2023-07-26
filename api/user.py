# _*_ coding: utf-8 _*_

"""
user api
"""

from typing import List

from fastapi import APIRouter, Body, Depends
from pydantic import Field
from sqlalchemy.orm import Session

from core.security import check_password_hash, get_password_hash
from data import get_session
from data.models import User
from data.schemas import FileTagSchema, Resp
from data.schemas import UserSchema, UserUpdate
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data_user: UserSchema = Field(None)
    data_filetag_list: List[FileTagSchema] = Field(None)


@router.get("/me", response_model=RespUser)
def _get_me(current_user: User = Depends(get_current_user)):
    """
    get user schema and filetag schema list
    """
    # filetag schema list
    filetag_schema_list = []
    for filetag_model in current_user.filetags:
        filetag_schema = FileTagSchema(**filetag_model.dict())
        filetag_schema_list.append(filetag_schema)

    # return user schema and filetag schema list
    user_schema = UserSchema(**current_user.dict())
    return RespUser(data_user=user_schema, data_filetag_list=filetag_schema_list)


@router.patch("/me", response_model=RespUser)
def _patch_me(user_schema: UserUpdate = Body(..., description="update schema"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    update user model, return user schema
    """
    # update user model based on update schema
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(current_user, field, getattr(user_schema, field))
    session.merge(current_user)
    session.commit()

    # return user schema
    user_schema = UserSchema(**current_user.dict())
    return RespUser(data_user=user_schema, data_filetag_list=[])


@router.post("/password", response_model=RespUser)
def _post_password(password_old: str = Body(..., description="old password"),
                   password_new: str = Body(..., min_length=6, max_length=20),
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """
    update password of current_user, return user schema
    - **status=-1**: password_old incorrect
    """
    # check password of user_model
    if not check_password_hash(password_old, current_user.password):
        return RespUser(status=-1, msg="password_old incorrect")
    pwd_hash = get_password_hash(password_new)

    # update password of current_user
    current_user.password = pwd_hash
    session.merge(current_user)
    session.commit()

    # return user schema
    user_schema = UserSchema(**current_user.dict())
    return RespUser(data_user=user_schema, data_filetag_list=[])
