#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Rotational Motion Timeline Widget """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.rot_motion import RotMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class RotationalMotionTimeline(MotionTimeline):
    """ A Rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RotMotion)
    deleted = QtCore.Signal(int, RotMotion)
    def __init__(self, index, rot_motion, parent=None):
        if not isinstance(rot_motion, RotMotion):
            raise TypeError("You tried to spawn a rotational motion widget in the timeline with a wrong object")
        if rot_motion is None:
            raise TypeError("You tried to spawn a rotational motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtWidgets.QLabel("Rotational \nMotion  ")
        self.label.setMinimumWidth(75)
        self.velocity_label = QtWidgets.QLabel("Vel: ")
        self.velocity_input = VelocityInput(minwidth=85,maxwidth=85)
        self.axis_label = QtWidgets.QLabel("Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtWidgets.QVBoxLayout()
        self.axis_first_row_layout = QtWidgets.QHBoxLayout()
        self.axis_second_row_layout = QtWidgets.QHBoxLayout()
        self.x1_input = SizeInput(minwidth=85,maxwidth=85)
        self.y1_input = SizeInput(minwidth=85,maxwidth=85)
        self.z1_input = SizeInput(minwidth=85,maxwidth=85)
        self.x2_input = SizeInput(minwidth=85,maxwidth=85)
        self.y2_input = SizeInput(minwidth=85,maxwidth=85)
        self.z2_input = SizeInput(minwidth=85,maxwidth=85)
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
        self.main_layout.addWidget(self.velocity_label)
        self.main_layout.addWidget(self.velocity_input)
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rot_motion)
        self._init_connections()

    def fill_values(self, rot_motion):
        """ Fills values from the data structure onto the widget. """
        self.x1_input.setValue(rot_motion.axis1[0])
        self.y1_input.setValue(rot_motion.axis1[1])
        self.z1_input.setValue(rot_motion.axis1[2])
        self.x2_input.setValue(rot_motion.axis2[0])
        self.y2_input.setValue(rot_motion.axis2[1])
        self.z2_input.setValue(rot_motion.axis2[2])
        self.velocity_input.setValue(rot_motion.ang_vel)
        self.time_input.setValue(rot_motion.duration)

    def _init_connections(self):
        self.x1_input.value_changed.connect(self.on_change)
        self.y1_input.value_changed.connect(self.on_change)
        self.z1_input.value_changed.connect(self.on_change)
        self.x2_input.value_changed.connect(self.on_change)
        self.y2_input.value_changed.connect(self.on_change)
        self.z2_input.value_changed.connect(self.on_change)
        self.velocity_input.value_changed.connect(self.on_change)
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def construct_motion_object(self):
        """ Constructs a new RotMotion with the data currently introduced on the widget. """
        return RotMotion(
            ang_vel=self.velocity_input.value(),
            axis1=[self.x1_input.value(),
                   self.y1_input.value(),
                   self.z1_input.value()],
            axis2=[self.x2_input.value(),
                   self.y2_input.value(),
                   self.z2_input.value()],
            duration=self.time_input.value())

