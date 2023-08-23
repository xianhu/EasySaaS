# _*_ coding: utf-8 _*_

"""
test file
"""

import logging
import pprint
import time

from core import create_jwt_token, get_jwt_payload
from core import send_email_of_code, send_phone_of_code
from core import settings, settings_name

# print settings
pprint.pprint(settings.model_dump())
pprint.pprint(settings_name)

# test jwt and payload -- expire_duration
token = create_jwt_token("111", expire_duration=10)
logging.warning("get payload: %s", get_jwt_payload(token))

# Signature has expired
time.sleep(15)
logging.warning("get payload: %s", get_jwt_payload(token))

# test jwt and payload -- audience
token = create_jwt_token("111", audience="web")
logging.warning("get payload: %s", get_jwt_payload(token, audience="web"))

# test send email and phone
status_code = send_email_of_code(123456, "qixianhu@qq.com")
logging.warning("send email to qixianhu@qq.com: %s", status_code)

status_code = send_phone_of_code(123456, "+86-18000000000")
logging.warning("send phone to +86-18000000000: %s", status_code)
