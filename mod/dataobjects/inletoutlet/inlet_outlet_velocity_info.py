#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet Velocity info. """

from mod.dataobjects.inletoutlet.velocities.parabolic_velocity import ParabolicVelocity
from mod.dataobjects.inletoutlet.velocities.linear_velocity import LinearVelocity
from mod.enums import InletOutletVelocitySpecType, InletOutletVelocityType


class InletOutletVelocityInfo():
    """ Stores Inlet/Outlet Velocity information and parameters. """

    def __init__(self):
        self.velocity_type: InletOutletVelocityType = InletOutletVelocityType.FIXED
        self.velocity_specification_type: InletOutletVelocitySpecType = InletOutletVelocitySpecType.FIXED_CONSTANT
        self.fixed_constant_value: float = 0.0
        self.fixed_linear_value: LinearVelocity = LinearVelocity()
        self.fixed_parabolic_value: ParabolicVelocity = ParabolicVelocity()
        self.variable_uniform_values: list = [] #[(float(time), float(value))]
        self.variable_linear_values: list = [] #[(float(time), LinearVelocity)]
        self.variable_parabolic_values: list = [] #[(float(time), ParabolicVelocity)]
        self.file_path: str = "" # This path is shared across Uniform, Linear, Parabolic and Interpolated file types
        self.gridresetvelz: bool = False
        self.gridposzero: list = [] # [float(x), float(z)]
