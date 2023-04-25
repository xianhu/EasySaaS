# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import get_db
from models.schemas import UserSchema
from .utils import get_current_user

router = APIRouter()


@router.post("/me", response_model=UserSchema)
def user_me(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    """
    login to get access token
    """
    return UserSchema(**current_user.dict())
