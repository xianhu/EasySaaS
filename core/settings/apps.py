# _*_ coding: utf-8 _*_

"""
settings of application
"""

import os
import secrets

from pydantic_settings import BaseSettings

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

    # settings -- session or token duration
    PERMANENT_SESSION_LIFETIME: int = 60 * 60 * 24 * 7
    NORMAL_TOKEN_EXPIRE_DURATION: int = 60 * 10  # 10 minutes
    ACCESS_TOKEN_EXPIRE_DURATION: int = 60 * 60 * 24 * 300
    REFRESH_TOKEN_EXPIRE_DURATION: int = 60 * 60 * 24 * 7

    # Config
    class Config:
        case_sensitive = True


# instance
settings = Settings()
