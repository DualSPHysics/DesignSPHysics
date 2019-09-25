#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

''' Translation related tools. '''

from os import path
import json

import FreeCADGui


def __(text):
    ''' Translation helper. Takes a string and tries to return its translation to the current FreeCAD locale.
    If the translation is missing or the file does not exists, return default english string. '''
    # Get FreeCAD current language
    freecad_locale = FreeCADGui.getLocale().lower().replace(", ", "-").replace(" ", "-")

    # Find mod directory
    utils_dir = path.dirname(path.abspath(__file__))

    # Open translation file and print the matching string, if it's defined.
    filename = "{utils_dir}/lang/{locale}.json".format(utils_dir=utils_dir, locale=freecad_locale)

    if not path.isfile(filename):
        filename = "{utils_dir}/lang/{locale}.json".format(utils_dir=utils_dir, locale="english")

    with open(filename, "rb") as f:
        translation = json.load(f)

    # Tries to return the translation. It it does not exist, creates it
    to_ret = translation.get(text, None)

    if not to_ret:
        translation[text] = text
        with open(filename, "w", encoding="utf8") as f:
            json.dump(translation, f, indent=4)
        return text
    return to_ret
