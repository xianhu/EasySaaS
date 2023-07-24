# _*_ coding: utf-8 _*_

"""
utility functions used for api
"""

import time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import get_jwt_payload
from core.utils import get_id_string
from data import get_session
from data.models import FILETAG_SYSTEM_SET
from data.models import FileTag, User

# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(access_token: str = Depends(oauth2),
                     session: Session = Depends(get_session)) -> User:
    """
    check access_token, return user model
    - **status_code=401**: token invalid
    """
    # get payload from access_token
    payload = get_jwt_payload(access_token)

    # check if user_id existed or raise exception
    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )
    user_id = payload["sub"]

    # check if user existed or raise exception
    user_model = session.query(User).get(user_id)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )

    # return user
    return user_model

