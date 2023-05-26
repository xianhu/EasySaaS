# _*_ coding: utf-8 _*_

"""
utils of security
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext

from ..settings import settings

# global
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt", ], deprecated="auto")


def create_token_data(data: Dict[str, Any], expires_duration: int = None) -> str:
    """
    create token based on data and expires_duration
    :param data: {"sub": user_id, "scopes": ["user:read", ...,], ...}
    :param expires_duration: seconds, default ACCESS_TOKEN_EXPIRE_DURATION
    """
    # define expire value
    seconds = expires_duration or settings.ACCESS_TOKEN_EXPIRE_DURATION
    expire = datetime.utcnow() + timedelta(seconds=seconds)

    # define payload and token
    payload = {**data, "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    # return
    return token


def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    get payload from token, return None if token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except jwt.JWTError:
        payload = None

    # return
    return payload


def get_password_hash(pwd_plain: str) -> str:
    """
    get hash value of password
    """
    return pwd_context.hash(pwd_plain)


def check_password_hash(pwd_plain: str, pwd_hash: str) -> bool:
    """
    check password with hash value
    """
    return pwd_context.verify(pwd_plain, pwd_hash)
