#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock DP Intro Widget """

from PySide import QtGui

from mod.translation_tools import __

from mod.dataobjects.case import Case


class DockDPWidget(QtGui.QWidget):
    """ DesignSPHysics Dock DP Intro widget. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.dp_label = QtGui.QLabel(__("Inter-particle distance: "))
        self.dp_label.setToolTip(__("Lower DP to have more particles in the case."))

        self.dp_input = QtGui.QLineEdit()
        self.dp_input.setToolTip(__("Lower DP to have more particles in the case."))
        self.dp_validator = QtGui.QDoubleValidator(0.0, 100, 8, self.dp_input)
        self.dp_input.setValidator(self.dp_validator)
        self.dp_input.setMaxLength(10)
        self.dp_input.setText(str(Case.the().dp))
        self.dp_input.textChanged.connect(self.on_dp_changed)

        self.dp_units_label = QtGui.QLabel(" meters")

        self.main_layout.addWidget(self.dp_label)
        self.main_layout.addWidget(self.dp_input)
        self.main_layout.addWidget(self.dp_units_label)

        self.setLayout(self.main_layout)

    def on_dp_changed(self):
        """ DP Introduction. Changes the dp at the moment the user changes the text. """
        Case.the().dp = float(self.dp_input.text())
