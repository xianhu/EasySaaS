# _*_ coding: utf-8 _*_

"""
email functions
"""

from typing import Any, Dict, Union

import emails
from emails.template import JinjaTemplate

from .settings import settings

# email config
smtp_options = {
    "host": settings.MAIL_SERVER,
    "port": settings.MAIL_PORT,
    "user": settings.MAIL_USERNAME,
    "password": settings.MAIL_PASSWORD,
    "tls": False, "ssl": True, "timeout": 10,
}
mail_from = (settings.APP_NAME, settings.MAIL_USERNAME)


def _send_email(mail_to: Union[str, tuple], subject: str, html_raw: str, render: Dict[str, Any]) -> int:
    """
    send email via smtp, return status code
    """
    global mail_from, smtp_options

    # define Jinja template
    jj_subject = JinjaTemplate(subject)
    jj_html = JinjaTemplate(html_raw)

    # define message and send it
    message = emails.Message(mail_from=mail_from, subject=jj_subject, html=jj_html)
    response = message.send(to=mail_to, render=render, smtp=smtp_options)

    # return status_code - 250
    return response.status_code


def send_email_of_code(code: int, mail_to: Union[str, tuple]) -> int:
    """
    send email of code, return status code
    """
    # define email content and render
    mail_subject = "Verify of {{ app_name }}"
    mail_html = "Verify code: <b>{{ code }}</b>"
    render = dict(app_name=settings.APP_NAME, code=code)

    # send email and return status code (250)
    return _send_email(mail_to, subject=mail_subject, html_raw=mail_html, render=render)
