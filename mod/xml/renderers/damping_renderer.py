# -*- coding: utf-8 -*-
""" Damping template renderer.

Renders the <damping> tag of the GenCase XML.
"""

import FreeCAD

from mod.constants import DIVIDER, LINE_END
from mod.enums import DampingType
from mod.tools.template_tools import get_template_text


class DampingRenderer():
    """ Renders the <damping> tag of the GenCase XML. """

    DAMPING_BASE = "/templates/gencase/damping/base.xml"
    DAMPING_ZONE_EACH = "/templates/gencase/damping/zone_each.xml"
    DAMPING_BOX_EACH = "/templates/gencase/damping/box_each.xml"
    DAMPING_CYLINDER_EACH = "/templates/gencase/damping/cylinder_each.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        each_damping_template: list = []

        for obj_name, dzone in data["damping_zones"].items():
            if dzone["damping_type"]==DampingType.ZONE:
                line = FreeCAD.ActiveDocument.getObject(obj_name).OutList[0]
                dzone.update({
                    "limitmin": [
                        line.Placement.Base.x / DIVIDER,
                        line.Placement.Base.y / DIVIDER,
                        line.Placement.Base.z / DIVIDER
                    ],
                    "limitmax": [
                        (line.Placement.Base.x+line.X2.Value) / DIVIDER,
                        (line.Placement.Base.y+line.Y2.Value) / DIVIDER,
                        (line.Placement.Base.y+line.Z2.Value) / DIVIDER/ DIVIDER
                    ]
                })
                each_damping_template.append(get_template_text(cls.DAMPING_ZONE_EACH).format(**dzone))
            elif dzone["damping_type"]==DampingType.BOX:
                box1 = FreeCAD.ActiveDocument.getObject(obj_name).OutList[0]
                box2 = FreeCAD.ActiveDocument.getObject(obj_name).OutList[1]
                dzone.update({
                    "limitmin_pointini": [
                        box1.Placement.Base[0] / DIVIDER,
                        box1.Placement.Base[1] / DIVIDER,
                        box1.Placement.Base[2] / DIVIDER
                    ],
                    "limitmin_pointend": [
                        (box1.Placement.Base[0] + box1.Length.Value) / DIVIDER,
                        (box1.Placement.Base[1] + box1.Width.Value) / DIVIDER,
                        (box1.Placement.Base[2] + box1.Height.Value) / DIVIDER
                    ],
                    "limitmax_pointini": [
                        box2.Placement.Base[0] / DIVIDER,
                        box2.Placement.Base[1] / DIVIDER,
                        box2.Placement.Base[2] / DIVIDER
                    ],
                    "limitmax_pointend": [
                        (box2.Placement.Base[0] + box2.Length.Value) / DIVIDER,
                        (box2.Placement.Base[1] + box2.Width.Value) / DIVIDER,
                        (box2.Placement.Base[2] + box2.Height.Value) / DIVIDER
                    ],
                    "directions" : dzone["damping_directions"]["face_print"].replace('|',',')

                })
                each_damping_template.append(get_template_text(cls.DAMPING_BOX_EACH).format(**dzone))
            elif dzone["damping_type"] == DampingType.CYLINDER:
                line = FreeCAD.ActiveDocument.getObject(obj_name).OutList[0]
                circle_min = FreeCAD.ActiveDocument.getObject(obj_name).OutList[1]
                circle_max = FreeCAD.ActiveDocument.getObject(obj_name).OutList[2]
                dzone.update({
                    "point1" : [
                        line.X1.Value / DIVIDER,
                        line.Y1.Value / DIVIDER,
                        line.Z1.Value / DIVIDER
                    ],
                    "point2": [
                        line.X2.Value / DIVIDER,
                        line.Y2.Value / DIVIDER,
                        line.Z2.Value / DIVIDER
                    ],
                    "limitmin": circle_min.Radius.Value / DIVIDER
                    ,
                    "limitmax": circle_max.Radius.Value / DIVIDER
                })
                each_damping_template.append(get_template_text(cls.DAMPING_CYLINDER_EACH).format(**dzone))

        formatter = {
            "each": LINE_END.join(each_damping_template)
        }

        return get_template_text(cls.DAMPING_BASE).format(**formatter)
