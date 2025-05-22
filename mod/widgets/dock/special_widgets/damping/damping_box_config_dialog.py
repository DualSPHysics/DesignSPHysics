#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Damping Configutarion Dialog"""

import FreeCAD

from PySide2 import QtCore, QtWidgets
from mod.constants import DIVIDER
from mod.tools.translation_tools import __
from mod.widgets.dock.special_widgets.damping.damping_config_dialog import DampingConfigDialog
from mod.widgets.custom_widgets.size_input import SizeInput


class DampingBoxConfigDialog(DampingConfigDialog):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    def __init__(self, damping, group, parent=None):
        super().__init__(damping=damping,group=group,parent=parent)

        self.setWindowTitle("Damping box configuration")

        # DAMPING BOX
        self.box_layout = QtWidgets.QVBoxLayout()
        self.box_directions_layout = QtWidgets.QVBoxLayout()
        self.all_directions = QtWidgets.QCheckBox(__("All directions"))
        self.all_directions.setChecked(QtCore.Qt.Checked)
        self.all_directions.toggled.connect(self.on_directions_checkbox)
        self.front_direction = QtWidgets.QCheckBox(__("Front direction"))
        self.back_direction = QtWidgets.QCheckBox(__("Back direction"))
        self.top_direction = QtWidgets.QCheckBox(__("Top direction"))
        self.bottom_direction = QtWidgets.QCheckBox(__("Bottom direction"))
        self.left_direction = QtWidgets.QCheckBox(__("Left direction"))
        self.right_direction = QtWidgets.QCheckBox(__("Right direction"))

        self.box_directions_options_row1_layout = QtWidgets.QHBoxLayout()
        self.box_directions_options_row2_layout = QtWidgets.QHBoxLayout()
        self.box_directions_options_row1_layout.addWidget(self.front_direction)
        self.box_directions_options_row1_layout.addWidget(self.top_direction)
        self.box_directions_options_row1_layout.addWidget(self.left_direction)
        self.box_directions_options_row2_layout.addWidget(self.back_direction)
        self.box_directions_options_row2_layout.addWidget(self.bottom_direction)
        self.box_directions_options_row2_layout.addWidget(self.right_direction)
        self.box_directions_layout.addWidget(self.all_directions)
        self.box_directions_layout.addLayout(self.box_directions_options_row1_layout)
        self.box_directions_layout.addLayout(self.box_directions_options_row2_layout)

        self.box_limitmin_pointini_layout = QtWidgets.QHBoxLayout()
        self.box_limitmin_pointini_label = QtWidgets.QLabel("Limit Min Point Ini. (X, Y, Z): ")
        self.box_limitmin_pointini_input_x = SizeInput()
        self.box_limitmin_pointini_input_y = SizeInput()
        self.box_limitmin_pointini_input_z = SizeInput()
        self.box_limitmin_pointini_layout.addWidget(self.box_limitmin_pointini_label)
        self.box_limitmin_pointini_layout.addWidget(self.box_limitmin_pointini_input_x)
        self.box_limitmin_pointini_layout.addWidget(self.box_limitmin_pointini_input_y)
        self.box_limitmin_pointini_layout.addWidget(self.box_limitmin_pointini_input_z)

        self.box_limitmin_pointend_layout = QtWidgets.QHBoxLayout()
        self.box_limitmin_pointend_label = QtWidgets.QLabel("Limit Min Point End. (X, Y, Z): ")
        self.box_limitmin_pointend_input_x = SizeInput()
        self.box_limitmin_pointend_input_y = SizeInput()
        self.box_limitmin_pointend_input_z = SizeInput()
        self.box_limitmin_pointend_layout.addWidget(self.box_limitmin_pointend_label)
        self.box_limitmin_pointend_layout.addWidget(self.box_limitmin_pointend_input_x)
        self.box_limitmin_pointend_layout.addWidget(self.box_limitmin_pointend_input_y)
        self.box_limitmin_pointend_layout.addWidget(self.box_limitmin_pointend_input_z)

        self.box_limitmax_pointini_layout = QtWidgets.QHBoxLayout()
        self.box_limitmax_pointini_label = QtWidgets.QLabel("Limit Max point ini. (X, Y, Z): ")
        self.box_limitmax_pointini_input_x = SizeInput()
        self.box_limitmax_pointini_input_y = SizeInput()
        self.box_limitmax_pointini_input_z = SizeInput()
        self.box_limitmax_pointini_layout.addWidget(self.box_limitmax_pointini_label)
        self.box_limitmax_pointini_layout.addWidget(self.box_limitmax_pointini_input_x)
        self.box_limitmax_pointini_layout.addWidget(self.box_limitmax_pointini_input_y)
        self.box_limitmax_pointini_layout.addWidget(self.box_limitmax_pointini_input_z)

        self.box_limitmax_pointend_layout = QtWidgets.QHBoxLayout()
        self.box_limitmax_pointend_label = QtWidgets.QLabel("Limit Max point end (X, Y, Z): ")
        self.box_limitmax_pointend_input_x = SizeInput()
        self.box_limitmax_pointend_input_y = SizeInput()
        self.box_limitmax_pointend_input_z = SizeInput()
        self.box_limitmax_pointend_layout.addWidget(self.box_limitmax_pointend_label)
        self.box_limitmax_pointend_layout.addWidget(self.box_limitmax_pointend_input_x)
        self.box_limitmax_pointend_layout.addWidget(self.box_limitmax_pointend_input_y)
        self.box_limitmax_pointend_layout.addWidget(self.box_limitmax_pointend_input_z)

        self.box_layout.addLayout(self.box_directions_layout)
        self.box_layout.addLayout(self.box_limitmin_pointini_layout)
        self.box_layout.addLayout(self.box_limitmin_pointend_layout)
        self.box_layout.addLayout(self.box_limitmax_pointini_layout)
        self.box_layout.addLayout(self.box_limitmax_pointend_layout)

        self.main_groupbox_layout.insertLayout(0,self.box_layout)

        self.ok_button.clicked.connect(self.on_ok)
        self.enabled_checkbox.stateChanged.connect(self.on_enable_chk)
        self.fill_Values()

    def fill_Values(self):
        # Fill fields with case data
        super().fill_Values()
        box1 = self.group.OutList[0]
        box2 = self.group.OutList[1]
        self.box_limitmin_pointini_input_x.setValue(box1.Placement.Base[0] / DIVIDER)
        self.box_limitmin_pointini_input_y.setValue(box1.Placement.Base[1] / DIVIDER)
        self.box_limitmin_pointini_input_z.setValue(box1.Placement.Base[2] / DIVIDER)
        self.box_limitmin_pointend_input_x.setValue((box1.Placement.Base[0] + box1.Length.Value) / DIVIDER)
        self.box_limitmin_pointend_input_y.setValue((box1.Placement.Base[1] + box1.Width.Value) / DIVIDER)
        self.box_limitmin_pointend_input_z.setValue((box1.Placement.Base[2] + box1.Height.Value) / DIVIDER)
        self.box_limitmax_pointini_input_x.setValue(box2.Placement.Base[0] / DIVIDER)
        self.box_limitmax_pointini_input_y.setValue(box2.Placement.Base[1] / DIVIDER)
        self.box_limitmax_pointini_input_z.setValue(box2.Placement.Base[2] / DIVIDER)
        self.box_limitmax_pointend_input_x.setValue((box2.Placement.Base[0] + box2.Length.Value) / DIVIDER)
        self.box_limitmax_pointend_input_y.setValue((box2.Placement.Base[0] + box2.Width.Value) / DIVIDER)
        self.box_limitmax_pointend_input_z.setValue((box2.Placement.Base[0] + box2.Height.Value) / DIVIDER)


    # Window logic
    def on_ok(self):
        """ Saves damping zone data to the data structure. """
        super().on_ok()
        box1 = self.group.OutList[0]
        box2 = self.group.OutList[1]
        fp = self.damping.damping_directions
        if self.all_directions.isChecked():
            fp.all_faces = True
        else:
            fp.front_face = self.front_direction.isChecked()
            fp.back_face = self.back_direction.isChecked()
            fp.top_face = self.top_direction.isChecked()
            fp.bottom_face = self.bottom_direction.isChecked()
            fp.left_face = self.left_direction.isChecked()
            fp.right_face = self.right_direction.isChecked()
        fp.build_face_print()



        box1.Placement.Base = (self.box_limitmin_pointini_input_x.value() * DIVIDER,
                               self.box_limitmin_pointini_input_y.value() * DIVIDER,
                               self.box_limitmin_pointini_input_z.value() * DIVIDER)
        box1.Length = (self.box_limitmin_pointend_input_x.value() -
            self.box_limitmin_pointini_input_x.value()) * DIVIDER
        box1.Width = (self.box_limitmin_pointend_input_y.value() -
            self.box_limitmin_pointini_input_y.value()) * DIVIDER
        box1.Height = (self.box_limitmin_pointend_input_z.value() -
            self.box_limitmin_pointini_input_z.value()) * DIVIDER
        box2.Placement.Base = (self.box_limitmax_pointini_input_x.value() * DIVIDER,
                               self.box_limitmax_pointini_input_y.value() * DIVIDER,
                               self.box_limitmax_pointini_input_z.value() * DIVIDER)
        box2.Length = (self.box_limitmax_pointend_input_x.value() -
            self.box_limitmax_pointini_input_x.value()) * DIVIDER
        box2.Width = (self.box_limitmax_pointend_input_y.value() -
            self.box_limitmax_pointini_input_y.value()) * DIVIDER
        box2.Height = (self.box_limitmax_pointend_input_z.value() -
            self.box_limitmax_pointini_input_z.value()) * DIVIDER

        FreeCAD.ActiveDocument.recompute()
        self.accept()


    def on_directions_checkbox(self):
        """ Checks the directions state """
        if self.all_directions.isChecked():
            self.front_direction.setEnabled(False)
            self.back_direction.setEnabled(False)
            self.top_direction.setEnabled(False)
            self.bottom_direction.setEnabled(False)
            self.left_direction.setEnabled(False)
            self.right_direction.setEnabled(False)
        else:
            self.front_direction.setEnabled(True)
            self.back_direction.setEnabled(True)
            self.top_direction.setEnabled(True)
            self.bottom_direction.setEnabled(True)
            self.left_direction.setEnabled(True)
            self.right_direction.setEnabled(True)