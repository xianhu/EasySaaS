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


@router.get("/me", response_model=RespUser)
def _get_me(current_user: User = Depends(get_current_user)):
    """
    get schema of current_user, return user schema
    """
    # get user_model
    user_model = current_user

    # return user schema
    return RespUser(data=UserSchema(**user_model.dict()))


@router.patch("/me", response_model=RespUser)
def _patch_me(user_schema: UserUpdate = Body(..., description="update schema"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    update schema of current_user, return user schema
    """
    # get user_model
    user_model = current_user

    # update user_model based on update schema
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(user_model, field, getattr(user_schema, field))
    session.merge(user_model)
    session.commit()

    # return user schema
    return RespUser(data=UserSchema(**user_model.dict()))


@router.post("/password", response_model=RespUser)
def _post_password(password_old: str = Body(..., description="old password"),
                   password_new: str = Body(..., min_length=6, max_length=20),
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """
    update password of current_user, return user schema
    - **status=-1**: password_old incorrect
    """
    # get user_model
    user_model = current_user

    # check password of user_model
    if not check_password_hash(password_old, user_model.password):
        return Resp(status=-1, msg="password_old incorrect")
    pwd_hash = get_password_hash(password_new)

    # update password of user_model
    user_model.password = pwd_hash
    session.merge(user_model)
    session.commit()

    # return user schema
    return RespUser(data=UserSchema(**user_model.dict()))
