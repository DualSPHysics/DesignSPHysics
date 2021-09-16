# -*- coding: utf-8 -*-
""" Inout template renderer.

Renders the <inout> tag of the GenCase XML.
"""

from mod.template_tools import get_template_text

from mod.constants import LINE_END
from mod.enums import InletOutletVelocitySpecType, InletOutletZSurfMode, InletOutletZoneGeneratorType, InletOutletZoneType, InletOutletVelocityType, InletOutletElevationType


class InoutRenderer():
    """ Renders the <inout> tag of the GenCase XML. """

    INOUT_BASE = "/templates/gencase/inout/base.xml"
    INOUT_USEBOXLIMITWITHFREECENTRE = "/templates/gencase/inout/useboxlimit/withfreecentre.xml"
    INOUT_USEBOXLIMITWITHOUTFREECENTRE = "/templates/gencase/inout/useboxlimit/withoutfreecentre.xml"
    INOUT_EACH = "/templates/gencase/inout/each_zone.xml"
    INOUT_ZONE2D = "/templates/gencase/inout/zoneinfo/zone2d.xml"
    INOUT_ZONE3D = "/templates/gencase/inout/zoneinfo/zone3d.xml"
    INOUT_ZONE_GENERATOR_MK = "/templates/gencase/inout/zoneinfo/generator_mk.xml"
    INOUT_ZONE_GENERATOR_LINE = "/templates/gencase/inout/zoneinfo/generator_line.xml"
    INOUT_ZONE_GENERATOR_LINE_ROTATION = "/templates/gencase/inout/zoneinfo/generator_line_rotation.xml"
    INOUT_ZONE_GENERATOR_BOX = "/templates/gencase/inout/zoneinfo/generator_box.xml"
    INOUT_ZONE_GENERATOR_BOX_ROTATION = "/templates/gencase/inout/zoneinfo/generator_box_rotation.xml"
    INOUT_ZONE_GENERATOR_CIRCLE = "/templates/gencase/inout/zoneinfo/generator_circle.xml"
    INOUT_IMPOSEVELOCITY_FIXED_CONSTANT = "/templates/gencase/inout/imposevelocity/fixed_constant.xml"
    INOUT_IMPOSEVELOCITY_FIXED_LINEAR = "/templates/gencase/inout/imposevelocity/fixed_linear.xml"
    INOUT_IMPOSEVELOCITY_FIXED_PARABOLIC = "/templates/gencase/inout/imposevelocity/fixed_parabolic.xml"
    INOUT_IMPOSEVELOCITY_VARIABLE_UNIFORM = "/templates/gencase/inout/imposevelocity/variable_uniform.xml"
    INOUT_IMPOSEVELOCITY_VARIABLE_UNIFORM_EACH = "/templates/gencase/inout/imposevelocity/variable_uniform_each.xml"
    INOUT_IMPOSEVELOCITY_VARIABLE_LINEAR = "/templates/gencase/inout/imposevelocity/variable_linear.xml"
    INOUT_IMPOSEVELOCITY_VARIABLE_LINEAR_EACH = "/templates/gencase/inout/imposevelocity/variable_linear_each.xml"
    INOUT_IMPOSEVELOCITY_VARIABLE_PARABOLIC = "/templates/gencase/inout/imposevelocity/variable_parabolic.xml"
    INOUT_IMPOSEVELOCITY_VARIABLE_PARABOLIC_EACH = "/templates/gencase/inout/imposevelocity/variable_parabolic_each.xml"
    INOUT_IMPOSEVELOCITY_FILE_UNIFORM = "/templates/gencase/inout/imposevelocity/file_uniform.xml"
    INOUT_IMPOSEVELOCITY_FILE_LINEAR = "/templates/gencase/inout/imposevelocity/file_linear.xml"
    INOUT_IMPOSEVELOCITY_FILE_PARABOLIC = "/templates/gencase/inout/imposevelocity/file_parabolic.xml"
    INOUT_ZSURF = "/templates/gencase/inout/zsurf/base.xml"
    INOUT_ZSURF_FIXED = "/templates/gencase/inout/zsurf/zsurf_fixed.xml"
    INOUT_ZSURF_TIMELIST = "/templates/gencase/inout/zsurf/zsurf_timelist.xml"
    INOUT_ZSURF_TIMELIST_TIMEVALUE_EACH = "/templates/gencase/inout/zsurf/zsurf_timelist_timevalue_each.xml"
    INOUT_ZSURF_FILE = "/templates/gencase/inout/zsurf/zsurf_file.xml"
    INOUT_ZSURF_AUTOMATIC = "/templates/gencase/inout/zsurf/zsurf_automatic.xml"

    @classmethod
    def render(cls, data):
        """ Returns the rendered string. """
        if not data["inlet_outlet"]["zones"]:
            return ""

        inout_zone_template_list: list = list()

        for zone in data["inlet_outlet"]["zones"]:
            each_formatter = zone
            each_formatter["zoneinfo"] = cls.get_zone_template(zone)
            each_formatter["imposevelocity_param"] = cls.get_imposevelocity_param_template(zone)
            each_formatter["zsurf_param"] = cls.get_zsurf_param_template(zone)
            inout_zone_template_list.append(get_template_text(cls.INOUT_EACH).format(**each_formatter))

        formatter: dict = data["inlet_outlet"]
        # 16/09/2021 Remove useboxlimit from the XML as Alex stated
        # formatter["useboxlimit_template"] = cls.get_useboxlimit_template(data["inlet_outlet"])
        formatter["useboxlimit_template"] = ""
        formatter["each_zone"] = LINE_END.join(inout_zone_template_list)

        return get_template_text(cls.INOUT_BASE).format(**formatter)

    @classmethod
    def get_useboxlimit_template(cls, iodata: dict) -> str:
        if iodata["useboxlimit_freecentre_enabled"] == "true":
            return get_template_text(cls.INOUT_USEBOXLIMITWITHFREECENTRE).format(**iodata)
        else:
            return get_template_text(cls.INOUT_USEBOXLIMITWITHOUTFREECENTRE).format(**iodata)

    @classmethod
    def get_zone_template(cls, zone: dict) -> str:
        """ Returns the zone2d/3d inner template. """
        if zone["zone_info"]["zone_type"] == InletOutletZoneType.ZONE_2D:
            zone_template = cls.INOUT_ZONE2D
        else:
            zone_template = cls.INOUT_ZONE3D

        formatter: dict = {}
        if zone["zone_info"]["zone_generator_type"] == InletOutletZoneGeneratorType.MK:
            formatter["generator_template"] = get_template_text(cls.INOUT_ZONE_GENERATOR_MK).format(**zone["zone_info"]["zone_mk_generator"])
        elif zone["zone_info"]["zone_generator_type"] == InletOutletZoneGeneratorType.LINE:
            line_gen_formatter: dict = zone["zone_info"]["zone_line_generator"]
            if zone["zone_info"]["zone_line_generator"]["has_rotation"] == "true":
                line_gen_formatter["generator_line_rotation"] =  get_template_text(cls.INOUT_ZONE_GENERATOR_LINE_ROTATION).format(**zone["zone_info"]["zone_line_generator"])
            else:
                line_gen_formatter["generator_line_rotation"] = ""
            formatter["generator_template"] = get_template_text(cls.INOUT_ZONE_GENERATOR_LINE).format(**line_gen_formatter)
        elif zone["zone_info"]["zone_generator_type"] == InletOutletZoneGeneratorType.BOX:
            box_gen_formatter: dict = zone["zone_info"]["zone_box_generator"]
            if zone["zone_info"]["zone_box_generator"]["rotateaxis_enabled"] == "true":
                box_gen_formatter["generator_box_rotation"] =  get_template_text(cls.INOUT_ZONE_GENERATOR_BOX_ROTATION).format(**zone["zone_info"]["zone_box_generator"])
            else:
                box_gen_formatter["generator_box_rotation"] = ""
            formatter["generator_template"] = get_template_text(cls.INOUT_ZONE_GENERATOR_BOX).format(**box_gen_formatter)
        elif zone["zone_info"]["zone_generator_type"] == InletOutletZoneGeneratorType.CIRCLE:
            formatter["generator_template"] = get_template_text(cls.INOUT_ZONE_GENERATOR_CIRCLE).format(**zone["zone_info"]["zone_circle_generator"])

        return get_template_text(zone_template).format(**formatter)

    @classmethod
    def get_imposevelocity_param_template(cls, zone: dict) -> str:
        """ Returns the imposevelocity inner template. """
        velocity_type = zone["velocity_info"]["velocity_type"]
        if velocity_type == InletOutletVelocityType.EXTRAPOLATED:
            return ""

        if velocity_type == InletOutletVelocityType.INTERPOLATED:
            raise Exception("Inlet/Outlet Velocity type INTERPOLATED is not implemented on the XML renderer")

        spec_type = zone["velocity_info"]["velocity_specification_type"]

        if velocity_type == InletOutletVelocityType.FIXED:
            if spec_type == InletOutletVelocitySpecType.FIXED_CONSTANT:
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_FIXED_CONSTANT).format(zone["velocity_info"]["fixed_constant_value"])
            elif spec_type == InletOutletVelocitySpecType.FIXED_LINEAR:
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_FIXED_LINEAR).format(**zone["velocity_info"]["fixed_linear_value"])
            elif spec_type == InletOutletVelocitySpecType.FIXED_PARABOLIC:
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_FIXED_PARABOLIC).format(**zone["velocity_info"]["fixed_parabolic_value"])
        elif velocity_type == InletOutletVelocityType.VARIABLE:
            if spec_type == InletOutletVelocitySpecType.FILE_UNIFORM:
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_FILE_UNIFORM).format(**zone["velocity_info"])
            elif spec_type == InletOutletVelocitySpecType.FILE_LINEAR:
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_FILE_LINEAR).format(**zone["velocity_info"])
            elif spec_type == InletOutletVelocitySpecType.FILE_PARABOLIC:
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_FILE_PARABOLIC).format(**zone["velocity_info"])
            elif spec_type == InletOutletVelocitySpecType.VARIABLE_UNIFORM:
                each_template = list()
                for each in zone["velocity_info"]["variable_uniform_values"]:
                    each_template.append(get_template_text(cls.INOUT_IMPOSEVELOCITY_VARIABLE_UNIFORM_EACH).format(time=each[0], v=each[1]))
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_VARIABLE_UNIFORM).format(variable_uniform_each=LINE_END.join(each_template))
            elif spec_type == InletOutletVelocitySpecType.VARIABLE_LINEAR:
                each_template = list()
                for each in zone["velocity_info"]["variable_linear_values"]:
                    each_template.append(get_template_text(cls.INOUT_IMPOSEVELOCITY_VARIABLE_LINEAR_EACH).format(time=each[0], **each[1]))
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_VARIABLE_LINEAR).format(variable_linear_each=LINE_END.join(each_template))
            elif spec_type == InletOutletVelocitySpecType.VARIABLE_PARABOLIC:
                each_template = list()
                for each in zone["velocity_info"]["variable_parabolic_values"]:
                    each_template.append(get_template_text(cls.INOUT_IMPOSEVELOCITY_VARIABLE_PARABOLIC_EACH).format(time=each[0], **each[1]))
                return get_template_text(cls.INOUT_IMPOSEVELOCITY_VARIABLE_PARABOLIC).format(variable_parabolic_each=LINE_END.join(each_template))

    @classmethod
    def get_zsurf_param_template(cls, zone: dict) -> str:
        """ Returns the imposezsurf inner template. """

        if zone["elevation_info"]["elevation_type"] == InletOutletElevationType.FIXED:
            return get_template_text(cls.INOUT_ZSURF_FIXED).format(**zone["elevation_info"])
        elif zone["elevation_info"]["elevation_type"] == InletOutletElevationType.VARIABLE and zone["elevation_info"]["zsurf_mode"] == InletOutletZSurfMode.FILE:
            return get_template_text(cls.INOUT_ZSURF_FILE).format(**zone["elevation_info"])
        elif zone["elevation_info"]["elevation_type"] == InletOutletElevationType.VARIABLE and zone["elevation_info"]["zsurf_mode"] == InletOutletZSurfMode.TIMELIST:
            inout_zsurf_timelist_formatter = zone["elevation_info"]
            time_value_each = []
            for zsurftimevalue in zone["elevation_info"]["zsurftimes"]:
                time_value_each.append(get_template_text(cls.INOUT_ZSURF_TIMELIST_TIMEVALUE_EACH).format(zsurftimevalue[0], zsurftimevalue[1]))
            inout_zsurf_timelist_formatter["timevalue_each"] = LINE_END.join(time_value_each)
            return get_template_text(cls.INOUT_ZSURF_TIMELIST).format(**inout_zsurf_timelist_formatter)
        elif zone["elevation_info"]["elevation_type"] == InletOutletElevationType.AUTOMATIC:
            return get_template_text(cls.INOUT_ZSURF_AUTOMATIC).format(**zone["elevation_info"])

        # TEXTO CO INTERIOR DO TAG IMPOSEZSURF
        return ""
