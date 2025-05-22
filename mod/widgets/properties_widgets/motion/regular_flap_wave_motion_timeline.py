#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Regular Flap Wave Motion Timeline Widget """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.regular_flap_wave_gen import RegularFlapWaveGen
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.tools.dialog_tools import warning_dialog


class RegularFlapWaveMotionTimeline(QtWidgets.QWidget):
    """ A Regular Flap Wave motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, RegularFlapWaveGen)

    def __init__(self, reg_wave_gen, parent=None):
        if not isinstance(reg_wave_gen, RegularFlapWaveGen):
            raise TypeError("You tried to spawn a regular flap wave generator "
                            "motion widget in the timeline with a wrong object")
        if reg_wave_gen is None:
            raise TypeError("You tried to spawn a regular flap wave generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(
            __("Regular flap wave generator (Flap)"))

        self.duration_label = QtWidgets.QLabel(__("Duration: "))
        self.duration_input = TimeInput()

        self.wave_order_label = QtWidgets.QLabel(__("Wave Order"))
        self.wave_order_selector = QtWidgets.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtWidgets.QLabel(__("Depth: "))
        self.depth_input = SizeInput()

        self.flap_axis_0_label = QtWidgets.QLabel(
            __("Flap axis 0 (X, Y, Z): "))
        self.flap_axis_0_x = SizeInput()
        self.flap_axis_0_y = SizeInput()
        self.flap_axis_0_z = SizeInput()

        self.flap_axis_1_label = QtWidgets.QLabel(
            __("Flap axis 1 (X, Y, Z): "))
        self.flap_axis_1_x = SizeInput()
        self.flap_axis_1_y = SizeInput()
        self.flap_axis_1_z = SizeInput()

        self.wave_height_label = QtWidgets.QLabel(__("Wave height:"))
        self.wave_height_input = SizeInput()

        self.wave_period_label = QtWidgets.QLabel(__("Wave period: "))
        self.wave_period_input = TimeInput()

        self.variable_draft_label = QtWidgets.QLabel(__("Variable Draft:"))
        self.variable_draft_input = SizeInput()

        self.gainstroke_label = QtWidgets.QLabel(__("Gain factor: "))
        self.gainstroke_input = ValueInput()

        self.phase_label = QtWidgets.QLabel(__("Phase (rad): "))
        self.phase_input = ValueInput()

        self.ramp_label = QtWidgets.QLabel(__("Ramp: "))
        self.ramp_input = ValueInput()

        self.disksave_label = QtWidgets.QLabel(__("Save theoretical values > "))
        self.disksave_periods = IntValueInput(min_val=1,minwidth=60,maxwidth=60)
        self.disksave_periods_label = QtWidgets.QLabel(__("Periods: "))
        self.disksave_periodsteps = IntValueInput(min_val=1,minwidth=60,maxwidth=60)
        self.disksave_periodsteps_label = QtWidgets.QLabel(__("Period Steps: "))
        self.disksave_xpos = SizeInput(minwidth=100,maxwidth=100)
        self.disksave_xpos_label = QtWidgets.QLabel(__("X Pos:"))
        self.disksave_zpos = SizeInput(minwidth=100,maxwidth=100)
        self.disksave_zpos_label = QtWidgets.QLabel(__("Z Pos:"))

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
        for x in [self.gainstroke_label, self.gainstroke_input, self.phase_label, self.phase_input, self.ramp_label, self.ramp_input]:
            self.fifth_row_layout.addWidget(x)

        self.sixth_row_layout = QtWidgets.QHBoxLayout()
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
        """ Fills the values from the data structure onto the widget. """
        self.duration_input.setValue(reg_wave_gen.duration)
        self.wave_order_selector.setCurrentIndex(
            int(reg_wave_gen.wave_order) - 1)
        self.depth_input.setValue(reg_wave_gen.depth)
        self.flap_axis_0_x.setValue(reg_wave_gen.flapaxis0[0])
        self.flap_axis_0_y.setValue(reg_wave_gen.flapaxis0[1])
        self.flap_axis_0_z.setValue(reg_wave_gen.flapaxis0[2])
        self.flap_axis_1_x.setValue(reg_wave_gen.flapaxis1[0])
        self.flap_axis_1_y.setValue(reg_wave_gen.flapaxis1[1])
        self.flap_axis_1_z.setValue(reg_wave_gen.flapaxis1[2])
        self.variable_draft_input.setValue(reg_wave_gen.variable_draft)
        self.wave_height_input.setValue(reg_wave_gen.wave_height)
        self.wave_period_input.setValue(reg_wave_gen.wave_period)
        self.gainstroke_input.setValue(reg_wave_gen.gainstroke)
        self.phase_input.setValue(reg_wave_gen.phase)
        self.ramp_input.setValue(reg_wave_gen.ramp)
        self.disksave_periods.setValue(reg_wave_gen.disksave_periods)
        self.disksave_periodsteps.setValue(reg_wave_gen.disksave_periodsteps)
        self.disksave_xpos.setValue(reg_wave_gen.disksave_xpos)
        self.disksave_zpos.setValue(reg_wave_gen.disksave_zpos)

    def _init_connections(self):
        self.wave_order_selector.currentIndexChanged.connect(self.on_change)
        for x in [self.duration_input, self.depth_input,
                  self.variable_draft_input, self.flap_axis_0_x,
                  self.flap_axis_0_y, self.flap_axis_0_z,
                  self.flap_axis_1_x,
                  self.flap_axis_1_y, self.flap_axis_1_z,
                  self.wave_height_input, self.wave_period_input,
                  self.ramp_input, self.gainstroke_input, self.phase_input, self.disksave_periods,
                  self.disksave_periodsteps, self.disksave_xpos,
                  self.disksave_zpos]:
            x.value_changed.connect(self.on_change)

    def on_change(self):
        """ Reacts to input change, firing a signal with the corresponding object. """
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            warning_dialog("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs a RegularFlapWaveGen with the data currently introduced in the widget. """
        return RegularFlapWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                  duration=self.duration_input.value(), depth=self.depth_input.value(),
                                  flapaxis0=[self.flap_axis_0_x.value(),
                                             self.flap_axis_0_y.value(),
                                             self.flap_axis_0_z.value()],
                                  flapaxis1=[self.flap_axis_1_x.value(),
                                             self.flap_axis_1_y.value(),
                                             self.flap_axis_1_z.value()],
                                  variable_draft=self.variable_draft_input.value(),
                                  wave_height=self.wave_height_input.value(),
                                  wave_period=self.wave_period_input.value(),
                                  gainstroke=self.gainstroke_input.value(),
                                  phase=self.phase_input.value(),
                                  ramp=self.ramp_input.value(),
                                  disksave_periods=int(
                                      self.disksave_periods.value()),
                                  disksave_periodsteps=int(
                                      self.disksave_periodsteps.value()),
                                  disksave_xpos=self.disksave_xpos.value(),
                                  disksave_zpos=self.disksave_zpos.value())

    def on_delete(self):
        """ Deletes the currently represented object. """
        self.deleted.emit(self.index, self.construct_motion_object())
