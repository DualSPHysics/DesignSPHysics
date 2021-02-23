#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet elevation info. """

from mod.enums import InletOutletElevationType, InletOutletZSurfMode


class InletOutletElevationInfo():
    """ Stores Inlet/Outlet elevation information and parameters. """

    def __init__(self):
        self.elevation_type: InletOutletElevationType = InletOutletElevationType.FIXED
        self.savevtk: bool = False
        self.remove: bool = False
        self.zbottom: float = 0.0
        self.zsurf_mode: InletOutletZSurfMode = InletOutletZSurfMode.FIXED
        self.zsurf: float = 0.0
        self.zsurftimes: list = [] # [(float(time), float(value))]
        self.zsurffile: str = ""