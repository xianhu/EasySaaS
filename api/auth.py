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
from core.security import create_token_data, get_token_payload
from core.settings import settings
from core.utemail import send_email
from data import get_session
from data.models import User
from data.schemas import AccessToken, Resp

# define router
router = APIRouter()


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                  session: Session = Depends(get_session)):
    """
    get access_token by OAuth2PasswordRequestForm, return access_token or raise exception(401)
    - **username**: value of email, or phone number, etc.
    - **password**: value of password
    """
    # get username、password from form_data
    email, pwd_plain = form_data.username, form_data.password
    logging.warning("access_token_0: %s - %s", email, pwd_plain)

    # check if user existed or raise exception
    user_model = session.query(User).filter(User.email == email).first()
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

    # create access_token with user_id
    access_token = create_token_data({"sub": str(user_id)})
    logging.warning("access_token_1: %s - %s", email, access_token)

    # return access_token
    return AccessToken(access_token=access_token)


# define enum of type
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# response model
class RespSend(Resp):
    token: str = Field(None)


@router.post("/send-code", response_model=RespSend)
def _send_code(background_tasks: BackgroundTasks,
               email: EmailStr = Body(..., description="email address"),
               _type: TypeName = Body(..., description="type of send"),
               session: Session = Depends(get_session)):
    """
    send a code to email, and return token with code
    - **status=0**: send email success, data=token
    - **status=-1**: email existed or not existed
    """
    # check if user existed or not by _type
    user_model = session.query(User).filter(User.email == email).first()
    if _type == TypeName.signup and user_model:
        return RespSend(status=-1, msg="email existed")
    if _type == TypeName.reset and (not user_model):
        return RespSend(status=-1, msg="email not existed")

    # define code, data and token
    code = random.randint(100000, 999999)
    data = dict(sub=email, code=code, type=_type)
    token = create_token_data(data, expires_duration=settings.NORMAL_TOKEN_EXPIRE_DURATION)

    # define email content and render
    mail_subject = "Verify of {{ app_name }}"
    mail_html = "Verify code: <b>{{ code }}</b>"
    render = dict(app_name=settings.APP_NAME, code=code)

    # define _from and kwargs
    _from = (settings.APP_NAME, settings.MAIL_USERNAME)
    kwargs = dict(subject=mail_subject, html_raw=mail_html, render=render)

    # send email in background (check status_code == 250)
    background_tasks.add_task(send_email, _from, email, **kwargs)
    logging.warning("send code: %s - %s - %s - %s", email, code, _type, token)

    # return token with code
    return RespSend(token=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code(code: int = Body(..., ge=100000, le=999999),
                 token: str = Body(..., min_length=10, max_length=500),
                 password: str = Body(..., min_length=6, max_length=20),
                 session: Session = Depends(get_session)):
    """
    verify code and token, then create user or update password
    - **status=0**: verify success, create or update success
    - **status=-1**: token invalid
    - **status=-2**: code invalid
    """
    # get payload from token
    payload = get_token_payload(token)
    logging.warning("get payload: %s - %s", code, payload)

    # check token: type(!!!)
    if (not payload.get("type")) or (payload["type"] not in TypeName.__members__):
        return Resp(status=-1, msg="token invalid")
    _type = payload["type"]

    # check token: email(sub)
    if not payload.get("sub"):
        return Resp(status=-1, msg="token invalid")
    email = payload["sub"]

    # check token: code(int)
    if (not payload.get("code")) or (payload["code"] != code):
        return Resp(status=-2, msg="code invalid")
    pwd_hash = get_password_hash(password)

    # get user_model from db
    user_model = session.query(User).filter(User.email == email).first()

    # check token type: signup
    if _type == TypeName.signup and (not user_model):
        # create user based on email and password
        user_model = User(name=email, email=email, password=pwd_hash, email_verified=True)
        session.add(user_model)
        session.commit()

        # logging and return result
        logging.warning("create user: %s", user_model.to_dict())
        return Resp(msg=f"{_type} successfully")

    # check token type: reset
    if _type == TypeName.reset and user_model:
        # update password based on password
        user_model.password = pwd_hash
        session.merge(user_model)
        session.commit()

        # logging and return result
        logging.warning("reset password: %s", user_model.to_dict())
        return Resp(msg=f"{_type} successfully")

    # return result
    return Resp(status=-1, msg="token invalid")
