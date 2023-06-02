# _*_ coding: utf-8 _*_

"""
utils functions
"""

from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from core.security import get_token_payload
from core.settings import error_tips
from data import get_session
from data.crud import crud_user
from data.models import User


# define enum of scopes
class ScopeName(str, Enum):
    user_read = "user:read"
    user_write = "user:write"
    files_ud = "files:updown"


# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/access-token",
    scopes={scope.value: scope.name for scope in ScopeName},
)


def get_current_user(security_scopes: SecurityScopes,
                     access_token: str = Depends(oauth2),
                     session: Session = Depends(get_session)) -> User:
    """
    check security_scopes and access_token, return user model or raise exception(401)
    """
    # define authenticate
    scope_str = security_scopes.scope_str
    authenticate = f"Bearer scope=\"{scope_str}\""

    # get payload from access_token
    payload = get_token_payload(access_token)

    # check user_id(sub)
    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.TOKEN_INVALID,
            headers={"WWW-Authenticate": authenticate},
        )
    user_id = int(payload["sub"])

    # get user_model from db
    user_model = crud_user.get(session, _id=user_id)

    # check user model
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.TOKEN_INVALID,
            headers={"WWW-Authenticate": authenticate},
        )
    user_scopes = payload.get("scopes", [])

    # check user scopes
    for scope in security_scopes.scopes:  # needed scopes
        if scope not in user_scopes:  # provided scopes by user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_tips.SCOPE_INVALID,
                headers={"WWW-Authenticate": authenticate},
            )

    # return user
    return user_model
