#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone Uniform Config Dialog. """

from PySide import QtGui

from mod.translation_tools import __
from mod.freecad_tools import get_fc_main_window

from mod.widgets.velocity_times_dialog import VelocityTimesDialog

from mod.dataobjects.relaxation_zone_uniform import RelaxationZoneUniform


class RelaxationZoneUniformConfigDialog(QtGui.QDialog):
    """ A configuration dialog for a uniform relaxation zone. """
    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneUniform()
        self.relaxationzone = relaxationzone
        self.velocity_times = list()
        self.velocity_times_dialog = VelocityTimesDialog(self.temp_relaxationzone, parent=get_fc_main_window())

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

        self.domainbox_groupbox = QtGui.QGroupBox(__("Domain Box"))
        self.domainbox_layout = QtGui.QVBoxLayout()

        self.domainbox_point_layout = QtGui.QHBoxLayout()
        self.domainbox_point_label = QtGui.QLabel(__("Point [X, Y, Z] (m): "))
        self.domainbox_point_x = QtGui.QLineEdit()
        self.domainbox_point_y = QtGui.QLineEdit()
        self.domainbox_point_z = QtGui.QLineEdit()
        for x in [self.domainbox_point_label,
                  self.domainbox_point_x,
                  self.domainbox_point_y,
                  self.domainbox_point_z]:
            self.domainbox_point_layout.addWidget(x)
        self.domainbox_layout.addLayout(self.domainbox_point_layout)

        self.domainbox_size_layout = QtGui.QHBoxLayout()
        self.domainbox_size_label = QtGui.QLabel(__("Size [X, Y, Z] (m): "))
        self.domainbox_size_x = QtGui.QLineEdit()
        self.domainbox_size_y = QtGui.QLineEdit()
        self.domainbox_size_z = QtGui.QLineEdit()
        for x in [self.domainbox_size_label,
                  self.domainbox_size_x,
                  self.domainbox_size_y,
                  self.domainbox_size_z]:
            self.domainbox_size_layout.addWidget(x)
        self.domainbox_layout.addLayout(self.domainbox_size_layout)

        self.domainbox_direction_layout = QtGui.QHBoxLayout()
        self.domainbox_direction_label = QtGui.QLabel(__("Direction [X, Y, Z] (m): "))
        self.domainbox_direction_x = QtGui.QLineEdit()
        self.domainbox_direction_y = QtGui.QLineEdit()
        self.domainbox_direction_z = QtGui.QLineEdit()
        for x in [self.domainbox_direction_label,
                  self.domainbox_direction_x,
                  self.domainbox_direction_y,
                  self.domainbox_direction_z]:
            self.domainbox_direction_layout.addWidget(x)
        self.domainbox_layout.addLayout(self.domainbox_direction_layout)

        self.domainbox_groupbox.setLayout(self.domainbox_layout)

        self.use_velocity_check = QtGui.QCheckBox(__("Use Velocity (Uncheck for velocity in time)"))

        self.velocity_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel(__("Velocity: "))
        self.velocity_input = QtGui.QLineEdit()
        for x in [self.velocity_label,
                  self.velocity_input]:
            self.velocity_layout.addWidget(x)

        self.velocity_times_button = QtGui.QPushButton(__("Edit velocity in time"))

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

        for x in [self.start_layout, self.duration_layout]:
            self.data_layout.addLayout(x)

        self.data_layout.addWidget(self.domainbox_groupbox)
        self.data_layout.addWidget(self.use_velocity_check)
        self.data_layout.addWidget(self.velocity_times_button)

        for x in [self.velocity_layout, self.coefdt_layout, self.function_layout]:
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
        self.use_velocity_check.stateChanged.connect(self.on_velocity_check)
        self.velocity_times_button.clicked.connect(self.on_velocity_times)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.on_velocity_check()
        self.exec_()

    def on_apply(self):
        """ Applies the data from the dialog to the data structure. """
        self.temp_relaxationzone.start = float(self.start_input.text())
        self.temp_relaxationzone.duration = float(self.duration_input.text())
        self.temp_relaxationzone.domainbox_point = [
            float(self.domainbox_point_x.text()),
            float(self.domainbox_point_y.text()),
            float(self.domainbox_point_z.text())]
        self.temp_relaxationzone.domainbox_size = [
            float(self.domainbox_size_x.text()),
            float(self.domainbox_size_y.text()),
            float(self.domainbox_size_z.text())]
        self.temp_relaxationzone.domainbox_direction = [
            float(self.domainbox_direction_x.text()),
            float(self.domainbox_direction_y.text()),
            float(self.domainbox_direction_z.text())]
        self.temp_relaxationzone.use_velocity = bool(self.use_velocity_check.isChecked())
        self.temp_relaxationzone.velocity = float(self.velocity_input.text())
        self.temp_relaxationzone.velocity_times = self.velocity_times
        self.temp_relaxationzone.coefdt = float(self.coefdt_input.text())
        self.temp_relaxationzone.function_psi = float(self.function_psi_input.text())
        self.temp_relaxationzone.function_beta = float(self.function_beta_input.text())
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        """ Deletes the currently represented relaxation zone. """
        self.relaxationzone = None
        self.reject()

    def on_velocity_times(self):
        """ Reacts to the velocity times button being pressed to configure the velocity times. """
        result = self.velocity_times_dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            self.velocity_times = self.velocity_times_dialog.velocity_times

    def on_velocity_check(self):
        """ Reacts to the velocity checkbox enabling/disabling velocity times and input. """
        self.velocity_times_button.setEnabled(not self.use_velocity_check.isChecked())
        self.velocity_input.setEnabled(self.use_velocity_check.isChecked())

    def fill_data(self):
        """ Fills the data from the data structure onto the dialog. """
        self.start_input.setText(str(self.temp_relaxationzone.start))
        self.duration_input.setText(str(self.temp_relaxationzone.duration))
        self.domainbox_point_x.setText(str(self.temp_relaxationzone.domainbox_point[0]))
        self.domainbox_point_y.setText(str(self.temp_relaxationzone.domainbox_point[1]))
        self.domainbox_point_z.setText(str(self.temp_relaxationzone.domainbox_point[2]))
        self.domainbox_size_x.setText(str(self.temp_relaxationzone.domainbox_size[0]))
        self.domainbox_size_y.setText(str(self.temp_relaxationzone.domainbox_size[1]))
        self.domainbox_size_z.setText(str(self.temp_relaxationzone.domainbox_size[2]))
        self.domainbox_direction_x.setText(str(self.temp_relaxationzone.domainbox_direction[0]))
        self.domainbox_direction_y.setText(str(self.temp_relaxationzone.domainbox_direction[1]))
        self.domainbox_direction_z.setText(str(self.temp_relaxationzone.domainbox_direction[2]))
        self.use_velocity_check.setChecked(bool(self.temp_relaxationzone.use_velocity))
        self.velocity_input.setText(str(self.temp_relaxationzone.velocity))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))
