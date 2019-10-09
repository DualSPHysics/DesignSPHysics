#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet elevation info. """

from mod.enums import InletOutletElevationType


class InletOutletElevationInfo():
    """ Stores Inlet/Outlet elevation information and parameters. """

    def __init__(self):
        super().__init__()
        self.elevation_type: InletOutletElevationType.FIXED
        self.zbottom: float = 0.0
        self.zsurf: float = 0.0
