#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics IsoSurface Config and Execution Dialog."""

# from PySide import QtGui
from PySide6 import QtWidgets

from mod.translation_tools import __
from mod.post_processing_tools import isosurface_export

from mod.dataobjects.case import Case


class IsoSurfaceDialog(QtWidgets.QDialog):
    """ DesignSPHysics IsoSurface Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_procesing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("IsoSurface Tool"))
        self.isosurface_tool_layout = QtWidgets.QVBoxLayout()

        self.isosfc_filename_layout = QtWidgets.QHBoxLayout()
        self.isosfc_parameters_layout = QtWidgets.QHBoxLayout()
        self.isosfc_buttons_layout = QtWidgets.QHBoxLayout()

        self.isosfc_selector_layout = QtWidgets.QHBoxLayout()
        self.isosfc_selector_label = QtWidgets.QLabel(__("Save: "))
        self.isosfc_selector = QtWidgets.QComboBox()
        self.isosfc_selector.insertItems(0, ["Surface", "Slice"])
        self.isosfc_selector_layout.addWidget(self.isosfc_selector_label)
        self.isosfc_selector_layout.addWidget(self.isosfc_selector)

        self.isosfc_file_name_label = QtWidgets.QLabel(__("File name"))
        self.isosfc_file_name_text = QtWidgets.QLineEdit()
        self.isosfc_file_name_text.setText("FileIso")
        self.isosfc_filename_layout.addWidget(self.isosfc_file_name_label)
        self.isosfc_filename_layout.addWidget(self.isosfc_file_name_text)

        self.isosfc_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.isosfc_parameters_text = QtWidgets.QLineEdit()
        self.isosfc_parameters_layout.addWidget(self.isosfc_parameters_label)
        self.isosfc_parameters_layout.addWidget(self.isosfc_parameters_text)

        self.isosfc_open_at_end = QtWidgets.QCheckBox("Open with ParaView")
        self.isosfc_open_at_end.setEnabled(Case.the().executable_paths.paraview != "")

        self.isosfc_export_button = QtWidgets.QPushButton(__("Export"))
        self.isosfc_cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.isosfc_buttons_layout.addWidget(self.isosfc_export_button)
        self.isosfc_buttons_layout.addWidget(self.isosfc_cancel_button)

        self.isosurface_tool_layout.addLayout(self.isosfc_selector_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_filename_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_parameters_layout)
        self.isosurface_tool_layout.addWidget(self.isosfc_open_at_end)
        self.isosurface_tool_layout.addStretch(1)
        self.isosurface_tool_layout.addLayout(self.isosfc_buttons_layout)

        self.setLayout(self.isosurface_tool_layout)

        self.isosfc_export_button.clicked.connect(self.on_isosfc_export)
        self.isosfc_cancel_button.clicked.connect(self.on_isosfc_cancel)
        self.exec_()

    def on_isosfc_cancel(self):
        """ IsoSurface dialog cancel button behaviour."""
        self.reject()

    def on_isosfc_export(self):
        """ IsoSurface dialog export button behaviour."""
        export_parameters = dict()

        if "surface" in self.isosfc_selector.currentText().lower():
            export_parameters["surface_or_slice"] = "-saveiso"
        else:
            export_parameters["surface_or_slice"] = "-saveslice"

        if self.isosfc_file_name_text.text():
            export_parameters["file_name"] = self.isosfc_file_name_text.text()
        else:
            export_parameters["file_name"] = "IsoFile"

        if self.isosfc_parameters_text.text():
            export_parameters["additional_parameters"] = self.isosfc_parameters_text.text()
        else:
            export_parameters["additional_parameters"] = ""

        export_parameters["open_paraview"] = self.isosfc_open_at_end.isChecked()

        isosurface_export(export_parameters, Case.the(), self.post_procesing_widget)
        self.accept()
