# _*_ coding: utf-8 _*_

"""
user api
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from data import get_session
from data.crud import crud_user
from data.models import User
from data.schemas import Resp, UserSchema
from data.schemas import UserUpdate, UserUpdatePri
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data: UserSchema = None


@router.get("/get", response_model=RespUser)
def _get(current_user: Annotated[User, Security(get_current_user, scopes=["user:read"])]):
    """
    get schema of current_user
    - **status=0**: data=UserSchema
    """
    user_model = current_user

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))


@router.post("/update", response_model=RespUser)
def _update(user_schema: UserUpdate,
            current_user: Annotated[User, Security(get_current_user, scopes=["user:write"])],
            session: Session = Depends(get_session)):
    """
    update schema of current_user
    - **status=0**: data=UserSchema
    """
    user_model = current_user

    # update user based on UserUpdatePri
    user_schema = UserUpdatePri(**user_schema.dict(exclude_unset=True))
    user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))
