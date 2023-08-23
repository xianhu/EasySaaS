# _*_ coding: utf-8 _*_

"""
admin api of user
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
    # get user schema list
    user_schema_list = []
    for user_schema in (session.query(User)
            .order_by(User.created_at.desc())
            .offset(skip).limit(limit).all()):
        user_schema = UserSchema(**user_schema.dict())
        user_schema_list.append(user_schema)

    # return total count and user schema list
    user_total = session.query(User).count()
    return RespUserList(data_user_total=user_total, data_user_list=user_schema_list)
