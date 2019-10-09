#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Inlet/Outlet zone info. '''

from mod.enums import InletOutletZoneType, InletOutletDirection


class InletOutletZoneInfo():
    ''' Stores Inlet/Outlet zone information and parameters. '''

    def __init__(self):
        super().__init__()
        self.zone_type: InletOutletZoneType = InletOutletZoneType.ZONE_2D
        self.mkfluid: int = 0
        self.direction: InletOutletDirection = InletOutletDirection.LEFT
