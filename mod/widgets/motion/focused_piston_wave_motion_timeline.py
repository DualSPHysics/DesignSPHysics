#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Focused Piston Wave Motion Timeline Widget"""

# from PySide import QtCore, QtGui
from PySide6 import QtCore, QtWidgets

from mod.translation_tools import __
from mod.gui_tools import h_line_generator
from mod.stdout_tools import debug

from mod.enums import  IrregularSpectrum, IrregularDiscretization

from mod.dataobjects.motion.focused_piston_wave_gen import FocusedPistonWaveGen

from mod.functions import make_float

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

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.root_label = QtWidgets.QLabel(__("Focused wave generator (Piston)"))

        self.duration_label = QtWidgets.QLabel(__("Duration"))
        self.duration_input = QtWidgets.QLineEdit()

        self.wave_order_label = QtWidgets.QLabel(__("Wave Order"))
        self.wave_order_selector = QtWidgets.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtWidgets.QLabel(__("Depth (m): "))
        self.depth_input = QtWidgets.QLineEdit()

        self.piston_dir_label = QtWidgets.QLabel(
            __("Piston direction (X, Y, Z): "))
        self.piston_dir_x = QtWidgets.QLineEdit()
        self.piston_dir_y = QtWidgets.QLineEdit()
        self.piston_dir_z = QtWidgets.QLineEdit()

        self.wave_height_label = QtWidgets.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtWidgets.QLineEdit()

        self.wave_period_label = QtWidgets.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtWidgets.QLineEdit()

        self.gainstroke_label = QtWidgets.QLabel(__("Gain factor: "))
        self.gainstroke_input = QtWidgets.QLineEdit()

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
        self.peak_coef_input = QtWidgets.QLineEdit()

        self.waves_label = QtWidgets.QLabel(__("Number of waves"))
        self.waves_input = QtWidgets.QLineEdit()

        self.randomseed_label = QtWidgets.QLabel(__("Random Seed"))
        self.randomseed_input = QtWidgets.QLineEdit()

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

        self.xf_label = QtWidgets.QLabel(__("Focused location: "))
        self.xf_input = QtWidgets.QLineEdit()

        self.fphase_label = QtWidgets.QLabel(__("Focused phase (deg): "))
        self.fphase_input = QtWidgets.QLineEdit()

        self.maxwaveh_label = QtWidgets.QLabel(__("Compute maximum wave H"))
        self.maxwaveh_nwaves_label = QtWidgets.QLabel(__("Number of waves: "))
        self.maxwaveh_nwaves_input = QtWidgets.QLineEdit()

        self.maxwaveh_time_label = QtWidgets.QLabel(__("Time (s): "))
        self.maxwaveh_time_input = QtWidgets.QLineEdit()

        self.fpretime_label = QtWidgets.QLabel(__("Initial extra time for focus generation (s): "))
        self.fpretime_input = QtWidgets.QLineEdit()
    
        self.fmovtime_label = QtWidgets.QLabel(__("Final time for paddle motion (s): "))
        self.fmovtime_input = QtWidgets.QLineEdit()

        self.fmovramp_label = QtWidgets.QLabel(__("Final ramp time before final time motion (s): "))
        self.fmovramp_input = QtWidgets.QLineEdit()

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

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout, 
            self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout, 
            self.seventh_row_layout]:
            self.main_layout.addLayout(x)

        self.main_layout.addWidget(h_line_generator())

        for x in [self.eighth_row_layout]:
            self.main_layout.addLayout(x)

        self.main_layout.addWidget(h_line_generator())
        
        for x in [self.ninth_row_layout,self.tenth_row_layout]:
            self.main_layout.addLayout(x)

        self.main_layout.addWidget(h_line_generator())

        for x in [self.eleventh_row_layout,self.twelfth_row_layout,self.thirteenth_row_layout]:
            self.main_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(focused_wave_gen)
        self._init_connections()

    def fill_values(self, focused_wave_gen):

        """ Fills the value from the data structure onto the widget. """
        self.duration_input.setText(str(focused_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(focused_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(focused_wave_gen.depth))
        self.piston_dir_x.setText(str(focused_wave_gen.piston_dir[0]))
        self.piston_dir_y.setText(str(focused_wave_gen.piston_dir[1]))
        self.piston_dir_z.setText(str(focused_wave_gen.piston_dir[2]))
        self.wave_height_input.setText(str(focused_wave_gen.wave_height))
        self.wave_period_input.setText(str(focused_wave_gen.wave_period))
        self.gainstroke_input.setText(str(focused_wave_gen.gainstroke))
        self.spectrum_selector.setCurrentIndex({IrregularSpectrum.JONSWAP: 0, IrregularSpectrum.PIERSON_MOSKOWITZ: 1}[focused_wave_gen.spectrum])
        self.discretization_selector.setCurrentIndex({IrregularDiscretization.REGULAR: 0,
                                                      IrregularDiscretization.RANDOM: 1,
                                                      IrregularDiscretization.STRETCHED: 2,
                                                      IrregularDiscretization.COSSTRETCHED: 3}[focused_wave_gen.discretization])
        self.peak_coef_input.setText(str(focused_wave_gen.peak_coef))
        self.waves_input.setText(str(focused_wave_gen.waves))
        self.randomseed_input.setText(str(focused_wave_gen.randomseed))
        self.ramptime_input.setText(str(focused_wave_gen.ramptime))
        self.savemotion_time_input.setText(str(focused_wave_gen.savemotion_time))
        self.savemotion_timedt_input.setText(
            str(focused_wave_gen.savemotion_timedt))
        self.savemotion_xpos_input.setText(str(focused_wave_gen.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(focused_wave_gen.savemotion_zpos))
        
        self.xf_input.setText(str(focused_wave_gen.xf))
        self.fphase_input.setText(str(focused_wave_gen.fphase))
        self.maxwaveh_nwaves_input.setText(str(focused_wave_gen.maxwaveh_nwaves))
        self.maxwaveh_time_input.setText(str(focused_wave_gen.maxwaveh_time))
        self.fpretime_input.setText(str(focused_wave_gen.fpretime))
        self.fmovtime_input.setText(str(focused_wave_gen.fmovtime))
        self.fmovramp_input.setText(str(focused_wave_gen.fmovramp))

   
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
            x.textChanged.connect(self.on_change)

    def on_change(self):
        """ Reacts to change, sanitizes input and fires an event with the resulting object. """
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")


    def construct_motion_object(self):
        """ Constructs an object from the data introduced in the widget. """


        return FocusedPistonWaveGen(wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                      duration=make_float(self.duration_input.text()), depth=make_float(self.depth_input.text()),
                                      piston_dir=[make_float(self.piston_dir_x.text()), make_float(self.piston_dir_y.text()), make_float(self.piston_dir_z.text())],
                                      wave_height=make_float(self.wave_height_input.text()),
                                      wave_period=make_float(self.wave_period_input.text()),
                                      gainstroke=make_float(self.gainstroke_input.text()),
                                      spectrum={0: IrregularSpectrum.JONSWAP, 1: IrregularSpectrum.PIERSON_MOSKOWITZ}[self.spectrum_selector.currentIndex()],
                                      discretization={0: IrregularDiscretization.REGULAR, 1: IrregularDiscretization.RANDOM, 2: IrregularDiscretization.STRETCHED, 3: IrregularDiscretization.COSSTRETCHED}[self.discretization_selector.currentIndex()],
                                      peak_coef=make_float(self.peak_coef_input.text()),
                                      waves=make_float(self.waves_input.text()),
                                      randomseed=make_float(self.randomseed_input.text()),
                                      ramptime=make_float(self.ramptime_input.text()),
                                      savemotion_time=str(self.savemotion_time_input.text()),
                                      savemotion_timedt=str(self.savemotion_timedt_input.text()),
                                      savemotion_xpos=str(self.savemotion_xpos_input.text()),
                                      savemotion_zpos=str(self.savemotion_zpos_input.text())  ,
                                      xf=make_float(self.xf_input.text()),
                                      fphase=make_float(self.fphase_input.text()),
                                      maxwaveh_nwaves=make_float(self.maxwaveh_nwaves_input.text()),
                                      maxwaveh_time=make_float(self.maxwaveh_time_input.text()),
                                      fpretime=make_float(self.fpretime_input.text()),
                                      fmovtime=make_float(self.fmovtime_input.text()),
                                      fmovramp=make_float(self.fmovramp_input.text())                                
                                      )

    def on_delete(self):
        """ Deletes the currently defined object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        for x in [self.duration_input, self.depth_input, self.piston_dir_x,
                  self.piston_dir_y, self.piston_dir_z,
                  self.wave_height_input, self.wave_period_input, 
                  self.gainstroke_input, self.peak_coef_input, 
                  self.randomseed_input, self.ramptime_input, 
                  self.savemotion_time_input, self.savemotion_timedt_input,
                  self.savemotion_xpos_input, self.savemotion_zpos_input,
                  self.xf_input, self.fphase_input, self.maxwaveh_nwaves_input, 
                  self.maxwaveh_time_input, self.fpretime_input, 
                  self.fmovtime_input, self.fmovramp_input]:
            x.setText("0" if not x.text() else x.text().replace(",", "."))
