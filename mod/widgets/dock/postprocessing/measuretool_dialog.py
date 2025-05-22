#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics ComputeForces Config and Execution Dialog."""

from PySide2 import QtWidgets, QtCore
from mod.constants import MKFLUID_LIMIT
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.enums import ObjectType
from mod.dataobjects.case import Case, mk_help_list
from mod.tools.dialog_tools import error_dialog, info_dialog, warning_dialog
from mod.tools.file_tools import save_measuretool_point_list, save_measuretool_point_grid
from mod.tools.post_processing_tools import measuretool_export
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames
from mod.widgets.dock.postprocessing.measuretool_grid_dialog import MeasureToolGridDialog
from mod.widgets.dock.postprocessing.measuretool_points_dialog import MeasureToolPointsDialog
from mod.widgets.dock.postprocessing.mk_helper_widget import MkHelperWidget


class MeasureToolDialog(QtWidgets.QDialog):
    """ DesignSPHysics ComputeForces Config and Execution Dialog. """

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("MeasureTool"))
        self.measuretool_tool_layout = QtWidgets.QVBoxLayout()

        self.mtool_format_layout = QtWidgets.QHBoxLayout()
        self.mtool_onlyMK_layout = QtWidgets.QHBoxLayout()
        self.mtool_onlyid_layout = QtWidgets.QHBoxLayout()
        self.mtool_onlypos_layout = QtWidgets.QHBoxLayout()
        self.mtool_onlytype_groupbox = QtWidgets.QGroupBox(__("Types to process"))
        self.mtool_variables_groupbox = QtWidgets.QGroupBox(__("Variables to export"))
        self.mtool_filename_layout = QtWidgets.QHBoxLayout()
        self.mtool_parameters_layout = QtWidgets.QHBoxLayout()
        self.mtool_mk_help_list_button_layout = QtWidgets.QHBoxLayout()
        self.mtool_mk_help_list_layout = QtWidgets.QHBoxLayout()
        self.mtool_buttons_layout = QtWidgets.QHBoxLayout()

        self.outformat_label = QtWidgets.QLabel(__("Output format"))
        self.outformat_combobox = QtWidgets.QComboBox()
        self.outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
        self.outformat_combobox.setCurrentIndex(1)
        self.mtool_format_layout.addWidget(self.outformat_label)
        self.mtool_format_layout.addStretch(1)
        self.mtool_format_layout.addWidget(self.outformat_combobox)

        self.mtool_onlyMK_label = QtWidgets.QLabel(__("MKs to process (empty for all)"))
        self.mtool_onlyMK_text = QtWidgets.QLineEdit()
        self.mtool_onlyMK_text.setPlaceholderText("1,2,3 or 1-30")
        self.mtool_onlyMK_layout.addWidget(self.mtool_onlyMK_label)
        self.mtool_onlyMK_layout.addWidget(self.mtool_onlyMK_text)

        self.mtool_onlyid_label = QtWidgets.QLabel(__("ids to process (empty for all)"))
        self.mtool_onlyid_text = QtWidgets.QLineEdit()
        self.mtool_onlyid_text.setPlaceholderText("1,2,3 or 1-30")
        self.mtool_onlyid_layout.addWidget(self.mtool_onlyid_label)
        self.mtool_onlyid_layout.addWidget(self.mtool_onlyid_text)

        self.mtool_onlypos_label = QtWidgets.QLabel(__("pos to process (empty for all)"))
        self.mtool_onlypos_text = QtWidgets.QLineEdit()
        self.mtool_onlypos_text.setPlaceholderText("xmin:ymin:zmin:xmax:ymax:zmax (m)")
        self.mtool_onlypos_layout.addWidget(self.mtool_onlypos_label)
        self.mtool_onlypos_layout.addWidget(self.mtool_onlypos_text)

        self.mtool_types_groupbox_layout = QtWidgets.QVBoxLayout()
        self.mtool_types_groupbox_layout_row1 = QtWidgets.QHBoxLayout()
        self.mtool_types_groupbox_layout_row2 = QtWidgets.QHBoxLayout()
        self.mtool_types_chk_all = QtWidgets.QCheckBox(__("All"))
        self.mtool_types_chk_all.setCheckState(QtCore.Qt.Checked)
        self.mtool_types_chk_bound = QtWidgets.QCheckBox(__("Bound"))
        self.mtool_types_chk_fluid = QtWidgets.QCheckBox(__("Fluid"))
        for x in [self.mtool_types_chk_all,
                  self.mtool_types_chk_bound,
                  self.mtool_types_chk_fluid]:
            self.mtool_types_groupbox_layout_row1.addWidget(x)
        self.mtool_types_chk_fixed = QtWidgets.QCheckBox(__("Fixed"))
        self.mtool_types_chk_moving = QtWidgets.QCheckBox(__("Moving"))
        self.mtool_types_chk_floating = QtWidgets.QCheckBox(__("Floating"))
        for x in [self.mtool_types_chk_fixed,
                  self.mtool_types_chk_moving,
                  self.mtool_types_chk_floating]:
            self.mtool_types_groupbox_layout_row2.addWidget(x)
        self.mtool_types_groupbox_layout.addLayout(self.mtool_types_groupbox_layout_row1)
        self.mtool_types_groupbox_layout.addLayout(self.mtool_types_groupbox_layout_row2)

        self.mtool_onlytype_groupbox.setLayout(self.mtool_types_groupbox_layout)

        self.mtool_variables_groupbox_layout = QtWidgets.QVBoxLayout()
        self.mtool_variables_groupbox_row1_layout = QtWidgets.QHBoxLayout()
        self.mtool_variables_chk_all = QtWidgets.QCheckBox(__("All"))
        self.mtool_variables_chk_all.setCheckState(QtCore.Qt.Checked)
        self.mtool_variables_chk_vel = QtWidgets.QCheckBox(__("Velocity"))
        self.mtool_variables_chk_rhop = QtWidgets.QCheckBox(__("Density"))
        self.mtool_variables_chk_press = QtWidgets.QCheckBox(__("Pressure"))
        for x in [self.mtool_variables_chk_all,
                  self.mtool_variables_chk_vel,
                  self.mtool_variables_chk_rhop,
                  self.mtool_variables_chk_press]:
            self.mtool_variables_groupbox_row1_layout.addWidget(x)
        self.mtool_variables_groupbox_row2_layout = QtWidgets.QHBoxLayout()
        self.mtool_variables_chk_mass = QtWidgets.QCheckBox(__("Mass"))
        self.mtool_variables_chk_vol = QtWidgets.QCheckBox(__("Volume"))
        self.mtool_variables_chk_idp = QtWidgets.QCheckBox(__("Particle ID"))
        self.mtool_variables_chk_ace = QtWidgets.QCheckBox(__("Acceleration"))
        for x in [self.mtool_variables_chk_mass,
                  self.mtool_variables_chk_vol,
                  self.mtool_variables_chk_idp,
                  self.mtool_variables_chk_ace]:
            self.mtool_variables_groupbox_row2_layout.addWidget(x)

        self.mtool_variables_groupbox_row3_layout = QtWidgets.QHBoxLayout()
        self.mtool_variables_chk_vor = QtWidgets.QCheckBox(__("Vorticity"))
        self.mtool_variables_chk_kcorr = QtWidgets.QCheckBox(__("KCorr"))
        for x in [self.mtool_variables_chk_vor,
                 self.mtool_variables_chk_kcorr]:
            self.mtool_variables_groupbox_row3_layout.addWidget(x,stretch=1)
        self.mtool_variables_groupbox_row3_layout.addStretch(2)

        self.mtool_variables_groupbox_layout.addLayout(self.mtool_variables_groupbox_row1_layout)
        self.mtool_variables_groupbox_layout.addLayout(self.mtool_variables_groupbox_row2_layout)
        self.mtool_variables_groupbox_layout.addLayout(self.mtool_variables_groupbox_row3_layout)

        self.mtool_variables_groupbox.setLayout(self.mtool_variables_groupbox_layout)

        self.mtool_calculate_elevation = QtWidgets.QCheckBox(__("Calculate water elevation"))
        self.mtool_calculate_flow = QtWidgets.QCheckBox(__("Calculate water flow"))
        self.mtool_calculate_flow_units_selector = QtWidgets.QComboBox()
        self.mtool_calculate_flow_units_selector.addItems(["m3/s","l/s","gal/s","gal/min"])
        self.mtool_calculate_flow_layout=QtWidgets.QHBoxLayout()
        self.mtool_calculate_flow_layout.addWidget(self.mtool_calculate_flow)
        self.mtool_calculate_flow_layout.addWidget(self.mtool_calculate_flow_units_selector)


        self.mtool_track_mk = QtWidgets.QCheckBox(__("Follow object:"))
        self.mtool_track_mk_select = MkSelectInputWithNames(ObjectType.BOUND)
        self.mtool_track_mk_layout=QtWidgets.QHBoxLayout()
        self.mtool_track_mk_layout.addWidget(self.mtool_track_mk)
        self.mtool_track_mk_layout.addWidget(self.mtool_track_mk_select)



        self.mtool_points_selector_layout=QtWidgets.QHBoxLayout()
        self.mtool_points_selector=QtWidgets.QComboBox()
        self.mtool_points_selector.addItems(["List of points","Grid of points","Load points file","Load mesh file"])
        self.mtool_edit_button = QtWidgets.QPushButton("Edit")


        self.mtool_points_selector_layout.addWidget(self.mtool_points_selector)
        self.mtool_points_selector_layout.addWidget(self.mtool_edit_button)

        self.mtool_points_file_layout = QtWidgets.QHBoxLayout()
        self.mtool_points_filename_input=QtWidgets.QLineEdit()
        self.mtool_export_points_button = QtWidgets.QPushButton("Export points")
        self.mtool_points_file_layout.addWidget(self.mtool_points_filename_input)
        self.mtool_points_file_layout.addWidget(self.mtool_export_points_button)

        self.mtool_file_name_label = QtWidgets.QLabel(__("File name"))
        self.mtool_file_name_text = QtWidgets.QLineEdit()
        self.mtool_file_name_text.setText("MeasurePart")
        self.mtool_filename_layout.addWidget(self.mtool_file_name_label)
        self.mtool_filename_layout.addWidget(self.mtool_file_name_text)

        self.mtool_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.mtool_parameters_text = QtWidgets.QLineEdit()
        self.mtool_parameters_layout.addWidget(self.mtool_parameters_label)
        self.mtool_parameters_layout.addWidget(self.mtool_parameters_text)

        self.mtool_mk_help_list_widget=MkHelperWidget()
        self.mtool_mk_help_list_layout.addWidget(self.mtool_mk_help_list_widget)

        self.mtool_export_button = QtWidgets.QPushButton(__("Export"))
        self.mtool_cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.mtool_generate_script_button = QtWidgets.QPushButton(__("Generate script"))

        self.mtool_buttons_layout.addWidget(self.mtool_export_button)
        if not ApplicationSettings.the().basic_visualization:
            self.mtool_buttons_layout.addWidget(self.mtool_generate_script_button)
        self.mtool_buttons_layout.addWidget(self.mtool_cancel_button)

        self.measuretool_tool_layout.addLayout(self.mtool_format_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_onlyMK_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_onlyid_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_onlypos_layout)
        self.measuretool_tool_layout.addWidget(self.mtool_onlytype_groupbox)
        self.measuretool_tool_layout.addWidget(self.mtool_variables_groupbox)
        self.measuretool_tool_layout.addStretch(1)
        self.measuretool_tool_layout.addWidget(self.mtool_calculate_elevation)
        self.measuretool_tool_layout.addLayout(self.mtool_calculate_flow_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_track_mk_layout)

        self.measuretool_tool_layout.addLayout(self.mtool_points_selector_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_points_file_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_filename_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_parameters_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_mk_help_list_button_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_mk_help_list_layout)
        self.measuretool_tool_layout.addLayout(self.mtool_buttons_layout)

        self.setLayout(self.measuretool_tool_layout)
        self.measuretool_tool_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.mtool_types_chk_all.stateChanged.connect(self.on_mtool_type_all_change)
        self.mtool_types_chk_bound.stateChanged.connect(self.on_mtool_type_single_change)
        self.mtool_types_chk_fluid.stateChanged.connect(self.on_mtool_type_single_change)
        self.mtool_types_chk_fixed.stateChanged.connect(self.on_mtool_type_single_change)
        self.mtool_types_chk_moving.stateChanged.connect(self.on_mtool_type_single_change)
        self.mtool_types_chk_floating.stateChanged.connect(self.on_mtool_type_single_change)

        self.mtool_variables_chk_all.stateChanged.connect(self.on_mtool_measure_all_change)
        self.mtool_variables_chk_vel.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_rhop.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_press.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_mass.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_vol.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_idp.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_ace.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_vor.stateChanged.connect(self.on_mtool_measure_single_change)
        self.mtool_variables_chk_kcorr.stateChanged.connect(self.on_mtool_measure_single_change)

        self.mtool_edit_button.clicked.connect(self.on_mtool_edit)
        self.mtool_export_button.clicked.connect(self.on_mtool_local_run)
        self.mtool_export_points_button.clicked.connect(self.on_mtool_export_points)

        self.mtool_points_selector.currentIndexChanged.connect(self.on_mtool_points_selector_changed)

        self.mtool_generate_script_button.clicked.connect(self.on_mtool_generate_script)

        self.mtool_cancel_button.clicked.connect(self.on_mtool_cancel)
        self.exec_()

    def on_mtool_cancel(self):
        """ Cancel button behaviour."""
        self.reject()

    def on_mtool_generate_script(self):
        self.on_mtool_export(True)

    def on_mtool_local_run(self):
        self.on_mtool_export(False)


    def on_mtool_export(self,generate_script):
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters["save_mode"] = self.outformat_combobox.currentIndex()
        export_parameters["save_vars"] = "-all"
        export_parameters["-onlymk"] = self.mtool_onlyMK_text.text()
        export_parameters["-onlyid"] = self.mtool_onlyid_text.text()
        export_parameters["-onlypos"] = self.mtool_onlypos_text.text()

        export_parameters["save_types"] = "-all"

        if self.mtool_types_chk_all.isChecked():
            export_parameters["save_types"] = "+all"
        else:
            if self.mtool_types_chk_bound.isChecked():
                export_parameters["save_types"] += ",+bound"
            if self.mtool_types_chk_fluid.isChecked():
                export_parameters["save_types"] += ",+fluid"
            if self.mtool_types_chk_fixed.isChecked():
                export_parameters["save_types"] += ",+fixed"
            if self.mtool_types_chk_moving.isChecked():
                export_parameters["save_types"] += ",+moving"
            if self.mtool_types_chk_floating.isChecked():
                export_parameters["save_types"] += ",+floating"

        if export_parameters["save_types"] == "-all":
            export_parameters["save_types"] = "+all"
        
        if self.mtool_variables_chk_all.isChecked():
            export_parameters["save_vars"] = "+all"
        else:
            if self.mtool_variables_chk_vel.isChecked():
                export_parameters["save_vars"] += ",+vel"
            if self.mtool_variables_chk_rhop.isChecked():
                export_parameters["save_vars"] += ",+rhop"
            if self.mtool_variables_chk_press.isChecked():
                export_parameters["save_vars"] += ",+press"
            if self.mtool_variables_chk_mass.isChecked():
                export_parameters["save_vars"] += ",+mass"
            if self.mtool_variables_chk_vol.isChecked():
                export_parameters["save_vars"] += ",+vol"
            if self.mtool_variables_chk_idp.isChecked():
                export_parameters["save_vars"] += ",+idp"
            if self.mtool_variables_chk_ace.isChecked():
                export_parameters["save_vars"] += ",+ace"
            if self.mtool_variables_chk_vor.isChecked():
                export_parameters["save_vars"] += ",+vor"
            if self.mtool_variables_chk_kcorr.isChecked():
                export_parameters["save_vars"] += ",+kcorr"

        if export_parameters["save_vars"] == "-all" and not self.mtool_calculate_elevation.isChecked():
            export_parameters["save_vars"] = "+all"

        export_parameters["calculate_water_elevation"] = self.mtool_calculate_elevation.isChecked()
        export_parameters["calculate_water_flow"] = self.mtool_calculate_flow.isChecked()
        export_parameters["water_flow_units"] = self.mtool_calculate_flow_units_selector.currentIndex()+1
        export_parameters["follow_mk_enable"] = self.mtool_track_mk.isChecked()
        export_parameters["follow_mk_number"] = self.mtool_track_mk_select.get_mk_value() + MKFLUID_LIMIT

        if self.mtool_file_name_text.text():
            export_parameters["filename"] = self.mtool_file_name_text.text()
        else:
            export_parameters["filename"] = "MeasurePart"

        if self.mtool_parameters_text.text():
            export_parameters["additional_parameters"] = self.mtool_parameters_text.text()
        else:
            export_parameters["additional_parameters"] = ""

        if self.mtool_points_filename_input.text():
            export_parameters["points_file"] = self.mtool_points_filename_input.text()
        else:
            export_parameters["points_file"] = "points.txt"

        if self.mtool_points_selector.currentIndex()==0 and not Case.the().post_processing_settings.measuretool_points:
            error_dialog(
                __("No 'List of points' defined to execute MeasureTool"),
                __("Please define a 'List of points' or select different option to continue. MeasureTool will not be executed.")
            )
            return
        if self.mtool_points_selector.currentIndex() == 1 and not Case.the().post_processing_settings.measuretool_grid:
            error_dialog(
                __("No 'Grid of points' are defined to execute MeasureTool"),
                __("Please define a 'Grid of points' to continue, or select a different option. MeasureTool will not be executed.")
            )
            return
        export_parameters["points_source"]=self.mtool_points_selector.currentIndex()

        if export_parameters["calculate_water_flow"] and export_parameters["points_source"]==0:
            warning_dialog("Flow calculation cannot be done with list of points, it needs a grid of points or a mesh of points")
            return

        measuretool_export(export_parameters, Case.the(), self.post_processing_widget,generate_script)
        self.accept()

    def on_mtool_measure_all_change(self, state):
        """ "All" checkbox behaviour"""
        if state == QtCore.Qt.Checked:
            for chk in [self.mtool_variables_chk_vel,
                        self.mtool_variables_chk_rhop,
                        self.mtool_variables_chk_press,
                        self.mtool_variables_chk_mass,
                        self.mtool_variables_chk_vol,
                        self.mtool_variables_chk_idp,
                        self.mtool_variables_chk_ace,
                        self.mtool_variables_chk_vor,
                        self.mtool_variables_chk_kcorr]:
                chk.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_type_all_change(self,state):
        """ "Type All" checkbox behaviour"""
        if state == QtCore.Qt.Checked:
            for chk in [self.mtool_types_chk_bound,
                        self.mtool_types_chk_fluid,
                        self.mtool_types_chk_fixed,
                        self.mtool_types_chk_floating,
                        self.mtool_types_chk_moving]:
                chk.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_type_single_change(self,state):
        """ "Type Single" checkbox behaviour"""
        if state == QtCore.Qt.Checked:
            self.mtool_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_measure_single_change(self, state):
        """ Behaviour for all checkboxes except "All" """
        if state == QtCore.Qt.Checked:
            self.mtool_variables_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_edit(self):
        if self.mtool_points_selector.currentIndex()==0:
            MeasureToolPointsDialog(parent=None)
        else:
            MeasureToolGridDialog(parent=None)

    def on_help_list(self):
        info = mk_help_list()
        self.mtool_mk_help_list_label.setText(info)

    def on_mtool_points_selector_changed(self,index):
        if index<2:
            self.mtool_export_points_button.setEnabled(True)
            self.mtool_edit_button.setEnabled(True)
            self.mtool_points_filename_input.setPlaceholderText("Name of the file to export")
        else:
            self.mtool_export_points_button.setEnabled(False)
            self.mtool_edit_button.setEnabled(False)
            self.mtool_points_filename_input.setPlaceholderText("Name of the file to load")
        if index==3:
            self.mtool_track_mk.setChecked(False)
            self.mtool_track_mk.setEnabled(False)
        else:
            self.mtool_track_mk.setEnabled(True)

    def on_mtool_export_points(self):
        if not Case.the().path:
            warning_dialog("Case is not saved. You need to save your case first")
            return
        if self.mtool_points_filename_input.text():
            pointsfile = self.mtool_points_filename_input.text()
        else:
            pointsfile="points.txt"
        try:
            if self.mtool_points_selector.currentIndex()==0:
                save_measuretool_point_list(Case.the().path, pointsfile, Case.the().post_processing_settings.measuretool_points)
            else:
                save_measuretool_point_grid(Case.the().path, pointsfile, Case.the().post_processing_settings.measuretool_grid)
        except RuntimeError:
            return
        info_dialog(f"Points exported successfully into {pointsfile}")



