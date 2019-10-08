#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics Inlet/Outlet configuration. '''

from mod.enums import InletOutletDetermLimit

class InletOutletConfig():
    ''' Configuration for Inlet/Oulet Zones. '''

    def __init__(self):
        super().__init__()
        self.reuseids: bool = False
        self.resizetime: float = 0.5
        self.userefilling: bool = False
        self.determlimit: InletOutletDetermLimit = InletOutletDetermLimit.ZEROTH_ORDER
        self.zones: list = list() # [InletOutletZone]
