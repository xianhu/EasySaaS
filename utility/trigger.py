# _*_ coding: utf-8 _*_

"""
trigger functions
"""

import json


def get_trigger_property(triggered):
    """
    parse dash.callback_context.triggered
    Basic: [{'prop_id': '_id._property', 'value': value}, ...]
    Pattern: [{'prop_id': '{"type":_id,"index":_id_index}._property', 'value': value}, ...]
    AIO: [{'prop_id': '{"aio_id":_id,"subcomponent":_id_index}._property', 'value': value}, ...]
    :return _id, _id_index, _property, value
    """
    if not triggered:
        return None, None, None, None

    # find trigger
    trigger = triggered[0]
    for trigger in triggered:
        if trigger["value"] is not None:
            break

    # parse trigger: {'prop_id': xx, 'value': xx}
    prop_id, value = trigger["prop_id"], trigger["value"]

    # parse prop_id: component_id._property
    frags = [item.strip() for item in prop_id.split(".")]
    component_id, _property = ".".join(frags[:-1]), frags[-1]
    if (not component_id) or (not _property):
        return None, None, None, None

    # parse component_id: _id/_id_index
    _id, _id_index = component_id, None
    if component_id.startswith("{") and component_id.endswith("}"):
        _dict = json.loads(component_id)
        # type/index OR aio_id/subcomponent
        _id = _dict.get("type", _dict.get("aio_id"))
        _id_index = _dict.get("index", _dict.get("subcomponent"))

    # return result
    return _id, _id_index, _property, value
