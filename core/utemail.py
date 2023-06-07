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


def send_email(_from: Union[str, tuple],
               _to: Union[str, tuple],
               subject: str,
               html_raw: str,
               render: Dict[str, Any]) -> int:
    """
    send email via smtp, return status code
    """
    # define Jinja template
    jj_html = JinjaTemplate(html_raw)
    jj_subject = JinjaTemplate(subject)

    # define message and send it
    message = emails.Message(mail_from=_from, subject=jj_subject, html=jj_html)
    response = message.send(to=_to, render=render, smtp=smtp_options)

    # return status_code - 250
    return response.status_code
