# _*_ coding: utf-8 _*_

"""
code of user api
"""

import random

from fastapi import APIRouter, BackgroundTasks
from fastapi import Body, Depends
from pydantic import EmailStr, Field
from redis import Redis
from sqlalchemy.orm import Session

from core.security import create_jwt_token, get_jwt_payload
from core.settings import settings
from core.utemail import send_email_of_code
from data import get_redis, get_session
from data.models import User
from data.schemas import Resp
from data.vars import PhoneStr
from ..utils import get_current_user

# define router
router = APIRouter()


# response model
class RespSend(Resp):
    token: str = Field(None)


@router.post("/send-code", response_model=RespSend)
def _send_code_to_xxxx(background_tasks: BackgroundTasks,
                       username: EmailStr | PhoneStr = Body(..., description="email or phone"),
                       current_user: User = Depends(get_current_user),
                       rd_conn: Redis = Depends(get_redis)):
    """
    send a code to email or phone for bind, return token with code
    - **status=-1**: send code too frequently
    """
    # check if send code too frequently
    if rd_conn.get(f"{settings.APP_NAME}-send-{username}"):
        return RespSend(status=-1, msg="send code too frequently")
    code = random.randint(100000, 999999)

    # define token based on username
    data = dict(code=code, ttype="bind")
    duration = settings.NORMAL_TOKEN_EXPIRE_DURATION
    token = create_jwt_token(username, audience="send", expire_duration=duration, **data)

    # send code in background
    if username.find("@") > 0:
        background_tasks.add_task(send_email_of_code, code, username)
    else:
        raise NotImplemented
    rd_conn.set(f"{settings.APP_NAME}-send-{username}", token, ex=60)

    # return token with code
    return RespSend(token=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code_token(code: int = Body(..., ge=100000, le=999999),
                       token: str = Body(..., description="token value"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    verify code & token from send-code, and bind email or phone to user
    - **status=-1**: token invalid or expired
    - **status=-2**: code invalid or not match
    """
    # get payload from token, audience="send"
    payload = get_jwt_payload(token, audience="send")

    # check token: ttype
    if (not payload) or (not payload.get("ttype")):
        return Resp(status=-1, msg="token invalid or expired")
    assert payload["ttype"] == "bind", "token ttype must be bind"

    # check token: sub(email/phone) and code(int)
    if (not payload.get("sub")) or (not payload.get("code")):
        return Resp(status=-1, msg="token invalid or expired")
    username, code_in_token = payload["sub"], payload["code"]

    # check token: code
    if code != code_in_token:
        return Resp(status=-2, msg="code invalid or not match")

    # update user_model
    if username.find("@") > 0:
        current_user.email = username
        current_user.email_verified = True
    else:
        current_user.phone = username
        current_user.phone_verified = True
    session.merge(current_user)
    session.commit()

    # return
    return Resp(msg="bind success")
