# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *


# response model
class RespUser(Resp):
    data_user: Optional[UserSchema] = Field(None)


# response model
class RespSend(Resp):
    token: Optional[str] = Field(None)
