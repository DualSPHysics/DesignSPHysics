#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn default line properties. """


class MoorDynLineDefaultConfiguration():
    """ MoorDyn LineDefault configuration object. """

    def __init__(self):
        self.ea: str = "2.9e3"
        self.diameter: str = "3.656E-3"
        self.massDenInAir: float = 0.0607
        self.ba: float = -0.8
        self.can: float = 1.0
        self.cat: float = 0.0
        self.cdn: float = 1.6
        self.cdt: float = 0.05
        self.breaktension: float = 0.0
        self.outputFlags: str = "pvc"
