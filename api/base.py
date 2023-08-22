# _*_ coding: utf-8 _*_

"""
base import
"""

import json
import logging
import os
import random
import time
import urllib.parse as urllib_parse
import uuid
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

import sqlalchemy
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi import Body, Cookie, Depends, Form, Header, Path, Query, Request, Response
from fastapi import File as UploadFileClass, UploadFile  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr, Field, HttpUrl, UUID4
from redis import Redis
from sqlalchemy import func
from sqlalchemy.orm import Session

from core import check_password_hash, get_password_hash
from core import create_jwt_token, get_jwt_payload
from core import get_id_string, iter_file, settings
from core import send_email_of_code, send_phone_of_code
from data import FILETAG_SYSTEM_SET, PhoneStr, get_redis, get_session
from data.models import File, FileTag, FileTagFile, Project, User, UserLog, UserProject
from data.schemas import FileCreate, FileSchema, FileUpdate, Resp, RespSend
from data.schemas import FileTagCreate, FileTagSchema, FileTagUpdate
from data.schemas import UserCreate, UserCreateEmail, UserCreatePhone, UserSchema, UserUpdate

__all__ = [
    # from python
    "json", "logging", "os", "random", "urllib_parse", "uuid",
    "time", "date", "datetime", "timedelta", "timezone",
    "Enum", "Any", "Dict", "List", "Optional",

    # from pip install
    "APIRouter", "BackgroundTasks", "HTTPException", "status",
    "Body", "Cookie", "Depends", "Form", "Header", "Path", "Query", "Request", "Response",
    "UploadFileClass", "UploadFile", "FileResponse", "StreamingResponse",
    "OAuth2PasswordBearer", "OAuth2PasswordRequestForm",
    "EmailStr", "Field", "HttpUrl", "UUID4", "sqlalchemy", "func", "Redis", "Session",

    # from core module
    "check_password_hash", "get_password_hash", "create_jwt_token", "get_jwt_payload",
    "get_id_string", "iter_file", "settings", "send_email_of_code", "send_phone_of_code",

    # from data module -- utils
    "FILETAG_SYSTEM_SET", "PhoneStr", "get_redis", "get_session",

    # from data module -- models
    "File", "FileTag", "FileTagFile", "Project", "User", "UserLog", "UserProject",

    # from data module -- schemas
    "FileCreate", "FileSchema", "FileUpdate", "Resp", "RespSend",
    "FileTagCreate", "FileTagSchema", "FileTagUpdate",
    "UserCreate", "UserCreateEmail", "UserCreatePhone", "UserSchema", "UserUpdate",
]
