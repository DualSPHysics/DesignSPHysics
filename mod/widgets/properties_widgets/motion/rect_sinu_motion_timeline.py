#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Rectilinear Sinusoidal Motion Timeline """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.rect_sinu_motion import RectSinuMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class RectSinuMotionTimeline(MotionTimeline):
    """ A sinusoidal rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RectSinuMotion)
    deleted = QtCore.Signal(int, RectSinuMotion)
    
    def __init__(self, index, rect_sinu_motion, parent=None):
        if not isinstance(rect_sinu_motion, RectSinuMotion):
            raise TypeError("You tried to spawn an accelerated circular motion widget in the timeline with a wrong object")
        if rect_sinu_motion is None:
            raise TypeError("You tried to spawn an accelerated circular motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtWidgets.QLabel("Sinusoidal \nRectilinear \nMotion ")
        self.label.setMinimumWidth(75)
        self.rows_layout = QtWidgets.QVBoxLayout()
        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout = QtWidgets.QHBoxLayout()
        
        self.freq_label = QtWidgets.QLabel("Freq (X, Y, Z): ")
        self.amp_label = QtWidgets.QLabel("Amp (X, Y, Z): ")
        self.freq_x_input = ValueInput(minwidth=60,maxwidth=60)
        self.freq_y_input = ValueInput(minwidth=60,maxwidth=60)
        self.freq_z_input = ValueInput(minwidth=60,maxwidth=60)
        self.amp_x_input = SizeInput(minwidth=85,maxwidth=85)
        self.amp_y_input = SizeInput(minwidth=85,maxwidth=85)
        self.amp_z_input = SizeInput(minwidth=85,maxwidth=85)

        self.phase_label = QtWidgets.QLabel("Phase (X, Y, Z): ")
        self.phase_x_input = ValueInput(minwidth=60,maxwidth=60)
        self.phase_y_input = ValueInput(minwidth=60,maxwidth=60)
        self.phase_z_input = ValueInput(minwidth=60,maxwidth=60)

        self.time_label = QtWidgets.QLabel(__("Duration:"))
        self.time_input = TimeInput(minwidth=75,maxwidth=75)
        self.delete_button = QtWidgets.QPushButton(
            get_icon("trash.png"), None)
        self.order_button_layout = QtWidgets.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtWidgets.QPushButton(
            get_icon("up_arrow.png"), None)
        self.order_down_button = QtWidgets.QPushButton(
            get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.first_row_layout.addWidget(self.freq_label)
        self.first_row_layout.addWidget(self.freq_x_input)
        self.first_row_layout.addWidget(self.freq_y_input)
        self.first_row_layout.addWidget(self.freq_z_input)
        self.second_row_layout.addWidget(self.amp_label)
        self.second_row_layout.addWidget(self.amp_x_input)
        self.second_row_layout.addWidget(self.amp_y_input)
        self.second_row_layout.addWidget(self.amp_z_input)
        self.third_row_layout.addWidget(self.phase_label)
        self.third_row_layout.addWidget(self.phase_x_input)
        self.third_row_layout.addWidget(self.phase_y_input)
        self.third_row_layout.addWidget(self.phase_z_input)
        self.rows_layout.addLayout(self.first_row_layout)
        self.rows_layout.addLayout(self.second_row_layout)
        self.rows_layout.addLayout(self.third_row_layout)
        self.main_layout.addLayout(self.rows_layout)

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rect_sinu_motion)
        self._init_connections()

    def fill_values(self, rect_sinu_motion):
        """ Fills the values from the data structure onto the widget. """
        self.freq_x_input.setValue(rect_sinu_motion.freq[0])
        self.freq_y_input.setValue(rect_sinu_motion.freq[1])
        self.freq_z_input.setValue(rect_sinu_motion.freq[2])
        self.amp_x_input.setValue(rect_sinu_motion.ampl[0])
        self.amp_y_input.setValue(rect_sinu_motion.ampl[1])
        self.amp_z_input.setValue(rect_sinu_motion.ampl[2])
        self.phase_x_input.setValue(rect_sinu_motion.phase[0])
        self.phase_y_input.setValue(rect_sinu_motion.phase[1])
        self.phase_z_input.setValue(rect_sinu_motion.phase[2])
        self.time_input.setValue(rect_sinu_motion.duration)

    def _init_connections(self):
        self.freq_x_input.value_changed.connect(self.on_change)
        self.freq_y_input.value_changed.connect(self.on_change)
        self.freq_z_input.value_changed.connect(self.on_change)
        self.phase_x_input.value_changed.connect(self.on_change)
        self.phase_y_input.value_changed.connect(self.on_change)
        self.phase_z_input.value_changed.connect(self.on_change)
        self.amp_x_input.value_changed.connect(self.on_change)
        self.amp_y_input.value_changed.connect(self.on_change)
        self.amp_z_input.value_changed.connect(self.on_change)
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def construct_motion_object(self):
        """ Constructs a RectSinuMotion object from the values in the widget. """
        return RectSinuMotion(
            phase=[self.phase_x_input.value(),
                   self.phase_y_input.value(),
                   self.phase_z_input.value()],
            freq=[self.freq_x_input.value(),
                  self.freq_y_input.value(),
                  self.freq_z_input.value()],
            ampl=[self.amp_x_input.value(),
                  self.amp_y_input.value(),
                  self.amp_z_input.value()],
            duration=self.time_input.value())
