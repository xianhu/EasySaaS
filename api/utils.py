# _*_ coding: utf-8 _*_

"""
utils functions
"""
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import get_token_data
from data import get_session
from data.crud import crud_user
from data.models import User
from data.schemas import TokenData

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
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    logging.warning(security_scopes.scopes)
    logging.warning(security_scopes.scope_str)

    # get data from access_token
    payload = get_token_data(access_token)

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_scopes = payload.get("scopes", [])
    token_data = TokenData(scopes=token_scopes, user_id=payload.get("user_id"), user_name=payload.get("user_name"))
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
