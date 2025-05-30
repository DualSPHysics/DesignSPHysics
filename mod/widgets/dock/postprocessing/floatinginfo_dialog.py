#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics FloatingInfo configuration and execution Dialog."""

from PySide2 import QtWidgets
from mod.dataobjects.case import Case, mk_help_list
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.post_processing_tools import floatinginfo_export
from mod.tools.translation_tools import __
from mod.widgets.dock.postprocessing.mk_helper_widget import MkHelperWidget


class FloatingInfoDialog(QtWidgets.QDialog):
    """ FloatingInfo configuration and execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("FloatingInfo Tool"))
        self.floatinfo_tool_layout = QtWidgets.QVBoxLayout()

        self.finfo_onlyprocess_layout = QtWidgets.QHBoxLayout()
        self.finfo_filename_layout = QtWidgets.QHBoxLayout()
        self.finfo_additional_parameters_layout = QtWidgets.QHBoxLayout()
        self.finfo_mk_help_list_button_layout = QtWidgets.QHBoxLayout()
        self.finfo_mk_help_list_layout = QtWidgets.QHBoxLayout()
        self.finfo_buttons_layout = QtWidgets.QHBoxLayout()

        self.finfo_onlyprocess_label = QtWidgets.QLabel(__("MK to process (empty for all)"))
        self.finfo_onlyprocess_text = QtWidgets.QLineEdit()
        self.finfo_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        self.finfo_onlyprocess_layout.addWidget(self.finfo_onlyprocess_label)
        self.finfo_onlyprocess_layout.addWidget(self.finfo_onlyprocess_text)

        self.finfo_filename_label = QtWidgets.QLabel(__("File Name"))
        self.finfo_filename_text = QtWidgets.QLineEdit()
        self.finfo_filename_text.setText("FloatingMotion")
        self.finfo_filename_layout.addWidget(self.finfo_filename_label)
        self.finfo_filename_layout.addWidget(self.finfo_filename_text)

        self.finfo_additional_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.finfo_additional_parameters_text = QtWidgets.QLineEdit()
        self.finfo_additional_parameters_layout.addWidget(self.finfo_additional_parameters_label)
        self.finfo_additional_parameters_layout.addWidget(self.finfo_additional_parameters_text)


        self.finfo_mk_help_list_widget=MkHelperWidget()
        self.finfo_mk_help_list_layout.addWidget(self.finfo_mk_help_list_widget)

        self.finfo_export_button = QtWidgets.QPushButton(__("Export"))
        self.finfo_generate_script_button = QtWidgets.QPushButton(__("Generate script"))
        self.finfo_cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.finfo_buttons_layout.addWidget(self.finfo_export_button)
        if not ApplicationSettings.the().basic_visualization:
            self.finfo_buttons_layout.addWidget(self.finfo_generate_script_button)
        self.finfo_buttons_layout.addWidget(self.finfo_cancel_button)

        self.floatinfo_tool_layout.addLayout(self.finfo_onlyprocess_layout)
        self.floatinfo_tool_layout.addLayout(self.finfo_filename_layout)
        self.floatinfo_tool_layout.addLayout(self.finfo_additional_parameters_layout)
        self.floatinfo_tool_layout.addLayout(self.finfo_mk_help_list_button_layout)
        self.floatinfo_tool_layout.addLayout(self.finfo_mk_help_list_layout)
        self.floatinfo_tool_layout.addStretch(1)
        
        self.floatinfo_tool_layout.addLayout(self.finfo_buttons_layout)
        self.floatinfo_tool_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.setLayout(self.floatinfo_tool_layout)

        self.finfo_export_button.clicked.connect(self.on_finfo_local_run)
        self.finfo_generate_script_button.clicked.connect(self.on_finfo_generate_script)
        self.finfo_cancel_button.clicked.connect(self.on_finfo_cancel)
        self.finfo_filename_text.setFocus()
        self.exec_()

    def on_finfo_cancel(self):
        """ Cancel button behaviour."""
        self.reject()

    def on_finfo_local_run(self):
        self.on_finfo_export(False)

    def on_finfo_generate_script(self):
        self.on_finfo_export(True)

    def on_finfo_export(self,generate_script):
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters["onlyprocess"] = self.finfo_onlyprocess_text.text()
        export_parameters["filename"] = self.finfo_filename_text.text()
        export_parameters["additional_parameters"] = self.finfo_additional_parameters_text.text()

        floatinginfo_export(export_parameters, Case.the(), self.post_processing_widget,generate_script)

        self.accept()
        
    def on_help_list(self):
        info = mk_help_list()
        self.finfo_mk_help_list_label.setText(info)
