# _*_ coding: utf-8 _*_

"""
utils functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from core.security import get_token_payload
from core.settings import error_tips
from data import get_session
from data.crud import crud_user
from data.models import User

# define OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/access-token",
    scopes={
        "user:read": "Read users.",
        "user:write": "Write users.",
        "files": "Upload or Download files.",
    },
)


def get_current_user(security_scopes: SecurityScopes,
                     access_token: str = Depends(oauth2),
                     session: Session = Depends(get_session)) -> User:
    """
    check security_scopes and access_token, return user model or raise exception(401)
    """
    # define authenticate_value
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        scope_str = security_scopes.scope_str
        authenticate_value = f"Bearer scope=\"{scope_str}\""

    # define credentials_exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_tips.TOKEN_INVALID,
        headers={"WWW-Authenticate": authenticate_value},
    )

    # get payload from access_token
    payload = get_token_payload(access_token)
    user_id, scopes = payload.get("sub"), payload.get("scopes", [])
    if not user_id:
        raise credentials_exception

    # check user scopes
    for scope in security_scopes.scopes:
        if scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_tips.TOKEN_INVALID,
                headers={"WWW-Authenticate": authenticate_value},
            )

    # get user model
    user_model = crud_user.get(session, _id=user_id)
    if not user_model:
        raise credentials_exception

    # return user
    return user_model
