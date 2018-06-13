#!/usr/bin/env python2.7
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
import shutil
import glob

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
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
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
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
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if rect_motion is None:
            raise TypeError(
                "You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super(RectilinearMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rect_motion.parent_movement
        self.label = QtGui.QLabel("Rectilinear \nMotion  ")
        self.label.setMinimumWidth(75)
        self.velocity_label = QtGui.QLabel("Vel (X, Y, Z): ")
        self.x_input = QtGui.QLineEdit()
        self.x_input.setStyleSheet("width: 5px;")
        self.y_input = QtGui.QLineEdit()
        self.y_input.setStyleSheet("width: 5px;")
        self.z_input = QtGui.QLineEdit()
        self.z_input.setStyleSheet("width: 5px;")
        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

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
        self.label = QtGui.QLabel("Accelerated \nRectilinear \nMotion ")
        self.label.setMinimumWidth(75)
        self.data_layout = QtGui.QVBoxLayout()
        self.data_layout.setContentsMargins(0, 0, 0, 0)
        self.data_velocity_layout = QtGui.QHBoxLayout()
        self.data_velocity_layout.setContentsMargins(0, 0, 0, 0)
        self.data_acceleration_layout = QtGui.QHBoxLayout()
        self.data_acceleration_layout.setContentsMargins(0, 0, 0, 0)

        self.velocity_label = QtGui.QLabel("Vel (X, Y, Z): ")
        self.x_input = QtGui.QLineEdit()
        self.x_input.setStyleSheet("width: 5px;")
        self.y_input = QtGui.QLineEdit()
        self.y_input.setStyleSheet("width: 5px;")
        self.z_input = QtGui.QLineEdit()
        self.z_input.setStyleSheet("width: 5px;")

        self.acceleration_label = QtGui.QLabel("Acc (X, Y, Z): ")
        self.xa_input = QtGui.QLineEdit()
        self.xa_input.setStyleSheet("width: 5px;")
        self.ya_input = QtGui.QLineEdit()
        self.ya_input.setStyleSheet("width: 5px;")
        self.za_input = QtGui.QLineEdit()
        self.za_input.setStyleSheet("width: 5px;")

        [self.data_velocity_layout.addWidget(x) for x in [
            self.velocity_label, self.x_input, self.y_input, self.z_input
        ]]
        [self.data_acceleration_layout.addWidget(x) for x in [
            self.acceleration_label, self.xa_input, self.ya_input, self.za_input
        ]]

        self.data_layout.addLayout(self.data_velocity_layout)
        self.data_layout.addLayout(self.data_acceleration_layout)

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

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
            raise TypeError(
                "You tried to spawn a rotational motion widget in the timeline with a wrong object")
        if rot_motion is None:
            raise TypeError(
                "You tried to spawn a rotational motion widget in the timeline without a motion object")
        super(RotationalMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rot_motion.parent_movement
        self.label = QtGui.QLabel("Rotational \nMotion  ")
        self.label.setMinimumWidth(75)
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_input.setStyleSheet("width: 5px;")
        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

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
        self.velocity_input.setText(
            self.velocity_input.text().replace(",", "."))
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
        self.label = QtGui.QLabel("Accelerated \nRotational \nMotion ")
        self.label.setMinimumWidth(75)
        self.vel_and_acc_layout = QtGui.QVBoxLayout()
        self.vel_layout = QtGui.QHBoxLayout()
        self.acc_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.acceleration_input = QtGui.QLineEdit()
        self.acceleration_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_input.setStyleSheet("width: 5px;")
        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

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
        self.velocity_input.setText(
            self.velocity_input.text().replace(",", "."))
        self.acceleration_input.setText(
            self.acceleration_input.text().replace(",", "."))
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
        self.label = QtGui.QLabel("Accelerated \nCircular \nMotion ")
        self.label.setMinimumWidth(75)
        self.vel_and_acc_layout = QtGui.QVBoxLayout()
        self.vel_layout = QtGui.QHBoxLayout()
        self.acc_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.acceleration_input = QtGui.QLineEdit()
        self.acceleration_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_input.setStyleSheet("width: 5px;")

        self.reference_label = QtGui.QLabel("Ref (X, Y, Z): ")
        self.reference_x_input = QtGui.QLineEdit()
        self.reference_x_input.setStyleSheet("width: 5px;")
        self.reference_y_input = QtGui.QLineEdit()
        self.reference_y_input.setStyleSheet("width: 5px;")
        self.reference_z_input = QtGui.QLineEdit()
        self.reference_z_input.setStyleSheet("width: 5px;")

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

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
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addWidget(self.reference_label)
        self.main_layout.addWidget(self.reference_x_input)
        self.main_layout.addWidget(self.reference_y_input)
        self.main_layout.addWidget(self.reference_z_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
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
        self.reference_x_input.setText(
            self.reference_x_input.text().replace(",", "."))
        self.reference_y_input.setText(
            self.reference_y_input.text().replace(",", "."))
        self.reference_z_input.setText(
            self.reference_z_input.text().replace(",", "."))
        self.velocity_input.setText(
            self.velocity_input.text().replace(",", "."))
        self.acceleration_input.setText(
            self.acceleration_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))


class RotSinuMotionTimeline(QtGui.QWidget):
    """ A sinusoidal rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RotSinuMotion)
    deleted = QtCore.Signal(int, RotSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rot_sinu_motion):
        if not isinstance(rot_sinu_motion, RotSinuMotion):
            raise TypeError("You tried to spawn a sinusoidal rotational "
                            "motion widget in the timeline with a wrong object")
        if rot_sinu_motion is None:
            raise TypeError("You tried to spawn a sinusoidal rotational "
                            "motion widget in the timeline without a motion object")
        super(RotSinuMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = rot_sinu_motion.parent_movement
        self.label = QtGui.QLabel("Sinusoidal \nRotational \nMotion ")
        self.label.setMinimumWidth(75)
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_input.setStyleSheet("width: 5px;")

        self.freq_label = QtGui.QLabel("Freq (hz)")
        self.freq_input = QtGui.QLineEdit()
        self.freq_input.setStyleSheet("width: 5px;")

        self.ampl_label = QtGui.QLabel("Ampl (rad)")
        self.ampl_input = QtGui.QLineEdit()
        self.ampl_input.setStyleSheet("width: 5px;")

        self.phase_label = QtGui.QLabel("Phase (rad)")
        self.phase_input = QtGui.QLineEdit()
        self.phase_input.setStyleSheet("width: 5px;")

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
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
        self.main_layout.addWidget(self.freq_label)
        self.main_layout.addWidget(self.freq_input)
        self.main_layout.addWidget(self.ampl_label)
        self.main_layout.addWidget(self.ampl_input)
        self.main_layout.addWidget(self.phase_label)
        self.main_layout.addWidget(self.phase_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
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
    """ A sinusoidal circular motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, CirSinuMotion)
    deleted = QtCore.Signal(int, CirSinuMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, cir_sinu_motion):
        if not isinstance(cir_sinu_motion, CirSinuMotion):
            raise TypeError("You tried to spawn a sinusoidal circular "
                            "motion widget in the timeline with a wrong object")
        if cir_sinu_motion is None:
            raise TypeError("You tried to spawn a sinusoidal circular "
                            "motion widget in the timeline without a motion object")
        super(CirSinuMotionTimeline, self).__init__()
        self.index = index
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.parent_movement = cir_sinu_motion.parent_movement
        self.label = QtGui.QLabel("Sinusoidal \nCircular \nMotion ")
        self.label.setMinimumWidth(75)
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
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

        self.reference_label = QtGui.QLabel("Ref (X, Y, Z): ")
        self.reference_x_input = QtGui.QLineEdit()
        self.reference_x_input.setStyleSheet("width: 5px;")
        self.reference_y_input = QtGui.QLineEdit()
        self.reference_y_input.setStyleSheet("width: 5px;")
        self.reference_z_input = QtGui.QLineEdit()
        self.reference_z_input.setStyleSheet("width: 5px;")

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
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

        self.ref_first_row.addWidget(self.freq_label)
        self.ref_first_row.addWidget(self.freq_input)
        self.ref_first_row.addWidget(self.ampl_label)
        self.ref_first_row.addWidget(self.ampl_input)
        self.ref_first_row.addWidget(self.phase_label)
        self.ref_first_row.addWidget(self.phase_input)

        self.ref_second_row.addWidget(self.reference_label)
        self.ref_second_row.addWidget(self.reference_x_input)
        self.ref_second_row.addWidget(self.reference_y_input)
        self.ref_second_row.addWidget(self.reference_z_input)

        self.ref_layout.addLayout(self.ref_first_row)
        self.ref_layout.addLayout(self.ref_second_row)

        self.main_layout.addLayout(self.ref_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
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
        self.reference_x_input.setText(
            self.reference_x_input.text().replace(",", "."))
        self.reference_y_input.setText(
            self.reference_y_input.text().replace(",", "."))
        self.reference_z_input.setText(
            self.reference_z_input.text().replace(",", "."))
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
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

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
    """ A sinusoidal rectilinear motion graphical representation for a table-based timeline """

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
        self.label = QtGui.QLabel("Sinusoidal \nRectilinear \nMotion ")
        self.label.setMinimumWidth(75)
        self.freq_amp_layout = QtGui.QVBoxLayout()
        self.freq_amp_first_row_layout = QtGui.QHBoxLayout()
        self.freq_amp_second_row_layout = QtGui.QHBoxLayout()
        self.freq_label = QtGui.QLabel("Freq (X, Y, Z): ")
        self.amp_label = QtGui.QLabel("Amp (X, Y, Z): ")
        self.freq_x_input = QtGui.QLineEdit()
        self.freq_x_input.setStyleSheet("width: 5px;")
        self.freq_y_input = QtGui.QLineEdit()
        self.freq_y_input.setStyleSheet("width: 5px;")
        self.freq_z_input = QtGui.QLineEdit()
        self.freq_z_input.setStyleSheet("width: 5px;")
        self.amp_x_input = QtGui.QLineEdit()
        self.amp_x_input.setStyleSheet("width: 5px;")
        self.amp_y_input = QtGui.QLineEdit()
        self.amp_y_input.setStyleSheet("width: 5px;")
        self.amp_z_input = QtGui.QLineEdit()
        self.amp_z_input.setStyleSheet("width: 5px;")

        self.phase_label = QtGui.QLabel("Phase (X, Y, Z): ")
        self.phase_x_input = QtGui.QLineEdit()
        self.phase_x_input.setStyleSheet("width: 5px;")
        self.phase_y_input = QtGui.QLineEdit()
        self.phase_y_input.setStyleSheet("width: 5px;")
        self.phase_z_input = QtGui.QLineEdit()
        self.phase_z_input.setStyleSheet("width: 5px;")

        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            guiutils.get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)

        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.freq_amp_first_row_layout.addWidget(self.freq_label)
        self.freq_amp_first_row_layout.addWidget(self.freq_x_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_y_input)
        self.freq_amp_first_row_layout.addWidget(self.freq_z_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_label)
        self.freq_amp_second_row_layout.addWidget(self.amp_x_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_y_input)
        self.freq_amp_second_row_layout.addWidget(self.amp_z_input)
        self.freq_amp_layout.addLayout(self.freq_amp_first_row_layout)
        self.freq_amp_layout.addLayout(self.freq_amp_second_row_layout)
        self.main_layout.addLayout(self.freq_amp_layout)
        self.main_layout.addWidget(self.phase_label)
        self.main_layout.addWidget(self.phase_x_input)
        self.main_layout.addWidget(self.phase_y_input)
        self.main_layout.addWidget(self.phase_z_input)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
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


class RegularPistonWaveMotionTimeline(QtGui.QWidget):
    """ A Regular Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RegularPistonWaveGen)

    def __init__(self, reg_wave_gen):
        if not isinstance(reg_wave_gen, RegularPistonWaveGen):
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline with a wrong object")
        if reg_wave_gen is None:
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline without a motion object")
        super(RegularPistonWaveMotionTimeline, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = reg_wave_gen.parent_movement

        self.root_label = QtGui.QLabel(__("Regular wave generator (Piston)"))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.wave_order_label = QtGui.QLabel(__("Wave Order"))
        self.wave_order_selector = QtGui.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtGui.QLabel(__("Depth (m): "))
        self.depth_input = QtGui.QLineEdit()

        self.fixed_depth_label = QtGui.QLabel(__("Fixed depth (m): "))
        self.fixed_depth_input = QtGui.QLineEdit()
        self.fixed_depth_input.setEnabled(False)

        self.piston_dir_label = QtGui.QLabel(
            __("Piston direction (X, Y, Z): "))
        self.piston_dir_x = QtGui.QLineEdit()
        self.piston_dir_y = QtGui.QLineEdit()
        self.piston_dir_z = QtGui.QLineEdit()

        self.wave_height_label = QtGui.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtGui.QLineEdit()

        self.wave_period_label = QtGui.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtGui.QLineEdit()

        self.phase_label = QtGui.QLabel(__("Phase (rad): "))
        self.phase_input = QtGui.QLineEdit()

        self.ramp_label = QtGui.QLabel(__("Ramp: "))
        self.ramp_input = QtGui.QLineEdit()

        self.disksave_label = QtGui.QLabel(__("Save theoretical values > "))
        self.disksave_periods = QtGui.QLineEdit()
        self.disksave_periods_label = QtGui.QLabel(__("Periods: "))
        self.disksave_periodsteps = QtGui.QLineEdit()
        self.disksave_periodsteps_label = QtGui.QLabel(__("Period Steps: "))
        self.disksave_xpos = QtGui.QLineEdit()
        self.disksave_xpos_label = QtGui.QLabel(__("X Pos (m): "))
        self.disksave_zpos = QtGui.QLineEdit()
        self.disksave_zpos_label = QtGui.QLabel(__("Z Pos (m): "))

        self.awas_label = QtGui.QLabel(__("AWAS configuration"))
        self.awas_enabled = QtGui.QCheckBox(__("Enabled"))

        self.awas_startawas_label = QtGui.QLabel(__("Start AWAS (s): "))
        self.awas_startawas_input = QtGui.QLineEdit()

        self.awas_swl_label = QtGui.QLabel(__("Still water level (m): "))
        self.awas_swl_input = QtGui.QLineEdit()

        self.awas_elevation_label = QtGui.QLabel(__("Wave order: "))
        self.awas_elevation_selector = QtGui.QComboBox()
        self.awas_elevation_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.awas_gaugex_label = QtGui.QLabel(__("Gauge X (coef*h): "))
        self.awas_gaugex_input = QtGui.QLineEdit()

        self.awas_gaugey_label = QtGui.QLabel(__("Gauge Y (m): "))
        self.awas_gaugey_input = QtGui.QLineEdit()

        self.awas_gaugezmin_label = QtGui.QLabel(__("Gauge Z Min (m): "))
        self.awas_gaugezmin_input = QtGui.QLineEdit()

        self.awas_gaugezmax_label = QtGui.QLabel(__("Gauge Z Max (m): "))
        self.awas_gaugezmax_input = QtGui.QLineEdit()

        self.awas_gaugedp_label = QtGui.QLabel(__("Gauge dp: "))
        self.awas_gaugedp_input = QtGui.QLineEdit()

        self.awas_coefmasslimit_label = QtGui.QLabel(__("Coef. mass limit: "))
        self.awas_coefmasslimit_input = QtGui.QLineEdit()

        self.awas_savedata_label = QtGui.QLabel(__("Save data: "))
        self.awas_savedata_selector = QtGui.QComboBox()
        self.awas_savedata_selector.insertItems(
            0, [__("By Part"), __("More Info"), __("By Step")])

        self.awas_limitace_label = QtGui.QLabel(__("Limit acceleration: "))
        self.awas_limitace_input = QtGui.QLineEdit()

        self.awas_correction_label = QtGui.QLabel(__("Drift correction: "))
        self.awas_correction_enabled = QtGui.QCheckBox(__("Enabled"))

        self.awas_correction_coefstroke_label = QtGui.QLabel(__("Coefstroke"))
        self.awas_correction_coefstroke_input = QtGui.QLineEdit()

        self.awas_correction_coefperiod_label = QtGui.QLabel(__("Coefperiod"))
        self.awas_correction_coefperiod_input = QtGui.QLineEdit()

        self.awas_correction_powerfunc_label = QtGui.QLabel(__("Powerfunc"))
        self.awas_correction_powerfunc_input = QtGui.QLineEdit()

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        [self.root_layout.addWidget(x) for x in [
            self.duration_label, self.duration_input]]

        self.first_row_layout = QtGui.QHBoxLayout()
        [self.first_row_layout.addWidget(x) for x in [self.wave_order_label, self.wave_order_selector,
                                                      self.depth_label, self.depth_input,
                                                      self.fixed_depth_label, self.fixed_depth_input]]

        self.second_row_layout = QtGui.QHBoxLayout()
        [self.second_row_layout.addWidget(x) for x in [self.piston_dir_label,
                                                       self.piston_dir_x,
                                                       self.piston_dir_y,
                                                       self.piston_dir_z]]

        self.third_row_layout = QtGui.QHBoxLayout()
        [self.third_row_layout.addWidget(x) for x in [self.wave_height_label, self.wave_height_input,
                                                      self.wave_period_label, self.wave_period_input]]

        self.fourth_row_layout = QtGui.QHBoxLayout()
        [self.fourth_row_layout.addWidget(x) for x in [self.phase_label, self.phase_input,
                                                       self.ramp_label, self.ramp_input]]

        self.fifth_row_layout = QtGui.QHBoxLayout()
        [self.fifth_row_layout.addWidget(x) for x in [self.disksave_label,
                                                      self.disksave_periods_label, self.disksave_periods,
                                                      self.disksave_periodsteps_label, self.disksave_periodsteps,
                                                      self.disksave_xpos_label, self.disksave_xpos,
                                                      self.disksave_zpos_label, self.disksave_zpos]]

        self.awas_root_layout = QtGui.QHBoxLayout()
        self.awas_root_layout.addWidget(self.awas_label)
        self.awas_root_layout.addStretch(1)
        self.awas_root_layout.addWidget(self.awas_enabled)

        self.awas_first_row_layout = QtGui.QHBoxLayout()
        [self.awas_first_row_layout.addWidget(x) for x in [self.awas_startawas_label, self.awas_startawas_input,
                                                           self.awas_swl_label, self.awas_swl_input,
                                                           self.awas_elevation_label, self.awas_elevation_selector]]

        self.awas_second_row_layout = QtGui.QHBoxLayout()
        [self.awas_second_row_layout.addWidget(x) for x in [
            self.awas_gaugex_label, self.awas_gaugex_input, self.awas_gaugey_label, self.awas_gaugey_input]]

        self.awas_third_row_layout = QtGui.QHBoxLayout()
        [self.awas_third_row_layout.addWidget(x) for x in [
            self.awas_gaugezmin_label, self.awas_gaugezmin_input, self.awas_gaugezmax_label, self.awas_gaugezmax_input]]

        self.awas_fourth_row_layout = QtGui.QHBoxLayout()
        [self.awas_fourth_row_layout.addWidget(x) for x in [
            self.awas_gaugedp_label, self.awas_gaugedp_input, self.awas_coefmasslimit_label,
            self.awas_coefmasslimit_input]]

        self.awas_fifth_row_layout = QtGui.QHBoxLayout()
        [self.awas_fifth_row_layout.addWidget(x) for x in [
            self.awas_savedata_label, self.awas_savedata_selector, self.awas_limitace_label, self.awas_limitace_input]]

        self.awas_sixth_row_layout = QtGui.QHBoxLayout()
        [self.awas_sixth_row_layout.addWidget(x) for x in
         [self.awas_correction_label, self.awas_correction_enabled, self.awas_correction_coefstroke_label,
          self.awas_correction_coefstroke_input,
          self.awas_correction_coefperiod_label, self.awas_correction_coefperiod_input,
          self.awas_correction_powerfunc_label, self.awas_correction_powerfunc_input]]

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.first_row_layout, self.second_row_layout,
                                                 self.third_row_layout, self.fourth_row_layout,
                                                 self.fifth_row_layout]]
        self.main_layout.addWidget(guiutils.h_line_generator())
        self.main_layout.addLayout(self.awas_root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.awas_first_row_layout,
                                                 self.awas_second_row_layout, self.awas_third_row_layout,
                                                 self.awas_fourth_row_layout, self.awas_fifth_row_layout,
                                                 self.awas_sixth_row_layout]]

        self.setLayout(self.main_layout)
        self.fill_values(reg_wave_gen)
        self._init_connections()

    def fill_values(self, reg_wave_gen):
        self.duration_input.setText(str(reg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(reg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(reg_wave_gen.depth))
        self.fixed_depth_input.setText(str(reg_wave_gen.fixed_depth))
        self.piston_dir_x.setText(str(reg_wave_gen.piston_dir[0]))
        self.piston_dir_y.setText(str(reg_wave_gen.piston_dir[1]))
        self.piston_dir_z.setText(str(reg_wave_gen.piston_dir[2]))
        self.wave_height_input.setText(str(reg_wave_gen.wave_height))
        self.wave_period_input.setText(str(reg_wave_gen.wave_period))
        self.phase_input.setText(str(reg_wave_gen.phase))
        self.ramp_input.setText(str(reg_wave_gen.ramp))
        self.disksave_periods.setText(str(reg_wave_gen.disksave_periods))
        self.disksave_periodsteps.setText(
            str(reg_wave_gen.disksave_periodsteps))
        self.disksave_xpos.setText(str(reg_wave_gen.disksave_xpos))
        self.disksave_zpos.setText(str(reg_wave_gen.disksave_zpos))
        self.awas_enabled.setChecked(bool(reg_wave_gen.awas.enabled))
        self.awas_startawas_input.setText(str(reg_wave_gen.awas.startawas))
        self.awas_swl_input.setText(str(reg_wave_gen.awas.swl))
        self.awas_gaugex_input.setText(str(reg_wave_gen.awas.gaugex))
        self.awas_gaugey_input.setText(str(reg_wave_gen.awas.gaugey))
        self.awas_gaugezmin_input.setText(str(reg_wave_gen.awas.gaugezmin))
        self.awas_gaugezmax_input.setText(str(reg_wave_gen.awas.gaugezmax))
        self.awas_gaugedp_input.setText(str(reg_wave_gen.awas.gaugedp))
        self.awas_coefmasslimit_input.setText(
            str(reg_wave_gen.awas.coefmasslimit))
        self.awas_limitace_input.setText(str(reg_wave_gen.awas.limitace))
        self.awas_elevation_selector.setCurrentIndex(
            int(reg_wave_gen.awas.elevation) - 1)
        self.awas_savedata_selector.setCurrentIndex(
            int(reg_wave_gen.awas.savedata) - 1)
        self.awas_correction_enabled.setChecked(
            bool(reg_wave_gen.awas.correction.enabled))
        self.awas_correction_coefstroke_input.setText(
            str(reg_wave_gen.awas.correction.coefstroke))
        self.awas_correction_coefperiod_input.setText(
            str(reg_wave_gen.awas.correction.coefperiod))
        self.awas_correction_powerfunc_input.setText(
            str(reg_wave_gen.awas.correction.powerfunc))
        self._awas_enabled_handler()

    def _init_connections(self):
        self.wave_order_selector.currentIndexChanged.connect(self.on_change)
        self.awas_savedata_selector.currentIndexChanged.connect(self.on_change)
        self.awas_elevation_selector.currentIndexChanged.connect(
            self.on_change)
        self.awas_enabled.stateChanged.connect(self.on_change)
        self.awas_correction_enabled.stateChanged.connect(
            self._awas_correction_enabled_handler)
        [x.textChanged.connect(self.on_change) for x in [self.duration_input, self.depth_input,
                                                         self.fixed_depth_input, self.piston_dir_x,
                                                         self.piston_dir_y, self.piston_dir_z,
                                                         self.wave_height_input, self.wave_period_input,
                                                         self.ramp_input, self.phase_input, self.disksave_periods,
                                                         self.disksave_periodsteps, self.disksave_xpos,
                                                         self.disksave_zpos, self.awas_startawas_input,
                                                         self.awas_swl_input, self.awas_gaugex_input,
                                                         self.awas_gaugey_input, self.awas_gaugezmin_input,
                                                         self.awas_gaugezmax_input, self.awas_coefmasslimit_input,
                                                         self.awas_limitace_input,
                                                         self.awas_correction_coefstroke_input,
                                                         self.awas_correction_coefperiod_input,
                                                         self.awas_correction_powerfunc_input]]

    def on_change(self):
        self._sanitize_input()
        self._awas_enabled_handler()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def _awas_enabled_handler(self):
        [x.setEnabled(self.awas_enabled.isChecked()) for x in [
            self.awas_startawas_input, self.awas_swl_input,
            self.awas_elevation_selector, self.awas_gaugex_input,
            self.awas_gaugey_input, self.awas_gaugezmin_input,
            self.awas_gaugezmax_input, self.awas_gaugedp_input,
            self.awas_coefmasslimit_input, self.awas_savedata_selector,
            self.awas_limitace_input, self.awas_correction_coefperiod_input,
            self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
            self.awas_correction_enabled
        ]]
        self._awas_correction_enabled_handler()

    def _awas_correction_enabled_handler(self):
        enable_state = self.awas_correction_enabled.isChecked()
        if not self.awas_enabled.isChecked():
            enable_state = False

        [x.setEnabled(enable_state) for x in [
            self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
            self.awas_correction_coefperiod_input
        ]]

    def construct_motion_object(self):
        _cmo_elevation = None
        if self.awas_elevation_selector.currentIndex() is 0:
            _cmo_elevation = AWASWaveOrder.FIRST_ORDER
        elif self.awas_elevation_selector.currentIndex() is 1:
            _cmo_elevation = AWASWaveOrder.SECOND_ORDER
        else:
            _cmo_elevation = AWASWaveOrder.FIRST_ORDER

        _cmo_savedata = None
        if self.awas_savedata_selector.currentIndex() is 0:
            _cmo_savedata = AWASSaveMethod.BY_PART
        elif self.awas_savedata_selector.currentIndex() is 1:
            _cmo_savedata = AWASSaveMethod.MORE_INFO
        elif self.awas_savedata_selector.currentIndex() is 2:
            _cmo_savedata = AWASSaveMethod.BY_STEP
        else:
            _cmo_savedata = AWASSaveMethod.BY_PART

        _cmo_correction = AWASCorrection(
            enabled=self.awas_correction_enabled.isChecked(),
            coefstroke=float(self.awas_correction_coefstroke_input.text()),
            coefperiod=float(self.awas_correction_coefperiod_input.text()),
            powerfunc=float(self.awas_correction_powerfunc_input.text())
        )

        awas_object = AWAS(
            enabled=self.awas_enabled.isChecked(),
            startawas=float(self.awas_startawas_input.text()),
            swl=float(self.awas_swl_input.text()),
            elevation=_cmo_elevation,
            gaugex=float(self.awas_gaugex_input.text()),
            gaugey=float(self.awas_gaugey_input.text()),
            gaugezmin=float(self.awas_gaugezmin_input.text()),
            gaugezmax=float(self.awas_gaugezmax_input.text()),
            gaugedp=float(self.awas_gaugedp_input.text()),
            coefmasslimit=float(self.awas_coefmasslimit_input.text()),
            savedata=_cmo_savedata,
            limitace=float(self.awas_limitace_input.text()),
            correction=_cmo_correction
        )

        return RegularPistonWaveGen(parent_movement=self.parent_movement,
                                    wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                    duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
                                    fixed_depth=float(
                                        self.fixed_depth_input.text()),
                                    piston_dir=[float(self.piston_dir_x.text()),
                                                float(
                                                    self.piston_dir_y.text()),
                                                float(self.piston_dir_z.text())],
                                    wave_height=float(
                                        self.wave_height_input.text()),
                                    wave_period=float(
                                        self.wave_period_input.text()),
                                    phase=float(self.phase_input.text()),
                                    ramp=float(self.ramp_input.text()),
                                    disksave_periods=float(
                                        self.disksave_periods.text()),
                                    disksave_periodsteps=float(
                                        self.disksave_periodsteps.text()),
                                    disksave_xpos=float(
                                        self.disksave_xpos.text()),
                                    disksave_zpos=float(
                                        self.disksave_zpos.text()),
                                    awas=awas_object)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        [x.setText("0")
         if len(x.text()) is 0
         else x.setText(x.text().replace(",", "."))
         for x in [self.duration_input, self.depth_input,
                   self.fixed_depth_input, self.piston_dir_x,
                   self.piston_dir_y, self.piston_dir_z,
                   self.wave_height_input, self.wave_period_input,
                   self.ramp_input, self.phase_input, self.disksave_periods,
                   self.disksave_periodsteps, self.disksave_xpos,
                   self.disksave_zpos, self.awas_startawas_input,
                   self.awas_swl_input, self.awas_gaugex_input,
                   self.awas_gaugey_input, self.awas_gaugezmax_input,
                   self.awas_gaugezmin_input, self.awas_gaugedp_input,
                   self.awas_coefmasslimit_input, self.awas_limitace_input,
                   self.awas_correction_coefstroke_input, self.awas_correction_coefperiod_input,
                   self.awas_correction_powerfunc_input]]


class IrregularPistonWaveMotionTimeline(QtGui.QWidget):
    """ An Irregular Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, IrregularPistonWaveGen)

    def __init__(self, irreg_wave_gen):
        if not isinstance(irreg_wave_gen, IrregularPistonWaveGen):
            raise TypeError("You tried to spawn an irregular wave generator "
                            "motion widget in the timeline with a wrong object")
        if irreg_wave_gen is None:
            raise TypeError("You tried to spawn an irregular wave generator "
                            "motion widget in the timeline without a motion object")
        super(IrregularPistonWaveMotionTimeline, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = irreg_wave_gen.parent_movement

        self.root_label = QtGui.QLabel(__("Irregular wave generator (Piston)"))

        self.duration_label = QtGui.QLabel(__("Duration"))
        self.duration_input = QtGui.QLineEdit()

        self.wave_order_label = QtGui.QLabel(__("Wave Order"))
        self.wave_order_selector = QtGui.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtGui.QLabel(__("Depth (m): "))
        self.depth_input = QtGui.QLineEdit()

        self.fixed_depth_label = QtGui.QLabel(__("Fixed depth (m): "))
        self.fixed_depth_input = QtGui.QLineEdit()
        self.fixed_depth_input.setEnabled(False)
        self.fixed_depth_units_label = QtGui.QLabel()

        self.piston_dir_label = QtGui.QLabel(
            __("Piston direction (X, Y, Z): "))
        self.piston_dir_x = QtGui.QLineEdit()
        self.piston_dir_y = QtGui.QLineEdit()
        self.piston_dir_z = QtGui.QLineEdit()

        self.wave_height_label = QtGui.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtGui.QLineEdit()

        self.wave_period_label = QtGui.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtGui.QLineEdit()

        self.spectrum_label = QtGui.QLabel(__("Spectrum"))
        self.spectrum_selector = QtGui.QComboBox()
        # Index numbers match IrregularSpectrum static values
        self.spectrum_selector.insertItems(0, ["Jonswap", "Pierson-Moskowitz"])

        self.discretization_label = QtGui.QLabel(__("Discretization"))
        self.discretization_selector = QtGui.QComboBox()
        # Index numbers match IrregularDiscretization static values
        self.discretization_selector.insertItems(
            0, ["Regular", "Random", "Stretched", "Crosstreched"])

        self.peak_coef_label = QtGui.QLabel(__("Peak Coeff"))
        self.peak_coef_input = QtGui.QLineEdit()

        self.waves_label = QtGui.QLabel(__("Number of waves"))
        self.waves_input = QtGui.QLineEdit()

        self.randomseed_label = QtGui.QLabel(__("Random Seed"))
        self.randomseed_input = QtGui.QLineEdit()

        self.serieini_label = QtGui.QLabel(
            __("Initial time in wave serie (s): "))
        self.serieini_input = QtGui.QLineEdit()

        self.serieini_autofit = QtGui.QCheckBox("Auto fit")

        self.ramptime_label = QtGui.QLabel(__("Time of ramp (s): "))
        self.ramptime_input = QtGui.QLineEdit()

        self.savemotion_label = QtGui.QLabel(__("Motion saving > "))
        self.savemotion_time_input = QtGui.QLineEdit()
        self.savemotion_time_label = QtGui.QLabel(__("Time (s): "))
        self.savemotion_timedt_input = QtGui.QLineEdit()
        self.savemotion_timedt_label = QtGui.QLabel(__("DT Time (s): "))
        self.savemotion_xpos_input = QtGui.QLineEdit()
        self.savemotion_xpos_label = QtGui.QLabel(__("X Pos (m): "))
        self.savemotion_zpos_input = QtGui.QLineEdit()
        self.savemotion_zpos_label = QtGui.QLabel(__("Z Pos (m): "))

        self.saveserie_label = QtGui.QLabel(__("Save serie > "))
        self.saveserie_timemin_input = QtGui.QLineEdit()
        self.saveserie_timemin_label = QtGui.QLabel(__("Min. Time (s): "))
        self.saveserie_timemax_input = QtGui.QLineEdit()
        self.saveserie_timemax_label = QtGui.QLabel(__("Max. Time (s): "))
        self.saveserie_timedt_input = QtGui.QLineEdit()
        self.saveserie_timedt_label = QtGui.QLabel(__("DT Time (s): "))
        self.saveserie_xpos_input = QtGui.QLineEdit()
        self.saveserie_xpos_label = QtGui.QLabel(__("X Pos (m): "))

        self.saveseriewaves_label = QtGui.QLabel(__("Save serie waves > "))
        self.saveseriewaves_timemin_input = QtGui.QLineEdit()
        self.saveseriewaves_timemin_label = QtGui.QLabel(__("Min. Time (s): "))
        self.saveseriewaves_timemax_input = QtGui.QLineEdit()
        self.saveseriewaves_timemax_label = QtGui.QLabel(__("Max. Time (s): "))
        self.saveseriewaves_xpos_input = QtGui.QLineEdit()
        self.saveseriewaves_xpos_label = QtGui.QLabel(__("X Pos (m): "))

        self.awas_label = QtGui.QLabel(__("AWAS configuration"))
        self.awas_enabled = QtGui.QCheckBox(__("Enabled"))

        self.awas_startawas_label = QtGui.QLabel(__("Start AWAS (s): "))
        self.awas_startawas_input = QtGui.QLineEdit()

        self.awas_swl_label = QtGui.QLabel(__("Still water level (m): "))
        self.awas_swl_input = QtGui.QLineEdit()

        self.awas_elevation_label = QtGui.QLabel(__("Wave order: "))
        self.awas_elevation_selector = QtGui.QComboBox()
        self.awas_elevation_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.awas_gaugex_label = QtGui.QLabel(__("Gauge X (coef*h): "))
        self.awas_gaugex_input = QtGui.QLineEdit()

        self.awas_gaugey_label = QtGui.QLabel(__("Gauge Y (m): "))
        self.awas_gaugey_input = QtGui.QLineEdit()

        self.awas_gaugezmin_label = QtGui.QLabel(__("Gauge Z Min (m): "))
        self.awas_gaugezmin_input = QtGui.QLineEdit()

        self.awas_gaugezmax_label = QtGui.QLabel(__("Gauge Z Max (m): "))
        self.awas_gaugezmax_input = QtGui.QLineEdit()

        self.awas_gaugedp_label = QtGui.QLabel(__("Gauge dp: "))
        self.awas_gaugedp_input = QtGui.QLineEdit()

        self.awas_coefmasslimit_label = QtGui.QLabel(__("Coef. mass limit: "))
        self.awas_coefmasslimit_input = QtGui.QLineEdit()

        self.awas_savedata_label = QtGui.QLabel(__("Save data: "))
        self.awas_savedata_selector = QtGui.QComboBox()
        self.awas_savedata_selector.insertItems(
            0, [__("By Part"), __("More Info"), __("By Step")])

        self.awas_limitace_label = QtGui.QLabel(__("Limit acceleration: "))
        self.awas_limitace_input = QtGui.QLineEdit()

        self.awas_correction_label = QtGui.QLabel(__("Drift correction: "))
        self.awas_correction_enabled = QtGui.QCheckBox(__("Enabled"))

        self.awas_correction_coefstroke_label = QtGui.QLabel(__("Coefstroke"))
        self.awas_correction_coefstroke_input = QtGui.QLineEdit()

        self.awas_correction_coefperiod_label = QtGui.QLabel(__("Coefperiod"))
        self.awas_correction_coefperiod_input = QtGui.QLineEdit()

        self.awas_correction_powerfunc_label = QtGui.QLabel(__("Powerfunc"))
        self.awas_correction_powerfunc_input = QtGui.QLineEdit()

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        [self.root_layout.addWidget(x) for x in [
            self.duration_label, self.duration_input]]

        self.first_row_layout = QtGui.QHBoxLayout()
        [self.first_row_layout.addWidget(x) for x in [self.wave_order_label, self.wave_order_selector,
                                                      self.depth_label, self.depth_input,
                                                      self.fixed_depth_label, self.fixed_depth_input]]

        self.second_row_layout = QtGui.QHBoxLayout()
        [self.second_row_layout.addWidget(x) for x in [self.piston_dir_label,
                                                       self.piston_dir_x,
                                                       self.piston_dir_y,
                                                       self.piston_dir_z]]

        self.third_row_layout = QtGui.QHBoxLayout()
        [self.third_row_layout.addWidget(x) for x in [self.wave_height_label, self.wave_height_input,
                                                      self.wave_period_label, self.wave_period_input]]

        self.fourth_row_layout = QtGui.QHBoxLayout()
        [self.fourth_row_layout.addWidget(x) for x in [self.spectrum_label, self.spectrum_selector,
                                                       self.discretization_label, self.discretization_selector,
                                                       self.peak_coef_label, self.peak_coef_input]]

        self.fifth_row_layout = QtGui.QHBoxLayout()
        [self.fifth_row_layout.addWidget(x) for x in [self.waves_label, self.waves_input,
                                                      self.randomseed_label, self.randomseed_input]]

        self.sixth_row_layout = QtGui.QHBoxLayout()
        [self.sixth_row_layout.addWidget(
            x) for x in [self.serieini_label, self.serieini_input, self.serieini_autofit]]

        self.seventh_row_layout = QtGui.QHBoxLayout()
        [self.seventh_row_layout.addWidget(
            x) for x in [self.ramptime_label, self.ramptime_input]]

        self.eighth_row_layout = QtGui.QHBoxLayout()
        [self.eighth_row_layout.addWidget(x) for x in [self.savemotion_label,
                                                       self.savemotion_time_label, self.savemotion_time_input,
                                                       self.savemotion_timedt_label, self.savemotion_timedt_input,
                                                       self.savemotion_xpos_label, self.savemotion_xpos_input,
                                                       self.savemotion_zpos_label, self.savemotion_zpos_input]]

        self.ninth_row_layout = QtGui.QHBoxLayout()
        [self.ninth_row_layout.addWidget(x) for x in [self.saveserie_label,
                                                      self.saveserie_timemin_label,
                                                      self.saveserie_timemin_input,
                                                      self.saveserie_timemax_label,
                                                      self.saveserie_timemax_input,
                                                      self.saveserie_timedt_label,
                                                      self.saveserie_timedt_input,
                                                      self.saveserie_xpos_label,
                                                      self.saveserie_xpos_input]]

        self.tenth_row_layout = QtGui.QHBoxLayout()
        [self.tenth_row_layout.addWidget(x) for x in [self.saveseriewaves_label,
                                                      self.saveseriewaves_timemin_label,
                                                      self.saveseriewaves_timemin_input,
                                                      self.saveseriewaves_timemax_label,
                                                      self.saveseriewaves_timemax_input,
                                                      self.saveseriewaves_xpos_label,
                                                      self.saveseriewaves_xpos_input]]

        self.awas_root_layout = QtGui.QHBoxLayout()
        self.awas_root_layout.addWidget(self.awas_label)
        self.awas_root_layout.addStretch(1)
        self.awas_root_layout.addWidget(self.awas_enabled)

        self.awas_first_row_layout = QtGui.QHBoxLayout()
        [self.awas_first_row_layout.addWidget(x) for x in [self.awas_startawas_label, self.awas_startawas_input,
                                                           self.awas_swl_label, self.awas_swl_input,
                                                           self.awas_elevation_label, self.awas_elevation_selector]]

        self.awas_second_row_layout = QtGui.QHBoxLayout()
        [self.awas_second_row_layout.addWidget(x) for x in [
            self.awas_gaugex_label, self.awas_gaugex_input, self.awas_gaugey_label, self.awas_gaugey_input]]

        self.awas_third_row_layout = QtGui.QHBoxLayout()
        [self.awas_third_row_layout.addWidget(x) for x in [
            self.awas_gaugezmin_label, self.awas_gaugezmin_input, self.awas_gaugezmax_label, self.awas_gaugezmax_input]]

        self.awas_fourth_row_layout = QtGui.QHBoxLayout()
        [self.awas_fourth_row_layout.addWidget(x) for x in [
            self.awas_gaugedp_label, self.awas_gaugedp_input, self.awas_coefmasslimit_label,
            self.awas_coefmasslimit_input]]

        self.awas_fifth_row_layout = QtGui.QHBoxLayout()
        [self.awas_fifth_row_layout.addWidget(x) for x in [
            self.awas_savedata_label, self.awas_savedata_selector, self.awas_limitace_label, self.awas_limitace_input]]

        self.awas_sixth_row_layout = QtGui.QHBoxLayout()
        [self.awas_sixth_row_layout.addWidget(x) for x in
         [self.awas_correction_label, self.awas_correction_enabled, self.awas_correction_coefstroke_label,
          self.awas_correction_coefstroke_input,
          self.awas_correction_coefperiod_label, self.awas_correction_coefperiod_input,
          self.awas_correction_powerfunc_label, self.awas_correction_powerfunc_input]]

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout,
                                                 self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout,
                                                 self.seventh_row_layout, self.eighth_row_layout, self.ninth_row_layout,
                                                 self.tenth_row_layout]]

        self.main_layout.addWidget(guiutils.h_line_generator())
        self.main_layout.addLayout(self.awas_root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.awas_first_row_layout,
                                                 self.awas_second_row_layout, self.awas_third_row_layout,
                                                 self.awas_fourth_row_layout, self.awas_fifth_row_layout,
                                                 self.awas_sixth_row_layout]]

        self.setLayout(self.main_layout)
        self.fill_values(irreg_wave_gen)
        self._init_connections()

    def fill_values(self, irreg_wave_gen):
        self.duration_input.setText(str(irreg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(irreg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(irreg_wave_gen.depth))
        self.fixed_depth_input.setText(str(irreg_wave_gen.fixed_depth))
        self.piston_dir_x.setText(str(irreg_wave_gen.piston_dir[0]))
        self.piston_dir_y.setText(str(irreg_wave_gen.piston_dir[1]))
        self.piston_dir_z.setText(str(irreg_wave_gen.piston_dir[2]))
        self.wave_height_input.setText(str(irreg_wave_gen.wave_height))
        self.wave_period_input.setText(str(irreg_wave_gen.wave_period))
        self.spectrum_selector.setCurrentIndex(int(irreg_wave_gen.spectrum))
        self.discretization_selector.setCurrentIndex(
            int(irreg_wave_gen.discretization))
        self.peak_coef_input.setText(str(irreg_wave_gen.peak_coef))
        self.waves_input.setText(str(irreg_wave_gen.waves))
        self.randomseed_input.setText(str(irreg_wave_gen.randomseed))
        self.serieini_input.setText(str(irreg_wave_gen.serieini))
        self.serieini_autofit.setChecked(irreg_wave_gen.serieini_autofit)
        self.ramptime_input.setText(str(irreg_wave_gen.ramptime))
        self.savemotion_time_input.setText(str(irreg_wave_gen.savemotion_time))
        self.savemotion_timedt_input.setText(
            str(irreg_wave_gen.savemotion_timedt))
        self.savemotion_xpos_input.setText(str(irreg_wave_gen.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(irreg_wave_gen.savemotion_zpos))
        self.saveserie_timemin_input.setText(
            str(irreg_wave_gen.saveserie_timemin))
        self.saveserie_timemax_input.setText(
            str(irreg_wave_gen.saveserie_timemax))
        self.saveserie_timedt_input.setText(
            str(irreg_wave_gen.saveserie_timedt))
        self.saveserie_xpos_input.setText(str(irreg_wave_gen.saveserie_xpos))
        self.saveseriewaves_timemin_input.setText(
            str(irreg_wave_gen.saveseriewaves_timemin))
        self.saveseriewaves_timemax_input.setText(
            str(irreg_wave_gen.saveseriewaves_timemax))
        self.saveseriewaves_xpos_input.setText(
            str(irreg_wave_gen.saveseriewaves_xpos))
        self.awas_enabled.setChecked(bool(irreg_wave_gen.awas.enabled))
        self.awas_startawas_input.setText(str(irreg_wave_gen.awas.startawas))
        self.awas_swl_input.setText(str(irreg_wave_gen.awas.swl))
        self.awas_gaugex_input.setText(str(irreg_wave_gen.awas.gaugex))
        self.awas_gaugey_input.setText(str(irreg_wave_gen.awas.gaugey))
        self.awas_gaugezmin_input.setText(str(irreg_wave_gen.awas.gaugezmin))
        self.awas_gaugezmax_input.setText(str(irreg_wave_gen.awas.gaugezmax))
        self.awas_gaugedp_input.setText(str(irreg_wave_gen.awas.gaugedp))
        self.awas_coefmasslimit_input.setText(
            str(irreg_wave_gen.awas.coefmasslimit))
        self.awas_limitace_input.setText(str(irreg_wave_gen.awas.limitace))
        self.awas_elevation_selector.setCurrentIndex(
            int(irreg_wave_gen.awas.elevation) - 1)
        self.awas_savedata_selector.setCurrentIndex(
            int(irreg_wave_gen.awas.savedata) - 1)
        self.awas_correction_enabled.setChecked(
            bool(irreg_wave_gen.awas.correction.enabled))
        self.awas_correction_coefstroke_input.setText(
            str(irreg_wave_gen.awas.correction.coefstroke))
        self.awas_correction_coefperiod_input.setText(
            str(irreg_wave_gen.awas.correction.coefperiod))
        self.awas_correction_powerfunc_input.setText(
            str(irreg_wave_gen.awas.correction.powerfunc))
        self._awas_enabled_handler()

    def _init_connections(self):
        self.serieini_autofit.stateChanged.connect(self.on_change)
        self.awas_savedata_selector.currentIndexChanged.connect(self.on_change)
        self.awas_elevation_selector.currentIndexChanged.connect(
            self.on_change)
        self.awas_enabled.stateChanged.connect(self.on_change)
        self.awas_correction_enabled.stateChanged.connect(
            self._awas_correction_enabled_handler)
        [x.currentIndexChanged.connect(self.on_change) for x in [self.wave_order_selector, self.spectrum_selector,
                                                                 self.discretization_selector]]

        [x.textChanged.connect(self.on_change) for x in [self.peak_coef_input, self.waves_input, self.randomseed_input,
                                                         self.serieini_input, self.ramptime_input, self.duration_input,
                                                         self.depth_input, self.fixed_depth_input, self.piston_dir_x,
                                                         self.piston_dir_y, self.piston_dir_z, self.wave_height_input,
                                                         self.wave_period_input, self.savemotion_time_input,
                                                         self.savemotion_timedt_input, self.savemotion_xpos_input,
                                                         self.savemotion_zpos_input, self.saveserie_timemin_input,
                                                         self.saveserie_timemax_input, self.saveserie_timedt_input,
                                                         self.saveserie_xpos_input, self.saveseriewaves_timemin_input,
                                                         self.saveseriewaves_timemax_input,
                                                         self.saveseriewaves_xpos_input, self.awas_startawas_input,
                                                         self.awas_swl_input, self.awas_gaugex_input,
                                                         self.awas_gaugey_input, self.awas_gaugezmin_input,
                                                         self.awas_gaugezmax_input, self.awas_coefmasslimit_input,
                                                         self.awas_limitace_input,
                                                         self.awas_correction_coefstroke_input,
                                                         self.awas_correction_coefperiod_input,
                                                         self.awas_correction_powerfunc_input]]

    def on_change(self):
        self._sanitize_input()
        self._awas_enabled_handler()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def _awas_enabled_handler(self):
        [x.setEnabled(self.awas_enabled.isChecked()) for x in [
            self.awas_startawas_input, self.awas_swl_input,
            self.awas_elevation_selector, self.awas_gaugex_input,
            self.awas_gaugey_input, self.awas_gaugezmin_input,
            self.awas_gaugezmax_input, self.awas_gaugedp_input,
            self.awas_coefmasslimit_input, self.awas_savedata_selector,
            self.awas_limitace_input, self.awas_correction_coefperiod_input,
            self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
            self.awas_correction_enabled
        ]]
        self._awas_correction_enabled_handler()

    def _awas_correction_enabled_handler(self):
        enable_state = self.awas_correction_enabled.isChecked()
        if not self.awas_enabled.isChecked():
            enable_state = False

        [x.setEnabled(enable_state) for x in [
            self.awas_correction_coefstroke_input, self.awas_correction_powerfunc_input,
            self.awas_correction_coefperiod_input
        ]]

    def construct_motion_object(self):
        _cmo_elevation = None
        if self.awas_elevation_selector.currentIndex() is 0:
            _cmo_elevation = AWASWaveOrder.FIRST_ORDER
        elif self.awas_elevation_selector.currentIndex() is 1:
            _cmo_elevation = AWASWaveOrder.SECOND_ORDER
        else:
            _cmo_elevation = AWASWaveOrder.FIRST_ORDER

        _cmo_savedata = None
        if self.awas_savedata_selector.currentIndex() is 0:
            _cmo_savedata = AWASSaveMethod.BY_PART
        elif self.awas_savedata_selector.currentIndex() is 1:
            _cmo_savedata = AWASSaveMethod.MORE_INFO
        elif self.awas_savedata_selector.currentIndex() is 2:
            _cmo_savedata = AWASSaveMethod.BY_STEP
        else:
            _cmo_savedata = AWASSaveMethod.BY_PART

        _cmo_correction = AWASCorrection(
            enabled=self.awas_correction_enabled.isChecked(),
            coefstroke=float(self.awas_correction_coefstroke_input.text()),
            coefperiod=float(self.awas_correction_coefperiod_input.text()),
            powerfunc=float(self.awas_correction_powerfunc_input.text())
        )

        awas_object = AWAS(
            enabled=self.awas_enabled.isChecked(),
            startawas=float(self.awas_startawas_input.text()),
            swl=float(self.awas_swl_input.text()),
            elevation=_cmo_elevation,
            gaugex=float(self.awas_gaugex_input.text()),
            gaugey=float(self.awas_gaugey_input.text()),
            gaugezmin=float(self.awas_gaugezmin_input.text()),
            gaugezmax=float(self.awas_gaugezmax_input.text()),
            gaugedp=float(self.awas_gaugedp_input.text()),
            coefmasslimit=float(self.awas_coefmasslimit_input.text()),
            savedata=_cmo_savedata,
            limitace=float(self.awas_limitace_input.text()),
            correction=_cmo_correction
        )

        return IrregularPistonWaveGen(parent_movement=self.parent_movement,
                                      wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                      duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
                                      fixed_depth=float(
                                          self.fixed_depth_input.text()),
                                      piston_dir=[float(self.piston_dir_x.text()),
                                                  float(
                                                      self.piston_dir_y.text()),
                                                  float(self.piston_dir_z.text())],
                                      wave_height=float(
                                          self.wave_height_input.text()),
                                      wave_period=float(
                                          self.wave_period_input.text()),
                                      spectrum=self.spectrum_selector.currentIndex(),
                                      discretization=self.discretization_selector.currentIndex(),
                                      peak_coef=float(
                                          self.peak_coef_input.text()),
                                      waves=float(self.waves_input.text()),
                                      randomseed=float(
                                          self.randomseed_input.text()),
                                      serieini=float(
                                          self.serieini_input.text()),
                                      ramptime=float(
                                          self.ramptime_input.text()),
                                      serieini_autofit=self.serieini_autofit.isChecked(),
                                      savemotion_time=str(
                                          self.savemotion_time_input.text()),
                                      savemotion_timedt=str(
                                          self.savemotion_timedt_input.text()),
                                      savemotion_xpos=str(
                                          self.savemotion_xpos_input.text()),
                                      savemotion_zpos=str(
                                          self.savemotion_zpos_input.text()),
                                      saveserie_timemin=str(
                                          self.saveserie_timemin_input.text()),
                                      saveserie_timemax=str(
                                          self.saveserie_timemax_input.text()),
                                      saveserie_timedt=str(
                                          self.saveserie_timedt_input.text()),
                                      saveserie_xpos=str(
                                          self.saveserie_xpos_input.text()),
                                      saveseriewaves_timemin=str(
                                          self.saveseriewaves_timemin_input.text()),
                                      saveseriewaves_timemax=str(
                                          self.saveseriewaves_timemax_input.text()),
                                      saveseriewaves_xpos=str(self.saveseriewaves_xpos_input.text()),
                                      awas=awas_object)

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        [x.setText("0")
         if len(x.text()) is 0
         else x.setText(x.text().replace(",", "."))
         for x in [self.duration_input, self.depth_input,
                   self.fixed_depth_input, self.piston_dir_x,
                   self.piston_dir_y, self.piston_dir_z,
                   self.wave_height_input, self.wave_period_input,
                   self.peak_coef_input, self.randomseed_input,
                   self.serieini_input, self.ramptime_input,
                   self.savemotion_time_input, self.savemotion_timedt_input,
                   self.savemotion_xpos_input, self.savemotion_zpos_input,
                   self.saveserie_timemin_input, self.saveserie_timemax_input,
                   self.saveserie_timedt_input, self.saveserie_xpos_input,
                   self.saveseriewaves_timemin_input, self.saveseriewaves_timemax_input,
                   self.saveseriewaves_xpos_input, self.awas_startawas_input,
                   self.awas_swl_input, self.awas_gaugex_input,
                   self.awas_gaugey_input, self.awas_gaugezmax_input,
                   self.awas_gaugezmin_input, self.awas_gaugedp_input,
                   self.awas_coefmasslimit_input, self.awas_limitace_input,
                   self.awas_correction_coefstroke_input, self.awas_correction_coefperiod_input,
                   self.awas_correction_powerfunc_input]]


class RegularFlapWaveMotionTimeline(QtGui.QWidget):
    """ A Regular Flap Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RegularFlapWaveGen)

    def __init__(self, reg_wave_gen):
        if not isinstance(reg_wave_gen, RegularFlapWaveGen):
            raise TypeError("You tried to spawn a regular flap wave generator "
                            "motion widget in the timeline with a wrong object")
        if reg_wave_gen is None:
            raise TypeError("You tried to spawn a regular flap wave generator "
                            "motion widget in the timeline without a motion object")
        super(RegularFlapWaveMotionTimeline, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = reg_wave_gen.parent_movement

        self.root_label = QtGui.QLabel(
            __("Regular flap wave generator (Flap)"))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.wave_order_label = QtGui.QLabel(__("Wave Order"))
        self.wave_order_selector = QtGui.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtGui.QLabel(__("Depth (m): "))
        self.depth_input = QtGui.QLineEdit()

        self.fixed_depth_label = QtGui.QLabel(__("Fixed depth (m): "))
        self.fixed_depth_input = QtGui.QLineEdit()
        self.fixed_depth_input.setEnabled(False)

        self.flap_axis_0_label = QtGui.QLabel(
            __("Flap axis 0 (X, Y, Z): "))
        self.flap_axis_0_x = QtGui.QLineEdit()
        self.flap_axis_0_y = QtGui.QLineEdit()
        self.flap_axis_0_z = QtGui.QLineEdit()

        self.flap_axis_1_label = QtGui.QLabel(
            __("Flap axis 1 (X, Y, Z): "))
        self.flap_axis_1_x = QtGui.QLineEdit()
        self.flap_axis_1_y = QtGui.QLineEdit()
        self.flap_axis_1_z = QtGui.QLineEdit()

        self.wave_height_label = QtGui.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtGui.QLineEdit()

        self.wave_period_label = QtGui.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtGui.QLineEdit()

        self.variable_draft_label = QtGui.QLabel(__("Variable Draft (m): "))
        self.variable_draft_input = QtGui.QLineEdit()

        self.phase_label = QtGui.QLabel(__("Phase (rad): "))
        self.phase_input = QtGui.QLineEdit()

        self.ramp_label = QtGui.QLabel(__("Ramp: "))
        self.ramp_input = QtGui.QLineEdit()

        self.disksave_label = QtGui.QLabel(__("Save theoretical values > "))
        self.disksave_periods = QtGui.QLineEdit()
        self.disksave_periods_label = QtGui.QLabel(__("Periods: "))
        self.disksave_periodsteps = QtGui.QLineEdit()
        self.disksave_periodsteps_label = QtGui.QLabel(__("Period Steps: "))
        self.disksave_xpos = QtGui.QLineEdit()
        self.disksave_xpos_label = QtGui.QLabel(__("X Pos (m): "))
        self.disksave_zpos = QtGui.QLineEdit()
        self.disksave_zpos_label = QtGui.QLabel(__("Z Pos (m): "))

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        [self.root_layout.addWidget(x) for x in [
            self.duration_label, self.duration_input]]

        self.first_row_layout = QtGui.QHBoxLayout()
        [self.first_row_layout.addWidget(x) for x in [self.wave_order_label, self.wave_order_selector,
                                                      self.depth_label, self.depth_input,
                                                      self.fixed_depth_label, self.fixed_depth_input]]

        self.second_row_layout = QtGui.QHBoxLayout()
        [self.second_row_layout.addWidget(x) for x in [self.flap_axis_0_label,
                                                       self.flap_axis_0_x,
                                                       self.flap_axis_0_y,
                                                       self.flap_axis_0_z]]

        self.third_row_layout = QtGui.QHBoxLayout()
        [self.third_row_layout.addWidget(x) for x in [self.flap_axis_1_label,
                                                      self.flap_axis_1_x,
                                                      self.flap_axis_1_y,
                                                      self.flap_axis_1_z]]

        self.fourth_row_layout = QtGui.QHBoxLayout()
        [self.fourth_row_layout.addWidget(x) for x in [self.wave_height_label, self.wave_height_input,
                                                       self.wave_period_label, self.wave_period_input,
                                                       self.variable_draft_label, self.variable_draft_input]]

        self.fifth_row_layout = QtGui.QHBoxLayout()
        [self.fifth_row_layout.addWidget(x) for x in [self.phase_label, self.phase_input,
                                                      self.ramp_label, self.ramp_input]]

        self.sixth_row_layout = QtGui.QHBoxLayout()
        [self.sixth_row_layout.addWidget(x) for x in [self.disksave_label,
                                                      self.disksave_periods_label, self.disksave_periods,
                                                      self.disksave_periodsteps_label, self.disksave_periodsteps,
                                                      self.disksave_xpos_label, self.disksave_xpos,
                                                      self.disksave_zpos_label, self.disksave_zpos]]

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.first_row_layout, self.second_row_layout,
                                                 self.third_row_layout, self.fourth_row_layout,
                                                 self.fifth_row_layout, self.sixth_row_layout]]

        self.setLayout(self.main_layout)
        self.fill_values(reg_wave_gen)
        self._init_connections()

    def fill_values(self, reg_wave_gen):
        self.duration_input.setText(str(reg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(reg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(reg_wave_gen.depth))
        self.fixed_depth_input.setText(str(reg_wave_gen.fixed_depth))
        self.flap_axis_0_x.setText(str(reg_wave_gen.flapaxis0[0]))
        self.flap_axis_0_y.setText(str(reg_wave_gen.flapaxis0[1]))
        self.flap_axis_0_z.setText(str(reg_wave_gen.flapaxis0[2]))
        self.flap_axis_1_x.setText(str(reg_wave_gen.flapaxis1[0]))
        self.flap_axis_1_y.setText(str(reg_wave_gen.flapaxis1[1]))
        self.flap_axis_1_z.setText(str(reg_wave_gen.flapaxis1[2]))
        self.variable_draft_input.setText(str(reg_wave_gen.variable_draft))
        self.wave_height_input.setText(str(reg_wave_gen.wave_height))
        self.wave_period_input.setText(str(reg_wave_gen.wave_period))
        self.phase_input.setText(str(reg_wave_gen.phase))
        self.ramp_input.setText(str(reg_wave_gen.ramp))
        self.disksave_periods.setText(str(reg_wave_gen.disksave_periods))
        self.disksave_periodsteps.setText(
            str(reg_wave_gen.disksave_periodsteps))
        self.disksave_xpos.setText(str(reg_wave_gen.disksave_xpos))
        self.disksave_zpos.setText(str(reg_wave_gen.disksave_zpos))

    def _init_connections(self):
        self.wave_order_selector.currentIndexChanged.connect(self.on_change)
        [x.textChanged.connect(self.on_change) for x in [self.duration_input, self.depth_input,
                                                         self.fixed_depth_input,
                                                         self.variable_draft_input, self.flap_axis_0_x,
                                                         self.flap_axis_0_y, self.flap_axis_0_z,
                                                         self.flap_axis_1_x,
                                                         self.flap_axis_1_y, self.flap_axis_1_z,
                                                         self.wave_height_input, self.wave_period_input,
                                                         self.ramp_input, self.phase_input, self.disksave_periods,
                                                         self.disksave_periodsteps, self.disksave_xpos,
                                                         self.disksave_zpos]]

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return RegularFlapWaveGen(parent_movement=self.parent_movement,
                                  wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                  duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
                                  fixed_depth=float(
                                      self.fixed_depth_input.text()),
                                  flapaxis0=[float(self.flap_axis_0_x.text()),
                                             float(
                                                 self.flap_axis_0_y.text()),
                                             float(self.flap_axis_0_z.text())],
                                  flapaxis1=[float(self.flap_axis_1_x.text()),
                                             float(
                                                 self.flap_axis_1_y.text()),
                                             float(self.flap_axis_1_z.text())],
                                  variable_draft=float(
                                      self.variable_draft_input.text()),
                                  wave_height=float(
                                      self.wave_height_input.text()),
                                  wave_period=float(
                                      self.wave_period_input.text()),
                                  phase=float(self.phase_input.text()),
                                  ramp=float(self.ramp_input.text()),
                                  disksave_periods=float(
                                      self.disksave_periods.text()),
                                  disksave_periodsteps=float(
                                      self.disksave_periodsteps.text()),
                                  disksave_xpos=float(
                                      self.disksave_xpos.text()),
                                  disksave_zpos=float(self.disksave_zpos.text()))

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        [x.setText("0")
         if len(x.text()) is 0
         else x.setText(x.text().replace(",", "."))
         for x in [self.duration_input, self.depth_input,
                   self.fixed_depth_input, self.flap_axis_0_x,
                   self.flap_axis_0_y, self.flap_axis_0_z,
                   self.flap_axis_1_x,
                   self.flap_axis_1_y, self.flap_axis_1_z,
                   self.variable_draft_input,
                   self.wave_height_input, self.wave_period_input,
                   self.ramp_input, self.phase_input, self.disksave_periods,
                   self.disksave_periodsteps, self.disksave_xpos,
                   self.disksave_zpos]]


class IrregularFlapWaveMotionTimeline(QtGui.QWidget):
    """ An Irregular Flap Wave motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, IrregularFlapWaveGen)

    def __init__(self, irreg_wave_gen):
        if not isinstance(irreg_wave_gen, IrregularFlapWaveGen):
            raise TypeError("You tried to spawn an irregular flap wave generator "
                            "motion widget in the timeline with a wrong object")
        if irreg_wave_gen is None:
            raise TypeError("You tried to spawn an irregular flap wave generator "
                            "motion widget in the timeline without a motion object")
        super(IrregularFlapWaveMotionTimeline, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = irreg_wave_gen.parent_movement

        self.root_label = QtGui.QLabel(
            __("Irregular flap wave generator (Flap)"))

        self.duration_label = QtGui.QLabel(__("Duration"))
        self.duration_input = QtGui.QLineEdit()

        self.wave_order_label = QtGui.QLabel(__("Wave Order"))
        self.wave_order_selector = QtGui.QComboBox()
        self.wave_order_selector.insertItems(
            0, [__("1st Order"), __("2nd Order")])

        self.depth_label = QtGui.QLabel(__("Depth (m): "))
        self.depth_input = QtGui.QLineEdit()

        self.fixed_depth_label = QtGui.QLabel(__("Fixed depth (m): "))
        self.fixed_depth_input = QtGui.QLineEdit()
        self.fixed_depth_input.setEnabled(False)
        self.fixed_depth_units_label = QtGui.QLabel()

        self.flap_axis_0_label = QtGui.QLabel(
            __("Flap axis 0 (X, Y, Z): "))
        self.flap_axis_0_x = QtGui.QLineEdit()
        self.flap_axis_0_y = QtGui.QLineEdit()
        self.flap_axis_0_z = QtGui.QLineEdit()

        self.flap_axis_1_label = QtGui.QLabel(
            __("Flap axis 1 (X, Y, Z): "))
        self.flap_axis_1_x = QtGui.QLineEdit()
        self.flap_axis_1_y = QtGui.QLineEdit()
        self.flap_axis_1_z = QtGui.QLineEdit()

        self.wave_height_label = QtGui.QLabel(__("Wave height (m): "))
        self.wave_height_input = QtGui.QLineEdit()

        self.wave_period_label = QtGui.QLabel(__("Wave period (s): "))
        self.wave_period_input = QtGui.QLineEdit()

        self.variable_draft_label = QtGui.QLabel(__("Variable Draft (m): "))
        self.variable_draft_input = QtGui.QLineEdit()

        self.spectrum_label = QtGui.QLabel(__("Spectrum"))
        self.spectrum_selector = QtGui.QComboBox()
        # Index numbers match IrregularSpectrum static values
        self.spectrum_selector.insertItems(0, ["Jonswap", "Pierson-Moskowitz"])

        self.discretization_label = QtGui.QLabel(__("Discretization"))
        self.discretization_selector = QtGui.QComboBox()
        # Index numbers match IrregularDiscretization static values
        self.discretization_selector.insertItems(
            0, ["Regular", "Random", "Stretched", "Crosstreched"])

        self.peak_coef_label = QtGui.QLabel(__("Peak Coeff"))
        self.peak_coef_input = QtGui.QLineEdit()

        self.waves_label = QtGui.QLabel(__("Number of waves"))
        self.waves_input = QtGui.QLineEdit()

        self.randomseed_label = QtGui.QLabel(__("Random Seed"))
        self.randomseed_input = QtGui.QLineEdit()

        self.serieini_label = QtGui.QLabel(
            __("Initial time in wave serie (s): "))
        self.serieini_input = QtGui.QLineEdit()

        self.serieini_autofit = QtGui.QCheckBox("Auto fit")

        self.ramptime_label = QtGui.QLabel(__("Time of ramp (s): "))
        self.ramptime_input = QtGui.QLineEdit()

        self.savemotion_label = QtGui.QLabel(__("Motion saving > "))
        self.savemotion_time_input = QtGui.QLineEdit()
        self.savemotion_time_label = QtGui.QLabel(__("Time (s): "))
        self.savemotion_timedt_input = QtGui.QLineEdit()
        self.savemotion_timedt_label = QtGui.QLabel(__("DT Time (s): "))
        self.savemotion_xpos_input = QtGui.QLineEdit()
        self.savemotion_xpos_label = QtGui.QLabel(__("X Pos (m): "))
        self.savemotion_zpos_input = QtGui.QLineEdit()
        self.savemotion_zpos_label = QtGui.QLabel(__("Z Pos (m): "))

        self.saveserie_label = QtGui.QLabel(__("Save serie > "))
        self.saveserie_timemin_input = QtGui.QLineEdit()
        self.saveserie_timemin_label = QtGui.QLabel(__("Min. Time (s): "))
        self.saveserie_timemax_input = QtGui.QLineEdit()
        self.saveserie_timemax_label = QtGui.QLabel(__("Max. Time (s): "))
        self.saveserie_timedt_input = QtGui.QLineEdit()
        self.saveserie_timedt_label = QtGui.QLabel(__("DT Time (s): "))
        self.saveserie_xpos_input = QtGui.QLineEdit()
        self.saveserie_xpos_label = QtGui.QLabel(__("X Pos (m): "))

        self.saveseriewaves_label = QtGui.QLabel(__("Save serie waves > "))
        self.saveseriewaves_timemin_input = QtGui.QLineEdit()
        self.saveseriewaves_timemin_label = QtGui.QLabel(__("Min. Time (s): "))
        self.saveseriewaves_timemax_input = QtGui.QLineEdit()
        self.saveseriewaves_timemax_label = QtGui.QLabel(__("Max. Time (s): "))
        self.saveseriewaves_xpos_input = QtGui.QLineEdit()
        self.saveseriewaves_xpos_label = QtGui.QLabel(__("X Pos (m): "))

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        [self.root_layout.addWidget(x) for x in [
            self.duration_label, self.duration_input]]

        self.first_row_layout = QtGui.QHBoxLayout()
        [self.first_row_layout.addWidget(x) for x in [self.wave_order_label, self.wave_order_selector,
                                                      self.depth_label, self.depth_input,
                                                      self.fixed_depth_label, self.fixed_depth_input]]

        self.second_row_layout = QtGui.QHBoxLayout()
        [self.second_row_layout.addWidget(x) for x in [self.flap_axis_0_label,
                                                       self.flap_axis_0_x,
                                                       self.flap_axis_0_y,
                                                       self.flap_axis_0_z]]

        self.third_row_layout = QtGui.QHBoxLayout()
        [self.third_row_layout.addWidget(x) for x in [self.flap_axis_1_label,
                                                      self.flap_axis_1_x,
                                                      self.flap_axis_1_y,
                                                      self.flap_axis_1_z]]

        self.fourth_row_layout = QtGui.QHBoxLayout()
        [self.fourth_row_layout.addWidget(x) for x in [self.wave_height_label, self.wave_height_input,
                                                       self.wave_period_label, self.wave_period_input,
                                                       self.variable_draft_label, self.variable_draft_input]]

        self.fifth_row_layout = QtGui.QHBoxLayout()
        [self.fifth_row_layout.addWidget(x) for x in [self.spectrum_label, self.spectrum_selector,
                                                      self.discretization_label, self.discretization_selector,
                                                      self.peak_coef_label, self.peak_coef_input]]

        self.sixth_row_layout = QtGui.QHBoxLayout()
        [self.sixth_row_layout.addWidget(x) for x in [self.waves_label, self.waves_input,
                                                      self.randomseed_label, self.randomseed_input]]

        self.seventh_row_layout = QtGui.QHBoxLayout()
        [self.seventh_row_layout.addWidget(
            x) for x in [self.serieini_label, self.serieini_input, self.serieini_autofit]]

        self.eighth_row_layout = QtGui.QHBoxLayout()
        [self.eighth_row_layout.addWidget(
            x) for x in [self.ramptime_label, self.ramptime_input]]

        self.ninth_row_layout = QtGui.QHBoxLayout()
        [self.ninth_row_layout.addWidget(x) for x in [self.savemotion_label,
                                                      self.savemotion_time_label, self.savemotion_time_input,
                                                      self.savemotion_timedt_label, self.savemotion_timedt_input,
                                                      self.savemotion_xpos_label, self.savemotion_xpos_input,
                                                      self.savemotion_zpos_label, self.savemotion_zpos_input]]

        self.tenth_row_layout = QtGui.QHBoxLayout()
        [self.tenth_row_layout.addWidget(x) for x in [self.saveserie_label,
                                                      self.saveserie_timemin_label,
                                                      self.saveserie_timemin_input,
                                                      self.saveserie_timemax_label,
                                                      self.saveserie_timemax_input,
                                                      self.saveserie_timedt_label,
                                                      self.saveserie_timedt_input,
                                                      self.saveserie_xpos_label,
                                                      self.saveserie_xpos_input]]

        self.eleventh_row_layout = QtGui.QHBoxLayout()
        [self.eleventh_row_layout.addWidget(x) for x in [self.saveseriewaves_label,
                                                         self.saveseriewaves_timemin_label,
                                                         self.saveseriewaves_timemin_input,
                                                         self.saveseriewaves_timemax_label,
                                                         self.saveseriewaves_timemax_input,
                                                         self.saveseriewaves_xpos_label,
                                                         self.saveseriewaves_xpos_input]]

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.first_row_layout, self.second_row_layout, self.third_row_layout,
                                                 self.fourth_row_layout, self.fifth_row_layout, self.sixth_row_layout,
                                                 self.seventh_row_layout, self.eighth_row_layout, self.ninth_row_layout,
                                                 self.tenth_row_layout, self.eleventh_row_layout]]

        self.setLayout(self.main_layout)
        self.fill_values(irreg_wave_gen)
        self._init_connections()

    def fill_values(self, irreg_wave_gen):
        self.duration_input.setText(str(irreg_wave_gen.duration))
        self.wave_order_selector.setCurrentIndex(
            int(irreg_wave_gen.wave_order) - 1)
        self.depth_input.setText(str(irreg_wave_gen.depth))
        self.fixed_depth_input.setText(str(irreg_wave_gen.fixed_depth))
        self.flap_axis_0_x.setText(str(irreg_wave_gen.flapaxis0[0]))
        self.flap_axis_0_y.setText(str(irreg_wave_gen.flapaxis0[1]))
        self.flap_axis_0_z.setText(str(irreg_wave_gen.flapaxis0[2]))
        self.flap_axis_1_x.setText(str(irreg_wave_gen.flapaxis1[0]))
        self.flap_axis_1_y.setText(str(irreg_wave_gen.flapaxis1[1]))
        self.flap_axis_1_z.setText(str(irreg_wave_gen.flapaxis1[2]))
        self.wave_height_input.setText(str(irreg_wave_gen.wave_height))
        self.wave_period_input.setText(str(irreg_wave_gen.wave_period))
        self.variable_draft_input.setText(str(irreg_wave_gen.variable_draft))
        self.spectrum_selector.setCurrentIndex(int(irreg_wave_gen.spectrum))
        self.discretization_selector.setCurrentIndex(
            int(irreg_wave_gen.discretization))
        self.peak_coef_input.setText(str(irreg_wave_gen.peak_coef))
        self.waves_input.setText(str(irreg_wave_gen.waves))
        self.randomseed_input.setText(str(irreg_wave_gen.randomseed))
        self.serieini_input.setText(str(irreg_wave_gen.serieini))
        self.serieini_autofit.setChecked(irreg_wave_gen.serieini_autofit)
        self.ramptime_input.setText(str(irreg_wave_gen.ramptime))
        self.savemotion_time_input.setText(str(irreg_wave_gen.savemotion_time))
        self.savemotion_timedt_input.setText(
            str(irreg_wave_gen.savemotion_timedt))
        self.savemotion_xpos_input.setText(str(irreg_wave_gen.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(irreg_wave_gen.savemotion_zpos))
        self.saveserie_timemin_input.setText(
            str(irreg_wave_gen.saveserie_timemin))
        self.saveserie_timemax_input.setText(
            str(irreg_wave_gen.saveserie_timemax))
        self.saveserie_timedt_input.setText(
            str(irreg_wave_gen.saveserie_timedt))
        self.saveserie_xpos_input.setText(str(irreg_wave_gen.saveserie_xpos))
        self.saveseriewaves_timemin_input.setText(
            str(irreg_wave_gen.saveseriewaves_timemin))
        self.saveseriewaves_timemax_input.setText(
            str(irreg_wave_gen.saveseriewaves_timemax))
        self.saveseriewaves_xpos_input.setText(
            str(irreg_wave_gen.saveseriewaves_xpos))

    def _init_connections(self):
        self.serieini_autofit.stateChanged.connect(self.on_change)
        [x.currentIndexChanged.connect(self.on_change) for x in [self.wave_order_selector, self.spectrum_selector,
                                                                 self.discretization_selector]]

        [x.textChanged.connect(self.on_change) for x in [self.peak_coef_input, self.waves_input, self.randomseed_input,
                                                         self.serieini_input, self.ramptime_input, self.duration_input,
                                                         self.depth_input, self.fixed_depth_input, self.flap_axis_0_x,
                                                         self.flap_axis_0_y, self.flap_axis_0_z,
                                                         self.flap_axis_1_x,
                                                         self.flap_axis_1_y, self.flap_axis_1_z,
                                                         self.wave_height_input,
                                                         self.wave_period_input, self.variable_draft_input,
                                                         self.savemotion_time_input,
                                                         self.savemotion_timedt_input, self.savemotion_xpos_input,
                                                         self.savemotion_zpos_input, self.saveserie_timemin_input,
                                                         self.saveserie_timemax_input, self.saveserie_timedt_input,
                                                         self.saveserie_xpos_input, self.saveseriewaves_timemin_input,
                                                         self.saveseriewaves_timemax_input,
                                                         self.saveseriewaves_xpos_input]]

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return IrregularFlapWaveGen(parent_movement=self.parent_movement,
                                    wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                    duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
                                    fixed_depth=float(
                                        self.fixed_depth_input.text()),
                                    flapaxis0=[float(self.flap_axis_0_x.text()),
                                               float(
                                                   self.flap_axis_0_y.text()),
                                               float(self.flap_axis_0_z.text())],
                                    flapaxis1=[float(self.flap_axis_1_x.text()),
                                               float(
                                                   self.flap_axis_1_y.text()),
                                               float(self.flap_axis_1_z.text())],
                                    wave_height=float(
                                        self.wave_height_input.text()),
                                    wave_period=float(
                                        self.wave_period_input.text()),
                                    variable_draft=float(
                                        self.variable_draft_input.text()),
                                    spectrum=self.spectrum_selector.currentIndex(),
                                    discretization=self.discretization_selector.currentIndex(),
                                    peak_coef=float(
                                        self.peak_coef_input.text()),
                                    waves=float(self.waves_input.text()),
                                    randomseed=float(
                                        self.randomseed_input.text()),
                                    serieini=float(
                                        self.serieini_input.text()),
                                    ramptime=float(
                                        self.ramptime_input.text()),
                                    serieini_autofit=self.serieini_autofit.isChecked(),
                                    savemotion_time=str(
                                        self.savemotion_time_input.text()),
                                    savemotion_timedt=str(
                                        self.savemotion_timedt_input.text()),
                                    savemotion_xpos=str(
                                        self.savemotion_xpos_input.text()),
                                    savemotion_zpos=str(
                                        self.savemotion_zpos_input.text()),
                                    saveserie_timemin=str(
                                        self.saveserie_timemin_input.text()),
                                    saveserie_timemax=str(
                                        self.saveserie_timemax_input.text()),
                                    saveserie_timedt=str(
                                        self.saveserie_timedt_input.text()),
                                    saveserie_xpos=str(
                                        self.saveserie_xpos_input.text()),
                                    saveseriewaves_timemin=str(
                                        self.saveseriewaves_timemin_input.text()),
                                    saveseriewaves_timemax=str(
                                        self.saveseriewaves_timemax_input.text()),
                                    saveseriewaves_xpos=str(self.saveseriewaves_xpos_input.text()))

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        [x.setText("0")
         if len(x.text()) is 0
         else x.setText(x.text().replace(",", "."))
         for x in [self.duration_input, self.depth_input,
                   self.fixed_depth_input, self.flap_axis_0_x,
                   self.flap_axis_0_y, self.flap_axis_0_z,
                   self.flap_axis_1_x,
                   self.flap_axis_1_y, self.flap_axis_1_z,
                   self.wave_height_input, self.wave_period_input,
                   self.variable_draft_input,
                   self.peak_coef_input, self.randomseed_input,
                   self.serieini_input, self.ramptime_input,
                   self.savemotion_time_input, self.savemotion_timedt_input,
                   self.savemotion_xpos_input, self.savemotion_zpos_input,
                   self.saveserie_timemin_input, self.saveserie_timemax_input,
                   self.saveserie_timedt_input, self.saveserie_xpos_input,
                   self.saveseriewaves_timemin_input, self.saveseriewaves_timemax_input,
                   self.saveseriewaves_xpos_input]]


class FileMotionTimeline(QtGui.QWidget):
    """ A File motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, FileGen)

    def __init__(self, file_wave_gen, project_folder_path):
        if not isinstance(file_wave_gen, FileGen):
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline with a wrong object")
        if file_wave_gen is None:
            raise TypeError("You tried to spawn a regular wave generator "
                            "motion widget in the timeline without a motion object")
        super(FileMotionTimeline, self).__init__()
        # Needed for copying movement file to root of the case.
        self.project_folder_path = project_folder_path
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = file_wave_gen.parent_movement

        self.root_label = QtGui.QLabel(__("File movement: "))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.filename_label = QtGui.QLabel(__("File name: "))
        self.filename_input = QtGui.QLineEdit()
        self.filename_browse = QtGui.QPushButton(__("Browse"))

        self.fields_label = QtGui.QLabel(__("Number of fields: "))
        self.fields_input = QtGui.QLineEdit()

        self.fieldtime_label = QtGui.QLabel(__("Column with time: "))
        self.fieldtime_input = QtGui.QLineEdit()

        self.fieldx_label = QtGui.QLabel(__("X position column: "))
        self.fieldx_input = QtGui.QLineEdit()

        self.fieldy_label = QtGui.QLabel(__("Y position column: "))
        self.fieldy_input = QtGui.QLineEdit()

        self.fieldz_label = QtGui.QLabel(__("Z position column: "))
        self.fieldz_input = QtGui.QLineEdit()

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.duration_label)
        self.root_layout.addWidget(self.duration_input)

        self.first_row_layout = QtGui.QHBoxLayout()
        self.first_row_layout.addWidget(self.filename_label)
        self.first_row_layout.addWidget(self.filename_input)
        self.first_row_layout.addWidget(self.filename_browse)

        self.second_row_layout = QtGui.QHBoxLayout()
        self.second_row_layout.addWidget(self.fields_label)
        self.second_row_layout.addWidget(self.fields_input)

        self.third_row_layout = QtGui.QHBoxLayout()
        self.third_row_layout.addWidget(self.fieldtime_label)
        self.third_row_layout.addWidget(self.fieldtime_input)

        self.fourth_row_layout = QtGui.QHBoxLayout()
        [self.fourth_row_layout.addWidget(x) for x in [self.fieldx_label, self.fieldx_input, self.fieldy_label,
                                                       self.fieldy_input, self.fieldz_label, self.fieldz_input]]

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.first_row_layout, self.second_row_layout,
                                                 self.third_row_layout, self.fourth_row_layout]]

        self.setLayout(self.main_layout)
        self.fill_values(file_wave_gen)
        self._init_connections()

    def fill_values(self, file_wave_gen):
        self.duration_input.setText(str(file_wave_gen.duration))
        self.filename_input.setText(str(file_wave_gen.filename))
        self.fields_input.setText(str(file_wave_gen.fields))
        self.fieldtime_input.setText(str(file_wave_gen.fieldtime))
        self.fieldx_input.setText(str(file_wave_gen.fieldx))
        self.fieldy_input.setText(str(file_wave_gen.fieldy))
        self.fieldz_input.setText(str(file_wave_gen.fieldz))

    def _init_connections(self):
        [x.textChanged.connect(self.on_change) for x in [self.duration_input, self.filename_input, self.fields_input,
                                                         self.fieldtime_input, self.fieldx_input,
                                                         self.fieldy_input, self.fieldz_input]]
        self.filename_browse.clicked.connect(self.on_file_browse)

    def on_file_browse(self):
        # noinspection PyArgumentList
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self, __("Open file"), QtCore.QDir.homePath())
        self.filename_input.setText(filename)

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return FileGen(parent_movement=self.parent_movement,
                       duration=float(self.duration_input.text()),
                       filename=str(self.filename_input.text()),
                       fields=str(self.fields_input.text()),
                       fieldtime=str(self.fieldtime_input.text()),
                       fieldx=str(self.fieldx_input.text()),
                       fieldy=str(self.fieldy_input.text()),
                       fieldz=str(self.fieldz_input.text()))

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        [x.setText("0")
         if len(x.text()) is 0
         else x.setText(x.text().replace(",", "."))
         for x in [self.duration_input, self.fields_input, self.fieldtime_input, self.fieldx_input,
                   self.fieldy_input, self.fieldz_input]]


class RotationFileMotionTimeline(QtGui.QWidget):
    """ A rotation file motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, RotationFileGen)

    def __init__(self, rot_file_gen, project_folder_path):
        if not isinstance(rot_file_gen, RotationFileGen):
            raise TypeError("You tried to spawn a rotation file generator "
                            "motion widget in the timeline with a wrong object")
        if rot_file_gen is None:
            raise TypeError("You tried to spawn a rotation file generator "
                            "motion widget in the timeline without a motion object")
        super(RotationFileMotionTimeline, self).__init__()
        # Needed for copying movement file to root of the case.
        self.project_folder_path = project_folder_path
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.parent_movement = rot_file_gen.parent_movement

        self.root_label = QtGui.QLabel(__("Rotation file movement"))

        self.duration_label = QtGui.QLabel(__("Duration (s): "))
        self.duration_input = QtGui.QLineEdit()

        self.filename_label = QtGui.QLabel(__("File name: "))
        self.filename_input = QtGui.QLineEdit()
        self.filename_browse = QtGui.QPushButton(__("Browse"))

        self.anglesunits_label = QtGui.QLabel(__("Angle Units: "))
        self.anglesunits_selector = QtGui.QComboBox()
        self.anglesunits_selector.insertItems(
            0, [__("Degrees"), __("Radians")])

        self.axisp1x_label = QtGui.QLabel(__("Axis 1 X: "))
        self.axisp1x_input = QtGui.QLineEdit()

        self.axisp1y_label = QtGui.QLabel(__("Axis 1 Y: "))
        self.axisp1y_input = QtGui.QLineEdit()

        self.axisp1z_label = QtGui.QLabel(__("Axis 1 Z: "))
        self.axisp1z_input = QtGui.QLineEdit()

        self.axisp2x_label = QtGui.QLabel(__("Axis 2 X: "))
        self.axisp2x_input = QtGui.QLineEdit()

        self.axisp2y_label = QtGui.QLabel(__("Axis 2 Y: "))
        self.axisp2y_input = QtGui.QLineEdit()

        self.axisp2z_label = QtGui.QLabel(__("Axis 2 Z: "))
        self.axisp2z_input = QtGui.QLineEdit()

        self.root_layout = QtGui.QHBoxLayout()
        self.root_layout.addWidget(self.root_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.anglesunits_label)
        self.root_layout.addWidget(self.anglesunits_selector)
        self.root_layout.addWidget(self.duration_label)
        self.root_layout.addWidget(self.duration_input)

        self.first_row_layout = QtGui.QHBoxLayout()
        self.first_row_layout.addWidget(self.filename_label)
        self.first_row_layout.addWidget(self.filename_input)
        self.first_row_layout.addWidget(self.filename_browse)

        self.second_row_layout = QtGui.QHBoxLayout()
        [self.second_row_layout.addWidget(x) for x in [self.axisp1x_label, self.axisp1x_input,
                                                       self.axisp1y_label, self.axisp1y_input,
                                                       self.axisp1z_label, self.axisp1z_input]]

        self.third_row_layout = QtGui.QHBoxLayout()
        [self.third_row_layout.addWidget(x) for x in [self.axisp2x_label, self.axisp2x_input,
                                                      self.axisp2y_label, self.axisp2y_input,
                                                      self.axisp2z_label, self.axisp2z_input]]

        self.main_layout.addLayout(self.root_layout)
        self.main_layout.addWidget(guiutils.h_line_generator())
        [self.main_layout.addLayout(x) for x in [self.first_row_layout, self.second_row_layout,
                                                 self.third_row_layout]]

        self.setLayout(self.main_layout)
        self.fill_values(rot_file_gen)
        self._init_connections()

    def fill_values(self, rot_file_wave_gen):
        self.anglesunits_selector.setCurrentIndex(
            0 if rot_file_wave_gen.anglesunits == "degrees" else 1)
        self.duration_input.setText(str(rot_file_wave_gen.duration))
        self.filename_input.setText(str(rot_file_wave_gen.filename))
        self.axisp1x_input.setText(str(rot_file_wave_gen.axisp1[0]))
        self.axisp1y_input.setText(str(rot_file_wave_gen.axisp1[1]))
        self.axisp1z_input.setText(str(rot_file_wave_gen.axisp1[2]))
        self.axisp2x_input.setText(str(rot_file_wave_gen.axisp2[0]))
        self.axisp2y_input.setText(str(rot_file_wave_gen.axisp2[1]))
        self.axisp2z_input.setText(str(rot_file_wave_gen.axisp2[2]))

    def _init_connections(self):
        [x.textChanged.connect(self.on_change) for x in [self.duration_input, self.filename_input,
                                                         self.axisp1x_input, self.axisp1y_input, self.axisp1z_input,
                                                         self.axisp2x_input, self.axisp2y_input, self.axisp2z_input]]
        self.anglesunits_selector.currentIndexChanged.connect(self.on_change)
        self.filename_browse.clicked.connect(self.on_file_browse)

    def on_file_browse(self):
        # noinspection PyArgumentList
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self, __("Open file"), QtCore.QDir.homePath())
        self.filename_input.setText(filename)

    def on_change(self):
        self._sanitize_input()
        try:
            self.changed.emit(0, self.construct_motion_object())
        except ValueError:
            utils.debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        return RotationFileGen(parent_movement=self.parent_movement,
                               duration=float(self.duration_input.text()),
                               filename=str(self.filename_input.text()),
                               anglesunits=str(
                                   self.anglesunits_selector.currentText().lower()),
                               axisp1=[float(self.axisp1x_input.text()),
                                       float(self.axisp1y_input.text()),
                                       float(self.axisp1z_input.text())],
                               axisp2=[float(self.axisp2x_input.text()),
                                       float(self.axisp2y_input.text()),
                                       float(self.axisp2z_input.text())])

    def on_delete(self):
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        [x.setText("0")
         if len(x.text()) is 0
         else x.setText(x.text().replace(",", "."))
         for x in [self.duration_input, self.axisp1x_input, self.axisp1y_input, self.axisp1z_input,
                   self.axisp2x_input, self.axisp2y_input, self.axisp2z_input]]


