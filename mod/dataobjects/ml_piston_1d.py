#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Multi-Layer Piston 1D Data. """

from mod.dataobjects.ml_piston import MLPiston

from mod.enums import MLPistonType

class MLPiston1D(MLPiston):
    """ Multi-Layer Pistons using external velocity (for example, from SWASH) """

    def __init__(self, filevelx=None, incz=0, timedataini=0, smooth=0):
        MLPiston.__init__(self, incz=incz)
        self.type = MLPistonType.MLPISTON1D
        self.filevelx = filevelx
        self.timedataini = timedataini
        self.smooth = smooth
