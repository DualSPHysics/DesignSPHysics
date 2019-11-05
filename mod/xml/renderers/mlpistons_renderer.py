# -*- coding: utf-8 -*-
""" MLPistons template renderer.

Renders the <mlayerpistons> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.enums import MLPistonType
from mod.constants import LINE_END

class MLPistonsRenderer():
    """ Renders the <mlayerpistons> tag of the GenCase XML. """

    MLPISTONS_BASE = "/templates/gencase/mlpistons/base.xml"
    MLPISTONS_EACH_1D = "/templates/gencase/mlpistons/each_1d.xml"
    MLPISTONS_EACH_2D = "/templates/gencase/mlpistons/each_2d.xml"
    MLPISTONS_EACH_2D_VELDATA = "/templates/gencase/mlpistons/each_veldata.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        ml_pistons: dict = dict()
        for mk, mk_prop in data["mkbasedproperties"].items():
            if mk_prop["mlayerpiston"]:
                ml_pistons[mk] = mk_prop["mlayerpiston"]

        if not ml_pistons.values():
            return ""

        each_mlpiston_template: list = list()
        for mk, mlpiston in ml_pistons.items():
            if mlpiston["type"] == MLPistonType.MLPISTON1D:
                mlpiston.update({"mk": mk})
                each_mlpiston_template.append(get_template_text(cls.MLPISTONS_EACH_1D).format(**mlpiston))
            elif mlpiston["type"] == MLPistonType.MLPISTON2D:
                each_veldata_templates: list = list()
                for veldata in mlpiston["veldata"]:
                    each_veldata_templates.append(get_template_text(cls.MLPISTONS_EACH_2D_VELDATA).format(**veldata))
                mlpiston.update({
                    "mk": mk,
                    "each_veldata": LINE_END.join(each_veldata_templates)
                })
                each_mlpiston_template.append(get_template_text(cls.MLPISTONS_EACH_2D).format(**mlpiston))

        formatter = {
            "each": LINE_END.join(each_mlpiston_template)
        }

        return get_template_text(cls.MLPISTONS_BASE).format(**formatter)
