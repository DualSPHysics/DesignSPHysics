#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone Irregular Config Dialog """

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.relaxation_zone.relaxation_zone_irregular import RelaxationZoneIrregular
from mod.enums import IrregularSpectrum, IrregularDiscretization
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.value_input import ValueInput

from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class RelaxationZoneIrregularConfigDialog(QtWidgets.QDialog):
    """ A configuration dialog for a irregular relaxation zone. """

    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneIrregular()
        self.relaxationzone = relaxationzone

        self.main_layout = QtWidgets.QVBoxLayout()
        self.data_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.relaxation_zone_scroll = QtWidgets.QScrollArea()  # "Import VTM options"
        self.relaxation_zone_scroll.setFixedWidth(820)
        self.relaxation_zone_scroll.setWidgetResizable(True)
        self.relaxation_zone_scroll_widget = QtWidgets.QWidget()
        self.relaxation_zone_scroll_widget.setMinimumWidth(820)
        self.relaxation_zone_scroll_widget.setLayout(self.data_layout)

        self.relaxation_zone_scroll.setWidget(self.relaxation_zone_scroll_widget)
        self.relaxation_zone_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setFixedWidth(840)


        self.duration_layout = QtWidgets.QHBoxLayout()
        self.start_label = QtWidgets.QLabel(__("Start time:"))
        self.start_input = TimeInput()
        self.duration_label = QtWidgets.QLabel(__("Duration (0 for end of simulation):"))
        self.duration_input = TimeInput()
        for x in [self.start_label, self.start_input,self.duration_label, self.duration_input]:
            self.duration_layout.addWidget(x)

        self.peakcoef_layout = QtWidgets.QHBoxLayout()
        self.peakcoef_label = QtWidgets.QLabel(__("Peak enhancement coefficient:"))
        self.peakcoef_input = ValueInput()
        for x in [self.peakcoef_label, self.peakcoef_input]:
            self.peakcoef_layout.addWidget(x)

        self.spectrum_layout = QtWidgets.QHBoxLayout()
        self.spectrum_label = QtWidgets.QLabel(__("Spectrum type:"))
        self.spectrum_selector = QtWidgets.QComboBox()
        self.spectrum_selector.insertItems(0, [__("Jonswap"), __("Pierson-Moskowitz")])
        self.discretization_label = QtWidgets.QLabel(__("Spectrum discretization:"))
        self.discretization_selector = QtWidgets.QComboBox()
        self.discretization_selector.insertItems(0, [__("Regular"), __("Random"), __("Stretched"), __("Cosstretched")])
        for x in [self.spectrum_label, self.spectrum_selector,self.discretization_label, self.discretization_selector]:
            self.spectrum_layout.addWidget(x)

        self.waveorder_layout = QtWidgets.QHBoxLayout()
        self.waveorder_label = QtWidgets.QLabel(__("Order wave generation:"))
        self.waveorder_input = QtWidgets.QComboBox()
        self.waveorder_input.addItems(["1st order", "2nd order"])
        for x in [self.waveorder_label, self.waveorder_input]:
            self.waveorder_layout.addWidget(x)

        self.waveheight_layout = QtWidgets.QHBoxLayout()
        self.waveheight_label = QtWidgets.QLabel(__("Wave Height:"))
        self.waveheight_input = SizeInput()
        self.waveperiod_label = QtWidgets.QLabel(__("Wave Period:"))
        self.waveperiod_input = ValueInput()
        for x in [self.waveheight_label, self.waveheight_input,self.waveperiod_label, self.waveperiod_input]:
            self.waveheight_layout.addWidget(x)

        self.waves_layout = QtWidgets.QHBoxLayout()
        self.waves_label = QtWidgets.QLabel(__("Number of waves:"))
        self.waves_input = IntValueInput()
        self.randomseed_label = QtWidgets.QLabel(__("Random seed:"))
        self.randomseed_input = IntValueInput()
        for x in [self.waves_label, self.waves_input,self.randomseed_label, self.randomseed_input]:
            self.waves_layout.addWidget(x)

        self.depth_layout = QtWidgets.QHBoxLayout()
        self.depth_label = QtWidgets.QLabel(__("Water depth:"))
        self.depth_input = SizeInput()
        self.swl_label = QtWidgets.QLabel(__("Still water level:"))
        self.swl_input = SizeInput()
        for x in [self.depth_label, self.depth_input, self.swl_label, self.swl_input]:
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
        self.ramptime_label = QtWidgets.QLabel(__("Time of initial ramp:"))
        self.ramptime_input = TimeInput()
        for x in [self.width_label, self.width_input, self.ramptime_label, self.ramptime_input]:
            self.width_layout.addWidget(x)

        '''self.serieini_layout = QtWidgets.QHBoxLayout()
        self.serieini_label = QtWidgets.QLabel(__("Initial time:"))
        self.serieini_input = ValueInput()
        for x in [self.serieini_label, self.serieini_input]:
            self.serieini_layout.addWidget(x)'''

        self.savemotion_label_layout=QtWidgets.QHBoxLayout()
        self.savemotion_label = QtWidgets.QLabel(__("-------- Save motion data --------"))
        self.savemotion_label_layout.addStretch()
        self.savemotion_label_layout.addWidget(self.savemotion_label)
        self.savemotion_label_layout.addStretch()
        self.savemotion_time_layout = QtWidgets.QHBoxLayout()
        self.savemotion_time_label = QtWidgets.QLabel(__("Time: "))
        self.savemotion_time_input = TimeInput()
        self.savemotion_timedt_label = QtWidgets.QLabel(__("Dt: "))
        self.savemotion_timedt_input = TimeInput()
        for x in [self.savemotion_time_label,
                  self.savemotion_time_input,
                  self.savemotion_timedt_label,
                  self.savemotion_timedt_input]:
            self.savemotion_time_layout.addWidget(x)

        self.savemotion_pos_layout = QtWidgets.QHBoxLayout()
        self.savemotion_xpos_label = QtWidgets.QLabel(__("X Position: "))
        self.savemotion_xpos_input = SizeInput()
        self.savemotion_zpos_label = QtWidgets.QLabel(__("Z Position: "))
        self.savemotion_zpos_input = SizeInput()
        for x in [self.savemotion_xpos_label,
                  self.savemotion_xpos_input,
                  self.savemotion_zpos_label,
                  self.savemotion_zpos_input]:
            self.savemotion_pos_layout.addWidget(x)

        self.saveserie_label_layout = QtWidgets.QHBoxLayout()
        self.saveserie_label = QtWidgets.QLabel(__("-------- Save serie data --------"))
        self.saveserie_label_layout.addStretch()
        self.saveserie_label_layout.addWidget(self.saveserie_label)
        self.saveserie_label_layout.addStretch()
        self.saveserie_time_layout = QtWidgets.QHBoxLayout()
        self.saveserie_timemin_label = QtWidgets.QLabel(__("Time min.: "))
        self.saveserie_timemin_input = TimeInput()
        self.saveserie_timemax_label = QtWidgets.QLabel(__("Time max.: "))
        self.saveserie_timemax_input = TimeInput()
        for x in [self.saveserie_timemin_label,
                  self.saveserie_timemin_input,
                  self.saveserie_timemax_label,
                  self.saveserie_timemax_input]:
            self.saveserie_time_layout.addWidget(x)

        self.saveserie_dt_layout = QtWidgets.QHBoxLayout()
        self.saveserie_timedt_label = QtWidgets.QLabel(__("Dt: "))
        self.saveserie_timedt_input = TimeInput()
        self.saveserie_xpos_label = QtWidgets.QLabel(__("X Position: "))
        self.saveserie_xpos_input = SizeInput()

        for x in [self.saveserie_timedt_label,
                  self.saveserie_timedt_input,
                  self.saveserie_xpos_label,
                  self.saveserie_xpos_input]:
            self.saveserie_dt_layout.addWidget(x)

        self.saveseriewaves_label_layout = QtWidgets.QHBoxLayout()

        self.saveseriewaves_label = QtWidgets.QLabel(__("-------- Save serie heights --------"))
        self.saveseriewaves_label_layout.addStretch()
        self.saveseriewaves_label_layout.addWidget(self.saveseriewaves_label)
        self.saveseriewaves_label_layout.addStretch()
        self.saveseriewaves_layout = QtWidgets.QHBoxLayout()
        self.saveseriewaves_timemin_label = QtWidgets.QLabel(__("Time min.: "))
        self.saveseriewaves_timemin_input = TimeInput()
        self.saveseriewaves_timemax_label = QtWidgets.QLabel(__("Time max.: "))
        self.saveseriewaves_timemax_input = TimeInput()
        for x in [self.saveseriewaves_timemin_label,
                  self.saveseriewaves_timemin_input,
                  self.saveseriewaves_timemax_label,
                  self.saveseriewaves_timemax_input]:
            self.saveseriewaves_layout.addWidget(x)
        self.saveseriewaves_pos_layout = QtWidgets.QHBoxLayout()
        self.saveseriewaves_xpos_label = QtWidgets.QLabel(__("X Position: "))
        self.saveseriewaves_xpos_input = SizeInput()
        self.saveseriewaves_pos_layout.addWidget(self.saveseriewaves_xpos_label)
        self.saveseriewaves_pos_layout.addWidget(self.saveseriewaves_xpos_input)


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
        for x in [self.driftcorrection_label, self.driftcorrection_input]:
            self.driftcorrection_layout.addWidget(x)

        for x in [self.duration_layout,
                  self.peakcoef_layout,
                  self.spectrum_layout,
                  self.waveheight_layout,
                  self.waves_layout,
                  self.depth_layout,
                  self.center_layout,
                  self.width_layout,
                  self.savemotion_label_layout,
                  self.savemotion_time_layout,
                  self.savemotion_pos_layout,
                  self.saveserie_label_layout,
                  self.saveserie_time_layout,
                  self.saveserie_dt_layout,
                  self.saveseriewaves_label_layout,
                  self.saveseriewaves_layout,
                  self.saveseriewaves_pos_layout,
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
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_apply(self):
        """ Applies the data currently introduced into the dialog to the data structure. """
        self.temp_relaxationzone.start = self.start_input.value()
        self.temp_relaxationzone.duration = self.duration_input.value()
        self.temp_relaxationzone.peakcoef = self.peakcoef_input.value()
        self.temp_relaxationzone.spectrum = {0: IrregularSpectrum.JONSWAP, 1: IrregularSpectrum.PIERSON_MOSKOWITZ}[self.spectrum_selector.currentIndex()]
        self.temp_relaxationzone.discretization = {0: IrregularDiscretization.REGULAR, 1: IrregularDiscretization.RANDOM, 2: IrregularDiscretization.STRETCHED, 3: IrregularDiscretization.COSSTRETCHED}[self.discretization_selector.currentIndex()]
        self.temp_relaxationzone.waveorder = self.waveorder_input.currentIndex()+1
        self.temp_relaxationzone.waveheight = self.waveheight_input.value()
        self.temp_relaxationzone.waveperiod = self.waveperiod_input.value()
        self.temp_relaxationzone.waves = self.waves_input.value()
        self.temp_relaxationzone.randomseed = self.waveperiod_input.value()
        self.temp_relaxationzone.depth = self.depth_input.value()
        self.temp_relaxationzone.swl = self.swl_input.value()
        self.temp_relaxationzone.center[0] = self.center_x.value()
        self.temp_relaxationzone.center[1] = self.center_y.value()
        self.temp_relaxationzone.center[2] = self.center_z.value()
        self.temp_relaxationzone.width = self.width_input.value()
        self.temp_relaxationzone.ramptime = self.ramptime_input.value()
        self.temp_relaxationzone.serieini = self.serieini_input.value()
        self.temp_relaxationzone.savemotion_time = self.savemotion_time_input.value()
        self.temp_relaxationzone.savemotion_timedt = self.savemotion_timedt_input.value()
        self.temp_relaxationzone.savemotion_xpos = self.savemotion_xpos_input.value()
        self.temp_relaxationzone.savemotion_zpos = self.savemotion_zpos_input.value()
        self.temp_relaxationzone.saveserie_timemin = self.saveserie_timemin_input.value()
        self.temp_relaxationzone.saveserie_timemax = self.saveserie_timemax_input.value()
        self.temp_relaxationzone.saveserie_timedt = self.saveserie_timedt_input.value()
        self.temp_relaxationzone.saveserie_xpos = self.saveserie_xpos_input.value()
        self.temp_relaxationzone.saveseriewaves_timemin = self.saveseriewaves_timemin_input.value()
        self.temp_relaxationzone.saveseriewaves_timemax = self.saveseriewaves_timemax_input.value()
        self.temp_relaxationzone.saveseriewaves_xpos = self.saveseriewaves_xpos_input.value()
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
        """ Deletes the currently represented object. """
        self.relaxationzone = None
        self.reject()

    def fill_data(self):
        """ Fills the data from the data structure onto the dialog. """
        self.start_input.setValue(self.temp_relaxationzone.start)
        self.duration_input.setValue(self.temp_relaxationzone.duration)
        self.peakcoef_input.setValue(self.temp_relaxationzone.peakcoef)
        self.spectrum_selector.setCurrentIndex({IrregularSpectrum.JONSWAP: 0, IrregularSpectrum.PIERSON_MOSKOWITZ: 1}[self.temp_relaxationzone.spectrum])
        self.discretization_selector.setCurrentIndex({IrregularDiscretization.REGULAR: 0, IrregularDiscretization.RANDOM: 1, IrregularDiscretization.STRETCHED: 2, IrregularDiscretization.COSSTRETCHED: 3}[self.temp_relaxationzone.discretization])
        self.waveorder_input.setCurrentIndex(self.temp_relaxationzone.waveorder-1)
        self.waveheight_input.setValue(self.temp_relaxationzone.waveheight)
        self.waveperiod_input.setValue(self.temp_relaxationzone.waveperiod)
        self.waves_input.setValue(self.temp_relaxationzone.waves)
        self.randomseed_input.setValue(self.temp_relaxationzone.randomseed)
        self.depth_input.setValue(self.temp_relaxationzone.depth)
        self.swl_input.setValue(self.temp_relaxationzone.swl)
        self.center_x.setValue(self.temp_relaxationzone.center[0])
        self.center_y.setValue(self.temp_relaxationzone.center[1])
        self.center_z.setValue(self.temp_relaxationzone.center[2])
        self.width_input.setValue(self.temp_relaxationzone.width)
        self.ramptime_input.setValue(self.temp_relaxationzone.ramptime)
        #self.serieini_input.setValue(self.temp_relaxationzone.serieini)
        self.savemotion_time_input.setValue(self.temp_relaxationzone.savemotion_time)
        self.savemotion_timedt_input.setValue(self.temp_relaxationzone.savemotion_timedt)
        self.savemotion_xpos_input.setValue(self.temp_relaxationzone.savemotion_xpos)
        self.savemotion_zpos_input.setValue(self.temp_relaxationzone.savemotion_zpos)
        self.saveserie_timemin_input.setValue(self.temp_relaxationzone.saveserie_timemin)
        self.saveserie_timemax_input.setValue(self.temp_relaxationzone.saveserie_timemax)
        self.saveserie_timedt_input.setValue(self.temp_relaxationzone.saveserie_timedt)
        self.saveserie_xpos_input.setValue(self.temp_relaxationzone.saveserie_xpos)
        self.saveseriewaves_timemin_input.setValue(self.temp_relaxationzone.saveseriewaves_timemin)
        self.saveseriewaves_timemax_input.setValue(self.temp_relaxationzone.saveseriewaves_timemax)
        self.saveseriewaves_xpos_input.setValue(self.temp_relaxationzone.saveseriewaves_xpos)
        self.coefdir_x.setValue(self.temp_relaxationzone.coefdir[0])
        self.coefdir_y.setValue(self.temp_relaxationzone.coefdir[1])
        self.coefdir_z.setValue(self.temp_relaxationzone.coefdir[2])
        self.coefdt_input.setValue(self.temp_relaxationzone.coefdt)
        self.function_psi_input.setValue(self.temp_relaxationzone.function_psi)
        self.function_beta_input.setValue(self.temp_relaxationzone.function_beta)
        self.driftcorrection_input.setValue(self.temp_relaxationzone.driftcorrection)
