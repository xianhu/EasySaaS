# _*_ coding: utf-8 _*_

"""
user api
"""

from pydantic import Field

from data.schemas import Resp
from data.schemas import UserSchema


# response model
class RespUser(Resp):
    data_user: UserSchema = Field(None)


# response model
class RespSend(Resp):
    token: str = Field(None)
