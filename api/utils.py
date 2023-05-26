# _*_ coding: utf-8 _*_

"""
utils functions
"""
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import get_token_payload
from data import get_session
from data.crud import crud_user
from data.models import User

# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/access-token",
    scopes={
        "user:read": "Read users.",
        "user:write": "Write users.",
    },
)


def get_current_user(security_scopes: SecurityScopes,
                     access_token: str = Depends(oauth2),
                     session: Session = Depends(get_session)) -> User:
    """
    check security_scopes and access_token, return user model or raise exception(401)
    """
    # define auth_value
    auth_value = "Bearer"
    if security_scopes.scopes:
        auth_value = f'Bearer scope="{security_scopes.scope_str}"'
    logging.warning("auth_value: %s", auth_value)
    logging.warning("access_token: %s", access_token)
    logging.warning(security_scopes.scopes)
    logging.warning(security_scopes.scope_str)

    # define credentials_exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_tips.TOKEN_INVALID,
        headers={"WWW-Authenticate": auth_value},
    )

    # get payload from access_token
    payload = get_token_payload(access_token)
    user_id, user_scopes = payload.get("sub"), payload.get("scopes", [])
    if not user_id:
        raise credentials_exception

    user_model = crud_user.get(session, _id=user_id)
    if not user_model:
        raise credentials_exception

    # check user scopes
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_tips.TOKEN_INVALID,
                headers={"WWW-Authenticate": auth_value},
            )

    # return user
    return user_model
