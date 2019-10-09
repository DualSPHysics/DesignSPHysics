#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Additional Parameters Dialog for running configuration. """

from PySide import QtGui

from mod.translation_tools import __


from mod.dataobjects.case import Case


class RunAdditionalParametersDialog(QtGui.QDialog):
    """ A Dialog to introduce text parameters used as additional configuration for running a case simulation. """

    def __init__(self):
        super().__init__()

        self.additional_parameters_window = QtGui.QDialog()
        self.additional_parameters_window.setWindowTitle(__("Additional parameters"))

        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Button layout definition
        self.eo_button_layout = QtGui.QHBoxLayout()
        self.eo_button_layout.addStretch(1)
        self.eo_button_layout.addWidget(self.ok_button)
        self.eo_button_layout.addWidget(self.cancel_button)

        self.paramintro_layout = QtGui.QHBoxLayout()
        self.paramintro_label = QtGui.QLabel(__("Additional Parameters: "))
        self.export_params = QtGui.QLineEdit()
        self.export_params.setText(Case.instance().info.run_additional_parameters)
        self.paramintro_layout.addWidget(self.paramintro_label)
        self.paramintro_layout.addWidget(self.export_params)

        self.additional_parameters_layout = QtGui.QVBoxLayout()
        self.additional_parameters_layout.addLayout(self.paramintro_layout)
        self.additional_parameters_layout.addStretch(1)
        self.additional_parameters_layout.addLayout(self.eo_button_layout)

        self.additional_parameters_window.setLayout(self.additional_parameters_layout)
        self.additional_parameters_window.exec_()

    def on_ok(self):
        """ OK Button handler."""
        Case.instance().info.run_additional_parameters = self.export_params.text()
        self.additional_parameters_window.accept()

    def on_cancel(self):
        """ Cancel button handler."""
        self.additional_parameters_window.reject()
