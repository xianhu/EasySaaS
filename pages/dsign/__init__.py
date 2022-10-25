# _*_ coding: utf-8 _*_

"""
sign page
"""

from dash import html

from utility.paths import PATH_LOGIN, PATH_SIGNUP, PATH_FORGOTPWD

# define link text
LINK_LOGIN = "Log in"
LINK_SIGNUP = "Sign up"
LINK_FORGOTPWD = "Forgot password?"

# define label text
LABEL_EMAIL = "Email"
LABEL_PWD = "Password"
LABEL_PWD_CFM = "Confirm password"

# define text
LOGIN_TEXT_HD = "Welcome back"
LOGIN_TEXT_SUB = "Login to analysis your data."
LOGIN_TEXT_BUTTON = "Log in"

SIGNUP_TEXT_HD = "Welcome to ES"
SIGNUP_TEXT_SUB = "Fill out the email to get started."
SIGNUP_TEXT_BUTTON = "Verify the email"

FORGOTPWD_TEXT_HD = "Forgot password?"
FORGOTPWD_TEXT_SUB = "Fill out the email to reset password."
FORGOTPWD_TEXT_BUTTON = "Verify the email"

SETPWD_TEXT_HD = "Set password"
SETPWD_TEXT_SUB = "Set the password of this email please."
SETPWD_TEXT_BUTTON = "Set password"

# define error message
ERROR_EMAIL_FORMAT = "Format of email is invalid"
ERROR_EMAIL_EXIST = "This email has been registered"
ERROR_EMAIL_NOTEXIST = "This Email does't exist"

ERROR_PWD_SHORT = "Password is too short"
ERROR_PWD_FORMAT = "Password must contain numbers and letters"
ERROR_PWD_INCORRECT = "Password is incorrect"
ERROR_PWD_INCONSISTENT = "Passwords are inconsistent"

# define components
A_LOGIN = html.A(LINK_LOGIN, href=PATH_LOGIN)
A_SIGNUP = html.A(LINK_SIGNUP, href=PATH_SIGNUP)
A_FORGOTPWD = html.A(LINK_FORGOTPWD, href=PATH_FORGOTPWD)
