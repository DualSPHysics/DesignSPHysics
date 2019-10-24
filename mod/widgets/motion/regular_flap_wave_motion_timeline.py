#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Regular Flap Wave Motion Timeline Widget """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import h_line_generator
from mod.stdout_tools import debug

from mod.dataobjects.motion.regular_flap_wave_gen import RegularFlapWaveGen


class RegularFlapWaveMotionTimeline(QtGui.QWidget):
    """ A Regular Flap Wave motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, RegularFlapWaveGen)

    def __init__(self, reg_wave_gen, parent=None):
        if not isinstance(reg_wave_gen, RegularFlapWaveGen):
            raise TypeError("You tried to spawn a regular flap wave generator "
                            "motion widget in the timeline with a wrong object")
        if reg_wave_gen is None:
            raise TypeError("You tried to spawn a regular flap wave generator "
                            "motion widget in the timeline without a motion object")
        super(RegularFlapWaveMotionTimeline, self).__init__(parent=parent)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtGui.QLabel(
            __("Regular flap wave generator (Flap)"))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.wave_order_label = QtGui.QLabel(__("Wave Order"))
        self.wave_order_selector = QtGui.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtGui.QLabel(__("Depth (m): "))
        self.depth_input = QtGui.QLineEdit()

        self.flap_axis_0_label = QtGui.QLabel(
            __("Flap axis 0 (X, Y, Z): "))
        self.flap_axis_0_x = QtGui.QLineEdit()
        self.flap_axis_0_y = QtGui.QLineEdit()
        self.flap_axis_0_z = QtGui.QLineEdit()

        self.flap_axis_1_label = QtGui.QLabel(
            __("Flap axis 1 (X, Y, Z): "))
        self.flap_axis_1_x = QtGui.QLineEdit()
        self.flap_axis_1_y = QtGui.QLineEdit()
        self.flap_axis_1_z = QtGui.QLineEdit()

        self.wave_height_label = QtGui.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtGui.QLineEdit()

        self.wave_period_label = QtGui.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtGui.QLineEdit()

        self.variable_draft_label = QtGui.QLabel(__("Variable Draft (m): "))
        self.variable_draft_input = QtGui.QLineEdit()

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

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        for x in [self.duration_label, self.duration_input]:
            self.root_layout.addWidget(x)

        self.first_row_layout = QtGui.QHBoxLayout()
        for x in [self.wave_order_label, self.wave_order_selector, self.depth_label, self.depth_input]:
            self.first_row_layout.addWidget(x)

        self.second_row_layout = QtGui.QHBoxLayout()
        for x in [self.flap_axis_0_label, self.flap_axis_0_x, self.flap_axis_0_y, self.flap_axis_0_z]:
            self.second_row_layout.addWidget(x)

        self.third_row_layout = QtGui.QHBoxLayout()
        for x in [self.flap_axis_1_label, self.flap_axis_1_x, self.flap_axis_1_y, self.flap_axis_1_z]:
            self.third_row_layout.addWidget(x)

        self.fourth_row_layout = QtGui.QHBoxLayout()
        for x in [self.wave_height_label, self.wave_height_input, self.wave_period_label, self.wave_period_input, self.variable_draft_label, self.variable_draft_input]:
            self.fourth_row_layout.addWidget(x)

        self.fifth_row_layout = QtGui.QHBoxLayout()
        for x in [self.phase_label, self.phase_input, self.ramp_label, self.ramp_input]:
            self.fifth_row_layout.addWidget(x)

        self.sixth_row_layout = QtGui.QHBoxLayout()
        for x in [self.disksave_label, self.disksave_periods_label, self.disksave_periods, self.disksave_periodsteps_label,
                  self.disksave_periodsteps, self.disksave_xpos_label, self.disksave_xpos, self.disksave_zpos_label,
                  self.disksave_zpos]:
            self.sixth_row_layout.addWidget(x)

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(reg_wave_gen)
        self._init_connections()

    def fill_values(self, reg_wave_gen):
        self.duration_input.setText(str(reg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(reg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(reg_wave_gen.depth))
        self.flap_axis_0_x.setText(str(reg_wave_gen.flapaxis0[0]))
        self.flap_axis_0_y.setText(str(reg_wave_gen.flapaxis0[1]))
        self.flap_axis_0_z.setText(str(reg_wave_gen.flapaxis0[2]))
        self.flap_axis_1_x.setText(str(reg_wave_gen.flapaxis1[0]))
        self.flap_axis_1_y.setText(str(reg_wave_gen.flapaxis1[1]))
        self.flap_axis_1_z.setText(str(reg_wave_gen.flapaxis1[2]))
        self.variable_draft_input.setText(str(reg_wave_gen.variable_draft))
        self.wave_height_input.setText(str(reg_wave_gen.wave_height))
        self.wave_period_input.setText(str(reg_wave_gen.wave_period))
        self.phase_input.setText(str(reg_wave_gen.phase))
        self.ramp_input.setText(str(reg_wave_gen.ramp))
        self.disksave_periods.setText(str(reg_wave_gen.disksave_periods))
        self.disksave_periodsteps.setText(
            str(reg_wave_gen.disksave_periodsteps))
        self.disksave_xpos.setText(str(reg_wave_gen.disksave_xpos))
        self.disksave_zpos.setText(str(reg_wave_gen.disksave_zpos))

    def _init_connections(self):
        self.wave_order_selector.currentIndexChanged.connect(self.on_change)
        for x in [self.duration_input, self.depth_input,
                  self.variable_draft_input, self.flap_axis_0_x,
                  self.flap_axis_0_y, self.flap_axis_0_z,
                  self.flap_axis_1_x,
                  self.flap_axis_1_y, self.flap_axis_1_z,
                  self.wave_height_input, self.wave_period_input,
                  self.ramp_input, self.phase_input, self.disksave_periods,
                  self.disksave_periodsteps, self.disksave_xpos,
                  self.disksave_zpos]:
            x.textChanged.connect(self.on_change)

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return RegularFlapWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                  duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
                                  flapaxis0=[float(self.flap_axis_0_x.text()),
                                             float(
                                                 self.flap_axis_0_y.text()),
                                             float(self.flap_axis_0_z.text())],
                                  flapaxis1=[float(self.flap_axis_1_x.text()),
                                             float(
                                                 self.flap_axis_1_y.text()),
                                             float(self.flap_axis_1_z.text())],
                                  variable_draft=float(
                                      self.variable_draft_input.text()),
                                  wave_height=float(
                                      self.wave_height_input.text()),
                                  wave_period=float(
                                      self.wave_period_input.text()),
                                  phase=float(self.phase_input.text()),
                                  ramp=float(self.ramp_input.text()),
                                  disksave_periods=float(
                                      self.disksave_periods.text()),
                                  disksave_periodsteps=float(
                                      self.disksave_periodsteps.text()),
                                  disksave_xpos=float(
                                      self.disksave_xpos.text()),
                                  disksave_zpos=float(self.disksave_zpos.text()))

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        for x in [self.duration_input, self.depth_input, self.flap_axis_0_x,
                  self.flap_axis_0_y, self.flap_axis_0_z,
                  self.flap_axis_1_x,
                  self.flap_axis_1_y, self.flap_axis_1_z,
                  self.variable_draft_input,
                  self.wave_height_input, self.wave_period_input,
                  self.ramp_input, self.phase_input, self.disksave_periods,
                  self.disksave_periodsteps, self.disksave_xpos,
                  self.disksave_zpos]:
            x.setText("0" if not x.text() else x.text().replace(",", "."))
