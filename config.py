# _*_ coding: utf-8 _*_

"""
Config File
"""

import os

# define prefix
ENV_PREFIX = "ES"

# define saas application
CONFIG_APP_NAME = "EasySaaS"
CONFIG_APP_DOMAIN = os.environ.get(f"{ENV_PREFIX}_APP_DOMAIN")
CONFIG_SECRET_KEY = os.environ.get(f"{ENV_PREFIX}_SECRET_KEY")

# define mail config
CONFIG_MAIL_SERVER = os.environ.get(f"{ENV_PREFIX}_MAIL_SERVER")
CONFIG_MAIL_PORT = os.environ.get(f"{ENV_PREFIX}_MAIL_PORT")
CONFIG_MAIL_USERNAME = os.environ.get(f"{ENV_PREFIX}_MAIL_USERNAME")
CONFIG_MAIL_PASSWORD = os.environ.get(f"{ENV_PREFIX}_MAIL_PASSWORD")
CONFIG_MAIL_SENDER = (CONFIG_APP_NAME, CONFIG_MAIL_USERNAME)

# define uri of database (use 10/11/12 of redis)
CONFIG_REDIS_URI = os.environ.get(f"{ENV_PREFIX}_REDIS_URI")
CONFIG_DATABASE_URI = os.environ.get(f"{ENV_PREFIX}_DATABASE_URI")

if __name__ == "__main__":
    for key, value in list(locals().items()):
        if key.startswith("CONFIG_"):
            print(f"{key} = {value}")
            assert value, f"Please set {key} in environment variables."
