#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone File config Dialog"""

from os import path

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.dataobjects.relaxation_zone.relaxation_zone_file import RelaxationZoneFile
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput

from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class RelaxationZoneFileConfigDialog(QtWidgets.QDialog):
    """ A dialog with configuration related to a relaxation zone with file. """

    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneFile()
        self.relaxationzone = relaxationzone

        self.main_layout = QtWidgets.QVBoxLayout()
        self.data_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.relaxation_zone_scroll = QtWidgets.QScrollArea()  # "Import VTM options"
        self.relaxation_zone_scroll.setFixedWidth(780)
        self.relaxation_zone_scroll.setWidgetResizable(True)
        self.relaxation_zone_scroll_widget = QtWidgets.QWidget()
        self.relaxation_zone_scroll_widget.setFixedWidth(780)
        self.relaxation_zone_scroll_widget.setLayout(self.data_layout)

        self.relaxation_zone_scroll.setWidget(self.relaxation_zone_scroll_widget)
        self.relaxation_zone_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setFixedWidth(800)

        self.start_layout = QtWidgets.QHBoxLayout()
        self.start_label = QtWidgets.QLabel(__("Start time:"))
        self.start_input = TimeInput()
        self.duration_label = QtWidgets.QLabel(__("Duration (0 for end of simulation):"))
        self.duration_input = TimeInput()
        for x in [self.start_label, self.start_input, self.duration_label, self.duration_input]:
            self.start_layout.addWidget(x)

        self.depth_layout = QtWidgets.QHBoxLayout()
        self.depth_label = QtWidgets.QLabel(__("Water depth:"))
        self.depth_input = SizeInput()
        self.swl_label = QtWidgets.QLabel(__("Still water level:"))
        self.swl_input = SizeInput()
        for x in [self.depth_label, self.depth_input, self.swl_label, self.swl_input]:
            self.depth_layout.addWidget(x)

        self.filesvel_layout = QtWidgets.QHBoxLayout()
        self.filesvel_label = QtWidgets.QLabel(__("Velocity file:"))
        self.filesvel_input = QtWidgets.QLineEdit()
        self.filesvel_browse = QtWidgets.QPushButton("...")
        for x in [self.filesvel_label, self.filesvel_input, self.filesvel_browse]:
            self.filesvel_layout.addWidget(x)

        self.filesvelx_initial_layout = QtWidgets.QHBoxLayout()
        self.filesvelx_initial_label = QtWidgets.QLabel(__("First file:"))
        self.filesvelx_initial_input = IntValueInput()
        self.filesvelx_count_label = QtWidgets.QLabel(__("File count:"))
        self.filesvelx_count_input = IntValueInput()
        for x in [self.filesvelx_initial_label, self.filesvelx_initial_input,self.filesvelx_count_label, self.filesvelx_count_input]:
            self.filesvelx_initial_layout.addWidget(x)





        self.usevelz_check = QtWidgets.QCheckBox(__("Use velocity in Z"))

        self.movedata_layout = QtWidgets.QHBoxLayout()
        self.movedata_label = QtWidgets.QLabel(__("Movement of data in CSV files (X, Y, Z):"))
        self.movedata_x = IntValueInput()
        self.movedata_y = IntValueInput()
        self.movedata_z = IntValueInput()
        for x in [self.movedata_label, self.movedata_x, self.movedata_y, self.movedata_z]:
            self.movedata_layout.addWidget(x)

        self.dpz_layout = QtWidgets.QHBoxLayout()
        self.dpz_label = QtWidgets.QLabel(__("Distance between key points in Z (dp):"))
        self.dpz_input = ValueInput()
        for x in [self.dpz_label, self.dpz_input]:
            self.dpz_layout.addWidget(x)

        self.smooth_layout = QtWidgets.QHBoxLayout()
        self.smooth_label = QtWidgets.QLabel(__("Smooth motion level:"))
        self.smooth_input = ValueInput()
        for x in [self.smooth_label, self.smooth_input]:
            self.smooth_layout.addWidget(x)

        self.center_layout = QtWidgets.QHBoxLayout()
        self.center_label = QtWidgets.QLabel(__("Central point (X, Y, Z):"))
        self.center_x = SizeInput()
        self.center_y = SizeInput()
        self.center_z = SizeInput()
        for x in [self.center_label, self.center_x, self.center_y, self.center_z]:
            self.center_layout.addWidget(x)

        self.width_layout = QtWidgets.QHBoxLayout()
        self.width_label = QtWidgets.QLabel(__("Width for generation:"))
        self.width_input = ValueInput()
        for x in [self.width_label, self.width_input]:
            self.width_layout.addWidget(x)

        self.coefdir_layout = QtWidgets.QHBoxLayout()
        self.coefdir_label = QtWidgets.QLabel(__("Coefficient for each direction (X, Y, Z):"))
        self.coefdir_x = SizeInput()
        self.coefdir_x.setEnabled(False)
        self.coefdir_y = SizeInput()
        self.coefdir_y.setEnabled(False)
        self.coefdir_z = SizeInput()
        self.coefdir_z.setEnabled(False)
        for x in [self.coefdir_label, self.coefdir_x, self.coefdir_y, self.coefdir_z]:
            self.coefdir_layout.addWidget(x)

        self.coefdt_layout = QtWidgets.QHBoxLayout()
        self.coefdt_label = QtWidgets.QLabel(__("Multiplier for dt value:"))
        self.coefdt_input = ValueInput()
        self.coefdt_input.setEnabled(False)
        for x in [self.coefdt_label, self.coefdt_input]:
            self.coefdt_layout.addWidget(x)

        self.function_label_layout = QtWidgets.QHBoxLayout()
        self.function_label = QtWidgets.QLabel(__("-------- Coefficients in function for velocity --------"))
        self.function_label_layout.addStretch()
        self.function_label_layout.addWidget(self.function_label)
        self.function_label_layout.addStretch()
        self.function_layout = QtWidgets.QHBoxLayout()
        self.function_psi_label = QtWidgets.QLabel(__("Psi: "))
        self.function_psi_input = ValueInput()
        self.function_beta_label = QtWidgets.QLabel(__("Beta: "))
        self.function_beta_input = ValueInput()
        for x in [self.function_psi_label,
                  self.function_psi_input,
                  self.function_beta_label,
                  self.function_beta_input]:
            self.function_layout.addWidget(x)

        self.driftcorrection_layout = QtWidgets.QHBoxLayout()
        self.driftcorrection_label = QtWidgets.QLabel(__("Coefficient of drift correction (for X):"))
        self.driftcorrection_input = ValueInput()
        self.driftinitialramp_label = QtWidgets.QLabel(__("TInitial ramp:"))
        self.driftinitialramp_input = TimeInput()
        for x in [self.driftcorrection_label, self.driftcorrection_input,self.driftinitialramp_label, self.driftinitialramp_input]:
            self.driftcorrection_layout.addWidget(x)

        for x in [self.start_layout,
                  self.depth_layout,
                  self.filesvel_layout,
                  self.filesvelx_initial_layout]:
            self.data_layout.addLayout(x)

        self.data_layout.addWidget(self.usevelz_check)
        for x in [self.movedata_layout,
                  self.dpz_layout,
                  self.smooth_layout,
                  self.center_layout,
                  self.width_layout,
                  self.coefdir_layout,
                  self.coefdt_layout,
                  self.function_label_layout,
                  self.function_layout,
                  self.driftcorrection_layout]:
            self.data_layout.addLayout(x)

        self.delete_button = QtWidgets.QPushButton(__("Delete RZ configuration"))
        self.apply_button = QtWidgets.QPushButton(__("Apply this configuration"))

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addWidget(self.relaxation_zone_scroll)
        self.main_layout.addLayout(self.button_layout)
        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.filesvel_browse.clicked.connect(self.on_browse)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_browse(self):
        """ Opens a file dialog to select a series of files. Then processes it to extract the series. """
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, __("Open a file from the serie"), Case.the().info.last_used_directory, "External velocity data (*_x*_y*.csv)")
        Case.the().info.update_last_used_directory(file_name)
        if not file_name:
            return

        basename: str = path.basename(file_name)
        folder: str = path.dirname(file_name)

        # Takes only the filename without the serie data in its name
        self.filesvel_input.setText("{}/{}".format(folder, basename.split("_vel")[0]))

    def on_apply(self):
        """ Saves the data on the dialog into the data structure. """
        self.temp_relaxationzone.start = self.start_input.value()
        self.temp_relaxationzone.duration = self.duration_input.value()
        self.temp_relaxationzone.depth = self.depth_input.value()
        self.temp_relaxationzone.swl = self.swl_input.value()
        self.temp_relaxationzone.filesvel = str(self.filesvel_input.text())
        self.temp_relaxationzone.filesvelx_initial = self.filesvelx_initial_input.value()
        self.temp_relaxationzone.filesvelx_count = self.filesvelx_count_input.value()
        self.temp_relaxationzone.usevelz = bool(self.usevelz_check.isChecked())
        self.temp_relaxationzone.movedata[0] = self.movedata_x.value()
        self.temp_relaxationzone.movedata[1] = self.movedata_y.value()
        self.temp_relaxationzone.movedata[2] = self.movedata_z.value()
        self.temp_relaxationzone.dpz = self.dpz_input.value()
        self.temp_relaxationzone.smooth = self.smooth_input.value()
        self.temp_relaxationzone.center[0] = self.center_x.value()
        self.temp_relaxationzone.center[1] = self.center_y.value()
        self.temp_relaxationzone.center[2] = self.center_z.value()
        self.temp_relaxationzone.width = self.width_input.value()
        self.temp_relaxationzone.coefdir[0] = self.coefdir_x.value()
        self.temp_relaxationzone.coefdir[1] = self.coefdir_y.value()
        self.temp_relaxationzone.coefdir[2] = self.coefdir_z.value()
        self.temp_relaxationzone.coefdt = self.coefdt_input.value()
        self.temp_relaxationzone.function_psi = self.function_psi_input.value()
        self.temp_relaxationzone.function_beta = self.function_beta_input.value()
        self.temp_relaxationzone.driftcorrection = self.driftcorrection_input.value()
        self.temp_relaxationzone.driftinitialramp = self.driftinitialramp_input.value()
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        """ Deletes the currently represented relaxation zone. """
        self.relaxationzone = None
        self.reject()

    def fill_data(self):
        """ Fills the data from the data structure onto the dialog. """
        self.start_input.setValue(self.temp_relaxationzone.start)
        self.duration_input.setValue(self.temp_relaxationzone.duration)
        self.depth_input.setValue(self.temp_relaxationzone.depth)
        self.swl_input.setValue(self.temp_relaxationzone.swl)
        self.filesvel_input.setText(self.temp_relaxationzone.filesvel)
        self.filesvelx_initial_input.setValue(self.temp_relaxationzone.filesvelx_initial)
        self.filesvelx_count_input.setValue(self.temp_relaxationzone.filesvelx_count)
        self.usevelz_check.setChecked(bool(self.temp_relaxationzone.usevelz))
        self.movedata_x.setValue(self.temp_relaxationzone.movedata[0])
        self.movedata_y.setValue(self.temp_relaxationzone.movedata[1])
        self.movedata_z.setValue(self.temp_relaxationzone.movedata[2])
        self.dpz_input.setValue(self.temp_relaxationzone.dpz)
        self.smooth_input.setValue(self.temp_relaxationzone.smooth)
        self.center_x.setValue(self.temp_relaxationzone.center[0])
        self.center_y.setValue(self.temp_relaxationzone.center[1])
        self.center_z.setValue(self.temp_relaxationzone.center[2])
        self.width_input.setValue(self.temp_relaxationzone.width)
        self.coefdir_x.setValue(self.temp_relaxationzone.coefdir[0])
        self.coefdir_y.setValue(self.temp_relaxationzone.coefdir[1])
        self.coefdir_z.setValue(self.temp_relaxationzone.coefdir[2])
        self.coefdt_input.setValue(self.temp_relaxationzone.coefdt)
        self.function_psi_input.setValue(self.temp_relaxationzone.function_psi)
        self.function_beta_input.setValue(self.temp_relaxationzone.function_beta)
        self.driftcorrection_input.setValue(self.temp_relaxationzone.driftcorrection)
        self.driftinitialramp_input.setValue(self.temp_relaxationzone.driftinitialramp)
