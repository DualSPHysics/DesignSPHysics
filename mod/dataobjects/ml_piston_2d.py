#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Multi-Layer Piston 2D Data. """

from mod.dataobjects.ml_piston import MLPiston


class MLPiston2D(MLPiston):
    """ Multi-Layer Pistons using external velocity (for example, from SWASH) """

    def __init__(self, incz=0, smoothz=0, smoothy=0, veldata=None):
        super().__init__(incz=incz)
        self.smoothz = smoothz
        self.smoothy = smoothy
        self.veldata = veldata or []  # [MLPiston2DVeldata]
