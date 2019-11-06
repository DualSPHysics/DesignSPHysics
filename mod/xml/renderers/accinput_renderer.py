# -*- coding: utf-8 -*-
""" Accinput template renderer.

Renders the <accinput> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END


class AccinputRenderer():
    """ Renders the <accinput> tag of the GenCase XML. """

    ACCINPUT_BASE = "/templates/gencase/accinput/base.xml"
    ACCINPUT_EACH = "/templates/gencase/accinput/each.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if data["acceleration_input"]["enabled"] == "false":
            return ""

        accinput_template_list: list = list()

        for accinput in data["acceleration_input"]["acclist"]:
            accinput["globalgravity_int"] = 1 if accinput["globalgravity"] else 0
            accinput_template_list.append(get_template_text(cls.ACCINPUT_EACH).format(**accinput))

        formatter: dict = {
            "each": LINE_END.join(accinput_template_list)
        }

        return get_template_text(cls.ACCINPUT_BASE).format(**formatter)
