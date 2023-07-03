# _*_ coding: utf-8 _*_

"""
utils functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import get_token_payload
from core.settings import error_tips
from data import get_session
from data.models import User

# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(access_token: str = Depends(oauth2),
                     session: Session = Depends(get_session)) -> User:
    """
    check access_token, return user model or raise exception(401)
    """
    # get payload from access_token
    payload = get_token_payload(access_token)

    # check user_id(sub)
    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.TOKEN_INVALID,
        )
    user_id = int(payload["sub"])

    # get user_model and check
    user_model = session.query(User).get(user_id)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.TOKEN_INVALID,
        )

    # return user
    return user_model


def iter_file(file_path: str) -> iter:
    """
    iter file, yield chunk
    """
    with open(file_path, "rb") as file_in:
        while True:
            chunk = file_in.read(1024 * 1024)
            if not chunk:
                break
            yield chunk
