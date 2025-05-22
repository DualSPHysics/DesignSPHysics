#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Flow Tool Box. """

from uuid import UUID, uuid4


class FlowToolXmlBox():
    """ A structure representing a box used by FlowTool to measure data. """

    DEFAULT_NAME: str = "FLOWBOX"

    def __init__(self):
        self.id: UUID = uuid4()
        self.name: str = self.DEFAULT_NAME
        self.point: list[float] = [0.0, 0.0, 0.0]
        self.size: list() = [0.0, 0.0, 0.0]
        self.angle: list() = [0.0, 0.0, 0.0]
        self.divide_axis:bool=False
        self.axis:str="x"
        self.fc_object_name:str=""
