#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

""" Template loading and formatting related tools. """

from os import path


def get_template_text(template_path) -> str:
    """ Returns the text for a given template. """
    template_data = ""
    mod_folder = path.dirname(path.realpath(__file__))

    with open("{}{}".format(mod_folder, template_path), "r", encoding="utf-8") as template:
        template_data = template.read()
    return template_data


def obj_to_dict(obj, classkey=None):
    """ Converts an object to dictionary recursively. """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = obj_to_dict(v, classkey)
        return data
    if hasattr(obj, "_ast"):
        return obj_to_dict(obj._ast())  # pylint: disable=protected-access
    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [obj_to_dict(v, classkey) for v in obj]
    if hasattr(obj, "__dict__"):
        data = {key: obj_to_dict(value, classkey) for key, value in obj.__dict__.items() if not callable(value) and not key.startswith("_")}
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    return obj
