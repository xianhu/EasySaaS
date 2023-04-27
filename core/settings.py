# _*_ coding: utf-8 _*_

"""
settings file
"""

import os
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    # settings -- security
    SECRET_KEY: str = secrets.token_hex(32)
    PERMANENT_SESSION_LIFETIME: int = 60 * 60 * 24 * 7
    ACCESS_TOKEN_EXPIRE_DURATION: int = 60 * 60 * 24 * 7

    # settings -- base
    ENV_PRE: str = "ES"
    APP_NAME: str = "EasySaaS"

    # settings from environment variables -- base
    APP_DOMAIN: str = os.getenv(f"{ENV_PRE}_APP_DOMAIN")

    # settings from environment variables -- email
    MAIL_SERVER: str = os.getenv(f"{ENV_PRE}_MAIL_SERVER")
    MAIL_PORT: str = os.getenv(f"{ENV_PRE}_MAIL_PORT")
    MAIL_USERNAME: str = os.getenv(f"{ENV_PRE}_MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv(f"{ENV_PRE}_MAIL_PASSWORD")
    MAIL_SENDER: list = (APP_NAME, MAIL_USERNAME)

    # settings from environment variables -- database
    REDIS_URI: str = os.getenv(f"{ENV_PRE}_REDIS_URI")
    DATABASE_URI: str = os.getenv(f"{ENV_PRE}_DATABASE_URI")

    # Config
    class Config:
        case_sensitive = True


settings = Settings()


class ErrorTips(BaseSettings):
    CAPTCHA_INCORRECT: str = "Captcha is incorrect"

    # error tips -- email
    EMAIL_INVALID: str = "Format of email is invalid"
    EMAIL_EXISTED: str = "This email has been registered"
    EMAIL_NOT_EXISTED: str = "This email hasn't been registered"

    # error tips -- password
    PWD_INCORRECT: str = "Password is incorrect"
    PWD_FMT_SHORT: str = "Password is too short"
    PWD_FMT_ERROR: str = "Password must contain numbers and letters"
    PWD_INCONSISTENT: str = "Passwords are inconsistent"


error_tips = ErrorTips()

if __name__ == "__main__":
    import pprint

    pprint.pprint(settings.dict())
