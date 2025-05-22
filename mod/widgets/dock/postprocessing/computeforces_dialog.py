#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics ComputeForces Config and Execution Dialog."""


from PySide2 import QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.post_processing_tools import computeforces_export
from mod.tools.translation_tools import __
from mod.widgets.dock.postprocessing.mk_helper_widget import MkHelperWidget


class ComputeForcesDialog(QtWidgets.QDialog):
    """ DesignSPHysics ComputeForces Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("ComputeForces Tool"))
        self.compforces_tool_layout = QtWidgets.QVBoxLayout()

        self.cfces_format_layout = QtWidgets.QHBoxLayout()
        self.cfces_onlyprocess_layout = QtWidgets.QHBoxLayout()
        self.cfces_filename_layout = QtWidgets.QHBoxLayout()
        self.cfces_additional_parameters_layout = QtWidgets.QHBoxLayout()
        self.cfces_mk_help_list_button_layout = QtWidgets.QHBoxLayout()
        self.cfces_mk_help_list_layout = QtWidgets.QHBoxLayout()
        self.cfces_buttons_layout = QtWidgets.QHBoxLayout()


        self.outformat_label = QtWidgets.QLabel(__("Output format"))
        self.outformat_combobox = QtWidgets.QComboBox()
        self.outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
        self.outformat_combobox.setCurrentIndex(1)
        self.cfces_format_layout.addWidget(self.outformat_label)
        self.cfces_format_layout.addStretch(1)
        self.cfces_format_layout.addWidget(self.outformat_combobox)

        self.cfces_onlyprocess_selector = QtWidgets.QComboBox()
        self.cfces_onlyprocess_selector.insertItems(0, ["MK", "id", "position"])
        self.cfces_onlyprocess_label = QtWidgets.QLabel(__("to process (empty for all)"))
        self.cfces_onlyprocess_text = QtWidgets.QLineEdit()
        self.cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        self.cfces_onlyprocess_layout.addWidget(self.cfces_onlyprocess_selector)
        self.cfces_onlyprocess_layout.addWidget(self.cfces_onlyprocess_label)
        self.cfces_onlyprocess_layout.addWidget(self.cfces_onlyprocess_text)

        self.cfces_filename_label = QtWidgets.QLabel(__("File Name"))
        self.cfces_filename_text = QtWidgets.QLineEdit()
        self.cfces_filename_text.setText("Force")
        self.cfces_filename_layout.addWidget(self.cfces_filename_label)
        self.cfces_filename_layout.addWidget(self.cfces_filename_text)

        self.cfces_additional_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.cfces_additional_parameters_text = QtWidgets.QLineEdit()
        self.cfces_additional_parameters_layout.addWidget(self.cfces_additional_parameters_label)
        self.cfces_additional_parameters_layout.addWidget(self.cfces_additional_parameters_text)

        self.cfces_mk_help_list_widget=MkHelperWidget()
        self.cfces_mk_help_list_layout.addWidget(self.cfces_mk_help_list_widget)

        self.cfces_export_button = QtWidgets.QPushButton(__("Export"))
        self.cfces_generate_script_button = QtWidgets.QPushButton(__("Generate script"))
        self.cfces_cancel_button = QtWidgets.QPushButton(__("Cancel"))

        self.cfces_buttons_layout.addWidget(self.cfces_export_button)
        if not ApplicationSettings.the().basic_visualization:
            self.cfces_buttons_layout.addWidget(self.cfces_generate_script_button)
        self.cfces_buttons_layout.addWidget(self.cfces_cancel_button)

        self.compforces_tool_layout.addLayout(self.cfces_format_layout)
        self.compforces_tool_layout.addLayout(self.cfces_onlyprocess_layout)
        self.compforces_tool_layout.addLayout(self.cfces_filename_layout)
        self.compforces_tool_layout.addLayout(self.cfces_additional_parameters_layout)
        self.compforces_tool_layout.addLayout(self.cfces_mk_help_list_button_layout)
        self.compforces_tool_layout.addLayout(self.cfces_mk_help_list_layout)
        self.compforces_tool_layout.addStretch(1)
        self.compforces_tool_layout.addLayout(self.cfces_buttons_layout)

        self.setLayout(self.compforces_tool_layout)

        self.compforces_tool_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.cfces_onlyprocess_selector.currentIndexChanged.connect(self.on_cfces_onlyprocess_changed)
        self.cfces_export_button.clicked.connect(self.on_cfces_local_run)
        self.cfces_generate_script_button.clicked.connect(self.on_cfces_generate_script)
        self.cfces_cancel_button.clicked.connect(self.on_cfces_cancel)
        self.exec_()

    def on_cfces_cancel(self):
        """ Cancel button behaviour."""
        self.reject()

    def on_cfces_local_run(self):
        self.on_cfces_export(False)

    def on_cfces_generate_script(self):
        self.on_cfces_export(True)

    def on_cfces_export(self,generate_script:bool):
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters["save_mode"] = self.outformat_combobox.currentIndex()

        if "mk" in self.cfces_onlyprocess_selector.currentText().lower():
            export_parameters["onlyprocess_tag"] = "-onlymk:"
        elif "id" in self.cfces_onlyprocess_selector.currentText().lower():
            export_parameters["onlyprocess_tag"] = "-onlyid:"
        elif "position" in self.cfces_onlyprocess_selector.currentText().lower():
            export_parameters["onlyprocess_tag"] = "-onlypos:"

        export_parameters["onlyprocess"] = self.cfces_onlyprocess_text.text()
        export_parameters["filename"] = self.cfces_filename_text.text()
        export_parameters["additional_parameters"] = self.cfces_additional_parameters_text.text()
        computeforces_export(export_parameters, Case.the(), self.post_processing_widget,generate_script)
        self.accept()

    def on_cfces_onlyprocess_changed(self):
        """ Defines behaviour on target property to process change. """
        if "mk" in self.cfces_onlyprocess_selector.currentText().lower():
            self.cfces_onlyprocess_text.setText("")
            self.cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        elif "id" in self.cfces_onlyprocess_selector.currentText().lower():
            self.cfces_onlyprocess_text.setText("")
            self.cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        elif "position" in self.cfces_onlyprocess_selector.currentText().lower():
            self.cfces_onlyprocess_text.setText("")
            self.cfces_onlyprocess_text.setPlaceholderText("xmin:ymin:zmin:xmax:ymax:zmax (m)")



