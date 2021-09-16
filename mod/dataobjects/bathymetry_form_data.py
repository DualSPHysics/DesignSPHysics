#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Bathymetry Form data """


class BathymetryFormData():
    """ Bathymetry Form Data. """

    def __init__(self):
        self.move = ["0", "0", "0"]
        self.rotate = ["0", "0", "0"]
        self.scale = ["1", "1", "1"]
        self.selection_enabled = False
        self.selection_point = ["", ""]
        self.selection_size = ["", ""]
        self.gdp = "1"
        self.initdomain_enabled = False
        self.initdomain_point = ["", ""]
        self.initdomain_size = ["", ""]
        self.xmin_enabled = False
        self.expands_xmin = ["", "", "", ""]
        self.xmax_enabled = False
        self.expands_xmax = ["", "", "", ""]
        self.ymin_enabled = False
        self.expands_ymin = ["", "", "", ""]
        self.ymax_enabled = False
        self.expands_ymax = ["", "", "", ""]
        self.periodicx_enabled = False
        self.periodicx_rampwidth = ""
        self.periodicx_flatwidth = ""
        self.periodicy_enabled = False
        self.periodicy_rampwidth = ""
        self.periodicy_flatwidth = ""
        self.finalmove_enabled = False
        self.finalmove = ["", "", ""]
