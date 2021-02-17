#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet configuration. """

from mod.enums import InletOutletDetermLimit, InletOutletExtrapolateMode

from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone


class InletOutletConfig():
    """ Configuration for Inlet/Oulet Zones. """

    def __init__(self):
        self.memoryresize_size0: int = 2
        self.memoryresize_size: int = 4
        self.useboxlimit_enabled: bool = True
        self.useboxlimit_freecentre_enabled: bool = False
        self.useboxlimit_freecentre_values: bool = [0.0, 0.0, 0.0]
        self.determlimit: InletOutletDetermLimit = InletOutletDetermLimit.ZEROTH_ORDER
        self.extrapolatemode: InletOutletExtrapolateMode = InletOutletExtrapolateMode.FAST_SINGLE
        self.zones: list = list()  # [InletOutletZone]

    def get_io_zone_for_id(self, search_id) -> InletOutletZone:
        """ Returns the InletOutletZone for a given id. """
        found_zone: InletOutletZone = None

        for zone in self.zones:
            if zone.id == search_id:
                found_zone = zone

        return found_zone