class ObjectOrderWidget(QtGui.QWidget):
    """ A widget representing the object order. """

    up = QtCore.Signal(int)  # Passes element index
    down = QtCore.Signal(int)  # Passes element index

    def __init__(self, index=999, object_name="No name", object_mk=-1, mktype="bound",
                 up_disabled=False, down_disabled=False):
        super(ObjectOrderWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.index = index
        self.object_name = object_name
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.mk_label = QtGui.QLabel(
            "<b>{}{}</b>".format(mktype[0].upper(), str(object_mk)))
        self.name_label = QtGui.QLabel(str(object_name))
        self.up_button = QtGui.QPushButton(
            guiutils.get_icon("up_arrow.png"), None)
        self.up_button.clicked.connect(self.on_up)
        self.down_button = QtGui.QPushButton(
            guiutils.get_icon("down_arrow.png"), None)
        self.down_button.clicked.connect(self.on_down)

        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.up_button)
        self.main_layout.addWidget(self.down_button)

        self.up_button.setEnabled(not up_disabled)
        self.down_button.setEnabled(not down_disabled)

        self.setLayout(self.main_layout)
        self.setToolTip("MK: {} ({})\n"
                        "Name: {}\n"
                        "{}".format(object_mk, mktype.lower().title(), object_name,
                                    __("Press up or down to reorder.")))

    def disable_up(self):
        self.up_button.setEnabled(False)

    def disable_down(self):
        self.down_button.setEnabled(False)

    def on_up(self):
        self.up.emit(self.index)

    def on_down(self):
        self.down.emit(self.index)


