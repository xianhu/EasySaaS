# _*_ coding: utf-8 _*_

"""
constants of page
"""

from dash import html

# =============================================================================
PATH_LOGIN = "/login"
PATH_LOGOUT = "/logout"

# =============================================================================
PATH_RESET_EMAIL = "/reset-email"
PATH_RESET_EMAIL_RESULT = f"{PATH_RESET_EMAIL}-result"
PATH_RESET_EMAIL_PWD = f"{PATH_RESET_EMAIL}-password"
PATH_RESET_EMAIL_PWD_RESULT = f"{PATH_RESET_EMAIL}-password-result"
PATH_EMAIL_SET = {
    PATH_RESET_EMAIL, PATH_RESET_EMAIL_RESULT,
    PATH_RESET_EMAIL_PWD, PATH_RESET_EMAIL_PWD_RESULT,
}

# =============================================================================
PATH_REGISTER_EMAIL = "/register-email"
PATH_REGISTER_EMAIL_RESULT = f"{PATH_REGISTER_EMAIL}-result"
PATH_REGISTER_EMAIL_PWD = f"{PATH_REGISTER_EMAIL}-password"
PATH_REGISTER_EMAIL_PWD_RESULT = f"{PATH_REGISTER_EMAIL}-password-result"
PATH_EMAIL_SET.update({
    PATH_REGISTER_EMAIL, PATH_REGISTER_EMAIL_RESULT,
    PATH_REGISTER_EMAIL_PWD, PATH_REGISTER_EMAIL_PWD_RESULT,
})

# =============================================================================
COMP_A_LOGIN = html.A("Sign in", href=PATH_LOGIN)
COMP_A_REGISTER = html.A("Sign up", href=PATH_REGISTER_EMAIL)
COMP_A_RESET = html.A("Forget password?", href=PATH_RESET_EMAIL)
