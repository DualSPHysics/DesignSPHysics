#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Wait Motion Timeline Widget '''

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.guiutils import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.wait_motion import WaitMotion


class WaitMotionTimeline(QtGui.QWidget):
    ''' A wait motion graphical representation for a table-based timeline '''

    changed = QtCore.Signal(int, WaitMotion)
    deleted = QtCore.Signal(int, WaitMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, wait_motion):
        if not isinstance(wait_motion, WaitMotion):
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if wait_motion is None:
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline without a motion object")

        super(WaitMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = wait_motion.parent_movement
        self.label = QtGui.QLabel("Wait")
        self.label.setMinimumWidth(75)
        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
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
        self.time_input.textChanged.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def disable_order_up_button(self):
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        self.order_up.emit(self.index)

    def on_order_down(self):
        self.order_down.emit(self.index)

    def _fill_values(self, wait_motion):
        self.time_input.setText(str(wait_motion.duration))

    def construct_motion_object(self):
        return WaitMotion(duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_change(self):
        if not self.time_input.text():
            self.time_input.setText("0")
        self.time_input.setText(self.time_input.text().replace(",", "."))
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number")

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())
