#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics save options for moorings configuration. """


class MooringsSaveOptions():
    """ DesignSPHysics save options for moorings configuration. """

    def __init__(self):
        self.savevtk_moorings: bool = True
        self.savecsv_points: bool = True
        self.savevtk_points: bool = False
