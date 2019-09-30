#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics FloatingInfo configuration and execution Dialog.'''

from PySide import QtGui

from mod.translation_tools import __


class FloatingInfoDialog(QtGui.QDialog):
    ''' FloatingInfo configuration and execution Dialog. '''

    def __init__(self):
        super().__init__()
        self.setModal(False)
        self.setWindowTitle(__("FloatingInfo Tool"))
        self.floatinfo_tool_layout = QtGui.QVBoxLayout()

        self.finfo_onlyprocess_layout = QtGui.QHBoxLayout()
        self.finfo_filename_layout = QtGui.QHBoxLayout()
        self.finfo_additional_parameters_layout = QtGui.QHBoxLayout()
        self.finfo_buttons_layout = QtGui.QHBoxLayout()

        self.finfo_onlyprocess_label = QtGui.QLabel(__("MK to process (empty for all)"))
        self.finfo_onlyprocess_text = QtGui.QLineEdit()
        self.finfo_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        self.finfo_onlyprocess_layout.addWidget(self.finfo_onlyprocess_label)
        self.finfo_onlyprocess_layout.addWidget(self.finfo_onlyprocess_text)

        self.finfo_filename_label = QtGui.QLabel(__("File Name"))
        self.finfo_filename_text = QtGui.QLineEdit()
        self.finfo_filename_text.setText("FloatingMotion")
        self.finfo_filename_layout.addWidget(self.finfo_filename_label)
        self.finfo_filename_layout.addWidget(self.finfo_filename_text)

        self.finfo_additional_parameters_label = QtGui.QLabel(__("Additional Parameters"))
        self.finfo_additional_parameters_text = QtGui.QLineEdit()
        self.finfo_additional_parameters_layout.addWidget(self.finfo_additional_parameters_label)
        self.finfo_additional_parameters_layout.addWidget(self.finfo_additional_parameters_text)

        self.finfo_export_button = QtGui.QPushButton(__("Export"))
        self.finfo_cancel_button = QtGui.QPushButton(__("Cancel"))
        self.finfo_buttons_layout.addWidget(self.finfo_export_button)
        self.finfo_buttons_layout.addWidget(self.finfo_cancel_button)

        self.floatinfo_tool_layout.addLayout(self.finfo_onlyprocess_layout)
        self.floatinfo_tool_layout.addLayout(self.finfo_filename_layout)
        self.floatinfo_tool_layout.addLayout(self.finfo_additional_parameters_layout)
        self.floatinfo_tool_layout.addStretch(1)
        self.floatinfo_tool_layout.addLayout(self.finfo_buttons_layout)

        self.setLayout(self.floatinfo_tool_layout)

        self.finfo_export_button.clicked.connect(self.on_finfo_export)
        self.finfo_cancel_button.clicked.connect(self.on_finfo_cancel)
        self.finfo_filename_text.setFocus()
        self.exec_()

    def on_finfo_cancel(self):
        ''' Cancel button behaviour.'''
        self.reject()

    def on_finfo_export(self):
        ''' Export button behaviour.'''
        export_parameters = dict()
        export_parameters['onlyprocess'] = self.finfo_onlyprocess_text.text()
        export_parameters['filename'] = self.finfo_filename_text.text()
        export_parameters['additional_parameters'] = self.finfo_additional_parameters_text.text()

        floatinginfo_export(export_parameters)

        self.accept()
