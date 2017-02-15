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


class WaveMovementActions(QtGui.QWidget):
    """ A set of wave movement actions (use and delete) with its custom signals"""
    delete = QtCore.Signal(int)
    use = QtCore.Signal(int, bool)

    def __init__(self, index, use_checked):
        super(WaveMovementActions, self).__init__()
        self.index = index
        self.use_checkbox = QtGui.QCheckBox(__("Use"))
        self.use_checkbox.setChecked(use_checked)
        self.use_checkbox.stateChanged.connect(self.on_use)
        self.delete_button = QtGui.QPushButton(guiutils.get_icon("trash.png"), None)
        self.delete_button.clicked.connect(self.on_delete)
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QtGui.QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.addWidget(self.use_checkbox)
        main_layout.addWidget(self.delete_button)
        self.setLayout(main_layout)

    def on_delete(self):
        self.delete.emit(self.index)

    def on_use(self):
        self.use.emit(self.index, self.use_checkbox.isChecked())


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
        self.label = QtGui.QLabel("ARect ")
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


class RotationalMotionTimeline(QtGui.QWidget):
    """ A Rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RotMotion)
    deleted = QtCore.Signal(int, RotMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rot_motion):
        if not isinstance(rot_motion, RotMotion):
            raise TypeError("You tried to spawn a rotational motion widget in the timeline with a wrong object")
        if rot_motion is None:
            raise TypeError("You tried to spawn a rotational motion widget in the timeline without a motion object")
        super(RotationalMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rot_motion.parent_movement
        self.label = QtGui.QLabel("Rot  ")
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel("Axis: ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_label = QtGui.QLabel("X ")
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_label = QtGui.QLabel("Y ")
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_label = QtGui.QLabel("Z")
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_label = QtGui.QLabel("X ")
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_label = QtGui.QLabel("Y ")
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_label = QtGui.QLabel("Z")
        self.z2_input.setStyleSheet("width: 5px;")
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
        self.main_layout.addWidget(self.velocity_input)
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.x1_label)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.y1_label)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_first_row_layout.addWidget(self.z1_label)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.x2_label)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.y2_label)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_second_row_layout.addWidget(self.z2_label)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rot_motion)
        self._init_connections()

    def fill_values(self, rot_motion):
        self.x1_input.setText(str(rot_motion.axis1[0]))
        self.y1_input.setText(str(rot_motion.axis1[1]))
        self.z1_input.setText(str(rot_motion.axis1[2]))
        self.x2_input.setText(str(rot_motion.axis2[0]))
        self.y2_input.setText(str(rot_motion.axis2[1]))
        self.z2_input.setText(str(rot_motion.axis2[2]))
        self.velocity_input.setText(str(rot_motion.ang_vel))
        self.time_input.setText(str(rot_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.velocity_input.textChanged.connect(self.on_change)
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
        return RotMotion(
            ang_vel=float(self.velocity_input.text()),
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x1_input.text()) is 0:
            self.x1_input.setText("0")
        if len(self.y1_input.text()) is 0:
            self.y1_input.setText("0")
        if len(self.z1_input.text()) is 0:
            self.z1_input.setText("0")
        if len(self.x2_input.text()) is 0:
            self.x2_input.setText("0")
        if len(self.y2_input.text()) is 0:
            self.y2_input.setText("0")
        if len(self.z2_input.text()) is 0:
            self.z2_input.setText("0")
        if len(self.velocity_input.text()) is 0:
            self.velocity_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.velocity_input.setText(self.velocity_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class AccRotationalMotionTimeline(QtGui.QWidget):
    """ An accelerated rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, AccRotMotion)
    deleted = QtCore.Signal(int, AccRotMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, acc_rot_motion):
        if not isinstance(acc_rot_motion, AccRotMotion):
            raise TypeError("You tried to spawn an accelerated rotational "
                            "motion widget in the timeline with a wrong object")
        if acc_rot_motion is None:
            raise TypeError("You tried to spawn an accelerated rotational "
                            "motion widget in the timeline without a motion object")
        super(AccRotationalMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = acc_rot_motion.parent_movement
        self.label = QtGui.QLabel("ARot ")
        self.vel_and_acc_layout = QtGui.QVBoxLayout()
        self.vel_layout = QtGui.QHBoxLayout()
        self.acc_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.acceleration_input = QtGui.QLineEdit()
        self.acceleration_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel("Axis: ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_label = QtGui.QLabel("X ")
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_label = QtGui.QLabel("Y ")
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_label = QtGui.QLabel("Z")
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_label = QtGui.QLabel("X ")
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_label = QtGui.QLabel("Y ")
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_label = QtGui.QLabel("Z")
        self.z2_input.setStyleSheet("width: 5px;")
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

        self.vel_layout.addWidget(self.velocity_label)
        self.vel_layout.addWidget(self.velocity_input)
        self.acc_layout.addWidget(self.acceleration_label)
        self.acc_layout.addWidget(self.acceleration_input)
        self.vel_and_acc_layout.addLayout(self.vel_layout)
        self.vel_and_acc_layout.addLayout(self.acc_layout)
        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.vel_and_acc_layout)
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.x1_label)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.y1_label)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_first_row_layout.addWidget(self.z1_label)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.x2_label)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.y2_label)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_second_row_layout.addWidget(self.z2_label)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_rot_motion)
        self._init_connections()

    def fill_values(self, acc_rot_motion):
        self.x1_input.setText(str(acc_rot_motion.axis1[0]))
        self.y1_input.setText(str(acc_rot_motion.axis1[1]))
        self.z1_input.setText(str(acc_rot_motion.axis1[2]))
        self.x2_input.setText(str(acc_rot_motion.axis2[0]))
        self.y2_input.setText(str(acc_rot_motion.axis2[1]))
        self.z2_input.setText(str(acc_rot_motion.axis2[2]))
        self.velocity_input.setText(str(acc_rot_motion.ang_vel))
        self.acceleration_input.setText(str(acc_rot_motion.ang_acc))
        self.time_input.setText(str(acc_rot_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.velocity_input.textChanged.connect(self.on_change)
        self.acceleration_input.textChanged.connect(self.on_change)
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
        return AccRotMotion(
            ang_vel=float(self.velocity_input.text()),
            ang_acc=float(self.acceleration_input.text()),
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x1_input.text()) is 0:
            self.x1_input.setText("0")
        if len(self.y1_input.text()) is 0:
            self.y1_input.setText("0")
        if len(self.z1_input.text()) is 0:
            self.z1_input.setText("0")
        if len(self.x2_input.text()) is 0:
            self.x2_input.setText("0")
        if len(self.y2_input.text()) is 0:
            self.y2_input.setText("0")
        if len(self.z2_input.text()) is 0:
            self.z2_input.setText("0")
        if len(self.velocity_input.text()) is 0:
            self.velocity_input.setText("0")
        if len(self.acceleration_input.text()) is 0:
            self.acceleration_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.velocity_input.setText(self.velocity_input.text().replace(",", "."))
        self.acceleration_input.setText(self.acceleration_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class AccCircularMotionTimeline(QtGui.QWidget):
    """ An accelerated circular motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, AccCirMotion)
    deleted = QtCore.Signal(int, AccCirMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, acc_cir_motion):
        if not isinstance(acc_cir_motion, AccCirMotion):
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline with a wrong object")
        if acc_cir_motion is None:
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline without a motion object")
        super(AccCircularMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = acc_cir_motion.parent_movement
        self.label = QtGui.QLabel("ACir ")
        self.vel_and_acc_layout = QtGui.QVBoxLayout()
        self.vel_layout = QtGui.QHBoxLayout()
        self.acc_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.acceleration_input = QtGui.QLineEdit()
        self.acceleration_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel("Axis: ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_label = QtGui.QLabel("X ")
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_label = QtGui.QLabel("Y ")
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_label = QtGui.QLabel("Z")
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_label = QtGui.QLabel("X ")
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_label = QtGui.QLabel("Y ")
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_label = QtGui.QLabel("Z")
        self.z2_input.setStyleSheet("width: 5px;")

        self.reference_label = QtGui.QLabel("Ref ")
        self.reference_x_input = QtGui.QLineEdit()
        self.reference_x_input.setStyleSheet("width: 5px;")
        self.reference_x_label = QtGui.QLabel("X ")
        self.reference_y_input = QtGui.QLineEdit()
        self.reference_y_input.setStyleSheet("width: 5px;")
        self.reference_y_label = QtGui.QLabel("Y ")
        self.reference_z_input = QtGui.QLineEdit()
        self.reference_z_input.setStyleSheet("width: 5px;")
        self.reference_z_label = QtGui.QLabel("Z")

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

        self.vel_layout.addWidget(self.velocity_label)
        self.vel_layout.addWidget(self.velocity_input)
        self.acc_layout.addWidget(self.acceleration_label)
        self.acc_layout.addWidget(self.acceleration_input)
        self.vel_and_acc_layout.addLayout(self.vel_layout)
        self.vel_and_acc_layout.addLayout(self.acc_layout)
        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.vel_and_acc_layout)
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.x1_label)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.y1_label)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_first_row_layout.addWidget(self.z1_label)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.x2_label)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.y2_label)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_second_row_layout.addWidget(self.z2_label)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addWidget(self.reference_label)
        self.main_layout.addWidget(self.reference_x_input)
        self.main_layout.addWidget(self.reference_x_label)
        self.main_layout.addWidget(self.reference_y_input)
        self.main_layout.addWidget(self.reference_y_label)
        self.main_layout.addWidget(self.reference_z_input)
        self.main_layout.addWidget(self.reference_z_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_cir_motion)
        self._init_connections()

    def fill_values(self, acc_cir_motion):
        self.x1_input.setText(str(acc_cir_motion.axis1[0]))
        self.y1_input.setText(str(acc_cir_motion.axis1[1]))
        self.z1_input.setText(str(acc_cir_motion.axis1[2]))
        self.x2_input.setText(str(acc_cir_motion.axis2[0]))
        self.y2_input.setText(str(acc_cir_motion.axis2[1]))
        self.z2_input.setText(str(acc_cir_motion.axis2[2]))
        self.reference_x_input.setText(str(acc_cir_motion.reference[0]))
        self.reference_y_input.setText(str(acc_cir_motion.reference[1]))
        self.reference_z_input.setText(str(acc_cir_motion.reference[2]))
        self.velocity_input.setText(str(acc_cir_motion.ang_vel))
        self.acceleration_input.setText(str(acc_cir_motion.ang_acc))
        self.time_input.setText(str(acc_cir_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.reference_x_input.textChanged.connect(self.on_change)
        self.reference_y_input.textChanged.connect(self.on_change)
        self.reference_z_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.velocity_input.textChanged.connect(self.on_change)
        self.acceleration_input.textChanged.connect(self.on_change)
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
        return AccCirMotion(
            ang_vel=float(self.velocity_input.text()),
            ang_acc=float(self.acceleration_input.text()),
            reference=[float(self.reference_x_input.text()),
                       float(self.reference_y_input.text()),
                       float(self.reference_z_input.text())],
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x1_input.text()) is 0:
            self.x1_input.setText("0")
        if len(self.y1_input.text()) is 0:
            self.y1_input.setText("0")
        if len(self.z1_input.text()) is 0:
            self.z1_input.setText("0")
        if len(self.x2_input.text()) is 0:
            self.x2_input.setText("0")
        if len(self.y2_input.text()) is 0:
            self.y2_input.setText("0")
        if len(self.z2_input.text()) is 0:
            self.z2_input.setText("0")
        if len(self.reference_x_input.text()) is 0:
            self.reference_x_input.setText("0")
        if len(self.reference_y_input.text()) is 0:
            self.reference_y_input.setText("0")
        if len(self.reference_z_input.text()) is 0:
            self.reference_z_input.setText("0")
        if len(self.velocity_input.text()) is 0:
            self.velocity_input.setText("0")
        if len(self.acceleration_input.text()) is 0:
            self.acceleration_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.reference_x_input.setText(self.reference_x_input.text().replace(",", "."))
        self.reference_y_input.setText(self.reference_y_input.text().replace(",", "."))
        self.reference_z_input.setText(self.reference_z_input.text().replace(",", "."))
        self.velocity_input.setText(self.velocity_input.text().replace(",", "."))
        self.acceleration_input.setText(self.acceleration_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class RotSinuMotionTimeline(QtGui.QWidget):
    """ An sinusoidal rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RotSinuMotion)
    deleted = QtCore.Signal(int, RotSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rot_sinu_motion):
        if not isinstance(rot_sinu_motion, RotSinuMotion):
            raise TypeError("You tried to spawn an sinusoidal rotational "
                            "motion widget in the timeline with a wrong object")
        if rot_sinu_motion is None:
            raise TypeError("You tried to spawn an sinusoidal rotational "
                            "motion widget in the timeline without a motion object")
        super(RotSinuMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rot_sinu_motion.parent_movement
        self.label = QtGui.QLabel("SRot ")
        self.axis_label = QtGui.QLabel("Axis: ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_label = QtGui.QLabel("X ")
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_label = QtGui.QLabel("Y ")
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_label = QtGui.QLabel("Z")
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_label = QtGui.QLabel("X ")
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_label = QtGui.QLabel("Y ")
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_label = QtGui.QLabel("Z")
        self.z2_input.setStyleSheet("width: 5px;")

        self.freq_label = QtGui.QLabel("Freq ")
        self.freq_input = QtGui.QLineEdit()
        self.freq_input.setStyleSheet("width: 5px;")

        self.ampl_label = QtGui.QLabel("Ampl ")
        self.ampl_input = QtGui.QLineEdit()
        self.ampl_input.setStyleSheet("width: 5px;")

        self.phase_label = QtGui.QLabel("Phase ")
        self.phase_input = QtGui.QLineEdit()
        self.phase_input.setStyleSheet("width: 5px;")

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
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.x1_label)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.y1_label)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_first_row_layout.addWidget(self.z1_label)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.x2_label)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.y2_label)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_second_row_layout.addWidget(self.z2_label)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addWidget(self.freq_label)
        self.main_layout.addWidget(self.freq_input)
        self.main_layout.addWidget(self.ampl_label)
        self.main_layout.addWidget(self.ampl_input)
        self.main_layout.addWidget(self.phase_label)
        self.main_layout.addWidget(self.phase_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rot_sinu_motion)
        self._init_connections()

    def fill_values(self, rot_sinu_motion):
        self.x1_input.setText(str(rot_sinu_motion.axis1[0]))
        self.y1_input.setText(str(rot_sinu_motion.axis1[1]))
        self.z1_input.setText(str(rot_sinu_motion.axis1[2]))
        self.x2_input.setText(str(rot_sinu_motion.axis2[0]))
        self.y2_input.setText(str(rot_sinu_motion.axis2[1]))
        self.z2_input.setText(str(rot_sinu_motion.axis2[2]))
        self.freq_input.setText(str(rot_sinu_motion.freq))
        self.ampl_input.setText(str(rot_sinu_motion.ampl))
        self.phase_input.setText(str(rot_sinu_motion.phase))
        self.time_input.setText(str(rot_sinu_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.freq_input.textChanged.connect(self.on_change)
        self.ampl_input.textChanged.connect(self.on_change)
        self.phase_input.textChanged.connect(self.on_change)
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
        return RotSinuMotion(
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            duration=float(self.time_input.text()), freq=float(self.freq_input.text()),
            ampl=float(self.ampl_input.text()), phase=float(self.phase_input.text()),
            parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x1_input.text()) is 0:
            self.x1_input.setText("0")
        if len(self.y1_input.text()) is 0:
            self.y1_input.setText("0")
        if len(self.z1_input.text()) is 0:
            self.z1_input.setText("0")
        if len(self.x2_input.text()) is 0:
            self.x2_input.setText("0")
        if len(self.y2_input.text()) is 0:
            self.y2_input.setText("0")
        if len(self.z2_input.text()) is 0:
            self.z2_input.setText("0")
        if len(self.freq_input.text()) is 0:
            self.freq_input.setText("0")
        if len(self.ampl_input.text()) is 0:
            self.ampl_input.setText("0")
        if len(self.phase_input.text()) is 0:
            self.phase_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.freq_input.setText(self.freq_input.text().replace(",", "."))
        self.ampl_input.setText(self.ampl_input.text().replace(",", "."))
        self.phase_input.setText(self.phase_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class CirSinuMotionTimeline(QtGui.QWidget):
    """ An sinusoidal circular motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, CirSinuMotion)
    deleted = QtCore.Signal(int, CirSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, cir_sinu_motion):
        if not isinstance(cir_sinu_motion, CirSinuMotion):
            raise TypeError("You tried to spawn an sinusoidal circular "
                            "motion widget in the timeline with a wrong object")
        if cir_sinu_motion is None:
            raise TypeError("You tried to spawn an sinusoidal circular "
                            "motion widget in the timeline without a motion object")
        super(CirSinuMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = cir_sinu_motion.parent_movement
        self.label = QtGui.QLabel("SCir ")
        self.axis_label = QtGui.QLabel("Axis: ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_label = QtGui.QLabel("X ")
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_label = QtGui.QLabel("Y ")
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_label = QtGui.QLabel("Z")
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_label = QtGui.QLabel("X ")
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_label = QtGui.QLabel("Y ")
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_label = QtGui.QLabel("Z")
        self.z2_input.setStyleSheet("width: 5px;")

        self.ref_layout = QtGui.QVBoxLayout()
        self.ref_first_row = QtGui.QHBoxLayout()
        self.ref_second_row = QtGui.QHBoxLayout()
        self.freq_label = QtGui.QLabel("Freq ")
        self.freq_input = QtGui.QLineEdit()
        self.freq_input.setStyleSheet("width: 5px;")

        self.ampl_label = QtGui.QLabel("Ampl ")
        self.ampl_input = QtGui.QLineEdit()
        self.ampl_input.setStyleSheet("width: 5px;")

        self.phase_label = QtGui.QLabel("Phase ")
        self.phase_input = QtGui.QLineEdit()
        self.phase_input.setStyleSheet("width: 5px;")

        self.reference_label = QtGui.QLabel("Ref ")
        self.reference_x_input = QtGui.QLineEdit()
        self.reference_x_input.setStyleSheet("width: 5px;")
        self.reference_x_label = QtGui.QLabel("X ")
        self.reference_y_input = QtGui.QLineEdit()
        self.reference_y_input.setStyleSheet("width: 5px;")
        self.reference_y_label = QtGui.QLabel("Y ")
        self.reference_z_input = QtGui.QLineEdit()
        self.reference_z_input.setStyleSheet("width: 5px;")
        self.reference_z_label = QtGui.QLabel("Z")

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
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.x1_label)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.y1_label)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_first_row_layout.addWidget(self.z1_label)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.x2_label)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.y2_label)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_second_row_layout.addWidget(self.z2_label)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)

        self.ref_first_row.addWidget(self.freq_label)
        self.ref_first_row.addWidget(self.freq_input)
        self.ref_first_row.addWidget(self.ampl_label)
        self.ref_first_row.addWidget(self.ampl_input)
        self.ref_first_row.addWidget(self.phase_label)
        self.ref_first_row.addWidget(self.phase_input)

        self.ref_second_row.addWidget(self.reference_label)
        self.ref_second_row.addWidget(self.reference_x_input)
        self.ref_second_row.addWidget(self.reference_x_label)
        self.ref_second_row.addWidget(self.reference_y_input)
        self.ref_second_row.addWidget(self.reference_y_label)
        self.ref_second_row.addWidget(self.reference_z_input)
        self.ref_second_row.addWidget(self.reference_z_label)

        self.ref_layout.addLayout(self.ref_first_row)
        self.ref_layout.addLayout(self.ref_second_row)

        self.main_layout.addLayout(self.ref_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(cir_sinu_motion)
        self._init_connections()

    def fill_values(self, cir_sinu_motion):
        self.x1_input.setText(str(cir_sinu_motion.axis1[0]))
        self.y1_input.setText(str(cir_sinu_motion.axis1[1]))
        self.z1_input.setText(str(cir_sinu_motion.axis1[2]))
        self.x2_input.setText(str(cir_sinu_motion.axis2[0]))
        self.y2_input.setText(str(cir_sinu_motion.axis2[1]))
        self.z2_input.setText(str(cir_sinu_motion.axis2[2]))
        self.reference_x_input.setText(str(cir_sinu_motion.reference[0]))
        self.reference_y_input.setText(str(cir_sinu_motion.reference[1]))
        self.reference_z_input.setText(str(cir_sinu_motion.reference[2]))
        self.freq_input.setText(str(cir_sinu_motion.freq))
        self.ampl_input.setText(str(cir_sinu_motion.ampl))
        self.phase_input.setText(str(cir_sinu_motion.phase))
        self.time_input.setText(str(cir_sinu_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.reference_x_input.textChanged.connect(self.on_change)
        self.reference_y_input.textChanged.connect(self.on_change)
        self.reference_z_input.textChanged.connect(self.on_change)
        self.freq_input.textChanged.connect(self.on_change)
        self.ampl_input.textChanged.connect(self.on_change)
        self.phase_input.textChanged.connect(self.on_change)
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
        return CirSinuMotion(
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            reference=[float(self.reference_x_input.text()),
                       float(self.reference_y_input.text()),
                       float(self.reference_z_input.text())],
            duration=float(self.time_input.text()), freq=float(self.freq_input.text()),
            ampl=float(self.ampl_input.text()), phase=float(self.phase_input.text()),
            parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.x1_input.text()) is 0:
            self.x1_input.setText("0")
        if len(self.y1_input.text()) is 0:
            self.y1_input.setText("0")
        if len(self.z1_input.text()) is 0:
            self.z1_input.setText("0")
        if len(self.x2_input.text()) is 0:
            self.x2_input.setText("0")
        if len(self.y2_input.text()) is 0:
            self.y2_input.setText("0")
        if len(self.z2_input.text()) is 0:
            self.z2_input.setText("0")
        if len(self.reference_x_input.text()) is 0:
            self.reference_x_input.setText("0")
        if len(self.reference_y_input.text()) is 0:
            self.reference_y_input.setText("0")
        if len(self.reference_z_input.text()) is 0:
            self.reference_z_input.setText("0")
        if len(self.freq_input.text()) is 0:
            self.freq_input.setText("0")
        if len(self.ampl_input.text()) is 0:
            self.ampl_input.setText("0")
        if len(self.phase_input.text()) is 0:
            self.phase_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.reference_x_input.setText(self.reference_x_input.text().replace(",", "."))
        self.reference_y_input.setText(self.reference_y_input.text().replace(",", "."))
        self.reference_z_input.setText(self.reference_z_input.text().replace(",", "."))
        self.freq_input.setText(self.freq_input.text().replace(",", "."))
        self.ampl_input.setText(self.ampl_input.text().replace(",", "."))
        self.phase_input.setText(self.phase_input.text().replace(",", "."))
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


class RectSinuMotionTimeline(QtGui.QWidget):
    """ An sinusoidal rectilinear motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RectSinuMotion)
    deleted = QtCore.Signal(int, RectSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rect_sinu_motion):
        if not isinstance(rect_sinu_motion, RectSinuMotion):
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline with a wrong object")
        if rect_sinu_motion is None:
            raise TypeError("You tried to spawn an accelerated circular "
                            "motion widget in the timeline without a motion object")
        super(RectSinuMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rect_sinu_motion.parent_movement
        self.label = QtGui.QLabel("SRect ")
        self.freq_amp_layout = QtGui.QVBoxLayout()
        self.freq_amp_first_row_layout = QtGui.QHBoxLayout()
        self.freq_amp_second_row_layout = QtGui.QHBoxLayout()
        self.freq_label = QtGui.QLabel("Freq: ")
        self.amp_label = QtGui.QLabel("Amp: ")
        self.freq_x_input = QtGui.QLineEdit()
        self.freq_x_label = QtGui.QLabel("X ")
        self.freq_x_input.setStyleSheet("width: 5px;")
        self.freq_y_input = QtGui.QLineEdit()
        self.freq_y_label = QtGui.QLabel("Y ")
        self.freq_y_input.setStyleSheet("width: 5px;")
        self.freq_z_input = QtGui.QLineEdit()
        self.freq_z_label = QtGui.QLabel("Z")
        self.freq_z_input.setStyleSheet("width: 5px;")
        self.amp_x_input = QtGui.QLineEdit()
        self.amp_x_label = QtGui.QLabel("X ")
        self.amp_x_input.setStyleSheet("width: 5px;")
        self.amp_y_input = QtGui.QLineEdit()
        self.amp_y_label = QtGui.QLabel("Y ")
        self.amp_y_input.setStyleSheet("width: 5px;")
        self.amp_z_input = QtGui.QLineEdit()
        self.amp_z_label = QtGui.QLabel("Z")
        self.amp_z_input.setStyleSheet("width: 5px;")

        self.phase_label = QtGui.QLabel("Phase ")
        self.phase_x_input = QtGui.QLineEdit()
        self.phase_x_input.setStyleSheet("width: 5px;")
        self.phase_x_label = QtGui.QLabel("X ")
        self.phase_y_input = QtGui.QLineEdit()
        self.phase_y_input.setStyleSheet("width: 5px;")
        self.phase_y_label = QtGui.QLabel("Y ")
        self.phase_z_input = QtGui.QLineEdit()
        self.phase_z_input.setStyleSheet("width: 5px;")
        self.phase_z_label = QtGui.QLabel("Z")

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
        self.main_layout.addWidget(self.freq_label)
        self.freq_amp_first_row_layout.addWidget(self.freq_x_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_x_label)
        self.freq_amp_first_row_layout.addWidget(self.freq_y_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_y_label)
        self.freq_amp_first_row_layout.addWidget(self.freq_z_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_z_label)
        self.freq_amp_second_row_layout.addWidget(self.amp_x_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_x_label)
        self.freq_amp_second_row_layout.addWidget(self.amp_y_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_y_label)
        self.freq_amp_second_row_layout.addWidget(self.amp_z_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_z_label)
        self.freq_amp_layout.addLayout(self.freq_amp_first_row_layout)
        self.freq_amp_layout.addLayout(self.freq_amp_second_row_layout)
        self.main_layout.addLayout(self.freq_amp_layout)
        self.main_layout.addWidget(self.phase_label)
        self.main_layout.addWidget(self.phase_x_input)
        self.main_layout.addWidget(self.phase_x_label)
        self.main_layout.addWidget(self.phase_y_input)
        self.main_layout.addWidget(self.phase_y_label)
        self.main_layout.addWidget(self.phase_z_input)
        self.main_layout.addWidget(self.phase_z_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(rect_sinu_motion)
        self._init_connections()

    def fill_values(self, rect_sinu_motion):
        self.freq_x_input.setText(str(rect_sinu_motion.freq[0]))
        self.freq_y_input.setText(str(rect_sinu_motion.freq[1]))
        self.freq_z_input.setText(str(rect_sinu_motion.freq[2]))
        self.amp_x_input.setText(str(rect_sinu_motion.ampl[0]))
        self.amp_y_input.setText(str(rect_sinu_motion.ampl[1]))
        self.amp_z_input.setText(str(rect_sinu_motion.ampl[2]))
        self.phase_x_input.setText(str(rect_sinu_motion.phase[0]))
        self.phase_y_input.setText(str(rect_sinu_motion.phase[1]))
        self.phase_z_input.setText(str(rect_sinu_motion.phase[2]))
        self.time_input.setText(str(rect_sinu_motion.duration))

    def _init_connections(self):
        self.freq_x_input.textChanged.connect(self.on_change)
        self.freq_y_input.textChanged.connect(self.on_change)
        self.freq_z_input.textChanged.connect(self.on_change)
        self.phase_x_input.textChanged.connect(self.on_change)
        self.phase_y_input.textChanged.connect(self.on_change)
        self.phase_z_input.textChanged.connect(self.on_change)
        self.amp_x_input.textChanged.connect(self.on_change)
        self.amp_y_input.textChanged.connect(self.on_change)
        self.amp_z_input.textChanged.connect(self.on_change)
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
        return RectSinuMotion(
            phase=[float(self.phase_x_input.text()),
                   float(self.phase_y_input.text()),
                   float(self.phase_z_input.text())],
            freq=[float(self.freq_x_input.text()),
                  float(self.freq_y_input.text()),
                  float(self.freq_z_input.text())],
            ampl=[float(self.amp_x_input.text()),
                  float(self.amp_y_input.text()),
                  float(self.amp_z_input.text())],
            duration=float(self.time_input.text()), parent_movement=self.parent_movement)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if len(self.freq_x_input.text()) is 0:
            self.freq_x_input.setText("0")
        if len(self.freq_y_input.text()) is 0:
            self.freq_y_input.setText("0")
        if len(self.freq_z_input.text()) is 0:
            self.freq_z_input.setText("0")
        if len(self.amp_x_input.text()) is 0:
            self.amp_x_input.setText("0")
        if len(self.amp_y_input.text()) is 0:
            self.amp_y_input.setText("0")
        if len(self.amp_z_input.text()) is 0:
            self.amp_z_input.setText("0")
        if len(self.phase_x_input.text()) is 0:
            self.phase_x_input.setText("0")
        if len(self.phase_y_input.text()) is 0:
            self.phase_y_input.setText("0")
        if len(self.phase_z_input.text()) is 0:
            self.phase_z_input.setText("0")
        if len(self.time_input.text()) is 0:
            self.time_input.setText("0")

        self.freq_x_input.setText(self.freq_x_input.text().replace(",", "."))
        self.freq_y_input.setText(self.freq_y_input.text().replace(",", "."))
        self.freq_z_input.setText(self.freq_z_input.text().replace(",", "."))
        self.amp_x_input.setText(self.amp_x_input.text().replace(",", "."))
        self.amp_y_input.setText(self.amp_y_input.text().replace(",", "."))
        self.amp_z_input.setText(self.amp_z_input.text().replace(",", "."))
        self.phase_x_input.setText(self.phase_x_input.text().replace(",", "."))
        self.phase_y_input.setText(self.phase_y_input.text().replace(",", "."))
        self.phase_z_input.setText(self.phase_z_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class RegularWaveMotionTimeline(QtGui.QWidget):
    """ A Regular Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RegularWaveGen)

    def __init__(self, reg_wave_gen):
        if not isinstance(reg_wave_gen, RegularWaveGen):
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline with a wrong object")
        if reg_wave_gen is None:
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline without a motion object")
        super(RegularWaveMotionTimeline, self).__init__()
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)


class IrregularWaveMotionTimeline(QtGui.QWidget):
    """ An Irregular Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, IrregularWaveGen)

    def __init__(self, irreg_wave_gen):
        if not isinstance(irreg_wave_gen, IrregularWaveGen):
            raise TypeError("You tried to spawn an irregular wave generator "
                            "motion widget in the timeline with a wrong object")
        if irreg_wave_gen is None:
            raise TypeError("You tried to spawn an irregular wave generator "
                            "motion widget in the timeline without a motion object")
        super(IrregularWaveMotionTimeline, self).__init__()
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)
