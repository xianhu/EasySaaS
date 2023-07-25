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
from sqlalchemy.orm import Session

from core.security import check_password_hash, get_password_hash
from core.security import create_jwt_token, get_jwt_payload
from core.settings import settings
from core.utemail import send_email_of_code
from data import get_redis, get_session
from data.models import User
from data.schemas import AccessToken, Resp, UserCreate
from data.utils import init_user_object

# define router
router = APIRouter()


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                  session: Session = Depends(get_session)):
    """
    get access_token by OAuth2PasswordRequestForm, return access_token
    - **username**: value of email, or phone number, etc.
    - **password**: value of password, plain text
    - **status_code=401**: user not found or password incorrect
    """
    # get username、password from form_data
    email, pwd_plain = form_data.username, form_data.password
    user_model = session.query(User).filter(User.email == email).first()

    # check if user existed or raise exception
    if not user_model:
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

    # create access_token and return
    access_token = create_jwt_token(user_id)
    return AccessToken(access_token=access_token)


# define enum of ttype
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# response model
class RespSend(Resp):
    token: str = Field(None)


@router.post("/send-code", response_model=RespSend)
def _send_code(background_tasks: BackgroundTasks,
               email: EmailStr = Body(..., description="email"),
               ttype: TypeName = Body(..., description="type of send"),
               session: Session = Depends(get_session)):
    """
    send a code to email, return token with code
    - **status=-1**: send email too frequently
    - **status=-2**: email existed or not existed
    """
    redis = get_redis()

    # check if send email too frequently
    if redis.get(f"{settings.APP_NAME}-send-{email}"):
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
    expire_duration = settings.NORMAL_TOKEN_EXPIRE_DURATION
    token = create_jwt_token(email, audience="send", expire_duration=expire_duration, **data)

    # send email in background (status_code == 250)
    background_tasks.add_task(send_email_of_code, code, email)
    redis.set(f"{settings.APP_NAME}-send-{email}", token, ex=60)

    # return token with code
    return RespSend(token=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code(code: int = Body(..., ge=100000, le=999999),
                 token: str = Body(..., description="token value"),
                 password: str = Body(..., min_length=6, max_length=20),
                 session: Session = Depends(get_session)):
    """
    verify code and token, and create user or update password
    - **status=-1**: token invalid
    - **status=-2**: code invalid
    """
    # get payload from token, audience="send"
    payload = get_jwt_payload(token, audience="send")

    # check token: ttype
    if not payload.get("ttype"):
        return Resp(status=-1, msg="token invalid")
    if payload["ttype"] not in TypeName.__members__:
        return Resp(status=-1, msg="token invalid")
    ttype = payload["ttype"]

    # check token: sub(email) and code(int)
    if (not payload.get("sub")) or (not payload.get("code")):
        return Resp(status=-1, msg="token invalid")
    email, code_in_token = payload["sub"], payload["code"]

    # check token: code
    if code != code_in_token:
        return Resp(status=-2, msg="code invalid")
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
    return Resp(status=-1, msg="token invalid")
