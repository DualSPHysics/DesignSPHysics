#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus Fix Connection. """


class MoorDynPlusFixConnection():
    """ MoorDynPlus Fix Connection representation. """

    def __init__(self, point=None):
        self.point: list = point or [0.0, 0.0, 0.0]
