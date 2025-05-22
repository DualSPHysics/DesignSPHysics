#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone Regular Config Dialog. """

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.relaxation_zone.relaxation_zone_regular import RelaxationZoneRegular
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput

from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class RelaxationZoneRegularConfigDialog(QtWidgets.QDialog):
    """ A configuration dialog for a regular relaxation zone. """

    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneRegular()
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
        for x in [self.start_label, self.start_input,self.duration_label, self.duration_input]:
            self.start_layout.addWidget(x)

        self.waveorder_layout = QtWidgets.QHBoxLayout()
        self.waveorder_label = QtWidgets.QLabel(__("Order wave generation:"))
        self.waveorder_input = QtWidgets.QComboBox()
        self.waveorder_input.addItems(["1st order","2nd order"])
        for x in [self.waveorder_label, self.waveorder_input]:
            self.waveorder_layout.addWidget(x)

        self.waveheight_layout = QtWidgets.QHBoxLayout()
        self.waveheight_label = QtWidgets.QLabel(__("Wave Height:"))
        self.waveheight_input = SizeInput()
        self.waveperiod_label = QtWidgets.QLabel(__("Wave Period:"))
        self.waveperiod_input = ValueInput()
        for x in [self.waveheight_label, self.waveheight_input,self.waveperiod_label, self.waveperiod_input]:
            self.waveheight_layout.addWidget(x)

        self.depth_layout = QtWidgets.QHBoxLayout()
        self.depth_label = QtWidgets.QLabel(__("Water depth:"))
        self.depth_input = SizeInput()
        self.swl_label = QtWidgets.QLabel(__("Still water level:"))
        self.swl_input = SizeInput()
        for x in [self.depth_label, self.depth_input,self.swl_label, self.swl_input]:
            self.depth_layout.addWidget(x)

        self.center_layout = QtWidgets.QHBoxLayout()
        self.center_label = QtWidgets.QLabel(__("Central point (X, Y, Z):"))
        self.center_x = SizeInput()
        self.center_y = SizeInput()
        self.center_z = SizeInput()
        for x in [self.center_label, self.center_x, self.center_y, self.center_z]:
            self.center_layout.addWidget(x)

        self.width_layout = QtWidgets.QHBoxLayout()
        self.width_label = QtWidgets.QLabel(__("Width for generation:"))
        self.width_input = SizeInput()
        self.phase_layout = QtWidgets.QHBoxLayout()
        self.phase_label = QtWidgets.QLabel(__("Initial wave phase:"))
        self.phase_input = ValueInput()
        for x in [self.width_label, self.width_input,self.phase_label, self.phase_input]:
            self.width_layout.addWidget(x)

        self.ramp_layout=QtWidgets.QHBoxLayout()
        self.ramp_label = QtWidgets.QLabel(__("Periods of ramp:"))
        self.ramp_input = ValueInput()
        for x in [self.ramp_label, self.ramp_input]:
            self.ramp_layout.addWidget(x)


        self.savemotion_groupbox=QtWidgets.QGroupBox(__("SaveMotion"))
        self.savemotion_layout = QtWidgets.QVBoxLayout()
        self.savemotion_periods_layout = QtWidgets.QHBoxLayout()
        self.savemotion_periods_label = QtWidgets.QLabel(__("Periods: "))
        self.savemotion_periods_input = IntValueInput()
        self.savemotion_periodsteps_label = QtWidgets.QLabel(__("Period steps: "))
        self.savemotion_periodsteps_input = IntValueInput()
        self.savemotion_pos_layout = QtWidgets.QHBoxLayout()
        self.savemotion_xpos_label = QtWidgets.QLabel(__("X Position: "))
        self.savemotion_xpos_input = SizeInput()
        self.savemotion_zpos_label = QtWidgets.QLabel(__("Z Position: "))
        self.savemotion_zpos_input = SizeInput()
        for x in [self.savemotion_periods_label,
                  self.savemotion_periods_input,
                  self.savemotion_periodsteps_label,
                  self.savemotion_periodsteps_input ]:
            self.savemotion_periods_layout.addWidget(x)
        for x in [self.savemotion_xpos_label,
                  self.savemotion_xpos_input,
                  self.savemotion_zpos_label,
                  self.savemotion_zpos_input]:
            self.savemotion_pos_layout.addWidget(x)
        self.savemotion_layout.addLayout(self.savemotion_periods_layout)
        self.savemotion_layout.addLayout(self.savemotion_pos_layout)
        self.savemotion_groupbox.setLayout(self.savemotion_layout)

        self.coefdir_layout = QtWidgets.QHBoxLayout()
        self.coefdir_label = QtWidgets.QLabel(__("Direction coefficient (X, Y, Z):"))
        self.coefdir_x = ValueInput()
        self.coefdir_x.setEnabled(False) #WHY?
        self.coefdir_y = ValueInput()
        self.coefdir_y.setEnabled(False)
        self.coefdir_z = ValueInput()
        self.coefdir_z.setEnabled(False)
        for x in [self.coefdir_label, self.coefdir_x, self.coefdir_y, self.coefdir_z]:
            self.coefdir_layout.addWidget(x)

        self.coefdt_layout = QtWidgets.QHBoxLayout()
        self.coefdt_label = QtWidgets.QLabel(__("Multiplier for dt:"))
        self.coefdt_input = ValueInput()
        self.coefdt_input.setEnabled(False)
        for x in [self.coefdt_label, self.coefdt_input]:
            self.coefdt_layout.addWidget(x)

        self.function_layout = QtWidgets.QHBoxLayout()
        self.function_psi_label = QtWidgets.QLabel(__("Coef Psi: "))
        self.function_psi_input = ValueInput()
        self.function_beta_label = QtWidgets.QLabel(__("Coef Beta: "))
        self.function_beta_input = ValueInput()
        for x in [self.function_psi_label,
                  self.function_psi_input,
                  self.function_beta_label,
                  self.function_beta_input]:
            self.function_layout.addWidget(x)

        self.driftcorrection_layout = QtWidgets.QHBoxLayout()
        self.driftcorrection_label = QtWidgets.QLabel(__("Drift correction coef (for X):"))
        self.driftcorrection_input = ValueInput()
        for x in [self.driftcorrection_label, self.driftcorrection_input]:
            self.driftcorrection_layout.addWidget(x)

        for x in [self.start_layout,
                  self.waveorder_layout,
                  self.waveheight_layout,
                  self.depth_layout,
                  self.center_layout,
                  self.width_layout,
                  self.ramp_layout]:
            self.data_layout.addLayout(x)
        self.data_layout.addWidget(self.savemotion_groupbox)
        for x in [self.coefdir_layout,
                  self.coefdt_layout,
                  self.function_layout,
                  self.driftcorrection_layout]:
            self.data_layout.addLayout(x)

        self.delete_button = QtWidgets.QPushButton(__("Delete RZ configuration"))
        self.apply_button = QtWidgets.QPushButton(__("Apply this configuration"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addWidget(self.relaxation_zone_scroll)
        #self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)
        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_apply(self):
        """ Saves the current dialog data into the data structure. """
        self.temp_relaxationzone.start = self.start_input.value()
        self.temp_relaxationzone.duration = self.duration_input.value()
        self.temp_relaxationzone.waveorder = self.waveorder_input.currentIndex()+1
        self.temp_relaxationzone.waveheight = self.waveheight_input.value()
        self.temp_relaxationzone.waveperiod = self.waveperiod_input.value()
        self.temp_relaxationzone.depth = self.depth_input.value()
        self.temp_relaxationzone.swl = self.swl_input.value()
        self.temp_relaxationzone.center[0] = self.center_x.value()
        self.temp_relaxationzone.center[1] = self.center_y.value()
        self.temp_relaxationzone.center[2] = self.center_z.value()
        self.temp_relaxationzone.width = self.width_input.value()
        self.temp_relaxationzone.phase = self.phase_input.value()
        self.temp_relaxationzone.ramp = self.ramp_input.value()
        self.temp_relaxationzone.savemotion_periods = self.savemotion_periods_input.value()
        self.temp_relaxationzone.savemotion_periodsteps = self.savemotion_periodsteps_input.value()
        self.temp_relaxationzone.savemotion_xpos = self.savemotion_xpos_input.value()
        self.temp_relaxationzone.savemotion_zpos = self.savemotion_zpos_input.value()
        self.temp_relaxationzone.coefdir[0] = self.coefdir_x.value()
        self.temp_relaxationzone.coefdir[1] = self.coefdir_y.value()
        self.temp_relaxationzone.coefdir[2] = self.coefdir_z.value()
        self.temp_relaxationzone.coefdt = self.coefdt_input.value()
        self.temp_relaxationzone.function_psi = self.function_psi_input.value()
        self.temp_relaxationzone.function_beta = self.function_beta_input.value()
        self.temp_relaxationzone.driftcorrection = self.driftcorrection_input.value()
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
        self.waveorder_input.setCurrentIndex(self.temp_relaxationzone.waveorder-1)
        self.waveheight_input.setValue(self.temp_relaxationzone.waveheight)
        self.waveperiod_input.setValue(self.temp_relaxationzone.waveperiod)
        self.depth_input.setValue(self.temp_relaxationzone.depth)
        self.swl_input.setValue(self.temp_relaxationzone.swl)
        self.center_x.setValue(self.temp_relaxationzone.center[0])
        self.center_y.setValue(self.temp_relaxationzone.center[1])
        self.center_z.setValue(self.temp_relaxationzone.center[2])
        self.width_input.setValue(self.temp_relaxationzone.width)
        self.phase_input.setValue(self.temp_relaxationzone.phase)
        self.ramp_input.setValue(self.temp_relaxationzone.ramp)
        self.savemotion_periods_input.setValue(self.temp_relaxationzone.savemotion_periods)
        self.savemotion_periodsteps_input.setValue(self.temp_relaxationzone.savemotion_periodsteps)
        self.savemotion_xpos_input.setValue(self.temp_relaxationzone.savemotion_xpos)
        self.savemotion_zpos_input.setValue(self.temp_relaxationzone.savemotion_zpos)
        self.coefdir_x.setValue(self.temp_relaxationzone.coefdir[0])
        self.coefdir_y.setValue(self.temp_relaxationzone.coefdir[1])
        self.coefdir_z.setValue(self.temp_relaxationzone.coefdir[2])
        self.coefdt_input.setValue(self.temp_relaxationzone.coefdt)
        self.function_psi_input.setValue(self.temp_relaxationzone.function_psi)
        self.function_beta_input.setValue(self.temp_relaxationzone.function_beta)
        self.driftcorrection_input.setValue(self.temp_relaxationzone.driftcorrection)
