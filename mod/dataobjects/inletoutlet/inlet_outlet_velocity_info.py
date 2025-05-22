#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Inlet/Outlet Velocity self. """
from mod.dataobjects.inletoutlet.velocities.jet_circle import JetCircle
from mod.dataobjects.inletoutlet.velocities.parabolic_velocity import ParabolicVelocity
from mod.dataobjects.inletoutlet.velocities.linear_velocity import LinearVelocity
from mod.dataobjects.inletoutlet.velocities.velocity_mesh_data import VelocityMeshData
from mod.enums import InletOutletVelocitySpecType, InletOutletVelocityType, FlowUnits


class InletOutletVelocityInfo():
    """ Stores Inlet/Outlet Velocity selfrmation and parameters. """

    def __init__(self):
        self.velocity_type: InletOutletVelocityType = InletOutletVelocityType.FIXED
        self.velocity_specification_type: InletOutletVelocitySpecType = InletOutletVelocitySpecType.FIXED_CONSTANT
        self.fixed_constant_value: float = 0.0
        self.fixed_linear_value: LinearVelocity = LinearVelocity()
        self.fixed_parabolic_value: ParabolicVelocity = ParabolicVelocity()
        self.variable_uniform_values: list = []  # [(float(time), float(value))]
        self.variable_linear_values: list = []  # [(float(time), LinearVelocity)]
        self.variable_parabolic_values: list = []  # [(float(time), ParabolicVelocity)]
        self.file_path: str = ""  # This path is shared across Uniform, Linear, Parabolic and Interpolated file types
        self.gridresetvelz: bool = False
        self.gridposzero: list = [0.0, 0.0]  # [float(x), float(z)]
        self.flow_velocity_active: bool = False
        self.flow_velocity_ratio: float = 1.0
        self.fixed_jetcircle_value: JetCircle = JetCircle()
        self.flow_velocity_units: FlowUnits = FlowUnits.LITERSSECOND
        self.velocity_mesh_data : VelocityMeshData = VelocityMeshData()

    def save_v_constant(self, values):
        self.fixed_constant_value = values["fixed_constant_value"]

    def save_v_fixed_linear(self, values):
        self.fixed_linear_value.v1 = values["fixed_linear_value.v1"]
        self.fixed_linear_value.v2 = values["fixed_linear_value.v2"]
        self.fixed_linear_value.z1 = values["fixed_linear_value.z1"]
        self.fixed_linear_value.z2 = values["fixed_linear_value.z2"]

    def save_v_fixed_parabolic(self, values):
        self.fixed_parabolic_value.v1 = values["fixed_parabolic_value.v1"]
        self.fixed_parabolic_value.v2 = values["fixed_parabolic_value.v2"]
        self.fixed_parabolic_value.v3 = values["fixed_parabolic_value.v3"]
        self.fixed_parabolic_value.z1 = values["fixed_parabolic_value.z1"]
        self.fixed_parabolic_value.z2 = values["fixed_parabolic_value.z2"]
        self.fixed_parabolic_value.z3 = values["fixed_parabolic_value.z3"]

    def save_v_variable_uniform(self, values):
        self.variable_uniform_values = values["variable_uniform_values"]

    def save_v_variable_linear(self, values):
        self.variable_linear_values = values["variable_linear_values"]

    def save_v_variable_parabolic(self, values):
        self.variable_parabolic_values = values["variable_parabolic_values"]

    def save_v_file(self, values):
        self.file_path = values["file_path"]

    def save_v_interpolated(self, values):
        self.file_path = values["file_path"]
        self.gridresetvelz = values["gridresetvelz"]
        self.gridposzero = values["gridposzero"]

    def save_flow_velocity(self, values):
        self.flow_velocity_active = values["flow_velocity_active"]
        self.flow_velocity_ratio = values["flow_velocity_ratio"]
        self.flow_velocity_units = values["flow_velocity_units"]

    def save_v_fixed_jetcircle(self, values):
        self.fixed_jetcircle_value.v = values["jet_circle.v"]
        self.fixed_jetcircle_value.distance = values["jet_circle.distance"]
        self.fixed_jetcircle_value.radius = values["jet_circle.radius"]

    def save_v_mesh_data(self,values):
        self.velocity_mesh_data.save(values)


