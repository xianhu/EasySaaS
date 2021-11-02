# _*_ coding: utf-8 _*_

"""
paths of page
"""

# =============================================================================
PATH_INTROS = "/intros"

# =============================================================================
PATH_LOGIN = "/login"
PATH_LOGOUT = "/logout"

# =============================================================================
PATH_EMAIL_REGISTER = "/email-register"
PATH_EMAIL_REGISTER_RESULT = f"{PATH_EMAIL_REGISTER}-result"
PATH_EMAIL_REGISTER_PWD = f"{PATH_EMAIL_REGISTER}-password"
PATH_EMAIL_REGISTER_PWD_RESULT = f"{PATH_EMAIL_REGISTER}-password-result"
PATH_EMAIL_SET = {
    PATH_EMAIL_REGISTER, PATH_EMAIL_REGISTER_RESULT,
    PATH_EMAIL_REGISTER_PWD, PATH_EMAIL_REGISTER_PWD_RESULT,
}

# =============================================================================
PATH_EMAIL_RESETPWD = "/email-resetpwd"
PATH_EMAIL_RESETPWD_RESULT = f"{PATH_EMAIL_RESETPWD}-result"
PATH_EMAIL_RESETPWD_PWD = f"{PATH_EMAIL_RESETPWD}-password"
PATH_EMAIL_RESETPWD_PWD_RESULT = f"{PATH_EMAIL_RESETPWD}-password-result"
PATH_EMAIL_SET.update({
    PATH_EMAIL_RESETPWD, PATH_EMAIL_RESETPWD_RESULT,
    PATH_EMAIL_RESETPWD_PWD, PATH_EMAIL_RESETPWD_PWD_RESULT,
})

# =============================================================================
PATH_MINE = "/mine"
PATH_MINE_NOTIFY = f"{PATH_MINE}/notify"
PATH_MINE_PROFILE = f"{PATH_MINE}/profile"
PATH_MINE_UPGRADE = f"{PATH_MINE}/upgrade"
PATH_MINE_SET = {
    PATH_MINE, PATH_MINE_NOTIFY,
    PATH_MINE_PROFILE, PATH_MINE_UPGRADE,
}

# =============================================================================
PATH_ANALYSIS = "/analysis"
PATH_ANALYSIS_DEMO = f"{PATH_ANALYSIS}/demo"
PATH_ANALYSIS_SET = {PATH_ANALYSIS, PATH_ANALYSIS_DEMO}
