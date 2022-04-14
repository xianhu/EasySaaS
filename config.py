# _*_ coding: utf-8 _*_

"""
Config File
"""

import os

# define prefix
ENV_PREFIX = "ES"

# define saas application
config_app_name = "EasySaaS"
config_app_domain = os.environ.get(f"{ENV_PREFIX}_APP_DOMAIN")
config_app_secret_key = os.environ.get(f"{ENV_PREFIX}_APP_SECRET_KEY")

# define mail config
config_mail_server = os.environ.get(f"{ENV_PREFIX}_MAIL_SERVER")
config_mail_port = os.environ.get(f"{ENV_PREFIX}_MAIL_PORT")
config_mail_username = os.environ.get(f"{ENV_PREFIX}_MAIL_USERNAME")
config_mail_password = os.environ.get(f"{ENV_PREFIX}_MAIL_PASSWORD")
config_mail_sender = (config_app_name, config_mail_username)

# define uri of database
config_redis_uri = os.environ.get(f"{ENV_PREFIX}_REDIS_URI")
config_database_uri = os.environ.get(f"{ENV_PREFIX}_DATABASE_URI")

if __name__ == "__main__":
    for key, value in list(locals().items()):
        if key.startswith("config_"):
            print(key, "=>", value)
