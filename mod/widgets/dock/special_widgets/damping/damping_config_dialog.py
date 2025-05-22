#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Damping Common Configutarion Dialog"""

import FreeCAD

from PySide2 import QtCore, QtWidgets
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class DampingConfigDialog(QtWidgets.QDialog):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    def __init__(self, damping, group, parent=None):
        super().__init__(parent=parent)

        self.damping = damping
        self.group = group
        self.damping_type = damping.damping_type

        # Creates a dialog and 2 main buttons
        self.setWindowTitle("Damping configuration")
        self.ok_button = QtWidgets.QPushButton(__("Save"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))

        self.main_layout = QtWidgets.QVBoxLayout()

        self.enabled_checkbox = QtWidgets.QCheckBox(__("Enabled"))

        self.main_groupbox = QtWidgets.QGroupBox(__("Damping parameters"))
        self.main_groupbox_layout = QtWidgets.QVBoxLayout()

        self.overlimit_layout = QtWidgets.QHBoxLayout()
        self.overlimit_label = QtWidgets.QLabel("Overlimit: ")
        self.overlimit_input = SizeInput()
        self.overlimit_layout.addWidget(self.overlimit_label)
        self.overlimit_layout.addWidget(self.overlimit_input)

        self.redumax_layout = QtWidgets.QHBoxLayout()
        self.redumax_label = QtWidgets.QLabel("Redumax: ")
        self.redumax_input = ValueInput()
        self.redumax_layout.addWidget(self.redumax_label)
        self.redumax_layout.addWidget(self.redumax_input)

        self.factorxyz_layout = QtWidgets.QHBoxLayout()
        self.factorxyz_label = QtWidgets.QLabel("FactorXYZ: (X,Y,Z)")
        self.factorxyz_x_input = ValueInput()
        self.factorxyz_y_input = ValueInput()
        self.factorxyz_z_input = ValueInput()
        self.factorxyz_layout.addWidget(self.factorxyz_label)
        self.factorxyz_layout.addWidget(self.factorxyz_x_input)
        self.factorxyz_layout.addWidget(self.factorxyz_y_input)
        self.factorxyz_layout.addWidget(self.factorxyz_z_input)

        self.main_groupbox_layout.addLayout(self.overlimit_layout)
        self.main_groupbox_layout.addLayout(self.redumax_layout)
        self.main_groupbox_layout.addLayout(self.factorxyz_layout)

        self.main_groupbox.setLayout(self.main_groupbox_layout)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout.addWidget(self.enabled_checkbox)
        self.main_layout.addWidget(self.main_groupbox)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.cancel_button.clicked.connect(self.on_cancel)


    def fill_Values(self):
        # Fill fields with case data

        self.enabled_checkbox.setChecked(self.damping.enabled)
        self.overlimit_input.setValue(self.damping.overlimit)
        self.redumax_input.setValue(self.damping.redumax)
        self.factorxyz_x_input.setValue(self.damping.factorxyz[0])
        self.factorxyz_y_input.setValue(self.damping.factorxyz[1])
        self.factorxyz_z_input.setValue(self.damping.factorxyz[2])
        self.on_enable_chk(QtCore.Qt.Checked if self.damping.enabled else QtCore.Qt.Unchecked)

    # Window logic
    def on_ok(self):
        """ Saves damping zone data to the data structure. """
        self.damping.enabled = self.enabled_checkbox.isChecked()
        self.damping.overlimit = self.overlimit_input.value()
        self.damping.redumax = self.redumax_input.value()
        self.damping.factorxyz[0] = self.factorxyz_x_input.value()
        self.damping.factorxyz[1] = self.factorxyz_y_input.value()
        self.damping.factorxyz[2] = self.factorxyz_z_input.value()
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

