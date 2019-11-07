# -*- coding: utf-8 -*-
""" Initials template renderer.

Renders the <initials> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END

class InitialsRenderer():
    """ Renders the <initials> tag of the GenCase XML. """

    INITIALS_XML = "/templates/gencase/initials.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        template = get_template_text(cls.INITIALS_XML)
        initials = map(lambda y: template.format(**y["initials"]), filter(lambda x: x["initials"] is not None, data["mkbasedproperties"].values()))
        return LINE_END.join(initials) if initials else ""