class MovementTimelinePlaceholder(QtGui.QWidget):
    """ A placeholder for the movement timeline table. """

    def __init__(self):
        super(MovementTimelinePlaceholder, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.placeholder_layout = QtGui.QHBoxLayout()
        self.placeholder_text = QtGui.QLabel("<i>{}</i>".format(__("Select or create a "
                                                                   "movement to edit its properties")))

        self.placeholder_layout.addStretch(0.5)
        self.placeholder_layout.addWidget(self.placeholder_text)
        self.placeholder_layout.addStretch(0.5)

        self.main_layout.addStretch(0.5)
        self.main_layout.addLayout(self.placeholder_layout)
        self.main_layout.addStretch(0.5)

        self.setLayout(self.main_layout)


class InfoDialogDetails(QtGui.QDialog):
    """ A popup dialog with a text box to show details."""

    def __init__(self, text=None):
        super(InfoDialogDetails, self).__init__()
        self.setModal(False)
        self.setWindowTitle(__("Details"))
        self.main_layout = QtGui.QVBoxLayout()

        self.details_text = QtGui.QTextEdit()
        self.details_text.setReadOnly(True)
        self.main_layout.addWidget(self.details_text)

        self.details_text.setText(text)

        self.setLayout(self.main_layout)


class InfoDialog(QtGui.QDialog):
    """ An information dialog with popup details and ok button."""

    def __init__(self, info_text="", detailed_text=None):
        super(InfoDialog, self).__init__()
        self.setWindowModality(QtCore.Qt.NonModal)
        self.has_details = detailed_text is not None
        if self.has_details:
            self.details_dialog = InfoDialogDetails(detailed_text)
        self.main_layout = QtGui.QVBoxLayout()

        self.text = QtGui.QLabel(str(info_text))
        self.text.setWordWrap(True)

        if self.has_details:
            self.details_button = QtGui.QPushButton("Details")
        self.ok_button = QtGui.QPushButton("Ok")

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)
        if self.has_details:
            self.button_layout.addWidget(self.details_button)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.text)
        self.main_layout.addWidget(guiutils.h_line_generator())
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

        self.connections()
        self.show()

    def on_details_button(self):
        if self.details_dialog.isVisible():
            self.details_dialog.hide()
        else:
            self.details_dialog.show()
            self.details_dialog.move(
                self.x() - self.details_dialog.width() - 15,
                self.y() - abs(self.height() - self.details_dialog.height()) / 2)

    def on_ok_button(self):
        if self.has_details:
            self.details_dialog.hide()
        self.accept()

    def connections(self):
        if self.has_details:
            self.details_button.clicked.connect(self.on_details_button)
        self.ok_button.clicked.connect(self.on_ok_button)


