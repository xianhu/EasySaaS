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
from models import get_db
from models.crud import crud_user
from models.schemas import AccessToken, Result, Token
from models.schemas import UserCreate, UserUpdatePri
from .utils import user_existed, user_not_existed

# define router
router = APIRouter()


# define name of type
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    get access token by email and password
    """
    email, pwd_plain = form_data.username, form_data.password

    # get user, or raise exception
    user_db = user_existed(email=email, db=db)
    logging.warning("get user: %s", user_db.to_dict())

    # check password
    if not check_pwd_hash(pwd_plain, user_db.pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.PWD_INCORRECT,
        )

    # create access_token
    access_token = create_sub_token(user_db.id)
    logging.warning("create access_token: %s", access_token)

    # return access_token
    return AccessToken(access_token=access_token)


@router.post("/send-code", response_model=Token)
def _send_code(email: str, _type: TypeName, db: Session = Depends(get_db)):
    """
    send a code to email, and return token
    """
    if _type == TypeName.signup:
        # user not existed, or raise exception
        user_not_existed(email=email, db=db)
    elif _type == TypeName.reset:
        # user existed, or raise exception
        user_existed(email=email, db=db)

    # create token with code and _type
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
        db: Session = Depends(get_db),
):
    """
    verify code and token, then create user or update password
    """
    email, pwd_plain = form_data.username, form_data.password
    sub_dict = json.loads(get_token_sub(token) or "{}")

    # check token: _type
    if not sub_dict.get("_type"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.TOKEN_INVALID,
        )

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
            detail=error_tips.TOKEN_INVALID,
        )
    pwd_hash = get_pwd_hash(pwd_plain)

    # check token: _type == signup
    if sub_dict["_type"] == TypeName.signup:
        # user not existed, or raise exception
        user_not_existed(email=email, db=db)

        # create user with email (verified)
        user_schema = UserCreate(pwd=pwd_hash, email=email, email_verified=True)
        user_db = crud_user.create(db, obj_schema=user_schema)
        logging.warning("create user: %s", user_db.to_dict())

        # return result
        return Result(msg="Sign up successfully")

    # check token: _type == reset
    if sub_dict["_type"] == TypeName.reset:
        # user existed, or raise exception
        user_db = user_existed(email=email, db=db)

        # update user's pwd with UserUpdatePri
        user_schema = UserUpdatePri(pwd=get_pwd_hash(pwd_plain))
        user_db = crud_user.update(db, obj_db=user_db, obj_schema=user_schema)
        logging.warning("reset password: %s", user_db.to_dict())

        # return result
        return Result(msg="Reset password successfully")

    # raise exception
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=error_tips.TOKEN_INVALID,
    )
