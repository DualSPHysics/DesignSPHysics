# -*- coding: utf-8 -*-
""" RZones template renderer.

Renders the <relaxationzones> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END

class RZonesRenderer():
    """ Renders the <relaxationzones> tag of the GenCase XML. """

    RZONES_XML = "/templates/gencase/rzones/base.xml"
    RZONE_REGULAR_XML = "/templates/gencase/rzones/regular.xml"
    RZONE_IRREGULAR_XML = "/templates/gencase/rzones/irregular.xml"
    RZONE_FILE_XML = "/templates/gencase/rzones/file.xml"
    RZONE_UNIFORM_XML = "/templates/gencase/rzones/uniform.xml"
    RZONE_UNIFORM_VELOCITY_XML = "/templates/gencase/rzones/uniform_velocity.xml"
    RZONE_UNIFORM_VELOCITYTIMES_XML = "/templates/gencase/rzones/uniform_velocitytimes.xml"
    RZONE_UNIFORM_VELOCITYTIMES_EACH_XML = "/templates/gencase/rzones/uniform_velocitytimes_each.xml"

    @classmethod
    def render(cls, data, rz_type: str):
        """ Returns the rendered string. """
        template = get_template_text(cls.RZONES_XML)
        rz_templates = {
            "RelaxationZoneRegular": cls.RZONE_REGULAR_XML,
            "RelaxationZoneIrregular": cls.RZONE_IRREGULAR_XML,
            "RelaxationZoneFile": cls.RZONE_FILE_XML,
            "RelaxationZoneUniform": cls.RZONE_UNIFORM_XML
        }
        rzone_formatter = {}

        if rz_type == "RelaxationZoneUniform":
            if data["relaxation_zone"]["use_velocity"] == "true":
                rzone_formatter["rzuniform_velocity"] = get_template_text(cls.RZONE_UNIFORM_VELOCITY_XML).format(data["relaxation_zone"]["velocity"])
            else:
                rzone_formatter["rzuniform_velocity"] = cls.get_velocity_times_template(data["relaxation_zone"]["velocity_times"])

        rzone_formatter.update(data["relaxation_zone"])
        formatter = {
            "rzone": get_template_text(rz_templates[rz_type]).format(**rzone_formatter)
        }
        return template.format(**formatter)

    @classmethod
    def get_velocity_times_template(cls, times: list) -> str:
        """ Renders the velocity times template for a uniform relaxation zone. """
        timevalues = LINE_END.join(map(lambda tv: get_template_text(cls.RZONE_UNIFORM_VELOCITYTIMES_EACH_XML).format(tv[0], tv[1]), times))
        return get_template_text(cls.RZONE_UNIFORM_VELOCITYTIMES_XML).format(each=timevalues)
