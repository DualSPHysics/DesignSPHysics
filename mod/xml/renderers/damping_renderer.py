# -*- coding: utf-8 -*-
""" Damping template renderer.

Renders the <damping> tag of the GenCase XML.
"""

import FreeCAD

from mod.template_tools import get_template_text

from mod.constants import DIVIDER, LINE_END


class DampingRenderer():
    """ Renders the <damping> tag of the GenCase XML. """

    DAMPING_BASE = "/templates/gencase/damping/base.xml"
    DAMPING_EACH = "/templates/gencase/damping/each.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        each_damping_template: list = []

        for obj_name, dzone in data["damping_zones"].items():
            fc_object = FreeCAD.ActiveDocument.getObject(obj_name)
            dzone.update({
                "limitmin": [
                    fc_object.OutList[0].Start[0] / DIVIDER,
                    fc_object.OutList[0].Start[1] / DIVIDER,
                    fc_object.OutList[0].Start[2] / DIVIDER
                ],
                "limitmax": [
                    str(fc_object.OutList[0].End[0] / DIVIDER),
                    str(fc_object.OutList[0].End[1] / DIVIDER),
                    str(fc_object.OutList[0].End[2] / DIVIDER)
                ]
            })
            each_damping_template.append(get_template_text(cls.DAMPING_EACH).format(**dzone))

        formatter = {
            "each": LINE_END.join(each_damping_template)
        }

        return get_template_text(cls.DAMPING_BASE).format(**formatter)
