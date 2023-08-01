# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Depends
from pydantic import Field
from sqlalchemy.orm import Session

from core.security import check_password_hash, get_password_hash
from core.settings import settings
from data import get_session
from data.models import User
from data.schemas import Resp, UserSchema, UserUpdate
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data_user: UserSchema = Field(None)


@router.get("/me", response_model=RespUser)
def _get_user_schema(current_user: User = Depends(get_current_user)):
    """
    get current_user schema
    """
    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.patch("/me", response_model=RespUser)
def _update_user_model(user_schema: UserUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update current_user model based on update schema, return user schema
    """
    # update user model based on update schema
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(current_user, field, getattr(user_schema, field))
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.post("/me/password", response_model=RespUser)
def _update_user_password(password_old: str = Body(..., description="old password"),
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
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.delete("/me", response_model=RespUser)
def _delete_user_model(current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    delete current_user model, return user schema (only in DEBUG mode)
    """
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="can not delete user model",
        )

    # delete user model
    session.delete(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))
