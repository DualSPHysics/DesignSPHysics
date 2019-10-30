# -*- coding: utf-8 -*-
""" SimulationDomain template renderer.

Renders the <simulationdomain> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

class SimulationDomainRenderer():
    """ Renders the <simulationdomain> tag of the GenCase XML. """

    SIMULATIONDOMAIN_XML = "/templates/gencase/simulationdomain.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if data["domain"]["enabled"].lower() == "false":
            return ""
        template = get_template_text(cls.SIMULATIONDOMAIN_XML)
        formatter = {}
        for key in ["posmin_x", "posmin_y", "posmin_z", "posmax_x", "posmax_y", "posmax_z"]:
            value = data["domain"][key]["value"]
            symbol = "+" if value >= 0 else "-"
            modes = {
                0: "default",
                1: str(value),
                2: "default{}{}".format(symbol, str(abs(value))),
                3: "default{}{}%".format(symbol, str(abs(value)))
            }
            formatter[key] = modes[data["domain"][key]["type"]]
        return template.format(**formatter)
