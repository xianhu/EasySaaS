# _*_ coding: utf-8 _*_

"""
auth api
"""

from enum import Enum

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis
from sqlalchemy.orm import Session

from core.security import check_password_hash
from core.security import create_jwt_token
from core.settings import settings
from data import get_redis, get_session
from data.models import User
from data.schemas import AccessToken, Resp
from ..utils import get_current_user

# define router
router = APIRouter()


# define enum of client_id
class ClientID(str, Enum):
    web = "web"
    ios = "ios"
    android = "android"


@router.post("/access-token", response_model=AccessToken)
def _get_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                      session: Session = Depends(get_session),
                      rd_conn: Redis = Depends(get_redis)):
    """
    get access_token based on OAuth2PasswordRequestForm, return access_token
    - **username**: value of email or phone, etc.
    - **password**: value of password, plain text
    - **client_id**: value of client_id, default "web"
    - **status_code=401**: user not found, password incorrect, client_id invalid
    """
    # get username、password from form_data, and get user_model
    username, pwd_plain = form_data.username, form_data.password
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()

    # check if user exist or raise exception
    if (not user_model) or (user_model.status != 1):
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

    # get client_id from form_data
    client_id = form_data.client_id or "web"
    if client_id not in ClientID.__members__:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="client_id invalid"
        )

    # create access_token and save to redis
    access_token = create_jwt_token(user_id, client_id=client_id)
    rd_conn.set(f"{settings.APP_NAME}-access-{client_id}-{user_id}", access_token)

    # return access_token
    return AccessToken(access_token=access_token)


@router.post("/access-token-logout", response_model=Resp)
def _logout_access_token(client_id: ClientID = Body(..., embed=True, description="client id"),
                         current_user: User = Depends(get_current_user),
                         rd_conn: Redis = Depends(get_redis)):
    """
    logout access_token based on client_id
    """
    user_id = current_user.id

    # delete access_token from redis
    rd_conn.delete(f"{settings.APP_NAME}-access-{client_id}-{user_id}")

    # return result
    return Resp(msg="logout success")
