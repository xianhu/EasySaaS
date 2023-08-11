# _*_ coding: utf-8 _*_

"""
user schema
"""

from .base import *


# used for response_model
class UserSchema(BaseModel):
    id: Optional[str] = None

    avatar: Optional[HttpUrl] = None
    nickname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None

    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None
    phone: Optional[PhoneStr] = None
    phone_verified: Optional[bool] = None
    # password: Optional[str] = None

    expire_time: Optional[datetime] = None
    reset_time: Optional[datetime] = None

    points_left: Optional[int] = None
    points_total: Optional[int] = None
    points_history: Optional[list] = None

    minutes_left: Optional[int] = None
    minutes_total: Optional[int] = None
    minutes_history: Optional[list] = None

    space_used: Optional[int] = None
    space_total: Optional[int] = None
    space_history: Optional[list] = None


# used for request body
class UserCreate(BaseModel):
    __abstract__ = True
    password: str = Field(..., description="Password")
    is_admin: bool = Field(False, description="Is Admin")
    role_json: dict = Field({}, description="Role Json")


class UserCreateEmail(UserCreate):
    email: EmailStr = Field(..., description="Email")
    email_verified: bool = Field(False, description="Verified?")


class UserCreatePhone(UserCreate):
    phone: PhoneStr = Field(..., description="Phone")
    phone_verified: bool = Field(False, description="Verified?")


# used for request body
class UserUpdate(BaseModel):
    # avatar: Optional[HttpUrl] = Field(None, description="Avatar Url")
    nickname: Optional[str] = Field(None, min_length=2, max_length=20)
    birthday: Optional[date] = Field(None, description="Date of Birthday")
    gender: Optional[int] = Field(None, description="1-Male, 2-Female")
    country: Optional[str] = Field(None, description="Country")
    address: Optional[str] = Field(None, description="Address")
