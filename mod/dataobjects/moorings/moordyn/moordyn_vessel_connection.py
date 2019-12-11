#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Vessel Connection. """


class MoorDynVesselConnection():
    """ MoorDyn Vessel Connection representation. """

    def __init__(self, bodyref=-1, point=None):
        self.bodyref: int = bodyref
        self.point: list = point or [0.0, 0.0, 0.0]
