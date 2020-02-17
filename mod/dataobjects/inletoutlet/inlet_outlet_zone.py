#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet zone. """

from uuid import UUID, uuid4

from mod.enums import InletOutletRefillingMode, InletOutletInputTreatment
from mod.stdout_tools import debug

from mod.dataobjects.inletoutlet.inlet_outlet_zone_info import InletOutletZoneInfo
from mod.dataobjects.inletoutlet.inlet_outlet_velocity_info import InletOutletVelocityInfo
from mod.dataobjects.inletoutlet.inlet_outlet_density_info import InletOutletDensityInfo
from mod.dataobjects.inletoutlet.inlet_outlet_elevation_info import InletOutletElevationInfo


class InletOutletZone:
    """ Inlet/Outlet Zone definition. """

    def __init__(self):
        self.id: UUID = uuid4()
        self.refilling: InletOutletRefillingMode = InletOutletRefillingMode.SIMPLE_FULL
        self.inputtreatment: InletOutletInputTreatment = InletOutletInputTreatment.NO_CHANGES
        self.layers: int = 0
        self.zone_info: InletOutletZoneInfo = InletOutletZoneInfo()
        self.velocity_info: InletOutletVelocityInfo = InletOutletVelocityInfo()
        self.density_info: InletOutletDensityInfo = InletOutletDensityInfo()
        self.elevation_info: InletOutletElevationInfo = InletOutletElevationInfo()

    def __getattr__(self, attr):
        if attr == "refilling":
            debug("refilling property in InletOutletZone <{}> nonexistent: Creating one".format(self.id))
            self.refilling: InletOutletRefillingMode = InletOutletRefillingMode.SIMPLE_FULL
            return self.refilling
        if attr == "inputtreatment":
            debug("inputtreatment property in InletOutletZone <{}> nonexistent: Creating one".format(self.id))
            self.inputtreatment: InletOutletInputTreatment = InletOutletInputTreatment.NO_CHANGES
            return self.inputtreatment
        raise AttributeError()
