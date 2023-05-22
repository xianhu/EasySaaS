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
    check access_token, return user model or raise exception(401)
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
