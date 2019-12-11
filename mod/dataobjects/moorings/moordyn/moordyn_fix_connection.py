#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Fix Connection. """


class MoorDynFixConnection():
    """ MoorDyn Fix Connection representation. """

    def __init__(self, point=None):
        self.point: list = point or [0.0, 0.0, 0.0]
