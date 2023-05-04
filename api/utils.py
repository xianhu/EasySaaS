# _*_ coding: utf-8 _*_

"""
utils functions
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import get_token_sub
from models import User, get_db
from models.crud import crud_user

# define OAuth2PasswordBearer
token_url = "/api/auth/access-token"
oauth2 = OAuth2PasswordBearer(tokenUrl=token_url)


def get_current_user(access_token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    """
    check access_token, return user model or raise exception
    """
    # check access_token and get user_id
    user_id = get_token_sub(access_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_tips.TOKEN_INVALID,
        )

    # check user by user_id
    user_db = crud_user.get(db, _id=user_id)
    if not (user_db and user_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_tips.USER_NOT_EXISTED,
        )

    # return
    return user_db


def user_existed(email: str, db: Session) -> Optional[User]:
    """
    check user existed by email, return user model or raise exception
    """
    user_db = crud_user.get_by_email(db, email=email)
    if not (user_db and user_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.USER_NOT_EXISTED,
        )
    return user_db


def user_not_existed(email: str, db: Session) -> Optional[User]:
    """
    check user existed by email, return user model or raise exception
    """
    user_db = crud_user.get_by_email(db, email=email)
    if user_db and user_db.status is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.USER_EXISTED,
        )
    return user_db
