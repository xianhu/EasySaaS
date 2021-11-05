# _*_ coding: utf-8 _*_

"""
config file
"""

import os

# define saas application
config_app_name = "EasySaaS"
config_app_domain = os.environ.get("APP_DOMAIN")
config_app_secret_key = os.environ.get("APP_SECRET_KEY")

# define uri of database
config_database_uri = "sqlite:///.data/main.db?charset=utf8"
# "mysql+pymysql://user:pwd@localhost:3306/main?charset=utf8"

# define uri of redis
config_redis_uri = "redis://localhost:6379/0"
config_redis_uri_1 = "redis://localhost:6379/1"
config_redis_uri_2 = "redis://localhost:6379/2"

# define mail config
config_mail_server = os.environ.get("MAIL_SERVER")
config_mail_port = os.environ.get("MAIL_PORT")
config_mail_username = os.environ.get("MAIL_USERNAME")
config_mail_password = os.environ.get("MAIL_PASSWORD")
config_mail_sender = (config_app_name, config_mail_username)

# define logging format
config_log_format = "%(asctime)s\t%(levelname)s\t%(process)d\t%(filename)s\t%(funcName)s\t%(message)s"

if __name__ == "__main__":
    _vars = list(locals().items())
    for key, value in _vars:
        print(key, "=>", value)
