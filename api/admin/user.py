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
def _get_user_schema_list(skip: int = Query(0, description="skip count"),
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


@router.delete("/{user_id}", response_model=Resp)
def _delete_user_model(user_id: int = Path(..., description="user id"),
                       current_user: User = Depends(get_current_user_admin),
                       session: Session = Depends(get_session)):
    """
    delete user model by id, return user schema
    """
    session.query(User).get(user_id).delete()
    session.commit()
    return Resp(msg="delete success")
