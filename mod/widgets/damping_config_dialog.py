#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Damping Configutarion Dialog"""

import FreeCAD
from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.dialog_tools import error_dialog

from mod.constants import DIVIDER


class DampingConfigDialog(QtGui.QDialog):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    def __init__(self, object_key, case, parent=None):
        super().__init__(parent=parent)

        self.case = case
        self.object_key = object_key

        # Creates a dialog and 2 main buttons
        self.setWindowTitle("Damping configuration")
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")

        self.main_layout = QtGui.QVBoxLayout()

        self.enabled_checkbox = QtGui.QCheckBox("Enabled")

        self.main_groupbox = QtGui.QGroupBox("Damping parameters")
        self.main_groupbox_layout = QtGui.QVBoxLayout()

        self.limitmin_layout = QtGui.QHBoxLayout()
        self.limitmin_label = QtGui.QLabel("Limit Min. (X, Y, Z) (m): ")
        self.limitmin_input_x = QtGui.QLineEdit()
        self.limitmin_input_y = QtGui.QLineEdit()
        self.limitmin_input_z = QtGui.QLineEdit()
        self.limitmin_layout.addWidget(self.limitmin_label)
        self.limitmin_layout.addWidget(self.limitmin_input_x)
        self.limitmin_layout.addWidget(self.limitmin_input_y)
        self.limitmin_layout.addWidget(self.limitmin_input_z)

        self.limitmax_layout = QtGui.QHBoxLayout()
        self.limitmax_label = QtGui.QLabel("Limit Max. (X, Y, Z) (m): ")
        self.limitmax_input_x = QtGui.QLineEdit()
        self.limitmax_input_y = QtGui.QLineEdit()
        self.limitmax_input_z = QtGui.QLineEdit()
        self.limitmax_layout.addWidget(self.limitmax_label)
        self.limitmax_layout.addWidget(self.limitmax_input_x)
        self.limitmax_layout.addWidget(self.limitmax_input_y)
        self.limitmax_layout.addWidget(self.limitmax_input_z)

        self.overlimit_layout = QtGui.QHBoxLayout()
        self.overlimit_label = QtGui.QLabel("Overlimit (m): ")
        self.overlimit_input = QtGui.QLineEdit()
        self.overlimit_layout.addWidget(self.overlimit_label)
        self.overlimit_layout.addWidget(self.overlimit_input)

        self.redumax_layout = QtGui.QHBoxLayout()
        self.redumax_label = QtGui.QLabel("Redumax: ")
        self.redumax_input = QtGui.QLineEdit()
        self.redumax_layout.addWidget(self.redumax_label)
        self.redumax_layout.addWidget(self.redumax_input)

        self.main_groupbox_layout.addLayout(self.limitmin_layout)
        self.main_groupbox_layout.addLayout(self.limitmax_layout)
        self.main_groupbox_layout.addLayout(self.overlimit_layout)
        self.main_groupbox_layout.addLayout(self.redumax_layout)

        self.main_groupbox.setLayout(self.main_groupbox_layout)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout.addWidget(self.enabled_checkbox)
        self.main_layout.addWidget(self.main_groupbox)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.enabled_checkbox.stateChanged.connect(self.on_enable_chk)
        self.overlimit_input.textChanged.connect(self.on_value_change)
        self.redumax_input.textChanged.connect(self.on_value_change)

        # Fill fields with case data
        self.enabled_checkbox.setChecked(self.case.get_damping_zone(self.object_key).enabled)
        self.group = FreeCAD.ActiveDocument.getObject(self.object_key)
        self.limitmin_input_x.setText(str(self.group.OutList[0].Start[0] / DIVIDER))
        self.limitmin_input_y.setText(str(self.group.OutList[0].Start[1] / DIVIDER))
        self.limitmin_input_z.setText(str(self.group.OutList[0].Start[2] / DIVIDER))
        self.limitmax_input_x.setText(str(self.group.OutList[0].End[0] / DIVIDER))
        self.limitmax_input_y.setText(str(self.group.OutList[0].End[1] / DIVIDER))
        self.limitmax_input_z.setText(str(self.group.OutList[0].End[2] / DIVIDER))
        self.overlimit_input.setText(str(self.case.get_damping_zone(self.object_key).overlimit))
        self.redumax_input.setText(str(self.case.get_damping_zone(self.object_key).redumax))
        self.redumax_input.setText(str(self.case.get_damping_zone(self.object_key).redumax))
        self.on_enable_chk(QtCore.Qt.Checked if self.case.get_damping_zone(self.object_key).enabled else QtCore.Qt.Unchecked)

        self.exec_()

    # Window logic
    def on_ok(self):
        """ Saves damping zone data to the data structure. """
        self.case.get_damping_zone(self.object_key).enabled = self.enabled_checkbox.isChecked()
        self.case.get_damping_zone(self.object_key).overlimit = float(self.overlimit_input.text())
        self.case.get_damping_zone(self.object_key).redumax = float(self.redumax_input.text())
        damping_group = FreeCAD.ActiveDocument.getObject(self.object_key)
        damping_group.OutList[0].Start = (float(self.limitmin_input_x.text()) * DIVIDER,
                                          float(self.limitmin_input_y.text()) * DIVIDER,
                                          float(self.limitmin_input_z.text()) * DIVIDER)
        damping_group.OutList[0].End = (float(self.limitmax_input_x.text()) * DIVIDER,
                                        float(self.limitmax_input_y.text()) * DIVIDER,
                                        float(self.limitmax_input_z.text()) * DIVIDER)
        damping_group.OutList[1].Start = damping_group.OutList[0].End

        overlimit_vector = FreeCAD.Vector(*damping_group.OutList[0].End) - FreeCAD.Vector(*damping_group.OutList[0].Start)
        try:
            overlimit_vector.normalize()
        except FreeCAD.Base.FreeCADError:
            error_dialog(__("The vector between minimum and maximum limit must have length."))

        overlimit_vector = overlimit_vector * (self.case.get_damping_zone(self.object_key).overlimit * DIVIDER)
        overlimit_vector = overlimit_vector + FreeCAD.Vector(*damping_group.OutList[0].End)

        damping_group.OutList[1].End = (overlimit_vector.x, overlimit_vector.y, overlimit_vector.z)
        FreeCAD.ActiveDocument.recompute()
        self.accept()

    def on_cancel(self):
        """ Closes the window with a rejection when cancel is pressed. """
        self.reject()

    def on_enable_chk(self, state):
        """ Reacts to the enable checkbox enabling the main group of the window. """
        if state == QtCore.Qt.Checked:
            self.main_groupbox.setEnabled(True)
        else:
            self.main_groupbox.setEnabled(False)

    def on_value_change(self):
        """ Reacts to a value change and reformats wrong introduced and invalid characters. """
        for x in [self.overlimit_input, self.redumax_input, self.limitmin_input_x, self.limitmin_input_y, self.limitmin_input_z, self.limitmax_input_x, self.limitmax_input_y, self.limitmax_input_z]:
            x.setText(x.text().replace(",", "."))
