# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


# used for response_model
class UserSchema(BaseModel):
    id: Optional[int] = None
    nickname: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = None
    # password: Optional[str] = None
    # system_admin: Optional[bool] = None
    # system_role: Optional[dict] = None


# used for request body
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=6, max_length=20)


# used for request body
class UserUpdate(BaseModel):
    # id: int = Field(...)
    name: Optional[str] = Field(min_length=2, max_length=20)
    avatar: Optional[HttpUrl] = Field(description="Avatar Url")
