#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Additional Parameters Dialog for running configuration. """

from PySide2 import QtWidgets

from mod.tools.translation_tools import __


from mod.dataobjects.case import Case


class RunAdditionalParametersDialog(QtWidgets.QDialog):
    """ A Dialog to introduce text parameters used as additional configuration for running a case simulation. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.additional_parameters_window = QtWidgets.QDialog()
        self.additional_parameters_window.setWindowTitle(__("Additional parameters"))

        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Button layout definition
        self.eo_button_layout = QtWidgets.QHBoxLayout()
        self.eo_button_layout.addStretch(1)
        self.eo_button_layout.addWidget(self.ok_button)
        self.eo_button_layout.addWidget(self.cancel_button)

        self.paramintro_layout = QtWidgets.QHBoxLayout()
        self.paramintro_label = QtWidgets.QLabel(__("Additional Parameters: "))
        self.export_params = QtWidgets.QLineEdit()
        self.export_params.setText(Case.the().info.run_additional_parameters)
        self.paramintro_layout.addWidget(self.paramintro_label)
        self.paramintro_layout.addWidget(self.export_params)

        self.additional_parameters_layout = QtWidgets.QVBoxLayout()
        self.additional_parameters_layout.addLayout(self.paramintro_layout)
        self.additional_parameters_layout.addStretch(1)
        self.additional_parameters_layout.addLayout(self.eo_button_layout)

        self.additional_parameters_window.setLayout(self.additional_parameters_layout)
        self.additional_parameters_window.exec_()

    def on_ok(self):
        """ OK Button handler."""
        Case.the().info.run_additional_parameters = self.export_params.text()
        self.additional_parameters_window.accept()

    def on_cancel(self):
        """ Cancel button handler."""
        self.additional_parameters_window.reject()
