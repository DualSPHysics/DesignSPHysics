#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet zone. """

from uuid import UUID, uuid4

from mod.dataobjects.inletoutlet.inlet_outlet_zone_info import InletOutletZoneInfo
from mod.dataobjects.inletoutlet.inlet_outlet_velocity_info import InletOutletVelocityInfo
from mod.dataobjects.inletoutlet.inlet_outlet_density_info import InletOutletDensityInfo
from mod.dataobjects.inletoutlet.inlet_outlet_elevation_info import InletOutletElevationInfo


class InletOutletZone:
    """ Inlet/Outlet Zone definition. """

    def __init__(self):
        super().__init__()
        self.id: UUID = uuid4()
        self.convertfluid: bool = True
        self.layers: int = 0
        self.zone_info: InletOutletZoneInfo = InletOutletZoneInfo()
        self.velocity_info: InletOutletVelocityInfo = InletOutletVelocityInfo()
        self.density_info: InletOutletDensityInfo = InletOutletDensityInfo()
        self.elevation_info: InletOutletElevationInfo = InletOutletElevationInfo()
