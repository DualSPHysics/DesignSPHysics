#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics ComputeForces Config and Execution Dialog."""

from PySide import QtGui

from mod.translation_tools import __
from mod.post_processing_tools import computeforces_export

from mod.dataobjects.case import Case

class ComputeForcesDialog(QtGui.QDialog):
    """ DesignSPHysics ComputeForces Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("ComputeForces Tool"))
        self.compforces_tool_layout = QtGui.QVBoxLayout()

        self.cfces_format_layout = QtGui.QHBoxLayout()
        self.cfces_onlyprocess_layout = QtGui.QHBoxLayout()
        self.cfces_filename_layout = QtGui.QHBoxLayout()
        self.cfces_additional_parameters_layout = QtGui.QHBoxLayout()
        self.cfces_buttons_layout = QtGui.QHBoxLayout()

        self.outformat_label = QtGui.QLabel(__("Output format"))
        self.outformat_combobox = QtGui.QComboBox()
        self.outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
        self.outformat_combobox.setCurrentIndex(1)
        self.cfces_format_layout.addWidget(self.outformat_label)
        self.cfces_format_layout.addStretch(1)
        self.cfces_format_layout.addWidget(self.outformat_combobox)

        self.cfces_onlyprocess_selector = QtGui.QComboBox()
        self.cfces_onlyprocess_selector.insertItems(0, ["MK", "id", "position"])
        self.cfces_onlyprocess_label = QtGui.QLabel(__("to process (empty for all)"))
        self.cfces_onlyprocess_text = QtGui.QLineEdit()
        self.cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        self.cfces_onlyprocess_layout.addWidget(self.cfces_onlyprocess_selector)
        self.cfces_onlyprocess_layout.addWidget(self.cfces_onlyprocess_label)
        self.cfces_onlyprocess_layout.addWidget(self.cfces_onlyprocess_text)

        self.cfces_filename_label = QtGui.QLabel(__("File Name"))
        self.cfces_filename_text = QtGui.QLineEdit()
        self.cfces_filename_text.setText("Force")
        self.cfces_filename_layout.addWidget(self.cfces_filename_label)
        self.cfces_filename_layout.addWidget(self.cfces_filename_text)

        self.cfces_additional_parameters_label = QtGui.QLabel(__("Additional Parameters"))
        self.cfces_additional_parameters_text = QtGui.QLineEdit()
        self.cfces_additional_parameters_layout.addWidget(self.cfces_additional_parameters_label)
        self.cfces_additional_parameters_layout.addWidget(self.cfces_additional_parameters_text)

        self.cfces_export_button = QtGui.QPushButton(__("Export"))
        self.cfces_cancel_button = QtGui.QPushButton(__("Cancel"))
        self.cfces_buttons_layout.addWidget(self.cfces_export_button)
        self.cfces_buttons_layout.addWidget(self.cfces_cancel_button)

        self.compforces_tool_layout.addLayout(self.cfces_format_layout)
        self.compforces_tool_layout.addLayout(self.cfces_onlyprocess_layout)
        self.compforces_tool_layout.addLayout(self.cfces_filename_layout)
        self.compforces_tool_layout.addLayout(self.cfces_additional_parameters_layout)
        self.compforces_tool_layout.addStretch(1)
        self.compforces_tool_layout.addLayout(self.cfces_buttons_layout)

        self.setLayout(self.compforces_tool_layout)

        self.cfces_onlyprocess_selector.currentIndexChanged.connect(self.on_cfces_onlyprocess_changed)
        self.cfces_export_button.clicked.connect(self.on_cfces_export)
        self.cfces_cancel_button.clicked.connect(self.on_cfces_cancel)
        self.exec_()

    def on_cfces_cancel(self):
        """ Cancel button behaviour."""
        self.reject()

    def on_cfces_export(self):
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
        computeforces_export(export_parameters, Case.the(), self.post_processing_widget)
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
