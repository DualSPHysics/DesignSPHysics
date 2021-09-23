#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics ComputeForces Config and Execution Dialog."""

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.post_processing_tools import measuretool_export
from mod.freecad_tools import get_fc_main_window
from mod.dialog_tools import error_dialog

from mod.dataobjects.case import Case

from mod.widgets.postprocessing.measuretool_grid_dialog import MeasureToolGridDialog
from mod.widgets.postprocessing.measuretool_points_dialog import MeasureToolPointsDialog


class MeasureToolDialog(QtGui.QDialog):
    """ DesignSPHysics ComputeForces Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("MeasureTool"))
        self.measuretool_tool_layout = QtGui.QVBoxLayout()

        self.mtool_format_layout = QtGui.QHBoxLayout()
        self.mtool_types_groupbox = QtGui.QGroupBox(__("Variables to export"))
        self.mtool_filename_layout = QtGui.QHBoxLayout()
        self.mtool_parameters_layout = QtGui.QHBoxLayout()
        self.mtool_buttons_layout = QtGui.QHBoxLayout()

        self.outformat_label = QtGui.QLabel(__("Output format"))
        self.outformat_combobox = QtGui.QComboBox()
        self.outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
        self.outformat_combobox.setCurrentIndex(1)
        self.mtool_format_layout.addWidget(self.outformat_label)
        self.mtool_format_layout.addStretch(1)
        self.mtool_format_layout.addWidget(self.outformat_combobox)

        self.mtool_types_groupbox_layout = QtGui.QVBoxLayout()
        self.mtool_types_chk_all = QtGui.QCheckBox(__("All"))
        self.mtool_types_chk_all.setCheckState(QtCore.Qt.Checked)
        self.mtool_types_chk_vel = QtGui.QCheckBox(__("Velocity"))
        self.mtool_types_chk_rhop = QtGui.QCheckBox(__("Density"))
        self.mtool_types_chk_press = QtGui.QCheckBox(__("Pressure"))
        self.mtool_types_chk_mass = QtGui.QCheckBox(__("Mass"))
        self.mtool_types_chk_vol = QtGui.QCheckBox(__("Volume"))
        self.mtool_types_chk_idp = QtGui.QCheckBox(__("Particle ID"))
        self.mtool_types_chk_ace = QtGui.QCheckBox(__("Acceleration"))
        self.mtool_types_chk_vor = QtGui.QCheckBox(__("Vorticity"))
        self.mtool_types_chk_kcorr = QtGui.QCheckBox(__("KCorr"))
        for x in [self.mtool_types_chk_all,
                  self.mtool_types_chk_vel,
                  self.mtool_types_chk_rhop,
                  self.mtool_types_chk_press,
                  self.mtool_types_chk_mass,
                  self.mtool_types_chk_vol,
                  self.mtool_types_chk_idp,
                  self.mtool_types_chk_ace,
                  self.mtool_types_chk_vor,
                  self.mtool_types_chk_kcorr]:
            self.mtool_types_groupbox_layout.addWidget(x)

        self.mtool_types_groupbox.setLayout(self.mtool_types_groupbox_layout)

        self.mtool_calculate_elevation = QtGui.QCheckBox(__("Calculate water elevation"))

        self.mtool_set_points_layout = QtGui.QHBoxLayout()
        self.mtool_set_points = QtGui.QPushButton("List of points")
        self.mtool_set_grid = QtGui.QPushButton("Grid of points")
        self.mtool_set_points_layout.addWidget(self.mtool_set_points)
        self.mtool_set_points_layout.addWidget(self.mtool_set_grid)

        self.mtool_file_name_label = QtGui.QLabel(__("File name"))
        self.mtool_file_name_text = QtGui.QLineEdit()
        self.mtool_file_name_text.setText("MeasurePart")
        self.mtool_filename_layout.addWidget(self.mtool_file_name_label)
        self.mtool_filename_layout.addWidget(self.mtool_file_name_text)

        self.mtool_parameters_label = QtGui.QLabel(__("Additional Parameters"))
        self.mtool_parameters_text = QtGui.QLineEdit()
        self.mtool_parameters_layout.addWidget(self.mtool_parameters_label)
        self.mtool_parameters_layout.addWidget(self.mtool_parameters_text)

        self.mtool_export_button = QtGui.QPushButton(__("Export"))
        self.mtool_cancel_button = QtGui.QPushButton(__("Cancel"))
        self.mtool_buttons_layout.addWidget(self.mtool_export_button)
        self.mtool_buttons_layout.addWidget(self.mtool_cancel_button)

        self.measuretool_tool_layout.addLayout(self.mtool_format_layout)
        self.measuretool_tool_layout.addWidget(self.mtool_types_groupbox)
        self.measuretool_tool_layout.addStretch(1)
        self.measuretool_tool_layout.addWidget(self.mtool_calculate_elevation)
        self.measuretool_tool_layout.addLayout(self.mtool_set_points_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_filename_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_parameters_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_buttons_layout)

        self.setLayout(self.measuretool_tool_layout)

        self.mtool_types_chk_all.stateChanged.connect(self.on_mtool_measure_all_change)
        self.mtool_types_chk_vel.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_rhop.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_press.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_mass.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_vol.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_idp.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_ace.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_vor.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_types_chk_kcorr.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_set_points.clicked.connect(self.on_mtool_set_points)
        self.mtool_set_grid.clicked.connect(self.on_mtool_set_grid)
        self.mtool_export_button.clicked.connect(self.on_mtool_export)
        self.mtool_cancel_button.clicked.connect(self.on_mtool_cancel)
        self.exec_()

    def on_mtool_cancel(self):
        """ Cancel button behaviour."""
        self.reject()

    def on_mtool_export(self):
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters["save_mode"] = self.outformat_combobox.currentIndex()
        export_parameters["save_vars"] = "-all"
        if self.mtool_types_chk_all.isChecked():
            export_parameters["save_vars"] = "+all"
        else:
            if self.mtool_types_chk_vel.isChecked():
                export_parameters["save_vars"] += ",+vel"
            if self.mtool_types_chk_rhop.isChecked():
                export_parameters["save_vars"] += ",+rhop"
            if self.mtool_types_chk_press.isChecked():
                export_parameters["save_vars"] += ",+press"
            if self.mtool_types_chk_mass.isChecked():
                export_parameters["save_vars"] += ",+mass"
            if self.mtool_types_chk_vol.isChecked():
                export_parameters["save_vars"] += ",+vol"
            if self.mtool_types_chk_idp.isChecked():
                export_parameters["save_vars"] += ",+idp"
            if self.mtool_types_chk_ace.isChecked():
                export_parameters["save_vars"] += ",+ace"
            if self.mtool_types_chk_vor.isChecked():
                export_parameters["save_vars"] += ",+vor"
            if self.mtool_types_chk_kcorr.isChecked():
                export_parameters["save_vars"] += ",+kcorr"

        if export_parameters["save_vars"] == "-all" and not self.mtool_calculate_elevation.isChecked():
            export_parameters["save_vars"] = "+all"

        export_parameters["calculate_water_elevation"] = self.mtool_calculate_elevation.isChecked()

        if self.mtool_file_name_text.text():
            export_parameters["filename"] = self.mtool_file_name_text.text()
        else:
            export_parameters["filename"] = "MeasurePart"

        if self.mtool_parameters_text.text():
            export_parameters["additional_parameters"] = self.mtool_parameters_text.text()
        else:
            export_parameters["additional_parameters"] = ""

        if not Case.the().info.measuretool_points and not Case.the().info.measuretool_grid:
            error_dialog(
                __("No points or grid are defined to execute MeasureTool"),
                __("Please define either list of points or a grid of points to continue. MeasureTool won't be executed.")
            )
        else:
            measuretool_export(export_parameters, Case.the(), self.post_processing_widget)
            self.accept()

    def on_mtool_measure_all_change(self, state):
        """ "All" checkbox behaviour"""
        if state == QtCore.Qt.Checked:
            for chk in [self.mtool_types_chk_vel,
                        self.mtool_types_chk_rhop,
                        self.mtool_types_chk_press,
                        self.mtool_types_chk_mass,
                        self.mtool_types_chk_vol,
                        self.mtool_types_chk_idp,
                        self.mtool_types_chk_ace,
                        self.mtool_types_chk_vor,
                        self.mtool_types_chk_kcorr]:
                chk.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_measure_single_change(self, state):
        """ Behaviour for all checkboxes except "All" """
        if state == QtCore.Qt.Checked:
            self.mtool_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_set_points(self):
        """ Point list button behaviour."""
        MeasureToolPointsDialog(parent=get_fc_main_window())

    def on_mtool_set_grid(self):
        """ Spawns a Grid configuration dialog for MeasureTool. """
        MeasureToolGridDialog(parent=get_fc_main_window())
