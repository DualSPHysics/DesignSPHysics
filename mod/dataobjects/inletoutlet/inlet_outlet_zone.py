#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet zone. """

from uuid import UUID, uuid4

from mod.enums import InletOutletRefillingMode, InletOutletInputTreatment, InletOutletZoneType, \
    InletOutletZoneGeneratorType
from mod.tools.stdout_tools import debug

from mod.dataobjects.inletoutlet.inlet_outlet_zone_info import InletOutletZoneInfo
from mod.dataobjects.inletoutlet.inlet_outlet_velocity_info import InletOutletVelocityInfo
from mod.dataobjects.inletoutlet.inlet_outlet_density_info import InletOutletDensityInfo
from mod.dataobjects.inletoutlet.inlet_outlet_elevation_info import InletOutletElevationInfo


class InletOutletZone:
    """ Inlet/Outlet Zone definition. """

    def __init__(self,io_zone_type:InletOutletZoneGeneratorType):
        self.id: UUID = uuid4()
        self.refilling: InletOutletRefillingMode = InletOutletRefillingMode.SIMPLE_FULL
        self.inputtreatment: InletOutletInputTreatment = InletOutletInputTreatment.NO_CHANGES
        self.layers: int = 1
        self.zone_info: InletOutletZoneInfo = InletOutletZoneInfo(io_zone_type)
        self.velocity_info: InletOutletVelocityInfo = InletOutletVelocityInfo()
        self.density_info: InletOutletDensityInfo = InletOutletDensityInfo()
        self.elevation_info: InletOutletElevationInfo = InletOutletElevationInfo()
        self.fc_object_name:str=""

