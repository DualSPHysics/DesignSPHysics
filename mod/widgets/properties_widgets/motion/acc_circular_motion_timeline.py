#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Accelerated Circular Motion Timeline widget"""

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.motion.acc_cir_motion import AccCirMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.acceleration_input import AccelerationInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class AccCircularMotionTimeline(MotionTimeline):
    """ An accelerated circular motion graphical representation for a table-based timeline """
    changed = QtCore.Signal(int, AccCirMotion)
    deleted = QtCore.Signal(int, AccCirMotion)

    def __init__(self, index, acc_cir_motion, parent=None):
        if not isinstance(acc_cir_motion, AccCirMotion):
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline with a wrong object")
        if acc_cir_motion is None:
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.rows_layout=QtWidgets.QVBoxLayout()
        self.first_row_layout=QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Accelerated \nCircular \nMotion ")
        self.label.setMinimumWidth(79)
        self.velocity_label = QtWidgets.QLabel("Vel:")
        self.velocity_input = VelocityInput(minwidth=80,maxwidth=80)
        self.acceleration_label = QtWidgets.QLabel("Acc:")
        self.acceleration_input = AccelerationInput(minwidth=100,maxwidth=100)
        self.axis1_label = QtWidgets.QLabel(
            "Axis 1(X,Y,Z):")
        self.axis2_label = QtWidgets.QLabel(
            "Axis 2(X,Y,Z):")

        self.x1_input = SizeInput(minwidth=85,maxwidth=85)
        self.y1_input = SizeInput(minwidth=85,maxwidth=85)
        self.z1_input = SizeInput(minwidth=85,maxwidth=85)
        self.x2_input = SizeInput(minwidth=85,maxwidth=85)
        self.y2_input = SizeInput(minwidth=85,maxwidth=85)
        self.z2_input = SizeInput(minwidth=85,maxwidth=85)

        self.reference_label = QtWidgets.QLabel("Ref(X,Y,Z):")
        self.reference_x_input = SizeInput(minwidth=85,maxwidth=85)
        self.reference_y_input = SizeInput(minwidth=85,maxwidth=85)
        self.reference_z_input = SizeInput(minwidth=85,maxwidth=85)
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

        self.main_layout.addWidget(self.label)
        self.rows_layout.addLayout(self.first_row_layout)
        self.rows_layout.addLayout(self.second_row_layout)
        self.rows_layout.addLayout(self.third_row_layout)
        self.main_layout.addLayout(self.rows_layout)
        self.first_row_layout.addWidget(self.velocity_label)
        self.first_row_layout.addWidget(self.velocity_input)
        self.second_row_layout.addWidget(self.acceleration_label)
        self.second_row_layout.addWidget(self.acceleration_input)
        self.first_row_layout.addWidget(self.axis1_label)
        self.first_row_layout.addWidget(self.x1_input)
        self.first_row_layout.addWidget(self.y1_input)
        self.first_row_layout.addWidget(self.z1_input)
        self.second_row_layout.addWidget(self.axis2_label)
        self.second_row_layout.addWidget(self.x2_input)
        self.second_row_layout.addWidget(self.y2_input)
        self.second_row_layout.addWidget(self.z2_input)
        self.third_row_layout.addWidget(self.reference_label)
        self.third_row_layout.addWidget(self.reference_x_input)
        self.third_row_layout.addWidget(self.reference_y_input)
        self.third_row_layout.addWidget(self.reference_z_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)

        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_cir_motion)
        self._init_connections()

    def fill_values(self, acc_cir_motion):
        """ Fills the widget values with the current data. """
        self.x1_input.setValue(acc_cir_motion.axis1[0])
        self.y1_input.setValue(acc_cir_motion.axis1[1])
        self.z1_input.setValue(acc_cir_motion.axis1[2])
        self.x2_input.setValue(acc_cir_motion.axis2[0])
        self.y2_input.setValue(acc_cir_motion.axis2[1])
        self.z2_input.setValue(acc_cir_motion.axis2[2])
        self.reference_x_input.setValue(acc_cir_motion.reference[0])
        self.reference_y_input.setValue(acc_cir_motion.reference[1])
        self.reference_z_input.setValue(acc_cir_motion.reference[2])
        self.velocity_input.setValue(acc_cir_motion.ang_vel)
        self.acceleration_input.setValue(acc_cir_motion.ang_acc)
        self.time_input.setValue(acc_cir_motion.duration)

    def _init_connections(self):
        """ Setups widget connections with the different functions. """
        self.x1_input.value_changed.connect(self.on_change)
        self.y1_input.value_changed.connect(self.on_change)
        self.z1_input.value_changed.connect(self.on_change)
        self.reference_x_input.value_changed.connect(self.on_change)
        self.reference_y_input.value_changed.connect(self.on_change)
        self.reference_z_input.value_changed.connect(self.on_change)
        self.x2_input.value_changed.connect(self.on_change)
        self.y2_input.value_changed.connect(self.on_change)
        self.z2_input.value_changed.connect(self.on_change)
        self.velocity_input.value_changed.connect(self.on_change)
        self.acceleration_input.value_changed.connect(self.on_change)
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def construct_motion_object(self):
        """ Constructs a AccCirMotion object with the data introduced in the widget. """
        return AccCirMotion(
            ang_vel=self.velocity_input.value(),
            ang_acc=self.acceleration_input.value(),
            reference=[self.reference_x_input.value(),
                       self.reference_y_input.value(),
                       self.reference_z_input.value()],
            axis1=[self.x1_input.value(),
                   self.y1_input.value(),
                   self.z1_input.value()],
            axis2=[self.x2_input.value(),
                   self.y2_input.value(),
                   self.z2_input.value()],
            duration=self.time_input.value())
