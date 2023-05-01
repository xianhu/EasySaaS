# _*_ coding: utf-8 _*_

"""
settings file
"""

import os
import secrets

from pydantic import BaseSettings

ENV_PRE = "ES"


class Settings(BaseSettings):
    # settings -- security
    PERMANENT_SESSION_LIFETIME: int = 60 * 60 * 24 * 7
    ACCESS_TOKEN_EXPIRE_DURATION: int = 60 * 60 * 24 * 7
    SECRET_KEY: str = os.getenv(f"{ENV_PRE}_SECRET_KEY", secrets.token_urlsafe(32))

    # settings -- base
    APP_NAME: str = os.getenv(f"{ENV_PRE}_APP_NAME")
    APP_DOMAIN: str = os.getenv(f"{ENV_PRE}_APP_DOMAIN")

    # settings from environment variables -- email
    MAIL_SERVER: str = os.getenv(f"{ENV_PRE}_MAIL_SERVER")
    MAIL_PORT: str = os.getenv(f"{ENV_PRE}_MAIL_PORT")
    MAIL_USERNAME: str = os.getenv(f"{ENV_PRE}_MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv(f"{ENV_PRE}_MAIL_PASSWORD")

    # settings from environment variables -- database
    REDIS_URI: str = os.getenv(f"{ENV_PRE}_REDIS_URI")
    DATABASE_URI: str = os.getenv(f"{ENV_PRE}_DATABASE_URI")

    # Config
    class Config:
        case_sensitive = True


settings = Settings()


class ErrorTips(BaseSettings):
    # error tips -- common
    CAPTCHA_INCORRECT: str = "Captcha is incorrect"
    TOKEN_INVALID: str = "Token is invalid or expired"
    CODE_INVALID: str = "Code is invalid or expired"

    # error tips -- password
    PWD_INCORRECT: str = "Password is incorrect"
    PWD_FMT_SHORT: str = "Password is too short"
    PWD_FMT_ERROR: str = "Password must contain numbers and letters"
    PWD_FMT_INCONSISTENT: str = "Passwords are inconsistent"

    # error tips -- email
    EMAIL_INVALID: str = "Format of email is invalid"
    EMAIL_EXISTED: str = "This email existed in system"
    EMAIL_NOT_EXISTED: str = "This email not existed in system"
    EMAIL_SEND_FAILED: str = "Email send failed"

    # error tips -- user
    USER_EXISTED: str = "This user existed in system"
    USER_NOT_EXISTED: str = "This user not existed in system"

    # error tips -- crud
    CREATE_FAILED: str = "Create failed"
    UPDATE_FAILED: str = "Update failed"
    DELETE_FAILED: str = "Delete failed"
    QUERY_FAILED: str = "Query failed"


error_tips = ErrorTips()

if __name__ == "__main__":
    import pprint

    pprint.pprint(settings.dict())
    pprint.pprint(error_tips.dict())
