#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet zone info. """

from mod.dataobjects.inletoutlet.inlet_outlet_zone_circle_generator import InletOutletZoneCircleGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_box_generator import InletOutletZoneBoxGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_line_generator import InletOutletZoneLineGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_mk_generator import InletOutletZoneMKGenerator
from mod.enums import InletOutletZoneGeneratorType, InletOutletZoneType


class InletOutletZoneInfo():
    """ Stores Inlet/Outlet zone information and parameters. """

    def __init__(self):
        self.zone_type: InletOutletZoneType = InletOutletZoneType.ZONE_2D
        self.zone_generator_type: InletOutletZoneGeneratorType = InletOutletZoneGeneratorType.MK
        self.zone_mk_generator: InletOutletZoneMKGenerator = InletOutletZoneMKGenerator()
        self.zone_line_generator: InletOutletZoneLineGenerator = InletOutletZoneLineGenerator()
        self.zone_box_generator: InletOutletZoneBoxGenerator = InletOutletZoneBoxGenerator()
        self.zone_circle_generator: InletOutletZoneCircleGenerator = InletOutletZoneCircleGenerator()
