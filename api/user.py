# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter, Depends

from models import User
from models.schemas import UserSchema
from .utils import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def _me(current_user: User = Depends(get_current_user)):
    """
    get current user's info
    """
    return current_user.to_dict()


@router.get("/{user_id}", response_model=UserSchema)
def _get_user(user_id: int):
    """
    get user's info
    """
    return User.get_by_id(user_id).to_dict()
