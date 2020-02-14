# -*- coding: utf-8 -*-
""" Definition template renderer.

Renders the <definition> tag of the GenCase XML.
"""

import FreeCAD

from mod.constants import DIVIDER

from mod.template_tools import get_template_text

class DefinitionRenderer():
    """ Renders the <definition> tag of the GenCase XML. """

    DEFINITION_XML = "/templates/gencase/definition.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        template = get_template_text(cls.DEFINITION_XML)
        fc_object = FreeCAD.ActiveDocument.getObject("Case_Limits")
        min_point = fc_object.Placement.Base
        formatter = {
            "dp": data["dp"],
            "pointmin": [min_point.x / DIVIDER, min_point.y / DIVIDER, min_point.z / DIVIDER],
            "pointmax": [
                min_point.x / DIVIDER + fc_object.Length.Value / DIVIDER,
                min_point.y / DIVIDER + fc_object.Width.Value / DIVIDER if data["mode3d"] == "true" else min_point.y / DIVIDER,
                min_point.z / DIVIDER + fc_object.Height.Value / DIVIDER
            ]
        }
        return template.format(**formatter)
