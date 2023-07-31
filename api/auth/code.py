# _*_ coding: utf-8 _*_

"""
code of auth api
"""

import logging
import random
from enum import Enum

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from pydantic import EmailStr, Field
from redis import Redis
from sqlalchemy.orm import Session

from core.security import create_jwt_token, get_jwt_payload
from core.security import get_password_hash
from core.settings import settings
from core.utemail import send_email_of_code
from data import get_redis, get_session
from data.models import User
from data.schemas import Resp, UserCreate
from data.utils import init_user_object

# define router
router = APIRouter()


# response model
class RespSend(Resp):
    token: str = Field(None)


# define enum of ttype
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


@router.post("/send-code", response_model=RespSend)
def _send_code_to_email(background_tasks: BackgroundTasks,
                        email: EmailStr = Body(..., description="email"),
                        ttype: TypeName = Body(..., description="type of send"),
                        session: Session = Depends(get_session),
                        rd_conn: Redis = Depends(get_redis)):
    """
    send a code to email for signup or reset, return token with code
    - **status=-1**: send email too frequently
    - **status=-2**: email existed or not exist
    """
    # check if send email too frequently
    if rd_conn.get(f"{settings.APP_NAME}-send-{email}"):
        return RespSend(status=-1, msg="send email too frequently")
    user_model = session.query(User).filter(User.email == email).first()

    # check if user exist or not by ttype
    if ttype == TypeName.signup and user_model:
        return RespSend(status=-2, msg="email existed")
    if ttype == TypeName.reset and (not user_model):
        return RespSend(status=-2, msg="email not exist")
    code = random.randint(100000, 999999)

    # define token based on email
    data = dict(code=code, ttype=ttype)
    duration = settings.NORMAL_TOKEN_EXPIRE_DURATION
    token = create_jwt_token(email, audience="send", expire_duration=duration, **data)

    # send email in background (status_code == 250)
    background_tasks.add_task(send_email_of_code, code, email)
    rd_conn.set(f"{settings.APP_NAME}-send-{email}", token, ex=60)

    # return token with code
    return RespSend(token=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code_token(code: int = Body(..., ge=100000, le=999999),
                       token: str = Body(..., description="token value"),
                       password: str = Body(..., min_length=6, max_length=20),
                       session: Session = Depends(get_session)):
    """
    verify code & token from send-code, and create user or reset password
    - **status=-1**: token invalid or expired
    - **status=-2**: code invalid or not match
    """
    # get payload from token, audience="send"
    payload = get_jwt_payload(token, audience="send")

    # check token: ttype
    if not payload.get("ttype"):
        return Resp(status=-1, msg="token invalid or expired")
    if payload["ttype"] not in TypeName.__members__:
        return Resp(status=-1, msg="token invalid or expired")
    ttype = payload["ttype"]

    # check token: sub(email) and code(int)
    if (not payload.get("sub")) or (not payload.get("code")):
        return Resp(status=-1, msg="token invalid or expired")
    email, code_in_token = payload["sub"], payload["code"]

    # check token: code
    if code != code_in_token:
        return Resp(status=-2, msg="code invalid or not match")
    user_model = session.query(User).filter(User.email == email).first()
    pwd_hash = get_password_hash(password)

    # check token ttype: signup
    if ttype == TypeName.signup and (not user_model):
        # create user based on email and pwd_hash
        user_schema = UserCreate(email=email, password=pwd_hash)
        user_model = init_user_object(user_schema, session)

        # logging user and return result
        logging.warning(f"signup: %s", user_model.dict())
        return Resp(msg=f"{ttype} success")

    # check token ttype: reset
    if ttype == TypeName.reset and user_model:
        # reset user password based on pwd_hash
        user_model.password = pwd_hash
        session.merge(user_model)
        session.commit()

        # logging user and return result
        logging.warning(f"reset: %s", user_model.dict())
        return Resp(msg=f"{ttype} success")

    # return -1 (token invalid or expired)
    return Resp(status=-1, msg="token invalid or expired")
