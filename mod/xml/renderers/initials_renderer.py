# -*- coding: utf-8 -*-
""" Initials template renderer.

Renders the <initials> tag of the GenCase XML.
"""

from mod.constants import LINE_END
from mod.enums import BoundNormalsType
from mod.enums import InitialsType
from mod.tools.template_tools import get_template_text


class InitialsRenderer():
    """ Renders the <initials> tag of the GenCase XML. """

    BASE_XML = "/templates/gencase/initials/base.xml"
    UNIFORM_XML = "/templates/gencase/initials/uniform.xml"
    LINEAR_XML = "/templates/gencase/initials/linear.xml"
    PARABOLIC_XML = "/templates/gencase/initials/parabolic.xml"



    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """

        suitable_mkbasedproperties = filter(lambda x: x["initials"] is not None , data["mkbasedproperties"].values())

        if not suitable_mkbasedproperties:
            return ""

        initials_templates = list()
        for mkbasedproperty in suitable_mkbasedproperties:
            initials = mkbasedproperty["initials"]
            if initials is not None:
                if initials["initials_type"] == InitialsType.UNIFORM:
                    initials_templates.append(get_template_text(cls.UNIFORM_XML).format(**initials))
                elif initials["initials_type"] == InitialsType.LINEAR:
                    initials_templates.append(get_template_text(cls.LINEAR_XML).format(**initials))
                elif initials["initials_type"] == InitialsType.PARABOLIC:
                    initials_templates.append(get_template_text(cls.PARABOLIC_XML).format(**initials))



        return get_template_text(cls.BASE_XML).format(initials_each=LINE_END.join(initials_templates))
