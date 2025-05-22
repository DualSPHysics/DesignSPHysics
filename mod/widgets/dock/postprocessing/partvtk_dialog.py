#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics PartVTK Config and Execution Dialog."""

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.post_processing_tools import partvtk_export
from mod.tools.translation_tools import __



class PartVTKDialog(QtWidgets.QDialog):
    """ A PartVTK Configuration and Execution Dialog. """

    DEFAULT_NAMES = ["PartAll", "PartBound", "PartFluid", "PartFixed", "PartMoving", "PartFloating"]

    def __init__(self, post_processing_widget, parent=None):
        super().__init__(parent=parent)

        self.post_processing_widget = post_processing_widget

        self.setModal(False)
        self.setWindowTitle(__("PartVTK Tool"))
        self.partvtk_tool_layout = QtWidgets.QVBoxLayout()

        self.pvtk_format_layout = QtWidgets.QHBoxLayout()
        self.pvtk_onlypos_layout = QtWidgets.QHBoxLayout()

        self.pvtk_types_groupbox = QtWidgets.QGroupBox(__("Types to export"))

        self.pvtk_filename_layout = QtWidgets.QHBoxLayout()
        self.pvtk_parameters_layout = QtWidgets.QHBoxLayout()
        self.pvtk_buttons_layout = QtWidgets.QHBoxLayout()


        self.outformat_label = QtWidgets.QLabel(__("Output format"))
        self.outformat_combobox = QtWidgets.QComboBox()
        self.outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
        self.pvtk_format_layout.addWidget(self.outformat_label)
        self.pvtk_format_layout.addStretch(1)
        self.pvtk_format_layout.addWidget(self.outformat_combobox)

        self.pvtk_onlypos_label = QtWidgets.QLabel(__("pos to process (empty for all)"))
        self.pvtk_onlypos_text = QtWidgets.QLineEdit()
        self.pvtk_onlypos_text.setPlaceholderText("xmin:ymin:zmin:xmax:ymax:zmax (m)")
        self.pvtk_onlypos_layout.addWidget(self.pvtk_onlypos_label)
        self.pvtk_onlypos_layout.addWidget(self.pvtk_onlypos_text)

        self.pvtk_types_groupbox_layout = QtWidgets.QVBoxLayout()
        self.pvtk_types_groupbox_layout_row1 = QtWidgets.QHBoxLayout()
        self.pvtk_types_groupbox_layout_row2 = QtWidgets.QHBoxLayout()
        self.pvtk_types_chk_all = QtWidgets.QCheckBox(__("All"))
        self.pvtk_types_chk_all.setCheckState(QtCore.Qt.Checked)
        self.pvtk_types_chk_bound = QtWidgets.QCheckBox(__("Bound"))
        self.pvtk_types_chk_fluid = QtWidgets.QCheckBox(__("Fluid"))
        self.pvtk_types_chk_fixed = QtWidgets.QCheckBox(__("Fixed"))
        self.pvtk_types_chk_moving = QtWidgets.QCheckBox(__("Moving"))
        self.pvtk_types_chk_floating = QtWidgets.QCheckBox(__("Floating"))
        for x in [self.pvtk_types_chk_all,
                  self.pvtk_types_chk_bound,
                  self.pvtk_types_chk_fluid]:
            self.pvtk_types_groupbox_layout_row1.addWidget(x)
        self.pvtk_types_chk_fixed = QtWidgets.QCheckBox(__("Fixed"))
        self.pvtk_types_chk_moving = QtWidgets.QCheckBox(__("Moving"))
        self.pvtk_types_chk_floating = QtWidgets.QCheckBox(__("Floating"))
        for x in [self.pvtk_types_chk_fixed,
                  self.pvtk_types_chk_moving,
                  self.pvtk_types_chk_floating]:
            self.pvtk_types_groupbox_layout_row2.addWidget(x)
        self.pvtk_types_groupbox_layout.addLayout(self.pvtk_types_groupbox_layout_row1)
        self.pvtk_types_groupbox_layout.addLayout(self.pvtk_types_groupbox_layout_row2)

        self.pvtk_types_groupbox.setLayout(self.pvtk_types_groupbox_layout)

        self.pvtk_file_name_label = QtWidgets.QLabel(__("File name"))
        self.pvtk_file_name_text = QtWidgets.QLineEdit()
        self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[0])
        self.pvtk_filename_layout.addWidget(self.pvtk_file_name_label)
        self.pvtk_filename_layout.addWidget(self.pvtk_file_name_text)

        self.pvtk_parameters_label = QtWidgets.QLabel(__("Additional Parameters"))
        self.pvtk_parameters_text = QtWidgets.QLineEdit()
        self.pvtk_parameters_layout.addWidget(self.pvtk_parameters_label)
        self.pvtk_parameters_layout.addWidget(self.pvtk_parameters_text)

        self.pvtk_open_at_end = QtWidgets.QCheckBox("Open with ParaView (only local)")
        self.pvtk_open_at_end.setEnabled(Case.the().executable_paths.paraview != "")

        self.pvtk_export_button = QtWidgets.QPushButton(__("Export"))
        self.pvtk_generate_script_button = QtWidgets.QPushButton(__("Generate script"))
        self.pvtk_cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.pvtk_buttons_layout.addWidget(self.pvtk_export_button)
        if not ApplicationSettings.the().basic_visualization:
              self.pvtk_buttons_layout.addWidget(self.pvtk_generate_script_button)
        self.pvtk_buttons_layout.addWidget(self.pvtk_cancel_button)

        self.partvtk_tool_layout.addLayout(self.pvtk_format_layout)
        self.partvtk_tool_layout.addLayout(self.pvtk_onlypos_layout)
        self.partvtk_tool_layout.addWidget(self.pvtk_types_groupbox)
        self.partvtk_tool_layout.addStretch(1)
        self.partvtk_tool_layout.addLayout(self.pvtk_filename_layout)
        self.partvtk_tool_layout.addLayout(self.pvtk_parameters_layout)
        self.partvtk_tool_layout.addWidget(self.pvtk_open_at_end)
        self.partvtk_tool_layout.addLayout(self.pvtk_buttons_layout)

        self.setLayout(self.partvtk_tool_layout)

        self.outformat_combobox.currentIndexChanged.connect(self.on_pvtk_export_format_change)
        self.pvtk_types_chk_all.stateChanged.connect(self.on_pvtk_type_all_change)
        self.pvtk_types_chk_bound.stateChanged.connect(self.on_pvtk_type_bound_change)
        self.pvtk_types_chk_fluid.stateChanged.connect(self.on_pvtk_type_fluid_change)
        self.pvtk_types_chk_fixed.stateChanged.connect(self.on_pvtk_type_fixed_change)
        self.pvtk_types_chk_moving.stateChanged.connect(self.on_pvtk_type_moving_change)
        self.pvtk_types_chk_floating.stateChanged.connect(self.on_pvtk_type_floating_change)
        self.pvtk_export_button.clicked.connect(self.on_pvtk_local_run)
        self.pvtk_generate_script_button.clicked.connect(self.on_pvtk_generate_script)
        self.pvtk_cancel_button.clicked.connect(self.on_pvtk_cancel)
        self.exec_()

    def on_pvtk_cancel(self):
        """ Cancel button behaviour """
        self.reject()

    def on_pvtk_local_run(self):
        self.on_pvtk_export(False)

    def on_pvtk_generate_script(self):
        self.on_pvtk_export(True)

    def on_pvtk_export(self, generate_script:bool):
        """ Export button behaviour """
        export_parameters = dict()
        export_parameters["save_mode"] = self.outformat_combobox.currentIndex()
        export_parameters["-onlypos"] = self.pvtk_onlypos_text.text()        
        export_parameters["save_types"] = "-all"

        if self.pvtk_types_chk_all.isChecked():
            export_parameters["save_types"] = "+all"
        else:
            if self.pvtk_types_chk_bound.isChecked():
                export_parameters["save_types"] += ",+bound"
            if self.pvtk_types_chk_fluid.isChecked():
                export_parameters["save_types"] += ",+fluid"
            if self.pvtk_types_chk_fixed.isChecked():
                export_parameters["save_types"] += ",+fixed"
            if self.pvtk_types_chk_moving.isChecked():
                export_parameters["save_types"] += ",+moving"
            if self.pvtk_types_chk_floating.isChecked():
                export_parameters["save_types"] += ",+floating"

        if export_parameters["save_types"] == "-all":
            export_parameters["save_types"] = "+all"

        export_parameters["open_paraview"] = self.pvtk_open_at_end.isChecked()

        if self.pvtk_file_name_text.text():
            export_parameters["file_name"] = self.pvtk_file_name_text.text()
        else:
            export_parameters["file_name"] = "ExportedPart"


        if self.pvtk_parameters_text.text():
            export_parameters["additional_parameters"] = self.pvtk_parameters_text.text()
        else:
            export_parameters["additional_parameters"] = ""


        partvtk_export(export_parameters, Case.the(), self.post_processing_widget,generate_script)
        self.accept()

    def on_pvtk_type_all_change(self, state):
        """ "All" type selection handler """
        if state == QtCore.Qt.Checked:
            for chk in [self.pvtk_types_chk_bound,
                        self.pvtk_types_chk_fluid,
                        self.pvtk_types_chk_fixed,
                        self.pvtk_types_chk_moving,
                        self.pvtk_types_chk_floating]:
                chk.setCheckState(QtCore.Qt.Unchecked)
        if self.pvtk_file_name_text.text() in self.DEFAULT_NAMES:
            self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[0])

    def on_pvtk_type_bound_change(self, state):
        """ "Bound" type selection handler """
        if state == QtCore.Qt.Checked:
            self.pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)
        if self.pvtk_file_name_text.text() in self.DEFAULT_NAMES:
            self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[1])

    def on_pvtk_type_fluid_change(self, state):
        """ "Fluid" type selection handler """
        if state == QtCore.Qt.Checked:
            self.pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)
        if self.pvtk_file_name_text.text() in self.DEFAULT_NAMES:
            self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[2])

    def on_pvtk_type_fixed_change(self, state):
        """ "Fixed" type selection handler """
        if state == QtCore.Qt.Checked:
            self.pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)
        if self.pvtk_file_name_text.text() in self.DEFAULT_NAMES:
            self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[3])

    def on_pvtk_type_moving_change(self, state):
        """ "Moving" type selection handler """
        if state == QtCore.Qt.Checked:
            self.pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)
        if self.pvtk_file_name_text.text() in self.DEFAULT_NAMES:
            self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[4])

    def on_pvtk_type_floating_change(self, state):
        """ "Floating" type selection handler """
        if state == QtCore.Qt.Checked:
            self.pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)
        if self.pvtk_file_name_text.text() in self.DEFAULT_NAMES:
            self.pvtk_file_name_text.setText(self.DEFAULT_NAMES[5])

    def on_pvtk_export_format_change(self, _):
        """ Export format combobox handler"""
        if "vtk" in self.outformat_combobox.currentText().lower() and Case.the().executable_paths.paraview != "":
            self.pvtk_open_at_end.setEnabled(True)
        else:
            self.pvtk_open_at_end.setEnabled(False)
