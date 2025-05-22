#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Soliotary Piston Wave Motion Timeline Widget """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.awas import AWAS
from mod.dataobjects.motion.awas_correction import AWASCorrection
from mod.dataobjects.motion.solitary_piston_wave_gen import SolitaryPistonWaveGen
from mod.enums import AWASWaveOrder, AWASSaveMethod
from mod.functions import make_float, make_int
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.tools.dialog_tools import warning_dialog

class SolitaryPistonWaveMotionTimeline(QtWidgets.QWidget):
    """ A Solitary Wave motion graphical representation for a table-based timeline """

    MINIMUM_TABLE_SECTION_HEIGHT = 64

    changed = QtCore.Signal(int, SolitaryPistonWaveGen)

    def __init__(self, sol_wave_gen, parent=None):
        if not isinstance(sol_wave_gen, SolitaryPistonWaveGen):
            raise TypeError("You tried to spawn a Solitary wave generator "
                            "motion widget in the timeline with a wrong object")
        if sol_wave_gen is None:
            raise TypeError("You tried to spawn a Solitary wave generator "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.solitary_waves = list()  # SolitaryWave
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

        self.root_label = QtWidgets.QLabel(__("Solitary wave generator (Piston)"))

        self.depth_label = QtWidgets.QLabel(__("Depth: "))
        self.depth_input = SizeInput()

        self.piston_dir_label = QtWidgets.QLabel(
            __("Piston direction (X, Y, Z): "))
        self.piston_dir_x = ValueInput()
        self.piston_dir_y = ValueInput()
        self.piston_dir_z = ValueInput()

        self.theory_label=QtWidgets.QLabel(__("Theory"))
        self.theory_input = QtWidgets.QComboBox()
        self.theory_input.addItem("1")
        self.theory_input.addItem("2")
        self.theory_input.addItem("3")
        self.theory_input.setMaximumWidth(160)

        self.n_waves_label = QtWidgets.QLabel(__("Number of waves"))
        self.n_waves_input = QtWidgets.QComboBox()
        self.n_waves_input.addItem("1")
        self.n_waves_input.addItem("2")
        self.n_waves_input.addItem("3")
        self.n_waves_input.setMaximumWidth(160)

        self.wave_1_height_label = QtWidgets.QLabel(__("Wave 1:  Wave height:"))
        self.wave_1_height_input = SizeInput()
        self.wave_1_duration_coef_label = QtWidgets.QLabel(__("Duration coef: "))
        self.wave_1_duration_coef_input = ValueInput()

        self.wave_2_height_label = QtWidgets.QLabel(__("Wave 2:  Wave height:"))
        self.wave_2_height_input = SizeInput()
        self.wave_2_height_input.setEnabled(False)
        self.wave_2_duration_coef_label = QtWidgets.QLabel(__("Duration coef:"))
        self.wave_2_duration_coef_input = ValueInput()
        self.wave_2_duration_coef_input.setEnabled(False)
        self.wave_2_start_coef_label = QtWidgets.QLabel(__("Start coef:"))
        self.wave_2_start_coef_input = ValueInput()
        self.wave_2_start_coef_input.setEnabled(False)


        self.wave_3_height_label = QtWidgets.QLabel(__("Wave 3:  Wave height:"))
        self.wave_3_height_input =SizeInput()
        self.wave_3_height_input.setEnabled(False)
        self.wave_3_duration_coef_label = QtWidgets.QLabel(__("Duration coef:"))
        self.wave_3_duration_coef_input = ValueInput()
        self.wave_3_duration_coef_input.setEnabled(False)
        self.wave_3_start_coef_label = QtWidgets.QLabel(__("Start coef:"))
        self.wave_3_start_coef_input = ValueInput()
        self.wave_3_start_coef_input.setEnabled(False)


        self.savemotion_label = QtWidgets.QLabel(__("Motion saving > "))
        self.savemotion_time_input = TimeInput()
        self.savemotion_time_label = QtWidgets.QLabel(__("Time:"))
        self.savemotion_timedt_input = TimeInput()
        self.savemotion_timedt_label = QtWidgets.QLabel(__("DT Time:"))
        self.savemotion_xpos_input = SizeInput()
        self.savemotion_xpos_label = QtWidgets.QLabel(__("X Pos:"))

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

        self.awas_gaugex_label = QtWidgets.QLabel(__("Gauge X (value*h): "))
        self.awas_gaugex_input = ValueInput()

        self.awas_gaugey_label = QtWidgets.QLabel(__("Gauge Y:"))
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
        self.awas_savedata_selector.setMaximumWidth(160)

        self.awas_limitace_label = QtWidgets.QLabel(__("Limit acceleration: "))
        self.awas_limitace_input = ValueInput()

        self.awas_correction_label = QtWidgets.QLabel(__("Drift correction: "))
        self.awas_correction_enabled = QtWidgets.QCheckBox(__("Enabled"))

        self.awas_correction_coefstroke_label = QtWidgets.QLabel(__("Coefstroke"))
        self.awas_correction_coefstroke_input = ValueInput(minwidth=70,maxwidth=70)

        self.awas_correction_coefperiod_label = QtWidgets.QLabel(__("Coefperiod"))
        self.awas_correction_coefperiod_input = ValueInput(minwidth=70,maxwidth=70)

        self.awas_correction_powerfunc_label = QtWidgets.QLabel(__("Powerfunc"))
        self.awas_correction_powerfunc_input = ValueInput(minwidth=70,maxwidth=70)

        self.root_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)

        self.first_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.depth_label, self.depth_input]:
            self.first_row_layout.addWidget(x)

        self.second_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.piston_dir_label, self.piston_dir_x, self.piston_dir_y, self.piston_dir_z]:
            self.second_row_layout.addWidget(x, 10, QtCore.Qt.AlignLeft)

        self.third_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout.addWidget(self.theory_label)
        self.third_row_layout.addWidget(self.theory_input)
        self.third_row_layout.addWidget(self.n_waves_label)
        self.third_row_layout.addWidget(self.n_waves_input)

        self.fourth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_1_height_label,self.wave_1_height_input,self.wave_1_duration_coef_label,self.wave_1_duration_coef_input]:
            self.fourth_row_layout.addWidget(x)

        self.fifth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_2_height_label ,self.wave_2_height_input,self.wave_2_duration_coef_label, self.wave_2_duration_coef_input,
                 self.wave_2_start_coef_label,self.wave_2_start_coef_input]:
            self.fifth_row_layout.addWidget(x)

        self.sixth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.wave_3_height_label, self.wave_3_height_input,self.wave_3_duration_coef_label,
                  self.wave_3_duration_coef_input, self.wave_3_start_coef_label, self.wave_3_start_coef_input ]:
            self.sixth_row_layout.addWidget(x)


        self.savemotion_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.savemotion_label, self.savemotion_time_label, self.savemotion_time_input,
                  self.savemotion_timedt_label, self.savemotion_timedt_input,
                  self.savemotion_xpos_label, self.savemotion_xpos_input]:
            self.savemotion_row_layout.addWidget(x)

        self.awas_root_layout = QtWidgets.QHBoxLayout()
        self.awas_root_layout.addWidget(self.awas_label)
        self.awas_root_layout.addWidget(self.awas_enabled)

        self.awas_first_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_startawas_label, self.awas_startawas_input, self.awas_swl_label, self.awas_swl_input,
                  self.awas_elevation_label, self.awas_elevation_selector]:
            self.awas_first_row_layout.addWidget(x)

        self.awas_second_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_gaugex_label, self.awas_gaugex_input, self.awas_gaugey_label, self.awas_gaugey_input]:
            self.awas_second_row_layout.addWidget(x)

        self.awas_third_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_gaugezmin_label, self.awas_gaugezmin_input, self.awas_gaugezmax_label,
                  self.awas_gaugezmax_input]:
            self.awas_third_row_layout.addWidget(x)

        self.awas_fourth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_gaugedp_label, self.awas_gaugedp_input, self.awas_coefmasslimit_label,
                  self.awas_coefmasslimit_input]:
            self.awas_fourth_row_layout.addWidget(x)

        self.awas_fifth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_savedata_label, self.awas_savedata_selector, self.awas_limitace_label,
                  self.awas_limitace_input]:
            self.awas_fifth_row_layout.addWidget(x)

        self.awas_sixth_row_layout = QtWidgets.QHBoxLayout()
        for x in [self.awas_correction_label, self.awas_correction_enabled, self.awas_correction_coefstroke_label,
                  self.awas_correction_coefstroke_input,
                  self.awas_correction_coefperiod_label, self.awas_correction_coefperiod_input,
                  self.awas_correction_powerfunc_label, self.awas_correction_powerfunc_input]:
            self.awas_sixth_row_layout.addWidget(x)

        self.wave_generator_layout.addLayout(self.root_layout)
        self.wave_generator_layout.addWidget(h_line_generator())
        for x in [self.first_row_layout, self.second_row_layout,
                  self.third_row_layout, self.fourth_row_layout,
                  self.fifth_row_layout, self.sixth_row_layout,
                  self.savemotion_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.wave_generator_layout.addWidget(h_line_generator())
        self.wave_generator_layout.addLayout(self.awas_root_layout)
        self.wave_generator_layout.addWidget(h_line_generator())
        for x in [self.awas_first_row_layout,
                  self.awas_second_row_layout, self.awas_third_row_layout,
                  self.awas_fourth_row_layout, self.awas_fifth_row_layout,
                  self.awas_sixth_row_layout]:
            self.wave_generator_layout.addLayout(x)

        self.setLayout(self.main_layout)
        self.fill_values(sol_wave_gen)
        self._init_connections()

    def fill_values(self, sol_wave_gen):
        """ Fills the values from the data structure onto the widget. """

        self.depth_input.setValue(sol_wave_gen.depth)
        self.piston_dir_x.setValue(sol_wave_gen.piston_dir[0])
        self.piston_dir_y.setValue(sol_wave_gen.piston_dir[1])
        self.piston_dir_z.setValue(sol_wave_gen.piston_dir[2])
        self.wave_1_height_input.setValue(sol_wave_gen.wave_height)
        self.wave_1_duration_coef_input.setValue(sol_wave_gen.wave_1_duration_coef)
        self.wave_2_height_input.setValue(sol_wave_gen.wave_2_height)
        self.wave_2_duration_coef_input.setValue(sol_wave_gen.wave_2_duration_coef)
        self.wave_2_start_coef_input.setValue(sol_wave_gen.wave_2_start_coef)
        self.wave_3_height_input.setValue(sol_wave_gen.wave_3_height)
        self.wave_3_duration_coef_input.setValue(sol_wave_gen.wave_3_duration_coef)
        self.wave_3_start_coef_input.setValue(sol_wave_gen.wave_3_start_coef)
        self.theory_input.setCurrentIndex(sol_wave_gen.theory-1)
        self.n_waves_input.setCurrentIndex(sol_wave_gen.n_waves - 1)
        self.savemotion_time_input.setValue(sol_wave_gen.savemotion_time)
        self.savemotion_timedt_input.setValue(sol_wave_gen.savemotion_timedt)
        self.savemotion_xpos_input.setValue(sol_wave_gen.savemotion_xpos)
        self.awas_enabled.setChecked(bool(sol_wave_gen.awas.enabled))
        self.awas_startawas_input.setValue(sol_wave_gen.awas.startawas)
        self.awas_swl_input.setValue(sol_wave_gen.awas.swl)
        self.awas_gaugex_input.setValue(sol_wave_gen.awas.gaugex)
        self.awas_gaugey_input.setValue(sol_wave_gen.awas.gaugey)
        self.awas_gaugezmin_input.setValue(sol_wave_gen.awas.gaugezmin)
        self.awas_gaugezmax_input.setValue(sol_wave_gen.awas.gaugezmax)
        self.awas_gaugedp_input.setValue(sol_wave_gen.awas.gaugedp)
        self.awas_coefmasslimit_input.setValue(sol_wave_gen.awas.coefmasslimit)
        self.awas_limitace_input.setValue(sol_wave_gen.awas.limitace)
        self.awas_elevation_selector.setCurrentIndex(
            int(sol_wave_gen.awas.elevation) - 1)
        self.awas_savedata_selector.setCurrentIndex(
            int(sol_wave_gen.awas.savedata) - 1)
        self.awas_correction_enabled.setChecked(
            bool(sol_wave_gen.awas.correction.enabled))
        self.awas_correction_coefstroke_input.setValue(sol_wave_gen.awas.correction.coefstroke)
        self.awas_correction_coefperiod_input.setValue(sol_wave_gen.awas.correction.coefperiod)
        self.awas_correction_powerfunc_input.setValue(sol_wave_gen.awas.correction.powerfunc)
        self._awas_enabled_handler()
        self._number_wave_change_handler()

    def _init_connections(self):
        self.awas_savedata_selector.currentIndexChanged.connect(self.on_change)
        self.awas_elevation_selector.currentIndexChanged.connect(
            self.on_change)
        self.awas_enabled.stateChanged.connect(self.on_change)
        self.awas_correction_enabled.stateChanged.connect(
            self._awas_correction_enabled_handler)
        self.n_waves_input.currentIndexChanged.connect(self._number_wave_change_handler)
        self.theory_input.currentIndexChanged.connect(self.on_change)
        for x in [self.depth_input, self.piston_dir_x,
                  self.piston_dir_y, self.piston_dir_z,
                  self.wave_1_height_input,
                  self.wave_1_duration_coef_input,
                  self.wave_2_height_input,
                  self.wave_2_duration_coef_input,
                  self.wave_2_start_coef_input,
                  self.wave_3_height_input,
                  self.wave_3_duration_coef_input,
                  self.wave_3_start_coef_input,
                  self.savemotion_time_input,
                  self.savemotion_timedt_input, self.savemotion_xpos_input,
                  self.awas_startawas_input,
                  self.awas_swl_input, self.awas_gaugex_input, self.awas_gaugedp_input,
                  self.awas_gaugey_input, self.awas_gaugezmin_input,
                  self.awas_gaugezmax_input, self.awas_coefmasslimit_input,
                  self.awas_limitace_input,
                  self.awas_correction_coefstroke_input,
                  self.awas_correction_coefperiod_input,
                  self.awas_correction_powerfunc_input]:
            x.value_changed.connect(self.on_change)

    def on_change(self):
        """ Reacts to input change, sanitizing it and firing a signal with the correspondent data object. """
        # self._sanitize_input()
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

        for x in [self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
                  self.awas_correction_coefperiod_input]:
            x.setEnabled(enable_state)

    def _number_wave_change_handler(self):
        enable_wave_2 = int(self.n_waves_input.itemText(self.n_waves_input.currentIndex())) > 1
        enable_wave_3 = int(self.n_waves_input.itemText(self.n_waves_input.currentIndex())) > 2

        for x in [self.wave_2_height_input, self.wave_2_start_coef_input,self.wave_2_duration_coef_input]:
            x.setEnabled(enable_wave_2)
        for x in [self.wave_3_height_input, self.wave_3_start_coef_input, self.wave_3_duration_coef_input]:
            x.setEnabled(enable_wave_3)

    def construct_motion_object(self):
        """ Constructs an SolitaryPistonWaveGen object from the data currently introduced on the widget. """
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

        return SolitaryPistonWaveGen(depth=self.depth_input.value(),
                                     piston_dir=[self.piston_dir_x.value(),
                                                 self.piston_dir_y.value(),
                                                 self.piston_dir_z.value()],
                                     theory=int(self.theory_input.itemText(self.theory_input.currentIndex())),
                                     wave_height=self.wave_1_height_input.value(),
                                     wave_2_height=self.wave_2_height_input.value(),
                                     wave_3_height=self.wave_3_height_input.value(),
                                     wave_1_duration_coef=self.wave_1_duration_coef_input.value(),
                                     wave_2_duration_coef=self.wave_2_duration_coef_input.value(),
                                     wave_3_duration_coef=self.wave_3_duration_coef_input.value(),
                                     wave_2_start_coef=self.wave_2_start_coef_input.value(),
                                     wave_3_start_coef=self.wave_3_start_coef_input.value(),
                                     n_waves=int(self.n_waves_input.itemText(self.n_waves_input.currentIndex())),
                                     savemotion_time=self.savemotion_time_input.value(),
                                     savemotion_timedt=self.savemotion_timedt_input.value(),
                                     savemotion_xpos=self.savemotion_xpos_input.value(),
                                     awas=awas_object)

    def on_delete(self):
        """ Deletes the currently represented motion object. """
        self.deleted.emit(self.index, self.construct_motion_object())
