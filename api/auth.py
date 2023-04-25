# _*_ coding: utf-8 _*_

"""
auth api
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import create_access_token
from models import get_db
from models.crud import crud_user
from models.schemas import Token

router = APIRouter()


@router.post("/access-token", response_model=Token)
def auth_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    login to get access token
    """
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return Token(access_token=create_access_token(user.id), token_type="bearer")
