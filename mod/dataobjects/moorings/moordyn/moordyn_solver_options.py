#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn solver options. """


class MoorDynSolverOptions():
    """ MoorDyn general solver options dataobject. """

    def __init__(self):
        self.gravity: float = 9.81
        self.water_depth: float = 0.5
        self.freesurface: float = 0.0
        self.kBot: str = "3.0e6"
        self.cBot: str = "3.0e6"
        self.dtM: float = 0.0001
        self.waveKin: int = 0
        self.writeUnits: str = "yes"
        self.frictionCoefficient: float = 0.0
        self.fricDamp: float = 200.0
        self.statDynFricScale: float = 1.0
        self.dtIC: float = 1.0
        self.cdScaleIC: float = 5.0
        self.threshIC: float = 0.01
        self.tmaxIC: float = 10.0
        self.timeMax: float = 10.0
