#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Wait Motion Timeline Widget """

from PySide2 import QtCore, QtWidgets
from mod.dataobjects.motion.wait_motion import WaitMotion
from mod.tools.gui_tools import get_icon
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.properties_widgets.motion.motion_timeline import MotionTimeline


class WaitMotionTimeline(MotionTimeline):
    """ A wait motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, WaitMotion)
    deleted = QtCore.Signal(int, WaitMotion)

    def __init__(self, index, wait_motion, parent=None):

        if not isinstance(wait_motion, WaitMotion):
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if wait_motion is None:
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtWidgets.QLabel("Wait")
        self.label.setMinimumWidth(75)
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
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self._fill_values(wait_motion)
        self._init_connections()

    def _init_connections(self):
        self.time_input.value_changed.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)


    def _fill_values(self, wait_motion):
        self.time_input.setValue(wait_motion.duration)

    def construct_motion_object(self):
        """ Constructs a new WaitMotion data object from the data currently introduced on the widget. """
        return WaitMotion(duration=self.time_input.value())
