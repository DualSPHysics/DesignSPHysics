#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Rectilinear Motion Timeline Widget """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.motion.rect_motion import RectMotion

from mod.functions import make_float

class RectilinearMotionTimeline(QtGui.QWidget):
    """ A Rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RectMotion)
    deleted = QtCore.Signal(int, RectMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rect_motion, parent=None):
        if not isinstance(rect_motion, RectMotion):
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if rect_motion is None:
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index

        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtGui.QLabel("Rectilinear \nMotion  ")
        self.label.setMinimumWidth(75)
        self.velocity_label = QtGui.QLabel("Vel (X, Y, Z): ")
        self.x_input = QtGui.QLineEdit()
        self.y_input = QtGui.QLineEdit()
        self.z_input = QtGui.QLineEdit()
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
        self.x_input.setText(str(rect_motion.velocity[0]))
        self.y_input.setText(str(rect_motion.velocity[1]))
        self.z_input.setText(str(rect_motion.velocity[2]))
        self.time_input.setText(str(rect_motion.duration))

    def _init_connections(self):
        self.x_input.textChanged.connect(self.on_change)
        self.y_input.textChanged.connect(self.on_change)
        self.z_input.textChanged.connect(self.on_change)
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

    def on_change(self):
        """ Reacts to any input sanitizing it and firing a signal with the appropriate data object. """
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs a new RectMotion object with the current data from the widget. """
        return RectMotion(
            velocity=[make_float(self.x_input.text()),
                      make_float(self.y_input.text()),
                      make_float(self.z_input.text())],
            duration=make_float(self.time_input.text()))

    def on_delete(self):
        """ Deletes the currently represented motion object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if not self.x_input.text():
            self.x_input.setText("0")
        if not self.y_input.text():
            self.y_input.setText("0")
        if not self.z_input.text():
            self.z_input.setText("0")
        if not self.time_input.text():
            self.time_input.setText("0")

        self.x_input.setText(self.x_input.text().replace(",", "."))
        self.y_input.setText(self.y_input.text().replace(",", "."))
        self.z_input.setText(self.z_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))
