# -*- coding: utf-8 -*-
""" Periodicity template renderer.

Renders the periodicity related tags of the GenCase XML.
"""

from mod.constants import LINE_END

from mod.template_tools import get_template_text


class PeriodicityRenderer():
    """ Renders the periodicity related tags of the GenCase XML. """

    PERIODICTY_BASE_XML = "/templates/gencase/periodicity/base.xml"
    XINCY_XML = "/templates/gencase/periodicity/x_inc_y.xml"
    XINCZ_XML = "/templates/gencase/periodicity/x_inc_z.xml"
    YINCX_XML = "/templates/gencase/periodicity/y_inc_x.xml"
    YINCZ_XML = "/templates/gencase/periodicity/y_inc_z.xml"
    ZINCX_XML = "/templates/gencase/periodicity/z_inc_x.xml"
    ZINCY_XML = "/templates/gencase/periodicity/z_inc_y.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        periodicity_fragments: list = list()
        mode_3d: bool = data["mode3d"] == "true"

        if data["periodicity"]["x_periodicity"]["enabled"].lower() == "true":
            periodicity_fragments.append(get_template_text(cls.XINCY_XML).format(value=data["periodicity"]["x_periodicity"]["y_increment"]) if mode_3d else "")
            periodicity_fragments.append(get_template_text(cls.XINCZ_XML).format(value=data["periodicity"]["x_periodicity"]["z_increment"]))

        if mode_3d and data["periodicity"]["y_periodicity"]["enabled"].lower() == "true":
            periodicity_fragments.append(get_template_text(cls.YINCX_XML).format(value=data["periodicity"]["y_periodicity"]["x_increment"]))
            periodicity_fragments.append(get_template_text(cls.YINCZ_XML).format(value=data["periodicity"]["y_periodicity"]["z_increment"]))

        if data["periodicity"]["z_periodicity"]["enabled"].lower() == "true":
            periodicity_fragments.append(get_template_text(cls.ZINCX_XML).format(value=data["periodicity"]["z_periodicity"]["x_increment"]))
            periodicity_fragments.append(get_template_text(cls.ZINCY_XML).format(value=data["periodicity"]["z_periodicity"]["y_increment"]) if mode_3d else "")

        return LINE_END.join(periodicity_fragments)
