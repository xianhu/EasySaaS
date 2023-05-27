# _*_ coding: utf-8 _*_

"""
email module
"""

import logging
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
               html: str,
               render: Dict[str, Any]) -> int:
    """
    send email via smtp, return status code or -1 if failed
    """
    try:
        # define Jinja
        html = JinjaTemplate(html)
        subject = JinjaTemplate(subject)

        # define message and send it
        message = emails.Message(mail_from=_from, subject=subject, html=html)
        response = message.send(to=_to, render=render, smtp=smtp_options)

        # return status_code
        return response.status_code  # 250
    except Exception as excep:
        logging.error("send email error: %s", excep)
        return -1  # failed
