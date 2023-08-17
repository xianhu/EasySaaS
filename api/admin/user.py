# _*_ coding: utf-8 _*_

"""
user api of admin
"""

from ..base import *
from ..user.utils import RespUserList

# define router
router = APIRouter()


@router.get("/", response_model=RespUserList)
def _get_user_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          session: Session = Depends(get_session)):
    """
    get user schema list, support pagination
    """
    # get user model list and schema list
    user_model_list = (session.query(User)
                       .order_by(User.created_at.desc())
                       .offset(skip).limit(limit).all())
    user_schema_list = [UserSchema(**um.dict()) for um in user_model_list]

    # return total count and user schema list
    user_total = session.query(User).count()
    return RespUserList(data_user_total=user_total, data_user_list=user_schema_list)
