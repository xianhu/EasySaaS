# _*_ coding: utf-8 _*_

"""
Config File
"""

import os

# define text config
_config_text_english = {
    "app_name": "EasySaaS",
    "login": "Login",
    "logout": "Logout",
    "register": "Register",
    "forget_password": "Forget Password",
}

_config_text_chinese = {
    "app_name": "EasySaaS",
    "login": "登录",
    "logout": "登出",
    "register": "注册",
    "forget_password": "忘记密码",
}

config_text = _config_text_english

# define prefix
ENV_PREFIX = "ES"

# define saas application
config_app_domain = os.environ.get(f"{ENV_PREFIX}_APP_DOMAIN")
config_secret_key = os.environ.get(f"{ENV_PREFIX}_SECRET_KEY")

# define mail config
config_mail_server = os.environ.get(f"{ENV_PREFIX}_MAIL_SERVER")
config_mail_port = os.environ.get(f"{ENV_PREFIX}_MAIL_PORT")
config_mail_username = os.environ.get(f"{ENV_PREFIX}_MAIL_USERNAME")
config_mail_password = os.environ.get(f"{ENV_PREFIX}_MAIL_PASSWORD")
config_mail_sender = (config_text["app_name"], config_mail_username)

# define uri of database
config_redis_uri = os.environ.get(f"{ENV_PREFIX}_REDIS_URI")
config_database_uri = os.environ.get(f"{ENV_PREFIX}_DATABASE_URI")

if __name__ == "__main__":
    for key, value in list(locals().items()):
        if key.startswith("config_"):
            print(key, "=>", value)
