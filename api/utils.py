# _*_ coding: utf-8 _*_

"""
utility functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis import Redis
from sqlalchemy.orm import Session

from core.security import get_jwt_payload
from core.settings import settings
from data import get_redis, get_session
from data.models import User

# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(access_token: str = Depends(oauth2),
                     session: Session = Depends(get_session),
                     rd_conn: Redis = Depends(get_redis)) -> User:
    """
    check access_token, return user model
    - **status_code=401**: token invalid or expired
    """
    # get payload from access_token
    payload = get_jwt_payload(access_token)

    # check if user_id existed
    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid or expired",
        )
    user_id = payload["sub"]

    # check if token valid in redis
    client_id = payload.get("client_id", "web")
    token = rd_conn.get(f"{settings.APP_NAME}-{user_id}-token-{client_id}")
    if (not token) or (access_token != token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid or expired",
        )

    # check if user existed or raise exception
    user_model = session.query(User).get(user_id)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid or expired",
        )

    # return user
    return user_model
