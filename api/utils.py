# _*_ coding: utf-8 _*_

"""
utility functions used for api
"""

import time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import get_jwt_payload
from core.utility import get_id_string
from data import get_session
from data.models import FILETAG_DEFAULT_SET
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


def init_current_user(email: str, pwd_hash: str, session: Session = Depends(get_session)) -> User | None:
    """
    init current_user
    """
    try:
        user_id = get_id_string(f"{email}-{time.time()}")
        user_model = User(id=user_id, email=email, password=pwd_hash, email_verified=True)
        session.add(user_model)

        for filetag_name in FILETAG_DEFAULT_SET:
            filetag_id = get_id_string(f"{user_model.id}-{filetag_name}-{time.time()}")
            filetag_model = FileTag(id=filetag_id,
                                    user_id=user_model.id,
                                    name=filetag_name,
                                    ttype="system")
            session.add(filetag_model)

        session.commit()
    except Exception as excep:
        session.rollback()
        return None

    return user_model
