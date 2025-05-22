#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics IsoSurface Config and Execution Dialog."""

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case, mk_help_list
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.post_processing_tools import isosurface_export
from mod.tools.translation_tools import __
from mod.widgets.dock.postprocessing.mk_helper_widget import MkHelperWidget


class IsoSurfaceDialog(QtWidgets.QDialog):
    """ DesignSPHysics IsoSurface Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_procesing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("IsoSurface Tool"))
        self.isosurface_tool_layout = QtWidgets.QVBoxLayout()

        self.isosfc_selector_layout = QtWidgets.QHBoxLayout()
        self.isosfc_onlyMK_layout = QtWidgets.QHBoxLayout()
        self.isosfc_onlypos_layout = QtWidgets.QHBoxLayout()
        self.isosfc_onlytype_groupbox = QtWidgets.QGroupBox(__("Types to process"))
        self.isosfc_filename_layout = QtWidgets.QHBoxLayout()
        self.isosfc_parameters_layout = QtWidgets.QHBoxLayout()
        self.isosfc_mk_help_list_button_layout = QtWidgets.QHBoxLayout()
        self.isosfc_mk_help_list_layout = QtWidgets.QHBoxLayout()
        self.isosfc_buttons_layout = QtWidgets.QHBoxLayout()

        
        self.isosfc_selector_label = QtWidgets.QLabel(__("Save: "))
        self.isosfc_selector = QtWidgets.QComboBox()
        self.isosfc_selector.insertItems(0, ["Surface", "Slice"])
        self.isosfc_selector_layout.addWidget(self.isosfc_selector_label)
        self.isosfc_selector_layout.addWidget(self.isosfc_selector)

        self.isosfc_onlyMK_label = QtWidgets.QLabel(__("MKs to process (empty for all)"))
        self.isosfc_onlyMK_text = QtWidgets.QLineEdit()
        self.isosfc_onlyMK_text.setPlaceholderText("1,2,3 or 1-30")
        self.isosfc_onlyMK_layout.addWidget(self.isosfc_onlyMK_label)
        self.isosfc_onlyMK_layout.addWidget(self.isosfc_onlyMK_text)

        self.isosfc_onlypos_label = QtWidgets.QLabel(__("pos to process (empty for all)"))
        self.isosfc_onlypos_text = QtWidgets.QLineEdit()
        self.isosfc_onlypos_text.setPlaceholderText("xmin:ymin:zmin:xmax:ymax:zmax (m)")
        self.isosfc_onlypos_layout.addWidget(self.isosfc_onlypos_label)
        self.isosfc_onlypos_layout.addWidget(self.isosfc_onlypos_text)
        

        self.isosfc_types_groupbox_layout = QtWidgets.QVBoxLayout()
        self.isosfc_types_chk_all = QtWidgets.QCheckBox(__("All"))
        self.isosfc_types_chk_all.setCheckState(QtCore.Qt.Checked)
        self.isosfc_types_chk_bound = QtWidgets.QCheckBox(__("Bound"))
        self.isosfc_types_chk_fluid = QtWidgets.QCheckBox(__("Fluid"))
        self.isosfc_types_chk_fixed = QtWidgets.QCheckBox(__("Fixed"))
        self.isosfc_types_chk_moving = QtWidgets.QCheckBox(__("Moving"))
        self.isosfc_types_chk_floating = QtWidgets.QCheckBox(__("Floating"))
        for x in [self.isosfc_types_chk_all,
                  self.isosfc_types_chk_bound,
                  self.isosfc_types_chk_fluid,
                  self.isosfc_types_chk_fixed,
                  self.isosfc_types_chk_moving,
                  self.isosfc_types_chk_floating]:
            self.isosfc_types_groupbox_layout.addWidget(x)

        self.isosfc_onlytype_groupbox.setLayout(self.isosfc_types_groupbox_layout)

        self.isosfc_file_name_label = QtWidgets.QLabel(__("File name"))
        self.isosfc_file_name_text = QtWidgets.QLineEdit()
        self.isosfc_file_name_text.setText("FileIso")
        self.isosfc_filename_layout.addWidget(self.isosfc_file_name_label)
        self.isosfc_filename_layout.addWidget(self.isosfc_file_name_text)

        self.isosfc_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.isosfc_parameters_text = QtWidgets.QLineEdit()
        self.isosfc_parameters_layout.addWidget(self.isosfc_parameters_label)
        self.isosfc_parameters_layout.addWidget(self.isosfc_parameters_text)

        self.isosfc_mk_help_list_widget=MkHelperWidget()
        self.isosfc_mk_help_list_layout.addWidget(self.isosfc_mk_help_list_widget)

        self.isosfc_open_at_end = QtWidgets.QCheckBox("Open with ParaView (only local)")
        self.isosfc_open_at_end.setEnabled(Case.the().executable_paths.paraview != "")

        self.isosfc_export_button = QtWidgets.QPushButton(__("Export"))
        self.isosfc_generate_script_button = QtWidgets.QPushButton(__("Generate script"))
        self.isosfc_cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.isosfc_buttons_layout.addWidget(self.isosfc_export_button)
        if not ApplicationSettings.the().basic_visualization:
            self.isosfc_buttons_layout.addWidget(self.isosfc_generate_script_button)
        self.isosfc_buttons_layout.addWidget(self.isosfc_cancel_button)

        self.isosurface_tool_layout.addLayout(self.isosfc_selector_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_onlyMK_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_onlypos_layout)
        self.isosurface_tool_layout.addWidget(self.isosfc_onlytype_groupbox)
        self.isosurface_tool_layout.addLayout(self.isosfc_filename_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_parameters_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_mk_help_list_button_layout)
        self.isosurface_tool_layout.addLayout(self.isosfc_mk_help_list_layout)

        self.isosurface_tool_layout.addWidget(self.isosfc_open_at_end)
        self.isosurface_tool_layout.addStretch(1)
        self.isosurface_tool_layout.addLayout(self.isosfc_buttons_layout)
        self.isosurface_tool_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.setLayout(self.isosurface_tool_layout)

        self.isosfc_types_chk_all.stateChanged.connect(self.on_isosfc_type_all_change)
        self.isosfc_types_chk_bound.stateChanged.connect(self.on_isosfc_type_any_change)
        self.isosfc_types_chk_fluid.stateChanged.connect(self.on_isosfc_type_any_change)
        self.isosfc_types_chk_fixed.stateChanged.connect(self.on_isosfc_type_any_change)
        self.isosfc_types_chk_moving.stateChanged.connect(self.on_isosfc_type_any_change)
        self.isosfc_types_chk_floating.stateChanged.connect(self.on_isosfc_type_any_change)

        self.isosfc_export_button.clicked.connect(self.on_isosfc_local_run)

        self.isosfc_generate_script_button.clicked.connect(self.on_isosfc_generate_script)
        self.isosfc_cancel_button.clicked.connect(self.on_isosfc_cancel)
        self.exec_()

    def on_isosfc_cancel(self):
        """ IsoSurface dialog cancel button behaviour."""
        self.reject()

    def on_isosfc_type_all_change(self,state):
        if state == QtCore.Qt.Checked:
            for chk in [self.isosfc_types_chk_bound,
                        self.isosfc_types_chk_fluid,
                        self.isosfc_types_chk_fixed,
                        self.isosfc_types_chk_moving,
                        self.isosfc_types_chk_floating]:
                chk.setCheckState(QtCore.Qt.Unchecked)

    def on_isosfc_type_any_change(self, state):
        if state == QtCore.Qt.Checked:
            self.isosfc_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_isosfc_local_run(self):
        self.on_isosfc_export(False)
    def on_isosfc_generate_script(self):
        self.on_isosfc_export(True)

    def on_isosfc_export(self,generate_script:bool):
        """ IsoSurface dialog export button behaviour."""
        export_parameters = dict()

        if "surface" in self.isosfc_selector.currentText().lower():
            export_parameters["surface_or_slice"] = "-saveiso"
        else:
            export_parameters["surface_or_slice"] = "-saveslice"

        export_parameters["-onlymk"] = self.isosfc_onlyMK_text.text()
        export_parameters["-onlypos"] = self.isosfc_onlypos_text.text()

        export_parameters["save_types"] = "-all"

        if self.isosfc_types_chk_all.isChecked():
            export_parameters["save_types"] = "+all"
        else:
            if self.isosfc_types_chk_bound.isChecked():
                export_parameters["save_types"] += ",+bound"
            if self.isosfc_types_chk_fluid.isChecked():
                export_parameters["save_types"] += ",+fluid"
            if self.isosfc_types_chk_fixed.isChecked():
                export_parameters["save_types"] += ",+fixed"
            if self.isosfc_types_chk_moving.isChecked():
                export_parameters["save_types"] += ",+moving"
            if self.isosfc_types_chk_floating.isChecked():
                export_parameters["save_types"] += ",+floating"

        if export_parameters["save_types"] == "-all":
            export_parameters["save_types"] = "+all"

        if self.isosfc_file_name_text.text():
            export_parameters["file_name"] = self.isosfc_file_name_text.text()
        else:
            export_parameters["file_name"] = "IsoFile"

        
        if self.isosfc_parameters_text.text():
            export_parameters["additional_parameters"] = self.isosfc_parameters_text.text()
        else:
            export_parameters["additional_parameters"] = ""

        export_parameters["open_paraview"] = self.isosfc_open_at_end.isChecked()

        #log(export_parameters)
        isosurface_export(export_parameters, Case.the(), self.post_procesing_widget,generate_script)
        self.accept()

    def on_help_list(self):
        info = mk_help_list()
        self.isosfc_mk_help_list_label.setText(info)