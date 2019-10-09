#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Domain Fixed Parameter data. """


class DomainFixedParameter():
    """ Fixed Domain for a DSPH case.

    Attributes:
        xmin = Minimum X coordinate for the fixed domain
        xmax = Maximum X coordinate for the fixed domain
        ymin = Minimum Y coordinate for the fixed domain
        ymax = Maximum Y coordinate for the fixed domain
        zmin = Minimum Z coordinate for the fixed domain
        zmax = Maximum Z coordinate for the fixed domain
    """

    def __init__(self, enabled, xmin, xmax, ymin, ymax, zmin, zmax):
        self.enabled = enabled
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __str__(self):
        to_ret = """
            Enabled: {}\n
            Xmin & Xmax: {} ; {}\n
            Ymin & Ymax: {} ; {}\n
            Zmin & Zmax: {} ; {}\n
            """
        return to_ret.format(self.enabled, self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)
