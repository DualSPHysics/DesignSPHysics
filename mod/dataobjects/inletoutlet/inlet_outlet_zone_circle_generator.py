#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" A generator that cretes partiles along the surface of a circle. """
from mod.constants import DIVIDER
import FreeCAD

class InletOutletZoneCircleGenerator:
    """ A generator that cretes partiles along the surface of a circle. """

    def __init__(self, point: list = None, radius: float = 0.0) -> None:
        if point is None:
            point=[0.0,0.0,0.0]
        self.point: list = point
        self.radius: float = radius
        self.manual_setting:bool = False

    def save_values(self, values):
        self.point = values["point"]
        self.radius = values["radius"]
        self.manual_setting =values["manual_setting"]

    def size_from_freecad_circle(self,circle):
        #self.point=list(circle.Placement.Base/ DIVIDER)
        self.radius = circle.Radius.Value / DIVIDER

    def from_freecad_circle(self, circle):
        self.point=list(circle.Placement.Base/ DIVIDER)
        self.radius = circle.Radius.Value / DIVIDER

    def move(self,displacement:FreeCAD.Vector):
        self.point = list((FreeCAD.Vector(self.point)*DIVIDER + displacement)/DIVIDER)