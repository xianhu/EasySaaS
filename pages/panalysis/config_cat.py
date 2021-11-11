# _*_ coding: utf-8 _*_

"""
catalog config of page
"""

from ..paths import PATH_ANALYSIS

_a1 = ["NAVIGATION", [
    ["Dashboards", {
        "icon": "bi bi-house-door",
        "href": None,
        "items": [
            ("Analytics", f"{PATH_ANALYSIS}-db-analytics"),
            ("CustomRM", f"{PATH_ANALYSIS}-db-cumtomrm"),
            ("Ecommerce", f"{PATH_ANALYSIS}-db-ecommerce"),
            ("Projects", f"{PATH_ANALYSIS}-db-projects"),
        ],
    }],
]]

_a2 = ["APPLICATIONS", [
    ["Calendar", {
        "icon": "bi bi-calendar-date",
        "href": f"{PATH_ANALYSIS}-calendar",
        "items": [],
    }],
    ["Chat", {
        "icon": "bi bi-chat-dots",
        "href": f"{PATH_ANALYSIS}-chat",
        "items": [],
    }],
    ["Ecommerce", {
        "icon": "bi bi-coin",
        "href": None,
        "items": [
            ("Products", f"{PATH_ANALYSIS}-ec-products"),
            ("Products Details", f"{PATH_ANALYSIS}-ec-prodetails"),
            ("Order", f"{PATH_ANALYSIS}-ec-order"),
            ("Order Details", f"{PATH_ANALYSIS}-ec-orddetails"),
            ("Customers", f"{PATH_ANALYSIS}-ec-customers"),
            ("Shopping Cart", f"{PATH_ANALYSIS}-ec-shopcart"),
            ("Checkout", f"{PATH_ANALYSIS}-ec-checkout"),
            ("Sellers", f"{PATH_ANALYSIS}-ec-sellers"),
        ],
    }],
    ["Email", {
        "icon": "bi bi-envelope",
        "href": None,
        "items": [
            ("Inbox", f"{PATH_ANALYSIS}-em-inbox"),
            ("Read Email", f"{PATH_ANALYSIS}-em-read"),
        ],
    }],
    ["Project", {
        "icon": "bi bi-cast",
        "href": None,
        "items": [
            ("List", f"{PATH_ANALYSIS}-pj-list"),
            ("Details", f"{PATH_ANALYSIS}-pj-details"),
            ("Gantt", f"{PATH_ANALYSIS}-pj-gantt"),
            ("Create Project", f"{PATH_ANALYSIS}-pj-create"),
        ],
    }],
    ["Social Feed", {
        "icon": "bi bi-rss",
        "href": f"{PATH_ANALYSIS}-socialfeed",
        "items": [],
    }],
    ["Tasks", {
        "icon": "bi bi-list-task",
        "href": None,
        "items": [
            ("List", f"{PATH_ANALYSIS}-ts-list"),
            ("Details", f"{PATH_ANALYSIS}-ts-details"),
            ("Kanban Board", f"{PATH_ANALYSIS}-ts-board"),
        ],
    }],
    ["File Manager", {
        "icon": "bi bi-folder",
        "href": f"{PATH_ANALYSIS}-filemanager",
        "items": [],
    }],
]]

_a3 = ["CUSTOM", [
    ["Pages", {
        "icon": "bi bi-file-break",
        "href": None,
        "items": [
            ("Profile", f"{PATH_ANALYSIS}-pg-profile"),
            ("Invoice", f"{PATH_ANALYSIS}-pg-invoice"),
            ("Pricing", f"{PATH_ANALYSIS}-pg-pricing"),
            ("Maintenance", f"{PATH_ANALYSIS}-pg-maintenance"),
            ("Starter Page", f"{PATH_ANALYSIS}-pg-starter"),
            ("With Preloader", f"{PATH_ANALYSIS}-pg-preloader"),
            ("Timeline", f"{PATH_ANALYSIS}-pg-timeline"),
        ],
    }],
    ["Landing", {
        "icon": "bi bi-bag-check",
        "href": f"{PATH_ANALYSIS}-landing",
        "items": [],
    }],
    ["Layouts", {
        "icon": "bi bi-columns-gap",
        "href": None,
        "items": [
            ("Horizontal", f"{PATH_ANALYSIS}-ly-horizontal"),
            ("Detached", f"{PATH_ANALYSIS}-ly-detached"),
        ],
    }],
]]

CATALOG_LIST = [_a1, _a2, _a3]
