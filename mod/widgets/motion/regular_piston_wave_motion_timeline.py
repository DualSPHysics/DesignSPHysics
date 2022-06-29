#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Regular Piston Wave Motion Timeline Widget """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import h_line_generator
from mod.stdout_tools import debug

from mod.enums import AWASWaveOrder, AWASSaveMethod

from mod.dataobjects.motion.regular_piston_wave_gen import RegularPistonWaveGen
from mod.dataobjects.awas_correction import AWASCorrection
from mod.dataobjects.awas import AWAS

from mod.functions import make_float, make_int

class RegularPistonWaveMotionTimeline(QtGui.QWidget):
    """ A Regular Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RegularPistonWaveGen)

    def __init__(self, reg_wave_gen, parent=None):
        if not isinstance(reg_wave_gen, RegularPistonWaveGen):
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline with a wrong object")
        if reg_wave_gen is None:
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtGui.QLabel(__("Regular wave generator (Piston)"))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.wave_order_label = QtGui.QLabel(__("Wave Order"))
        self.wave_order_selector = QtGui.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtGui.QLabel(__("Depth (m): "))
        self.depth_input = QtGui.QLineEdit()

        self.piston_dir_label = QtGui.QLabel(
            __("Piston direction (X, Y, Z): "))
        self.piston_dir_x = QtGui.QLineEdit()
        self.piston_dir_y = QtGui.QLineEdit()
        self.piston_dir_z = QtGui.QLineEdit()

        self.wave_height_label = QtGui.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtGui.QLineEdit()

        self.wave_period_label = QtGui.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtGui.QLineEdit()

        self.gainstroke_label = QtGui.QLabel(__("Gain factor: "))
        self.gainstroke_input = QtGui.QLineEdit()

        self.phase_label = QtGui.QLabel(__("Phase (rad): "))
        self.phase_input = QtGui.QLineEdit()

        self.ramp_label = QtGui.QLabel(__("Ramp: "))
        self.ramp_input = QtGui.QLineEdit()

        self.disksave_label = QtGui.QLabel(__("Save theoretical values > "))
        self.disksave_periods = QtGui.QLineEdit()
        self.disksave_periods_label = QtGui.QLabel(__("Periods: "))
        self.disksave_periodsteps = QtGui.QLineEdit()
        self.disksave_periodsteps_label = QtGui.QLabel(__("Period Steps: "))
        self.disksave_xpos = QtGui.QLineEdit()
        self.disksave_xpos_label = QtGui.QLabel(__("X Pos (m): "))
        self.disksave_zpos = QtGui.QLineEdit()
        self.disksave_zpos_label = QtGui.QLabel(__("Z Pos (m): "))

        self.awas_label = QtGui.QLabel(__("AWAS configuration"))
        self.awas_enabled = QtGui.QCheckBox(__("Enabled"))

        self.awas_startawas_label = QtGui.QLabel(__("Start AWAS (s): "))
        self.awas_startawas_input = QtGui.QLineEdit()

        self.awas_swl_label = QtGui.QLabel(__("Still water level (m): "))
        self.awas_swl_input = QtGui.QLineEdit()

        self.awas_elevation_label = QtGui.QLabel(__("Wave order: "))
        self.awas_elevation_selector = QtGui.QComboBox()
        self.awas_elevation_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.awas_gaugex_label = QtGui.QLabel(__("Gauge X (value*h): "))
        self.awas_gaugex_input = QtGui.QLineEdit()

        self.awas_gaugey_label = QtGui.QLabel(__("Gauge Y (m): "))
        self.awas_gaugey_input = QtGui.QLineEdit()

        self.awas_gaugezmin_label = QtGui.QLabel(__("Gauge Z Min (m): "))
        self.awas_gaugezmin_input = QtGui.QLineEdit()

        self.awas_gaugezmax_label = QtGui.QLabel(__("Gauge Z Max (m): "))
        self.awas_gaugezmax_input = QtGui.QLineEdit()

        self.awas_gaugedp_label = QtGui.QLabel(__("Gauge dp: "))
        self.awas_gaugedp_input = QtGui.QLineEdit()

        self.awas_coefmasslimit_label = QtGui.QLabel(__("Coef. mass limit: "))
        self.awas_coefmasslimit_input = QtGui.QLineEdit()

        self.awas_savedata_label = QtGui.QLabel(__("Save data: "))
        self.awas_savedata_selector = QtGui.QComboBox()
        self.awas_savedata_selector.insertItems(
            0, [__("By Part"), __("More Info"), __("By Step")])

        self.awas_limitace_label = QtGui.QLabel(__("Limit acceleration: "))
        self.awas_limitace_input = QtGui.QLineEdit()

        self.awas_correction_label = QtGui.QLabel(__("Drift correction: "))
        self.awas_correction_enabled = QtGui.QCheckBox(__("Enabled"))

        self.awas_correction_coefstroke_label = QtGui.QLabel(__("Coefstroke"))
        self.awas_correction_coefstroke_input = QtGui.QLineEdit()

        self.awas_correction_coefperiod_label = QtGui.QLabel(__("Coefperiod"))
        self.awas_correction_coefperiod_input = QtGui.QLineEdit()

        self.awas_correction_powerfunc_label = QtGui.QLabel(__("Powerfunc"))
        self.awas_correction_powerfunc_input = QtGui.QLineEdit()

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        for x in [self.duration_label, self.duration_input]:
            self.root_layout.addWidget(x)

        self.first_row_layout = QtGui.QHBoxLayout()
        for x in [self.wave_order_label, self.wave_order_selector, self.depth_label, self.depth_input]:
            self.first_row_layout.addWidget(x)

        self.second_row_layout = QtGui.QHBoxLayout()
        for x in [self.piston_dir_label, self.piston_dir_x, self.piston_dir_y, self.piston_dir_z]:
            self.second_row_layout.addWidget(x)

        self.third_row_layout = QtGui.QHBoxLayout()
        for x in [self.wave_height_label, self.wave_height_input, self.wave_period_label, self.wave_period_input]:
            self.third_row_layout.addWidget(x)

        self.fourth_row_layout = QtGui.QHBoxLayout()
        for x in [self.gainstroke_label, self.gainstroke_input, self.phase_label, self.phase_input, self.ramp_label, self.ramp_input]:
            self.fourth_row_layout.addWidget(x)

        self.fifth_row_layout = QtGui.QHBoxLayout()
        for x in [self.disksave_label, self.disksave_periods_label, self.disksave_periods, self.disksave_periodsteps_label,
                  self.disksave_periodsteps, self.disksave_xpos_label, self.disksave_xpos, self.disksave_zpos_label, self.disksave_zpos]:
            self.fifth_row_layout.addWidget(x)

        self.awas_root_layout = QtGui.QHBoxLayout()
        self.awas_root_layout.addWidget(self.awas_label)
        self.awas_root_layout.addStretch(1)
        self.awas_root_layout.addWidget(self.awas_enabled)

        self.awas_first_row_layout = QtGui.QHBoxLayout()
        for x in [self.awas_startawas_label, self.awas_startawas_input, self.awas_swl_label, self.awas_swl_input, self.awas_elevation_label, self.awas_elevation_selector]:
            self.awas_first_row_layout.addWidget(x)

        self.awas_second_row_layout = QtGui.QHBoxLayout()
        for x in [self.awas_gaugex_label, self.awas_gaugex_input, self.awas_gaugey_label, self.awas_gaugey_input]:
            self.awas_second_row_layout.addWidget(x)

        self.awas_third_row_layout = QtGui.QHBoxLayout()
        for x in [self.awas_gaugezmin_label, self.awas_gaugezmin_input, self.awas_gaugezmax_label, self.awas_gaugezmax_input]:
            self.awas_third_row_layout.addWidget(x)

        self.awas_fourth_row_layout = QtGui.QHBoxLayout()
        for x in [self.awas_gaugedp_label, self.awas_gaugedp_input, self.awas_coefmasslimit_label, self.awas_coefmasslimit_input]:
            self.awas_fourth_row_layout.addWidget(x)

        self.awas_fifth_row_layout = QtGui.QHBoxLayout()
        for x in [self.awas_savedata_label, self.awas_savedata_selector, self.awas_limitace_label, self.awas_limitace_input]:
            self.awas_fifth_row_layout.addWidget(x)

        self.awas_sixth_row_layout = QtGui.QHBoxLayout()
        for x in [self.awas_correction_label, self.awas_correction_enabled, self.awas_correction_coefstroke_label, self.awas_correction_coefstroke_input,
                  self.awas_correction_coefperiod_label, self.awas_correction_coefperiod_input,
                  self.awas_correction_powerfunc_label, self.awas_correction_powerfunc_input]:
            self.awas_sixth_row_layout.addWidget(x)

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout,
                  self.third_row_layout, self.fourth_row_layout,
                  self.fifth_row_layout]:
            self.main_layout.addLayout(x)

        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addLayout(self.awas_root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.awas_first_row_layout,
                  self.awas_second_row_layout, self.awas_third_row_layout,
                  self.awas_fourth_row_layout, self.awas_fifth_row_layout,
                  self.awas_sixth_row_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(reg_wave_gen)
        self._init_connections()

    def fill_values(self, reg_wave_gen):
        """ Fills the values from the data structure onto the widget. """

        self.duration_input.setText(str(reg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(reg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(reg_wave_gen.depth))
        self.piston_dir_x.setText(str(reg_wave_gen.piston_dir[0]))
        self.piston_dir_y.setText(str(reg_wave_gen.piston_dir[1]))
        self.piston_dir_z.setText(str(reg_wave_gen.piston_dir[2]))
        self.wave_height_input.setText(str(reg_wave_gen.wave_height))
        self.wave_period_input.setText(str(reg_wave_gen.wave_period))
        self.phase_input.setText(str(reg_wave_gen.phase))
        self.gainstroke_input.setText(str(reg_wave_gen.gainstroke))
        self.ramp_input.setText(str(reg_wave_gen.ramp))
        self.disksave_periods.setText(str(reg_wave_gen.disksave_periods))
        self.disksave_periodsteps.setText(str(reg_wave_gen.disksave_periodsteps))
        self.disksave_xpos.setText(str(reg_wave_gen.disksave_xpos))
        self.disksave_zpos.setText(str(reg_wave_gen.disksave_zpos))
        self.awas_enabled.setChecked(bool(reg_wave_gen.awas.enabled))
        self.awas_startawas_input.setText(str(reg_wave_gen.awas.startawas))
        self.awas_swl_input.setText(str(reg_wave_gen.awas.swl))
        self.awas_gaugex_input.setText(str(reg_wave_gen.awas.gaugex))
        self.awas_gaugey_input.setText(str(reg_wave_gen.awas.gaugey))
        self.awas_gaugezmin_input.setText(str(reg_wave_gen.awas.gaugezmin))
        self.awas_gaugezmax_input.setText(str(reg_wave_gen.awas.gaugezmax))
        self.awas_gaugedp_input.setText(str(reg_wave_gen.awas.gaugedp))
        self.awas_coefmasslimit_input.setText(
            str(reg_wave_gen.awas.coefmasslimit))
        self.awas_limitace_input.setText(str(reg_wave_gen.awas.limitace))
        self.awas_elevation_selector.setCurrentIndex(
            int(reg_wave_gen.awas.elevation) - 1)
        self.awas_savedata_selector.setCurrentIndex(
            int(reg_wave_gen.awas.savedata) - 1)
        self.awas_correction_enabled.setChecked(
            bool(reg_wave_gen.awas.correction.enabled))
        self.awas_correction_coefstroke_input.setText(
            str(reg_wave_gen.awas.correction.coefstroke))
        self.awas_correction_coefperiod_input.setText(
            str(reg_wave_gen.awas.correction.coefperiod))
        self.awas_correction_powerfunc_input.setText(
            str(reg_wave_gen.awas.correction.powerfunc))
        self._awas_enabled_handler()

    def _init_connections(self):
        self.wave_order_selector.currentIndexChanged.connect(self.on_change)
        self.awas_savedata_selector.currentIndexChanged.connect(self.on_change)
        self.awas_elevation_selector.currentIndexChanged.connect(
            self.on_change)
        self.awas_enabled.stateChanged.connect(self.on_change)
        self.awas_correction_enabled.stateChanged.connect(
            self._awas_correction_enabled_handler)
        for x in [self.duration_input, self.depth_input, self.piston_dir_x,
                  self.piston_dir_y, self.piston_dir_z,
                  self.wave_height_input, self.wave_period_input,
                  self.ramp_input, self.phase_input, self.gainstroke_input, self.disksave_periods,
                  self.disksave_periodsteps, self.disksave_xpos,
                  self.disksave_zpos, self.awas_startawas_input,
                  self.awas_swl_input, self.awas_gaugex_input, self.awas_gaugedp_input,
                  self.awas_gaugey_input, self.awas_gaugezmin_input,
                  self.awas_gaugezmax_input, self.awas_coefmasslimit_input,
                  self.awas_limitace_input,
                  self.awas_correction_coefstroke_input,
                  self.awas_correction_coefperiod_input,
                  self.awas_correction_powerfunc_input]:
            x.textChanged.connect(self.on_change)

    def on_change(self):
        """ Reacts to input change, sanitizing it and firing a signal with the correspondent data object. """
        self._sanitize_input()
        self._awas_enabled_handler()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

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

        for x in [self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
                  self.awas_correction_coefperiod_input]:
            x.setEnabled(enable_state)

    def construct_motion_object(self):
        """ Constructs an RegularPistonWaveGen object from the data currently introduced on the widget. """
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
            coefstroke=make_float(self.awas_correction_coefstroke_input.text()),
            coefperiod=make_float(self.awas_correction_coefperiod_input.text()),
            powerfunc=make_float(self.awas_correction_powerfunc_input.text())
        )

        awas_object = AWAS(
            enabled=self.awas_enabled.isChecked(),
            startawas=make_float(self.awas_startawas_input.text()),
            swl=make_float(self.awas_swl_input.text()),
            elevation=_cmo_elevation,
            gaugex=make_float(self.awas_gaugex_input.text()),
            gaugey=make_float(self.awas_gaugey_input.text()),
            gaugezmin=make_float(self.awas_gaugezmin_input.text()),
            gaugezmax=make_float(self.awas_gaugezmax_input.text()),
            gaugedp=make_float(self.awas_gaugedp_input.text()),
            coefmasslimit=make_float(self.awas_coefmasslimit_input.text()),
            savedata=_cmo_savedata,
            limitace=make_float(self.awas_limitace_input.text()),
            correction=_cmo_correction
        )

        return RegularPistonWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                    duration=make_float(self.duration_input.text()), 
                                    depth=make_float(self.depth_input.text()),
                                    piston_dir=[make_float(self.piston_dir_x.text()),make_float(self.piston_dir_y.text()),make_float(self.piston_dir_z.text())],
                                    wave_height=make_float(self.wave_height_input.text()),
                                    wave_period=make_float(self.wave_period_input.text()),
                                    gainstroke=make_float(self.gainstroke_input.text()),
                                    phase=make_float(self.phase_input.text()),
                                    ramp=make_float(self.ramp_input.text()),
                                    disksave_periods=make_int(self.disksave_periods.text()),
                                    disksave_periodsteps=make_int(self.disksave_periodsteps.text()),
                                    disksave_xpos=make_float(self.disksave_xpos.text()),
                                    disksave_zpos=make_float(self.disksave_zpos.text()),
                                    awas=awas_object)

    def on_delete(self):
        """ Deletes the currently represented motion object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        for x in [self.duration_input, self.depth_input, self.piston_dir_x,
                  self.piston_dir_y, self.piston_dir_z,
                  self.wave_height_input, self.wave_period_input,
                  self.ramp_input, self.gainstroke_input, self.phase_input, self.disksave_periods,
                  self.disksave_periodsteps, self.disksave_xpos,
                  self.disksave_zpos, self.awas_startawas_input,
                  self.awas_swl_input, self.awas_gaugex_input,
                  self.awas_gaugey_input, self.awas_gaugezmax_input,
                  self.awas_gaugezmin_input, self.awas_gaugedp_input,
                  self.awas_coefmasslimit_input, self.awas_limitace_input,
                  self.awas_correction_coefstroke_input, self.awas_correction_coefperiod_input,
                  self.awas_correction_powerfunc_input]:
            x.setText("0" if not x.text() else x.text().replace(",", "."))
