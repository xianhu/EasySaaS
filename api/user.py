# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import User, get_db
from models.crud import crud_user
from models.schemas import UserSchema, UserUpdate
from .utils import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def _me(current_user: User = Depends(get_current_user)):
    """
    get current user's schema
    """
    return UserSchema(**current_user.to_dict())


@router.put("/me", response_model=UserSchema)
def _update_me(user_schema: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    update current user's schema
    """
    crud_user.update(db, obj_db=current_user, obj_schema=user_schema)
    return UserSchema(**current_user.to_dict())
