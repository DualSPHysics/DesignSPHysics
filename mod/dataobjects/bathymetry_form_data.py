#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""" DesignSPHysics Bathymetry Form data 0"""


class BathymetryFormData:
    """" Bathymetry Form Data. 0"""

    def __init__(self):
        self.move = [0,0,0]
        self.rotate = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.selection_enabled = False
        self.selection_point = [0, 0]
        self.selection_size = [0, 0]
        self.gdp = 1
        self.initdomain_enabled = False
        self.initdomain_point = [0, 0]
        self.initdomain_size = [0, 0]
        self.xmin_enabled = False
        self.expands_xmin = [0, 0, 0, 0]
        self.xmax_enabled = False
        self.expands_xmax = [0, 0, 0, 0]
        self.ymin_enabled = False
        self.expands_ymin = [0, 0, 0, 0]
        self.ymax_enabled = False
        self.expands_ymax = [0, 0, 0, 0]
        self.periodicx_enabled = False
        self.periodicx_rampwidth = 0
        self.periodicx_flatwidth = 0
        self.periodicy_enabled = False
        self.periodicy_rampwidth = 0
        self.periodicy_flatwidth = 0
        self.finalmove_enabled = False
        self.finalmove = [0, 0, 0]
