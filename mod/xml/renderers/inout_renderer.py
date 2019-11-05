# -*- coding: utf-8 -*-
""" Inout template renderer.

Renders the <inout> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END
from mod.enums import InletOutletZoneType, InletOutletVelocityType, InletOutletElevationType


class InoutRenderer():
    """ Renders the <inout> tag of the GenCase XML. """

    INOUT_BASE = "/templates/gencase/inout/base.xml"
    INOUT_EACH = "/templates/gencase/inout/each_zone.xml"
    INOUT_ZONE2D = "/templates/gencase/inout/zone2d.xml"
    INOUT_ZONE3D = "/templates/gencase/inout/zone3d.xml"
    INOUT_IMPOSEVELOCITY_PARAM = "/templates/gencase/inout/imposevelocity_param.xml"
    INOUT_ZSURF_PARAM = "/templates/gencase/inout/zsurf_param.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if not data["inlet_outlet"]["zones"]:
            return ""

        inout_zone_template_list: list = list()

        for zone in data["inlet_outlet"]["zones"]:
            each_formatter = zone
            each_formatter["zone"] = cls.get_zone_template(zone)
            each_formatter["imposevelocity_param"] = cls.get_imposevelocity_param_template(zone)
            each_formatter["zsurf_param"] = cls.get_zsurf_param_template(zone)
            inout_zone_template_list.append(get_template_text(cls.INOUT_EACH).format(**each_formatter))

        formatter: dict = data["inlet_outlet"]
        formatter["each_zone"] = LINE_END.join(inout_zone_template_list)

        return get_template_text(cls.INOUT_BASE).format(**formatter)

    @classmethod
    def get_zone_template(cls, zone: dict) -> str:
        """ Returns the zone2d/3d inner template. """
        if zone["zone_info"]["zone_type"] == InletOutletZoneType.ZONE_2D:
            return get_template_text(cls.INOUT_ZONE2D).format(**zone["zone_info"])
        return get_template_text(cls.INOUT_ZONE3D).format(**zone["zone_info"])

    @classmethod
    def get_imposevelocity_param_template(cls, zone: dict) -> str:
        """ Returns the imposevelocity inner template. """
        if zone["velocity_info"]["velocity_type"] == InletOutletVelocityType.FIXED:
            return get_template_text(cls.INOUT_IMPOSEVELOCITY_PARAM).format(**zone["velocity_info"])
        return ""

    @classmethod
    def get_zsurf_param_template(cls, zone: dict) -> str:
        """ Returns the imposezsurf inner template. """
        if zone["elevation_info"]["elevation_type"] == InletOutletElevationType.FIXED or zone["elevation_info"]["elevation_type"] == InletOutletElevationType.AUTOMATIC:
            return get_template_text(cls.INOUT_ZSURF_PARAM).format(**zone["elevation_info"])
        return ""
