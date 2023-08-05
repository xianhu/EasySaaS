# _*_ coding: utf-8 _*_

"""
base model
"""

import random
import time
from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi import Body, Depends, Form, Path, Query, Request, UploadFile
from fastapi import File as UploadFileClass  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from redis import Redis
from sqlalchemy.orm import Session

from core import check_password_hash, get_password_hash
from core import create_jwt_token, get_jwt_payload
from core import get_id_string, iter_file, settings
from core import send_email_of_code, send_phone_of_code
from data import FILETAG_SYSTEM_SET, PhoneStr, get_redis, get_session
from data.models import File, FileTag, FileTagFile, User, UserLog
from data.schemas import AccessToken, Resp
from data.schemas import FileCreate, FileSchema, FileUpdate
from data.schemas import FileTagCreate, FileTagSchema, FileTagUpdate
from data.schemas import UserCreate, UserCreateEmail, UserCreatePhone, UserSchema, UserUpdate

__all__ = [
    "random", "time", "datetime", "Enum", "List", "Optional",
    "APIRouter", "BackgroundTasks", "HTTPException", "status",
    "Body", "Depends", "Form", "Path", "Query", "Request", "UploadFile",
    "UploadFileClass", "FileResponse", "StreamingResponse",
    "OAuth2PasswordBearer", "OAuth2PasswordRequestForm",
    "EmailStr", "Field", "Redis", "Session",
    "check_password_hash", "get_password_hash", "create_jwt_token", "get_jwt_payload",
    "get_id_string", "iter_file", "settings", "send_email_of_code", "send_phone_of_code",
    "FILETAG_SYSTEM_SET", "PhoneStr", "get_redis", "get_session",
    "File", "FileTag", "FileTagFile", "User", "UserLog",
    "AccessToken", "Resp", "FileCreate", "FileSchema", "FileUpdate",
    "FileTagCreate", "FileTagSchema", "FileTagUpdate",
    "UserCreate", "UserCreateEmail", "UserCreatePhone", "UserSchema", "UserUpdate",
]