# _*_ coding: utf-8 _*_

"""
utils functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.utils.security import get_token_sub
from models import User, get_db
from models.crud import crud_user

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2)) -> User:
    """
    get current user
    """
    user_id = get_token_sub(token)

    # check token
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

    # check user
    user_db = crud_user.get(db, _id=user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # return
    return user_db
