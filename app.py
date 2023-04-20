# _*_ coding: utf-8 _*_

"""
Dash Application
"""

import logging
import secrets
import uuid

import dash
import flask_login
import flask_mail
import flask_redis
from flask import request

from config import *
from models import app_db
from models.users import User
from tasks import app_celery

# logging config
log_format = "%(asctime)s %(levelname)s %(filename)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.WARNING, datefmt=None)

# define callback manager
callback_manager = dash.CeleryManager(app_celery, cache_by=[lambda: uuid.uuid4()], expire=60)

# define cdn list base on https://cdnjs.cloudflare.com/ or https://www.unpkg.com/
cdn_bootstrap_css = "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.3/css/bootstrap.min.css"
cdn_echarts_js = "https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.2/echarts.min.js"
cdn_flowjs_js = "https://cdnjs.cloudflare.com/ajax/libs/flow.js/2.14.1/flow.min.js"
# cdn_recorder_js = "https://www.unpkg.com/js-audio-recorder@1.0.7/dist/recorder.js"
# cdn_jsmind_css = "https://unpkg.com/jsmind@0.5/style/jsmind.css"
# cdn_jsmind_js = "https://unpkg.com/jsmind@0.5/es6/jsmind.js"

# create app
app = dash.Dash(
    __name__,
    server=True,
    serve_locally=True,
    compress=True,
    show_undo_redo=False,
    url_base_pathname="/",
    assets_folder="assets",
    title=CONFIG_APP_NAME,
    update_title="Updating...",
    prevent_initial_callbacks=False,
    suppress_callback_exceptions=True,
    background_callback_manager=callback_manager,
    external_stylesheets=[
        cdn_bootstrap_css,
    ],
    external_scripts=[
        cdn_echarts_js,
        cdn_flowjs_js,
    ],
    meta_tags=[{
        "charset": "utf-8",
    }, {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }],
)

# add ga code
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-xxxx"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-xxxx');
        </script>
    </head>
    <body>
        <!--[if IE]><script>
        alert("Dash v2.7+ does not support Internet Explorer. Please use a newer browser.");
        </script><![endif]-->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

# config server
server = app.server
server.config.update(
    SECRET_KEY=secrets.token_hex(16),

    MAIL_SERVER=CONFIG_MAIL_SERVER,
    MAIL_PORT=CONFIG_MAIL_PORT,
    MAIL_USERNAME=CONFIG_MAIL_USERNAME,
    MAIL_PASSWORD=CONFIG_MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER=CONFIG_MAIL_SENDER,
    MAIL_USE_TLS=False, MAIL_USE_SSL=True,

    REDIS_URL=f"{CONFIG_REDIS_URI}/10",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=CONFIG_DATABASE_URI,

    REMEMBER_COOKIE_NAME="remember_token",
    REMEMBER_COOKIE_DURATION=60 * 60 * 24 * 7,

    PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 7,
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


# overwrite user_loader
@login_manager.user_loader
def load_user(user_id):
    user = app_db.session.get(UserLogin, user_id)
    return user if user and user.status == 1 else None


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
