# _*_ coding: utf-8 _*_

"""
base model
"""

import json
import logging
import os
import random
import time
import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi import Body, Cookie, Depends, Form, Header, Path, Query, Request, Response, UploadFile
from fastapi import File as UploadFileClass  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr, Field
from redis import Redis
from sqlalchemy import func
from sqlalchemy.orm import Session

from core import check_password_hash, get_password_hash
from core import create_jwt_token, get_jwt_payload
from core import get_id_string, iter_file, settings
from core import send_email_of_code, send_phone_of_code
from data import FILETAG_SYSTEM_SET, PhoneStr, get_redis, get_session
from data.models import File, FileTag, FileTagFile, Project, User, UserLog, UserProject
from data.schemas import AccessToken, Resp
from data.schemas import FileCreate, FileSchema, FileUpdate
from data.schemas import FileTagCreate, FileTagSchema, FileTagUpdate
from data.schemas import UserCreate, UserCreateEmail, UserCreatePhone, UserSchema, UserUpdate

__all__ = [
    "json", "logging", "os", "random", "uuid", "time", "date", "datetime",
    "Enum", "Any", "Dict", "List", "Optional",

    "APIRouter", "BackgroundTasks", "HTTPException", "status",
    "Body", "Cookie", "Depends", "Form", "Header", "Path", "Query", "Request", "Response", "UploadFile",
    "UploadFileClass", "FileResponse", "StreamingResponse",
    "OAuth2PasswordBearer", "OAuth2PasswordRequestForm",
    "EmailStr", "Field", "Redis", "func", "Session",

    "check_password_hash", "get_password_hash", "create_jwt_token", "get_jwt_payload",
    "get_id_string", "iter_file", "settings", "send_email_of_code", "send_phone_of_code",
    "FILETAG_SYSTEM_SET", "PhoneStr", "get_redis", "get_session",
    "File", "FileTag", "FileTagFile", "Project", "User", "UserLog", "UserProject",
    "AccessToken", "Resp", "FileCreate", "FileSchema", "FileUpdate",
    "FileTagCreate", "FileTagSchema", "FileTagUpdate",
    "UserCreate", "UserCreateEmail", "UserCreatePhone", "UserSchema", "UserUpdate",
]
