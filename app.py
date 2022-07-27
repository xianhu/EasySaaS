# _*_ coding: utf-8 _*_

"""
Dash Application
"""

import logging

import dash
import dash_bootstrap_components as dbc
from celery import Celery
from dash.long_callback import CeleryLongCallbackManager
from flask_login import LoginManager, UserMixin
from flask_mail import Mail
from flask_redis import FlaskRedis

from config import *
from model import User, app_db

# logging config
log_format = "%(asctime)s\t%(levelname)s\t%(filename)s\t%(funcName)s\t%(message)s"
logging.basicConfig(format=log_format, level=logging.WARNING)

# celery -A app.app_celery worker -l INFO
app_celery = Celery(
    __name__,
    broker=f"{config_redis_uri}/11",
    backend=f"{config_redis_uri}/12",
    include=[
        "pages.panalysis.pfileud",
    ],
)
lc_manager = CeleryLongCallbackManager(app_celery)

# create app
app = dash.Dash(
    __name__,
    server=True,
    compress=True,
    serve_locally=True,
    show_undo_redo=False,
    prevent_initial_callbacks=False,
    suppress_callback_exceptions=True,
    long_callback_manager=lc_manager,
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

    REDIS_URL=f"{config_redis_uri}/10",
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
