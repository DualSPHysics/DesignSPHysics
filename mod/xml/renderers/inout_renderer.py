# -*- coding: utf-8 -*-
""" Inout template renderer.

Renders the <inout> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END


class InoutRenderer():
    """ Renders the <inout> tag of the GenCase XML. """

    INOUT_BASE = "/templates/gencase/inout/base.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if not data["inlet_outlet"]["zones"]:
            return ""

        inout_zone_template_list: list = list()

        for zone in data["inlet_outlet"]["zones"]:
            # TODO: Finish this when Inout config works
            pass

        formatter: dict = data["inlet_outlet"]
        formatter["each_zone"] = LINE_END.join(inout_zone_template_list)

        return get_template_text(cls.INOUT_BASE).format(**formatter)
