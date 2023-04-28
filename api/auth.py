# _*_ coding: utf-8 _*_

"""
auth api
"""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils import security, utemail
from models import get_db
from models.crud import crud_user
from models.schemas import AccessToken, Result, Token
from models.schemas import UserCreate, UserUpdate

router = APIRouter()


@router.post("/signup", response_model=Result)
def _signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    sign up to create a new user
    """
    email, pwd_plain = form_data.username, form_data.password

    # check user
    user_db = crud_user.get_by_email(db, email=email)
    if user_db and user_db.status is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_EXISTED,
        )
    pwd_hash = security.get_pwd_hash(pwd_plain)

    # create user with email (unverified)
    user_schema = UserCreate(pwd=pwd_hash, email=email)
    crud_user.create(db, obj_schema=user_schema)

    # return result
    return Result(msg="Sign up successfully")


@router.post("/access-token", response_model=AccessToken)
def _access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    log in to get access token
    """
    email, pwd_plain = form_data.username, form_data.password

    # check user
    user_db = crud_user.get_by_email(db, email=email)
    if not (user_db and user_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )

    # check password
    if not security.check_pwd_hash(pwd_plain, user_db.pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.PWD_INCORRECT,
        )

    # return access_token
    access_token = security.create_token(user_db.id)
    return AccessToken(access_token=access_token, token_type="bearer")


@router.post("/email-send", response_model=Token)
def _email_send(email: str, db: Session = Depends(get_db)):
    """
    send a code to email
    """
    # check user
    user_db = crud_user.get_by_email(db, email=email)
    if not (user_db and user_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )

    # create token_verify with code, and send email
    token_verify = utemail.send_email_code(email, _type="verify")

    # return token_verify
    return Token(token=token_verify, token_type="verify")


@router.get("/reset", response_model=Result)
def _reset(code: str, pwd: str, token_verify: str, db: Session = Depends(get_db)):
    """
    reset password based on code and token_verify
    """
    # parse token_verify to get sub_dict
    sub_dict = json.loads(security.get_token_sub(token_verify) or "{}")

    # check token_verify
    if (not sub_dict.get("code")) or (not sub_dict.get("email")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.CODE_INVALID,
        )
    code_token = str(sub_dict["code"])
    email = sub_dict["email"]

    # check code
    code = (code or "").strip()
    if (not code) or (code_token != code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.CODE_INVALID,
        )

    # get user from db
    user_db = crud_user.get_by_email(db, email=email)

    # update user's password
    user_schema = UserUpdate(pwd=security.get_pwd_hash(pwd))
    crud_user.update(db, obj_db=user_db, obj_schema=user_schema)

    # return result
    return Result(msg="Reset password successfully")
