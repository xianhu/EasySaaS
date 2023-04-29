# _*_ coding: utf-8 _*_

"""
email api
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.settings import error_tips
from core.utils import utemail
from models import get_db
from models.crud import crud_user
from models.schemas import Token

router = APIRouter()


@router.post("/verify-send", response_model=Token)
def _verify_send(email: str, is_code: bool = True, db: Session = Depends(get_db)):
    """
    send verify email to user
    """


    # check user by email
    user_db = crud_user.get_by_email(db, email=email)
    if not (user_db and user_db.status == 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_tips.EMAIL_NOT_EXISTED,
        )

    # create token_verify with code, and return it
    token_verify = utemail.send_email_code(email, _type="verify")
    return Token(token=token_verify, token_type="verify")
