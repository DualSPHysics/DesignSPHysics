#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Irregular Flap Wave Motion timeline widget."""

# from PySide import QtCore, QtGui
from PySide6 import QtCore, QtWidgets

from mod.translation_tools import __
from mod.gui_tools import h_line_generator
from mod.stdout_tools import debug
from mod.enums import IrregularDiscretization, IrregularSpectrum

from mod.dataobjects.motion.irregular_flap_wave_gen import IrregularFlapWaveGen

from mod.functions import make_float


class IrregularFlapWaveMotionTimeline(QtWidgets.QWidget):
    """ An Irregular Flap Wave motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, IrregularFlapWaveGen)

    def __init__(self, irreg_wave_gen, parent=None):
        if not isinstance(irreg_wave_gen, IrregularFlapWaveGen):
            raise TypeError("You tried to spawn an irregular flap wave generator "
                            "motion widget in the timeline with a wrong object")
        if irreg_wave_gen is None:
            raise TypeError("You tried to spawn an irregular flap wave generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(
            __("Irregular flap wave generator (Flap)"))

        self.duration_label = QtWidgets.QLabel(__("Duration"))
        self.duration_input = QtWidgets.QLineEdit()

        self.wave_order_label = QtWidgets.QLabel(__("Wave Order"))
        self.wave_order_selector = QtWidgets.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtWidgets.QLabel(__("Depth (m): "))
        self.depth_input = QtWidgets.QLineEdit()

        self.flap_axis_0_label = QtWidgets.QLabel(
            __("Flap axis 0 (X, Y, Z): "))
        self.flap_axis_0_x = QtWidgets.QLineEdit()
        self.flap_axis_0_y = QtWidgets.QLineEdit()
        self.flap_axis_0_z = QtWidgets.QLineEdit()

        self.flap_axis_1_label = QtWidgets.QLabel(
            __("Flap axis 1 (X, Y, Z): "))
        self.flap_axis_1_x = QtWidgets.QLineEdit()
        self.flap_axis_1_y = QtWidgets.QLineEdit()
        self.flap_axis_1_z = QtWidgets.QLineEdit()

        self.wave_height_label = QtWidgets.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtWidgets.QLineEdit()

        self.wave_period_label = QtWidgets.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtWidgets.QLineEdit()

        self.gainstroke_label = QtWidgets.QLabel(__("Gain factor: "))
        self.gainstroke_input = QtWidgets.QLineEdit()

        self.variable_draft_label = QtWidgets.QLabel(__("Variable Draft (m): "))
        self.variable_draft_input = QtWidgets.QLineEdit()

        self.spectrum_label = QtWidgets.QLabel(__("Spectrum"))
        self.spectrum_selector = QtWidgets.QComboBox()
        # Index numbers match IrregularSpectrum static values
        self.spectrum_selector.insertItems(0, ["Jonswap", "Pierson-Moskowitz"])

        self.discretization_label = QtWidgets.QLabel(__("Discretization"))
        self.discretization_selector = QtWidgets.QComboBox()
        # Index numbers match IrregularDiscretization static values
        self.discretization_selector.insertItems(
            0, ["Regular", "Random", "Stretched", "Crosstreched"])

        self.peak_coef_label = QtWidgets.QLabel(__("Peak Coeff"))
        self.peak_coef_input = QtWidgets.QLineEdit()

        self.waves_label = QtWidgets.QLabel(__("Number of waves"))
        self.waves_input = QtWidgets.QLineEdit()

        self.randomseed_label = QtWidgets.QLabel(__("Random Seed"))
        self.randomseed_input = QtWidgets.QLineEdit()

        self.serieini_label = QtWidgets.QLabel(__("Initial time in wave serie (s): "))
        self.serieini_input = QtWidgets.QLineEdit()

        self.serieini_autofit = QtWidgets.QCheckBox("Auto fit")

        self.ramptime_label = QtWidgets.QLabel(__("Time of ramp (s): "))
        self.ramptime_input = QtWidgets.QLineEdit()

        self.savemotion_label = QtWidgets.QLabel(__("Motion saving > "))
        self.savemotion_time_input = QtWidgets.QLineEdit()
        self.savemotion_time_label = QtWidgets.QLabel(__("Time (s): "))
        self.savemotion_timedt_input = QtWidgets.QLineEdit()
        self.savemotion_timedt_label = QtWidgets.QLabel(__("DT Time (s): "))
        self.savemotion_xpos_input = QtWidgets.QLineEdit()
        self.savemotion_xpos_label = QtWidgets.QLabel(__("X Pos (m): "))
        self.savemotion_zpos_input = QtWidgets.QLineEdit()
        self.savemotion_zpos_label = QtWidgets.QLabel(__("Z Pos (m): "))

        self.saveserie_label = QtWidgets.QLabel(__("Save serie > "))
        self.saveserie_timemin_input = QtWidgets.QLineEdit()
        self.saveserie_timemin_label = QtWidgets.QLabel(__("Min. Time (s): "))
        self.saveserie_timemax_input = QtWidgets.QLineEdit()
        self.saveserie_timemax_label = QtWidgets.QLabel(__("Max. Time (s): "))
        self.saveserie_timedt_input = QtWidgets.QLineEdit()
        self.saveserie_timedt_label = QtWidgets.QLabel(__("DT Time (s): "))
        self.saveserie_xpos_input = QtWidgets.QLineEdit()
        self.saveserie_xpos_label = QtWidgets.QLabel(__("X Pos (m): "))

        self.saveseriewaves_label = QtWidgets.QLabel(__("Save serie waves > "))
        self.saveseriewaves_timemin_input = QtWidgets.QLineEdit()
        self.saveseriewaves_timemin_label = QtWidgets.QLabel(__("Min. Time (s): "))
        self.saveseriewaves_timemax_input = QtWidgets.QLineEdit()
        self.saveseriewaves_timemax_label = QtWidgets.QLabel(__("Max. Time (s): "))
        self.saveseriewaves_xpos_input = QtWidgets.QLineEdit()
        self.saveseriewaves_xpos_label = QtWidgets.QLabel(__("X Pos (m): "))

        self.root_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)

        for x in [self.duration_label, self.duration_input]:
            self.root_layout.addWidget(x)

        self.first_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_order_label, self.wave_order_selector, self.depth_label, self.depth_input]:
            self.first_row_layout.addWidget(x)

        self.second_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.flap_axis_0_label, self.flap_axis_0_x, self.flap_axis_0_y, self.flap_axis_0_z]:
            self.second_row_layout.addWidget(x)

        self.third_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.flap_axis_1_label, self.flap_axis_1_x, self.flap_axis_1_y, self.flap_axis_1_z]:
            self.third_row_layout.addWidget(x)

        self.fourth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_height_label, self.wave_height_input, self.wave_period_label, self.wave_period_input, self.variable_draft_label, self.variable_draft_input]:
            self.fourth_row_layout.addWidget(x)

        self.fifth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.spectrum_label, self.spectrum_selector, self.discretization_label, self.discretization_selector, self.peak_coef_label, self.peak_coef_input]:
            self.fifth_row_layout.addWidget(x)

        self.sixth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.gainstroke_label, self.gainstroke_input, self.waves_label, self.waves_input, self.randomseed_label, self.randomseed_input]:
            self.sixth_row_layout.addWidget(x)

        self.seventh_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.serieini_label, self.serieini_input, self.serieini_autofit]:
            self.seventh_row_layout.addWidget(x)

        self.eighth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.ramptime_label, self.ramptime_input]:
            self.eighth_row_layout.addWidget(x)

        self.ninth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.savemotion_label, self.savemotion_time_label, self.savemotion_time_input, self.savemotion_timedt_label,
                  self.savemotion_timedt_input, self.savemotion_xpos_label, self.savemotion_xpos_input, self.savemotion_zpos_label, self.savemotion_zpos_input]:
            self.ninth_row_layout.addWidget(x)

        self.tenth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.saveserie_label, self.saveserie_timemin_label, self.saveserie_timemin_input, self.saveserie_timemax_label,
                  self.saveserie_timemax_input, self.saveserie_timedt_label, self.saveserie_timedt_input, self.saveserie_xpos_label, self.saveserie_xpos_input]:
            self.tenth_row_layout.addWidget(x)

        self.eleventh_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.saveseriewaves_label, self.saveseriewaves_timemin_label, self.saveseriewaves_timemin_input, self.saveseriewaves_timemax_label,
                  self.saveseriewaves_timemax_input, self.saveseriewaves_xpos_label, self.saveseriewaves_xpos_input]:
            self.eleventh_row_layout.addWidget(x)

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout, self.seventh_row_layout, self.eighth_row_layout, self.ninth_row_layout, self.tenth_row_layout, self.eleventh_row_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(irreg_wave_gen)
        self._init_connections()

    def fill_values(self, irreg_wave_gen):
        """ Fills the value from the data structure onto the widget. """

        self.duration_input.setText(str(irreg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(irreg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(irreg_wave_gen.depth))
        self.flap_axis_0_x.setText(str(irreg_wave_gen.flapaxis0[0]))
        self.flap_axis_0_y.setText(str(irreg_wave_gen.flapaxis0[1]))
        self.flap_axis_0_z.setText(str(irreg_wave_gen.flapaxis0[2]))
        self.flap_axis_1_x.setText(str(irreg_wave_gen.flapaxis1[0]))
        self.flap_axis_1_y.setText(str(irreg_wave_gen.flapaxis1[1]))
        self.flap_axis_1_z.setText(str(irreg_wave_gen.flapaxis1[2]))
        self.wave_height_input.setText(str(irreg_wave_gen.wave_height))
        self.wave_period_input.setText(str(irreg_wave_gen.wave_period))
        self.variable_draft_input.setText(str(irreg_wave_gen.variable_draft))
        self.spectrum_selector.setCurrentIndex({IrregularSpectrum.JONSWAP: 0, IrregularSpectrum.PIERSON_MOSKOWITZ: 1}[irreg_wave_gen.spectrum])
        self.discretization_selector.setCurrentIndex({IrregularDiscretization.REGULAR: 0,
                                                      IrregularDiscretization.RANDOM: 1,
                                                      IrregularDiscretization.STRETCHED: 2,
                                                      IrregularDiscretization.COSSTRETCHED: 3}[irreg_wave_gen.discretization])
        self.peak_coef_input.setText(str(irreg_wave_gen.peak_coef))
        self.waves_input.setText(str(irreg_wave_gen.waves))
        self.gainstroke_input.setText(str(irreg_wave_gen.gainstroke))
        self.randomseed_input.setText(str(irreg_wave_gen.randomseed))
        self.serieini_input.setText(str(irreg_wave_gen.serieini))
        self.serieini_autofit.setChecked(irreg_wave_gen.serieini_autofit)
        self.ramptime_input.setText(str(irreg_wave_gen.ramptime))
        self.savemotion_time_input.setText(str(irreg_wave_gen.savemotion_time))
        self.savemotion_timedt_input.setText(
            str(irreg_wave_gen.savemotion_timedt))
        self.savemotion_xpos_input.setText(str(irreg_wave_gen.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(irreg_wave_gen.savemotion_zpos))
        self.saveserie_timemin_input.setText(
            str(irreg_wave_gen.saveserie_timemin))
        self.saveserie_timemax_input.setText(
            str(irreg_wave_gen.saveserie_timemax))
        self.saveserie_timedt_input.setText(
            str(irreg_wave_gen.saveserie_timedt))
        self.saveserie_xpos_input.setText(str(irreg_wave_gen.saveserie_xpos))
        self.saveseriewaves_timemin_input.setText(
            str(irreg_wave_gen.saveseriewaves_timemin))
        self.saveseriewaves_timemax_input.setText(
            str(irreg_wave_gen.saveseriewaves_timemax))
        self.saveseriewaves_xpos_input.setText(
            str(irreg_wave_gen.saveseriewaves_xpos))

    def _init_connections(self):
        self.serieini_autofit.stateChanged.connect(self.on_change)
        for x in [self.wave_order_selector, self.spectrum_selector, self.discretization_selector]:
            x.currentIndexChanged.connect(self.on_change)

        for x in [self.peak_coef_input, self.waves_input, self.gainstroke_input, self.randomseed_input,
                  self.serieini_input, self.ramptime_input, self.duration_input,
                  self.depth_input, self.flap_axis_0_x,
                  self.flap_axis_0_y, self.flap_axis_0_z,
                  self.flap_axis_1_x,
                  self.flap_axis_1_y, self.flap_axis_1_z,
                  self.wave_height_input,
                  self.wave_period_input, self.variable_draft_input,
                  self.savemotion_time_input,
                  self.savemotion_timedt_input, self.savemotion_xpos_input,
                  self.savemotion_zpos_input, self.saveserie_timemin_input,
                  self.saveserie_timemax_input, self.saveserie_timedt_input,
                  self.saveserie_xpos_input, self.saveseriewaves_timemin_input,
                  self.saveseriewaves_timemax_input,
                  self.saveseriewaves_xpos_input]:
            x.textChanged.connect(self.on_change)

    def on_change(self):
        """ Reacts to changes on the widget, sanitizes the input and fires an event with the resulting object. """
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs an IrregularFlapWaveGen object from the widget data. """
        return IrregularFlapWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                    duration=make_float(self.duration_input.text()), depth=make_float(self.depth_input.text()),
                                    flapaxis0=[make_float(self.flap_axis_0_x.text()),
                                               make_float(
                                                   self.flap_axis_0_y.text()),
                                               make_float(self.flap_axis_0_z.text())],
                                    flapaxis1=[make_float(self.flap_axis_1_x.text()),
                                               make_float(
                                                   self.flap_axis_1_y.text()),
                                               make_float(self.flap_axis_1_z.text())],
                                    wave_height=make_float(
                                        self.wave_height_input.text()),
                                    wave_period=make_float(
                                        self.wave_period_input.text()),
                                    variable_draft=make_float(
                                        self.variable_draft_input.text()),
                                    spectrum={0: IrregularSpectrum.JONSWAP, 1: IrregularSpectrum.PIERSON_MOSKOWITZ}[self.spectrum_selector.currentIndex()],
                                    discretization={0: IrregularDiscretization.REGULAR, 1: IrregularDiscretization.RANDOM, 2: IrregularDiscretization.STRETCHED, 3: IrregularDiscretization.COSSTRETCHED}[self.discretization_selector.currentIndex()],
                                    peak_coef=make_float(
                                        self.peak_coef_input.text()),
                                    waves=make_float(self.waves_input.text()),
                                    gainstroke=make_float(self.gainstroke_input.text()),
                                    randomseed=make_float(
                                        self.randomseed_input.text()),
                                    serieini=make_float(
                                        self.serieini_input.text()),
                                    ramptime=make_float(
                                        self.ramptime_input.text()),
                                    serieini_autofit=self.serieini_autofit.isChecked(),
                                    savemotion_time=str(
                                        self.savemotion_time_input.text()),
                                    savemotion_timedt=str(
                                        self.savemotion_timedt_input.text()),
                                    savemotion_xpos=str(
                                        self.savemotion_xpos_input.text()),
                                    savemotion_zpos=str(
                                        self.savemotion_zpos_input.text()),
                                    saveserie_timemin=str(
                                        self.saveserie_timemin_input.text()),
                                    saveserie_timemax=str(
                                        self.saveserie_timemax_input.text()),
                                    saveserie_timedt=str(
                                        self.saveserie_timedt_input.text()),
                                    saveserie_xpos=str(
                                        self.saveserie_xpos_input.text()),
                                    saveseriewaves_timemin=str(
                                        self.saveseriewaves_timemin_input.text()),
                                    saveseriewaves_timemax=str(
                                        self.saveseriewaves_timemax_input.text()),
                                    saveseriewaves_xpos=str(self.saveseriewaves_xpos_input.text()))

    def on_delete(self):
        """ Deletes the currently defined object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        for x in [self.duration_input, self.depth_input, self.flap_axis_0_x,
                  self.flap_axis_0_y, self.flap_axis_0_z,
                  self.flap_axis_1_x,
                  self.flap_axis_1_y, self.flap_axis_1_z,
                  self.wave_height_input, self.wave_period_input,
                  self.variable_draft_input, self.gainstroke_input,
                  self.peak_coef_input, self.randomseed_input,
                  self.serieini_input, self.ramptime_input,
                  self.savemotion_time_input, self.savemotion_timedt_input,
                  self.savemotion_xpos_input, self.savemotion_zpos_input,
                  self.saveserie_timemin_input, self.saveserie_timemax_input,
                  self.saveserie_timedt_input, self.saveserie_xpos_input,
                  self.saveseriewaves_timemin_input, self.saveseriewaves_timemax_input,
                  self.saveseriewaves_xpos_input]:
            x.setText("0" if not x.text() else x.text().replace(",", "."))
