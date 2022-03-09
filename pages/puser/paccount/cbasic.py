# _*_ coding: utf-8 _*_

"""
Basic Information
"""

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app, app_db
from utility.consts import RE_PHONE

TAG = "user-basic"


def layout(pathname, search):
    """
    layout of card
    """
    # define text
    name = flask_login.current_user.name
    email = flask_login.current_user.email
    phone = flask_login.current_user.phone

    # define components
    c_email = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email", value=email, disabled=True),
        dbc.Label("Email:", html_for=f"id-{TAG}-email"),
    ])
    c_name = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-name", type="text", value=name),
        dbc.Label("FullName:", html_for=f"id-{TAG}-name"),
    ])
    c_phone = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-phone", type="tel", value=phone),
        dbc.Label("Phone:", html_for=f"id-{TAG}-phone"),
    ])

    # define components
    c_fb = html.Div(id=f"id-{TAG}-fb", className="text-danger text-center")
    c_button = dbc.Button("Update Information", id=f"id-{TAG}-button", class_name="w-100")

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("Basic Information:", class_name="px-4 py-3"),
        # html.Div("Basic Information:", className="border-bottom px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(c_email, width=12, md=4, class_name=None),
            dbc.Col(c_name, width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(c_phone, width=12, md=4, class_name="mt-2 mt-md-0"),
            # change line
            dbc.Col(c_fb, width=12, md={"size": 4, "order": "last"}, class_name="mt-0 mt-md-4"),
            dbc.Col(c_button, width=12, md=4, class_name="mt-4 mt-md-4"),
        ], align="center", class_name="p-4"),
        dbc.Modal(children=[
            dbc.ModalHeader(dbc.ModalTitle("Update Success"), close_button=False),
            dbc.ModalBody("The basic information was updated successfully"),
        ], id=f"id-{TAG}-modal", backdrop=True, is_open=False),
    ], class_name="mb-4")


@app.callback([
    Output(f"id-{TAG}-fb", "children"),
    Output(f"id-{TAG}-modal", "is_open"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-name", "value"),
    State(f"id-{TAG}-phone", "value"),
], prevent_initial_call=True)
def _button_click(n_clicks, name, phone):
    user = flask_login.current_user

    # check data
    if phone and (not RE_PHONE.match(phone)):
        return "Phone format is error", False

    # check data
    if (name or "") == (user.name or "") and (phone or "") == (user.phone or ""):
        return "No change has happened", False

    # update data
    user.name = name or ""
    user.phone = phone or ""

    # commit data
    app_db.session.merge(user)
    app_db.session.commit()

    # return result
    return None, True
