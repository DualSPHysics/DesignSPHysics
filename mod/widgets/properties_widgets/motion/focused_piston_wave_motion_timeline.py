#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Focused Piston Wave Motion Timeline Widget"""

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.focused_piston_wave_gen import FocusedPistonWaveGen
from mod.enums import IrregularSpectrum, IrregularDiscretization
from mod.functions import make_float
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.tools.dialog_tools import warning_dialog


class FocusedPistonWaveMotionTimeline(QtWidgets.QWidget):
    """ An Focused Wave motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, FocusedPistonWaveGen)

    def __init__(self, focused_wave_gen, parent=None):
        if not isinstance(focused_wave_gen, FocusedPistonWaveGen):
            raise TypeError("You tried to spawn an focused wave generator "
                            "motion widget in the timeline with a wrong object")
        if focused_wave_gen is None:
            raise TypeError("You tried to spawn an focused wave generator "
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

        self.root_label = QtWidgets.QLabel(__("Focused wave generator (Piston)"))

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

        self.wave_period_label = QtWidgets.QLabel(__("Wave period:"))
        self.wave_period_input = TimeInput()

        self.gainstroke_label = QtWidgets.QLabel(__("Gain factor: "))
        self.gainstroke_input = ValueInput()

        self.spectrum_label = QtWidgets.QLabel(__("Spectrum"))
        self.spectrum_selector = QtWidgets.QComboBox()
        # Index numbers match FocusedSpectrum static values
        self.spectrum_selector.insertItems(0, ["Jonswap", "Pierson-Moskowitz"])

        self.discretization_label = QtWidgets.QLabel(__("Discretization"))
        self.discretization_selector = QtWidgets.QComboBox()
        # Index numbers match FocusedDiscretization static values
        self.discretization_selector.insertItems(
            0, ["Regular", "Random", "Stretched", "Crosstreched"])

        self.peak_coef_label = QtWidgets.QLabel(__("Peak Coeff"))
        self.peak_coef_input = ValueInput()

        self.waves_label = QtWidgets.QLabel(__("Number of waves"))
        self.waves_input = IntValueInput(min_val=1)

        self.randomseed_label = QtWidgets.QLabel(__("Random Seed"))
        self.randomseed_input = IntValueInput()

        self.ramptime_label = QtWidgets.QLabel(__("Time of ramp: "))
        self.ramptime_input = TimeInput()

        self.savemotion_label = QtWidgets.QLabel(__("Motion saving > "))
        self.savemotion_time_input = TimeInput(minwidth=85,maxwidth=85)
        self.savemotion_time_label = QtWidgets.QLabel(__("Time: "))
        self.savemotion_timedt_input = TimeInput(minwidth=85,maxwidth=85)
        self.savemotion_timedt_label = QtWidgets.QLabel(__("DT Time: "))
        self.savemotion_xpos_input = SizeInput(minwidth=85,maxwidth=85)
        self.savemotion_xpos_label = QtWidgets.QLabel(__("X Pos: "))
        self.savemotion_zpos_input = SizeInput(minwidth=85,maxwidth=85)
        self.savemotion_zpos_label = QtWidgets.QLabel(__("Z Pos: "))

        self.xf_label = QtWidgets.QLabel(__("Focused location: "))
        self.xf_input = ValueInput()

        self.fphase_label = QtWidgets.QLabel(__("Focused phase (deg): "))
        self.fphase_input = ValueInput()

        self.maxwaveh_label = QtWidgets.QLabel(__("Compute maximum wave H"))
        self.maxwaveh_nwaves_label = QtWidgets.QLabel(__("Number of waves: "))
        self.maxwaveh_nwaves_input = IntValueInput(min_val=1)

        self.maxwaveh_time_label = QtWidgets.QLabel(__("Time:"))
        self.maxwaveh_time_input = TimeInput()

        self.fpretime_label = QtWidgets.QLabel(__("Initial extra time for focus generation: "))
        self.fpretime_input = TimeInput()
    
        self.fmovtime_label = QtWidgets.QLabel(__("Final time for paddle motion: "))
        self.fmovtime_input = TimeInput()

        self.fmovramp_label = QtWidgets.QLabel(__("Final ramp time before final time motion: "))
        self.fmovramp_input = TimeInput()

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
        for x in [self.ramptime_label, self.ramptime_input]:
            self.sixth_row_layout.addWidget(x)

        self.seventh_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.savemotion_label, self.savemotion_time_label, self.savemotion_time_input, self.savemotion_timedt_label, self.savemotion_timedt_input,
                  self.savemotion_xpos_label, self.savemotion_xpos_input, self.savemotion_zpos_label, self.savemotion_zpos_input]:
            self.seventh_row_layout.addWidget(x)

        self.eighth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.xf_label, self.xf_input, self.fphase_label,self.fphase_input]:
            self.eighth_row_layout.addWidget(x)

        self.ninth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.maxwaveh_label]: 
            self.ninth_row_layout.addWidget(x)
        
        self.tenth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.maxwaveh_nwaves_label, self.maxwaveh_nwaves_input, 
            self.maxwaveh_time_label, self.maxwaveh_time_input]: 
            self.tenth_row_layout.addWidget(x)

        self.eleventh_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.fpretime_label, self.fpretime_input]:
            self.eleventh_row_layout.addWidget(x)

        self.twelfth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.fmovtime_label, self.fmovtime_input]:
            self.twelfth_row_layout.addWidget(x)

        self.thirteenth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.fmovramp_label, self.fmovramp_input]:
            self.thirteenth_row_layout.addWidget(x)

        self.wave_generator_layout.addLayout(self.root_layout)
        self.wave_generator_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, 
            self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout, 
            self.seventh_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.wave_generator_layout.addWidget(h_line_generator())

        for x in [self.eighth_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.wave_generator_layout.addWidget(h_line_generator())
        
        for x in [self.ninth_row_layout,self.tenth_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.wave_generator_layout.addWidget(h_line_generator())

        for x in [self.eleventh_row_layout,self.twelfth_row_layout,self.thirteenth_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(focused_wave_gen)
        self._init_connections()

    def fill_values(self, focused_wave_gen):

        """ Fills the value from the data structure onto the widget. """
        self.duration_input.setValue(focused_wave_gen.duration)
        self.wave_order_selector.setCurrentIndex(
            int(focused_wave_gen.wave_order) - 1)
        self.depth_input.setValue(focused_wave_gen.depth)
        self.piston_dir_x.setValue(focused_wave_gen.piston_dir[0])
        self.piston_dir_y.setValue(focused_wave_gen.piston_dir[1])
        self.piston_dir_z.setValue(focused_wave_gen.piston_dir[2])
        self.wave_height_input.setValue(focused_wave_gen.wave_height)
        self.wave_period_input.setValue(focused_wave_gen.wave_period)
        self.gainstroke_input.setValue(focused_wave_gen.gainstroke)
        self.spectrum_selector.setCurrentIndex({IrregularSpectrum.JONSWAP: 0, IrregularSpectrum.PIERSON_MOSKOWITZ: 1}[focused_wave_gen.spectrum])
        self.discretization_selector.setCurrentIndex({IrregularDiscretization.REGULAR: 0,
                                                      IrregularDiscretization.RANDOM: 1,
                                                      IrregularDiscretization.STRETCHED: 2,
                                                      IrregularDiscretization.COSSTRETCHED: 3}[focused_wave_gen.discretization])
        self.peak_coef_input.setValue(focused_wave_gen.peak_coef)
        self.waves_input.setValue(focused_wave_gen.waves)
        self.randomseed_input.setValue(focused_wave_gen.randomseed)
        self.ramptime_input.setValue(focused_wave_gen.ramptime)
        self.savemotion_time_input.setValue(focused_wave_gen.savemotion_time)
        self.savemotion_timedt_input.setValue(focused_wave_gen.savemotion_timedt)
        self.savemotion_xpos_input.setValue(focused_wave_gen.savemotion_xpos)
        self.savemotion_zpos_input.setValue(focused_wave_gen.savemotion_zpos)
        
        self.xf_input.setValue(focused_wave_gen.xf)
        self.fphase_input.setValue(focused_wave_gen.fphase)
        self.maxwaveh_nwaves_input.setValue(focused_wave_gen.maxwaveh_nwaves)
        self.maxwaveh_time_input.setValue(focused_wave_gen.maxwaveh_time)
        self.fpretime_input.setValue(focused_wave_gen.fpretime)
        self.fmovtime_input.setValue(focused_wave_gen.fmovtime)
        self.fmovramp_input.setValue(focused_wave_gen.fmovramp)

   
    def _init_connections(self):
        for x in [self.wave_order_selector, self.spectrum_selector, self.discretization_selector]:
            x.currentIndexChanged.connect(self.on_change)

        for x in [self.peak_coef_input, self.waves_input, self.randomseed_input,
                  self.ramptime_input, self.duration_input,self.depth_input, 
                  self.piston_dir_x, self.piston_dir_y, self.piston_dir_z, 
                  self.wave_height_input, self.wave_period_input, 
                  self.gainstroke_input, self.savemotion_time_input,
                  self.savemotion_timedt_input, self.savemotion_xpos_input,
                  self.savemotion_zpos_input,self.xf_input, self.fphase_input, 
                  self.maxwaveh_nwaves_input, self.maxwaveh_time_input, 
                  self.fpretime_input, self.fmovtime_input, self.fmovramp_input]:
            x.value_changed.connect(self.on_change)

    def on_change(self):
        """ Reacts to change, and fires an event with the resulting object. """
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            warning_dialog("Introduced an invalid value for a float number.")


    def construct_motion_object(self):
        """ Constructs an object from the data introduced in the widget. """


        return FocusedPistonWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
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
                                      ramptime=self.ramptime_input.value(),
                                      savemotion_time=self.savemotion_time_input.value(),
                                      savemotion_timedt=self.savemotion_timedt_input.value(),
                                      savemotion_xpos=self.savemotion_xpos_input.value(),
                                      savemotion_zpos=self.savemotion_zpos_input.value(),
                                      xf=self.xf_input.value(),
                                      fphase=self.fphase_input.value(),
                                      maxwaveh_nwaves=self.maxwaveh_nwaves_input.value(),
                                      maxwaveh_time=self.maxwaveh_time_input.value(),
                                      fpretime=self.fpretime_input.value(),
                                      fmovtime=self.fmovtime_input.value(),
                                      fmovramp=self.fmovramp_input.value()
                                      )

    def on_delete(self):
        """ Deletes the currently defined object. """
        self.deleted.emit(self.index, self.construct_motion_object())
