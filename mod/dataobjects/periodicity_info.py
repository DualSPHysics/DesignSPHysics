#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Periodicity Information data. """

class PeriodicityInfo():
    """ Defines periodicty for an axis """

    def __init__(self, enabled=False, x_increment=0.0, y_increment=0.0, z_increment=0.0):
        self.enabled: bool = enabled
        self.x_increment: float = x_increment
        self.y_increment: float = y_increment
        self.z_increment: float = z_increment
