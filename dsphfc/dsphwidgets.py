#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DesignSPHysics Custom GUI implementations.

This file contains a collection of custom GUI implementations
to use with DesignSPHysics.

This module is needed for some specific actions not supported
in QT by default.

"""

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import utils
from utils import __
import guiutils
from properties import *


# Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
#
# This file is part of DesignSPHysics.
#
# DesignSPHysics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DesignSPHysics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.


class MovementActions(QtGui.QWidget):
    """ A set of movement actions (use and delete) with its custom signals"""
    delete = QtCore.Signal(int)
    use = QtCore.Signal(int, bool)
    loop = QtCore.Signal(int, bool)

    def __init__(self, index, use_checked, loop_checked):
        super(MovementActions, self).__init__()
        self.index = index
        self.use_checkbox = QtGui.QCheckBox(__("Use"))
        self.use_checkbox.setChecked(use_checked)
        self.use_checkbox.stateChanged.connect(self.on_use)
        self.loop_checkbox = QtGui.QCheckBox(__("Loop"))
        self.loop_checkbox.setChecked(loop_checked)
        self.loop_checkbox.stateChanged.connect(self.on_loop)
        self.delete_button = QtGui.QPushButton(guiutils.get_icon("trash.png"), None)
        self.delete_button.clicked.connect(self.on_delete)
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QtGui.QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.addWidget(self.use_checkbox)
        main_layout.addWidget(self.loop_checkbox)
        main_layout.addWidget(self.delete_button)
        self.setLayout(main_layout)

    def on_delete(self):
        self.delete.emit(self.index)

    def on_use(self):
        self.use.emit(self.index, self.use_checkbox.isChecked())

    def on_loop(self):
        self.loop.emit(self.index, self.loop_checkbox.isChecked())


class RectilinearMotionTimeline(QtGui.QWidget):
    """ A Rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RectMotion)
    deleted = QtCore.Signal(int, RectMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rect_motion):
        if not isinstance(rect_motion, RectMotion):
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if rect_motion is None:
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super(RectilinearMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rect_motion.parent_movement
        self.label = QtGui.QLabel("Rect  ")
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.x_input = QtGui.QLineEdit()
        self.x_label = QtGui.QLabel("X ")
        self.x_input.setStyleSheet("width: 5px;")
        self.y_input = QtGui.QLineEdit()
        self.y_label = QtGui.QLabel("Y ")
        self.y_input.setStyleSheet("width: 5px;")
        self.z_input = QtGui.QLineEdit()
        self.z_label = QtGui.QLabel("Z")
        self.z_input.setStyleSheet("width: 5px;")
        self.time_icon = QtGui.QPushButton(guiutils.get_icon("clock.png"), None)
        self.time_icon.setEnabled(False)
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(guiutils.get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.velocity_label)
        self.main_layout.addWidget(self.x_input)
        self.main_layout.addWidget(self.x_label)
        self.main_layout.addWidget(self.y_input)
        self.main_layout.addWidget(self.y_label)
        self.main_layout.addWidget(self.z_input)
        self.main_layout.addWidget(self.z_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rect_motion)
        self._init_connections()

    def fill_values(self, rect_motion):
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
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        self.order_up.emit(self.index)

    def on_order_down(self):
        self.order_down.emit(self.index)

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return RectMotion(
            velocity=[float(self.x_input.text()),
                      float(self.y_input.text()),
                      float(self.z_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x_input.text()) is 0:
            self.x_input.setText("0")
        if len(self.y_input.text()) is 0:
            self.y_input.setText("0")
        if len(self.z_input.text()) is 0:
            self.z_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x_input.setText(self.x_input.text().replace(",", "."))
        self.y_input.setText(self.y_input.text().replace(",", "."))
        self.z_input.setText(self.z_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class AccRectilinearMotionTimeline(QtGui.QWidget):
    """ Am accelerated ectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, AccRectMotion)
    deleted = QtCore.Signal(int, AccRectMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, acc_rect_motion):
        if not isinstance(acc_rect_motion, AccRectMotion):
            raise TypeError("You tried to spawn an accelerated rectilinear "
                            "motion widget in the timeline with a wrong object")
        if acc_rect_motion is None:
            raise TypeError("You tried to spawn an accelerated rectilinear "
                            "motion widget in the timeline without a motion object")
        super(AccRectilinearMotionTimeline, self).__init__()
        self.index = index
        self.setMinimumHeight(50)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = acc_rect_motion.parent_movement
        self.label = QtGui.QLabel("ARect  ")
        self.data_layout = QtGui.QVBoxLayout()
        self.data_layout.setContentsMargins(0, 0, 0, 0)
        self.data_velocity_layout = QtGui.QHBoxLayout()
        self.data_velocity_layout.setContentsMargins(0, 0, 0, 0)
        self.data_acceleration_layout = QtGui.QHBoxLayout()
        self.data_acceleration_layout.setContentsMargins(0, 0, 0, 0)

        self.velocity_label = QtGui.QLabel("Vel: ")
        self.x_input = QtGui.QLineEdit()
        self.x_label = QtGui.QLabel("X ")
        self.x_input.setStyleSheet("width: 5px;")
        self.y_input = QtGui.QLineEdit()
        self.y_label = QtGui.QLabel("Y ")
        self.y_input.setStyleSheet("width: 5px;")
        self.z_input = QtGui.QLineEdit()
        self.z_label = QtGui.QLabel("Z")
        self.z_input.setStyleSheet("width: 5px;")

        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.xa_input = QtGui.QLineEdit()
        self.xa_label = QtGui.QLabel("X ")
        self.xa_input.setStyleSheet("width: 5px;")
        self.ya_input = QtGui.QLineEdit()
        self.ya_label = QtGui.QLabel("Y ")
        self.ya_input.setStyleSheet("width: 5px;")
        self.za_input = QtGui.QLineEdit()
        self.za_label = QtGui.QLabel("Z")
        self.za_input.setStyleSheet("width: 5px;")

        [self.data_velocity_layout.addWidget(x) for x in [
            self.velocity_label,
            self.x_input, self.x_label,
            self.y_input, self.y_label,
            self.z_input, self.z_label,
        ]]
        [self.data_acceleration_layout.addWidget(x) for x in [
            self.acceleration_label,
            self.xa_input, self.xa_label,
            self.ya_input, self.ya_label,
            self.za_input, self.za_label,
        ]]

        self.data_layout.addLayout(self.data_velocity_layout)
        self.data_layout.addLayout(self.data_acceleration_layout)

        self.time_icon = QtGui.QPushButton(guiutils.get_icon("clock.png"), None)
        self.time_icon.setEnabled(False)
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(guiutils.get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_rect_motion)
        self._init_connections()

    def fill_values(self, acc_rect_motion):
        self.x_input.setText(str(acc_rect_motion.velocity[0]))
        self.y_input.setText(str(acc_rect_motion.velocity[1]))
        self.z_input.setText(str(acc_rect_motion.velocity[2]))
        self.xa_input.setText(str(acc_rect_motion.acceleration[0]))
        self.ya_input.setText(str(acc_rect_motion.acceleration[1]))
        self.za_input.setText(str(acc_rect_motion.acceleration[2]))
        self.time_input.setText(str(acc_rect_motion.duration))

    def _init_connections(self):
        self.x_input.textChanged.connect(self.on_change)
        self.y_input.textChanged.connect(self.on_change)
        self.z_input.textChanged.connect(self.on_change)
        self.xa_input.textChanged.connect(self.on_change)
        self.ya_input.textChanged.connect(self.on_change)
        self.za_input.textChanged.connect(self.on_change)
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

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return AccRectMotion(
            velocity=[float(self.x_input.text()),
                      float(self.y_input.text()),
                      float(self.z_input.text())],
            acceleration=[float(self.xa_input.text()),
                          float(self.ya_input.text()),
                          float(self.za_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x_input.text()) is 0:
            self.x_input.setText("0")
        if len(self.y_input.text()) is 0:
            self.y_input.setText("0")
        if len(self.z_input.text()) is 0:
            self.z_input.setText("0")
        if len(self.xa_input.text()) is 0:
            self.xa_input.setText("0")
        if len(self.ya_input.text()) is 0:
            self.ya_input.setText("0")
        if len(self.za_input.text()) is 0:
            self.za_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x_input.setText(self.x_input.text().replace(",", "."))
        self.y_input.setText(self.y_input.text().replace(",", "."))
        self.z_input.setText(self.z_input.text().replace(",", "."))
        self.xa_input.setText(self.xa_input.text().replace(",", "."))
        self.ya_input.setText(self.ya_input.text().replace(",", "."))
        self.za_input.setText(self.za_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class WaitMotionTimeline(QtGui.QWidget):
    """ A wait motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, WaitMotion)
    deleted = QtCore.Signal(int, WaitMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, wait_motion):
        if not isinstance(wait_motion, WaitMotion):
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if wait_motion is None:
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline without a motion object")

        super(WaitMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = wait_motion.parent_movement
        self.label = QtGui.QLabel("Wait")
        self.time_icon = QtGui.QPushButton(guiutils.get_icon("clock.png"), None)
        self.time_icon.setEnabled(False)
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(guiutils.get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
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
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")
        self.time_input.setText(self.time_input.text().replace(",", "."))
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number")

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())
