# _*_ coding: utf-8 _*_

"""
auth api
"""

from enum import Enum

from pydantic import Field

from data.schemas import Resp


# response model
class RespSend(Resp):
    token: str = Field(None)


# enum of ttype
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# enum of client_id
class ClientID(str, Enum):
    web = "web"
    ios = "ios"
    android = "android"
