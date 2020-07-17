#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Relaxation Zone Irregular Config Dialog """

from PySide import QtGui

from mod.translation_tools import __

from mod.enums import IrregularSpectrum, IrregularDiscretization

from mod.dataobjects.relaxation_zone_irregular import RelaxationZoneIrregular


class RelaxationZoneIrregularConfigDialog(QtGui.QDialog):
    """ A configuration dialog for a irregular relaxation zone. """

    def __init__(self, relaxationzone=None, parent=None):
        super().__init__(parent=parent)
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneIrregular()
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

        self.peakcoef_layout = QtGui.QHBoxLayout()
        self.peakcoef_label = QtGui.QLabel(__("Peak enhancement coefficient:"))
        self.peakcoef_input = QtGui.QLineEdit()
        for x in [self.peakcoef_label, self.peakcoef_input]:
            self.peakcoef_layout.addWidget(x)

        self.spectrum_layout = QtGui.QHBoxLayout()
        self.spectrum_label = QtGui.QLabel(__("Spectrum type:"))
        self.spectrum_selector = QtGui.QComboBox()
        self.spectrum_selector.insertItems(0, [__("Jonswap"), __("Pierson-Moskowitz")])
        for x in [self.spectrum_label, self.spectrum_selector]:
            self.spectrum_layout.addWidget(x)

        self.discretization_layout = QtGui.QHBoxLayout()
        self.discretization_label = QtGui.QLabel(__("Spectrum discretization:"))
        self.discretization_selector = QtGui.QComboBox()
        self.discretization_selector.insertItems(0, [__("Regular"), __("Random"), __("Stretched"), __("Cosstretched")])
        for x in [self.discretization_label, self.discretization_selector]:
            self.discretization_layout.addWidget(x)

        self.waveorder_layout = QtGui.QHBoxLayout()
        self.waveorder_label = QtGui.QLabel(__("Order wave generation:"))
        self.waveorder_input = QtGui.QLineEdit()
        for x in [self.waveorder_label, self.waveorder_input]:
            self.waveorder_layout.addWidget(x)

        self.waveheight_layout = QtGui.QHBoxLayout()
        self.waveheight_label = QtGui.QLabel(__("Wave Height:"))
        self.waveheight_input = QtGui.QLineEdit()
        for x in [self.waveheight_label, self.waveheight_input]:
            self.waveheight_layout.addWidget(x)

        self.waveperiod_layout = QtGui.QHBoxLayout()
        self.waveperiod_label = QtGui.QLabel(__("Wave Period:"))
        self.waveperiod_input = QtGui.QLineEdit()
        for x in [self.waveperiod_label, self.waveperiod_input]:
            self.waveperiod_layout.addWidget(x)

        self.waves_layout = QtGui.QHBoxLayout()
        self.waves_label = QtGui.QLabel(__("Number of waves:"))
        self.waves_input = QtGui.QLineEdit()
        for x in [self.waves_label, self.waves_input]:
            self.waves_layout.addWidget(x)

        self.randomseed_layout = QtGui.QHBoxLayout()
        self.randomseed_label = QtGui.QLabel(__("Random seed:"))
        self.randomseed_input = QtGui.QLineEdit()
        for x in [self.randomseed_label, self.randomseed_input]:
            self.randomseed_layout.addWidget(x)

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

        self.ramptime_layout = QtGui.QHBoxLayout()
        self.ramptime_label = QtGui.QLabel(__("Time of initial ramp:"))
        self.ramptime_input = QtGui.QLineEdit()
        for x in [self.ramptime_label, self.ramptime_input]:
            self.ramptime_layout.addWidget(x)

        self.serieini_layout = QtGui.QHBoxLayout()
        self.serieini_label = QtGui.QLabel(__("Initial time:"))
        self.serieini_input = QtGui.QLineEdit()
        for x in [self.serieini_label, self.serieini_input]:
            self.serieini_layout.addWidget(x)

        self.savemotion_layout = QtGui.QHBoxLayout()
        self.savemotion_label = QtGui.QLabel(__("Save motion data ->"))
        self.savemotion_time_label = QtGui.QLabel(__("Time: "))
        self.savemotion_time_input = QtGui.QLineEdit()
        self.savemotion_timedt_label = QtGui.QLabel(__("Time data: "))
        self.savemotion_timedt_input = QtGui.QLineEdit()
        self.savemotion_xpos_label = QtGui.QLabel(__("X Position: "))
        self.savemotion_xpos_input = QtGui.QLineEdit()
        self.savemotion_zpos_label = QtGui.QLabel(__("Z Position: "))
        self.savemotion_zpos_input = QtGui.QLineEdit()
        for x in [self.savemotion_label,
                  self.savemotion_time_label,
                  self.savemotion_time_input,
                  self.savemotion_timedt_label,
                  self.savemotion_timedt_input,
                  self.savemotion_xpos_label,
                  self.savemotion_xpos_input,
                  self.savemotion_zpos_label,
                  self.savemotion_zpos_input]:
            self.savemotion_layout.addWidget(x)

        self.saveserie_layout = QtGui.QHBoxLayout()
        self.saveserie_label = QtGui.QLabel(__("Save serie data ->"))
        self.saveserie_timemin_label = QtGui.QLabel(__("Time min.: "))
        self.saveserie_timemin_input = QtGui.QLineEdit()
        self.saveserie_timemax_label = QtGui.QLabel(__("Time max.: "))
        self.saveserie_timemax_input = QtGui.QLineEdit()
        self.saveserie_timedt_label = QtGui.QLabel(__("Time max.: "))
        self.saveserie_timedt_input = QtGui.QLineEdit()
        self.saveserie_xpos_label = QtGui.QLabel(__("X Position: "))
        self.saveserie_xpos_input = QtGui.QLineEdit()
        for x in [self.saveserie_label,
                  self.saveserie_timemin_label,
                  self.saveserie_timemin_input,
                  self.saveserie_timemax_label,
                  self.saveserie_timemax_input,
                  self.saveserie_timedt_label,
                  self.saveserie_timedt_input,
                  self.saveserie_xpos_label,
                  self.saveserie_xpos_input]:
            self.saveserie_layout.addWidget(x)

        self.saveseriewaves_layout = QtGui.QHBoxLayout()
        self.saveseriewaves_label = QtGui.QLabel(__("Save serie heights ->"))
        self.saveseriewaves_timemin_label = QtGui.QLabel(__("Time min.: "))
        self.saveseriewaves_timemin_input = QtGui.QLineEdit()
        self.saveseriewaves_timemax_label = QtGui.QLabel(__("Time max.: "))
        self.saveseriewaves_timemax_input = QtGui.QLineEdit()
        self.saveseriewaves_xpos_label = QtGui.QLabel(__("X Position: "))
        self.saveseriewaves_xpos_input = QtGui.QLineEdit()
        for x in [self.saveseriewaves_label,
                  self.saveseriewaves_timemin_label,
                  self.saveseriewaves_timemin_input,
                  self.saveseriewaves_timemax_label,
                  self.saveseriewaves_timemax_input,
                  self.saveseriewaves_xpos_label,
                  self.saveseriewaves_xpos_input]:
            self.saveseriewaves_layout.addWidget(x)

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

        for x in [self.start_layout,
                  self.duration_layout,
                  self.peakcoef_layout,
                  self.spectrum_layout,
                  self.discretization_layout,
                  self.waveorder_layout,
                  self.waveheight_layout,
                  self.waveperiod_layout,
                  self.waves_layout,
                  self.randomseed_layout,
                  self.depth_layout,
                  self.swl_layout,
                  self.center_layout,
                  self.width_layout,
                  self.ramptime_layout,
                  self.savemotion_layout,
                  self.saveserie_layout,
                  self.saveseriewaves_layout,
                  self.coefdir_layout,
                  self.coefdt_layout,
                  self.function_layout,
                  self.driftcorrection_layout]:
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
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_apply(self):
        """ Applies the data currently introduced into the dialog to the data structure. """
        self.temp_relaxationzone.start = float(self.start_input.text())
        self.temp_relaxationzone.duration = float(self.duration_input.text())
        self.temp_relaxationzone.peakcoef = float(self.peakcoef_input.text())
        self.temp_relaxationzone.spectrum = {0: IrregularSpectrum.JONSWAP, 1: IrregularSpectrum.PIERSON_MOSKOWITZ}[self.spectrum_selector.currentIndex()]
        self.temp_relaxationzone.discretization = {0: IrregularDiscretization.REGULAR, 1: IrregularDiscretization.RANDOM, 2: IrregularDiscretization.STRETCHED, 3: IrregularDiscretization.COSSTRETCHED}[self.discretization_selector.currentIndex()]
        self.temp_relaxationzone.waveorder = float(self.waveorder_input.text())
        self.temp_relaxationzone.waveheight = float(self.waveheight_input.text())
        self.temp_relaxationzone.waveperiod = float(self.waveperiod_input.text())
        self.temp_relaxationzone.waves = float(self.waves_input.text())
        self.temp_relaxationzone.randomseed = float(self.waveperiod_input.text())
        self.temp_relaxationzone.depth = float(self.depth_input.text())
        self.temp_relaxationzone.swl = float(self.swl_input.text())
        self.temp_relaxationzone.center[0] = float(self.center_x.text())
        self.temp_relaxationzone.center[1] = float(self.center_y.text())
        self.temp_relaxationzone.center[2] = float(self.center_z.text())
        self.temp_relaxationzone.width = float(self.width_input.text())
        self.temp_relaxationzone.ramptime = float(self.ramptime_input.text())
        self.temp_relaxationzone.serieini = float(self.serieini_input.text())
        self.temp_relaxationzone.savemotion_time = float(self.savemotion_time_input.text())
        self.temp_relaxationzone.savemotion_timedt = float(self.savemotion_timedt_input.text())
        self.temp_relaxationzone.savemotion_xpos = float(self.savemotion_xpos_input.text())
        self.temp_relaxationzone.savemotion_zpos = float(self.savemotion_zpos_input.text())
        self.temp_relaxationzone.saveserie_timemin = float(self.saveserie_timemin_input.text())
        self.temp_relaxationzone.saveserie_timemax = float(self.saveserie_timemax_input.text())
        self.temp_relaxationzone.saveserie_timedt = float(self.saveserie_timedt_input.text())
        self.temp_relaxationzone.saveserie_xpos = float(self.saveserie_xpos_input.text())
        self.temp_relaxationzone.saveseriewaves_timemin = float(self.saveseriewaves_timemin_input.text())
        self.temp_relaxationzone.saveseriewaves_timemax = float(self.saveseriewaves_timemax_input.text())
        self.temp_relaxationzone.saveseriewaves_xpos = float(self.saveseriewaves_xpos_input.text())
        self.temp_relaxationzone.coefdir[0] = float(self.coefdir_x.text())
        self.temp_relaxationzone.coefdir[1] = float(self.coefdir_y.text())
        self.temp_relaxationzone.coefdir[2] = float(self.coefdir_z.text())
        self.temp_relaxationzone.coefdt = float(self.coefdt_input.text())
        self.temp_relaxationzone.function_psi = float(self.function_psi_input.text())
        self.temp_relaxationzone.function_beta = float(self.function_beta_input.text())
        self.temp_relaxationzone.driftcorrection = float(self.driftcorrection_input.text())
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        """ Deletes the currenlty represented object. """
        self.relaxationzone = None
        self.reject()

    def fill_data(self):
        """ Fills the data from the data structure onto the dialog. """
        self.start_input.setText(str(self.temp_relaxationzone.start))
        self.duration_input.setText(str(self.temp_relaxationzone.duration))
        self.peakcoef_input.setText(str(self.temp_relaxationzone.peakcoef))
        self.spectrum_selector.setCurrentIndex({IrregularSpectrum.JONSWAP: 0, IrregularSpectrum.PIERSON_MOSKOWITZ: 1}[self.temp_relaxationzone.spectrum])
        self.discretization_selector.setCurrentIndex({IrregularDiscretization.REGULAR: 0, IrregularDiscretization.RANDOM: 1, IrregularDiscretization.STRETCHED: 2, IrregularDiscretization.COSSTRETCHED: 3}[self.temp_relaxationzone.discretization])
        self.waveorder_input.setText(str(self.temp_relaxationzone.waveorder))
        self.waveheight_input.setText(str(self.temp_relaxationzone.waveheight))
        self.waveperiod_input.setText(str(self.temp_relaxationzone.waveperiod))
        self.waves_input.setText(str(self.temp_relaxationzone.waves))
        self.randomseed_input.setText(str(self.temp_relaxationzone.randomseed))
        self.depth_input.setText(str(self.temp_relaxationzone.depth))
        self.swl_input.setText(str(self.temp_relaxationzone.swl))
        self.center_x.setText(str(self.temp_relaxationzone.center[0]))
        self.center_y.setText(str(self.temp_relaxationzone.center[1]))
        self.center_z.setText(str(self.temp_relaxationzone.center[2]))
        self.width_input.setText(str(self.temp_relaxationzone.width))
        self.ramptime_input.setText(str(self.temp_relaxationzone.ramptime))
        self.serieini_input.setText(str(self.temp_relaxationzone.serieini))
        self.savemotion_time_input.setText(str(self.temp_relaxationzone.savemotion_time))
        self.savemotion_timedt_input.setText(str(self.temp_relaxationzone.savemotion_timedt))
        self.savemotion_xpos_input.setText(str(self.temp_relaxationzone.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(self.temp_relaxationzone.savemotion_zpos))
        self.saveserie_timemin_input.setText(str(self.temp_relaxationzone.saveserie_timemin))
        self.saveserie_timemax_input.setText(str(self.temp_relaxationzone.saveserie_timemax))
        self.saveserie_timedt_input.setText(str(self.temp_relaxationzone.saveserie_timedt))
        self.saveserie_xpos_input.setText(str(self.temp_relaxationzone.saveserie_xpos))
        self.saveseriewaves_timemin_input.setText(str(self.temp_relaxationzone.saveseriewaves_timemin))
        self.saveseriewaves_timemax_input.setText(str(self.temp_relaxationzone.saveseriewaves_timemax))
        self.saveseriewaves_xpos_input.setText(str(self.temp_relaxationzone.saveseriewaves_xpos))
        self.coefdir_x.setText(str(self.temp_relaxationzone.coefdir[0]))
        self.coefdir_y.setText(str(self.temp_relaxationzone.coefdir[1]))
        self.coefdir_z.setText(str(self.temp_relaxationzone.coefdir[2]))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))
        self.driftcorrection_input.setText(str(self.temp_relaxationzone.driftcorrection))
