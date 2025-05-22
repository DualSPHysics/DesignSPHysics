#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Multi-Layer Piston data. """

from mod.enums import MLPistonType

class MLPiston():
    """ Multi-Layer Piston common attributes """

    def __init__(self, incz=0):
        self.type = MLPistonType.BASE
        self.incz = incz
