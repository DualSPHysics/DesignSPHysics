#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Rectilinear Motion Timeline Widget """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.rect_motion import RectMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class RectilinearMotionTimeline(MotionTimeline):
    """ A Rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RectMotion)
    deleted = QtCore.Signal(int, RectMotion)

    def __init__(self, index, rect_motion, parent=None):
        if not isinstance(rect_motion, RectMotion):
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if rect_motion is None:
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtWidgets.QLabel("Rectilinear \nMotion  ")
        self.label.setMinimumWidth(75)
        self.velocity_label = QtWidgets.QLabel("Vel (X, Y, Z): ")
        self.x_input = VelocityInput(minwidth=80,maxwidth=80)
        self.y_input = VelocityInput(minwidth=80,maxwidth=80)
        self.z_input = VelocityInput(minwidth=80,maxwidth=80)
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
        self.main_layout.addWidget(self.x_input)
        self.main_layout.addWidget(self.y_input)
        self.main_layout.addWidget(self.z_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rect_motion)
        self._init_connections()

    def fill_values(self, rect_motion):
        """ Fills the values from the data structure onto the widget. """
        self.x_input.setValue(rect_motion.velocity[0])
        self.y_input.setValue(rect_motion.velocity[1])
        self.z_input.setValue(rect_motion.velocity[2])
        self.time_input.setValue(rect_motion.duration)

    def _init_connections(self):
        self.x_input.value_changed.connect(self.on_change)
        self.y_input.value_changed.connect(self.on_change)
        self.z_input.value_changed.connect(self.on_change)
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def construct_motion_object(self):
        """ Constructs a new RectMotion object with the current data from the widget. """
        return RectMotion(
            velocity=[self.x_input.value(),
                      self.y_input.value(),
                      self.z_input.value()],
            duration=self.time_input.value())