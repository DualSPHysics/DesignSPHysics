#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Irregular Piston Wave Motion Timeline Widget"""

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.awas import AWAS
from mod.dataobjects.motion.awas_correction import AWASCorrection
from mod.dataobjects.motion.irregular_piston_wave_gen import IrregularPistonWaveGen
from mod.enums import AWASWaveOrder, AWASSaveMethod, IrregularSpectrum, IrregularDiscretization
from mod.functions import make_float
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.acceleration_input import AccelerationInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.tools.dialog_tools import warning_dialog


class IrregularPistonWaveMotionTimeline(QtWidgets.QWidget):
    """ An Irregular Wave motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, IrregularPistonWaveGen)

    def __init__(self, irreg_wave_gen, parent=None):
        if not isinstance(irreg_wave_gen, IrregularPistonWaveGen):
            raise TypeError("You tried to spawn an irregular wave generator "
                            "motion widget in the timeline with a wrong object")
        if irreg_wave_gen is None:
            raise TypeError("You tried to spawn an irregular wave generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.wave_generator_scroll = QtWidgets.QScrollArea()
        self.wave_generator_scroll.setMinimumWidth(720)
        self.wave_generator_scroll.setMinimumHeight(523)

        self.wave_generator_scroll.setWidgetResizable(True)
        self.wave_generator_scroll_widget = QtWidgets.QWidget()
        self.wave_generator_scroll_widget.setMinimumWidth(700)

        self.wave_generator_scroll.setWidget(self.wave_generator_scroll_widget)
        self.wave_generator_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.wave_generator_layout = QtWidgets.QVBoxLayout()
        self.wave_generator_scroll_widget.setLayout(self.wave_generator_layout)
        self.main_layout.addWidget(self.wave_generator_scroll)

        self.wave_generator_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(__("Irregular wave generator (Piston)"))

        self.duration_label = QtWidgets.QLabel(__("Duration"))
        self.duration_input = TimeInput()

        self.wave_order_label = QtWidgets.QLabel(__("Wave Order"))
        self.wave_order_selector = QtWidgets.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])
        self.wave_order_selector.setMaximumWidth(160)

        self.depth_label = QtWidgets.QLabel(__("Depth:"))
        self.depth_input = SizeInput()

        self.piston_dir_label = QtWidgets.QLabel(
            __("Piston direction (X, Y, Z): "))
        self.piston_dir_x = ValueInput()
        self.piston_dir_y = ValueInput()
        self.piston_dir_z = ValueInput()

        self.wave_height_label = QtWidgets.QLabel(__("Wave height:"))
        self.wave_height_input = SizeInput()

        self.wave_period_label = QtWidgets.QLabel(__("Wave period: "))
        self.wave_period_input = TimeInput()

        self.gainstroke_label = QtWidgets.QLabel(__("Gain factor: "))
        self.gainstroke_input = ValueInput()

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
        self.peak_coef_input = ValueInput()

        self.waves_label = QtWidgets.QLabel(__("Number of waves"))
        self.waves_input = IntValueInput(min_val=1)

        self.randomseed_label = QtWidgets.QLabel(__("Random Seed"))
        self.randomseed_input = IntValueInput()

        self.serieini_label = QtWidgets.QLabel(
            __("Initial time in wave serie: "))
        self.serieini_input = TimeInput()

        self.serieini_autofit = QtWidgets.QCheckBox("Auto fit")

        self.ramptime_label = QtWidgets.QLabel(__("Time of ramp: "))
        self.ramptime_input = TimeInput()

        self.savemotion_label = QtWidgets.QLabel(__("Motion saving > "))
        self.savemotion_time_input = TimeInput(minwidth=75,maxwidth=75)
        self.savemotion_time_label = QtWidgets.QLabel(__("Time: "))
        self.savemotion_timedt_input = TimeInput(minwidth=75,maxwidth=75)
        self.savemotion_timedt_label = QtWidgets.QLabel(__("DT Time: "))
        self.savemotion_xpos_input = SizeInput(minwidth=85,maxwidth=85)
        self.savemotion_xpos_label = QtWidgets.QLabel(__("X Pos: "))
        self.savemotion_zpos_input = SizeInput(minwidth=85,maxwidth=85)
        self.savemotion_zpos_label = QtWidgets.QLabel(__("Z Pos: "))

        self.saveserie_label = QtWidgets.QLabel(__("Save serie > "))
        self.saveserie_timemin_input =TimeInput(minwidth=75,maxwidth=75)
        self.saveserie_timemin_label = QtWidgets.QLabel(__("Min. Time: "))
        self.saveserie_timemax_input = TimeInput(minwidth=75,maxwidth=75)
        self.saveserie_timemax_label = QtWidgets.QLabel(__("Max. Time: "))
        self.saveserie_timedt_input = TimeInput(minwidth=75,maxwidth=75)
        self.saveserie_timedt_label = QtWidgets.QLabel(__("DT Time: "))
        self.saveserie_xpos_input = SizeInput(minwidth=85,maxwidth=85)
        self.saveserie_xpos_label = QtWidgets.QLabel(__("X Pos: "))

        self.saveseriewaves_label = QtWidgets.QLabel(__("Save serie waves > "))
        self.saveseriewaves_timemin_input = TimeInput(minwidth=75,maxwidth=75)
        self.saveseriewaves_timemin_label = QtWidgets.QLabel(__("Min. Time: "))
        self.saveseriewaves_timemax_input = TimeInput(minwidth=75,maxwidth=75)
        self.saveseriewaves_timemax_label = QtWidgets.QLabel(__("Max. Time: "))
        self.saveseriewaves_xpos_input = SizeInput(minwidth=85,maxwidth=85)
        self.saveseriewaves_xpos_label = QtWidgets.QLabel(__("X Pos: "))

        self.awas_label = QtWidgets.QLabel(__("AWAS configuration"))
        self.awas_enabled = QtWidgets.QCheckBox(__("Enabled"))

        self.awas_startawas_label = QtWidgets.QLabel(__("Start AWAS:"))
        self.awas_startawas_input = TimeInput()

        self.awas_swl_label = QtWidgets.QLabel(__("Still water level:"))
        self.awas_swl_input = SizeInput()

        self.awas_elevation_label = QtWidgets.QLabel(__("Wave order: "))
        self.awas_elevation_selector = QtWidgets.QComboBox()
        self.awas_elevation_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])
        self.awas_elevation_selector.setMaximumWidth(160)

        self.awas_gaugex_label = QtWidgets.QLabel(__("Gauge X (value*h): "))
        self.awas_gaugex_input = ValueInput()

        self.awas_gaugey_label = QtWidgets.QLabel(__("Gauge Y: "))
        self.awas_gaugey_input = SizeInput()

        self.awas_gaugezmin_label = QtWidgets.QLabel(__("Gauge Z Min:"))
        self.awas_gaugezmin_input = SizeInput()

        self.awas_gaugezmax_label = QtWidgets.QLabel(__("Gauge Z Max:"))
        self.awas_gaugezmax_input = SizeInput()

        self.awas_gaugedp_label = QtWidgets.QLabel(__("Gauge dp (value*dp): "))
        self.awas_gaugedp_input = ValueInput()

        self.awas_coefmasslimit_label = QtWidgets.QLabel(__("Coef. mass limit: "))
        self.awas_coefmasslimit_input = ValueInput()

        self.awas_savedata_label = QtWidgets.QLabel(__("Save data: "))
        self.awas_savedata_selector = QtWidgets.QComboBox()
        self.awas_savedata_selector.insertItems(
            0, [__("By Part"), __("More Info"), __("By Step")])

        self.awas_limitace_label = QtWidgets.QLabel(__("Limit acceleration: "))
        self.awas_limitace_input = AccelerationInput()

        self.awas_correction_label = QtWidgets.QLabel(__("Drift correction: "))
        self.awas_correction_enabled = QtWidgets.QCheckBox(__("Enabled"))

        self.awas_correction_coefstroke_label = QtWidgets.QLabel(__("Coefstroke"))
        self.awas_correction_coefstroke_input = ValueInput(minwidth=75,maxwidth=75)

        self.awas_correction_coefperiod_label = QtWidgets.QLabel(__("Coefperiod"))
        self.awas_correction_coefperiod_input = ValueInput(minwidth=75,maxwidth=75)

        self.awas_correction_powerfunc_label = QtWidgets.QLabel(__("Powerfunc"))
        self.awas_correction_powerfunc_input = ValueInput(minwidth=75,maxwidth=75)

        self.root_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        for x in [self.duration_label, self.duration_input]:
            self.root_layout.addWidget(x)

        self.first_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_order_label, self.wave_order_selector, self.depth_label, self.depth_input]:
            self.first_row_layout.addWidget(x)

        self.second_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.piston_dir_label, self.piston_dir_x, self.piston_dir_y, self.piston_dir_z]:
            self.second_row_layout.addWidget(x)

        self.third_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_height_label, self.wave_height_input, self.wave_period_label, self.wave_period_input, self.gainstroke_label, self.gainstroke_input]:
            self.third_row_layout.addWidget(x)

        self.fourth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.spectrum_label, self.spectrum_selector, self.discretization_label, self.discretization_selector, self.peak_coef_label, self.peak_coef_input]:
            self.fourth_row_layout.addWidget(x)

        self.fifth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.waves_label, self.waves_input, self.randomseed_label, self.randomseed_input]:
            self.fifth_row_layout.addWidget(x)

        self.sixth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.serieini_label, self.serieini_input, self.serieini_autofit]:
            self.sixth_row_layout.addWidget(x)

        self.seventh_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.ramptime_label, self.ramptime_input]:
            self.seventh_row_layout.addWidget(x)

        self.eighth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.savemotion_label, self.savemotion_time_label, self.savemotion_time_input, self.savemotion_timedt_label, self.savemotion_timedt_input,
                  self.savemotion_xpos_label, self.savemotion_xpos_input, self.savemotion_zpos_label, self.savemotion_zpos_input]:
            self.eighth_row_layout.addWidget(x)

        self.ninth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.saveserie_label, self.saveserie_timemin_label, self.saveserie_timemin_input, self.saveserie_timemax_label, self.saveserie_timemax_input,
                  self.saveserie_timedt_label, self.saveserie_timedt_input, self.saveserie_xpos_label, self.saveserie_xpos_input]:
            self.ninth_row_layout.addWidget(x)

        self.tenth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.saveseriewaves_label, self.saveseriewaves_timemin_label, self.saveseriewaves_timemin_input, self.saveseriewaves_timemax_label, self.saveseriewaves_timemax_input, self.saveseriewaves_xpos_label, self.saveseriewaves_xpos_input]:
            self.tenth_row_layout.addWidget(x)

        self.awas_root_layout = QtWidgets.QHBoxLayout()
        self.awas_root_layout.addWidget(self.awas_label)
        self.awas_root_layout.addStretch(1)
        self.awas_root_layout.addWidget(self.awas_enabled)

        self.awas_first_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_startawas_label, self.awas_startawas_input, self.awas_swl_label, self.awas_swl_input, self.awas_elevation_label, self.awas_elevation_selector]:
            self.awas_first_row_layout.addWidget(x)

        self.awas_second_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_gaugex_label, self.awas_gaugex_input, self.awas_gaugey_label, self.awas_gaugey_input]:
            self.awas_second_row_layout.addWidget(x)

        self.awas_third_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_gaugezmin_label, self.awas_gaugezmin_input, self.awas_gaugezmax_label, self.awas_gaugezmax_input]:
            self.awas_third_row_layout.addWidget(x)

        self.awas_fourth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_gaugedp_label, self.awas_gaugedp_input, self.awas_coefmasslimit_label, self.awas_coefmasslimit_input]:
            self.awas_fourth_row_layout.addWidget(x)

        self.awas_fifth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_savedata_label, self.awas_savedata_selector, self.awas_limitace_label, self.awas_limitace_input]:
            self.awas_fifth_row_layout.addWidget(x)

        self.awas_sixth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_correction_label, self.awas_correction_enabled, self.awas_correction_coefstroke_label, self.awas_correction_coefstroke_input, self.awas_correction_coefperiod_label, self.awas_correction_coefperiod_input, self.awas_correction_powerfunc_label, self.awas_correction_powerfunc_input]:
            self.awas_sixth_row_layout.addWidget(x)

        self.wave_generator_layout.addLayout(self.root_layout)
        self.wave_generator_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout, self.seventh_row_layout, self.eighth_row_layout, self.ninth_row_layout, self.tenth_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.wave_generator_layout.addWidget(h_line_generator())
        self.wave_generator_layout.addLayout(self.awas_root_layout)
        self.wave_generator_layout.addWidget(h_line_generator())
        for x in [self.awas_first_row_layout, self.awas_second_row_layout, self.awas_third_row_layout, self.awas_fourth_row_layout, self.awas_fifth_row_layout, self.awas_sixth_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(irreg_wave_gen)
        self._init_connections()

    def fill_values(self, irreg_wave_gen):
        """ Fills the value from the data structure onto the widget. """
        self.duration_input.setValue(irreg_wave_gen.duration)
        self.wave_order_selector.setCurrentIndex(
            int(irreg_wave_gen.wave_order) - 1)
        self.depth_input.setValue(irreg_wave_gen.depth)
        self.piston_dir_x.setValue(irreg_wave_gen.piston_dir[0])
        self.piston_dir_y.setValue(irreg_wave_gen.piston_dir[1])
        self.piston_dir_z.setValue(irreg_wave_gen.piston_dir[2])
        self.wave_height_input.setValue(irreg_wave_gen.wave_height)
        self.wave_period_input.setValue(irreg_wave_gen.wave_period)
        self.gainstroke_input.setValue(irreg_wave_gen.gainstroke)
        self.spectrum_selector.setCurrentIndex({IrregularSpectrum.JONSWAP: 0, IrregularSpectrum.PIERSON_MOSKOWITZ: 1}[irreg_wave_gen.spectrum])
        self.discretization_selector.setCurrentIndex({IrregularDiscretization.REGULAR: 0,
                                                      IrregularDiscretization.RANDOM: 1,
                                                      IrregularDiscretization.STRETCHED: 2,
                                                      IrregularDiscretization.COSSTRETCHED: 3}[irreg_wave_gen.discretization])
        self.peak_coef_input.setValue(irreg_wave_gen.peak_coef)
        self.waves_input.setValue(irreg_wave_gen.waves)
        self.randomseed_input.setValue(irreg_wave_gen.randomseed)
        self.serieini_input.setValue(irreg_wave_gen.serieini)
        self.serieini_autofit.setChecked(irreg_wave_gen.serieini_autofit)
        self.ramptime_input.setValue(irreg_wave_gen.ramptime)
        self.savemotion_time_input.setValue(irreg_wave_gen.savemotion_time)
        self.savemotion_timedt_input.setValue(irreg_wave_gen.savemotion_timedt)
        self.savemotion_xpos_input.setValue(irreg_wave_gen.savemotion_xpos)
        self.savemotion_zpos_input.setValue(irreg_wave_gen.savemotion_zpos)
        self.saveserie_timemin_input.setValue(irreg_wave_gen.saveserie_timemin)
        self.saveserie_timemax_input.setValue(irreg_wave_gen.saveserie_timemax)
        self.saveserie_timedt_input.setValue(irreg_wave_gen.saveserie_timedt)
        self.saveserie_xpos_input.setValue(irreg_wave_gen.saveserie_xpos)
        self.saveseriewaves_timemin_input.setValue(irreg_wave_gen.saveseriewaves_timemin)
        self.saveseriewaves_timemax_input.setValue(irreg_wave_gen.saveseriewaves_timemax)
        self.saveseriewaves_xpos_input.setValue(irreg_wave_gen.saveseriewaves_xpos)
        self.awas_enabled.setChecked(bool(irreg_wave_gen.awas.enabled))
        self.awas_startawas_input.setValue(irreg_wave_gen.awas.startawas)
        self.awas_swl_input.setValue(irreg_wave_gen.awas.swl)
        self.awas_gaugex_input.setValue(irreg_wave_gen.awas.gaugex)
        self.awas_gaugey_input.setValue(irreg_wave_gen.awas.gaugey)
        self.awas_gaugezmin_input.setValue(irreg_wave_gen.awas.gaugezmin)
        self.awas_gaugezmax_input.setValue(irreg_wave_gen.awas.gaugezmax)
        self.awas_gaugedp_input.setValue(irreg_wave_gen.awas.gaugedp)
        self.awas_coefmasslimit_input.setValue(irreg_wave_gen.awas.coefmasslimit)
        self.awas_limitace_input.setValue(irreg_wave_gen.awas.limitace)
        self.awas_elevation_selector.setCurrentIndex(
            int(irreg_wave_gen.awas.elevation) - 1)
        self.awas_savedata_selector.setCurrentIndex(
            int(irreg_wave_gen.awas.savedata) - 1)
        self.awas_correction_enabled.setChecked(
            bool(irreg_wave_gen.awas.correction.enabled))
        self.awas_correction_coefstroke_input.setValue(irreg_wave_gen.awas.correction.coefstroke)
        self.awas_correction_coefperiod_input.setValue(irreg_wave_gen.awas.correction.coefperiod)
        self.awas_correction_powerfunc_input.setValue(irreg_wave_gen.awas.correction.powerfunc)
        self._awas_enabled_handler()

    def _init_connections(self):
        self.serieini_autofit.stateChanged.connect(self.on_change)
        self.awas_savedata_selector.currentIndexChanged.connect(self.on_change)
        self.awas_elevation_selector.currentIndexChanged.connect(
            self.on_change)
        self.awas_enabled.stateChanged.connect(self.on_change)
        self.awas_correction_enabled.stateChanged.connect(
            self._awas_correction_enabled_handler)
        for x in [self.wave_order_selector, self.spectrum_selector, self.discretization_selector]:
            x.currentIndexChanged.connect(self.on_change)

        for x in [self.peak_coef_input, self.waves_input, self.randomseed_input,
                  self.serieini_input, self.ramptime_input, self.duration_input,
                  self.depth_input, self.piston_dir_x,
                  self.piston_dir_y, self.piston_dir_z, self.wave_height_input,
                  self.wave_period_input, self.gainstroke_input, self.savemotion_time_input,
                  self.savemotion_timedt_input, self.savemotion_xpos_input,
                  self.savemotion_zpos_input, self.saveserie_timemin_input,
                  self.saveserie_timemax_input, self.saveserie_timedt_input,
                  self.saveserie_xpos_input, self.saveseriewaves_timemin_input,
                  self.saveseriewaves_timemax_input,
                  self.saveseriewaves_xpos_input, self.awas_startawas_input,
                  self.awas_swl_input, self.awas_gaugex_input,
                  self.awas_gaugey_input, self.awas_gaugezmin_input,
                  self.awas_gaugezmax_input, self.awas_coefmasslimit_input,
                  self.awas_limitace_input,
                  self.awas_correction_coefstroke_input,
                  self.awas_correction_coefperiod_input,
                  self.awas_correction_powerfunc_input]:
            x.value_changed.connect(self.on_change)

    def on_change(self):
        """ Reacts to change, fires an event with the resulting object. """
        self._awas_enabled_handler()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            warning_dialog("Introduced an invalid value for a float number.")

    def _awas_enabled_handler(self):
        for x in [self.awas_startawas_input, self.awas_swl_input,
                  self.awas_elevation_selector, self.awas_gaugex_input,
                  self.awas_gaugey_input, self.awas_gaugezmin_input,
                  self.awas_gaugezmax_input, self.awas_gaugedp_input,
                  self.awas_coefmasslimit_input, self.awas_savedata_selector,
                  self.awas_limitace_input, self.awas_correction_coefperiod_input,
                  self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
                  self.awas_correction_enabled]:
            x.setEnabled(self.awas_enabled.isChecked())
        self._awas_correction_enabled_handler()

    def _awas_correction_enabled_handler(self):
        enable_state = self.awas_correction_enabled.isChecked()
        if not self.awas_enabled.isChecked():
            enable_state = False

        self.changed.emit(0, self.construct_motion_object())

        for x in [self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input, self.awas_correction_coefperiod_input]:
            x.setEnabled(enable_state)

    def construct_motion_object(self):
        """ Constructs an object from the data introduced in the widget. """
        _cmo_elevation = None
        if self.awas_elevation_selector.currentIndex() == 0:
            _cmo_elevation = AWASWaveOrder.FIRST_ORDER
        elif self.awas_elevation_selector.currentIndex() == 1:
            _cmo_elevation = AWASWaveOrder.SECOND_ORDER
        else:
            _cmo_elevation = AWASWaveOrder.FIRST_ORDER

        _cmo_savedata = None
        if self.awas_savedata_selector.currentIndex() == 0:
            _cmo_savedata = AWASSaveMethod.BY_PART
        elif self.awas_savedata_selector.currentIndex() == 1:
            _cmo_savedata = AWASSaveMethod.MORE_INFO
        elif self.awas_savedata_selector.currentIndex() == 2:
            _cmo_savedata = AWASSaveMethod.BY_STEP
        else:
            _cmo_savedata = AWASSaveMethod.BY_PART

        _cmo_correction = AWASCorrection(
            enabled=self.awas_correction_enabled.isChecked(),
            coefstroke=self.awas_correction_coefstroke_input.value(),
            coefperiod=self.awas_correction_coefperiod_input.value(),
            powerfunc=self.awas_correction_powerfunc_input.value()
        )

        awas_object = AWAS(
            enabled=self.awas_enabled.isChecked(),
            startawas=self.awas_startawas_input.value(),
            swl=self.awas_swl_input.value(),
            elevation=_cmo_elevation,
            gaugex=self.awas_gaugex_input.value(),
            gaugey=self.awas_gaugey_input.value(),
            gaugezmin=self.awas_gaugezmin_input.value(),
            gaugezmax=self.awas_gaugezmax_input.value(),
            gaugedp=self.awas_gaugedp_input.value(),
            coefmasslimit=self.awas_coefmasslimit_input.value(),
            savedata=_cmo_savedata,
            limitace=self.awas_limitace_input.value(),
            correction=_cmo_correction
        )

        return IrregularPistonWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                      duration=self.duration_input.value(), depth=self.depth_input.value(),
                                      piston_dir=[self.piston_dir_x.value(), self.piston_dir_y.value(), self.piston_dir_z.value()],
                                      wave_height=self.wave_height_input.value(),
                                      wave_period=self.wave_period_input.value(),
                                      gainstroke=self.gainstroke_input.value(),
                                      spectrum={0: IrregularSpectrum.JONSWAP, 1: IrregularSpectrum.PIERSON_MOSKOWITZ}[self.spectrum_selector.currentIndex()],
                                      discretization={0: IrregularDiscretization.REGULAR, 1: IrregularDiscretization.RANDOM, 2: IrregularDiscretization.STRETCHED, 3: IrregularDiscretization.COSSTRETCHED}[self.discretization_selector.currentIndex()],
                                      peak_coef=self.peak_coef_input.value(),
                                      waves=self.waves_input.value(),
                                      randomseed=self.randomseed_input.value(),
                                      serieini=self.serieini_input.value(),
                                      ramptime=self.ramptime_input.value(),
                                      serieini_autofit=self.serieini_autofit.isChecked(),
                                      savemotion_time=self.savemotion_time_input.value(),
                                      savemotion_timedt=self.savemotion_timedt_input.value(),
                                      savemotion_xpos=self.savemotion_xpos_input.value(),
                                      savemotion_zpos=self.savemotion_zpos_input.value(),
                                      saveserie_timemin=self.saveserie_timemin_input.value(),
                                      saveserie_timemax=self.saveserie_timemax_input.value(),
                                      saveserie_timedt=self.saveserie_timedt_input.value(),
                                      saveserie_xpos=self.saveserie_xpos_input.value(),
                                      saveseriewaves_timemin=self.saveseriewaves_timemin_input.value(),
                                      saveseriewaves_timemax=self.saveseriewaves_timemax_input.value(),
                                      saveseriewaves_xpos=self.saveseriewaves_xpos_input.value(),
                                      awas=awas_object)

    def on_delete(self):
        """ Deletes the currently defined object. """
        self.deleted.emit(self.index, self.construct_motion_object())
