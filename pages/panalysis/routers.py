# _*_ coding: utf-8 _*_

"""
routers of page
"""

ROUTER_MENU = [{
    "component": "Item",
    "props": {"key": "Echarts", "title": "Echarts", "icon": "antd-alert"},
}, {
    "component": "Item",
    "props": {"key": "Files", "title": "Files", "icon": "antd-calendar"},
}, {
    "component": "Item",
    "props": {"key": "Tables", "title": "Tables", "icon": "antd-dollar"},
}, {
    "component": "Item",
    "props": {"key": "Contact", "title": "Contact", "icon": "antd-mail"},
}, {
    "component": "SubMenu",
    "props": {"key": "Home", "title": "Home", "icon": "antd-home"},
    "children": [{
        "component": "Item",
        "props": {"key": "HM-Overview", "title": "Overview"},
    }, {
        "component": "Item",
        "props": {"key": "HM-Updates", "title": "Updates"},
    }, {
        "component": "Item",
        "props": {"key": "HM-Reports", "title": "Reports"},
    }]
}, {
    "component": "SubMenu",
    "props": {"key": "Dashboard", "title": "Dashboard", "icon": "antd-dashboard"},
    "children": [{
        "component": "Item",
        "props": {"key": "DB-Overview", "title": "Overview"},
    }, {
        "component": "Item",
        "props": {"key": "DB-Weekly", "title": "Weekly"},
    }, {
        "component": "Item",
        "props": {"key": "DB-Monthly", "title": "Monthly"},
    }, {
        "component": "Item",
        "props": {"key": "DB-Yearly", "title": "Yearly"},
    }]
}]
