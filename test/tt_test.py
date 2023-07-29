# _*_ coding: utf-8 _*_

"""
test file
"""

import logging
import time

from core.security import create_jwt_token, get_jwt_payload
from core.utemail import send_email_of_code

# test jwt and payload -- expire_duration
token = create_jwt_token("111", expire_duration=10)
logging.warning("get payload: %s", get_jwt_payload(token))

# Signature has expired
time.sleep(15)
logging.warning("get payload: %s", get_jwt_payload(token))

# test jwt and payload -- audience
token = create_jwt_token("111", audience="web")
logging.warning("get payload: %s", get_jwt_payload(token, audience="web"))

# test send email
send_email_of_code(123456, "qixianhu@qq.com")
