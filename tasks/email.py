# _*_ coding: utf-8 _*_

"""
email task
"""

from typing import Any, Dict, Union

import emails
from emails.template import JinjaTemplate

from core.settings import settings
from . import app_celery

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


@app_celery.task(name="send_email", queue="email", bind=True, max_retries=3)
def send_email_task(to: Union[str, list], subject: str, html: str, render: Dict[str, Any]) -> int:
    """
    send email via smtp
    """
    return send_email(to=to, subject=subject, html=html, render=render)
