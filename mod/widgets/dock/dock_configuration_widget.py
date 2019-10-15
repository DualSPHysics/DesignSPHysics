#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Configuration Widget. """

from PySide import QtGui

from mod.translation_tools import __

from mod.widgets.constants_dialog import ConstantsDialog
from mod.widgets.setup_plugin_dialog import SetupPluginDialog
from mod.widgets.execution_parameters_dialog import ExecutionParametersDialog


class DockConfigurationWidget(QtGui.QWidget):
    """DesignSPHysics Dock Configuration Widget. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QtGui.QLabel("<b>{}</b>".format(__("Configuration")))
        self.title_label.setWordWrap(True)

        self.constants_button = QtGui.QPushButton(__("Define\nConstants"))
        self.constants_button.setToolTip(__("Use this button to define case constants,\nsuch as gravity or fluid reference density."))

        self.setup_button = QtGui.QPushButton(__("Setup\nPlugin"))
        self.setup_button.setToolTip(__("Setup of the simulator executables"))

        self.execparams_button = QtGui.QPushButton(__("Execution\nParameters"))
        self.execparams_button.setToolTip(__("Change execution parameters, such as\ntime of simulation, viscosity, etc."))

        self.setup_button.clicked.connect(self.on_setup_button_pressed)
        self.execparams_button.clicked.connect(self.on_execparams_button_presed)
        self.constants_button.clicked.connect(self.on_constants_button_pressed)

        self.main_layout.addWidget(self.title_label)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addWidget(self.constants_button)
        self.button_layout.addWidget(self.execparams_button)
        self.button_layout.addWidget(self.setup_button)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def on_constants_button_pressed(self):
        """ Opens constant definition window on button click. """
        ConstantsDialog(parent=self)

    def on_setup_button_pressed(self):
        """ Opens constant definition window on button click. """
        SetupPluginDialog(parent=self)

    def on_execparams_button_presed(self):
        """ Opens a dialog to tweak the simulation's execution parameters """
        ExecutionParametersDialog(parent=self)

    def adapt_to_no_case(self):
        """ Adapts the contents of the widget to an environment with no opened case. """
        self.setup_button.setEnabled(True)
        for x in [self.execparams_button, self.constants_button]:
            x.setEnabled(False)

    def adapt_to_new_case(self):
        """ Adapts the contents of the widget to an environment with a new case created. """
        self.setup_button.setEnabled(True)
        for x in [self.execparams_button, self.constants_button]:
            x.setEnabled(True)
