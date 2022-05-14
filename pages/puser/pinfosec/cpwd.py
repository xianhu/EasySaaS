# _*_ coding: utf-8 _*_

"""
Change Password
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, html
from werkzeug import security

from app import app, app_db
from utility.consts import RE_PWD
from utility.paths import PATH_LOGIN, PATH_LOGOUT

TAG = "user-infosec-pwd"


def layout(class_name=None):
    """
    layout of component
    """
    # define components
    pwd = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-pwd", type="password"),
        dbc.Label("Current Password:", html_for=f"id-{TAG}-pwd"),
    ], class_name=None)
    pwd1 = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
        dbc.Label("New Password:", html_for=f"id-{TAG}-pwd1"),
    ], class_name=None)
    pwd2 = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-pwd2", type="password"),
        dbc.Label("Confirm Password:", html_for=f"id-{TAG}-pwd2"),
    ], class_name=None)

    # define components
    feedback = html.Div(id=f"id-{TAG}-feedback", className="text-danger text-center")
    button = dbc.Button("Update Password", id=f"id-{TAG}-button", class_name="w-100")

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("Change Password:", class_name="px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(pwd, width=12, md=4, class_name=None),
            dbc.Col(pwd1, width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(pwd2, width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(feedback, width=12, md={"size": 4, "order": "last"}, class_name="mt-0 mt-md-4"),
            dbc.Col(button, width=12, md={"size": 4, "order": None}, class_name="mt-4 mt-md-4"),
        ], align="center", class_name="p-4"),
        html.A(id={"type": "id-address", "index": TAG}),
        dbc.Modal(children=[
            dbc.ModalHeader(dbc.ModalTitle("Update Success"), close_button=False),
            dbc.ModalBody("The password was updated successfully"),
            dbc.ModalFooter(dbc.Button("Go back to re-login", href=PATH_LOGOUT, class_name="ms-auto")),
        ], id=f"id-{TAG}-modal", backdrop="static", is_open=False),
    ], class_name=class_name)


@app.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
    Output(f"id-{TAG}-modal", "is_open"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-pwd", "value"),
    State(f"id-{TAG}-pwd1", "value"),
    State(f"id-{TAG}-pwd2", "value"),
], prevent_initial_call=True)
def _button_click(n_clicks, pwd, pwd1, pwd2):
    # check user
    user = flask_login.current_user
    if not user.is_authenticated:
        return None, PATH_LOGIN, False

    # check password
    if (not pwd1) or (len(pwd1) < 6):
        return "Password is too short", dash.no_update, False
    if not RE_PWD.match(pwd1):
        return "Must contain numbers and letters", dash.no_update, False
    if (not pwd2) or (pwd2 != pwd1):
        return "Passwords are inconsistent", dash.no_update, False

    # check password
    if not security.check_password_hash(user.pwd, pwd or ""):
        return "Current password is wrong", dash.no_update, False

    # update user
    user.pwd = security.generate_password_hash(pwd1)

    # commit user
    app_db.session.merge(user)
    app_db.session.commit()

    # logout user
    flask_login.logout_user()

    # return result
    return None, dash.no_update, True
