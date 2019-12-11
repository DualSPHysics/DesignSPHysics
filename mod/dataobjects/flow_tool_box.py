#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Flow Tool Box. """

from uuid import UUID, uuid4


class FlowToolBox():
    """ A structure representing a box used by FlowTool to measure data. """

    DEFAULT_NAME: str = "BOX"

    def __init__(self):
        self.id: UUID = uuid4()
        self.name: str = self.DEFAULT_NAME
        self.point1: list() = [0.0, 0.0, 0.0]
        self.point2: list() = [0.0, 0.0, 0.0]
        self.point3: list() = [0.0, 0.0, 0.0]
        self.point4: list() = [0.0, 0.0, 0.0]
        self.point5: list() = [0.0, 0.0, 0.0]
        self.point6: list() = [0.0, 0.0, 0.0]
        self.point7: list() = [0.0, 0.0, 0.0]
        self.point8: list() = [0.0, 0.0, 0.0]
