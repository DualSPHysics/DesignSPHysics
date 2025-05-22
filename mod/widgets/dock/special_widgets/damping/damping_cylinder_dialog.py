#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Damping Configutarion Dialog"""

import FreeCAD

from PySide2 import QtWidgets
from mod.constants import DIVIDER
from mod.widgets.dock.special_widgets.damping.damping_config_dialog import DampingConfigDialog
from mod.widgets.custom_widgets.size_input import SizeInput


class DampingCylinderConfigDialog(DampingConfigDialog):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    def __init__(self, damping, group, parent=None):
        super().__init__(damping=damping,group=group,parent=parent)

        self.setWindowTitle("Damping cylinder configuration")
        # CYLINDER LAYOUT
        self.cylinder_layout = QtWidgets.QVBoxLayout()

        self.cylinder_point1_layout = QtWidgets.QHBoxLayout()
        self.cylinder_point1_label = QtWidgets.QLabel("Point 1. (X, Y, Z): ")
        self.cylinder_point1_input_x = SizeInput()
        self.cylinder_point1_input_y = SizeInput()
        self.cylinder_point1_input_z = SizeInput()
        self.cylinder_point1_layout.addWidget(self.cylinder_point1_label)
        self.cylinder_point1_layout.addWidget(self.cylinder_point1_input_x)
        self.cylinder_point1_layout.addWidget(self.cylinder_point1_input_y)
        self.cylinder_point1_layout.addWidget(self.cylinder_point1_input_z)

        self.cylinder_point2_layout = QtWidgets.QHBoxLayout()
        self.cylinder_point2_label = QtWidgets.QLabel("Point2. (X, Y, Z): ")
        self.cylinder_point2_input_x = SizeInput()
        self.cylinder_point2_input_y = SizeInput()
        self.cylinder_point2_input_z = SizeInput()
        self.cylinder_point2_layout.addWidget(self.cylinder_point2_label)
        self.cylinder_point2_layout.addWidget(self.cylinder_point2_input_x)
        self.cylinder_point2_layout.addWidget(self.cylinder_point2_input_y)
        self.cylinder_point2_layout.addWidget(self.cylinder_point2_input_z)

        self.cylinder_limits_layout = QtWidgets.QHBoxLayout()
        self.cylinder_limits_label = QtWidgets.QLabel("Limit radius (Min, Max) : ")
        self.cylinder_limits_min_input = SizeInput()
        self.cylinder_limits_max_input = SizeInput()
        self.cylinder_limits_layout.addWidget(self.cylinder_limits_label)
        self.cylinder_limits_layout.addWidget(self.cylinder_limits_min_input)
        self.cylinder_limits_layout.addWidget(self.cylinder_limits_max_input)

        self.cylinder_layout.addLayout(self.cylinder_point1_layout)
        self.cylinder_layout.addLayout(self.cylinder_point2_layout)
        self.cylinder_layout.addLayout(self.cylinder_limits_layout)

        self.main_groupbox_layout.insertLayout(0,self.cylinder_layout)

        self.ok_button.clicked.connect(self.on_ok)
        self.fill_Values()

    def fill_Values(self):
        # Fill fields with case data
        super().fill_Values()
        line = self.group.OutList[0]
        circle_min=self.group.OutList[1]
        circle_max = self.group.OutList[2]
        self.cylinder_point1_input_x.setValue(line.Placement.Base.x / DIVIDER)
        self.cylinder_point1_input_y.setValue(line.Placement.Base.y / DIVIDER)
        self.cylinder_point1_input_z.setValue(line.Placement.Base.z / DIVIDER)
        self.cylinder_point2_input_x.setValue((line.Placement.Base.x + line.X2.Value) / DIVIDER)
        self.cylinder_point2_input_y.setValue((line.Placement.Base.y + line.Y2.Value) / DIVIDER)
        self.cylinder_point2_input_z.setValue((line.Placement.Base.z + line.Z2.Value) / DIVIDER)
        self.cylinder_limits_min_input.setValue(circle_min.Radius.Value / DIVIDER)
        self.cylinder_limits_max_input.setValue(circle_max.Radius.Value / DIVIDER)



    # Window logic
    def on_ok(self):
        """ Saves damping zone data to the data structure. """
        super().on_ok()
        line = self.group.OutList[0]
        circle_min1 = self.group.OutList[1]
        circle_max1 = self.group.OutList[2]
        circle_min2 = self.group.OutList[3]
        circle_max2 = self.group.OutList[4]
        line.Placement.Base.x=self.cylinder_point1_input_x.value() * DIVIDER
        line.Placement.Base.y=self.cylinder_point1_input_y.value() * DIVIDER
        line.Placement.Base.z=self.cylinder_point1_input_z.value() * DIVIDER
        line.X2 = (self.cylinder_point2_input_x.value()- self.cylinder_point1_input_x.value()) * DIVIDER
        line.Y2 = (self.cylinder_point2_input_y.value()-self.cylinder_point1_input_y.value() )* DIVIDER
        line.Z2 = (self.cylinder_point2_input_z.value()-self.cylinder_point1_input_z.value()) * DIVIDER
        circle_min1.Radius = self.cylinder_limits_min_input.value() * DIVIDER
        circle_min2.Radius = circle_min1.Radius
        circle_max1.Radius = self.cylinder_limits_max_input.value() * DIVIDER
        circle_max2.Radius = circle_max1.Radius

        orig_vec=FreeCAD.Base.Vector(0,0,1)
        line_vec=FreeCAD.Base.Vector(line.X2,line.Y2,line.Z2)
        rotation=FreeCAD.Base.Rotation(orig_vec,line_vec)
        circle_min1.Placement.Rotation=rotation
        circle_max1.Placement=circle_min1.Placement
        circle_min2.Placement.Rotation=rotation
        circle_max2.Placement = circle_min2.Placement


        FreeCAD.ActiveDocument.recompute()
        self.accept()
