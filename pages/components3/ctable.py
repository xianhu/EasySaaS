# _*_ coding: utf-8 _*_

"""
table component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(
        pathname, search,
        tid, data, header_list, key_list,
        title_key=None, out_key=None,
        th_class=None, td_class=None, data_class=None,
        bordered=True, borderless=True, hover=True, striped=True, class_name=None,
):
    """
    layout of component
    """
    # define class
    th_class = th_class or "text-center p-1"
    td_class = td_class or "text-center p-1"

    # define thead
    th_list = [html.Th(name, className=th_class) for name in header_list]
    thead = html.Thead(html.Tr(th_list), id=tid + "-head", className=None)

    # define tr
    tr_list = []
    for index, item_info in enumerate(data or []):
        # define title and out's data
        tr_index = item_info.get(out_key, index)
        tr_title = str(item_info.get(title_key, ""))

        # define class list
        class_info = data_class[index] if data_class else {}
        class_list = [class_info.get(key, "") for key in key_list]
        class_list = [" ".join([td_class, _class]) for _class in class_list]

        # define value list and td list
        value_list = [item_info[key] for key in key_list]
        td_list = [html.Td(v, className=c) for (v, c) in zip(value_list, class_list)]

        # define tr_list
        tr_id = {"type": tid + "-row", "index": tr_index}
        tr_list.append(html.Tr(td_list, id=tr_id, title=tr_title, className=None))

    # return result
    args = {"bordered": bordered, "borderless": borderless, "hover": hover, "striped": striped}
    return dbc.Table(children=[thead, html.Tbody(tr_list)], id=tid, **args, class_name=class_name)
