#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Rotationial Sinusoidal Motion Timeline Widget. """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.rot_sinu_motion import RotSinuMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class RotSinuMotionTimeline(MotionTimeline):
    """ A sinusoidal rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RotSinuMotion)
    deleted = QtCore.Signal(int, RotSinuMotion)


    def __init__(self, index, rot_sinu_motion, parent=None):
        if not isinstance(rot_sinu_motion, RotSinuMotion):
            raise TypeError("You tried to spawn a sinusoidal rotational motion widget in the timeline with a wrong object")
        if rot_sinu_motion is None:
            raise TypeError("You tried to spawn a sinusoidal rotational motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtWidgets.QLabel("Sinusoidal \nRotational \nMotion ")
        self.label.setMinimumWidth(75)
        self.axis1_label = QtWidgets.QLabel(
            "Axis 1(X,Y,Z):")
        self.axis2_label = QtWidgets.QLabel(
            "Axis 2(X,Y,Z):")
        self.rows_layout = QtWidgets.QVBoxLayout()
        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout = QtWidgets.QHBoxLayout()
        self.x1_input = SizeInput(minwidth=85,maxwidth=85)
        self.y1_input = SizeInput(minwidth=85,maxwidth=85)
        self.z1_input = SizeInput(minwidth=85,maxwidth=85)
        self.x2_input = SizeInput(minwidth=85,maxwidth=85)
        self.y2_input = SizeInput(minwidth=85,maxwidth=85)
        self.z2_input = SizeInput(minwidth=85,maxwidth=85)

        self.freq_label = QtWidgets.QLabel("Freq")
        self.freq_input = ValueInput(minwidth=60,maxwidth=60)

        self.ampl_label = QtWidgets.QLabel("Ampl")
        self.ampl_input = SizeInput(minwidth=85,maxwidth=85)

        self.phase_label = QtWidgets.QLabel("Phase")
        self.phase_input = ValueInput(minwidth=60,maxwidth=60)

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
        self.first_row_layout.addWidget(self.axis1_label)
        self.first_row_layout.addWidget(self.x1_input)
        self.first_row_layout.addWidget(self.y1_input)
        self.first_row_layout.addWidget(self.z1_input)
        self.second_row_layout.addWidget(self.axis2_label)
        self.second_row_layout.addWidget(self.x2_input)
        self.second_row_layout.addWidget(self.y2_input)
        self.second_row_layout.addWidget(self.z2_input)

        self.third_row_layout.addWidget(self.freq_label)
        self.third_row_layout.addWidget(self.freq_input)
        self.third_row_layout.addWidget(self.ampl_label)
        self.third_row_layout.addWidget(self.ampl_input)
        self.third_row_layout.addWidget(self.phase_label)
        self.third_row_layout.addWidget(self.phase_input)

        self.main_layout.addLayout(self.rows_layout)

        self.rows_layout.addLayout(self.first_row_layout)
        self.rows_layout.addLayout(self.second_row_layout)
        self.rows_layout.addLayout(self.third_row_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rot_sinu_motion)
        self._init_connections()

    def fill_values(self, rot_sinu_motion):
        """ Fills the values from the data structure into the widget. """
        self.x1_input.setValue(rot_sinu_motion.axis1[0])
        self.y1_input.setValue(rot_sinu_motion.axis1[1])
        self.z1_input.setValue(rot_sinu_motion.axis1[2])
        self.x2_input.setValue(rot_sinu_motion.axis2[0])
        self.y2_input.setValue(rot_sinu_motion.axis2[1])
        self.z2_input.setValue(rot_sinu_motion.axis2[2])
        self.freq_input.setValue(rot_sinu_motion.freq)
        self.ampl_input.setValue(rot_sinu_motion.ampl)
        self.phase_input.setValue(rot_sinu_motion.phase)
        self.time_input.setValue(rot_sinu_motion.duration)

    def _init_connections(self):
        self.x1_input.value_changed.connect(self.on_change)
        self.y1_input.value_changed.connect(self.on_change)
        self.z1_input.value_changed.connect(self.on_change)
        self.x2_input.value_changed.connect(self.on_change)
        self.y2_input.value_changed.connect(self.on_change)
        self.z2_input.value_changed.connect(self.on_change)
        self.freq_input.value_changed.connect(self.on_change)
        self.ampl_input.value_changed.connect(self.on_change)
        self.phase_input.value_changed.connect(self.on_change)
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def construct_motion_object(self):
        """ Constructs a new RotSinuMotion object with the data currently introduced on the widget. """
        return RotSinuMotion(
            axis1=[self.x1_input.value(),
                   self.y1_input.value(),
                   self.z1_input.value()],
            axis2=[self.x2_input.value(),
                   self.y2_input.value(),
                   self.z2_input.value()],
            duration=self.time_input.value(), freq=self.freq_input.value(),
            ampl=self.ampl_input.text(), phase=self.phase_input.value())