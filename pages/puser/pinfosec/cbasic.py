# _*_ coding: utf-8 _*_

"""
Basic Information
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, html

from app import app, app_db
from utility.consts import RE_PHONE
from utility.paths import PATH_LOGIN

TAG = "user-infosec-basic"


def layout(class_name=None):
    """
    layout of component
    """
    # define components
    user = flask_login.current_user
    email = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email", value=user.email, readonly=True),
        dbc.Label("Email:", html_for=f"id-{TAG}-email"),
    ], class_name=None)
    name = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-name", type="text", value=user.name),
        dbc.Label("FullName:", html_for=f"id-{TAG}-name"),
    ], class_name=None)
    phone = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-phone", type="tel", value=user.phone),
        dbc.Label("Phone:", html_for=f"id-{TAG}-phone"),
    ], class_name=None)

    # define components
    feedback = html.Div(id=f"id-{TAG}-feedback", className="text-danger text-center")
    button = dbc.Button("Update Information", id=f"id-{TAG}-button", class_name="w-100")

    # define components
    return dbc.Card(children=[
        dbc.CardHeader("Basic Information:", class_name="px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(email, width=12, md=4, class_name=None),
            dbc.Col(name, width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(phone, width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(feedback, width=12, md={"size": 4, "order": "last"}, class_name="mt-0 mt-md-4"),
            dbc.Col(button, width=12, md={"size": 4, "order": None}, class_name="mt-4 mt-md-4"),
        ], align="center", justify="start", class_name="p-4"),
        html.A(id={"type": "id-address", "index": TAG}),
        dbc.Modal(children=[
            dbc.ModalHeader(dbc.ModalTitle("Update Success"), close_button=False),
            dbc.ModalBody("The basic information was updated successfully"),
        ], id=f"id-{TAG}-modal", backdrop=True, is_open=False),
    ], class_name=class_name)


@app.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
    Output(f"id-{TAG}-modal", "is_open"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-name", "value"),
    State(f"id-{TAG}-phone", "value"),
], prevent_initial_call=True)
def _button_click(n_clicks, name, phone):
    # check user
    user = flask_login.current_user
    if not user.is_authenticated:
        return None, PATH_LOGIN, False

    # check phone
    if phone and (not RE_PHONE.match(phone.strip())):
        return "Phone format is error", dash.no_update, False

    # check name and phone
    name, phone = (name or "").strip(), (phone or "").strip()
    if name == (user.name or "") and phone == (user.phone or ""):
        return "No change has happened", dash.no_update, False

    # update user
    user.name = name or ""
    user.phone = phone or ""

    # commit user
    app_db.session.merge(user)
    app_db.session.commit()

    # return result
    return None, dash.no_update, True
