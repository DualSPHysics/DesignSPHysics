# -*- coding: utf-8 -*-
""" Inout template renderer.

Renders the <chrono> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text


class ChronoRenderer():
    """ Renders the <chrono> tag of the GenCase XML. """

    CHRONO_BASE = "/templates/gencase/chrono/base.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if not data["chrono"]["objects"]:
            return ""

        formatter: dict = data["chrono"]

        return get_template_text(cls.CHRONO_BASE).format(**formatter)
