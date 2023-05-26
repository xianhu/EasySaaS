# _*_ coding: utf-8 _*_

"""
utils of email
"""

import logging
import random
from typing import Any, Dict, Optional, Union

import emails
from emails.template import JinjaTemplate

from .security import create_token_data
from .settings import settings

# email config
smtp_options = {
    "host": settings.MAIL_SERVER,
    "port": settings.MAIL_PORT,
    "user": settings.MAIL_USERNAME,
    "password": settings.MAIL_PASSWORD,
    "tls": False, "ssl": True, "timeout": 10,
}


def send_email(_from: Union[str, tuple], _to: Union[str, tuple], subject: str, html: str, render: Dict[str, Any]) -> int:
    """
    send email via smtp, return status code or -1 if failed
    """
    try:
        message = emails.Message(mail_from=_from, subject=JinjaTemplate(subject), html=JinjaTemplate(html))
        response = message.send(to=_to, render=render, smtp=smtp_options)
        return response.status_code  # 250
    except Exception as excep:
        logging.error("send email error: %s", excep)
        return -1  # failed


def send_email_verify(email: str, is_code: bool = True, _type: str = None) -> Optional[str]:
    """
    send code or link to email, and return token with sub: {email, code, type}
    :return token or None if send failed
    """
    # define code and token
    code = random.randint(100000, 999999) if is_code else 0
    data = dict(sub=email, code=code, type=_type)
    token = create_token_data(data, expires_duration=settings.NORMAL_TOKEN_EXPIRE_DURATION)

    # define email content
    mail_subject = "Verify of {{ app_name }}"
    if is_code:
        mail_html = "Verify code: <b>{{ code }}</b>"
    else:
        mail_html = "Verify link: <a href='{{ link }}'>click</a>"

    # define link and render
    link = f"{settings.APP_DOMAIN}?token={token}"
    render = dict(app_name=settings.APP_NAME, code=code, link=link)

    # send email and check status
    _from = (settings.APP_NAME, settings.MAIL_USERNAME)
    status = send_email(_from, email, subject=mail_subject, html=mail_html, render=render)

    # return token or None
    return token if status == 250 else None
