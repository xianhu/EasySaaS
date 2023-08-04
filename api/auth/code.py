# _*_ coding: utf-8 _*_

"""
auth api
"""

import random

from fastapi import APIRouter, BackgroundTasks
from fastapi import Body, Depends
from pydantic import EmailStr
from redis import Redis
from sqlalchemy.orm import Session

from core.security import create_jwt_token, get_jwt_payload, get_password_hash
from core.sendx import send_email_of_code, send_phone_of_code
from core.settings import settings
from data import get_redis, get_session
from data.models import User
from data.schemas import Resp, UserCreateEmail, UserCreatePhone
from data.utils import PhoneStr
from .utils import RespSend, TypeName, init_user_object

# define router
router = APIRouter()


@router.post("/send-code", response_model=RespSend)
def _send_code_to_xxxx(background_tasks: BackgroundTasks,
                       username: EmailStr | PhoneStr = Body(..., description="email or phone"),
                       ttype: TypeName = Body(..., description="type of send"),
                       session: Session = Depends(get_session),
                       rd_conn: Redis = Depends(get_redis)):
    """
    send a code to email or phone for signup or reset, return token with code
    - **status=-1**: send code too frequently
    - **status=-2**: user existed or not exist
    """
    # check if send code too frequently
    if rd_conn.get(f"{settings.APP_NAME}-send-{username}"):
        return RespSend(status=-1, msg="send code too frequently")

    # get user_model
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()

    # check if user exist or not by ttype
    if ttype == TypeName.signup and user_model:
        return RespSend(status=-2, msg="user existed")
    if ttype == TypeName.reset and (not user_model):
        return RespSend(status=-2, msg="user not exist")
    code = random.randint(100000, 999999)

    # define token based on username
    data = dict(code=code, ttype=ttype)
    duration = settings.NORMAL_TOKEN_EXPIRE_DURATION
    token = create_jwt_token(username, audience="send", expire_duration=duration, **data)

    # send code in background
    if username.find("@") > 0:
        background_tasks.add_task(send_email_of_code, code, username)
    else:
        background_tasks.add_task(send_phone_of_code, code, username)
    rd_conn.set(f"{settings.APP_NAME}-send-{username}", token, ex=60)

    # return token with code
    return RespSend(token=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code_token(code: int = Body(..., ge=100000, le=999999),
                       token: str = Body(..., description="token from send"),
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
    if (not payload) or (not payload.get("ttype")):
        return Resp(status=-1, msg="token invalid or expired")
    if payload["ttype"] not in TypeName.__members__:
        return Resp(status=-1, msg="token invalid or expired")
    ttype = payload["ttype"]

    # check token: sub(email or phone) and code(int)
    if (not payload.get("sub")) or (not payload.get("code")):
        return Resp(status=-1, msg="token invalid or expired")
    username, code_in_token = payload["sub"], payload["code"]

    # check token: code
    if code != code_in_token:
        return Resp(status=-2, msg="code invalid or not match")
    pwd_hash = get_password_hash(password)

    # get user_model
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()

    # check token ttype: signup
    if ttype == TypeName.signup and (not user_model):
        # create user model based on username and pwd_hash
        if username.find("@") > 0:
            user_schema = UserCreateEmail(email=username, email_verified=True, password=pwd_hash)
        else:
            user_schema = UserCreatePhone(phone=username, phone_verified=True, password=pwd_hash)
        _user_model = init_user_object(user_schema, session)

        # return result
        return Resp(msg=f"{ttype} success")

    # check token ttype: reset
    if ttype == TypeName.reset and user_model:
        # reset password of user model based on pwd_hash
        user_model.password = pwd_hash
        session.merge(user_model)
        session.commit()

        # return result
        return Resp(msg=f"{ttype} success")

    # return -1 (token invalid or expired)
    return Resp(status=-1, msg="token invalid or expired")
