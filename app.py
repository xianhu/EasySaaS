# _*_ coding: utf-8 _*_

"""
Dash Application
"""

import logging
import uuid

import dash
from flask import request

from core.settings import settings
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

# create app
app = dash.Dash(
    __name__,
    compress=True,
    show_undo_redo=False,
    url_base_pathname="/",
    title=settings.APP_NAME,
    update_title="Updating...",
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
    }, {
        "name": "keywords",
        "content": "saas, easy, python, dash, flask, echarts",
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
    SECRET_KEY=settings.SECRET_KEY,
    PERMANENT_SESSION_LIFETIME=settings.PERMANENT_SESSION_LIFETIME,
)


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
