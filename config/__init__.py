# _*_ coding: utf-8 _*_

"""
config module
"""

import os

# define prefix
ENV_PREFIX = "ES"
CONFIG_APP_NAME = "EasySaaS"

# define app config
CONFIG_APP_DOMAIN = os.environ.get(f"{ENV_PREFIX}_APP_DOMAIN")

# define mail config
CONFIG_MAIL_SERVER = os.environ.get(f"{ENV_PREFIX}_MAIL_SERVER")
CONFIG_MAIL_PORT = os.environ.get(f"{ENV_PREFIX}_MAIL_PORT")
CONFIG_MAIL_USERNAME = os.environ.get(f"{ENV_PREFIX}_MAIL_USERNAME")
CONFIG_MAIL_PASSWORD = os.environ.get(f"{ENV_PREFIX}_MAIL_PASSWORD")
CONFIG_MAIL_SENDER = (CONFIG_APP_NAME, CONFIG_MAIL_USERNAME)

# define uri of database (use redis if you need)
CONFIG_REDIS_URI = os.environ.get(f"{ENV_PREFIX}_REDIS_URI")
CONFIG_DATABASE_URI = os.environ.get(f"{ENV_PREFIX}_DATABASE_URI")

if __name__ == "__main__":
    for key, value in list(locals().items()):
        if key.startswith("CONFIG_"):
            print(f"{key} = {value}")
