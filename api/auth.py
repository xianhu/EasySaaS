# _*_ coding: utf-8 _*_

"""
auth api
"""

import logging
import random
from enum import Enum

from fastapi import APIRouter, HTTPException, status
from fastapi import BackgroundTasks, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from redis import Redis
from sqlalchemy.orm import Session

from core.security import check_password_hash, get_password_hash
from core.security import create_jwt_token, get_jwt_payload
from core.settings import settings
from core.utemail import send_email_of_code
from data import get_redis, get_session
from data.models import User
from data.schemas import AccessToken, Resp, UserCreate
from data.utils import init_user_object
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespSend(Resp):
    token: str = Field(None)


# define enum of client_id
class ClientID(str, Enum):
    web = "web"
    ios = "ios"
    android = "android"


# define enum of ttype
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


@router.post("/access-token", response_model=AccessToken)
def _get_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                      session: Session = Depends(get_session),
                      rd_conn: Redis = Depends(get_redis)):
    """
    get access_token based on OAuth2PasswordRequestForm, return access_token
    - **username**: value of email, or phone number, etc.
    - **password**: value of password, plain text
    - **client_id**: value of client_id, default "web"
    - **status_code=401**: user not found, password incorrect, client_id invalid
    """
    # get username、password from form_data
    email, pwd_plain = form_data.username, form_data.password
    user_model = session.query(User).filter(User.email == email).first()

    # check if user existed or raise exception
    if (not user_model) or (user_model.status != 1):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found",
        )
    pwd_hash = user_model.password

    # check if password correct or raise exception
    if not check_password_hash(pwd_plain, pwd_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password incorrect"
        )
    user_id = user_model.id

    # get client_id from form_data
    client_id = form_data.client_id or "web"
    if client_id not in ClientID.__members__:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="client_id invalid"
        )

    # create access_token and save to redis
    access_token = create_jwt_token(user_id, client_id=client_id)
    rd_conn.set(f"{settings.APP_NAME}-token-{client_id}-{user_id}", access_token)

    # return access_token
    return AccessToken(access_token=access_token)


@router.post("/access-token-logout", response_model=Resp)
def _logout_access_token(client_id: ClientID = Body(..., embed=True, description="client id"),
                         current_user: User = Depends(get_current_user),
                         rd_conn: Redis = Depends(get_redis)):
    """
    logout access_token based on client_id
    """
    user_id = current_user.id

    # delete access_token from redis
    rd_conn.delete(f"{settings.APP_NAME}-token-{client_id}-{user_id}")

    # return result
    return Resp(msg="logout success")


@router.post("/send-code", response_model=RespSend)
def _send_code_to_email(background_tasks: BackgroundTasks,
                        email: EmailStr = Body(..., description="email"),
                        ttype: TypeName = Body(..., description="type of send"),
                        session: Session = Depends(get_session),
                        rd_conn: Redis = Depends(get_redis)):
    """
    send a code to email for signup or reset, return token with code
    - **status=-1**: send email too frequently
    - **status=-2**: email existed or not existed
    """
    # check if send email too frequently
    if rd_conn.get(f"{settings.APP_NAME}-send-{email}"):
        return RespSend(status=-1, msg="send email too frequently")
    user_model = session.query(User).filter(User.email == email).first()

    # check if user existed or not by ttype
    if ttype == TypeName.signup and user_model:
        return RespSend(status=-2, msg="user existed")
    if ttype == TypeName.reset and (not user_model):
        return RespSend(status=-2, msg="user not existed")
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
    verify code & token from send-code, and create user or update password
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
        # create user based on email and password
        user_schema = UserCreate(email=email, password=pwd_hash)
        user_model = init_user_object(user_schema, session)

        # logging user and return result
        logging.warning(f"create user: %s", user_model.dict())
        return Resp(msg=f"{ttype} success")

    # check token ttype: reset
    if ttype == TypeName.reset and user_model:
        # update user based on password
        user_model.password = pwd_hash
        session.merge(user_model)
        session.commit()

        # logging user and return result
        logging.warning(f"update user: %s", user_model.dict())
        return Resp(msg=f"{ttype} success")

    # return -1 (token invalid)
    return Resp(status=-1, msg="token invalid or expired")
