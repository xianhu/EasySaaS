# _*_ coding: utf-8 _*_

"""
user api
"""

from fastapi import APIRouter
from fastapi import Body, Depends, Path
from pydantic import Field
from sqlalchemy.orm import Session

from data import get_session
from data.models import User
from data.schemas import Resp, UserSchema
from data.schemas import UserUpdate
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data: UserSchema = Field(None)


@router.get("/get", response_model=RespUser)
def _get(current_user: User = Depends(get_current_user)):
    """
    get schema of current_user
    - **status=0**: data=UserSchema
    """
    # get user_model
    user_model = current_user

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))


@router.post("/update", response_model=RespUser)
def _update(current_user: User = Depends(get_current_user),
            user_schema: UserUpdate = Body(...),
            session: Session = Depends(get_session)):
    """
    update schema of current_user
    - **status=0**: data=UserSchema
    """
    # get user_model
    user_id = current_user.id
    user_model = session.query(User).get(user_id)

    # update user based on UserUpdatePri
    # user_schema = UserUpdatePri(**user_schema.dict(exclude_unset=True))
    # user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))


@router.get("/get/{user_id}", response_model=RespUser)
def _get(current_user: User = Depends(get_current_user),
         user_id: int = Path(..., description="user_id"),
         session: Session = Depends(get_session)):
    """
    get schema of user by user_id
    - **status=0**: data=UserSchema
    """
    # check current_user
    if not current_user.is_admin:
        return RespUser(status=-1, msg="permission denied")

    # get user_model
    user_model = session.query(User).get(user_id)

    # return UserSchema
    return RespUser(data=UserSchema(**user_model.to_dict()))
