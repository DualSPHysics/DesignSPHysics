#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Accelerated Rectilinear Motion widget"""

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.acc_rect_motion import AccRectMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.acceleration_input import AccelerationInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class AccRectilinearMotionTimeline(MotionTimeline):
    """ An accelerated rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, AccRectMotion)
    deleted = QtCore.Signal(int, AccRectMotion)
    
    def __init__(self, index, acc_rect_motion, parent=None):
        if not isinstance(acc_rect_motion, AccRectMotion):
            raise TypeError("You tried to spawn an accelerated rectilinear "
                            "motion widget in the timeline with a wrong object")
        if acc_rect_motion is None:
            raise TypeError("You tried to spawn an accelerated rectilinear "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index
        self.setMinimumHeight(50)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtWidgets.QLabel("Accelerated \nRectilinear \nMotion ")
        self.label.setMinimumWidth(75)
        self.data_layout = QtWidgets.QVBoxLayout()
        self.data_layout.setContentsMargins(0, 0, 0, 0)
        self.data_velocity_layout = QtWidgets.QHBoxLayout()
        self.data_velocity_layout.setContentsMargins(0, 0, 0, 0)
        self.data_acceleration_layout = QtWidgets.QHBoxLayout()
        self.data_acceleration_layout.setContentsMargins(0, 0, 0, 0)

        self.velocity_label = QtWidgets.QLabel("Vel (X, Y, Z): ")
        self.x_input = VelocityInput(minwidth=80,maxwidth=80)
        self.y_input = VelocityInput(minwidth=80,maxwidth=80)
        self.z_input = VelocityInput(minwidth=80,maxwidth=80)

        self.acceleration_label = QtWidgets.QLabel("Acc (X, Y, Z): ")
        self.xa_input = AccelerationInput(minwidth=100,maxwidth=100)
        self.ya_input = AccelerationInput(minwidth=100,maxwidth=100)
        self.za_input = AccelerationInput(minwidth=100,maxwidth=100)

        self.data_velocity_layout.addWidget(self.velocity_label)
        self.data_velocity_layout.addWidget(self.x_input)
        self.data_velocity_layout.addWidget(self.y_input)
        self.data_velocity_layout.addWidget(self.z_input)

        self.data_acceleration_layout.addWidget(self.acceleration_label)
        self.data_acceleration_layout.addWidget(self.xa_input)
        self.data_acceleration_layout.addWidget(self.ya_input)
        self.data_acceleration_layout.addWidget(self.za_input)

        self.data_layout.addLayout(self.data_velocity_layout)
        self.data_layout.addLayout(self.data_acceleration_layout)

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
        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_rect_motion)
        self._init_connections()

    def fill_values(self, acc_rect_motion):
        """ Fills the values from the data structure for the dialog. """
        self.x_input.setValue(acc_rect_motion.velocity[0])
        self.y_input.setValue(acc_rect_motion.velocity[1])
        self.z_input.setValue(acc_rect_motion.velocity[2])
        self.xa_input.setValue(acc_rect_motion.acceleration[0])
        self.ya_input.setValue(acc_rect_motion.acceleration[1])
        self.za_input.setValue(acc_rect_motion.acceleration[2])
        self.time_input.setValue(acc_rect_motion.duration)

    def _init_connections(self):
        self.x_input.value_changed.connect(self.on_change)
        self.y_input.value_changed.connect(self.on_change)
        self.z_input.value_changed.connect(self.on_change)
        self.xa_input.value_changed.connect(self.on_change)
        self.ya_input.value_changed.connect(self.on_change)
        self.za_input.value_changed.connect(self.on_change)
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def construct_motion_object(self):
        """ Constructs an AccRectMotion object with the data on the widget. """
        return AccRectMotion(
            velocity=[self.x_input.value(),
                      self.y_input.value(),
                      self.z_input.value()],
            acceleration=[self.xa_input.value(),
                          self.ya_input.value(),
                          self.za_input.value()],
            duration=self.time_input.value())