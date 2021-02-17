#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A Zone generator that creates particles along a line """


class InletOutletZoneGenerator():
    """ Base class for the different Inlet/Outlet Zone Generators. """
    
    def __init__(self) -> None:
        self.point: list = [0.0, 0.0, 0.0]
        self.point2: list = [0.0, 0.0, 0.0]
        self.direction_enabled: bool = False
        self.direction: list = [0.0, 0.0, 0.0]
        self.has_rotation: bool = False
        self.rotate_angle: float = 0.0