#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Chrono Object. """

from mod.enums import ChronoModelNormalType, ChronoFloatingType


class ChronoObject:
    """ Chrono Object. """

    def __init__(self):
        self.id: str = ""  # FreeCAD Object Name
        self.name: str = ""
        self.mkbound: int = 0
        self.modelnormal_enabled: bool = False
        self.modelnormal_type: ChronoModelNormalType.ORIGINAL
        self.floating_type: ChronoFloatingType = ChronoFloatingType.BODYFIXED
