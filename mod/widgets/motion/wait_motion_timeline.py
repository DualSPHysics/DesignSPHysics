#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Wait Motion Timeline Widget """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.motion.wait_motion import WaitMotion

from mod.functions import make_float


class WaitMotionTimeline(QtGui.QWidget):
    """ A wait motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, WaitMotion)
    deleted = QtCore.Signal(int, WaitMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, wait_motion, parent=None):
        if not isinstance(wait_motion, WaitMotion):
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if wait_motion is None:
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtGui.QLabel("Wait")
        self.label.setMinimumWidth(75)
        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
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
        """ Disables the order up button. """
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        """ Disables the order down button. """
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        """ Reacts to the order up button being pressed. """
        self.order_up.emit(self.index)

    def on_order_down(self):
        """ Reacts to the order down button being pressed. """
        self.order_down.emit(self.index)

    def _fill_values(self, wait_motion):
        self.time_input.setText(str(wait_motion.duration))

    def construct_motion_object(self):
        """ Constructs a new WaitMotion data object from the data currently introduced on the widget. """
        return WaitMotion(duration=make_float(self.time_input.text()))

    def on_change(self):
        """ Reacts to any input change sanitizing it and firing a signal with the appropriate data object. """
        if not self.time_input.text():
            self.time_input.setText("0")
        self.time_input.setText(self.time_input.text().replace(",", "."))
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number")

    def on_delete(self):
        """ Deletes the currently represented data object. """
        self.deleted.emit(self.index, self.construct_motion_object())
