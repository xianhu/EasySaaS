# _*_ coding: utf-8 _*_

"""
utils of security
"""

from datetime import datetime, timedelta
from typing import Optional, Union

from jose import jwt
from passlib.context import CryptContext

from ..settings import settings

# global
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt", ], deprecated="auto")


def create_sub_token(sub: Union[str, int], expires_duration: int = None) -> str:
    """
    create token based on sub and expires_duration
    """
    seconds = expires_duration or settings.ACCESS_TOKEN_EXPIRE_DURATION
    expire = datetime.utcnow() + timedelta(seconds=seconds)

    # sub and exp is remained keys in jwt
    payload = {"sub": str(sub), "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    # return
    return token


def get_token_sub(token: str) -> Optional[str]:
    """
    get sub from token, return None if token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except jwt.JWTError:
        payload = None

    # return sub or None
    return payload["sub"] if payload else None


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
