# _*_ coding: utf-8 _*_

"""
config file
"""

import os
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_hex(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # settings -- base
    ENV_PRE: str = "EASY"
    APP_NAME: str = "EasyApi"

    # settings from environment variables -- base
    APP_DOMAIN: str = os.getenv(f"{ENV_PRE}_APP_DOMAIN")

    # settings from environment variables -- email
    MAIL_SERVER = os.getenv(f"{ENV_PRE}_MAIL_SERVER")
    MAIL_PORT = os.getenv(f"{ENV_PRE}_MAIL_PORT")
    MAIL_USERNAME = os.getenv(f"{ENV_PRE}_MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv(f"{ENV_PRE}_MAIL_PASSWORD")
    MAIL_SENDER = (APP_NAME, MAIL_USERNAME)

    # settings from environment variables -- database
    REDIS_URI: str = os.getenv(f"{ENV_PRE}_REDIS_URI")
    DATABASE_URI: str = os.getenv(f"{ENV_PRE}_DATABASE_URI")

    # Config
    class Config:
        case_sensitive = True


settings = Settings()

if __name__ == '__main__':
    import pprint

    pprint.pprint(settings.dict())
