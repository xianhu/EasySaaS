# _*_ coding: utf-8 _*_

"""
admin api (user)
"""

from ..base import *
from ..utils import get_current_user_admin

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data_user: Optional[UserSchema] = Field(None)


# response model
class RespUserList(Resp):
    data_user_list: List[UserSchema] = Field([])


@router.get("/", response_model=RespUserList)
def _get_user_schema(skip: int = Query(0, description="skip count"),
                     limit: int = Query(100, description="limit count"),
                     current_user: User = Depends(get_current_user_admin),
                     session: Session = Depends(get_session)):
    """
    get user schema list
    """
    # get user model list and schema list
    user_model_list = session.query(User).offset(skip).limit(limit).all()
    user_schema_list = [UserSchema(**um.dict()) for um in user_model_list]

    # return user schema list
    return RespUserList(data_user_list=user_schema_list)


@router.patch("/{user_id}", response_model=RespUser)
def _update_user_model(user_id: int = Path(..., description="user id"),
                       user_schema: UserUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user_admin),
                       session: Session = Depends(get_session)):
    """
    update user model based on update schema, return user schema
    - **status=-1**: user not exist
    """
    # get user model based on user_id
    user_model = session.query(User).get(user_id)
    if not user_model:
        return RespUser(status=-1, msg="user not exist")

    # update user model based on update schema
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(user_model, field, getattr(user_schema, field))
    session.merge(user_model)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**user_model.dict()))


@router.delete("/{user_id}", response_model=Resp)
def _delete_user_model(user_id: int = Path(..., description="user id"),
                       current_user: User = Depends(get_current_user_admin),
                       session: Session = Depends(get_session)):
    """
    delete user model, return user schema
    """
    session.query(User).filter(User.id == user_id).delete()
    session.commit()
    return Resp(msg="delete success")
