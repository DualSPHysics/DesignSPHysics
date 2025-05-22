#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Damping Configutarion Dialog"""

import FreeCAD

from PySide2 import QtWidgets
from mod.constants import DIVIDER
from mod.tools.dialog_tools import error_dialog
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.damping.damping_config_dialog import DampingConfigDialog
from mod.widgets.custom_widgets.size_input import SizeInput


class DampingZoneConfigDialog(DampingConfigDialog):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    def __init__(self, damping, group, parent=None):
        super().__init__(damping=damping,group=group,parent=parent)
        # DAMPING ZONE

        self.setWindowTitle("Damping zone configuration")
        self.zone_layout = QtWidgets.QVBoxLayout()

        self.zone_limitmin_layout = QtWidgets.QHBoxLayout()
        self.zone_limitmin_label = QtWidgets.QLabel("Limit Min. (X, Y, Z): ")
        self.zone_limitmin_input_x = SizeInput()
        self.zone_limitmin_input_y = SizeInput()
        self.zone_limitmin_input_z = SizeInput()
        self.zone_limitmin_layout.addWidget(self.zone_limitmin_label)
        self.zone_limitmin_layout.addWidget(self.zone_limitmin_input_x)
        self.zone_limitmin_layout.addWidget(self.zone_limitmin_input_y)
        self.zone_limitmin_layout.addWidget(self.zone_limitmin_input_z)

        self.zone_limitmax_layout = QtWidgets.QHBoxLayout()
        self.zone_limitmax_label = QtWidgets.QLabel("Limit Max. (X, Y, Z): ")
        self.zone_limitmax_input_x = SizeInput()
        self.zone_limitmax_input_y = SizeInput()
        self.zone_limitmax_input_z = SizeInput()
        self.zone_limitmax_layout.addWidget(self.zone_limitmax_label)
        self.zone_limitmax_layout.addWidget(self.zone_limitmax_input_x)
        self.zone_limitmax_layout.addWidget(self.zone_limitmax_input_y)
        self.zone_limitmax_layout.addWidget(self.zone_limitmax_input_z)

        self.zone_layout.addLayout(self.zone_limitmin_layout)
        self.zone_layout.addLayout(self.zone_limitmax_layout)

        self.main_groupbox_layout.insertLayout(0,self.zone_layout)

        self.ok_button.clicked.connect(self.on_ok)
        self.fill_Values()

    def fill_Values(self):
        # Fill fields with case data
        super().fill_Values()
        #self.enabled_checkbox.setChecked(self.damping.enabled)
        line = self.group.OutList[0]
        self.zone_limitmin_input_x.setValue(line.Placement.Base.x / DIVIDER)
        self.zone_limitmin_input_y.setValue(line.Placement.Base.y / DIVIDER)
        self.zone_limitmin_input_z.setValue(line.Placement.Base.z / DIVIDER)
        self.zone_limitmax_input_x.setValue((line.Placement.Base.x + line.X2.Value) / DIVIDER)
        self.zone_limitmax_input_y.setValue((line.Placement.Base.y + line.Y2.Value)/ DIVIDER)
        self.zone_limitmax_input_z.setValue((line.Placement.Base.z + line.Z2.Value) / DIVIDER)


    # Window logic
    def on_ok(self):
        """ Saves damping zone data to the data structure. """
        super().on_ok()
        line = self.group.OutList[0]
        overlimit_line = self.group.OutList[1]
        line.Placement.Base.x = self.zone_limitmin_input_x.value() * DIVIDER
        line.Placement.Base.y = self.zone_limitmin_input_y.value() * DIVIDER
        line.Placement.Base.z = self.zone_limitmin_input_z.value() * DIVIDER
        line.X2 = (self.zone_limitmax_input_x.value()-self.zone_limitmin_input_x.value()) * DIVIDER
        line.Y2 = (self.zone_limitmax_input_y.value()-self.zone_limitmin_input_y.value()) * DIVIDER
        line.Z2 = (self.zone_limitmax_input_z.value()-self.zone_limitmin_input_z.value()) * DIVIDER

        overlimit_line.Placement.Base.x = line.Placement.Base.x+line.X2.Value
        overlimit_line.Placement.Base.y = line.Placement.Base.y+line.Y2.Value
        overlimit_line.Placement.Base.z = line.Placement.Base.z+line.Z2.Value

        overlimit_vector = FreeCAD.Vector(line.X2, line.Y2, line.Z2)
        try:
            overlimit_vector.normalize()
        except FreeCAD.Base.FreeCADError:
            error_dialog(__("The vector between minimum and maximum limit must have length."))

        overlimit_vector = overlimit_vector * (self.damping.overlimit * DIVIDER)
        #overlimit_vector = overlimit_vector + FreeCAD.Vector(line.X2, line.Y2,line.Z2)

        overlimit_line.X2 = overlimit_vector.x
        overlimit_line.Y2 = overlimit_vector.y
        overlimit_line.Z2 = overlimit_vector.z
        overlimit_line.Placement.Base.x = line.Placement.Base.x + line.X2.Value
        overlimit_line.Placement.Base.y = line.Placement.Base.y + line.Y2.Value
        overlimit_line.Placement.Base.z = line.Placement.Base.z + line.Z2.Value

        #FreeCAD.ActiveDocument.recompute()
        self.accept()

