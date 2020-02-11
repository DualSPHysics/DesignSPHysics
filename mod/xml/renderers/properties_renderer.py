# -*- coding: utf-8 -*-
""" Properties template renderer.

Renders the <properties> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END, MKFLUID_LIMIT


class PropertiesRenderer():
    """ Renders the <properties> tag of the GenCase XML. """

    PROPERTIES_BASE = "/templates/gencase/properties/base.xml"
    EACH_LINK_XML = "/templates/gencase/properties/each_link.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        each_link_templates: list = list()

        for mkreal, mkbasedproperty in data["mkbasedproperties"].items():
            if mkbasedproperty["property"]:
                each_formatter: dict = {
                    "mkbound": mkreal - MKFLUID_LIMIT,
                    "property_name": mkbasedproperty["property"]["name"],
                }
                each_link_templates.append(get_template_text(cls.EACH_LINK_XML).format(**each_formatter))

        if not each_link_templates:
            return ""

        if data["execution_parameters"]["rigidalgorithm"] not in (2, 3):
            return ""

        formatter: dict = {
            "each_link": LINE_END.join(each_link_templates)
        }

        return get_template_text(cls.PROPERTIES_BASE).format(**formatter)