class MLPiston1DConfigDialog(QtGui.QDialog):
    def __init__(self, mk=None, mlpiston1d=None):
        super(MLPiston1DConfigDialog, self).__init__()
        self.mk = mk
        self.temp_mlpiston1d = mlpiston1d if mlpiston1d is not None else MLPiston1D()
        self.mlpiston1d = mlpiston1d

        self.main_layout = QtGui.QVBoxLayout()
        self.data_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()

        self.mk_label = QtGui.QLabel(__("MK to use: {}").format(self.mk))

        self.filevelx_layout = QtGui.QHBoxLayout()
        self.filevelx_label = QtGui.QLabel(__("File with X velocity:"))
        self.filevelx_input = QtGui.QLineEdit()
        self.filevelx_browse = QtGui.QPushButton("...")

        [self.filevelx_layout.addWidget(x) for x in [
            self.filevelx_label,
            self.filevelx_input,
            self.filevelx_browse
        ]]

        self.incz_layout = QtGui.QHBoxLayout()
        self.incz_label = QtGui.QLabel(__("Z offset (m):"))
        self.incz_input = QtGui.QLineEdit()

        [self.incz_layout.addWidget(x) for x in [
            self.incz_label, self.incz_input
        ]]

        self.timedataini_layout = QtGui.QHBoxLayout()
        self.timedataini_label = QtGui.QLabel(__("Time offset (s):"))
        self.timedataini_input = QtGui.QLineEdit()

        [self.timedataini_layout.addWidget(x) for x in [
            self.timedataini_label, self.timedataini_input
        ]]

        self.smooth_layout = QtGui.QHBoxLayout()
        self.smooth_label = QtGui.QLabel(__("Smooth motion level:"))
        self.smooth_input = QtGui.QLineEdit()

        [self.smooth_layout.addWidget(x) for x in [
            self.smooth_label, self.smooth_input
        ]]

        [self.data_layout.addLayout(x) for x in [self.filevelx_layout, self.incz_layout,
                                                 self.timedataini_layout, self.smooth_layout]]

        self.delete_button = QtGui.QPushButton(__("Delete piston configuration"))
        self.apply_button = QtGui.QPushButton(__("Apply this configuration"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(guiutils.h_line_generator())
        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)

        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.filevelx_browse.clicked.connect(self.on_browse)

        self.setLayout(self.main_layout)

        self.fill_data()
        self.exec_()

    def on_apply(self):
        self.temp_mlpiston1d.filevelx = str(self.filevelx_input.text())
        self.temp_mlpiston1d.incz = float(self.incz_input.text())
        self.temp_mlpiston1d.timedataini = float(self.timedataini_input.text())
        self.temp_mlpiston1d.smooth = float(self.smooth_input.text())
        self.mlpiston1d = self.temp_mlpiston1d
        self.accept()

    def on_delete(self):
        self.mlpiston1d = None
        self.reject()

    def fill_data(self):
        self.filevelx_input.setText(str(self.temp_mlpiston1d.filevelx))
        self.incz_input.setText(str(self.temp_mlpiston1d.incz))
        self.timedataini_input.setText(str(self.temp_mlpiston1d.timedataini))
        self.smooth_input.setText(str(self.temp_mlpiston1d.smooth))
        pass

    def on_browse(self):
        # noinspection PyArgumentList
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self,
            __("Open file"),
            QtCore.QDir.homePath(),
            "External velocity data (*.csv)")
        self.filevelx_input.setText(filename)


