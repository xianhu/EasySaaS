# _*_ coding: utf-8 _*_

"""
Dash Application
"""

import logging

import celery
import dash
import flask_login
import flask_mail
import flask_redis
from flask import request

from config import *
from models import app_db
from models.users import User

# logging config
log_format = "%(asctime)s %(levelname)s %(filename)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.WARNING)

# celery -A app.app_celery worker -l INFO --purge
broker, backend = f"{config_redis_uri}/11", f"{config_redis_uri}/12"
app_celery = celery.Celery(__name__, broker=broker, backend=backend, include=[
    "pages.dsign.plogin", "pages.dsign.pemail", "pages.dsign.psetpwd",
])

# define callback manager
callback_manager = dash.CeleryManager(app_celery)

# create app
app = dash.Dash(
    __name__,
    server=True,
    serve_locally=True,
    compress=True,
    show_undo_redo=False,
    url_base_pathname="/",
    # routes_pathname_prefix="/",
    # requests_pathname_prefix="/",
    assets_folder="assets",
    assets_ignore="favicon1.*",
    title=config_app_name,
    update_title="Updating...",
    prevent_initial_callbacks=False,
    suppress_callback_exceptions=True,
    background_callback_manager=callback_manager,
    external_stylesheets=[],
    external_scripts=[],
    meta_tags=[{
        "charset": "utf-8",
    }, {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }],
)

# config server
server = app.server
server.config.update(
    SECRET_KEY=config_secret_key,

    MAIL_SERVER=config_mail_server,
    MAIL_PORT=config_mail_port,
    MAIL_USERNAME=config_mail_username,
    MAIL_PASSWORD=config_mail_password,
    MAIL_DEFAULT_SENDER=config_mail_sender,
    MAIL_USE_TLS=False, MAIL_USE_SSL=True,

    REDIS_URL=f"{config_redis_uri}/10",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=config_database_uri,

    REMEMBER_COOKIE_NAME="remember_token",
    REMEMBER_COOKIE_DURATION=60 * 60 * 24 * 7,
)

# initial db
app_db.init_app(server)

# initial mail
app_mail = flask_mail.Mail(server)

# initial redis
app_redis = flask_redis.FlaskRedis(server)

# initial login_manager
login_manager = flask_login.LoginManager(server)


# define UserLogin class
class UserLogin(User, flask_login.UserMixin):
    pass


# overwirte user_loader
@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(user_id)


# func before_request
@server.before_request
def before_request():
    logging.debug(f"request.headers = {request.headers}")
    logging.debug(f"request.remote_addr = {request.remote_addr}")
    return None


# func after_request
@server.after_request
def after_request(response):
    logging.debug(f"response.headers = {response.headers}")
    logging.debug(f"response.status = {response.status}")
    return response
