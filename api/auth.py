# _*_ coding: utf-8 _*_

"""
auth api
"""

import random

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.utils.security import check_password_hash, create_token, get_password_hash
from models import get_db
from models.crud import crud_user
from models.schemas import Msg, Token, UserCreate, UserSchema

router = APIRouter()


@router.post("/sign-up", response_model=Msg)
def sign_up(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    sign up to get access token
    """
    user = crud_user.get_by_email(db, email=form_data.username)
    if user and user.status is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # create user
    pwd_hash = get_password_hash(form_data.password)
    user_schema = UserCreate(pwd=pwd_hash, email=form_data.username)
    user = crud_user.create(db, obj_in=UserSchema(email=form_data.username, pwd=form_data.password))
    token = create_token(user.id)
    return Token(access_token=token, token_type="bearer")


@router.post("/access-token", response_model=Token)
def auth_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    login to get access token
    """
    user = crud_user.get_by_email(db, email=form_data.username)
    if not (user and user.status == 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not check_password_hash(form_data.password, user.pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    token = create_token(user.id)
    return Token(access_token=token, token_type="bearer")


@router.post("/pwd-recovery", response_model=UserSchema)
def auth_pwd_recovery(email: str, db: Session = Depends(get_db)):
    """
    send email to reset password
    """
    user = crud_user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    code = random.randint(100000, 999999)
    token = create_token(code)
    return Token(access_token=token, token_type="bearer")


@router.get("/pwd-reset", response_model=UserSchema)
def auth_pwd_reset(code: str, token: str, pwd: str, db: Session = Depends(get_db)):
    """
    reset password
    """
    user = crud_user.get_by_code(db, code=code)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not check_password_hash(pwd, user.pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    user.pwd = get_password_hash(pwd)
    db.commit()
    return user
