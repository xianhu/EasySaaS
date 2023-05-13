# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from data import get_session
from data.crud import crud_user
from data.models import User
from data.schemas import UserSchema, UserUpdate
from .utils import get_current_user

# define router
router = APIRouter()


@router.get("/get", response_model=UserSchema)
def _get(current_user: User = Depends(get_current_user)):
    """
    get current_user's schema
    """
    return UserSchema(**current_user.to_dict())


@router.post("/update", response_model=UserSchema)
def _update(user_schema: UserUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    update current_user's schema
    """
    current_user = crud_user.update(session, obj_model=current_user, obj_schema=user_schema)
    return UserSchema(**current_user.to_dict())
