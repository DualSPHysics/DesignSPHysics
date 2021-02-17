#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A generator that creates particles along the surface of a box. """


class InletOutletZoneBoxGenerator():
    """ A generator that creates particles along the surface of a box. """
    
    def __init__(self) -> None:
        self.point: list = [0.0, 0.0, 0.0]
        self.size: list = [0.0, 0.0, 0.0]
        self.direction: list = [0.0, 0.0, 0.0]
        self.rotateaxis_enabled: bool = False
        self.rotateaxis_angle: float = 0.0
        self.rotateaxis_point1: list = [0.0, 0.0, 0.0]
        self.rotateaxis_point2: list = [0.0, 0.0, 0.0]