# -*- coding: utf-8 -*-
""" Moorings template renderer.

Renders the <moorings> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END
from mod.enums import MooringsConfigurationMethod


class MooringsRenderer():
    """ Renders the <moorings> tag of the GenCase XML. """

    MOORINGS_BASE = "/templates/gencase/moorings/base.xml"
    MOORINGS_MOORED_FLOATING = "/templates/gencase/moorings/moored_floatings.xml"
    MOORDYN_EXTERNAL_CONFIG = "/templates/gencase/moorings/moordyn/moordyn_file.xml"
    MOORDYN_EMBEDDED_CONFIG = "/templates/gencase/moorings/moordyn/moordyn_embedded.xml"
    MOORDYN_BODY_COMPACT_TEMPLATE = "/templates/gencase/moorings/moordyn/body/compact.xml"
    MOORDYN_BODY_EXTENDED_TEMPLATE = "/templates/gencase/moorings/moordyn/body/extended.xml"
    MOORDYN_LINE_TEMPLATE = "/templates/gencase/moorings/moordyn/line/base.xml"
    MOORDYN_LINE_EA_TEMPLATE = "/templates/gencase/moorings/moordyn/line/ea.xml"
    MOORDYN_LINE_DIAMETER_TEMPLATE = "/templates/gencase/moorings/moordyn/line/diameter.xml"
    MOORDYN_LINE_MASSDENINAIR_TEMPLATE = "/templates/gencase/moorings/moordyn/line/massdeninair.xml"
    MOORDYN_LINE_BA_TEMPLATE = "/templates/gencase/moorings/moordyn/line/ba.xml"
    MOORDYN_LINE_VESSEL_CONNECTION_TEMPLATE = "/templates/gencase/moorings/moordyn/line/vessel_connection.xml"
    MOORDYN_LINE_FIX_CONNECTION_TEMPLATE = "/templates/gencase/moorings/moordyn/line/fix_connection.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        moorings: dict = data["moorings"]

        if moorings["enabled"] == "false":
            return ""

        each_mooredfloatings_templates: list = list(map(lambda mkbound: get_template_text(cls.MOORINGS_MOORED_FLOATING).format(**{"mkbound": mkbound}), moorings["moored_floatings"]))

        formatter: dict = {
            "savevtk_moorings": moorings["saveoptions"]["savevtk_moorings"],
            "savecsv_points": moorings["saveoptions"]["savecsv_points"],
            "savevtk_points": moorings["saveoptions"]["savevtk_points"],
            "each_mooredfloatings_template": LINE_END.join(each_mooredfloatings_templates),
            "moordyn_template": cls.get_moordyn_embedded_template(data) if moorings["configuration_method"] == MooringsConfigurationMethod.EMBEDDED else get_template_text(cls.MOORDYN_EXTERNAL_CONFIG).format(moorings["moordyn_xml"])
        }

        return get_template_text(cls.MOORINGS_BASE).format(**formatter)

    @classmethod
    def get_moordyn_embedded_template(cls, data: dict) -> str:
        """ Returns the rendered embedded config for a moordyn configuration. """
        moordyn = data["moorings"]["moordyn_configuration"]

        formatter: dict = {
            "endTime": data["execution_parameters"]["timemax"],
            "dtOut": data["execution_parameters"]["timeout"],
            "bodies_template": cls.get_bodies_template(data),
            "lines_template": cls.get_lines_template(data)
        }

        formatter.update(moordyn)

        return get_template_text(cls.MOORDYN_EMBEDDED_CONFIG).format(**formatter)

    @classmethod
    def get_lines_template(cls, data) -> str:
        """ Returns a list of <line> tags for moordyn. """
        each_line_template: list = list()

        for line in data["moorings"]["moordyn_configuration"]["lines"]:
            line.update({
                "vessel1_template": get_template_text(cls.MOORDYN_LINE_VESSEL_CONNECTION_TEMPLATE).format(**line["vessel_connection"]) if line["vessel_connection"] else "",
                "vessel2_template": get_template_text(cls.MOORDYN_LINE_VESSEL_CONNECTION_TEMPLATE).format(**line["vessel2_connection"]) if line["vessel2_connection"] else "",
                "fix_template": get_template_text(cls.MOORDYN_LINE_FIX_CONNECTION_TEMPLATE).format(**line["fix_connection"]) if line["fix_connection"] else "",
                "ea_template": get_template_text(cls.MOORDYN_LINE_EA_TEMPLATE).format(**line) if line["ea"] else "",
                "diameter_template": get_template_text(cls.MOORDYN_LINE_DIAMETER_TEMPLATE).format(**line) if line["diameter"] else "",
                "massDenInAir_template": get_template_text(cls.MOORDYN_LINE_MASSDENINAIR_TEMPLATE).format(**line) if line["massDenInAir"] else "",
                "ba_template": get_template_text(cls.MOORDYN_LINE_BA_TEMPLATE).format(**line) if line["ba"] else "",
            })
            each_line_template.append(get_template_text(cls.MOORDYN_LINE_TEMPLATE).format(**line))

        return LINE_END.join(each_line_template)

    @classmethod
    def get_bodies_template(cls, data) -> str:
        """ Returns a list of <body> tags for moordyn. """
        each_body_template: list = list()

        for body in data["moorings"]["moordyn_configuration"]["bodies"]:
            each_body_template.append(get_template_text(cls.MOORDYN_BODY_COMPACT_TEMPLATE if body["depth"] == "false" else cls.MOORDYN_BODY_EXTENDED_TEMPLATE).format(**body))

        return LINE_END.join(each_body_template)
