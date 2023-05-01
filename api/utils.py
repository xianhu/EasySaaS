# _*_ coding: utf-8 _*_

"""
utils functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils import security
from models import User, get_db
from models.crud import crud_user

# define OAuth2PasswordBearer
token_url = "/api/auth/access-token"
oauth2 = OAuth2PasswordBearer(tokenUrl=token_url)


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    """
    check token, return user model or raise exception
    """
    # check token and get user_id
    user_id = security.get_token_sub(token)
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
