# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *


# response model
class RespUser(Resp):
    data_user: Optional[UserSchema] = Field(None)


# response model
class RespUserList(Resp):
    data_user_list: List[UserSchema] = Field([])
