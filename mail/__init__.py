# _*_ coding: utf-8 _*_

"""
mail service
"""

import flask_mail

from app import app_celery, app_mail


@app_celery.task
def send_email_simple(subject, body, html, sender, recipients):
    """
    send email simple
    """
    message = flask_mail.Message(
        subject=subject,
        body=body,
        html=html,
        sender=sender,
        recipients=recipients,
    )
    app_mail.send(message)
    return


if __name__ == "__main__":
    _subject = "subject"
    _body = "body"
    _html = "<h1>html</h1>"
    _sender = "(sender, noreply@databai.com)"
    _recipients = ["qixianhu@qq.com", ]
    send_email_simple(_subject, _body, _html, _sender, _recipients)
