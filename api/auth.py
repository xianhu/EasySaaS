# _*_ coding: utf-8 _*_

"""
auth api
"""

import json
import logging
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import check_pwd_hash, get_pwd_hash
from core.utils.security import create_sub_token, get_token_sub
from core.utils.utemail import send_email_verify
from data import get_session
from data.crud import crud_user
from data.schemas import AccessToken, Result, Token
from data.schemas import UserCreate, UserUpdatePri
from .utils import user_existed, user_not_existed

# define router
router = APIRouter()


# define name of type
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    get access token by email and password
    """
    email, pwd_plain = form_data.username, form_data.password

    # user existed, or raise exception
    user_model = user_existed(email=email, session=session)
    logging.warning("get user: %s", user_model.to_dict())

    # check password
    if not check_pwd_hash(pwd_plain, user_model.pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.PWD_INCORRECT,
        )

    # create access_token with user_id
    access_token = create_sub_token(user_model.id)
    logging.warning("create access_token: %s", access_token)

    # return access_token
    return AccessToken(access_token=access_token)


@router.post("/send-code", response_model=Token)
def _send_code(email: str, _type: TypeName, session: Session = Depends(get_session)):
    """
    send a code to email, and return token
    """
    if _type == TypeName.signup:
        # user not existed, or raise exception
        user_not_existed(email=email, session=session)
    elif _type == TypeName.reset:
        # user existed, or raise exception
        user_existed(email=email, session=session)

    # create token with code and type(!!!)
    token = send_email_verify(email, is_code=True, _type=_type)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_SEND_FAILED,
        )
    logging.warning("send code: %s - %s - %s", email, _type, token)

    # return token with code or link
    return Token(token=token, token_type="code")


@router.post("/verify-code-xxx", response_model=Result)
def _verify_code_xxx(
        form_data: OAuth2PasswordRequestForm = Depends(),
        code: int = Query(..., ge=100000, le=999999),
        token: str = Query(..., min_length=10),
        session: Session = Depends(get_session),
):
    """
    verify code and token, then create user or update password
    """
    email, pwd_plain = form_data.username, form_data.password

    # get sub_dict from token
    sub_dict = json.loads(get_token_sub(token) or "{}")
    logging.warning("get sub_dict: %s - %s", sub_dict, code)

    # check token: type
    if not sub_dict.get("type"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.TOKEN_INVALID,
        )
    _type = sub_dict["type"]

    # check token: email
    if (not sub_dict.get("email")) or (sub_dict["email"] != email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.TOKEN_INVALID,
        )

    # check token: code
    if (not sub_dict.get("code")) or (sub_dict["code"] != code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.CODE_INVALID,
        )
    pwd_hash = get_pwd_hash(pwd_plain)

    # check token type: signup
    if _type == TypeName.signup:
        # user not existed, or raise exception
        user_not_existed(email=email, session=session)

        # create user with email (verified)
        user_schema = UserCreate(pwd=pwd_hash, email=email, email_verified=True)
        user_model = crud_user.create(session, obj_schema=user_schema)
        logging.warning("create user: %s", user_model.to_dict())

        # return result
        return Result(msg="Sign up successfully")

    # check token type: reset
    if _type == TypeName.reset:
        # user existed, or raise exception
        user_model = user_existed(email=email, session=session)

        # update user's pwd with UserUpdatePri
        user_schema = UserUpdatePri(pwd=get_pwd_hash(pwd_plain))
        user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)
        logging.warning("reset password: %s", user_model.to_dict())

        # return result
        return Result(msg="Reset password successfully")

    # raise exception
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=error_tips.TOKEN_INVALID,
    )
