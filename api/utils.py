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
    check access_token based on token in redis, return user model
    - **status_code=401**: token invalid or expired
    """
    # get payload from access_token
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid or expired",
    )
    payload = get_jwt_payload(access_token)

    # check if user_id exist in payload
    if (not payload) or (not payload.get("sub")):
        raise exception
    user_id = payload["sub"]

    # get token by user_id and client_id
    client_id = payload.get("client_id", "web")
    rd_token = rd_conn.get(f"{settings.APP_NAME}-access-{client_id}-{user_id}")

    # check if access_token match token in redis
    if (not rd_token) or (access_token != rd_token):
        raise exception
    user_model = session.query(User).get(user_id)

    # check if user exist or raise exception
    if (not user_model) or (user_model.status != 1):
        raise exception

    # return user
    return user_model
