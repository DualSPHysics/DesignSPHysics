#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet density info. """

from mod.enums import InletOutletDensityType


class InletOutletDensityInfo():
    """ Stores Inlet/Outlet density information and parameters. """

    def __init__(self):
        self.density_type: InletOutletDensityType = InletOutletDensityType.FIXED
        self.value: float = 0.0
