# _*_ coding: utf-8 _*_

"""
security file
"""

import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from core.settings import settings

# define algorithm
ALGORITHM = "HS256"

# define password context
pwd_context = CryptContext(schemes=["bcrypt", ], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_minutes: int = None) -> str:
    """
    create access token, and return
    """
    minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=minutes)

    # sub and exp is remained keys in jwt
    pyload = {"sub": str(subject), "exp": expire}
    token = jwt.encode(pyload, settings.SECRET_KEY, algorithm=ALGORITHM)

    # return
    return token


def verify_access_token(token: str) -> Optional[str]:
    """
    verify access token, return subject or None
    """
    try:
        pyload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except jwt.JWTError:
        pyload = None

    # return
    return pyload["sub"] if pyload else None


def check_password_hash(pwd_plain: str, pwd_hash: str) -> bool:
    """
    check password hash
    """
    return pwd_context.verify(pwd_plain, pwd_hash)


def get_password_hash(pwd_plain: str) -> str:
    """
    get password hash
    """
    return pwd_context.hash(pwd_plain)


def get_md5(source: str) -> str:
    """
    get md5 of source
    """
    str_encode = source.encode()
    return hashlib.md5(str_encode).hexdigest()
