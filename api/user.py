# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter, Body, Depends
from pydantic import Field
from sqlalchemy.orm import Session

from core.security import check_password_hash, get_password_hash
from data import get_session
from data.models import User
from data.schemas import Resp, UserSchema, UserUpdate
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data: UserSchema = Field(None)


@router.get("/get", response_model=RespUser)
def _get(current_user: User = Depends(get_current_user)):
    """
    get schema of current_user
    - **status=0**: get success
    """
    # get user_model
    user_model = current_user

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))


@router.post("/update", response_model=RespUser)
def _update(user_schema: UserUpdate = Body(..., description="update schema"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    update current_user based on update schema
    - **status=0**: update success
    """
    # get user_model
    user_model = current_user

    # update user based on UserUpdate
    for field in user_schema.dict(exclude_unset=True):
        setattr(user_model, field, getattr(user_schema, field))
    session.merge(user_model)
    session.commit()

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))


@router.post("/update/password", response_model=RespUser)
def _update_password(password_old: str = Body(..., description="old password"),
                     password_new: str = Body(..., min_length=6, max_length=20),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    update password of current_user
    - **status=0**: update success
    - **status=-1**: old password error
    """
    # get user_model
    user_model = current_user

    # check password of user_model
    if not check_password_hash(password_old, user_model.password):
        return Resp(status=-1, msg="password incorrect")
    pwd_hash = get_password_hash(password_new)

    # update password of user_model
    user_model.password = pwd_hash
    session.merge(user_model)
    session.commit()

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))
