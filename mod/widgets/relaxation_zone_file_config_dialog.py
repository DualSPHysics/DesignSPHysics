#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone File config Dialog"""

from os import path

from PySide import QtGui

from mod.translation_tools import __

from mod.dataobjects.case import Case
from mod.dataobjects.relaxation_zone_file import RelaxationZoneFile


class RelaxationZoneFileConfigDialog(QtGui.QDialog):
    """ A dialog with configuration related to a relaxation zone with file. """

    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneFile()
        self.relaxationzone = relaxationzone

        self.main_layout = QtGui.QVBoxLayout()
        self.data_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()

        self.start_layout = QtGui.QHBoxLayout()
        self.start_label = QtGui.QLabel(__("Start time (s):"))
        self.start_input = QtGui.QLineEdit()
        for x in [self.start_label, self.start_input]:
            self.start_layout.addWidget(x)

        self.duration_layout = QtGui.QHBoxLayout()
        self.duration_label = QtGui.QLabel(__("Movement duration (0 for end of simulation):"))
        self.duration_input = QtGui.QLineEdit()
        for x in [self.duration_label, self.duration_input]:
            self.duration_layout.addWidget(x)

        self.depth_layout = QtGui.QHBoxLayout()
        self.depth_label = QtGui.QLabel(__("Water depth:"))
        self.depth_input = QtGui.QLineEdit()
        for x in [self.depth_label, self.depth_input]:
            self.depth_layout.addWidget(x)

        self.swl_layout = QtGui.QHBoxLayout()
        self.swl_label = QtGui.QLabel(__("Still water level:"))
        self.swl_input = QtGui.QLineEdit()
        for x in [self.swl_label, self.swl_input]:
            self.swl_layout.addWidget(x)

        self.filesvel_layout = QtGui.QHBoxLayout()
        self.filesvel_label = QtGui.QLabel(__("Name of the file with velocity to use:"))
        self.filesvel_input = QtGui.QLineEdit()
        self.filesvel_browse = QtGui.QPushButton("...")
        for x in [self.filesvel_label, self.filesvel_input, self.filesvel_browse]:
            self.filesvel_layout.addWidget(x)

        self.filesvelx_initial_layout = QtGui.QHBoxLayout()
        self.filesvelx_initial_label = QtGui.QLabel(__("First file:"))
        self.filesvelx_initial_input = QtGui.QLineEdit()
        for x in [self.filesvelx_initial_label, self.filesvelx_initial_input]:
            self.filesvelx_initial_layout.addWidget(x)

        self.filesvelx_count_layout = QtGui.QHBoxLayout()
        self.filesvelx_count_label = QtGui.QLabel(__("File count:"))
        self.filesvelx_count_input = QtGui.QLineEdit()
        for x in [self.filesvelx_count_label, self.filesvelx_count_input]:
            self.filesvelx_count_layout.addWidget(x)

        self.usevelz_check = QtGui.QCheckBox(__("Use velocity in Z"))

        self.movedata_layout = QtGui.QHBoxLayout()
        self.movedata_label = QtGui.QLabel(__("Movement of data in CSV files (X, Y, Z):"))
        self.movedata_x = QtGui.QLineEdit()
        self.movedata_y = QtGui.QLineEdit()
        self.movedata_z = QtGui.QLineEdit()
        for x in [self.movedata_label, self.movedata_x, self.movedata_y, self.movedata_z]:
            self.movedata_layout.addWidget(x)

        self.dpz_layout = QtGui.QHBoxLayout()
        self.dpz_label = QtGui.QLabel(__("Distance between key points in Z (dp):"))
        self.dpz_input = QtGui.QLineEdit()
        for x in [self.dpz_label, self.dpz_input]:
            self.dpz_layout.addWidget(x)

        self.smooth_layout = QtGui.QHBoxLayout()
        self.smooth_label = QtGui.QLabel(__("Smooth motion level:"))
        self.smooth_input = QtGui.QLineEdit()
        for x in [self.smooth_label, self.smooth_input]:
            self.smooth_layout.addWidget(x)

        self.center_layout = QtGui.QHBoxLayout()
        self.center_label = QtGui.QLabel(__("Central point (X, Y, Z):"))
        self.center_x = QtGui.QLineEdit()
        self.center_y = QtGui.QLineEdit()
        self.center_z = QtGui.QLineEdit()
        for x in [self.center_label, self.center_x, self.center_y, self.center_z]:
            self.center_layout.addWidget(x)

        self.width_layout = QtGui.QHBoxLayout()
        self.width_label = QtGui.QLabel(__("Width for generation:"))
        self.width_input = QtGui.QLineEdit()
        for x in [self.width_label, self.width_input]:
            self.width_layout.addWidget(x)

        self.coefdir_layout = QtGui.QHBoxLayout()
        self.coefdir_label = QtGui.QLabel(__("Coefficient for each direction (X, Y, Z):"))
        self.coefdir_x = QtGui.QLineEdit()
        self.coefdir_x.setEnabled(False)
        self.coefdir_y = QtGui.QLineEdit()
        self.coefdir_y.setEnabled(False)
        self.coefdir_z = QtGui.QLineEdit()
        self.coefdir_z.setEnabled(False)
        for x in [self.coefdir_label, self.coefdir_x, self.coefdir_y, self.coefdir_z]:
            self.coefdir_layout.addWidget(x)

        self.coefdt_layout = QtGui.QHBoxLayout()
        self.coefdt_label = QtGui.QLabel(__("Multiplier for dt value in each direction:"))
        self.coefdt_input = QtGui.QLineEdit()
        self.coefdt_input.setEnabled(False)
        for x in [self.coefdt_label, self.coefdt_input]:
            self.coefdt_layout.addWidget(x)

        self.function_layout = QtGui.QHBoxLayout()
        self.function_label = QtGui.QLabel(__("Coefficients in function for velocity ->"))
        self.function_psi_label = QtGui.QLabel(__("Psi: "))
        self.function_psi_input = QtGui.QLineEdit()
        self.function_beta_label = QtGui.QLabel(__("Beta: "))
        self.function_beta_input = QtGui.QLineEdit()
        for x in [self.function_label,
                  self.function_psi_label,
                  self.function_psi_input,
                  self.function_beta_label,
                  self.function_beta_input]:
            self.function_layout.addWidget(x)

        self.driftcorrection_layout = QtGui.QHBoxLayout()
        self.driftcorrection_label = QtGui.QLabel(__("Coefficient of drift correction (for X):"))
        self.driftcorrection_input = QtGui.QLineEdit()
        for x in [self.driftcorrection_label, self.driftcorrection_input]:
            self.driftcorrection_layout.addWidget(x)

        self.driftinitialramp_layout = QtGui.QHBoxLayout()
        self.driftinitialramp_label = QtGui.QLabel(__("Time to ignore waves from external data (s):"))
        self.driftinitialramp_input = QtGui.QLineEdit()
        for x in [self.driftinitialramp_label, self.driftinitialramp_input]:
            self.driftinitialramp_layout.addWidget(x)

        for x in [self.start_layout,
                  self.duration_layout,
                  self.depth_layout,
                  self.swl_layout,
                  self.filesvel_layout,
                  self.filesvelx_initial_layout,
                  self.filesvelx_count_layout]:
            self.data_layout.addLayout(x)

        self.data_layout.addWidget(self.usevelz_check)
        for x in [self.movedata_layout,
                  self.dpz_layout,
                  self.smooth_layout,
                  self.center_layout,
                  self.width_layout,
                  self.coefdir_layout,
                  self.coefdt_layout,
                  self.function_layout,
                  self.driftcorrection_layout,
                  self.driftinitialramp_layout]:
            self.data_layout.addLayout(x)

        self.delete_button = QtGui.QPushButton(__("Delete RZ configuration"))
        self.apply_button = QtGui.QPushButton(__("Apply this configuration"))

        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)
        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.filesvel_browse.clicked.connect(self.on_browse)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_browse(self):
        """ Opens a file dialog to select a series of files. Then processes it to extract the series. """
        file_name, _ = QtGui.QFileDialog.getOpenFileName(self, __("Open a file from the serie"), Case.the().info.last_used_directory, "External velocity data (*_x*_y*.csv)")
        Case.the().info.update_last_used_directory(file_name)
        if not file_name:
            return

        basename: str = path.basename(file_name)
        folder: str = path.dirname(file_name)

        # Takes only the filename without the serie data in its name
        self.filesvel_input.setText("{}/{}".format(folder, basename.split("_vel")[0]))

    def on_apply(self):
        """ Saves the data on the dialog into the data structure. """
        self.temp_relaxationzone.start = float(self.start_input.text())
        self.temp_relaxationzone.duration = float(self.duration_input.text())
        self.temp_relaxationzone.depth = float(self.depth_input.text())
        self.temp_relaxationzone.swl = float(self.swl_input.text())
        self.temp_relaxationzone.filesvel = str(self.filesvel_input.text())
        self.temp_relaxationzone.filesvelx_initial = int(self.filesvelx_initial_input.text())
        self.temp_relaxationzone.filesvelx_count = int(self.filesvelx_count_input.text())
        self.temp_relaxationzone.usevelz = bool(self.usevelz_check.isChecked())
        self.temp_relaxationzone.movedata[0] = float(self.movedata_x.text())
        self.temp_relaxationzone.movedata[1] = float(self.movedata_y.text())
        self.temp_relaxationzone.movedata[2] = float(self.movedata_z.text())
        self.temp_relaxationzone.dpz = float(self.dpz_input.text())
        self.temp_relaxationzone.smooth = int(self.smooth_input.text())
        self.temp_relaxationzone.center[0] = float(self.center_x.text())
        self.temp_relaxationzone.center[1] = float(self.center_y.text())
        self.temp_relaxationzone.center[2] = float(self.center_z.text())
        self.temp_relaxationzone.width = float(self.width_input.text())
        self.temp_relaxationzone.coefdir[0] = float(self.coefdir_x.text())
        self.temp_relaxationzone.coefdir[1] = float(self.coefdir_y.text())
        self.temp_relaxationzone.coefdir[2] = float(self.coefdir_z.text())
        self.temp_relaxationzone.coefdt = float(self.coefdt_input.text())
        self.temp_relaxationzone.function_psi = float(self.function_psi_input.text())
        self.temp_relaxationzone.function_beta = float(self.function_beta_input.text())
        self.temp_relaxationzone.driftcorrection = float(self.driftcorrection_input.text())
        self.temp_relaxationzone.driftinitialramp = float(self.driftinitialramp_input.text())
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        """ Deletes the currently represented relaxation zone. """
        self.relaxationzone = None
        self.reject()

    def fill_data(self):
        """ Fills the data from the data structure onto the dialog. """
        self.start_input.setText(str(self.temp_relaxationzone.start))
        self.duration_input.setText(str(self.temp_relaxationzone.duration))
        self.depth_input.setText(str(self.temp_relaxationzone.depth))
        self.swl_input.setText(str(self.temp_relaxationzone.swl))
        self.filesvel_input.setText(str(self.temp_relaxationzone.filesvel))
        self.filesvelx_initial_input.setText(str(self.temp_relaxationzone.filesvelx_initial))
        self.filesvelx_count_input.setText(str(self.temp_relaxationzone.filesvelx_count))
        self.usevelz_check.setChecked(bool(self.temp_relaxationzone.usevelz))
        self.movedata_x.setText(str(self.temp_relaxationzone.movedata[0]))
        self.movedata_y.setText(str(self.temp_relaxationzone.movedata[1]))
        self.movedata_z.setText(str(self.temp_relaxationzone.movedata[2]))
        self.dpz_input.setText(str(self.temp_relaxationzone.dpz))
        self.smooth_input.setText(str(self.temp_relaxationzone.smooth))
        self.center_x.setText(str(self.temp_relaxationzone.center[0]))
        self.center_y.setText(str(self.temp_relaxationzone.center[1]))
        self.center_z.setText(str(self.temp_relaxationzone.center[2]))
        self.width_input.setText(str(self.temp_relaxationzone.width))
        self.coefdir_x.setText(str(self.temp_relaxationzone.coefdir[0]))
        self.coefdir_y.setText(str(self.temp_relaxationzone.coefdir[1]))
        self.coefdir_z.setText(str(self.temp_relaxationzone.coefdir[2]))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))
        self.driftcorrection_input.setText(str(self.temp_relaxationzone.driftcorrection))
        self.driftinitialramp_input.setText(str(self.temp_relaxationzone.driftinitialramp))