class MLPiston2DConfigDialog(QtGui.QDialog):
    def __init__(self, mk=None, mlpiston2d=None):
        super(MLPiston2DConfigDialog, self).__init__()
        self.mk = mk
        self.temp_mlpiston2d = mlpiston2d if mlpiston2d is not None else MLPiston2D()
        self.mlpiston2d = mlpiston2d

        self.main_layout = QtGui.QVBoxLayout()
        self.data_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()

        self.mk_label = QtGui.QLabel(__("MK to use: {}").format(self.mk))

        self.incz_layout = QtGui.QHBoxLayout()
        self.incz_label = QtGui.QLabel(__("Z offset (m):"))
        self.incz_input = QtGui.QLineEdit()

        [self.incz_layout.addWidget(x) for x in [
            self.incz_label, self.incz_input
        ]]

        self.smooth_layout = QtGui.QHBoxLayout()
        self.smooth_label = QtGui.QLabel(__("Smooth motion level (Z, Y):"))
        self.smooth_z = QtGui.QLineEdit()
        self.smooth_y = QtGui.QLineEdit()

        [self.smooth_layout.addWidget(x) for x in [
            self.smooth_label, self.smooth_z, self.smooth_y
        ]]

        self.veldata_groupbox = QtGui.QGroupBox(__("Velocity data"))
        self.veldata_groupbox_layout = QtGui.QVBoxLayout()

        self.veldata_filevelx_layout = QtGui.QHBoxLayout()
        self.veldata_filevelx_label = QtGui.QLabel(__("File series"))
        self.veldata_filevelx_input = QtGui.QLineEdit()
        self.veldata_filevelx_browse = QtGui.QPushButton("...")
        [self.veldata_filevelx_layout.addWidget(x) for x in [
            self.veldata_filevelx_label, self.veldata_filevelx_input, self.veldata_filevelx_browse
        ]]

        self.veldata_files_label = QtGui.QLabel(__("No files selected"))

        self.veldata_posy_layout = QtGui.QHBoxLayout()
        self.veldata_posy_label = QtGui.QLabel(__("Y positions (separated by commas):"))
        self.veldata_posy_input = QtGui.QLineEdit()
        [self.veldata_posy_layout.addWidget(x) for x in [
            self.veldata_posy_label, self.veldata_posy_input
        ]]

        self.veldata_timedataini_layout = QtGui.QHBoxLayout()
        self.veldata_timedataini_label = QtGui.QLabel(__("Time offsets (separated by commas):"))
        self.veldata_timedataini_input = QtGui.QLineEdit()
        [self.veldata_timedataini_layout.addWidget(x) for x in [
            self.veldata_timedataini_label, self.veldata_timedataini_input
        ]]

        self.veldata_groupbox_layout.addLayout(self.veldata_filevelx_layout)
        self.veldata_groupbox_layout.addWidget(self.veldata_files_label)
        self.veldata_groupbox_layout.addLayout(self.veldata_posy_layout)
        self.veldata_groupbox_layout.addLayout(self.veldata_timedataini_layout)
        self.veldata_groupbox.setLayout(self.veldata_groupbox_layout)

        [self.data_layout.addLayout(x) for x in [
            self.incz_layout,
            self.smooth_layout,
        ]]
        self.data_layout.addWidget(self.veldata_groupbox)

        self.delete_button = QtGui.QPushButton(__("Delete piston configuration"))
        self.apply_button = QtGui.QPushButton(__("Apply this configuration"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(guiutils.h_line_generator())
        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)

        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.veldata_filevelx_browse.clicked.connect(self.on_browse)

        self.setLayout(self.main_layout)

        self.fill_data()
        self.exec_()

    def on_apply(self):
        self.temp_mlpiston2d.incz = float(self.incz_input.text())
        self.temp_mlpiston2d.smoothz = float(self.smooth_z.text())
        self.temp_mlpiston2d.smoothy = float(self.smooth_y.text())
        list_posy = self.veldata_posy_input.text().split(",")
        list_timedataini = self.veldata_timedataini_input.text().split(",")
        if len(list_posy) != len(list_timedataini) or len(self.temp_mlpiston2d.veldata) != len(list_posy) or len(
                self.temp_mlpiston2d.veldata) != len(list_timedataini):
            guiutils.error_dialog(__("Wrong number of Y positions or Time offsets. "
                                     "Introduce {} of them separated by commas").format(
                len(self.temp_mlpiston2d.veldata
                    )))
            return
        for index, value in enumerate(self.temp_mlpiston2d.veldata):
            self.temp_mlpiston2d.veldata[index].posy = list_posy[index]
            self.temp_mlpiston2d.veldata[index].timedataini = list_timedataini[index]

        self.mlpiston2d = self.temp_mlpiston2d
        self.accept()

    def on_delete(self):
        self.mlpiston2d = None
        self.reject()

    def fill_data(self):
        self.incz_input.setText(str(self.temp_mlpiston2d.incz))
        self.smooth_z.setText(str(self.temp_mlpiston2d.smoothz))
        self.smooth_y.setText(str(self.temp_mlpiston2d.smoothy))
        if len(self.temp_mlpiston2d.veldata) > 0:
            self.veldata_files_label.setText(__("The serie has {} files").format(len(self.temp_mlpiston2d.veldata)))
            self.veldata_filevelx_input.setText(self.temp_mlpiston2d.veldata[0].filevelx.split("_x")[0])
            self.veldata_posy_input.setText(",".join([str(x.posy) for x in self.temp_mlpiston2d.veldata]))
            self.veldata_timedataini_input.setText(",".join([str(x.timedataini) for x in self.temp_mlpiston2d.veldata]))
        else:
            self.veldata_files_label.setText(__("No files selected"))
            self.veldata_filevelx_input.setText("None")
            self.veldata_posy_input.setText("")
            self.veldata_timedataini_input.setText("")

    def on_browse(self):
        # noinspection PyArgumentList
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            self,
            __("Open a file from the serie"),
            QtCore.QDir.homePath(),
            "External velocity data (*_x*_y*.csv)")
        if len(filename) < 1:
            return
        filename_filtered = filename.split("_x")[0]
        self.veldata_filevelx_input.setText(str(filename_filtered))
        serie_filenames = glob.glob("{}*.csv".format(filename_filtered))
        self.temp_mlpiston2d.veldata = list()
        for serie_filename in serie_filenames:
            serie_filename = serie_filename.replace("\\", "/")
            self.temp_mlpiston2d.veldata.append(MLPiston2DVeldata(serie_filename, 0, 0))
        self.veldata_files_label.setText(__("The serie has {} files").format(len(self.temp_mlpiston2d.veldata)))
        self.veldata_posy_input.setText(",".join([str(x.posy) for x in self.temp_mlpiston2d.veldata]))
        self.veldata_timedataini_input.setText(",".join([str(x.timedataini) for x in self.temp_mlpiston2d.veldata]))


