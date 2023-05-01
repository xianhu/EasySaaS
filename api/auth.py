# _*_ coding: utf-8 _*_

"""
auth api
"""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils.security import check_pwd_hash, get_pwd_hash
from core.utils.security import create_token, get_token_sub
from core.utils.utemail import send_email_verify
from models import get_db
from models.crud import crud_user
from models.schemas import AccessToken, Result, Token
from models.schemas import UserCreate, UserUpdate
from .utils import user_existed, user_not_existed

router = APIRouter()


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    log in to get access token
    """
    email, pwd_plain = form_data.username, form_data.password

    # get user_db, or raise exception
    user_db = user_existed(email=email, db=db)

    # check password
    if not check_pwd_hash(pwd_plain, user_db.pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.PWD_INCORRECT,
        )

    # return AccessToken
    access_token = create_token(user_db.id)
    return AccessToken(access_token=access_token, token_type="bearer")


@router.post("/signup", response_model=Result)
def _signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    sign up to create a new user: email_verified = False
    """
    email, pwd_plain = form_data.username, form_data.password

    # user not existed, or raise exception
    user_db = user_not_existed(email=email, db=db)

    # create user with email (unverified)
    pwd_hash = get_pwd_hash(pwd_plain)
    user_schema = UserCreate(pwd=pwd_hash, email=email, email_verified=False)
    user_db = crud_user.create(db, obj_schema=user_schema)

    # return result
    return Result(msg="Sign up successfully")


@router.post("/send-code", response_model=Token)
def _send_code(email: str, db: Session = Depends(get_db)):
    """
    send a code to email, and return token
    """
    # get user_db, or raise exception
    user_db = user_existed(email=email, db=db)

    # create token with code, and return it
    token = send_email_verify(email, is_code=True, _type="verify")
    return Token(token=token, token_type="verify")


@router.post("/reset", response_model=Result)
def _reset(code: str, pwd: str, token: str, db: Session = Depends(get_db)):
    """
    reset password based on code and token
    """
    # parse token to get sub_dict
    sub_dict = json.loads(get_token_sub(token) or "{}")

    # check token: code and email
    if (not sub_dict.get("code")) or (not sub_dict.get("email")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.TOKEN_INVALID,
        )
    code_token = str(sub_dict["code"])

    # check code
    code = (code or "").strip()
    if (not code) or (code != code_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.CODE_INVALID,
        )
    email = sub_dict["email"]

    # get user_db, or raise exception
    user_db = user_existed(email=email, db=db)

    # update user's password
    user_schema = UserUpdate(pwd=get_pwd_hash(pwd))
    user_db = crud_user.update(db, obj_db=user_db, obj_schema=user_schema)

    # return result
    return Result(msg="Reset password successfully")
