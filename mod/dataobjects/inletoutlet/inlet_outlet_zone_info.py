#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet zone info. """

from mod.dataobjects.inletoutlet.inlet_outlet_zone_circle_generator import InletOutletZoneCircleGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_box_generator import InletOutletZoneBoxGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_direction import InletOutletZone3DDirection, \
    InletOutletZone2DDirection
from mod.dataobjects.inletoutlet.inlet_outlet_zone_line_generator import InletOutletZoneLineGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_mk_generator import InletOutletZoneMKGenerator
from mod.dataobjects.inletoutlet.inlet_outlet_zone_rotation import InletOutletZone3DRotation, InletOutletZone2DRotation
from mod.enums import InletOutletZoneGeneratorType, InletOutletZoneType


class InletOutletZoneInfo:
    """ Stores Inlet/Outlet zone information and parameters. """

    def __init__(self,zone_generator_type: InletOutletZoneGeneratorType = InletOutletZoneGeneratorType.BOX):
        self.zone_generator_type: InletOutletZoneGeneratorType = zone_generator_type
        if self.zone_generator_type <= InletOutletZoneGeneratorType.MK_2D :
            self.zone_type: InletOutletZoneType = InletOutletZoneType.ZONE_2D
            self.zone_direction_2d: InletOutletZone2DDirection = InletOutletZone2DDirection(direction = [1.0,0.0])
            self.zone_rotation_2d: InletOutletZone2DRotation = InletOutletZone2DRotation()
        else:
            self.zone_type: InletOutletZoneType = InletOutletZoneType.ZONE_3D
            self.zone_direction_3d: InletOutletZone3DDirection = InletOutletZone3DDirection(direction=[1.0,0.0,0.0])
            self.zone_rotation_3d: InletOutletZone3DRotation = InletOutletZone3DRotation()

        if self.zone_generator_type == InletOutletZoneGeneratorType.LINE:
            self.zone_line_generator: InletOutletZoneLineGenerator = InletOutletZoneLineGenerator(point=[0.1,0.0,0.1],point2=[0.1,0.0,0.9])
        elif self.zone_generator_type == InletOutletZoneGeneratorType.MK_2D:
            self.zone_mk_generator: InletOutletZoneMKGenerator = InletOutletZoneMKGenerator()
        elif self.zone_generator_type == InletOutletZoneGeneratorType.BOX:
            self.zone_box_generator: InletOutletZoneBoxGenerator = InletOutletZoneBoxGenerator(point=[0.0,0.3,0.3],size=[0,0.4,0.4])
        elif self.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
            self.zone_circle_generator: InletOutletZoneCircleGenerator = InletOutletZoneCircleGenerator(point=[0.0,0.5,0.5],radius=0.2)
        elif self.zone_generator_type == InletOutletZoneGeneratorType.MK_3D:
            self.zone_mk_generator: InletOutletZoneMKGenerator = InletOutletZoneMKGenerator()




