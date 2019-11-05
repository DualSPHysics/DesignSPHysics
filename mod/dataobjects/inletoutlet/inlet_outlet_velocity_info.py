#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet Velocity info. """

from mod.enums import InletOutletVelocityType


class InletOutletVelocityInfo():
    """ Stores Inlet/Outlet Velocity information and parameters. """

    def __init__(self):
        super().__init__()
        self.velocity_type: InletOutletVelocityType = InletOutletVelocityType.FIXED
        self.value: float = 0.0
