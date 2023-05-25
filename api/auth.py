# _*_ coding: utf-8 _*_

"""
auth api
"""

import json
import logging
from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import check_password_hash, get_password_hash
from core.utils.security import create_sub_token, get_token_sub
from core.utils.utemail import send_email_verify
from data import get_session
from data.crud import crud_user
from data.schemas import AccessToken, Resp
from data.schemas import UserCreatePri, UserUpdatePri

# define router
router = APIRouter()


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    get access_token by username and password, return access_token or raise exception(401)
    - **username**: value of email
    - **password**: value of password
    """
    # get username and password from form_data
    email, pwd_plain = form_data.username, form_data.password

    # check user existed (must raise exception)
    user_model = crud_user.get_by_email(session, email=email)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )
    logging.warning("get user: %s", user_model.to_dict())

    # check user password
    if not check_password_hash(pwd_plain, user_model.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_tips.PWD_INCORRECT,
        )

    # create access_token with user_id
    access_token = create_sub_token(user_model.id)
    logging.warning("create access_token: %s", access_token)

    # return access_token
    return AccessToken(access_token=access_token)


# name of verify type
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# response model
class RespSend(Resp):
    data: str = Field(None, description="token")


@router.post("/send-code", response_model=RespSend)
def _send_code(email: EmailStr = Body(...),
               _type: TypeName = Body(...),
               session: Session = Depends(get_session)):
    """
    send a code to email, and return token with code
    - **status=0**: send email success, data=token
    - **status=-1**: email existed or not existed
    - **status=-2**: send email failed
    """
    # check user existed or not
    user_model = crud_user.get_by_email(session, email=email)
    if _type == TypeName.signup and user_model:
        return RespSend(status=-1, msg=error_tips.EMAIL_EXISTED)
    if _type == TypeName.reset and (not user_model):
        return RespSend(status=-1, msg=error_tips.EMAIL_NOT_EXISTED)

    # create token with code and type(!!!)
    token = send_email_verify(email, is_code=True, _type=_type)
    if not token:
        return RespSend(status=-2, msg=error_tips.EMAIL_SEND_FAILED)
    logging.warning("send code: %s - %s - %s", email, _type, token)

    # return token with code
    return RespSend(data=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code(token: str = Body(..., min_length=10),
                 code: int = Body(..., ge=100000, le=999999),
                 password: str = Body(..., min_length=6, max_length=20),
                 session: Session = Depends(get_session)):
    """
    verify code and token, then create user or update password
    - **status=0**: verify success
    - **status=-1**: token invalid
    - **status=-2**: code invalid
    """
    # get sub_dict from token
    sub_dict = json.loads(get_token_sub(token) or "{}")
    logging.warning("get sub_dict: %s - %s", sub_dict, code)

    # check token: type(!!!)
    if (not sub_dict.get("type")) or (sub_dict["type"] not in TypeName.__members__):
        return Resp(status=-1, msg=error_tips.TOKEN_INVALID)
    _type = sub_dict["type"]

    # check token: email
    if not sub_dict.get("email"):
        return Resp(status=-1, msg=error_tips.TOKEN_INVALID)
    email = sub_dict["email"]
    user_model = crud_user.get_by_email(session, email=email)

    # check token: code
    if (not sub_dict.get("code")) or (sub_dict["code"] != code):
        return Resp(status=-2, msg=error_tips.CODE_INVALID)
    pwd_hash = get_password_hash(password)

    # check token type: signup
    if _type == TypeName.signup and (not user_model):
        # create user based on UserCreatePri
        user_schema = UserCreatePri(email=email, password=pwd_hash, email_verified=True)
        user_model = crud_user.create(session, obj_schema=user_schema)

        # logging and return result
        logging.warning("create user: %s", user_model.to_dict())
        return Resp(msg=f"{_type} successfully")

    # check token type: reset
    if _type == TypeName.reset and user_model:
        # update password based on UserUpdatePri
        user_schema = UserUpdatePri(password=pwd_hash)
        user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)

        # logging and return result
        logging.warning("reset password: %s", user_model.to_dict())
        return Resp(msg=f"{_type} successfully")

    # return result
    return Resp(status=-1, msg=error_tips.TOKEN_INVALID)
