# _*_ coding: utf-8 _*_

"""
security functions
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

from .settings import settings

# global variables for password context
pwd_context = CryptContext(schemes=["bcrypt", ], deprecated="auto")


def create_jwt_token(subject: str,  # user_id, email, ...
                     audience: str = None,  # client name or id, default None
                     expire_duration: int = settings.ACCESS_TOKEN_EXPIRE_DURATION,
                     secret_key: str = settings.SECRET_KEY,  # secret key
                     algorithm: str = "HS256",  # algorithm of jwt
                     **kwargs) -> str:  # other info to be stored in token
    """
    create jwt token based on subject, audience and expire_duration
    """
    # define expiration time
    issued_at = datetime.utcnow()
    expiration_at = issued_at + timedelta(seconds=expire_duration)

    # define payload - sub, aud, exp, iat, nbf ...
    payload = dict(sub=subject, aud=audience or "",
                   exp=expiration_at, iat=issued_at, **kwargs)
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    # return
    return token


def get_jwt_payload(token: str,  # token value
                    audience: str = None,  # client name or id, default None
                    secret_key: str = settings.SECRET_KEY,  # secret key
                    algorithm: str = "HS256") -> Dict[str, Any]:  # algorithm of jwt
    """
    get payload from token, return payload or {} if failed
    """
    try:
        # decode token and get payload, raise error if audience not match
        payload = jwt.decode(token, secret_key, algorithms=algorithm, audience=audience or "")
    except jwt.JWTError as excep:
        logging.error("get jwt payload error: %s", excep)
        payload = {}

    # return
    return payload


def get_password_hash(pwd_plain: str) -> str:
    """
    get hash value of password
    """
    global pwd_context
    return pwd_context.hash(pwd_plain)


def check_password_hash(pwd_plain: str, pwd_hash: str) -> bool:
    """
    check password with hash value
    """
    global pwd_context
    return pwd_context.verify(pwd_plain, pwd_hash)
