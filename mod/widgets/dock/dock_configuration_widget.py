#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Configuration Widget. """

# from PySide import QtGui
from PySide6 import QtWidgets

from mod.translation_tools import __
from mod.freecad_tools import get_fc_main_window

from mod.widgets.constants_dialog import ConstantsDialog
from mod.widgets.setup_plugin_dialog import SetupPluginDialog
from mod.widgets.execution_parameters_dialog import ExecutionParametersDialog

from mod.dataobjects.case import Case


class DockConfigurationWidget(QtWidgets.QWidget):
    """DesignSPHysics Dock Configuration Widget. """

    CASE_TITLE_TEMPLATE = "- <i>{}</i>"

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.case_name = None

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()

        self.title_label = QtWidgets.QLabel("<b>{}</b>".format(__("Configuration")))
        self.title_label.setWordWrap(True)

        self.case_title_label = QtWidgets.QLabel(self.CASE_TITLE_TEMPLATE.format(Case.the().name))
        self.case_title_label.setWordWrap(True)

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.case_title_label)
        self.title_layout.addStretch(1)

        self.constants_button = QtWidgets.QPushButton(__("Define\nConstants"))
        self.constants_button.setToolTip(__("Use this button to define case constants,\nsuch as gravity or fluid reference density."))

        self.setup_button = QtWidgets.QPushButton(__("Setup\nPlugin"))
        self.setup_button.setToolTip(__("Setup of the simulator executables"))

        self.execparams_button = QtWidgets.QPushButton(__("Execution\nParameters"))
        self.execparams_button.setToolTip(__("Change execution parameters, such as\ntime of simulation, viscosity, etc."))

        self.setup_button.clicked.connect(self.on_setup_button_pressed)
        self.execparams_button.clicked.connect(self.on_execparams_button_presed)
        self.constants_button.clicked.connect(self.on_constants_button_pressed)

        self.main_layout.addLayout(self.title_layout)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.constants_button)
        self.button_layout.addWidget(self.execparams_button)
        self.button_layout.addWidget(self.setup_button)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.update_case_name()

    def update_case_name(self, new_name=None):
        """ Reacts to a case name change and shows it in the label layout if its set to something. """
        self.case_name = new_name
        self.case_title_label.setText(self.CASE_TITLE_TEMPLATE.format(self.case_name))
        self.case_title_label.setVisible(bool(self.case_name))

    def on_constants_button_pressed(self):
        """ Opens constant definition window on button click. """
        ConstantsDialog(parent=get_fc_main_window())

    def on_setup_button_pressed(self):
        """ Opens constant definition window on button click. """
        SetupPluginDialog(parent=get_fc_main_window())

    def on_execparams_button_presed(self):
        """ Opens a dialog to tweak the simulation's execution parameters """
        ExecutionParametersDialog(parent=get_fc_main_window())

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
