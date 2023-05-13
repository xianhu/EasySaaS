# _*_ coding: utf-8 _*_

"""
utils functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import get_token_sub
from data import get_session
from data.crud import crud_user
from data.models import User

# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(access_token: str = Depends(oauth2), session: Session = Depends(get_session)) -> User:
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
    user_db = crud_user.get(session, _id=user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )

    # return
    return user_db


def user_existed(email: str, session: Session = Depends(get_session)) -> User:
    """
    check if user existed by email, raise exception or return user model
    """
    user_db = crud_user.get_by_email(session, email=email)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )
    return user_db


def user_not_existed(email: str, session: Session = Depends(get_session)) -> None:
    """
    check if user not existed by email, raise exception or return None
    """
    user_db = crud_user.get_by_email(session, email=email)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_EXISTED,
        )
    return None
