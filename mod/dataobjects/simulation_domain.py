#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Simulation domain data. """

from mod.dataobjects.sd_position_property import SDPositionProperty


class SimulationDomain():
    """ Case domain data information """

    def __init__(self):
        self.enabled: bool = False
        self.posmin_x: SDPositionProperty = SDPositionProperty()
        self.posmin_y: SDPositionProperty = SDPositionProperty()
        self.posmin_z: SDPositionProperty = SDPositionProperty()
        self.posmax_x: SDPositionProperty = SDPositionProperty()
        self.posmax_y: SDPositionProperty = SDPositionProperty()
        self.posmax_z: SDPositionProperty = SDPositionProperty()
