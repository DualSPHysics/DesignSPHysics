#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A Zone generator that creates particles along a line """
from mod.constants import DIVIDER
from mod.tools.stdout_tools import debug
import FreeCAD

class InletOutletZoneLineGenerator():
    """ A Zone generator that creates particles along a line """
    
    def __init__(self, point=None, point2=None) -> None:
        if point2 is None:
            point2 = [0.0, 0.0, 0.0]
        if point is None:
            point = [0.0, 0.0, 0.0]
        self.point: list = point
        self.point2: list = point2
        self.manual_setting:bool = False
        
    def save_values(self,values):
        self.point = values["point"]
        self.point2 = values["point2"]
        self.manual_setting = values["manual_setting"]

    def from_freecad_line(self,fc_obj):
        self.point = list(fc_obj.Placement.Base/DIVIDER)
        self.point2 = list((fc_obj.Placement.Base + FreeCAD.Vector(fc_obj.X2,fc_obj.Y2,fc_obj.Z2))/DIVIDER)

