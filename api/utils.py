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
    # get user_id from access_token
    user_id = get_token_sub(access_token)
    if user_id:
        # check user by user_id
        user_model = crud_user.get(session, _id=user_id)
        if user_model:
            return user_model

    # raise exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_tips.TOKEN_INVALID,
    )


def user_existed(email: str, session: Session) -> User:
    """
    ensure user existed, return user model or raise exception
    """
    user_model = crud_user.get_by_email(session, email=email)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )
    return user_model


def user_not_existed(email: str, session: Session) -> True:
    """
    ensure user not existed, return True or raise exception
    """
    user_model = crud_user.get_by_email(session, email=email)
    if user_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_EXISTED,
        )
    return True
