# _*_ coding: utf-8 _*_

"""
test file
"""

from core.security import create_jwt_token, get_jwt_payload
from core.utemail import send_email_of_code

# test jwt and payload
token = create_jwt_token("111")
payload = get_jwt_payload(token)
print(token, "\n", payload)

token = create_jwt_token("111", audience="system")
payload = get_jwt_payload(token, audience="system")
print(token, "\n", payload)

# test send email
send_email_of_code(123456, "qixianhu@qq.com")
