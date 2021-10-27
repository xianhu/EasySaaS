# _*_ coding: utf-8 _*_

"""
constants of page
"""

# =============================================================================
PATH_LOGIN = "/login"
PATH_LOGOUT = "/logout"

# =============================================================================
PATH_RESET_EMAIL = "/reset-email"
PATH_RESET_EMAIL_RESULT = f"{PATH_RESET_EMAIL}-result"
PATH_RESET_EMAIL_PWD = f"{PATH_RESET_EMAIL}-password"
PATH_RESET_EMAIL_PWD_RESULT = f"{PATH_RESET_EMAIL}-password-result"
PATH_SET_COMMON = {
    PATH_RESET_EMAIL, PATH_RESET_EMAIL_RESULT,
    PATH_RESET_EMAIL_PWD, PATH_RESET_EMAIL_PWD_RESULT,
}

# =============================================================================
PATH_REGISTER_EMAIL = "/register-email"
PATH_REGISTER_EMAIL_RESULT = f"{PATH_REGISTER_EMAIL}-result"
PATH_REGISTER_EMAIL_PWD = f"{PATH_REGISTER_EMAIL}-password"
PATH_REGISTER_EMAIL_PWD_RESULT = f"{PATH_REGISTER_EMAIL}-password-result"
PATH_SET_COMMON.update({
    PATH_REGISTER_EMAIL, PATH_REGISTER_EMAIL_RESULT,
    PATH_REGISTER_EMAIL_PWD, PATH_REGISTER_EMAIL_PWD_RESULT,
})

# =============================================================================
PATH_SYSTEM = "/system"
PATH_ANALYSIS = "/analysis"

PATH_NOTIFY = "/notify"
PATH_UPGRADE = "/upgrade"
PATH_PROFILE = "/profile"

PATH_SET_SYSTEM = {
    PATH_SYSTEM, PATH_ANALYSIS,
    PATH_NOTIFY, PATH_UPGRADE, PATH_PROFILE,
}

# =============================================================================
PATH_INDEX = "/"
PATH_INTROS = "/intros"
PATH_PRICING = "/pricing"
PATH_ABOUT = "/about"
PATH_SET_INDEX = {PATH_INDEX, PATH_INTROS, PATH_PRICING, PATH_ABOUT}
