# _*_ coding: utf-8 _*_

"""
Dash Application
"""

import logging

import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager, UserMixin
from flask_mail import Mail
from flask_redis import FlaskRedis

from config import *
from utility.consts import PATH_ROOT
from model import User, app_db

# logging config
log_format = "%(asctime)s\t%(levelname)s\t%(process)d\t%(filename)s\t%(funcName)s\t%(message)s"
logging.basicConfig(format=log_format, level=logging.WARNING)

# create app
app = dash.Dash(
    __name__,
    server=True,
    title="Dash",
    compress=True,
    serve_locally=True,
    show_undo_redo=False,
    assets_folder="assets",
    update_title="Updating...",
    url_base_pathname=PATH_ROOT,
    prevent_initial_callbacks=False,
    suppress_callback_exceptions=True,
    external_scripts=[],
    external_stylesheets=[
        dbc.icons.BOOTSTRAP,
        dbc.themes.BOOTSTRAP,
    ],
    meta_tags=[{
        "charset": "utf-8",
    }, {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }],
)

# create server
server = app.server
server.config.update(
    SECRET_KEY=config_app_secret_key,

    MAIL_SERVER=config_mail_server,
    MAIL_PORT=config_mail_port,
    MAIL_USERNAME=config_mail_username,
    MAIL_PASSWORD=config_mail_password,
    MAIL_DEFAULT_SENDER=config_mail_sender,
    MAIL_USE_TLS=False, MAIL_USE_SSL=True,

    REDIS_URL=config_redis_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=config_database_uri,
)

# initial db
app_db.init_app(server)

# initial mail
app_mail = Mail(server)

# initial redis
app_redis = FlaskRedis(server)

# initial login_manager
login_manager = LoginManager(server)


# define UserLogin class
class UserLogin(User, UserMixin):
    pass


# overwirte user_loader
@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(user_id)
