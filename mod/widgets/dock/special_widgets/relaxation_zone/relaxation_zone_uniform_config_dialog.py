#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone Uniform Config Dialog. """

from PySide2 import QtWidgets
from mod.dataobjects.relaxation_zone.relaxation_zone_uniform import RelaxationZoneUniform
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput
from mod.widgets.dock.special_widgets.relaxation_zone.velocity_times_dialog import VelocityTimesDialog


class RelaxationZoneUniformConfigDialog(QtWidgets.QDialog):
    """ A configuration dialog for a uniform relaxation zone. """
    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneUniform()
        self.relaxationzone = relaxationzone
        self.velocity_times = list()
        self.velocity_times_dialog = VelocityTimesDialog(self.temp_relaxationzone, parent=None)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.data_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.start_layout = QtWidgets.QHBoxLayout()
        self.start_label = QtWidgets.QLabel(__("Start time:"))
        self.start_input = TimeInput()
        self.duration_label = QtWidgets.QLabel(__("Duration (0 for end of simulation):"))
        self.duration_input = TimeInput()
        for x in [self.start_label, self.start_input, self.duration_label, self.duration_input]:
            self.start_layout.addWidget(x)

        self.domainbox_groupbox = QtWidgets.QGroupBox(__("Domain Box"))
        self.domainbox_layout = QtWidgets.QVBoxLayout()

        self.domainbox_point_layout = QtWidgets.QHBoxLayout()
        self.domainbox_point_label = QtWidgets.QLabel(__("Point [X, Y, Z]: "))
        self.domainbox_point_x = SizeInput()
        self.domainbox_point_y = SizeInput()
        self.domainbox_point_z = SizeInput()
        for x in [self.domainbox_point_label,
                  self.domainbox_point_x,
                  self.domainbox_point_y,
                  self.domainbox_point_z]:
            self.domainbox_point_layout.addWidget(x)
        self.domainbox_layout.addLayout(self.domainbox_point_layout)

        self.domainbox_size_layout = QtWidgets.QHBoxLayout()
        self.domainbox_size_label = QtWidgets.QLabel(__("Size [X, Y, Z]: "))
        self.domainbox_size_x = SizeInput()
        self.domainbox_size_y = SizeInput()
        self.domainbox_size_z = SizeInput()
        for x in [self.domainbox_size_label,
                  self.domainbox_size_x,
                  self.domainbox_size_y,
                  self.domainbox_size_z]:
            self.domainbox_size_layout.addWidget(x)
        self.domainbox_layout.addLayout(self.domainbox_size_layout)

        #TODO: Different way to choose direction?? (only one vector can be nonzero)
        self.domainbox_direction_layout = QtWidgets.QHBoxLayout()
        self.domainbox_direction_label = QtWidgets.QLabel(__("Direction [X, Y, Z]: "))
        self.domainbox_direction_x = ValueInput()
        self.domainbox_direction_y = ValueInput()
        self.domainbox_direction_z = ValueInput()
        for x in [self.domainbox_direction_label,
                  self.domainbox_direction_x,
                  self.domainbox_direction_y,
                  self.domainbox_direction_z]:
            self.domainbox_direction_layout.addWidget(x)
        self.domainbox_layout.addLayout(self.domainbox_direction_layout)

        self.domainbox_groupbox.setLayout(self.domainbox_layout)

        self.use_velocity_check = QtWidgets.QCheckBox(__("Use Velocity (Uncheck for velocity in time)"))

        self.velocity_layout = QtWidgets.QHBoxLayout()
        self.velocity_label = QtWidgets.QLabel(__("Velocity: "))
        self.velocity_input = VelocityInput()
        for x in [self.velocity_label,
                  self.velocity_input]:
            self.velocity_layout.addWidget(x)

        self.velocity_times_button = QtWidgets.QPushButton(__("Edit velocity in time"))

        self.coefdt_layout = QtWidgets.QHBoxLayout()
        self.coefdt_label = QtWidgets.QLabel(__("Multiplier for dt:"))
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

        for x in [self.start_layout]:
            self.data_layout.addLayout(x)

        self.data_layout.addWidget(self.domainbox_groupbox)
        self.data_layout.addWidget(self.use_velocity_check)
        self.data_layout.addWidget(self.velocity_times_button)

        for x in [self.velocity_layout, self.coefdt_layout, self.function_label_layout,self.function_layout]:
            self.data_layout.addLayout(x)

        self.delete_button = QtWidgets.QPushButton(__("Delete RZ configuration"))
        self.apply_button = QtWidgets.QPushButton(__("Apply this configuration"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addLayout(self.data_layout)
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
        self.temp_relaxationzone.start = self.start_input.value()
        self.temp_relaxationzone.duration = self.duration_input.value()
        self.temp_relaxationzone.domainbox_point = [
            self.domainbox_point_x.value(),
            self.domainbox_point_y.value(),
            self.domainbox_point_z.value()]
        self.temp_relaxationzone.domainbox_size = [
            self.domainbox_size_x.value(),
            self.domainbox_size_y.value(),
            self.domainbox_size_z.value()]
        self.temp_relaxationzone.domainbox_direction = [
            self.domainbox_direction_x.value(),
            self.domainbox_direction_y.value(),
            self.domainbox_direction_z.value()]
        self.temp_relaxationzone.use_velocity = bool(self.use_velocity_check.isChecked())
        self.temp_relaxationzone.velocity = self.velocity_input.value()
        self.temp_relaxationzone.velocity_times = self.velocity_times
        self.temp_relaxationzone.coefdt = self.coefdt_input.value()
        self.temp_relaxationzone.function_psi = self.function_psi_input.value()
        self.temp_relaxationzone.function_beta = self.function_beta_input.value()
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        """ Deletes the currently represented relaxation zone. """
        self.relaxationzone = None
        self.reject()

    def on_velocity_times(self):
        """ Reacts to the velocity times button being pressed to configure the velocity times. """
        result = self.velocity_times_dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            self.velocity_times = self.velocity_times_dialog.velocity_times

    def on_velocity_check(self):
        """ Reacts to the velocity checkbox enabling/disabling velocity times and input. """
        self.velocity_times_button.setEnabled(not self.use_velocity_check.isChecked())
        self.velocity_input.setEnabled(self.use_velocity_check.isChecked())

    def fill_data(self):
        """ Fills the data from the data structure onto the dialog. """
        self.start_input.setValue(self.temp_relaxationzone.start)
        self.duration_input.setValue(self.temp_relaxationzone.duration)
        self.domainbox_point_x.setValue(self.temp_relaxationzone.domainbox_point[0])
        self.domainbox_point_y.setValue(self.temp_relaxationzone.domainbox_point[1])
        self.domainbox_point_z.setValue(self.temp_relaxationzone.domainbox_point[2])
        self.domainbox_size_x.setValue(self.temp_relaxationzone.domainbox_size[0])
        self.domainbox_size_y.setValue(self.temp_relaxationzone.domainbox_size[1])
        self.domainbox_size_z.setValue(self.temp_relaxationzone.domainbox_size[2])
        self.domainbox_direction_x.setValue(self.temp_relaxationzone.domainbox_direction[0])
        self.domainbox_direction_y.setValue(self.temp_relaxationzone.domainbox_direction[1])
        self.domainbox_direction_z.setValue(self.temp_relaxationzone.domainbox_direction[2])
        self.use_velocity_check.setChecked(bool(self.temp_relaxationzone.use_velocity))
        self.velocity_input.setValue(self.temp_relaxationzone.velocity)
        self.coefdt_input.setValue(self.temp_relaxationzone.coefdt)
        self.function_psi_input.setValue(self.temp_relaxationzone.function_psi)
        self.function_beta_input.setValue(self.temp_relaxationzone.function_beta)
