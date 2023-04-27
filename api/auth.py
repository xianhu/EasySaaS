# _*_ coding: utf-8 _*_

"""
auth api
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import check_password_hash, create_token
from models import get_db
from models.crud import crud_user
from models.schemas import Token

router = APIRouter()


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
