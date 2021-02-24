#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet zone info. """

from mod.dataobjects.inletoutlet.inlet_outlet_zone_mk_generator import InletOutletZoneMKGenerator
from mod.enums import InletOutletZoneGeneratorType, InletOutletZoneType


class InletOutletZoneInfo():
    """ Stores Inlet/Outlet zone information and parameters. """

    def __init__(self):
        self.zone_type: InletOutletZoneType = InletOutletZoneType.ZONE_2D
        self.zone_generator_type: InletOutletZoneGeneratorType = InletOutletZoneGeneratorType.MK
        self.zone_generator: InletOutletZoneMKGenerator = InletOutletZoneMKGenerator()
