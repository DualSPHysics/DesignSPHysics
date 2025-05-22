#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A generator that creates particles along the surface of a box. """
from mod.constants import DIVIDER
import FreeCAD


class InletOutletZoneBoxGenerator():
    """ A generator that creates particles along the surface of a box. """

    def __init__(self, point=None, size=None) -> None:
        if size is None:
            size = [0.0, 0.0, 0.0]
        if point is None:
            point = [0.0, 0.0, 0.0]
        self.point = point
        self.size: list = size
        self.manual_setting:bool = False

    def save_values(self, values):
        self.point = values["point"]
        self.size = values["size"]
        self.manual_setting = values["manual_setting"]

    def from_freecad_box(self,box):
        self.point = list(box.Placement.Base / DIVIDER)
        self.size =  [  box.Length.Value / DIVIDER if box.Length.Value / DIVIDER > 10e-6 else 0,
                        box.Width.Value / DIVIDER if box.Width.Value / DIVIDER > 10e-6 else 0,
                        box.Height.Value / DIVIDER if box.Height.Value / DIVIDER > 10e-6 else 0]

    def move(self,displacement:FreeCAD.Vector):
        self.point = list((FreeCAD.Vector(self.point)*DIVIDER + displacement)/DIVIDER)