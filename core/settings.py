# _*_ coding: utf-8 _*_

"""
settings and error tips
"""

import os
import re
import secrets
from re import Pattern

from pydantic import BaseSettings

# prefix
ENV_PRE = "ES"


class Settings(BaseSettings):
    # settings from environment -- debug
    DEBUG: bool = int(os.getenv(f"{ENV_PRE}_DEBUG", "1"))

    # settings from environment -- name and version
    APP_NAME: str = os.getenv(f"{ENV_PRE}_APP_NAME", ENV_PRE)
    APP_VERSION: str = os.getenv(f"{ENV_PRE}_APP_VERSION", "0.0.1-beta")

    # settings from environment -- domain and secret key
    APP_DOMAIN: str = os.getenv(f"{ENV_PRE}_APP_DOMAIN", "http://127.0.0.1:8000")
    SECRET_KEY: str = os.getenv(f"{ENV_PRE}_SECRET_KEY", secrets.token_urlsafe(32))

    # settings from environment -- email
    MAIL_SERVER: str = os.getenv(f"{ENV_PRE}_MAIL_SERVER")
    MAIL_PORT: str = os.getenv(f"{ENV_PRE}_MAIL_PORT")
    MAIL_USERNAME: str = os.getenv(f"{ENV_PRE}_MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv(f"{ENV_PRE}_MAIL_PASSWORD")

    # settings from environment -- database
    REDIS_URI: str = os.getenv(f"{ENV_PRE}_REDIS_URI")
    DATABASE_URI: str = os.getenv(f"{ENV_PRE}_DATABASE_URI")

    # settings -- others
    FOLDER_UPLOAD: str = "/tmp"
    MAX_FILE_SIZE: int = 1024 * 1024 * 25

    # settings -- session or token
    PERMANENT_SESSION_LIFETIME: int = 60 * 60 * 24 * 7
    ACCESS_TOKEN_EXPIRE_DURATION: int = 60 * 60 * 24 * 7
    NORMAL_TOKEN_EXPIRE_DURATION: int = 60 * 10  # 10 minutes

    # settings -- regular of data field
    RE_PHONE: Pattern = re.compile(r"^(13\d|14[5|7]|15\d|18\d)\d{8}$")
    RE_EMAIL: Pattern = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    RE_PASSWORD: Pattern = re.compile(r"^(?!\d+$)(?![a-zA-Z]+$)[\d\D]{6,20}$")

    # Config
    class Config:
        case_sensitive = True


settings = Settings()


class ErrorTips(BaseSettings):
    # error tips -- common
    CODE_INVALID: str = "Code is invalid or expired"
    TOKEN_INVALID: str = "Token is invalid or expired"
    SCOPE_INVALID: str = "Scope is no permission"
    CAPTCHA_INCORRECT: str = "Captcha is incorrect"

    # error tips -- password
    PWD_INCORRECT: str = "Password is incorrect"
    PWD_FMT_SHORT: str = "Password is too short"
    PWD_FMT_ERROR: str = "Password must contain numbers and letters"
    PWD_FMT_INCONSISTENT: str = "Passwords are inconsistent"

    # error tips -- email
    EMAIL_INVALID: str = "Format of email is invalid"
    EMAIL_SEND_FAILED: str = "Email send failed"
    EMAIL_EXISTED: str = "This email existed in system"
    EMAIL_NOT_EXISTED: str = "This email not existed in system"

    # error tips -- user
    USER_EXISTED: str = "This user existed in system"
    USER_NOT_EXISTED: str = "This user not existed in system"

    # error tips -- file
    FILE_NOT_EXISTED: str = "file not existed"
    FILE_TYPE_INVALID: str = "file type invalid"
    FILE_SIZE_EXCEEDED: str = "file size too large"

    # error tips -- crud
    QUERY_FAILED: str = "Query failed"
    CREATE_FAILED: str = "Create failed"
    UPDATE_FAILED: str = "Update failed"
    DELETE_FAILED: str = "Delete failed"

    # Config
    class Config:
        case_sensitive = True


error_tips = ErrorTips()

if __name__ == "__main__":
    import pprint

    pprint.pprint(settings.dict())
    pprint.pprint(error_tips.dict())
