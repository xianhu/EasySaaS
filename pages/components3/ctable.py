# _*_ coding: utf-8 _*_

"""
table component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(
        pathname, search, tid, data, hd_names, row_keys, title_key=None, out_key=None,
        td_class="text-center p-1", th_class="text-center p-1 font-weight-bolder",
):
    """
    layout of component
    """
    # 创建表头，ID为tid-hd，带有两个数据属性：data-now和data-pre
    hd_list = [html.Th(name, className=th_class) for name in hd_names]
    thead = html.Thead(html.Tr(hd_list), id=tid + "-hd", **{"data-now": "-1", "data-pre": "-1"})

    # 创建行列表
    tr_list = []
    for index, item_info in enumerate(data or []):
        # 构建行ID，当selectable为True时，注意不同的ID形式
        tr_id = {"type": tid + "-row", "index": index}

        # 构建行的标题
        tr_title = item_info.get(title_key, None)

        # 构建行传递的数据，默认为index行号
        tr_odata = {"data-out": item_info.get(out_key, index)}

        # 构建单元格的值和样式，值和样式之间用$$进行分隔
        td_data_temp = [str(item_info[key]).split("$$") for key in row_keys]
        td_value_list = [data[0] if len(data) >= 1 else "" for data in td_data_temp]

        # 构建单元格的样式，值和样式之间用$$进行分隔
        td_class_list = [data[1] if len(data) >= 2 else "" for data in td_data_temp]
        td_class_list = [" ".join([td_class, _class]) for _class in td_class_list]

        # 创建单元格列表及tr组件
        td_list = [html.Td(td_value_list[i], className=td_class_list[i]) for i in range(len(row_keys))]
        tr_list.append(html.Tr(td_list, id=tr_id, title=tr_title, **tr_odata, className=""))

    # 考虑数据为空
    if not tr_list:
        tr_list.append(html.Tr(html.Td("暂无数据", colSpan=len(row_keys), className=td_class)))

    # 返回创建的表格，包含thead和tbody
    return dbc.Table(children=[thead, html.Tbody(tr_list)], id=tid, bordered=True, hover=True, striped=True)
