# _*_ coding: utf-8 _*_

"""
utils of email
"""

import json
import random
from typing import Any, Dict, Union

import emails
from emails.template import JinjaTemplate

from .security import create_token
from ..settings import settings

# email config
smtp_options = {
    "host": settings.MAIL_SERVER,
    "port": settings.MAIL_PORT,
    "user": settings.MAIL_USERNAME,
    "password": settings.MAIL_PASSWORD,
    "tls": False, "ssl": True, "timeout": 10,
}


def send_email(to: Union[str, list], subject: str, html: str, render: Dict[str, Any]) -> int:
    """
    send email via smtp
    """
    message = emails.Message(
        subject=JinjaTemplate(subject),
        html=JinjaTemplate(html),
        mail_from=settings.MAIL_SENDER,
    )
    response = message.send(to=to, render=render, smtp=smtp_options)
    return response.status_code  # 250


def send_email_code(email, _type=None):
    """
    send code to email
    """
    code = random.randint(100001, 999999)
    sub = json.dumps(dict(email=email, code=code, type=_type))
    token = create_token(sub, expires_duration=60 * 10)

    # define email content
    mail_subject = "Verify code of {{ app_name }}"
    mail_html = "Verify code: <b>{{ code }}</b>"

    # send email
    render = dict(app_name=settings.APP_NAME, code=code)
    return send_email(to=email, subject=mail_subject, html=mail_html, render=render)
