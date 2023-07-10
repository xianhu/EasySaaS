# _*_ coding: utf-8 _*_

"""
user schema
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


# used for response_model
class UserSchema(BaseModel):
    id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[HttpUrl] = None
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
    # id: str = Field(..., description="User ID")
    nickname: Optional[str] = Field(None, min_length=2, max_length=20)
    avatar: Optional[HttpUrl] = Field(None, description="Avatar Url")
