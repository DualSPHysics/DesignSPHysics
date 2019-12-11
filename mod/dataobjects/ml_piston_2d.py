#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Multi-Layer Piston 2D Data. """

from mod.dataobjects.ml_piston import MLPiston

from mod.enums import MLPistonType


class MLPiston2D(MLPiston):
    """ Multi-Layer Pistons using external velocity (for example, from SWASH) """

    def __init__(self, incz=0, smoothz=0, smoothy=0, veldata=None):
        MLPiston.__init__(self, incz=incz)
        self.type = MLPistonType.MLPISTON2D
        self.smoothz = smoothz
        self.smoothy = smoothy
        self.veldata = veldata or []  # [MLPiston2DVeldata]