class RelaxationZoneRegularConfigDialog(QtGui.QDialog):
    def __init__(self, relaxationzone=None):
        super(RelaxationZoneRegularConfigDialog, self).__init__()
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneRegular()
        self.relaxationzone = relaxationzone

        self.main_layout = QtGui.QVBoxLayout()
        self.data_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()

        self.start_layout = QtGui.QHBoxLayout()
        self.start_label = QtGui.QLabel(__("Start time (s):"))
        self.start_input = QtGui.QLineEdit()
        [self.start_layout.addWidget(x) for x in [self.start_label, self.start_input]]

        self.duration_layout = QtGui.QHBoxLayout()
        self.duration_label = QtGui.QLabel(__("Movement duration (0 for end of simulation):"))
        self.duration_input = QtGui.QLineEdit()
        [self.duration_layout.addWidget(x) for x in [self.duration_label, self.duration_input]]

        self.waveorder_layout = QtGui.QHBoxLayout()
        self.waveorder_label = QtGui.QLabel(__("Order wave generation:"))
        self.waveorder_input = QtGui.QLineEdit()
        [self.waveorder_layout.addWidget(x) for x in [self.waveorder_label, self.waveorder_input]]

        self.waveheight_layout = QtGui.QHBoxLayout()
        self.waveheight_label = QtGui.QLabel(__("Wave Height:"))
        self.waveheight_input = QtGui.QLineEdit()
        [self.waveheight_layout.addWidget(x) for x in [self.waveheight_label, self.waveheight_input]]

        self.waveperiod_layout = QtGui.QHBoxLayout()
        self.waveperiod_label = QtGui.QLabel(__("Wave Period:"))
        self.waveperiod_input = QtGui.QLineEdit()
        [self.waveperiod_layout.addWidget(x) for x in [self.waveperiod_label, self.waveperiod_input]]

        self.depth_layout = QtGui.QHBoxLayout()
        self.depth_label = QtGui.QLabel(__("Water depth:"))
        self.depth_input = QtGui.QLineEdit()
        [self.depth_layout.addWidget(x) for x in [self.depth_label, self.depth_input]]

        self.swl_layout = QtGui.QHBoxLayout()
        self.swl_label = QtGui.QLabel(__("Still water level:"))
        self.swl_input = QtGui.QLineEdit()
        [self.swl_layout.addWidget(x) for x in [self.swl_label, self.swl_input]]

        self.center_layout = QtGui.QHBoxLayout()
        self.center_label = QtGui.QLabel(__("Central point (X, Y, Z):"))
        self.center_x = QtGui.QLineEdit()
        self.center_y = QtGui.QLineEdit()
        self.center_z = QtGui.QLineEdit()
        [self.center_layout.addWidget(x) for x in [self.center_label, self.center_x, self.center_y, self.center_z]]

        self.width_layout = QtGui.QHBoxLayout()
        self.width_label = QtGui.QLabel(__("Width for generation:"))
        self.width_input = QtGui.QLineEdit()
        [self.width_layout.addWidget(x) for x in [self.width_label, self.width_input]]

        self.phase_layout = QtGui.QHBoxLayout()
        self.phase_label = QtGui.QLabel(__("Initial wave phase:"))
        self.phase_input = QtGui.QLineEdit()
        [self.phase_layout.addWidget(x) for x in [self.phase_label, self.phase_input]]

        self.ramp_layout = QtGui.QHBoxLayout()
        self.ramp_label = QtGui.QLabel(__("Periods of ramp:"))
        self.ramp_input = QtGui.QLineEdit()
        [self.ramp_layout.addWidget(x) for x in [self.ramp_label, self.ramp_input]]

        self.savemotion_layout = QtGui.QHBoxLayout()
        self.savemotion_label = QtGui.QLabel(__("Save motion data ->"))
        self.savemotion_periods_label = QtGui.QLabel(__("Periods: "))
        self.savemotion_periods_input = QtGui.QLineEdit()
        self.savemotion_periodsteps_label = QtGui.QLabel(__("Period steps: "))
        self.savemotion_periodsteps_input = QtGui.QLineEdit()
        self.savemotion_xpos_label = QtGui.QLabel(__("X Position: "))
        self.savemotion_xpos_input = QtGui.QLineEdit()
        self.savemotion_zpos_label = QtGui.QLabel(__("Z Position: "))
        self.savemotion_zpos_input = QtGui.QLineEdit()
        [self.savemotion_layout.addWidget(x) for x in [
            self.savemotion_label,
            self.savemotion_periods_label,
            self.savemotion_periods_input,
            self.savemotion_periodsteps_label,
            self.savemotion_periodsteps_input,
            self.savemotion_xpos_label,
            self.savemotion_xpos_input,
            self.savemotion_zpos_label,
            self.savemotion_zpos_input
        ]]

        self.coefdir_layout = QtGui.QHBoxLayout()
        self.coefdir_label = QtGui.QLabel(__("Coefficient for each direction (X, Y, Z):"))
        self.coefdir_x = QtGui.QLineEdit()
        self.coefdir_x.setEnabled(False)
        self.coefdir_y = QtGui.QLineEdit()
        self.coefdir_y.setEnabled(False)
        self.coefdir_z = QtGui.QLineEdit()
        self.coefdir_z.setEnabled(False)
        [self.coefdir_layout.addWidget(x) for x in [self.coefdir_label, self.coefdir_x, self.coefdir_y, self.coefdir_z]]

        self.coefdt_layout = QtGui.QHBoxLayout()
        self.coefdt_label = QtGui.QLabel(__("Multiplier for dt value in each direction:"))
        self.coefdt_input = QtGui.QLineEdit()
        self.coefdt_input.setEnabled(False)
        [self.coefdt_layout.addWidget(x) for x in [self.coefdt_label, self.coefdt_input]]

        self.function_layout = QtGui.QHBoxLayout()
        self.function_label = QtGui.QLabel(__("Coefficients in function for velocity ->"))
        self.function_psi_label = QtGui.QLabel(__("Psi: "))
        self.function_psi_input = QtGui.QLineEdit()
        self.function_beta_label = QtGui.QLabel(__("Beta: "))
        self.function_beta_input = QtGui.QLineEdit()
        [self.function_layout.addWidget(x) for x in [
            self.function_label,
            self.function_psi_label,
            self.function_psi_input,
            self.function_beta_label,
            self.function_beta_input
        ]]

        self.driftcorrection_layout = QtGui.QHBoxLayout()
        self.driftcorrection_label = QtGui.QLabel(__("Coefficient of drift correction (for X):"))
        self.driftcorrection_input = QtGui.QLineEdit()
        [self.driftcorrection_layout.addWidget(x) for x in [self.driftcorrection_label, self.driftcorrection_input]]

        [self.data_layout.addLayout(x) for x in [
            self.start_layout,
            self.duration_layout,
            self.waveorder_layout,
            self.waveheight_layout,
            self.waveperiod_layout,
            self.depth_layout,
            self.swl_layout,
            self.center_layout,
            self.width_layout,
            self.phase_layout,
            self.ramp_layout,
            self.savemotion_layout,
            self.coefdir_layout,
            self.coefdt_layout,
            self.function_layout,
            self.driftcorrection_layout
        ]]

        self.delete_button = QtGui.QPushButton(__("Delete RZ configuration"))
        self.apply_button = QtGui.QPushButton(__("Apply this configuration"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)
        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_apply(self):
        self.temp_relaxationzone.start = float(self.start_input.text())
        self.temp_relaxationzone.duration = float(self.duration_input.text())
        self.temp_relaxationzone.waveorder = float(self.waveorder_input.text())
        self.temp_relaxationzone.waveheight = float(self.waveheight_input.text())
        self.temp_relaxationzone.waveperiod = float(self.waveperiod_input.text())
        self.temp_relaxationzone.depth = float(self.depth_input.text())
        self.temp_relaxationzone.swl = float(self.swl_input.text())
        self.temp_relaxationzone.center[0] = float(self.center_x.text())
        self.temp_relaxationzone.center[1] = float(self.center_y.text())
        self.temp_relaxationzone.center[2] = float(self.center_z.text())
        self.temp_relaxationzone.width = float(self.width_input.text())
        self.temp_relaxationzone.phase = float(self.phase_input.text())
        self.temp_relaxationzone.ramp = float(self.ramp_input.text())
        self.temp_relaxationzone.savemotion_periods = float(self.savemotion_periods_input.text())
        self.temp_relaxationzone.savemotion_periodsteps = float(self.savemotion_periodsteps_input.text())
        self.temp_relaxationzone.savemotion_xpos = float(self.savemotion_xpos_input.text())
        self.temp_relaxationzone.savemotion_zpos = float(self.savemotion_zpos_input.text())
        self.temp_relaxationzone.coefdir[0] = float(self.coefdir_x.text())
        self.temp_relaxationzone.coefdir[1] = float(self.coefdir_y.text())
        self.temp_relaxationzone.coefdir[2] = float(self.coefdir_z.text())
        self.temp_relaxationzone.coefdt = float(self.coefdt_input.text())
        self.temp_relaxationzone.function_psi = float(self.function_psi_input.text())
        self.temp_relaxationzone.function_beta = float(self.function_beta_input.text())
        self.temp_relaxationzone.driftcorrection = float(self.driftcorrection_input.text())
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        self.relaxationzone = None
        self.reject()

    def fill_data(self):
        self.start_input.setText(str(self.temp_relaxationzone.start))
        self.duration_input.setText(str(self.temp_relaxationzone.duration))
        self.waveorder_input.setText(str(self.temp_relaxationzone.waveorder))
        self.waveheight_input.setText(str(self.temp_relaxationzone.waveheight))
        self.waveperiod_input.setText(str(self.temp_relaxationzone.waveperiod))
        self.depth_input.setText(str(self.temp_relaxationzone.depth))
        self.swl_input.setText(str(self.temp_relaxationzone.swl))
        self.center_x.setText(str(self.temp_relaxationzone.center[0]))
        self.center_y.setText(str(self.temp_relaxationzone.center[1]))
        self.center_z.setText(str(self.temp_relaxationzone.center[2]))
        self.width_input.setText(str(self.temp_relaxationzone.width))
        self.phase_input.setText(str(self.temp_relaxationzone.phase))
        self.ramp_input.setText(str(self.temp_relaxationzone.ramp))
        self.savemotion_periods_input.setText(str(self.temp_relaxationzone.savemotion_periods))
        self.savemotion_periodsteps_input.setText(str(self.temp_relaxationzone.savemotion_periodsteps))
        self.savemotion_xpos_input.setText(str(self.temp_relaxationzone.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(self.temp_relaxationzone.savemotion_zpos))
        self.coefdir_x.setText(str(self.temp_relaxationzone.coefdir[0]))
        self.coefdir_y.setText(str(self.temp_relaxationzone.coefdir[1]))
        self.coefdir_z.setText(str(self.temp_relaxationzone.coefdir[2]))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))
        self.driftcorrection_input.setText(str(self.temp_relaxationzone.driftcorrection))
