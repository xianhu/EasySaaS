# _*_ coding: utf-8 _*_

"""
user schema
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


# used for response_model
class UserSchema(BaseModel):
    id: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    nickname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[int] = None
    email: Optional[EmailStr] = None
    # password: Optional[str] = None
    email_verified: Optional[bool] = None
    # system_admin: Optional[bool] = None
    # system_role: Optional[dict] = None


# used for request body
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=6, max_length=20)


# used for request body
class UserUpdate(BaseModel):
    avatar: Optional[HttpUrl] = Field(None, description="Avatar Url")
    nickname: Optional[str] = Field(None, min_length=2, max_length=20)
    birthday: Optional[date] = Field(None, description="Date of Birthday")
    gender: Optional[int] = Field(None, description="1-Male, 2-Female")
