#!/usr/bin/env python3.7
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
import uuid
import shutil
import glob

import sys

from ds_modules import utils
from ds_modules.utils import __
from ds_modules import guiutils
from ds_modules import properties
from ds_modules.properties import *
from ds_modules import constants
from ds_modules import execution_parameters
from ds_modules.execution_parameters import *


# Copyright (C) 2019
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

    changed = QtCore.Signal(int, properties.RectMotion)
    deleted = QtCore.Signal(int, properties.RectMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, rect_motion):
        if not isinstance(rect_motion, properties.RectMotion):
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
        return properties.RectMotion(
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

    changed = QtCore.Signal(int, properties.WaitMotion)
    deleted = QtCore.Signal(int, properties.WaitMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, wait_motion):
        if not isinstance(wait_motion, properties.WaitMotion):
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
        self.time_label = QtGui.QLabel(utils.__("Duration (s): "))
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
        return properties.WaitMotion(duration=float(self.time_input.text()), parent_movement=self.parent_movement)

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

    changed = QtCore.Signal(int, properties.RegularPistonWaveGen)

    def __init__(self, reg_wave_gen):
        if not isinstance(reg_wave_gen, properties.RegularPistonWaveGen):
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
                                                      self.depth_label, self.depth_input]]

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
        [x.textChanged.connect(self.on_change) for x in [self.duration_input, self.depth_input, self.piston_dir_x,
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

        return properties.RegularPistonWaveGen(parent_movement=self.parent_movement,
                                    wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                    duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
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
         for x in [self.duration_input, self.depth_input, self.piston_dir_x,
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
    changed = QtCore.Signal(int, properties.IrregularPistonWaveGen)

    def __init__(self, irreg_wave_gen):
        if not isinstance(irreg_wave_gen, properties.IrregularPistonWaveGen):
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
                                                      self.depth_label, self.depth_input]]

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
                                                         self.depth_input, self.piston_dir_x,
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

        return properties.IrregularPistonWaveGen(parent_movement=self.parent_movement,
                                      wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                      duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
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
         for x in [self.duration_input, self.depth_input, self.piston_dir_x,
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
    changed = QtCore.Signal(int, properties.RegularFlapWaveGen)

    def __init__(self, reg_wave_gen):
        if not isinstance(reg_wave_gen, properties.RegularFlapWaveGen):
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
                                                      self.depth_label, self.depth_input]]

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
        return properties.RegularFlapWaveGen(parent_movement=self.parent_movement,
                                  wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                  duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
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
         for x in [self.duration_input, self.depth_input, self.flap_axis_0_x,
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
    changed = QtCore.Signal(int, properties.IrregularFlapWaveGen)

    def __init__(self, irreg_wave_gen):
        if not isinstance(irreg_wave_gen, properties.IrregularFlapWaveGen):
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
                                                      self.depth_label, self.depth_input]]

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
                                                         self.depth_input, self.flap_axis_0_x,
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
        return properties.IrregularFlapWaveGen(parent_movement=self.parent_movement,
                                    wave_order=self.wave_order_selector.currentIndex() + 1, start=0,
                                    duration=float(self.duration_input.text()), depth=float(self.depth_input.text()),
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
         for x in [self.duration_input, self.depth_input, self.flap_axis_0_x,
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
    changed = QtCore.Signal(int, properties.FileGen)

    def __init__(self, file_wave_gen, project_folder_path):
        if not isinstance(file_wave_gen, properties.FileGen):
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
        return properties.FileGen(parent_movement=self.parent_movement,
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
    changed = QtCore.Signal(int, properties.RotationFileGen)

    def __init__(self, rot_file_gen, project_folder_path):
        if not isinstance(rot_file_gen, properties.RotationFileGen):
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
        return properties.RotationFileGen(parent_movement=self.parent_movement,
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


class ObjectIsCheked(QtGui.QWidget):
    """ Widget shows check options for an object """

    def __init__(self, key, object_name="No name", object_mk=-1, mktype="bound", is_floating=""):
        super(ObjectIsCheked, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.key = key
        self.object_name = object_name
        self.object_mk = object_mk
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.mk_label = QtGui.QLabel(
            "<b>{}{}</b>".format(mktype[0].upper(), str(object_mk)))
        self.name_label = QtGui.QLabel(str(object_name))
        self.is_floating = is_floating
        self.object_check = QtGui.QCheckBox()
        self.geometry_check = QtGui.QCheckBox(__("Geometry"))
        self.modelnormal_input = QtGui.QComboBox()
        self.modelnormal_input.insertItems(0, ['Original', 'Invert', 'Two face'])

        self.main_layout.addWidget(self.object_check)
        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.geometry_check)
        self.main_layout.addWidget(self.modelnormal_input)

        self.setLayout(self.main_layout)


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
        self.setMinimumWidth(650)
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


class RelaxationZoneIrregularConfigDialog(QtGui.QDialog):
    def __init__(self, relaxationzone=None):
        super(RelaxationZoneIrregularConfigDialog, self).__init__()
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneIrregular()
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

        self.peakcoef_layout = QtGui.QHBoxLayout()
        self.peakcoef_label = QtGui.QLabel(__("Peak enhancement coefficient:"))
        self.peakcoef_input = QtGui.QLineEdit()
        [self.peakcoef_layout.addWidget(x) for x in [self.peakcoef_label, self.peakcoef_input]]

        self.spectrum_layout = QtGui.QHBoxLayout()
        self.spectrum_label = QtGui.QLabel(__("Spectrum type:"))
        self.spectrum_selector = QtGui.QComboBox()
        self.spectrum_selector.insertItems(
            0, [__("Jonswap"), __("Pierson-Moskowitz")])
        [self.spectrum_layout.addWidget(x) for x in [self.spectrum_label, self.spectrum_selector]]

        self.discretization_layout = QtGui.QHBoxLayout()
        self.discretization_label = QtGui.QLabel(__("Spectrum discretization:"))
        self.discretization_selector = QtGui.QComboBox()
        self.discretization_selector.insertItems(
            0, [__("Regular"), __("Random"), __("Stretched"), __("Cosstretched")])
        [self.discretization_layout.addWidget(x) for x in [self.discretization_label, self.discretization_selector]]

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

        self.waves_layout = QtGui.QHBoxLayout()
        self.waves_label = QtGui.QLabel(__("Number of waves:"))
        self.waves_input = QtGui.QLineEdit()
        [self.waves_layout.addWidget(x) for x in [self.waves_label, self.waves_input]]

        self.randomseed_layout = QtGui.QHBoxLayout()
        self.randomseed_label = QtGui.QLabel(__("Random seed:"))
        self.randomseed_input = QtGui.QLineEdit()
        [self.randomseed_layout.addWidget(x) for x in [self.randomseed_label, self.randomseed_input]]

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

        self.ramptime_layout = QtGui.QHBoxLayout()
        self.ramptime_label = QtGui.QLabel(__("Time of initial ramp:"))
        self.ramptime_input = QtGui.QLineEdit()
        [self.ramptime_layout.addWidget(x) for x in [self.ramptime_label, self.ramptime_input]]

        self.serieini_layout = QtGui.QHBoxLayout()
        self.serieini_label = QtGui.QLabel(__("Initial time:"))
        self.serieini_input = QtGui.QLineEdit()
        [self.serieini_layout.addWidget(x) for x in [self.serieini_label, self.serieini_input]]

        self.savemotion_layout = QtGui.QHBoxLayout()
        self.savemotion_label = QtGui.QLabel(__("Save motion data ->"))
        self.savemotion_time_label = QtGui.QLabel(__("Time: "))
        self.savemotion_time_input = QtGui.QLineEdit()
        self.savemotion_timedt_label = QtGui.QLabel(__("Time data: "))
        self.savemotion_timedt_input = QtGui.QLineEdit()
        self.savemotion_xpos_label = QtGui.QLabel(__("X Position: "))
        self.savemotion_xpos_input = QtGui.QLineEdit()
        self.savemotion_zpos_label = QtGui.QLabel(__("Z Position: "))
        self.savemotion_zpos_input = QtGui.QLineEdit()
        [self.savemotion_layout.addWidget(x) for x in [
            self.savemotion_label,
            self.savemotion_time_label,
            self.savemotion_time_input,
            self.savemotion_timedt_label,
            self.savemotion_timedt_input,
            self.savemotion_xpos_label,
            self.savemotion_xpos_input,
            self.savemotion_zpos_label,
            self.savemotion_zpos_input
        ]]

        self.saveserie_layout = QtGui.QHBoxLayout()
        self.saveserie_label = QtGui.QLabel(__("Save serie data ->"))
        self.saveserie_timemin_label = QtGui.QLabel(__("Time min.: "))
        self.saveserie_timemin_input = QtGui.QLineEdit()
        self.saveserie_timemax_label = QtGui.QLabel(__("Time max.: "))
        self.saveserie_timemax_input = QtGui.QLineEdit()
        self.saveserie_timedt_label = QtGui.QLabel(__("Time max.: "))
        self.saveserie_timedt_input = QtGui.QLineEdit()
        self.saveserie_xpos_label = QtGui.QLabel(__("X Position: "))
        self.saveserie_xpos_input = QtGui.QLineEdit()
        [self.saveserie_layout.addWidget(x) for x in [
            self.saveserie_label,
            self.saveserie_timemin_label,
            self.saveserie_timemin_input,
            self.saveserie_timemax_label,
            self.saveserie_timemax_input,
            self.saveserie_timedt_label,
            self.saveserie_timedt_input,
            self.saveserie_xpos_label,
            self.saveserie_xpos_input
        ]]

        self.saveseriewaves_layout = QtGui.QHBoxLayout()
        self.saveseriewaves_label = QtGui.QLabel(__("Save serie heights ->"))
        self.saveseriewaves_timemin_label = QtGui.QLabel(__("Time min.: "))
        self.saveseriewaves_timemin_input = QtGui.QLineEdit()
        self.saveseriewaves_timemax_label = QtGui.QLabel(__("Time max.: "))
        self.saveseriewaves_timemax_input = QtGui.QLineEdit()
        self.saveseriewaves_xpos_label = QtGui.QLabel(__("X Position: "))
        self.saveseriewaves_xpos_input = QtGui.QLineEdit()
        [self.saveseriewaves_layout.addWidget(x) for x in [
            self.saveseriewaves_label,
            self.saveseriewaves_timemin_label,
            self.saveseriewaves_timemin_input,
            self.saveseriewaves_timemax_label,
            self.saveseriewaves_timemax_input,
            self.saveseriewaves_xpos_label,
            self.saveseriewaves_xpos_input
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
            self.peakcoef_layout,
            self.spectrum_layout,
            self.discretization_layout,
            self.waveorder_layout,
            self.waveheight_layout,
            self.waveperiod_layout,
            self.waves_layout,
            self.randomseed_layout,
            self.depth_layout,
            self.swl_layout,
            self.center_layout,
            self.width_layout,
            self.ramptime_layout,
            self.savemotion_layout,
            self.saveserie_layout,
            self.saveseriewaves_layout,
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
        self.temp_relaxationzone.peakcoef = float(self.peakcoef_input.text())
        self.temp_relaxationzone.spectrum = self.spectrum_selector.currentIndex()
        self.temp_relaxationzone.discretization = self.discretization_selector.currentIndex()
        self.temp_relaxationzone.waveorder = float(self.waveorder_input.text())
        self.temp_relaxationzone.waveheight = float(self.waveheight_input.text())
        self.temp_relaxationzone.waveperiod = float(self.waveperiod_input.text())
        self.temp_relaxationzone.waves = float(self.waves_input.text())
        self.temp_relaxationzone.randomseed = float(self.waveperiod_input.text())
        self.temp_relaxationzone.depth = float(self.depth_input.text())
        self.temp_relaxationzone.swl = float(self.swl_input.text())
        self.temp_relaxationzone.center[0] = float(self.center_x.text())
        self.temp_relaxationzone.center[1] = float(self.center_y.text())
        self.temp_relaxationzone.center[2] = float(self.center_z.text())
        self.temp_relaxationzone.width = float(self.width_input.text())
        self.temp_relaxationzone.ramptime = float(self.ramptime_input.text())
        self.temp_relaxationzone.serieini = float(self.serieini_input.text())
        self.temp_relaxationzone.savemotion_time = float(self.savemotion_time_input.text())
        self.temp_relaxationzone.savemotion_timedt = float(self.savemotion_timedt_input.text())
        self.temp_relaxationzone.savemotion_xpos = float(self.savemotion_xpos_input.text())
        self.temp_relaxationzone.savemotion_zpos = float(self.savemotion_zpos_input.text())
        self.temp_relaxationzone.saveserie_timemin = float(self.saveserie_timemin_input.text())
        self.temp_relaxationzone.saveserie_timemax = float(self.saveserie_timemax_input.text())
        self.temp_relaxationzone.saveserie_timedt = float(self.saveserie_timedt_input.text())
        self.temp_relaxationzone.saveserie_xpos = float(self.saveserie_xpos_input.text())
        self.temp_relaxationzone.saveseriewaves_timemin = float(self.saveseriewaves_timemin_input.text())
        self.temp_relaxationzone.saveseriewaves_timemax = float(self.saveseriewaves_timemax_input.text())
        self.temp_relaxationzone.saveseriewaves_xpos = float(self.saveseriewaves_xpos_input.text())
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
        self.peakcoef_input.setText(str(self.temp_relaxationzone.peakcoef))
        self.spectrum_selector.setCurrentIndex(self.temp_relaxationzone.spectrum)
        self.discretization_selector.setCurrentIndex(self.temp_relaxationzone.discretization)
        self.waveorder_input.setText(str(self.temp_relaxationzone.waveorder))
        self.waveheight_input.setText(str(self.temp_relaxationzone.waveheight))
        self.waveperiod_input.setText(str(self.temp_relaxationzone.waveperiod))
        self.waves_input.setText(str(self.temp_relaxationzone.waves))
        self.randomseed_input.setText(str(self.temp_relaxationzone.randomseed))
        self.depth_input.setText(str(self.temp_relaxationzone.depth))
        self.swl_input.setText(str(self.temp_relaxationzone.swl))
        self.center_x.setText(str(self.temp_relaxationzone.center[0]))
        self.center_y.setText(str(self.temp_relaxationzone.center[1]))
        self.center_z.setText(str(self.temp_relaxationzone.center[2]))
        self.width_input.setText(str(self.temp_relaxationzone.width))
        self.ramptime_input.setText(str(self.temp_relaxationzone.ramptime))
        self.serieini_input.setText(str(self.temp_relaxationzone.serieini))
        self.savemotion_time_input.setText(str(self.temp_relaxationzone.savemotion_time))
        self.savemotion_timedt_input.setText(str(self.temp_relaxationzone.savemotion_timedt))
        self.savemotion_xpos_input.setText(str(self.temp_relaxationzone.savemotion_xpos))
        self.savemotion_zpos_input.setText(str(self.temp_relaxationzone.savemotion_zpos))
        self.saveserie_timemin_input.setText(str(self.temp_relaxationzone.saveserie_timemin))
        self.saveserie_timemax_input.setText(str(self.temp_relaxationzone.saveserie_timemax))
        self.saveserie_timedt_input.setText(str(self.temp_relaxationzone.saveserie_timedt))
        self.saveserie_xpos_input.setText(str(self.temp_relaxationzone.saveserie_xpos))
        self.saveseriewaves_timemin_input.setText(str(self.temp_relaxationzone.saveseriewaves_timemin))
        self.saveseriewaves_timemax_input.setText(str(self.temp_relaxationzone.saveseriewaves_timemax))
        self.saveseriewaves_xpos_input.setText(str(self.temp_relaxationzone.saveseriewaves_xpos))
        self.coefdir_x.setText(str(self.temp_relaxationzone.coefdir[0]))
        self.coefdir_y.setText(str(self.temp_relaxationzone.coefdir[1]))
        self.coefdir_z.setText(str(self.temp_relaxationzone.coefdir[2]))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))
        self.driftcorrection_input.setText(str(self.temp_relaxationzone.driftcorrection))


class RelaxationZoneFileConfigDialog(QtGui.QDialog):
    def __init__(self, relaxationzone=None):
        super(RelaxationZoneFileConfigDialog, self).__init__()
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneFile()
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

        self.depth_layout = QtGui.QHBoxLayout()
        self.depth_label = QtGui.QLabel(__("Water depth:"))
        self.depth_input = QtGui.QLineEdit()
        [self.depth_layout.addWidget(x) for x in [self.depth_label, self.depth_input]]

        self.swl_layout = QtGui.QHBoxLayout()
        self.swl_label = QtGui.QLabel(__("Still water level:"))
        self.swl_input = QtGui.QLineEdit()
        [self.swl_layout.addWidget(x) for x in [self.swl_label, self.swl_input]]

        self.filesvel_layout = QtGui.QHBoxLayout()
        self.filesvel_label = QtGui.QLabel(__("Name of the file with velocity to use:"))
        self.filesvel_input = QtGui.QLineEdit()
        self.filesvel_browse = QtGui.QPushButton("...")
        [self.filesvel_layout.addWidget(x) for x in [self.filesvel_label, self.filesvel_input, self.filesvel_browse]]

        self.filesvelx_initial_layout = QtGui.QHBoxLayout()
        self.filesvelx_initial_label = QtGui.QLabel(__("First file:"))
        self.filesvelx_initial_input = QtGui.QLineEdit()
        [self.filesvelx_initial_layout.addWidget(x) for x in
         [self.filesvelx_initial_label, self.filesvelx_initial_input]]

        self.filesvelx_count_layout = QtGui.QHBoxLayout()
        self.filesvelx_count_label = QtGui.QLabel(__("File count:"))
        self.filesvelx_count_input = QtGui.QLineEdit()
        [self.filesvelx_count_layout.addWidget(x) for x in [self.filesvelx_count_label, self.filesvelx_count_input]]

        self.usevelz_check = QtGui.QCheckBox(__("Use velocity in Z"))

        self.movedata_layout = QtGui.QHBoxLayout()
        self.movedata_label = QtGui.QLabel(__("Movement of data in CSV files (X, Y, Z):"))
        self.movedata_x = QtGui.QLineEdit()
        self.movedata_y = QtGui.QLineEdit()
        self.movedata_z = QtGui.QLineEdit()
        [self.movedata_layout.addWidget(x) for x in
         [self.movedata_label, self.movedata_x, self.movedata_y, self.movedata_z]]

        self.dpz_layout = QtGui.QHBoxLayout()
        self.dpz_label = QtGui.QLabel(__("Distance between key points in Z (dp):"))
        self.dpz_input = QtGui.QLineEdit()
        [self.dpz_layout.addWidget(x) for x in [self.dpz_label, self.dpz_input]]

        self.smooth_layout = QtGui.QHBoxLayout()
        self.smooth_label = QtGui.QLabel(__("Smooth motion level:"))
        self.smooth_input = QtGui.QLineEdit()
        [self.smooth_layout.addWidget(x) for x in [self.smooth_label, self.smooth_input]]

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

        self.driftinitialramp_layout = QtGui.QHBoxLayout()
        self.driftinitialramp_label = QtGui.QLabel(__("Time to ignore waves from external data (s):"))
        self.driftinitialramp_input = QtGui.QLineEdit()
        [self.driftinitialramp_layout.addWidget(x) for x in [self.driftinitialramp_label, self.driftinitialramp_input]]

        [self.data_layout.addLayout(x) for x in [
            self.start_layout,
            self.duration_layout,
            self.depth_layout,
            self.swl_layout,
            self.filesvel_layout,
            self.filesvelx_initial_layout,
            self.filesvelx_count_layout
        ]]
        self.data_layout.addWidget(self.usevelz_check)
        [self.data_layout.addLayout(x) for x in [
            self.movedata_layout,
            self.dpz_layout,
            self.smooth_layout,
            self.center_layout,
            self.width_layout,
            self.coefdir_layout,
            self.coefdt_layout,
            self.function_layout,
            self.driftcorrection_layout,
            self.driftinitialramp_layout
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
        self.filesvel_browse.clicked.connect(self.on_browse)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.exec_()

    def on_browse(self):
        # noinspection PyArgumentList
        file_name, _ = QtGui.QFileDialog.getOpenFileName(
            self,
            __("Open a file from the serie"),
            QtCore.QDir.homePath(),
            "External velocity data (*_x*_y*.csv)")
        if len(file_name) < 1:
            return
        # Takes only the filename without the serie data in its name
        filtered_filename = file_name.split("_v")[0]
        self.filesvel_input.setText(filtered_filename)

    def on_apply(self):
        self.temp_relaxationzone.start = float(self.start_input.text())
        self.temp_relaxationzone.duration = float(self.duration_input.text())
        self.temp_relaxationzone.depth = float(self.depth_input.text())
        self.temp_relaxationzone.swl = float(self.swl_input.text())
        self.temp_relaxationzone.filesvel = str(self.filesvel_input.text())
        self.temp_relaxationzone.filesvelx_initial = int(self.filesvelx_initial_input.text())
        self.temp_relaxationzone.filesvelx_count = int(self.filesvelx_count_input.text())
        self.temp_relaxationzone.usevelz = bool(self.usevelz_check.isChecked())
        self.temp_relaxationzone.movedata[0] = float(self.movedata_x.text())
        self.temp_relaxationzone.movedata[1] = float(self.movedata_y.text())
        self.temp_relaxationzone.movedata[2] = float(self.movedata_z.text())
        self.temp_relaxationzone.dpz = float(self.dpz_input.text())
        self.temp_relaxationzone.smooth = float(self.smooth_input.text())
        self.temp_relaxationzone.center[0] = float(self.center_x.text())
        self.temp_relaxationzone.center[1] = float(self.center_y.text())
        self.temp_relaxationzone.center[2] = float(self.center_z.text())
        self.temp_relaxationzone.width = float(self.width_input.text())
        self.temp_relaxationzone.coefdir[0] = float(self.coefdir_x.text())
        self.temp_relaxationzone.coefdir[1] = float(self.coefdir_y.text())
        self.temp_relaxationzone.coefdir[2] = float(self.coefdir_z.text())
        self.temp_relaxationzone.coefdt = float(self.coefdt_input.text())
        self.temp_relaxationzone.function_psi = float(self.function_psi_input.text())
        self.temp_relaxationzone.function_beta = float(self.function_beta_input.text())
        self.temp_relaxationzone.driftcorrection = float(self.driftcorrection_input.text())
        self.temp_relaxationzone.driftinitialramp = float(self.driftinitialramp_input.text())
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        self.relaxationzone = None
        self.reject()

    def fill_data(self):
        self.start_input.setText(str(self.temp_relaxationzone.start))
        self.duration_input.setText(str(self.temp_relaxationzone.duration))
        self.depth_input.setText(str(self.temp_relaxationzone.depth))
        self.swl_input.setText(str(self.temp_relaxationzone.swl))
        self.filesvel_input.setText(str(self.temp_relaxationzone.filesvel))
        self.filesvelx_initial_input.setText(str(self.temp_relaxationzone.filesvelx_initial))
        self.filesvelx_count_input.setText(str(self.temp_relaxationzone.filesvelx_count))
        self.usevelz_check.setChecked(bool(self.temp_relaxationzone.usevelz))
        self.movedata_x.setText(str(self.temp_relaxationzone.movedata[0]))
        self.movedata_y.setText(str(self.temp_relaxationzone.movedata[1]))
        self.movedata_z.setText(str(self.temp_relaxationzone.movedata[2]))
        self.dpz_input.setText(str(self.temp_relaxationzone.dpz))
        self.smooth_input.setText(str(self.temp_relaxationzone.smooth))
        self.center_x.setText(str(self.temp_relaxationzone.center[0]))
        self.center_y.setText(str(self.temp_relaxationzone.center[1]))
        self.center_z.setText(str(self.temp_relaxationzone.center[2]))
        self.width_input.setText(str(self.temp_relaxationzone.width))
        self.coefdir_x.setText(str(self.temp_relaxationzone.coefdir[0]))
        self.coefdir_y.setText(str(self.temp_relaxationzone.coefdir[1]))
        self.coefdir_z.setText(str(self.temp_relaxationzone.coefdir[2]))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))
        self.driftcorrection_input.setText(str(self.temp_relaxationzone.driftcorrection))
        self.driftinitialramp_input.setText(str(self.temp_relaxationzone.driftinitialramp))


class AccelerationInputDialog(QtGui.QDialog):
    """ A Dialog which shows the contents of the case AccelerationInput object.
    Shows a list with the AccelerationInputData objects defined for the case and
    its details when clicked.
    Returns: AccelerationInput object"""

    def __init__(self, accinput):
        super(AccelerationInputDialog, self).__init__()
        self.accinput = accinput
        self.setWindowTitle(__("Acceleration Input List"))

        self.main_layout = QtGui.QVBoxLayout()

        self.enabled_check = QtGui.QCheckBox(__("Enabled"))

        self.accinput_layout = QtGui.QHBoxLayout()

        self.accinput_list_groupbox = QtGui.QGroupBox(__("Acceleration Input list"))
        self.accinput_list_layout = QtGui.QVBoxLayout()
        self.accinput_list = QtGui.QListWidget()
        self.accinput_list_button_layout = QtGui.QHBoxLayout()
        self.accinput_list_add_button = QtGui.QPushButton("Add new")
        self.accinput_list_remove_button = QtGui.QPushButton("Remove selected")
        [self.accinput_list_button_layout.addWidget(x) for x in [
            self.accinput_list_add_button,
            self.accinput_list_remove_button
        ]]
        self.accinput_list_layout.addWidget(self.accinput_list)
        self.accinput_list_layout.addLayout(self.accinput_list_button_layout)
        self.accinput_list_groupbox.setLayout(self.accinput_list_layout)

        self.accinput_data_groupbox = QtGui.QGroupBox(__("Acceleration Input data"))
        self.accinput_data_layout = QtGui.QVBoxLayout()

        self.accinput_label_layout = QtGui.QHBoxLayout()
        self.accinput_label_label = QtGui.QLabel(__("Label:"))
        self.accinput_label_input = QtGui.QLineEdit()
        self.accinput_label_layout.addWidget(self.accinput_label_label)
        self.accinput_label_layout.addWidget(self.accinput_label_input)

        self.accinput_mkfluid_layout = QtGui.QHBoxLayout()
        self.accinput_mkfluid_label = QtGui.QLabel(__("Mk-fluid of selected particles:"))
        self.accinput_mkfluid_input = QtGui.QLineEdit()
        self.accinput_mkfluid_layout.addWidget(self.accinput_mkfluid_label)
        self.accinput_mkfluid_layout.addWidget(self.accinput_mkfluid_input)

        self.accinput_acccentre_layout = QtGui.QHBoxLayout()
        self.accinput_acccentre_label = QtGui.QLabel(__("Center of acceleration [X,Y,Z] (m):"))
        self.accinput_acccentre_x = QtGui.QLineEdit()
        self.accinput_acccentre_y = QtGui.QLineEdit()
        self.accinput_acccentre_z = QtGui.QLineEdit()
        [self.accinput_acccentre_layout.addWidget(x) for x in [
            self.accinput_acccentre_label,
            self.accinput_acccentre_x,
            self.accinput_acccentre_y,
            self.accinput_acccentre_z,
        ]]

        self.accinput_globalgravity_layout = QtGui.QHBoxLayout()
        self.accinput_globalgravity_check = QtGui.QCheckBox(__("Global Gravity"))
        self.accinput_globalgravity_layout.addWidget(self.accinput_globalgravity_check)

        self.accinput_datafile_layout = QtGui.QHBoxLayout()
        self.accinput_datafile_label = QtGui.QLabel(__("File with acceleration data:"))
        self.accinput_datafile_input = QtGui.QLineEdit()
        self.accinput_datafile_button = QtGui.QPushButton(__("..."))
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_label)
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_input)
        self.accinput_datafile_layout.addWidget(self.accinput_datafile_button)

        self.accinput_save_layout = QtGui.QHBoxLayout()
        self.accinput_save_button = QtGui.QPushButton(__("Save Data"))
        self.accinput_save_layout.addStretch(1)
        self.accinput_save_layout.addWidget(self.accinput_save_button)

        [self.accinput_data_layout.addLayout(x) for x in [
            self.accinput_label_layout,
            self.accinput_mkfluid_layout,
            self.accinput_acccentre_layout,
            self.accinput_globalgravity_layout,
            self.accinput_datafile_layout,
            self.accinput_save_layout
        ]]

        self.accinput_data_groupbox.setLayout(self.accinput_data_layout)

        self.accinput_layout.addWidget(self.accinput_list_groupbox)
        self.accinput_layout.addWidget(self.accinput_data_groupbox)

        self.button_layout = QtGui.QHBoxLayout()
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.enabled_check)
        self.main_layout.addLayout(self.accinput_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.fill_data()
        self.init_connections()

    def get_result(self):
        """ Returns the AccelerationInput object """
        return self.accinput

    def fill_data(self):
        self.list_refresh()
        self.on_list_select()
        self.enabled_check.setCheckState(QtCore.Qt.Checked if self.accinput.enabled else QtCore.Qt.Unchecked)
        self.on_enable()

    def init_connections(self):
        self.ok_button.clicked.connect(self.on_ok)
        self.accinput_datafile_button.clicked.connect(self.on_browse)
        self.accinput_list_add_button.clicked.connect(self.on_add)
        self.accinput_list_remove_button.clicked.connect(self.on_remove)
        self.accinput_list.itemSelectionChanged.connect(self.on_list_select)
        self.accinput_save_button.clicked.connect(self.on_save_data)
        self.enabled_check.stateChanged.connect(self.on_enable)

    def on_ok(self):
        self.accept()

    def on_browse(self):
        file_name, _ = QtGui.QFileDialog().getOpenFileName(self,
                                                           "Select file to use", QtCore.QDir.homePath())
        self.accinput_datafile_input.setText(file_name)

    def on_add(self):
        self.accinput.acclist.append(AccelerationInputData())
        self.list_refresh()

    def on_remove(self):
        if len(self.accinput.acclist) is 0:
            return
        index = self.accinput_list.currentRow()
        self.accinput.acclist.pop(index)
        self.list_refresh()

    def on_list_select(self):
        if len(self.accinput.acclist) is 0:
            return
        index = self.accinput_list.currentRow()
        item = self.accinput.acclist[index]
        self.accinput_label_input.setText(item.label)
        self.accinput_mkfluid_input.setText(str(item.mkfluid))
        self.accinput_acccentre_x.setText(str(item.acccentre[0]))
        self.accinput_acccentre_y.setText(str(item.acccentre[1]))
        self.accinput_acccentre_z.setText(str(item.acccentre[2]))
        self.accinput_globalgravity_check.setChecked(bool(item.globalgravity))
        self.accinput_datafile_input.setText(item.datafile)

    def list_refresh(self):
        self.accinput_list.clear()
        self.accinput_list.insertItems(0, [x.label for x in self.accinput.acclist])
        self.accinput_list.setCurrentRow(0)

    def on_save_data(self):
        if len(self.accinput.acclist) is 0:
            return
        index = self.accinput_list.currentRow()
        item = self.accinput.acclist[index]

        item.label = str(self.accinput_label_input.text())
        item.mkfluid = int(self.accinput_mkfluid_input.text())
        item.acccentre = [float(self.accinput_acccentre_x.text()),
                          float(self.accinput_acccentre_y.text()),
                          float(self.accinput_acccentre_z.text())]
        item.globalgravity = bool(self.accinput_globalgravity_check.isChecked())
        item.datafile = str(self.accinput_datafile_input.text())

        self.accinput.acclist[index] = item
        self.list_refresh()

    def on_enable(self):
        self.accinput.enabled = self.enabled_check.isChecked()
        self.accinput_list_groupbox.setEnabled(self.accinput.enabled)
        self.accinput_data_groupbox.setEnabled(self.accinput.enabled)


class RelaxationZoneUniformConfigDialog(QtGui.QDialog):
    def __init__(self, relaxationzone=None):
        super(RelaxationZoneUniformConfigDialog, self).__init__()
        self.temp_relaxationzone = relaxationzone if relaxationzone is not None else RelaxationZoneUniform()
        self.relaxationzone = relaxationzone
        self.velocity_times = list()
        self.velocity_times_dialog = VelocityTimesDialog(self.temp_relaxationzone)

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

        self.domainbox_groupbox = QtGui.QGroupBox(__("Domain Box"))
        self.domainbox_layout = QtGui.QVBoxLayout()

        self.domainbox_point_layout = QtGui.QHBoxLayout()
        self.domainbox_point_label = QtGui.QLabel(__("Point [X, Y, Z] (m): "))
        self.domainbox_point_x = QtGui.QLineEdit()
        self.domainbox_point_y = QtGui.QLineEdit()
        self.domainbox_point_z = QtGui.QLineEdit()
        [self.domainbox_point_layout.addWidget(x) for x in [
            self.domainbox_point_label,
            self.domainbox_point_x,
            self.domainbox_point_y,
            self.domainbox_point_z
        ]]
        self.domainbox_layout.addLayout(self.domainbox_point_layout)

        self.domainbox_size_layout = QtGui.QHBoxLayout()
        self.domainbox_size_label = QtGui.QLabel(__("Size [X, Y, Z] (m): "))
        self.domainbox_size_x = QtGui.QLineEdit()
        self.domainbox_size_y = QtGui.QLineEdit()
        self.domainbox_size_z = QtGui.QLineEdit()
        [self.domainbox_size_layout.addWidget(x) for x in [
            self.domainbox_size_label,
            self.domainbox_size_x,
            self.domainbox_size_y,
            self.domainbox_size_z
        ]]
        self.domainbox_layout.addLayout(self.domainbox_size_layout)

        self.domainbox_direction_layout = QtGui.QHBoxLayout()
        self.domainbox_direction_label = QtGui.QLabel(__("Direction [X, Y, Z] (m): "))
        self.domainbox_direction_x = QtGui.QLineEdit()
        self.domainbox_direction_y = QtGui.QLineEdit()
        self.domainbox_direction_z = QtGui.QLineEdit()
        [self.domainbox_direction_layout.addWidget(x) for x in [
            self.domainbox_direction_label,
            self.domainbox_direction_x,
            self.domainbox_direction_y,
            self.domainbox_direction_z
        ]]
        self.domainbox_layout.addLayout(self.domainbox_direction_layout)

        self.domainbox_groupbox.setLayout(self.domainbox_layout)

        self.use_velocity_check = QtGui.QCheckBox(__("Use Velocity (Uncheck for velocity in time)"))

        self.velocity_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel(__("Velocity: "))
        self.velocity_input = QtGui.QLineEdit()
        [self.velocity_layout.addWidget(x) for x in [
            self.velocity_label,
            self.velocity_input
        ]]

        self.velocity_times_button = QtGui.QPushButton(__("Edit velocity in time"))

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

        [self.data_layout.addLayout(x) for x in [
            self.start_layout,
            self.duration_layout
        ]]

        self.data_layout.addWidget(self.domainbox_groupbox)
        self.data_layout.addWidget(self.use_velocity_check)
        self.data_layout.addWidget(self.velocity_times_button)

        [self.data_layout.addLayout(x) for x in [
            self.velocity_layout,
            self.coefdt_layout,
            self.function_layout
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
        self.use_velocity_check.stateChanged.connect(self.on_velocity_check)
        self.velocity_times_button.clicked.connect(self.on_velocity_times)
        self.setLayout(self.main_layout)
        self.fill_data()
        self.on_velocity_check()
        self.exec_()

    def on_apply(self):
        self.temp_relaxationzone.start = float(self.start_input.text())
        self.temp_relaxationzone.duration = float(self.duration_input.text())
        self.temp_relaxationzone.domainbox_point = [
            float(self.domainbox_point_x.text()),
            float(self.domainbox_point_y.text()),
            float(self.domainbox_point_z.text())]
        self.temp_relaxationzone.domainbox_size = [
            float(self.domainbox_size_x.text()),
            float(self.domainbox_size_y.text()),
            float(self.domainbox_size_z.text())]
        self.temp_relaxationzone.domainbox_direction = [
            float(self.domainbox_direction_x.text()),
            float(self.domainbox_direction_y.text()),
            float(self.domainbox_direction_z.text())]
        self.temp_relaxationzone.use_velocity = bool(self.use_velocity_check.isChecked())
        self.temp_relaxationzone.velocity = float(self.velocity_input.text())
        self.temp_relaxationzone.velocity_times = self.velocity_times
        self.temp_relaxationzone.coefdt = float(self.coefdt_input.text())
        self.temp_relaxationzone.function_psi = float(self.function_psi_input.text())
        self.temp_relaxationzone.function_beta = float(self.function_beta_input.text())
        self.relaxationzone = self.temp_relaxationzone
        self.accept()

    def on_delete(self):
        self.relaxationzone = None
        self.reject()

    def on_velocity_times(self):
        result = self.velocity_times_dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            self.velocity_times = self.velocity_times_dialog.velocity_times

    def on_velocity_check(self):
        self.velocity_times_button.setEnabled(not self.use_velocity_check.isChecked())
        self.velocity_input.setEnabled(self.use_velocity_check.isChecked())

    def fill_data(self):
        self.start_input.setText(str(self.temp_relaxationzone.start))
        self.duration_input.setText(str(self.temp_relaxationzone.duration))
        self.domainbox_point_x.setText(str(self.temp_relaxationzone.domainbox_point[0]))
        self.domainbox_point_y.setText(str(self.temp_relaxationzone.domainbox_point[1]))
        self.domainbox_point_z.setText(str(self.temp_relaxationzone.domainbox_point[2]))
        self.domainbox_size_x.setText(str(self.temp_relaxationzone.domainbox_size[0]))
        self.domainbox_size_y.setText(str(self.temp_relaxationzone.domainbox_size[1]))
        self.domainbox_size_z.setText(str(self.temp_relaxationzone.domainbox_size[2]))
        self.domainbox_direction_x.setText(str(self.temp_relaxationzone.domainbox_direction[0]))
        self.domainbox_direction_y.setText(str(self.temp_relaxationzone.domainbox_direction[1]))
        self.domainbox_direction_z.setText(str(self.temp_relaxationzone.domainbox_direction[2]))
        self.use_velocity_check.setChecked(bool(self.temp_relaxationzone.use_velocity))
        self.velocity_input.setText(str(self.temp_relaxationzone.velocity))
        self.coefdt_input.setText(str(self.temp_relaxationzone.coefdt))
        self.function_psi_input.setText(str(self.temp_relaxationzone.function_psi))
        self.function_beta_input.setText(str(self.temp_relaxationzone.function_beta))


class VelocityTimesDialog(QtGui.QDialog):
    """ Dialog with a table to create velocity times. """

    def __init__(self, relaxationzone):
        super(VelocityTimesDialog, self).__init__()
        self.relaxationzone = relaxationzone
        self.velocity_times = relaxationzone.velocity_times

        self.main_layout = QtGui.QVBoxLayout()
        self.table = QtGui.QTableWidget(50, 2)
        self.table.setHorizontalHeaderLabels([__("Time"), __("Value")])

        self.button_layout = QtGui.QHBoxLayout()
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.fill_data()

    def fill_data(self):
        for row, value in enumerate(self.velocity_times):
            self.table.setItem(row, 0, QtGui.QTableWidgetItem(str(value[0])))
            self.table.setItem(row, 1, QtGui.QTableWidgetItem(str(value[1])))

    def on_cancel(self):
        self.reject()

    def on_ok(self):
        self.velocity_times = list()
        for i in range(self.table.rowCount()):
            value_to_insert = []
            try:
                value_to_insert = [float(self.table.item(i, 0).text()), float(self.table.item(i, 0).text())]
            except:
                pass
            if len(value_to_insert) > 0:
                self.velocity_times.append(value_to_insert)
        self.accept()


class HoverableLabel(QtGui.QLabel):
    hover = QtCore.Signal(str)
    help_text = ""

    def __init__(self, label_text):
        super(HoverableLabel, self).__init__(label_text)

    def setHelpText(self, help_text):
        self.help_text = help_text

    def enterEvent(self, *args, **kwargs):
        self.hover.emit(self.help_text)


class FocusableLineEdit(QtGui.QLineEdit):
    focus = QtCore.Signal(str)
    help_text = ""

    def __init__(self):
        super(FocusableLineEdit, self).__init__()

    def setHelpText(self, help_text):
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        QtGui.QLineEdit.focusInEvent(self, *args, **kwargs).__init__()
        self.focus.emit(self.help_text)


class FocusableComboBox(QtGui.QComboBox):
    focus = QtCore.Signal(str)
    help_text = ""

    def __init__(self):
        super(FocusableComboBox, self).__init__()

    def setHelpText(self, help_text):
        self.help_text = help_text

    def focusInEvent(self, *args, **kwargs):
        QtGui.QComboBox.focusInEvent(self, *args, **kwargs).__init__()
        self.focus.emit(self.help_text)


class ConstantsDialog(QtGui.QDialog):

    def __init__(self, data):
        super(ConstantsDialog, self).__init__()

        self.data = data

        self.setWindowTitle("DSPH Constant definition")
        self.help_window = QtGui.QTextEdit()
        self.help_window.setMaximumHeight(50)
        self.help_window.setReadOnly(True)
        self.ok_button = QtGui.QPushButton("Ok")
        self.cancel_button = QtGui.QPushButton("Cancel")

        # Lattice for boundaries layout and components
        self.lattice_layout = QtGui.QHBoxLayout()
        self.lattice_label = QtGui.QLabel("Lattice for Boundaries: ")
        self.lattice_input = QtGui.QComboBox()
        self.lattice_input.insertItems(0, ['Lattice 1', 'Lattice 2'])
        self.lattice_input.setCurrentIndex(int(self.data['lattice_bound']) - 1)

        self.lattice_layout.addWidget(self.lattice_label)
        self.lattice_layout.addWidget(self.lattice_input)
        self.lattice_layout.addStretch(1)

        # Lattice for fluids layout and components
        self.lattice2_layout = QtGui.QHBoxLayout()
        self.lattice2_label = QtGui.QLabel("Lattice for Fluids: ")
        self.lattice2_input = QtGui.QComboBox()
        self.lattice2_input.insertItems(0, ['Lattice 1', 'Lattice 2'])
        self.lattice2_input.setCurrentIndex(int(self.data['lattice_fluid']) - 1)

        self.lattice2_layout.addWidget(self.lattice2_label)
        self.lattice2_layout.addWidget(self.lattice2_input)
        self.lattice2_layout.addStretch(1)

        # Gravity
        self.gravity_layout = QtGui.QHBoxLayout()
        self.gravity_label = HoverableLabel("Gravity [X, Y, Z]: ")

        self.gravityx_input = QtGui.QLineEdit()
        self.gravityx_input = FocusableLineEdit()
        self.gravityx_input.setHelpText(utils.__(constants.HELP_GRAVITYX))
        self.gravityx_input.setMaxLength(10)

        self.gravityx_input.focus.connect(self.on_help_focus)

        self.gravityx_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityx_input)
        self.gravityx_input.setText(str(self.data['gravity'][0]))
        self.gravityx_input.setValidator(self.gravityx_validator)

        self.gravityy_input = QtGui.QLineEdit()
        self.gravityy_input = FocusableLineEdit()
        self.gravityy_input.setHelpText(utils.__(constants.HELP_GRAVITYY))
        self.gravityy_input.setMaxLength(10)

        self.gravityy_input.focus.connect(self.on_help_focus)

        self.gravityy_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityy_input)
        self.gravityy_input.setText(str(self.data['gravity'][1]))
        self.gravityy_input.setValidator(self.gravityy_validator)

        self.gravityz_input = QtGui.QLineEdit()
        self.gravityz_input = FocusableLineEdit()
        self.gravityz_input.setHelpText(utils.__(constants.HELP_GRAVITYZ))
        self.gravityz_input.setMaxLength(10)

        self.gravityz_input.focus.connect(self.on_help_focus)

        self.gravityz_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityz_input)
        self.gravityz_input.setText(str(self.data['gravity'][2]))
        self.gravityz_input.setValidator(self.gravityz_validator)

        self.gravity_label2 = QtGui.QLabel(
            "m/s<span style='vertical-align:super'>2</span>")

        self.gravity_layout.addWidget(self.gravity_label)
        self.gravity_layout.addWidget(self.gravityx_input)  # For X
        self.gravity_layout.addWidget(self.gravityy_input)  # For Y
        self.gravity_layout.addWidget(self.gravityz_input)  # For Z
        self.gravity_layout.addWidget(self.gravity_label2)

        # Reference density of the fluid: layout and components
        self.rhop0_layout = QtGui.QHBoxLayout()
        self.rhop0_label = QtGui.QLabel("Fluid reference density: ")

        self.rhop0_input = QtGui.QLineEdit()
        self.rhop0_input = FocusableLineEdit()
        self.rhop0_input.setHelpText(utils.__(constants.HELP_RHOP0))
        self.rhop0_input.setMaxLength(10)

        self.rhop0_input.focus.connect(self.on_help_focus)

        self.rhop0_validator = QtGui.QIntValidator(0, 10000, self.rhop0_input)
        self.rhop0_input.setText(str(self.data['rhop0']))
        self.rhop0_input.setValidator(self.rhop0_validator)
        self.rhop0_label2 = QtGui.QLabel(
            "kg/m<span style='vertical-align:super'>3<span>")

        self.rhop0_layout.addWidget(self.rhop0_label)
        self.rhop0_layout.addWidget(self.rhop0_input)
        self.rhop0_layout.addWidget(self.rhop0_label2)

        # Maximum still water lavel to calc.  spdofsound using coefsound: layout and
        # components
        self.hswlauto_layout = QtGui.QHBoxLayout()
        self.hswlauto_chk = QtGui.QCheckBox("Auto HSWL ")
        if self.data['hswl_auto']:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hswlauto_chk.toggled.connect(self.on_hswlauto_check)
        self.hswlauto_layout.addWidget(self.hswlauto_chk)

        self.hswl_layout = QtGui.QHBoxLayout()
        self.hswl_label = QtGui.QLabel("HSWL: ")
        self.hswl_input = QtGui.QLineEdit()
        self.hswl_input = FocusableLineEdit()
        self.hswl_input.setHelpText(utils.__(constants.HELP_HSWL))
        self.hswl_input.setMaxLength(10)

        self.hswl_input.focus.connect(self.on_help_focus)

        self.hswl_validator = QtGui.QIntValidator(0, 10000, self.hswl_input)
        self.hswl_input.setText(str(self.data['hswl']))
        self.hswl_input.setValidator(self.hswl_validator)
        self.hswl_label2 = QtGui.QLabel("metres")

        self.hswl_layout.addWidget(self.hswl_label)
        self.hswl_layout.addWidget(self.hswl_input)
        self.hswl_layout.addWidget(self.hswl_label2)

        # Manually trigger check for the first time
        self.on_hswlauto_check()

        # gamma: layout and components
        self.gamma_layout = QtGui.QHBoxLayout()
        self.gamma_label = QtGui.QLabel("Gamma: ")
        self.gamma_input = QtGui.QLineEdit()
        self.gamma_input = FocusableLineEdit()
        self.gamma_input.setHelpText(utils.__(constants.HELP_GAMMA))
        self.gamma_input.setMaxLength(3)

        self.gamma_input.focus.connect(self.on_help_focus)

        self.gamma_validator = QtGui.QIntValidator(0, 999, self.gamma_input)
        self.gamma_input.setText(str(self.data['gamma']))
        self.gamma_input.setValidator(self.gamma_validator)
        self.gamma_label2 = QtGui.QLabel("units")

        self.gamma_layout.addWidget(self.gamma_label)
        self.gamma_layout.addWidget(self.gamma_input)
        self.gamma_layout.addWidget(self.gamma_label2)

        # Speedsystem: layout and components
        self.speedsystemauto_layout = QtGui.QHBoxLayout()
        self.speedsystemauto_chk = QtGui.QCheckBox("Auto Speedsystem ")
        if self.data['speedsystem_auto']:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsystemauto_chk.toggled.connect(self.on_speedsystemauto_check)
        self.speedsystemauto_layout.addWidget(self.speedsystemauto_chk)

        self.speedsystem_layout = QtGui.QHBoxLayout()
        self.speedsystem_label = QtGui.QLabel("Speedsystem: ")
        self.speedsystem_input = QtGui.QLineEdit()
        self.speedsystem_input = FocusableLineEdit()
        self.speedsystem_input.setHelpText(utils.__(constants.HELP_SPEEDSYSTEM))
        self.speedsystem_input.setMaxLength(10)

        self.speedsystem_input.focus.connect(self.on_help_focus)

        self.speedsystem_validator = QtGui.QIntValidator(0, 10000, self.speedsystem_input)
        self.speedsystem_input.setText(str(self.data['speedsystem']))
        self.speedsystem_input.setValidator(self.speedsystem_validator)
        self.speedsystem_label2 = QtGui.QLabel("m/s")

        self.speedsystem_layout.addWidget(self.speedsystem_label)
        self.speedsystem_layout.addWidget(self.speedsystem_input)
        self.speedsystem_layout.addWidget(self.speedsystem_label2)

        # Manually trigger check for the first time
        self.on_speedsystemauto_check()

        # coefsound: layout and components
        self.coefsound_layout = QtGui.QHBoxLayout()
        self.coefsound_label = QtGui.QLabel("Coefsound: ")
        self.coefsound_input = QtGui.QLineEdit()
        self.coefsound_input = FocusableLineEdit()
        self.coefsound_input.setHelpText(utils.__(constants.HELP_COEFSOUND))
        self.coefsound_input.setMaxLength(3)

        self.coefsound_input.focus.connect(self.on_help_focus)

        self.coefsound_validator = QtGui.QIntValidator(0, 999, self.coefsound_input)
        self.coefsound_input.setText(str(self.data['coefsound']))
        self.coefsound_input.setValidator(self.coefsound_validator)
        self.coefsound_label2 = QtGui.QLabel("units")

        self.coefsound_layout.addWidget(self.coefsound_label)
        self.coefsound_layout.addWidget(self.coefsound_input)
        self.coefsound_layout.addWidget(self.coefsound_label2)

        # Speedsound: layout and components
        self.speedsoundauto_layout = QtGui.QHBoxLayout()
        self.speedsoundauto_chk = QtGui.QCheckBox("Auto Speedsound ")
        if self.data['speedsound_auto']:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsoundauto_chk.toggled.connect(self.on_speedsoundauto_check)
        self.speedsoundauto_layout.addWidget(self.speedsoundauto_chk)

        self.speedsound_layout = QtGui.QHBoxLayout()
        self.speedsound_label = QtGui.QLabel("Speedsound: ")
        self.speedsound_input = QtGui.QLineEdit()
        self.speedsound_input = FocusableLineEdit()
        self.speedsound_input.setHelpText(utils.__(constants.HELP_SPEEDSOUND))
        self.speedsound_input.setMaxLength(10)

        self.speedsound_input.focus.connect(self.on_help_focus)

        self.speedsound_validator = QtGui.QIntValidator(0, 10000, self.speedsound_input)
        self.speedsound_input.setText(str(self.data['speedsound']))
        self.speedsound_input.setValidator(self.speedsound_validator)
        self.speedsound_label2 = QtGui.QLabel("m/s")

        self.speedsound_layout.addWidget(self.speedsound_label)
        self.speedsound_layout.addWidget(self.speedsound_input)
        self.speedsound_layout.addWidget(self.speedsound_label2)

        # Manually trigger check for the first time
        self.on_speedsoundauto_check()

        # coefh: layout and components
        self.coefh_layout = QtGui.QHBoxLayout()
        self.coefh_label = QtGui.QLabel("CoefH: ")
        self.coefh_input = QtGui.QLineEdit()
        self.coefh_input = FocusableLineEdit()
        self.coefh_input.setHelpText(utils.__(constants.HELP_COEFH))
        self.coefh_input.setMaxLength(10)

        self.coefh_input.focus.connect(self.on_help_focus)

        self.coefh_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.coefh_input.setText(str(self.data['coefh']))
        self.coefh_input.setValidator(self.coefh_validator)
        self.coefh_label2 = QtGui.QLabel("units")

        self.coefh_layout.addWidget(self.coefh_label)
        self.coefh_layout.addWidget(self.coefh_input)
        self.coefh_layout.addWidget(self.coefh_label2)

        # cflnumber: layout and components
        self.cflnumber_layout = QtGui.QHBoxLayout()
        self.cflnumber_label = QtGui.QLabel("cflnumber: ")
        self.cflnumber_input = QtGui.QLineEdit()
        self.cflnumber_input = FocusableLineEdit()
        self.cflnumber_input.setHelpText(utils.__(constants.HELP_CFLNUMBER))
        self.cflnumber_input.setMaxLength(10)

        self.cflnumber_input.focus.connect(self.on_help_focus)

        self.cflnumber_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.cflnumber_input.setText(str(self.data['cflnumber']))
        self.cflnumber_input.setValidator(self.cflnumber_validator)
        self.cflnumber_label2 = QtGui.QLabel("units")

        self.cflnumber_layout.addWidget(self.cflnumber_label)
        self.cflnumber_layout.addWidget(self.cflnumber_input)
        self.cflnumber_layout.addWidget(self.cflnumber_label2)

        # h: layout and components
        self.hauto_layout = QtGui.QHBoxLayout()
        self.hauto_chk = QtGui.QCheckBox("Auto Smoothing length ")
        if self.data['h_auto']:
            self.hauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hauto_chk.toggled.connect(self.on_hauto_check)
        self.hauto_layout.addWidget(self.hauto_chk)

        self.h_layout = QtGui.QHBoxLayout()
        self.h_label = QtGui.QLabel("Smoothing Length: ")
        self.h_input = QtGui.QLineEdit()
        self.h_input = FocusableLineEdit()
        self.h_input.setHelpText("Smoothing Length")
        self.h_input.setMaxLength(10)

        self.h_input.focus.connect(self.on_help_focus)

        self.h_validator = QtGui.QDoubleValidator(0, 100, 8, self.h_input)
        self.h_input.setText(str(self.data['h']))
        self.h_input.setValidator(self.h_validator)
        self.h_label2 = QtGui.QLabel("metres")

        self.h_layout.addWidget(self.h_label)
        self.h_layout.addWidget(self.h_input)
        self.h_layout.addWidget(self.h_label2)

        # Manually trigger check for the first time
        self.on_hauto_check()

        # b: layout and components
        self.bauto_layout = QtGui.QHBoxLayout()
        self.bauto_chk = QtGui.QCheckBox("Auto b constant for EOS ")
        if self.data['b_auto']:
            self.bauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.bauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.bauto_chk.toggled.connect(self.on_bauto_check)
        self.bauto_layout.addWidget(self.bauto_chk)

        self.b_layout = QtGui.QHBoxLayout()
        self.b_label = QtGui.QLabel("B constant: ")
        self.b_input = QtGui.QLineEdit()
        self.b_input = FocusableLineEdit()
        self.b_input.setHelpText("B constant")
        self.b_input.setMaxLength(10)

        self.b_input.focus.connect(self.on_help_focus)

        self.b_validator = QtGui.QDoubleValidator(0, 100, 8, self.b_input)
        self.b_input.setText(str(self.data['b']))
        self.b_input.setValidator(self.b_validator)
        self.b_label2 = QtGui.QLabel("Pascal")

        self.b_layout.addWidget(self.b_label)
        self.b_layout.addWidget(self.b_input)
        self.b_layout.addWidget(self.b_label2)

        # Manually trigger check for the first time
        self.on_bauto_check()

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        # Help Text Layout definition

        self.cw_helpText_layout = QtGui.QHBoxLayout()
        self.cw_helpText_layout.addWidget(self.help_window)
        self.cw_helpText_layout.setStretchFactor(self.help_window,0)

        # Button layout definition
        self.cw_button_layout = QtGui.QHBoxLayout()
        self.cw_button_layout.addStretch(1)
        self.cw_button_layout.addWidget(self.ok_button)
        self.cw_button_layout.addWidget(self.cancel_button)

        # START Main layout definition and composition.
        self.cw_main_layout_scroll = QtGui.QScrollArea()
        self.cw_main_layout_scroll_widget = QtGui.QWidget()
        self.cw_main_layout = QtGui.QVBoxLayout()

        # Lattice was removed on 0.3Beta - 1 of June
        # self.cw_main_layout.addLayout(self.lattice_layout)
        # self.cw_main_layout.addLayout(self.lattice2_layout)
        self.cw_main_layout.addLayout(self.gravity_layout)
        self.cw_main_layout.addLayout(self.rhop0_layout)
        self.cw_main_layout.addLayout(self.hswlauto_layout)
        self.cw_main_layout.addLayout(self.hswl_layout)
        self.cw_main_layout.addLayout(self.gamma_layout)
        self.cw_main_layout.addLayout(self.speedsystemauto_layout)
        self.cw_main_layout.addLayout(self.speedsystem_layout)
        self.cw_main_layout.addLayout(self.coefsound_layout)
        self.cw_main_layout.addLayout(self.speedsoundauto_layout)
        self.cw_main_layout.addLayout(self.speedsound_layout)
        self.cw_main_layout.addLayout(self.coefh_layout)
        self.cw_main_layout.addLayout(self.cflnumber_layout)
        self.cw_main_layout.addLayout(self.hauto_layout)
        self.cw_main_layout.addLayout(self.h_layout)
        self.cw_main_layout.addLayout(self.bauto_layout)
        self.cw_main_layout.addLayout(self.b_layout)

        self.cw_main_layout.addStretch(1)

        self.cw_main_layout_scroll_widget.setLayout(self.cw_main_layout)
        self.cw_main_layout_scroll.setWidget(self.cw_main_layout_scroll_widget)
        self.cw_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.constants_window_layout = QtGui.QVBoxLayout()
        self.constants_window_layout.addWidget(self.cw_main_layout_scroll)
        self.constants_window_layout.addLayout(self.cw_helpText_layout)
        self.constants_window_layout.addLayout(self.cw_button_layout)
        self.setLayout(self.constants_window_layout)
        self.setMaximumHeight(550)
        # END Main layout definition and composition.

    # Controls if user selected auto HSWL or not enabling/disablen HSWL custom
    def on_hswlauto_check(self):
        # value introduction
        if self.hswlauto_chk.isChecked():
            self.hswl_input.setEnabled(False)
        else:
            self.hswl_input.setEnabled(True)

    def on_help_focus(self, help_text):
        self.help_window.setText(help_text)

    # Controls if user selected auto speedsystem or not enabling/disablen
    def on_speedsystemauto_check(self):
        # speedsystem custom value introduction
        if self.speedsystemauto_chk.isChecked():
            self.speedsystem_input.setEnabled(False)
        else:
            self.speedsystem_input.setEnabled(True)

    def on_speedsoundauto_check(self):  # Controls if user selected auto speedsound or not enabling/disablen speedsound
        # custom value introduction
        if self.speedsoundauto_chk.isChecked():
            self.speedsound_input.setEnabled(False)
        else:
            self.speedsound_input.setEnabled(True)

    # Controls if user selected auto h or not enabling/disablen h custom value introduction
    def on_hauto_check(self):
        if self.hauto_chk.isChecked():
            self.h_input.setEnabled(False)
        else:
            self.h_input.setEnabled(True)

    # Controls if user selected auto b or not enabling/disablen b custom value introduction
    def on_bauto_check(self):
        if self.bauto_chk.isChecked():
            self.b_input.setEnabled(False)
        else:
            self.b_input.setEnabled(True)

    def on_ok(self):
        self.data['lattice_bound'] = str(self.lattice_input.currentIndex() + 1)
        self.data['lattice_fluid'] = str(self.lattice2_input.currentIndex() + 1)
        self.data['gravity'] = [
            self.gravityx_input.text(),
            self.gravityy_input.text(),
            self.gravityz_input.text()
        ]
        self.data['rhop0'] = self.rhop0_input.text()
        self.data['hswl'] = self.hswl_input.text()
        self.data['hswl_auto'] = self.hswlauto_chk.isChecked()
        self.data['gamma'] = self.gamma_input.text()
        self.data['speedsystem'] = self.speedsystem_input.text()
        self.data['speedsystem_auto'] = self.speedsystemauto_chk.isChecked()
        self.data['coefsound'] = self.coefsound_input.text()
        self.data['speedsound'] = self.speedsound_input.text()
        self.data['speedsound_auto'] = self.speedsoundauto_chk.isChecked()
        self.data['coefh'] = self.coefh_input.text()
        self.data['cflnumber'] = self.cflnumber_input.text()
        self.data['h'] = self.h_input.text()
        self.data['h_auto'] = self.hauto_chk.isChecked()
        self.data['b'] = self.b_input.text()
        self.data['b_auto'] = self.bauto_chk.isChecked()
        utils.log("Constants changed")
        self.accept()

    def on_cancel(self):
        utils.log("Constants not changed")
        self.reject()


class ExecutionParametersDialog(QtGui.QDialog):
    """Defines the execution parameters window.
    Modifies the data dictionary passed as parameter."""

    def __init__(self, data):
        super(ExecutionParametersDialog, self).__init__()

        self.data = data

        # Creates a dialog and 2 main buttons
        self.setWindowTitle("DSPH Execution Parameters")
        self.help_window = QtGui.QTextEdit()
        self.help_window.setMaximumHeight(50)
        self.help_window.setReadOnly(True)
        self.ok_button = QtGui.QPushButton("Ok")
        self.cancel_button = QtGui.QPushButton("Cancel")

        # Precision in particle interaction
        self.posdouble_layout = QtGui.QHBoxLayout()
        self.posdouble_label = QtGui.QLabel("Precision in particle interaction: ")
        self.posdouble_input = FocusableComboBox()
        self.posdouble_input.insertItems(0,
                                    ['Double', 'Simple', 'Uses and saves double'])
        self.posdouble_input.setCurrentIndex(int(self.data['posdouble']))
        self.posdouble_input.setHelpText(utils.__(constants.HELP_POSDOUBLE))

        self.posdouble_input.focus.connect(self.on_help_focus)

        self.posdouble_layout.addWidget(self.posdouble_label)
        self.posdouble_layout.addWidget(self.posdouble_input)
        self.posdouble_layout.addStretch(1)

        self.stepalgorithm_layout = QtGui.QHBoxLayout()
        self.stepalgorithm_label = QtGui.QLabel("Step Algorithm: ")
        self.stepalgorithm_input = FocusableComboBox()
        self.stepalgorithm_input.insertItems(0, ['Symplectic', 'Verlet'])
        self.stepalgorithm_input.setCurrentIndex(int(self.data['stepalgorithm']) - 1)
        self.stepalgorithm_input.setHelpText(utils.__(constants.HELP_STEPALGORITHM))

        self.stepalgorithm_input.focus.connect(self.on_help_focus)

        self.stepalgorithm_input.currentIndexChanged.connect(self.on_step_change)

        self.stepalgorithm_layout.addWidget(self.stepalgorithm_label)
        self.stepalgorithm_layout.addWidget(self.stepalgorithm_input)
        self.stepalgorithm_layout.addStretch(1)

        # Verlet steps
        self.verletsteps_layout = QtGui.QHBoxLayout()
        self.verletsteps_label = QtGui.QLabel("Verlet Steps: ")
        self.verletsteps_input = QtGui.QLineEdit()
        self.verletsteps_input = FocusableLineEdit()
        self.verletsteps_input.setHelpText(utils.__(constants.HELP_VERLETSTEPS))
        self.verletsteps_input.setMaxLength(4)

        self.verletsteps_input.focus.connect(self.on_help_focus)

        self.verletsteps_validator = QtGui.QIntValidator(0, 9999, self.verletsteps_input)
        self.verletsteps_input.setText(str(self.data['verletsteps']))
        self.verletsteps_input.setValidator(self.verletsteps_validator)

        # Enable/Disable fields depending on selection
        self.on_step_change(self.stepalgorithm_input.currentIndex)

        self.verletsteps_layout.addWidget(self.verletsteps_label)
        self.verletsteps_layout.addWidget(self.verletsteps_input)

        # Kernel
        self.kernel_layout = QtGui.QHBoxLayout()
        self.kernel_label = QtGui.QLabel("Interaction kernel: ")
        self.kernel_input = FocusableComboBox()
        self.kernel_input.insertItems(0, ['Cubic spline', 'Wendland'])
        self.kernel_input.setHelpText(utils.__(constants.HELP_KERNEL))
        self.kernel_input.setCurrentIndex(int(self.data['kernel']) - 1)

        self.kernel_input.focus.connect(self.on_help_focus)

        self.kernel_layout.addWidget(self.kernel_label)
        self.kernel_layout.addWidget(self.kernel_input)
        self.kernel_layout.addStretch(1)

        # Viscosity formulation
        self.viscotreatment_layout = QtGui.QHBoxLayout()
        self.viscotreatment_label = QtGui.QLabel("Viscosity Formulation: ")
        self.viscotreatment_input = FocusableComboBox()
        self.viscotreatment_input.insertItems(0, ['Artificial', 'Laminar + SPS'])
        self.viscotreatment_input.setHelpText(utils.__(constants.HELP_VISCOTREATMENT))
        self.viscotreatment_input.setCurrentIndex(int(self.data['viscotreatment']) - 1)

        self.viscotreatment_input.focus.connect(self.on_help_focus)

        self.viscotreatment_layout.addWidget(self.viscotreatment_label)
        self.viscotreatment_layout.addWidget(self.viscotreatment_input)
        self.viscotreatment_layout.addStretch(1)

        # Viscosity value
        self.visco_layout = QtGui.QHBoxLayout()
        self.visco_label = QtGui.QLabel("Viscosity value: ")
        self.visco_input = FocusableLineEdit()
        self.visco_input.setHelpText(utils.__(constants.HELP_VISCO))
        self.visco_input.setMaxLength(10)

        self.visco_input.focus.connect(self.on_help_focus)

        self.visco_units_label = QtGui.QLabel("")
        self.visco_layout.addWidget(self.visco_label)
        self.visco_layout.addWidget(self.visco_input)
        self.visco_layout.addWidget(self.visco_units_label)

        self.on_viscotreatment_change(int(self.data['viscotreatment']) - 1)
        self.visco_input.setText(str(self.data['visco']))

        self.viscotreatment_input.currentIndexChanged.connect(self.on_viscotreatment_change)

        # Viscosity with boundary
        self.viscoboundfactor_layout = QtGui.QHBoxLayout()
        self.viscoboundfactor_label = QtGui.QLabel("Viscosity factor with boundary: ")
        self.viscoboundfactor_input = FocusableLineEdit()

        self.viscoboundfactor_input.setHelpText(utils.__(constants.HELP_VISCOBOUNDFACROT))

        self.viscoboundfactor_input.setMaxLength(10)

        self.viscoboundfactor_input.focus.connect(self.on_help_focus)

        self.viscoboundfactor_input.setText(str(self.data['viscoboundfactor']))

        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_label)
        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_input)

        self.deltasph_en_layout = QtGui.QHBoxLayout()
        self.deltasph_en_label = QtGui.QLabel("Enable DeltaSPH: ")
        self.deltasph_en_input = QtGui.QComboBox()
        self.deltasph_en_input.insertItems(0, ['No', 'Yes'])
        self.deltasph_en_input.setCurrentIndex(int(self.data['deltasph_en']))
        self.deltasph_en_input.currentIndexChanged.connect(self.on_deltasph_en_change)

        self.deltasph_en_layout.addWidget(self.deltasph_en_label)
        self.deltasph_en_layout.addWidget(self.deltasph_en_input)
        self.deltasph_en_layout.addStretch(1)

        # DeltaSPH value
        self.deltasph_layout = QtGui.QHBoxLayout()
        self.deltasph_label = QtGui.QLabel("DeltaSPH value: ")
        self.deltasph_input = FocusableLineEdit()
        self.deltasph_input.setHelpText(utils.__(constants.HELP_DELTASPH))
        self.deltasph_input.setMaxLength(10)

        self.deltasph_input.focus.connect(self.on_help_focus)

        self.deltasph_input.setText(str(self.data['deltasph']))
        self.deltasph_layout.addWidget(self.deltasph_label)
        self.deltasph_layout.addWidget(self.deltasph_input)

        if self.deltasph_en_input.currentIndex() == 0:
            self.deltasph_input.setEnabled(False)
        else:
            self.deltasph_input.setEnabled(True)

        self.shifting_layout = QtGui.QHBoxLayout()
        self.shifting_label = QtGui.QLabel("Shifting mode: ")
        self.shifting_input = FocusableComboBox()
        self.shifting_input.insertItems(
            0, ['None', 'Ignore bound', 'Ignore fixed', 'Full'])
        self.shifting_input.setHelpText(utils.__(constants.HELP_SHIFTING))

        self.shifting_input.focus.connect(self.on_help_focus)

        self.shifting_input.setCurrentIndex(int(self.data['shifting']))
        self.shifting_input.currentIndexChanged.connect(self.on_shifting_change)

        self.shifting_layout.addWidget(self.shifting_label)
        self.shifting_layout.addWidget(self.shifting_input)
        self.shifting_layout.addStretch(1)

        # Coefficient for shifting
        self.shiftcoef_layout = QtGui.QHBoxLayout()
        self.shiftcoef_label = QtGui.QLabel("Coefficient for shifting: ")
        self.shiftcoef_input = FocusableLineEdit()
        self.shiftcoef_input.setHelpText(utils.__(constants.HELP_SHIFTINGCOEF))
        self.shiftcoef_input.setMaxLength(10)

        self.shiftcoef_input.focus.connect(self.on_help_focus)

        self.shiftcoef_input.setText(str(self.data['shiftcoef']))
        self.shiftcoef_layout.addWidget(self.shiftcoef_label)
        self.shiftcoef_layout.addWidget(self.shiftcoef_input)

        # Free surface detection threshold
        self.shifttfs_layout = QtGui.QHBoxLayout()
        self.shifttfs_label = QtGui.QLabel("Free surface detection threshold: ")
        self.shifttfs_input = FocusableLineEdit()
        self.shifttfs_input.setHelpText(utils.__(constants.HELP_SHIFTINGTFS))
        self.shifttfs_input.setMaxLength(10)

        self.shifttfs_input.focus.connect(self.on_help_focus)

        self.shifttfs_input.setText(str(self.data['shifttfs']))
        self.shifttfs_layout.addWidget(self.shifttfs_label)
        self.shifttfs_layout.addWidget(self.shifttfs_input)

        # Enable/Disable fields depending on Shifting mode on window creation.
        self.on_shifting_change(self.shifting_input.currentIndex())

        # Rigid algorithm
        self.rigidalgorithm_layout = QtGui.QHBoxLayout()
        self.rigidalgorithm_label = QtGui.QLabel("Solid-solid interaction: ")
        self.rigidalgorithm_input = FocusableComboBox()
        self.rigidalgorithm_input.insertItems(0, ['SPH', 'DEM', 'CHRONO'])
        self.rigidalgorithm_input.setHelpText(utils.__(constants.HELP_RIGIDALGORITHM))
        self.rigidalgorithm_input.setCurrentIndex(int(self.data['rigidalgorithm']) - 1)

        self.rigidalgorithm_input.focus.connect(self.on_help_focus)

        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_label)
        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_input)
        self.rigidalgorithm_layout.addStretch(1)

        # Sim start freeze time
        self.ftpause_layout = QtGui.QHBoxLayout()
        self.ftpause_label = QtGui.QLabel("Floating freeze time: ")
        self.ftpause_input = FocusableLineEdit()
        self.ftpause_input.setHelpText(utils.__(constants.HELP_FTPAUSE))
        self.ftpause_input.setMaxLength(10)

        self.ftpause_input.focus.connect(self.on_help_focus)

        self.ftpause_input.setText(str(self.data['ftpause']))
        self.ftpause_label2 = QtGui.QLabel("seconds")
        self.ftpause_layout.addWidget(self.ftpause_label)
        self.ftpause_layout.addWidget(self.ftpause_input)
        self.ftpause_layout.addWidget(self.ftpause_label2)

        # Coefficient to calculate DT
        self.coefdtmin_layout = QtGui.QHBoxLayout()
        self.coefdtmin_label = QtGui.QLabel("Coefficient for minimum time step: ")
        self.coefdtmin_input = FocusableLineEdit()
        self.coefdtmin_input.setHelpText(utils.__(constants.HELP_COEFDTMIN))
        self.coefdtmin_input.setMaxLength(10)

        self.coefdtmin_input.focus.connect(self.on_help_focus)

        self.coefdtmin_input.setText(str(self.data['coefdtmin']))
        self.coefdtmin_layout.addWidget(self.coefdtmin_label)
        self.coefdtmin_layout.addWidget(self.coefdtmin_input)

        # Initial time step
        self.dtiniauto_layout = QtGui.QHBoxLayout()
        self.dtiniauto_chk = QtGui.QCheckBox("Initial time step auto")
        if self.data['dtini_auto']:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.dtiniauto_chk.toggled.connect(self.on_dtiniauto_check)
        self.dtiniauto_layout.addWidget(self.dtiniauto_chk)
        self.dtini_layout = QtGui.QHBoxLayout()
        self.dtini_label = QtGui.QLabel("Initial time step: ")
        self.dtini_input = FocusableLineEdit()
        self.dtini_input.setHelpText(utils.__(constants.HELP_DTINI))
        self.dtini_input.setMaxLength(10)

        self.dtini_input.focus.connect(self.on_help_focus)

        self.dtini_input.setText(str(self.data['dtini']))
        self.dtini_label2 = QtGui.QLabel("seconds")
        self.dtini_layout.addWidget(self.dtini_label)
        self.dtini_layout.addWidget(self.dtini_input)
        self.dtini_layout.addWidget(self.dtini_label2)
        self.on_dtiniauto_check()

        # Minimium time step
        self.dtminauto_layout = QtGui.QHBoxLayout()
        self.dtminauto_chk = QtGui.QCheckBox("Minimum time step: ")
        if self.data['dtmin_auto']:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.dtminauto_chk.toggled.connect(self.on_dtminauto_check)
        self.dtminauto_layout.addWidget(self.dtminauto_chk)
        self.dtmin_layout = QtGui.QHBoxLayout()
        self.dtmin_label = QtGui.QLabel("Minimium time step: ")
        self.dtmin_input = FocusableLineEdit()
        self.dtmin_input.setHelpText(utils.__(constants.HELP_DTMIN))
        self.dtmin_input.setMaxLength(10)

        self.dtmin_input.focus.connect(self.on_help_focus)

        self.dtmin_input.setText(str(self.data['dtmin']))
        self.dtmin_label2 = QtGui.QLabel("seconds")
        self.dtmin_layout.addWidget(self.dtmin_label)
        self.dtmin_layout.addWidget(self.dtmin_input)
        self.dtmin_layout.addWidget(self.dtmin_label2)
        self.on_dtminauto_check()

        # Fixed DT file
        self.dtfixed_layout = QtGui.QHBoxLayout()
        self.dtfixed_label = QtGui.QLabel("Fixed DT file: ")
        self.dtfixed_input = QtGui.QLineEdit()
        self.dtfixed_input.setText(str(self.data['dtfixed']))
        self.dtfixed_label2 = QtGui.QLabel("file")
        self.dtfixed_layout.addWidget(self.dtfixed_label)
        self.dtfixed_layout.addWidget(self.dtfixed_input)
        self.dtfixed_layout.addWidget(self.dtfixed_label2)

        # Velocity of particles
        self.dtallparticles_layout = QtGui.QHBoxLayout()
        self.dtallparticles_label = QtGui.QLabel("Velocity of particles: ")
        self.dtallparticles_input = QtGui.QLineEdit()
        self.dtallparticles_input.setMaxLength(1)
        self.dtallparticles_validator = QtGui.QIntValidator(0, 1, self.dtallparticles_input)
        self.dtallparticles_input.setText(str(self.data['dtallparticles']))
        self.dtallparticles_input.setValidator(self.dtallparticles_validator)
        self.dtallparticles_label2 = QtGui.QLabel("[0,1]")
        self.dtallparticles_layout.addWidget(self.dtallparticles_label)
        self.dtallparticles_layout.addWidget(self.dtallparticles_input)
        self.dtallparticles_layout.addWidget(self.dtallparticles_label2)

        # Time of simulation
        self.timemax_layout = QtGui.QHBoxLayout()
        self.timemax_label = QtGui.QLabel("Time of simulation: ")
        self.timemax_input = FocusableLineEdit()
        self.timemax_input.setHelpText(utils.__(constants.HELP_TIMEMAX))
        self.timemax_input.setMaxLength(10)

        self.timemax_input.focus.connect(self.on_help_focus)

        self.timemax_input.setText(str(self.data['timemax']))
        self.timemax_label2 = QtGui.QLabel("seconds")
        self.timemax_layout.addWidget(self.timemax_label)
        self.timemax_layout.addWidget(self.timemax_input)
        self.timemax_layout.addWidget(self.timemax_label2)

        # Time out data
        self.timeout_layout = QtGui.QHBoxLayout()
        self.timeout_label = QtGui.QLabel("Time out data: ")
        self.timeout_input = FocusableLineEdit()
        self.timeout_input.setHelpText(utils.__(constants.HELP_TIMEOUT))
        self.timeout_input.setMaxLength(10)

        self.timeout_input.focus.connect(self.on_help_focus)

        self.timeout_input.setText(str(self.data['timeout']))
        self.timeout_label2 = QtGui.QLabel("seconds")
        self.timeout_layout.addWidget(self.timeout_label)
        self.timeout_layout.addWidget(self.timeout_input)
        self.timeout_layout.addWidget(self.timeout_label2)

        # Max parts out allowed
        self.partsoutmax_layout = QtGui.QHBoxLayout()
        self.partsoutmax_label = QtGui.QLabel("Max parts out allowed (%): ")
        self.partsoutmax_input = FocusableLineEdit()
        self.partsoutmax_input.setHelpText(utils.__(constants.HELP_PARTSOUTMAX))
        self.partsoutmax_input.setMaxLength(10)

        self.partsoutmax_input.focus.connect(self.on_help_focus)

        self.partsoutmax_input.setText(str(float(self.data['partsoutmax']) * 100))
        self.partsoutmax_layout.addWidget(self.partsoutmax_label)
        self.partsoutmax_layout.addWidget(self.partsoutmax_input)

        # Minimum rhop valid
        self.rhopoutmin_layout = QtGui.QHBoxLayout()
        self.rhopoutmin_label = QtGui.QLabel("Minimum rhop valid: ")
        self.rhopoutmin_input = FocusableLineEdit()
        self.rhopoutmin_input.setHelpText(utils.__(constants.HELP_RHOPOUTMIN))
        self.rhopoutmin_input.setMaxLength(10)

        self.rhopoutmin_input.focus.connect(self.on_help_focus)

        self.rhopoutmin_input.setText(str(self.data['rhopoutmin']))
        self.rhopoutmin_label2 = QtGui.QLabel(
            "kg/m<span style='vertical-align:super'>3</span>")
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_input)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label2)

        # Maximum rhop valid
        self.rhopoutmax_layout = QtGui.QHBoxLayout()
        self.rhopoutmax_label = QtGui.QLabel("Maximum rhop valid: ")
        self.rhopoutmax_input = FocusableLineEdit()
        self.rhopoutmax_input.setHelpText(utils.__(constants.HELP_RHOPOUTMAX))
        self.rhopoutmax_input.setMaxLength(10)

        self.rhopoutmax_input.focus.connect(self.on_help_focus)

        self.rhopoutmax_input.setText(str(self.data['rhopoutmax']))
        self.rhopoutmax_label2 = QtGui.QLabel(
            "kg/m<span style='vertical-align:super'>3</span>")
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_input)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label2)

        self.period_x_layout = QtGui.QVBoxLayout()
        self.period_x_chk = QtGui.QCheckBox("X periodicity")
        #self.period_x_chk.setToolTip(utils.__(constants.PERIODX))
        self.period_x_inc_layout = QtGui.QHBoxLayout()
        self.period_x_inc_x_label = QtGui.QLabel("X Increment")
        self.period_x_inc_x_input = QtGui.QLineEdit("0")
        self.period_x_inc_y_label = QtGui.QLabel("Y Increment")
        self.period_x_inc_y_label.setToolTip(utils.__(constants.YINCEMENTX))
        self.period_x_inc_y_input = QtGui.QLineEdit("0")
        self.period_x_inc_z_label = QtGui.QLabel("Z Increment")
        self.period_x_inc_z_label.setToolTip(utils.__(constants.ZINCREMENTX))
        self.period_x_inc_z_input = QtGui.QLineEdit("0")
        self.period_x_inc_layout.addWidget(self.period_x_inc_x_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_x_input)
        self.period_x_inc_layout.addWidget(self.period_x_inc_y_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_y_input)
        self.period_x_inc_layout.addWidget(self.period_x_inc_z_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_z_input)
        self.period_x_layout.addWidget(self.period_x_chk)
        self.period_x_layout.addLayout(self.period_x_inc_layout)
        self.period_x_chk.stateChanged.connect(self.on_period_x_chk)

        try:
            self.period_x_chk.setChecked(self.data["period_x"][0])
            self.period_x_inc_x_input.setText(str(self.data["period_x"][1]))
            self.period_x_inc_y_input.setText(str(self.data["period_x"][2]))
            self.period_x_inc_z_input.setText(str(self.data["period_x"][3]))
        except:
            pass

        # Change the state of periodicity input on window open
        self.on_period_x_chk()

        self.period_y_layout = QtGui.QVBoxLayout()
        self.period_y_chk = QtGui.QCheckBox("Y periodicity")
        #self.period_y_chk.setToolTip(utils.__(constants.PERIODY))
        self.period_y_inc_layout = QtGui.QHBoxLayout()
        self.period_y_inc_x_label = QtGui.QLabel("X Increment")
        self.period_y_inc_x_label.setToolTip(utils.__(constants.XINCREMENTY))
        self.period_y_inc_x_input = QtGui.QLineEdit("0")
        self.period_y_inc_y_label = QtGui.QLabel("Y Increment")
        self.period_y_inc_y_input = QtGui.QLineEdit("0")
        self.period_y_inc_z_label = QtGui.QLabel("Z Increment")
        self.period_y_inc_z_label.setToolTip(utils.__(constants.XINCREMENTY))
        self.period_y_inc_z_input = QtGui.QLineEdit("0")
        self.period_y_inc_layout.addWidget(self.period_y_inc_x_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_x_input)
        self.period_y_inc_layout.addWidget(self.period_y_inc_y_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_y_input)
        self.period_y_inc_layout.addWidget(self.period_y_inc_z_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_z_input)
        self.period_y_layout.addWidget(self.period_y_chk)
        self.period_y_layout.addLayout(self.period_y_inc_layout)
        self.period_y_chk.stateChanged.connect(self.on_period_y_chk)

        try:
            self.period_y_chk.setChecked(self.data["period_y"][0])
            self.period_y_inc_x_input.setText(str(self.data["period_y"][1]))
            self.period_y_inc_y_input.setText(str(self.data["period_y"][2]))
            self.period_y_inc_z_input.setText(str(self.data["period_y"][3]))
        except:
            pass

        # Change the state of periodicity input on window open
        self.on_period_y_chk()

        self.period_z_layout = QtGui.QVBoxLayout()
        self.period_z_chk = QtGui.QCheckBox("Z periodicity")
        #self.period_z_chk.setToolTip(utils.__(constants.PERIODZ))
        self.period_z_inc_layout = QtGui.QHBoxLayout()
        self.period_z_inc_x_label = QtGui.QLabel("X Increment")
        self.period_z_inc_x_label.setToolTip(utils.__(constants.XINCREMENTZ))
        self.period_z_inc_x_input = QtGui.QLineEdit("0")
        self.period_z_inc_y_label = QtGui.QLabel("Y Increment")
        self.period_z_inc_y_label.setToolTip(utils.__(constants.YINCEMENTZ))
        self.period_z_inc_y_input = QtGui.QLineEdit("0")
        self.period_z_inc_z_label = QtGui.QLabel("Z Increment")
        self.period_z_inc_z_input = QtGui.QLineEdit("0")
        self.period_z_inc_layout.addWidget(self.period_z_inc_x_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_x_input)
        self.period_z_inc_layout.addWidget(self.period_z_inc_y_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_y_input)
        self.period_z_inc_layout.addWidget(self.period_z_inc_z_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_z_input)
        self.period_z_layout.addWidget(self.period_z_chk)
        self.period_z_layout.addLayout(self.period_z_inc_layout)
        self.period_z_chk.stateChanged.connect(self.on_period_z_chk)

        try:
            self.period_z_chk.setChecked(self.data["period_z"][0])
            self.period_z_inc_x_input.setText(str(self.data["period_z"][1]))
            self.period_z_inc_y_input.setText(str(self.data["period_z"][2]))
            self.period_z_inc_z_input.setText(str(self.data["period_z"][3]))
        except:
            pass

        # Change the state of periodicity input on window open
        self.on_period_z_chk()

        # Simulation domain
        self.simdomain_layout = QtGui.QVBoxLayout()
        self.simdomain_chk = QtGui.QCheckBox("Simulation Domain")
        try:
          self.simdomain_chk.setChecked(self.data['simdomain_chk'])
        except:
            pass
        self.simdomain_posmin_layout = QtGui.QHBoxLayout()
        self.simdomain_posminx_layout = QtGui.QVBoxLayout()
        self.simdomain_posminy_layout = QtGui.QVBoxLayout()
        self.simdomain_posminz_layout = QtGui.QVBoxLayout()
        self.simdomain_posmax_layout = QtGui.QHBoxLayout()
        self.simdomain_posmaxx_layout = QtGui.QVBoxLayout()
        self.simdomain_posmaxy_layout = QtGui.QVBoxLayout()
        self.simdomain_posmaxz_layout = QtGui.QVBoxLayout()
        self.simdomain_posmin_label = QtGui.QLabel("Minimum position(x, y, z): ")
        self.simdomain_posminx_combobox = QtGui.QComboBox()
        self.simdomain_posminx_combobox.insertItems(0, ['Default', 'Numeric value', 'Default - num', 'Default - %'])
        self.simdomain_posminx_line_edit = QtGui.QLineEdit(str(self.data['posmin'][1]))
        self.simdomain_posminy_combobox = QtGui.QComboBox()
        self.simdomain_posminy_combobox.insertItems(0, ['Default', 'Numeric value', 'Default - num', 'Default - %'])
        self.simdomain_posminy_line_edit = QtGui.QLineEdit(str(self.data['posmin'][3]))
        self.simdomain_posminz_combobox = QtGui.QComboBox()
        self.simdomain_posminz_combobox.insertItems(0, ['Default', 'Numeric value', 'Default - num', 'Default - %'])
        self.simdomain_posminz_line_edit = QtGui.QLineEdit(str(self.data['posmin'][5]))
        self.simdomain_posminx_layout.addWidget(self.simdomain_posminx_combobox)
        self.simdomain_posminx_layout.addWidget(self.simdomain_posminx_line_edit)
        self.simdomain_posminy_layout.addWidget(self.simdomain_posminy_combobox)
        self.simdomain_posminy_layout.addWidget(self.simdomain_posminy_line_edit)
        self.simdomain_posminz_layout.addWidget(self.simdomain_posminz_combobox)
        self.simdomain_posminz_layout.addWidget(self.simdomain_posminz_line_edit)
        self.simdomain_posmin_layout.addWidget(self.simdomain_posmin_label)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminx_layout)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminy_layout)
        self.simdomain_posmin_layout.addLayout(self.simdomain_posminz_layout)
        self.simdomain_posmax_label = QtGui.QLabel("Maximum position(x, y, z): ")
        self.simdomain_posmaxx_combobox = QtGui.QComboBox()
        self.simdomain_posmaxx_combobox.insertItems(0, ['Default', 'Numeric value', 'Default + num', 'Default + %'])
        self.simdomain_posmaxx_line_edit = QtGui.QLineEdit(str(self.data['posmax'][1]))
        self.simdomain_posmaxy_combobox = QtGui.QComboBox()
        self.simdomain_posmaxy_combobox.insertItems(0, ['Default', 'Numeric value', 'Default + num', 'Default + %'])
        self.simdomain_posmaxy_line_edit = QtGui.QLineEdit(str(self.data['posmax'][3]))
        self.simdomain_posmaxz_combobox = QtGui.QComboBox()
        self.simdomain_posmaxz_combobox.insertItems(0, ['Default', 'Numeric value', 'Default + num', 'Default + %'])
        self.simdomain_posmaxz_line_edit = QtGui.QLineEdit(str(self.data['posmax'][5]))
        self.simdomain_posmaxx_layout.addWidget(self.simdomain_posmaxx_combobox)
        self.simdomain_posmaxx_layout.addWidget(self.simdomain_posmaxx_line_edit)
        self.simdomain_posmaxy_layout.addWidget(self.simdomain_posmaxy_combobox)
        self.simdomain_posmaxy_layout.addWidget(self.simdomain_posmaxy_line_edit)
        self.simdomain_posmaxz_layout.addWidget(self.simdomain_posmaxz_combobox)
        self.simdomain_posmaxz_layout.addWidget(self.simdomain_posmaxz_line_edit)
        self.simdomain_posmax_layout.addWidget(self.simdomain_posmax_label)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxx_layout)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxy_layout)
        self.simdomain_posmax_layout.addLayout(self.simdomain_posmaxz_layout)

        try:
            self.simdomain_posminx_combobox.setCurrentIndex(self.data['posmin'][0])
            self.simdomain_posminy_combobox.setCurrentIndex(self.data['posmin'][2])
            self.simdomain_posminz_combobox.setCurrentIndex(self.data['posmin'][4])
            self.simdomain_posmaxx_combobox.setCurrentIndex(self.data['posmax'][0])
            self.simdomain_posmaxy_combobox.setCurrentIndex(self.data['posmax'][2])
            self.simdomain_posmaxz_combobox.setCurrentIndex(self.data['posmax'][4])
        except:
            pass

        self.simdomain_layout.addWidget(self.simdomain_chk)
        self.simdomain_layout.addLayout(self.simdomain_posmin_layout)
        self.simdomain_layout.addLayout(self.simdomain_posmax_layout)
        self.simdomain_chk.stateChanged.connect(self.on_simdomain_chk)
        self.simdomain_posmaxx_combobox.currentIndexChanged.connect(self.on_posmaxx_changed)
        self.simdomain_posmaxy_combobox.currentIndexChanged.connect(self.on_posmaxy_changed)
        self.simdomain_posmaxz_combobox.currentIndexChanged.connect(self.on_posmaxz_changed)
        self.simdomain_posminx_combobox.currentIndexChanged.connect(self.on_posminx_changed)
        self.simdomain_posminy_combobox.currentIndexChanged.connect(self.on_posminy_changed)
        self.simdomain_posminz_combobox.currentIndexChanged.connect(self.on_posminz_changed)

        self.on_simdomain_chk()
        self.on_posmaxx_changed()
        self.on_posmaxy_changed()
        self.on_posmaxz_changed()
        self.on_posminx_changed()
        self.on_posminy_changed()
        self.on_posminz_changed()

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Help Text Layout definition
        self.ep_helpText_layout = QtGui.QHBoxLayout()
        self.ep_helpText_layout.addWidget(self.help_window)
        self.ep_helpText_layout.setStretchFactor(self.help_window, 0)

        # Button layout definition
        self.ep_button_layout = QtGui.QHBoxLayout()
        self.ep_button_layout.addStretch(1)
        self.ep_button_layout.addWidget(self.ok_button)
        self.ep_button_layout.addWidget(self.cancel_button)

        # START Main layout definition and composition.
        self.ep_main_layout_scroll = QtGui.QScrollArea()
        self.ep_main_layout_scroll_widget = QtGui.QWidget()
        self.ep_main_layout = QtGui.QVBoxLayout()
        self.ep_main_layout.addLayout(self.posdouble_layout)
        self.ep_main_layout.addLayout(self.stepalgorithm_layout)
        self.ep_main_layout.addLayout(self.verletsteps_layout)
        self.ep_main_layout.addLayout(self.kernel_layout)
        self.ep_main_layout.addLayout(self.viscotreatment_layout)
        self.ep_main_layout.addLayout(self.visco_layout)
        self.ep_main_layout.addLayout(self.viscoboundfactor_layout)
        self.ep_main_layout.addLayout(self.deltasph_en_layout)
        self.ep_main_layout.addLayout(self.deltasph_layout)
        self.ep_main_layout.addLayout(self.shifting_layout)
        self.ep_main_layout.addLayout(self.shiftcoef_layout)
        self.ep_main_layout.addLayout(self.shifttfs_layout)
        self.ep_main_layout.addLayout(self.rigidalgorithm_layout)
        self.ep_main_layout.addLayout(self.ftpause_layout)
        self.ep_main_layout.addLayout(self.dtiniauto_layout)
        self.ep_main_layout.addLayout(self.dtini_layout)
        self.ep_main_layout.addLayout(self.dtminauto_layout)
        self.ep_main_layout.addLayout(self.dtmin_layout)
        self.ep_main_layout.addLayout(self.coefdtmin_layout)
        self.ep_main_layout.addLayout(self.timemax_layout)
        self.ep_main_layout.addLayout(self.timeout_layout)
        self.ep_main_layout.addLayout(self.partsoutmax_layout)
        self.ep_main_layout.addLayout(self.rhopoutmin_layout)
        self.ep_main_layout.addLayout(self.rhopoutmax_layout)
        self.ep_main_layout.addLayout(self.period_x_layout)
        self.ep_main_layout.addLayout(self.period_y_layout)
        self.ep_main_layout.addLayout(self.period_z_layout)
        self.ep_main_layout.addLayout(self.simdomain_layout)

        self.ep_main_layout_scroll_widget.setLayout(self.ep_main_layout)
        self.ep_main_layout_scroll.setWidget(self.ep_main_layout_scroll_widget)
        self.ep_main_layout_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)

        self.execparams_window_layout = QtGui.QVBoxLayout()
        self.execparams_window_layout.addWidget(self.ep_main_layout_scroll)
        self.execparams_window_layout.addLayout(self.ep_helpText_layout)
        self.execparams_window_layout.addLayout(self.ep_button_layout)
        self.setLayout(self.execparams_window_layout)
        # END Main layout definition and composition.

    def on_help_focus(self, help_text):
        self.help_window.setText(help_text)

    # Step Algorithm
    def on_step_change(self, index):
        if index == 1:
            self.verletsteps_input.setEnabled(True)
        else:
            self.verletsteps_input.setEnabled(False)

    def on_viscotreatment_change(self, index):
        self.visco_input.setText("0.01" if index == 0 else "0.000001")
        self.visco_label.setText("Viscosity value (alpha): "
                            if index == 0 else "Kinematic viscosity: ")
        self.visco_units_label.setText(
            "" if index == 0 else
            "m<span style='vertical-align:super'>2</span>/s")

    # DeltaSPH enabled selector
    def on_deltasph_en_change(self, index):
        if index == 0:
            self.deltasph_input.setEnabled(False)
        else:
            self.deltasph_input.setEnabled(True)
            self.deltasph_input.setText("0.1")

    # Shifting mode
    def on_shifting_change(self, index):
        if index == 0:
            self.shiftcoef_input.setEnabled(False)
            self.shifttfs_input.setEnabled(False)
        else:
            self.shiftcoef_input.setEnabled(True)
            self.shifttfs_input.setEnabled(True)

    # Controls if user selected auto b or not enabling/disablen b custom value
    def on_dtiniauto_check(self):
        # introduction
        if self.dtiniauto_chk.isChecked():
            self.dtini_input.setEnabled(False)
        else:
            self.dtini_input.setEnabled(True)

    # Controls if user selected auto b or not enabling/disablen b custom value
    def on_dtminauto_check(self):
        # introduction
        if self.dtminauto_chk.isChecked():
            self.dtmin_input.setEnabled(False)
        else:
            self.dtmin_input.setEnabled(True)

    # Periodicity in X
    def on_period_x_chk(self):
        if self.period_x_chk.isChecked():
            self.period_x_inc_x_input.setEnabled(False)
            self.period_x_inc_y_input.setEnabled(True)
            self.period_x_inc_z_input.setEnabled(True)
        else:
            self.period_x_inc_x_input.setEnabled(False)
            self.period_x_inc_y_input.setEnabled(False)
            self.period_x_inc_z_input.setEnabled(False)

    # Periodicity in Y
    def on_period_y_chk(self):
        if self.period_y_chk.isChecked():
            self.period_y_inc_x_input.setEnabled(True)
            self.period_y_inc_y_input.setEnabled(False)
            self.period_y_inc_z_input.setEnabled(True)
        else:
            self.period_y_inc_x_input.setEnabled(False)
            self.period_y_inc_y_input.setEnabled(False)
            self.period_y_inc_z_input.setEnabled(False)

    # Periodicity in X
    def on_period_z_chk(self):
        if self.period_z_chk.isChecked():
            self.period_z_inc_x_input.setEnabled(True)
            self.period_z_inc_y_input.setEnabled(True)
            self.period_z_inc_z_input.setEnabled(False)
        else:
            self.period_z_inc_x_input.setEnabled(False)
            self.period_z_inc_y_input.setEnabled(False)
            self.period_z_inc_z_input.setEnabled(False)

    def on_simdomain_chk(self):
        if self.simdomain_chk.isChecked():
            self.simdomain_posminx_combobox.setEnabled(True)
            self.simdomain_posminy_combobox.setEnabled(True)
            self.simdomain_posminz_combobox.setEnabled(True)
            self.simdomain_posmaxx_combobox.setEnabled(True)
            self.simdomain_posmaxy_combobox.setEnabled(True)
            self.simdomain_posmaxz_combobox.setEnabled(True)
            if self.simdomain_posminx_combobox.currentIndex() != 0:
                self.simdomain_posminx_line_edit.setEnabled(True)
            else:
                self.simdomain_posminx_line_edit.setEnabled(False)

            if self.simdomain_posminy_combobox.currentIndex() != 0:
                self.simdomain_posminy_line_edit.setEnabled(True)
            else:
                self.simdomain_posminy_line_edit.setEnabled(False)

            if self.simdomain_posminz_combobox.currentIndex() != 0:
                self.simdomain_posminz_line_edit.setEnabled(True)
            else:
                self.simdomain_posminz_line_edit.setEnabled(False)

            if self.simdomain_posmaxx_combobox.currentIndex() != 0:
                self.simdomain_posmaxx_line_edit.setEnabled(True)
            else:
                self.simdomain_posmaxx_line_edit.setEnabled(False)

            if self.simdomain_posmaxy_combobox.currentIndex() != 0:
                self.simdomain_posmaxy_line_edit.setEnabled(True)
            else:
                self.simdomain_posmaxy_line_edit.setEnabled(False)

            if self.simdomain_posmaxz_combobox.currentIndex() != 0:
                self.simdomain_posmaxz_line_edit.setEnabled(True)
            else:
                self.simdomain_posmaxz_line_edit.setEnabled(False)
        else:
            self.simdomain_posminx_combobox.setEnabled(False)
            self.simdomain_posminy_combobox.setEnabled(False)
            self.simdomain_posminz_combobox.setEnabled(False)
            self.simdomain_posmaxx_combobox.setEnabled(False)
            self.simdomain_posmaxy_combobox.setEnabled(False)
            self.simdomain_posmaxz_combobox.setEnabled(False)
            self.simdomain_posminx_line_edit.setEnabled(False)
            self.simdomain_posminy_line_edit.setEnabled(False)
            self.simdomain_posminz_line_edit.setEnabled(False)
            self.simdomain_posmaxx_line_edit.setEnabled(False)
            self.simdomain_posmaxy_line_edit.setEnabled(False)
            self.simdomain_posmaxz_line_edit.setEnabled(False)

    def on_posminx_changed(self):
        if self.simdomain_posminx_combobox.currentIndex() == 0:
            self.simdomain_posminx_line_edit.setEnabled(False)
        else:
            self.simdomain_posminx_line_edit.setEnabled(True)

    def on_posminy_changed(self):
        if self.simdomain_posminy_combobox.currentIndex() == 0:
            self.simdomain_posminy_line_edit.setEnabled(False)
        else:
            self.simdomain_posminy_line_edit.setEnabled(True)

    def on_posminz_changed(self):
        if self.simdomain_posminz_combobox.currentIndex() == 0:
            self.simdomain_posminz_line_edit.setEnabled(False)
        else:
            self.simdomain_posminz_line_edit.setEnabled(True)

    def on_posmaxx_changed(self):
        if self.simdomain_posmaxx_combobox.currentIndex() == 0:
            self.simdomain_posmaxx_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxx_line_edit.setEnabled(True)

    def on_posmaxy_changed(self):
        if self.simdomain_posmaxy_combobox.currentIndex() == 0:
            self.simdomain_posmaxy_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxy_line_edit.setEnabled(True)

    def on_posmaxz_changed(self):
        if self.simdomain_posmaxz_combobox.currentIndex() == 0:
            self.simdomain_posmaxz_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxz_line_edit.setEnabled(True)

    # ------------ Button behaviour definition --------------
    def on_ok(self):
        self.data['posdouble'] = str(self.posdouble_input.currentIndex())
        self.data['stepalgorithm'] = str(self.stepalgorithm_input.currentIndex() + 1)
        self.data['verletsteps'] = self.verletsteps_input.text()
        self.data['kernel'] = str(self.kernel_input.currentIndex() + 1)
        self.data['viscotreatment'] = self.viscotreatment_input.currentIndex() + 1
        self.data['visco'] = self.visco_input.text()
        self.data['viscoboundfactor'] = self.viscoboundfactor_input.text()
        self.data['deltasph'] = self.deltasph_input.text()
        self.data['deltasph_en'] = self.deltasph_en_input.currentIndex()
        self.data['shifting'] = str(self.shifting_input.currentIndex())
        self.data['shiftcoef'] = self.shiftcoef_input.text()
        self.data['shifttfs'] = self.shifttfs_input.text()
        self.data['rigidalgorithm'] = str(self.rigidalgorithm_input.currentIndex() + 1)
        self.data['ftpause'] = self.ftpause_input.text()
        self.data['coefdtmin'] = self.coefdtmin_input.text()
        self.data['dtini'] = self.dtini_input.text()
        self.data['dtini_auto'] = self.dtiniauto_chk.isChecked()
        self.data['dtmin'] = self.dtmin_input.text()
        self.data['dtmin'] = self.dtmin_input.text()
        self.data['dtmin_auto'] = self.dtminauto_chk.isChecked()
        self.data['dtfixed'] = self.dtfixed_input.text()
        self.data['dtallparticles'] = self.dtallparticles_input.text()
        self.data['timemax'] = self.timemax_input.text()
        self.data['timeout'] = self.timeout_input.text()
        self.data['partsoutmax'] = str(float(self.partsoutmax_input.text()) / 100)
        self.data['rhopoutmin'] = self.rhopoutmin_input.text()
        self.data['rhopoutmax'] = self.rhopoutmax_input.text()

        self.data['period_x'] = [
            self.period_x_chk.isChecked(),
            float(self.period_x_inc_x_input.text()),
            float(self.period_x_inc_y_input.text()),
            float(self.period_x_inc_z_input.text())
        ]
        self.data['period_y'] = [
            self.period_y_chk.isChecked(),
            float(self.period_y_inc_x_input.text()),
            float(self.period_y_inc_y_input.text()),
            float(self.period_y_inc_z_input.text())
        ]
        self.data['period_z'] = [
            self.period_z_chk.isChecked(),
            float(self.period_z_inc_x_input.text()),
            float(self.period_z_inc_y_input.text()),
            float(self.period_z_inc_z_input.text())
        ]

        if self.simdomain_chk.isChecked():
            self.data['simdomain_chk'] = True
            self.data['posmin'] = [
                self.simdomain_posminx_combobox.currentIndex(),
                float(self.simdomain_posminx_line_edit.text()),
                self.simdomain_posminy_combobox.currentIndex(),
                float(self.simdomain_posminy_line_edit.text()),
                self.simdomain_posminz_combobox.currentIndex(),
                float(self.simdomain_posminz_line_edit.text())
            ]

            self.data['posmax'] = [
                self.simdomain_posmaxx_combobox.currentIndex(),
                float(self.simdomain_posmaxx_line_edit.text()),
                self.simdomain_posmaxy_combobox.currentIndex(),
                float(self.simdomain_posmaxy_line_edit.text()),
                self.simdomain_posmaxz_combobox.currentIndex(),
                float(self.simdomain_posmaxz_line_edit.text())
            ]
            self.data['incz'] = 0
            self.simulation_domain()
        else:
            self.data['simdomain_chk'] = False
            self.data['posmin'] = [0, 0.0, 0, 0.0, 0, 0.0]
            self.data['posmax'] = [0, 0.0, 0, 0.0, 0, 0.0]

            utils.log("Execution Parameters changed")
        self.accept()

    def on_cancel(self):
        utils.log("Execution Parameters not changed")
        self.reject()

    def simulation_domain(self):
        if self.data['posmin'][0] == 0:
            self.data['posminxml'][0] = "default"
        elif self.data['posmin'][0] == 1:
            self.data['posminxml'][0] = str(self.data['posmin'][1])
        elif self.data['posmin'][0] == 2:
            self.data['posminxml'][0] = 'default-' + str(self.data['posmin'][1])
        elif data['posmin'][0] == 3:
            self.data['posminxml'][0] = 'default-' + str(self.data['posmin'][1]) + "%"

        if self.data['posmin'][2] == 0:
            self.data['posminxml'][1] = "default"
        elif self.data['posmin'][2] == 1:
            self.data['posminxml'][1] = str(self.data['posmin'][3])
        elif self.data['posmin'][2] == 2:
            self.data['posminxml'][1] = 'default-' + str(self.data['posmin'][3])
        elif self.data['posmin'][2] == 3:
            self.data['posminxml'][1] = 'default-' + str(self.data['posmin'][3]) + "%"

        if self.data['posmin'][4] == 0:
            self.data['posminxml'][2] = "default"
        elif self.data['posmin'][4] == 1:
            self.data['posminxml'][2] = str(self.data['posmin'][5])
        elif self.data['posmin'][4] == 2:
            self.data['posminxml'][2] = 'default-' + str(self.data['posmin'][5])
        elif self.data['posmin'][4] == 3:
            self.data['posminxml'][2] = 'default-' + str(self.data['posmin'][5]) + "%"

        if self.data['posmax'][0] == 0:
            self.data['posmaxxml'][0] = "default"
        elif self.data['posmax'][0] == 1:
            self.data['posmaxxml'][0] = str(self.data['posmax'][1])
        elif self.data['posmax'][0] == 2:
            self.data['posmaxxml'][0] = 'default+' + str(self.data['posmax'][1])
        elif data['posmax'][0] == 3:
            self.data['posmaxxml'][0] = 'default+' + str(self.data['posmax'][1]) + "%"

        if self.data['posmax'][2] == 0:
            self.data['posmaxxml'][1] = "default"
        elif self.data['posmax'][2] == 1:
            self.data['posmaxxml'][1] = str(self.data['posmax'][3])
        elif self.data['posmax'][2] == 2:
            self.data['posmaxxml'][1] = 'default+' + str(self.data['posmax'][3])
        elif self.data['posmax'][2] == 3:
            self.data['posmaxxml'][1] = 'default+' + str(self.data['posmax'][3]) + "%"

        if self.data['posmax'][4] == 0:
            self.data['posmaxxml'][2] = "default"
        elif self.data['posmax'][4] == 1:
            self.data['posmaxxml'][2] = str(self.data['posmax'][5])
        elif self.data['posmax'][4] == 2:
            self.data['posmaxxml'][2] = 'default+' + str(self.data['posmax'][5])
        elif self.data['posmax'][4] == 3:
            self.data['posmaxxml'][2] = 'default+' + str(self.data['posmax'][5]) + "%"


class MeasureToolGridDialog(QtGui.QDialog):
    """ Defines grid point button behaviour."""
    def __init__(self, temp_data):
        super(MeasureToolGridDialog, self).__init__()

        self.temp_data = temp_data

        self.setWindowTitle(__("MeasureTool Points"))
        self.measuregrid_tool_layout = QtGui.QVBoxLayout()
        self.mgrid_table = QtGui.QTableWidget()
        self.mgrid_table.setRowCount(100)
        self.mgrid_table.setColumnCount(12)
        self.mgrid_table.verticalHeader().setVisible(False)
        self.mgrid_table.setHorizontalHeaderLabels([
            "BeginX",
            "BeginY",
            "BeginZ",
            "StepX",
            "StepY",
            "StepZ",
            "CountX",
            "CountY",
            "CountZ",
            "FinalX",
            "FinalY",
            "FinalZ"
        ])

        for i, grid in enumerate(self.temp_data['measuretool_grid']):
            for j in range(0, self.mgrid_table.columnCount()):
                self.mgrid_table.setItem(i, j, QtGui.QTableWidgetItem(str(grid[j])))
                if j > 8:
                    self.mgrid_table.setItem(i, j, QtGui.QTableWidgetItem(str(grid[j])))
                    self.mgrid_table.item(i, j).setBackground(QtGui.QColor(210, 255, 255))
                    self.mgrid_table.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        if self.temp_data['measuretool_grid'] == list():
            for self.mgrid_row in range(0, self.mgrid_table.rowCount()):
                self.mgrid_table.setItem(self.mgrid_row, 9, QtGui.QTableWidgetItem(""))
                self.mgrid_table.setItem(self.mgrid_row, 10, QtGui.QTableWidgetItem(""))
                self.mgrid_table.setItem(self.mgrid_row, 11, QtGui.QTableWidgetItem(""))
                self.mgrid_table.item(self.mgrid_row, 9).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 10).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 11).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # Compute possible final points
        self.on_mgrid_change(0, 0)

        self.mgrid_bt_layout = QtGui.QHBoxLayout()
        self.mgrid_cancel = QtGui.QPushButton(__("Cancel"))
        self.mgrid_accept = QtGui.QPushButton(__("OK"))
        self.mgrid_accept.clicked.connect(self.on_mgrid_accept)
        self.mgrid_cancel.clicked.connect(self.on_mgrid_cancel)

        self.mgrid_bt_layout.addWidget(self.mgrid_accept)
        self.mgrid_bt_layout.addWidget(self.mgrid_cancel)

        self.mgrid_table.cellChanged.connect(self.on_mgrid_change)

        self.measuregrid_tool_layout.addWidget(self.mgrid_table)
        self.measuregrid_tool_layout.addLayout(self.mgrid_bt_layout)

        self.setLayout(self.measuregrid_tool_layout)
        self.resize(1250, 400)
        self.exec_()

    def on_mgrid_change(self, row, column):
        """ Defines what happens when a field changes on the table"""
        if column > 8:
            return
        for self.mgrid_row in range(0, self.mgrid_table.rowCount()):
            try:
                self.current_grid = [
                    float(self.mgrid_table.item(self.mgrid_row, 0).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 1).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 2).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 3).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 4).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 5).text()),
                    int(self.mgrid_table.item(self.mgrid_row, 6).text()),
                    int(self.mgrid_table.item(self.mgrid_row, 7).text()),
                    int(self.mgrid_table.item(self.mgrid_row, 8).text())
                ]

                utils.debug(self.current_grid)

                # Make the operations to calculate final points
                self.mgrid_table.setItem(self.mgrid_row, 9, QtGui.QTableWidgetItem(str(
                    float(self.current_grid[0]) +
                    float(self.current_grid[6] - 1) *
                    float(self.current_grid[3])
                )))
                self.mgrid_table.setItem(self.mgrid_row, 10, QtGui.QTableWidgetItem(str(
                    float(self.current_grid[1]) +
                    float(self.current_grid[7] - 1) *
                    float(self.current_grid[4])
                )))
                self.mgrid_table.setItem(self.mgrid_row, 11, QtGui.QTableWidgetItem(str(
                    float(self.current_grid[2]) +
                    float(self.current_grid[8] - 1) *
                    float(self.current_grid[5])
                )))

                if self.current_grid[6] is 0:
                    self.mgrid_table.setItem(self.mgrid_row, 9, QtGui.QTableWidgetItem(str(
                        "0"
                    )))
                if self.current_grid[7] is 0:
                    self.mgrid_table.setItem(self.mgrid_row, 10, QtGui.QTableWidgetItem(str(
                        "0"
                    )))
                if self.current_grid[8] is 0:
                    self.mgrid_table.setItem(self.mgrid_row, 11, QtGui.QTableWidgetItem(str(
                        "0"
                    )))

                self.mgrid_table.item(self.mgrid_row, 9).setBackground(QtGui.QColor(210, 255, 255))
                self.mgrid_table.item(self.mgrid_row, 10).setBackground(QtGui.QColor(210, 255, 255))
                self.mgrid_table.item(self.mgrid_row, 11).setBackground(QtGui.QColor(210, 255, 255))
                # Those should not be used
                self.mgrid_table.item(self.mgrid_row, 9).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 10).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.mgrid_table.item(self.mgrid_row, 11).setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            except (ValueError, AttributeError):
                pass

    def on_mgrid_accept(self):
        """ MeasureTool point grid accept button behaviour."""
        self.temp_data['measuretool_grid'] = list()
        for self.mgrid_row in range(0, self.mgrid_table.rowCount()):
            try:
                self.current_grid = [
                    float(self.mgrid_table.item(self.mgrid_row, 0).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 1).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 2).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 3).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 4).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 5).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 6).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 7).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 8).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 9).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 10).text()),
                    float(self.mgrid_table.item(self.mgrid_row, 11).text())
                ]
                self.temp_data['measuretool_grid'].append(self.current_grid)
            except (ValueError, AttributeError):
                pass

        # Deletes the list of points (not compatible together)
        self.temp_data['measuretool_points'] = list()
        #self.temp_data['measuretool_grid'] = list()
        self.accept()

    def on_mgrid_cancel(self):
        """ MeasureTool point grid cancel button behaviour"""
        self.reject()


class DampingConfigDialog(QtGui.QDialog):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    def __init__(self, data, object_key):
        super(DampingConfigDialog, self).__init__()

        self.data = data
        self.object_key = object_key

        # Creates a dialog and 2 main buttons
        self.setWindowTitle("Damping configuration")
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")

        self.main_layout = QtGui.QVBoxLayout()

        self.enabled_checkbox = QtGui.QCheckBox("Enabled")

        self.main_groupbox = QtGui.QGroupBox("Damping parameters")
        self.main_groupbox_layout = QtGui.QVBoxLayout()

        self.limitmin_layout = QtGui.QHBoxLayout()
        self.limitmin_label = QtGui.QLabel("Limit Min. (X, Y, Z) (m): ")
        self.limitmin_input_x = QtGui.QLineEdit()
        self.limitmin_input_y = QtGui.QLineEdit()
        self.limitmin_input_z = QtGui.QLineEdit()
        [self.limitmin_layout.addWidget(x) for x in [self.limitmin_label, self.limitmin_input_x, self.limitmin_input_y, self.limitmin_input_z]]

        self.limitmax_layout = QtGui.QHBoxLayout()
        self.limitmax_label = QtGui.QLabel("Limit Max. (X, Y, Z) (m): ")
        self.limitmax_input_x = QtGui.QLineEdit()
        self.limitmax_input_y = QtGui.QLineEdit()
        self.limitmax_input_z = QtGui.QLineEdit()
        [self.limitmax_layout.addWidget(x) for x in [self.limitmax_label, self.limitmax_input_x, self.limitmax_input_y, self.limitmax_input_z]]

        self.overlimit_layout = QtGui.QHBoxLayout()
        self.overlimit_label = QtGui.QLabel("Overlimit (m): ")
        self.overlimit_input = QtGui.QLineEdit()
        [self.overlimit_layout.addWidget(x) for x in [self.overlimit_label, self.overlimit_input]]

        self.redumax_layout = QtGui.QHBoxLayout()
        self.redumax_label = QtGui.QLabel("Redumax: ")
        self.redumax_input = QtGui.QLineEdit()
        [self.redumax_layout.addWidget(x) for x in [self.redumax_label, self.redumax_input]]

        self.main_groupbox_layout.addLayout(self.limitmin_layout)
        self.main_groupbox_layout.addLayout(self.limitmax_layout)
        self.main_groupbox_layout.addLayout(self.overlimit_layout)
        self.main_groupbox_layout.addLayout(self.redumax_layout)

        self.main_groupbox.setLayout(self.main_groupbox_layout)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout.addWidget(self.enabled_checkbox)
        self.main_layout.addWidget(self.main_groupbox)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.enabled_checkbox.stateChanged.connect(self.on_enable_chk)
        [x.textChanged.connect(self.on_value_change) for x in [self.overlimit_input, self.redumax_input]]

        # Fill fields with case data
        self.enabled_checkbox.setChecked(self.data["damping"][object_key].enabled)
        self.group = FreeCAD.ActiveDocument.getObject(object_key)
        self.limitmin_input_x.setText(str(self.group.OutList[0].Start[0] / 1000))
        self.limitmin_input_y.setText(str(self.group.OutList[0].Start[1] / 1000))
        self.limitmin_input_z.setText(str(self.group.OutList[0].Start[2] / 1000))
        self.limitmax_input_x.setText(str(self.group.OutList[0].End[0] / 1000))
        self.limitmax_input_y.setText(str(self.group.OutList[0].End[1] / 1000))
        self.limitmax_input_z.setText(str(self.group.OutList[0].End[2] / 1000))
        self.overlimit_input.setText(str(self.group.OutList[1].Length.Value / 1000))
        self.redumax_input.setText(str(self.data["damping"][self.object_key].redumax))
        self.redumax_input.setText(str(self.data["damping"][self.object_key].redumax))
        self.on_enable_chk(
            QtCore.Qt.Checked if self.data["damping"][self.object_key].enabled else QtCore.Qt.Unchecked)

        self.exec_()

    # Window logic
    def on_ok(self):
        self.data["damping"][self.object_key].enabled = self.enabled_checkbox.isChecked()
        self.data["damping"][self.object_key].overlimit = float(self.overlimit_input.text())
        self.data["damping"][self.object_key].redumax = float(self.redumax_input.text())
        self.damping_group = FreeCAD.ActiveDocument.getObject(self.object_key)
        self.damping_group.OutList[0].Start = (float(self.limitmin_input_x.text()) * 1000,
                                          float(self.limitmin_input_y.text()) * 1000,
                                          float(self.limitmin_input_z.text()) * 1000)
        self.damping_group.OutList[0].End = (float(self.limitmax_input_x.text()) * 1000,
                                        float(self.limitmax_input_y.text()) * 1000,
                                        float(self.limitmax_input_z.text()) * 1000)
        self.damping_group.OutList[1].Start = self.damping_group.OutList[0].End

        self.overlimit_vector = FreeCAD.Vector(*self.damping_group.OutList[0].End) - FreeCAD.Vector(*self.damping_group.OutList[0].Start)
        self.overlimit_vector.normalize()
        self.overlimit_vector = self.overlimit_vector * self.data["damping"][self.object_key].overlimit
        self.overlimit_vector = self.overlimit_vector + FreeCAD.Vector(*self.damping_group.OutList[0].End)

        self.damping_group.OutList[1].End = (self.overlimit_vector.x, self.overlimit_vector.y, self.overlimit_vector.z)
        FreeCAD.ActiveDocument.recompute()
        self.accept()

    def on_cancel(self):
        self.reject()

    def on_enable_chk(self, state):
        if state == QtCore.Qt.Checked:
            self.main_groupbox.setEnabled(True)
        else:
            self.main_groupbox.setEnabled(False)

    def on_value_change(self):
        [x.setText(x.text().replace(",", ".")) for x in
         [self.overlimit_input, self.redumax_input, self.limitmin_input_x, self.limitmin_input_y, self.limitmin_input_z, self.limitmax_input_x,
          self.limitmax_input_y, self.limitmax_input_z]]


class ChronoConfigDialog(QtGui.QDialog):
    """ Defines the Chrono dialog window.
    Modifies data dictionary passed as parameter. """

    def __init__(self, data):
        super(ChronoConfigDialog, self).__init__()

        self.data = data

        # Creates a dialog
        self.setWindowTitle("Chrono configuration")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.main_layout = QtGui.QVBoxLayout()

        # Option for saves CSV with data exchange for each time interval
        self.csv_option_layout = QtGui.QHBoxLayout()
        self.csv_intervals_checkbox = QtGui.QCheckBox()
        if self.data['csv_intervals_check']:
            self.csv_intervals_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.csv_intervals_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.csv_intervals_checkbox.toggled.connect(self.on_csv_intervals_check)
        self.csv_intervals_option = QtGui.QLabel(__("CSV intervals:"))
        self.csv_intervals_line_edit = QtGui.QLineEdit(str(self.data['csv_intervals']))
        self.csv_option_layout.addWidget(self.csv_intervals_checkbox)
        self.csv_option_layout.addWidget(self.csv_intervals_option)
        self.csv_option_layout.addWidget(self.csv_intervals_line_edit)

        # Option for define scale used to create the initial scheme of Chrono objects
        self.scale_scheme_option_layout = QtGui.QHBoxLayout()
        self.scale_scheme_checkbox = QtGui.QCheckBox()
        if self.data['scale_scheme_check']:
            self.scale_scheme_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.scale_scheme_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.scale_scheme_checkbox.toggled.connect(self.on_scale_scheme_checkbox)
        self.scale_scheme_option = QtGui.QLabel(__("Scale for scheme:"))
        self.scale_scheme_line_edit = QtGui.QLineEdit(str(self.data['scale_scheme']))
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_checkbox)
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_option)
        self.scale_scheme_option_layout.addWidget(self.scale_scheme_line_edit)

        # Option for allow collision overlap according Dp
        self.collisiondp_option_layout = QtGui.QHBoxLayout()
        self.collisiondp_checkbox = QtGui.QCheckBox()
        if self.data['collisiondp_check']:
            self.collisiondp_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.collisiondp_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.collisiondp_checkbox.toggled.connect(self.on_collisiondp_checkbox)
        self.collisiondp_option = QtGui.QLabel(__("Collision Dp:"))
        self.collisiondp_line_edit = QtGui.QLineEdit(str(self.data['collisiondp']))
        self.collisiondp_option_layout.addWidget(self.collisiondp_checkbox)
        self.collisiondp_option_layout.addWidget(self.collisiondp_option)
        self.collisiondp_option_layout.addWidget(self.collisiondp_line_edit)

        # Create the list for chrono objects
        self.main_chrono = QtGui.QGroupBox("Chrono objects")
        self.main_chrono.setMinimumHeight(150)
        self.chrono_layout = QtGui.QVBoxLayout()

        self.objectlist_table = QtGui.QTableWidget(0, 1)
        self.objectlist_table.setObjectName("Chrono objects table")
        self.objectlist_table.verticalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.objectlist_table.setEnabled(True)

        # Create the necessary spaces in the list
        self.count = 0
        for key in self.data['simobjects'].keys():
            self.context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
            if self.data['simobjects'][self.context_object.Name][1] != "Fluid" and \
                    self.context_object.Name != "Case_Limits":
                self.count += 1
        self.objectlist_table.setRowCount(self.count)
        self.current_row = 0
        self.objects_with_parent = list()
        self.is_floating = ""
        # TODO: LOW PRIORITY, CHANGE THIS FOR GLOBAL TEMP_TADA
        self.temp_data = list()

        # Select the objects that are going to be listed
        for key, value in self.data['simobjects'].items():
            self.context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
            if self.context_object.InList != list():
                self.objects_with_parent.append(self.context_object.Name)
                continue
            if self.context_object.Name == "Case_Limits":
                continue
            if self.data['simobjects'][self.context_object.Name][1] == "Fluid":
                continue

            self.is_floating = "bodyfloating" if str(
                value[0]) in data['floating_mks'].keys() else "bodyfixed"

            # Collects the information of the object
            self.target_widget = ObjectIsCheked(
                key=key,
                object_mk=self.data['simobjects'][self.context_object.Name][0],
                mktype=self.data['simobjects'][self.context_object.Name][1],
                object_name=self.context_object.Label,
                is_floating=self.is_floating
            )

            # Actualices the state of list options
            if len(self.data['chrono_objects']) > 0:
                for elem in self.data['chrono_objects']:
                    if elem[0] == str(key) and elem[3] == 1:
                        self.target_widget.object_check.setCheckState(QtCore.Qt.Checked)
                        self.target_widget.geometry_check.setCheckState(QtCore.Qt.Checked)
                        self.target_widget.modelnormal_input.setCurrentIndex(int(elem[4]))
                    elif elem[0] == str(key) and elem[3] == 0:
                        self.target_widget.object_check.setCheckState(QtCore.Qt.Checked)
                        self.target_widget.geometry_check.setCheckState(QtCore.Qt.Unchecked)
                        self.target_widget.modelnormal_input.setCurrentIndex(int(elem[4]))

            # Saves the information about object for being process later
            self.temp_data.append(self.target_widget)

            # Shows the object in table
            self.objectlist_table.setCellWidget(self.current_row, 0, self.target_widget)

            self.current_row += 1

        # Add table to the layout
        self.chrono_layout.addWidget(self.objectlist_table)

        # Creates 2 main buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Link Linearspring option list
        self.main_link_linearspring = QtGui.QGroupBox("Linearspring")
        self.link_linearspring_layout = QtGui.QVBoxLayout()
        self.link_linearspring_layout2 = QtGui.QVBoxLayout()

        self.link_linearspring_button_layout = QtGui.QHBoxLayout()
        self.button_link_linearspring = QtGui.QPushButton("Add")
        self.link_linearspring_button_layout.addStretch(1)
        self.link_linearspring_button_layout.addWidget(self.button_link_linearspring)
        self.button_link_linearspring.clicked.connect(self.on_link_linearspring_add)

        self.link_linearspring_layout.addLayout(self.link_linearspring_button_layout)
        self.link_linearspring_layout.addLayout(self.link_linearspring_layout2)
        self.main_link_linearspring.setLayout(self.link_linearspring_layout)

        self.refresh_link_linearspring()

        # Link hinge option list
        self.main_link_hinge = QtGui.QGroupBox("Hinge")
        self.link_hinge_layout = QtGui.QVBoxLayout()
        self.link_hinge_layout2 = QtGui.QVBoxLayout()

        self.link_hinge_button_layout = QtGui.QHBoxLayout()
        self.button_link_hinge = QtGui.QPushButton("Add")
        self.link_hinge_button_layout.addStretch(1)
        self.link_hinge_button_layout.addWidget(self.button_link_hinge)
        self.button_link_hinge.clicked.connect(self.on_link_hinge_add)

        self.link_hinge_layout.addLayout(self.link_hinge_button_layout)
        self.link_hinge_layout.addLayout(self.link_hinge_layout2)
        self.main_link_hinge.setLayout(self.link_hinge_layout)

        self.refresh_link_hinge()

        # Link Spheric option list
        self.main_link_spheric = QtGui.QGroupBox("Spheric")
        self.link_spheric_layout = QtGui.QVBoxLayout()
        self.link_spheric_layout2 = QtGui.QVBoxLayout()

        self.link_spheric_button_layout = QtGui.QHBoxLayout()
        self.button_link_spheric = QtGui.QPushButton("Add")
        self.link_spheric_button_layout.addStretch(1)
        self.link_spheric_button_layout.addWidget(self.button_link_spheric)
        self.button_link_spheric.clicked.connect(self.on_link_spheric_add)

        self.link_spheric_layout.addLayout(self.link_spheric_button_layout)
        self.link_spheric_layout.addLayout(self.link_spheric_layout2)
        self.main_link_spheric.setLayout(self.link_spheric_layout)

        self.refresh_link_spheric()

        # Link Pointline option list
        self.main_link_pointline = QtGui.QGroupBox("Pointline")
        self.link_pointline_layout = QtGui.QVBoxLayout()
        self.link_pointline_layout2 = QtGui.QVBoxLayout()

        self.link_pointline_button_layout = QtGui.QHBoxLayout()
        self.button_link_pointline = QtGui.QPushButton("Add")
        self.link_pointline_button_layout.addStretch(1)
        self.link_pointline_button_layout.addWidget(self.button_link_pointline)
        self.button_link_pointline.clicked.connect(self.on_link_pointline_add)

        self.link_pointline_layout.addLayout(self.link_pointline_button_layout)
        self.link_pointline_layout.addLayout(self.link_pointline_layout2)
        self.main_link_pointline.setLayout(self.link_pointline_layout)

        self.refresh_link_pointline()

        # Adds all layouts to main
        self.main_layout.addLayout(self.csv_option_layout)
        self.main_layout.addLayout(self.scale_scheme_option_layout)
        self.main_layout.addLayout(self.collisiondp_option_layout)
        self.main_chrono.setLayout(self.chrono_layout)
        self.main_layout.addWidget(self.main_chrono)
        self.main_layout.addWidget(self.main_link_linearspring)
        self.main_layout.addWidget(self.main_link_hinge)
        self.main_layout.addWidget(self.main_link_spheric)
        self.main_layout.addWidget(self.main_link_pointline)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        # Adds scroll area
        self.main_layout_dialog = QtGui.QVBoxLayout()
        self.main_layout_scroll = QtGui.QScrollArea()
        self.main_layout_scroll.setMinimumWidth(400)
        self.main_layout_scroll.setWidgetResizable(True)
        self.main_layout_scroll_widget = QtGui.QWidget()
        self.main_layout_scroll_widget.setMinimumWidth(400)

        self.main_layout_scroll_widget.setLayout(self.main_layout)
        self.main_layout_scroll.setWidget(self.main_layout_scroll_widget)
        self.main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout_dialog.addWidget(self.main_layout_scroll)
        self.main_layout_dialog.addLayout(self.button_layout)
        self.on_scale_scheme_checkbox()
        self.on_csv_intervals_check()
        self.on_collisiondp_checkbox()

        self.setLayout(self.main_layout_dialog)

        self.exec_()

    def on_collisiondp_checkbox(self):
        """ Checks the collisiondp state """
        if self.collisiondp_checkbox.isChecked():
            self.collisiondp_line_edit.setEnabled(True)
        else:
            self.collisiondp_line_edit.setEnabled(False)

    def on_scale_scheme_checkbox(self):
        """ Checks the scale scheme state """
        if self.scale_scheme_checkbox.isChecked():
            self.scale_scheme_line_edit.setEnabled(True)
        else:
            self.scale_scheme_line_edit.setEnabled(False)

    def on_csv_intervals_check(self):
        """ Checks the csv intervals state """
        if self.csv_intervals_checkbox.isChecked():
            self.csv_intervals_line_edit.setEnabled(True)
        else:
            self.csv_intervals_line_edit.setEnabled(False)

    def refresh_link_hinge(self):
        """ Refreshes the link hinge list """
        count = 0
        while self.link_hinge_layout2.count() > 0:
            target = self.link_hinge_layout2.takeAt(0)
            target.setParent(None)

        for linkhinge in self.data['link_hinge']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link hinge" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda lh=linkhinge[0]: self.link_hinge_edit(lh))
            to_add_deletebutton.clicked.connect(lambda lh=linkhinge[0]: self.link_hinge_delete(lh))
            self.link_hinge_layout2.addLayout(to_add_layout)

    def refresh_link_linearspring(self):
        """ Refreshes the link linearspring list """
        count = 0
        while self.link_linearspring_layout2.count() > 0:
            target = self.link_linearspring_layout2.takeAt(0)
            target.setParent(None)

        for linkLinearspring in self.data['link_linearspring']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link linearspring" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda ll=linkLinearspring[0]: self.link_linearspring_edit(ll))
            to_add_deletebutton.clicked.connect(lambda ll=linkLinearspring[0]: self.link_linearspring_delete(ll))
            self.link_linearspring_layout2.addLayout(to_add_layout)

    def refresh_link_spheric(self):
        """ Refreshes the link spheric list """
        count = 0
        while self.link_spheric_layout2.count() > 0:
            target = self.link_spheric_layout2.takeAt(0)
            target.setParent(None)

        for linkSpheric in self.data['link_spheric']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link spheric" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda ls=linkSpheric[0]: self.link_spheric_edit(ls))
            to_add_deletebutton.clicked.connect(lambda ls=linkSpheric[0]: self.link_spheric_delete(ls))
            self.link_spheric_layout2.addLayout(to_add_layout)

    def refresh_link_pointline(self):
        """ Refreshes the link pointline list """
        count = 0
        while self.link_pointline_layout2.count() > 0:
            target = self.link_pointline_layout2.takeAt(0)
            target.setParent(None)

        for linkPointline in self.data['link_pointline']:
            count += 1
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel("Link pointline" + str(count))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda lp=linkPointline[0]: self.link_pointline_edit(lp))
            to_add_deletebutton.clicked.connect(lambda lp=linkPointline[0]: self.link_pointline_delete(lp))
            self.link_pointline_layout2.addLayout(to_add_layout)

    def on_link_hinge_add(self):
        """ Adds Link hinge option at list """
        # data['link_hinge'] = [element id, body 1, body 2, rotpoint[x,y,z], rotvector[x,y,z], stiffness, damping]
        uid_temp = uuid.uuid4()
        self.data['link_hinge'].append([
            str(uid_temp), '', '', [0, 0, 0], [0, 0, 0], 0, 0])
        self.link_hinge_edit(str(uid_temp))
        #self.refresh_link_hinge()

    def link_hinge_delete(self, link_hinge_id):
        """ Delete a link hinge element """
        link_hinge_to_remove = None
        for lh in self.data['link_hinge']:
            if lh[0] == link_hinge_id:
                link_hinge_to_remove = lh
        if link_hinge_to_remove is not None:
            self.data['link_hinge'].remove(link_hinge_to_remove)
            self.refresh_link_hinge()

    def link_hinge_edit(self, link_hinge_id):
        """ Edit a link hinge element """
        LinkHingeEdit(self.data, self.temp_data, link_hinge_id)
        self.refresh_link_hinge()

    def on_link_linearspring_add(self):
        """ Adds Link linearspring option at list """
        uid_temp = uuid.uuid4()
        # data['link_linearspring'] = [element id, body 1, body 2, point_fb1[x,y,z], point_fb2[x,y,z], stiffness,
        # damping, rest_length, savevtk[nside, radius, length]]
        self.data['link_linearspring'].append([
            str(uid_temp), '', '', [0, 0, 0], [0, 0, 0], 0, 0, 0, [0, 0, 0]])
        self.link_linearspring_edit(str(uid_temp))
        #self.refresh_link_linearspring()

    def link_linearspring_delete(self, link_linearspring_id):
        """ Delete a link linearspring element """
        link_linearspring_to_remove = None
        for ll in self.data['link_linearspring']:
            if ll[0] == link_linearspring_id:
                link_linearspring_to_remove = ll
        if link_linearspring_to_remove is not None:
            self.data['link_linearspring'].remove(link_linearspring_to_remove)
            self.refresh_link_linearspring()

    def link_linearspring_edit(self, link_linearspring_id):
        """ Edit a link linearspring element """
        LinkLinearspringEdit(self.data, self.temp_data, link_linearspring_id)
        self.refresh_link_linearspring()

    def on_link_spheric_add(self):
        """ Adds Link spheric option at list """
        uid_temp = uuid.uuid4()
        # data['link_spheric'] = [element id, body 1, body 2, rotpoint[x,y,z], stiffness, damping]
        self.data['link_spheric'].append([
            str(uid_temp), '', '', [0, 0, 0], 0, 0])
        self.link_spheric_edit(str(uid_temp))
        #self.refresh_link_spheric()

    def link_spheric_delete(self, link_spheric_id):
        """ Delete a link spheric element """
        link_spheric_to_remove = None
        for ls in self.data['link_spheric']:
            if ls[0] == link_spheric_id:
                link_spheric_to_remove = ls
        if link_spheric_to_remove is not None:
            self.data['link_spheric'].remove(link_spheric_to_remove)
            self.refresh_link_spheric()

    def link_spheric_edit(self, link_spheric_id):
        """ Edit a link spheric element """
        LinkSphericEdit(self.data, self.temp_data, link_spheric_id)
        self.refresh_link_spheric()

    def on_link_pointline_add(self):
        """ Adds Link pointline option at list """
        uid_temp = uuid.uuid4()
        # data['link_pointline'] = [element id, body 1, slidingvector[x,y,z], rotpoint[x,y,z], rotvector[x,y,z],
        # rotvector2[x,y,z], stiffness, damping]
        self.data['link_pointline'].append([
            str(uid_temp), '', [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 0, 0])
        self.link_pointline_edit(str(uid_temp))
        #self.refresh_link_pointline()

    def link_pointline_delete(self, link_pointline_id):
        """ Delete a link pointline element """
        link_pointline_to_remove = None
        for lp in self.data['link_pointline']:
            if lp[0] == link_pointline_id:
                link_pointline_to_remove = lp
        if link_pointline_to_remove is not None:
            self.data['link_pointline'].remove(link_pointline_to_remove)
            self.refresh_link_pointline()

    def link_pointline_edit(self, link_pointline_id):
        """ Edit a link pointline element """
        LinkPointlineEdit(self.data, self.temp_data, link_pointline_id)
        self.refresh_link_pointline()

    def on_cancel(self):
        self.reject()

    def update_to_save(self):
        """ Check all the conditions before save """

        # Clean the chrono object list
        self.data['chrono_objects'] = list()

        # Checks the chrono objects and options for save
        for elem in self.temp_data:
            if elem.object_check.isChecked() and elem.geometry_check.isChecked():
                self.data['chrono_objects'].append([elem.key, elem.object_name, elem.object_mk, 1,
                                                    elem.modelnormal_input.currentIndex(), elem.is_floating])
            elif elem.object_check.isChecked():
                self.data['chrono_objects'].append([elem.key, elem.object_name, elem.object_mk, 0, 0, elem.is_floating])

        # Checks the csv interval option for save
        if self.csv_intervals_checkbox.isChecked():
            self.data['csv_intervals_check'] = True
            try:
                self.data['csv_intervals'] = float(self.csv_intervals_line_edit.text())
            except ValueError:
                self.data['csv_intervals_check'] = False
                self.data['csv_intervals'] = ""
                utils.debug("Introduced an invalid value for a float number.")
        else:
            self.data['csv_intervals_check'] = False
            self.data['csv_intervals'] = ""

        # Checks the scale scheme option for save
        if self.scale_scheme_checkbox.isChecked():
            self.data['scale_scheme_check'] = True
            try:
                self.data['scale_scheme'] = float(self.scale_scheme_line_edit.text())
            except ValueError:
                self.data['scale_scheme_check'] = False
                self.data['scale_scheme'] = ""
                utils.debug("Introduced an invalid value for a float number.")
        else:
            self.data['scale_scheme_check'] = False
            self.data['scale_scheme'] = ""

        # Checks the collisiondp option for save
        if self.collisiondp_checkbox.isChecked():
            self.data['collisiondp_check'] = True
            try:
                self.data['collisiondp'] = float(self.collisiondp_line_edit.text())
            except ValueError:
                self.data['collisiondp_check'] = False
                self.data['collisiondp'] = ""
                utils.debug("Introduced an invalid value for a float number.")
        else:
            self.data['collisiondp_check'] = False
            self.data['collisiondp'] = ""

    def on_ok(self):
        """ Save data """
        self.update_to_save()

        ChronoConfigDialog.accept(self)


class LinkHingeEdit(QtGui.QDialog):
    """ Defines Link hinge window dialog """

    def __init__(self, data, temp_data, link_hinge_id):
        super(LinkHingeEdit, self).__init__()

        self.data = data
        self.temp_data = temp_data
        self.link_hinge_id = link_hinge_id

        # Title
        self.setWindowTitle(__("Link hinge configuration"))
        self.link_hinge_edit_layout = QtGui.QVBoxLayout()

        # Find the link hinge for which the button was pressed
        target_link_hinge = None

        for link_hinge in self.data['link_hinge']:
            if link_hinge[0] == self.link_hinge_id:
                target_link_hinge = link_hinge

        # This should not happen but if no link hinge is found with reference id, it spawns an error.
        if target_link_hinge is None:
            guiutils.error_dialog("There was an error opnening the link hinge to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        self.body_one_line_edit.insertItems(0, [str(target_link_hinge[1])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_hinge[1]):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtGui.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtGui.QComboBox()
        self.body_two_line_edit.insertItems(0, [str(target_link_hinge[2])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_hinge[2]):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtGui.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_hinge_edit_layout.addLayout(self.body_layout)

        # Points for rotation
        self.rotpoints_layout = QtGui.QHBoxLayout()
        self.rotpoints_label = QtGui.QLabel(__("Points for rotation: "))
        self.rotpoints_x_label = QtGui.QLabel(__("X"))
        self.rotpoints_x_line_edit = QtGui.QLineEdit(str(target_link_hinge[3][0]))
        self.rotpoints_y_label = QtGui.QLabel(__("Y"))
        self.rotpoints_y_line_edit = QtGui.QLineEdit(str(target_link_hinge[3][1]))
        self.rotpoints_z_label = QtGui.QLabel(__("Z"))
        self.rotpoints_z_line_edit = QtGui.QLineEdit(str(target_link_hinge[3][2]))

        self.rotpoints_layout.addWidget(self.rotpoints_label)
        self.rotpoints_layout.addWidget(self.rotpoints_x_label)
        self.rotpoints_layout.addWidget(self.rotpoints_x_line_edit)
        self.rotpoints_layout.addWidget(self.rotpoints_y_label)
        self.rotpoints_layout.addWidget(self.rotpoints_y_line_edit)
        self.rotpoints_layout.addWidget(self.rotpoints_z_label)
        self.rotpoints_layout.addWidget(self.rotpoints_z_line_edit)

        self.link_hinge_edit_layout.addLayout(self.rotpoints_layout)

        # Vector direction for rotation
        self.rotvector_layout = QtGui.QHBoxLayout()
        self.rotvector_label = QtGui.QLabel(__("Vector direction: "))
        self.rotvector_x_label = QtGui.QLabel(__("X"))
        self.rotvector_x_line_edit = QtGui.QLineEdit(str(target_link_hinge[4][0]))
        self.rotvector_y_label = QtGui.QLabel(__("Y"))
        self.rotvector_y_line_edit = QtGui.QLineEdit(str(target_link_hinge[4][1]))
        self.rotvector_z_label = QtGui.QLabel(__("Z"))
        self.rotvector_z_line_edit = QtGui.QLineEdit(str(target_link_hinge[4][2]))

        self.rotvector_layout.addWidget(self.rotvector_label)
        self.rotvector_layout.addWidget(self.rotvector_x_label)
        self.rotvector_layout.addWidget(self.rotvector_x_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_y_label)
        self.rotvector_layout.addWidget(self.rotvector_y_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_z_label)
        self.rotvector_layout.addWidget(self.rotvector_z_line_edit)

        self.link_hinge_edit_layout.addLayout(self.rotvector_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness: "))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_hinge[5]))
        self.damping_label = QtGui.QLabel(__("Damping: "))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_hinge[6]))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_hinge_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_hinge_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_hinge_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_hinge_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link hinge edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link hinge save button behaviour"""
        count = -1
        for link_hinge_value in self.data['link_hinge']:
            count += 1
            if link_hinge_value[0] == self.link_hinge_id:
                self.data['link_hinge'][count][1] = str(self.body_one_line_edit.currentText())
                self.data['link_hinge'][count][2] = str(self.body_two_line_edit.currentText())
                self.data['link_hinge'][count][3] = [float(self.rotpoints_x_line_edit.text()),
                                                     float(self.rotpoints_y_line_edit.text()),
                                                     float(self.rotpoints_z_line_edit.text())]
                self.data['link_hinge'][count][4] = [float(self.rotvector_x_line_edit.text()),
                                                     float(self.rotvector_y_line_edit.text()),
                                                     float(self.rotvector_z_line_edit.text())]
                self.data['link_hinge'][count][5] = float(self.stiffness_line_edit.text())
                self.data['link_hinge'][count][6] = float(self.damping_line_edit.text())

        if self.data['link_hinge'][count][1] != "" and self.data['link_hinge'][count][2] != "":
            LinkHingeEdit.accept(self)
        else:
            link_hinge_error_dialog = QtGui.QMessageBox()
            link_hinge_error_dialog.setWindowTitle(__("Error!"))
            link_hinge_error_dialog.setText(__("bodies are necesary!"))
            link_hinge_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_hinge_error_dialog.exec_()


class LinkLinearspringEdit(QtGui.QDialog):
    """ Defines Link linearspring window dialog """

    def __init__(self, data, temp_data, link_linearspring_id):
        super(LinkLinearspringEdit, self).__init__()

        self.data = data
        self.temp_data = temp_data
        self.link_linearspring_id = link_linearspring_id

        # Title
        self.setWindowTitle(__("Link linearspring configuration"))
        self.link_linearspring_edit_layout = QtGui.QVBoxLayout()

        # Find the link linearspring for which the button was pressed
        target_link_linearspring = None

        for link_linearspring in self.data['link_linearspring']:
            if link_linearspring[0] == self.link_linearspring_id:
                target_link_linearspring = link_linearspring

        # This should not happen but if no link linearspring is found with reference id, it spawns an error.
        if target_link_linearspring is None:
            guiutils.error_dialog("There was an error opnening the link linearspring to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        self.body_one_line_edit.insertItems(0, [str(target_link_linearspring[1])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_linearspring[1]):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtGui.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtGui.QComboBox()
        self.body_two_line_edit.insertItems(0, [str(target_link_linearspring[2])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_linearspring[2]):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtGui.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_linearspring_edit_layout.addLayout(self.body_layout)

        # Points where the elements interact in body 1
        self.points_b1_layout = QtGui.QHBoxLayout()
        self.points_b1_label = QtGui.QLabel(__("Points in body 1: "))
        self.point_b1_x_label = QtGui.QLabel(__("X"))
        self.point_b1_x_line_edit = QtGui.QLineEdit(str(target_link_linearspring[3][0]))
        self.point_b1_y_label = QtGui.QLabel(__("Y"))
        self.point_b1_y_line_edit = QtGui.QLineEdit(str(target_link_linearspring[3][1]))
        self.point_b1_z_label = QtGui.QLabel(__("Z"))
        self.point_b1_z_line_edit = QtGui.QLineEdit(str(target_link_linearspring[3][2]))

        self.points_b1_layout.addWidget(self.points_b1_label)
        self.points_b1_layout.addWidget(self.point_b1_x_label)
        self.points_b1_layout.addWidget(self.point_b1_x_line_edit)
        self.points_b1_layout.addWidget(self.point_b1_y_label)
        self.points_b1_layout.addWidget(self.point_b1_y_line_edit)
        self.points_b1_layout.addWidget(self.point_b1_z_label)
        self.points_b1_layout.addWidget(self.point_b1_z_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.points_b1_layout)

        # Points where the elements interact in body 2
        self.points_b2_layout = QtGui.QHBoxLayout()
        self.points_b2_label = QtGui.QLabel(__("Points in body 2: "))
        self.point_b2_x_label = QtGui.QLabel(__("X"))
        self.point_b2_x_line_edit = QtGui.QLineEdit(str(target_link_linearspring[4][0]))
        self.point_b2_y_label = QtGui.QLabel(__("Y"))
        self.point_b2_y_line_edit = QtGui.QLineEdit(str(target_link_linearspring[4][1]))
        self.point_b2_z_label = QtGui.QLabel(__("Z"))
        self.point_b2_z_line_edit = QtGui.QLineEdit(str(target_link_linearspring[4][2]))

        self.points_b2_layout.addWidget(self.points_b2_label)
        self.points_b2_layout.addWidget(self.point_b2_x_label)
        self.points_b2_layout.addWidget(self.point_b2_x_line_edit)
        self.points_b2_layout.addWidget(self.point_b2_y_label)
        self.points_b2_layout.addWidget(self.point_b2_y_line_edit)
        self.points_b2_layout.addWidget(self.point_b2_z_label)
        self.points_b2_layout.addWidget(self.point_b2_z_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.points_b2_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness: "))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_linearspring[5]))
        self.damping_label = QtGui.QLabel(__("Damping: "))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_linearspring[6]))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_linearspring_edit_layout.addLayout(self.torsion_damping_layout)

        # Spring equilibrium length
        self.rest_layout = QtGui.QHBoxLayout()
        self.rest_label = QtGui.QLabel(__("Rest length: "))
        self.rest_line_edit = QtGui.QLineEdit(str(target_link_linearspring[7]))

        self.rest_layout.addWidget(self.rest_label)
        self.rest_layout.addWidget(self.rest_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.rest_layout)

        # vtk
        self.vtk_layout = QtGui.QHBoxLayout()
        self.vtk_nside_label = QtGui.QLabel(__("Number of sections: "))
        self.vtk_nside_line_edit = QtGui.QLineEdit(str(target_link_linearspring[8][0]))
        self.vtk_radius_label = QtGui.QLabel(__("Spring radius: "))
        self.vtk_radius_line_edit = QtGui.QLineEdit(str(target_link_linearspring[8][1]))
        self.vtk_length_label = QtGui.QLabel(__("Length for revolution: "))
        self.vtk_length_line_edit = QtGui.QLineEdit(str(target_link_linearspring[8][2]))

        self.vtk_layout.addWidget(self.vtk_nside_label)
        self.vtk_layout.addWidget(self.vtk_nside_line_edit)
        self.vtk_layout.addWidget(self.vtk_radius_label)
        self.vtk_layout.addWidget(self.vtk_radius_line_edit)
        self.vtk_layout.addWidget(self.vtk_length_label)
        self.vtk_layout.addWidget(self.vtk_length_line_edit)

        self.link_linearspring_edit_layout.addLayout(self.vtk_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_linearspring_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_linearspring_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link linearspring edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link linearspring save button behaviour"""
        count = -1
        for link_linearspring_value in self.data['link_linearspring']:
            count += 1
            if link_linearspring_value[0] == self.link_linearspring_id:
                self.data['link_linearspring'][count][1] = str(self.body_one_line_edit.currentText())
                self.data['link_linearspring'][count][2] = str(self.body_two_line_edit.currentText())
                self.data['link_linearspring'][count][3] = [float(self.point_b1_x_line_edit.text()),
                                                            float(self.point_b1_y_line_edit.text()),
                                                            float(self.point_b1_z_line_edit.text())]
                self.data['link_linearspring'][count][4] = [float(self.point_b2_x_line_edit.text()),
                                                            float(self.point_b2_y_line_edit.text()),
                                                            float(self.point_b2_z_line_edit.text())]
                self.data['link_linearspring'][count][5] = float(self.stiffness_line_edit.text())
                self.data['link_linearspring'][count][6] = float(self.damping_line_edit.text())
                self.data['link_linearspring'][count][7] = float(self.rest_line_edit.text())
                self.data['link_linearspring'][count][8] = [float(self.vtk_nside_line_edit.text()),
                                                            float(self.vtk_radius_line_edit.text()),
                                                            float(self.vtk_length_line_edit.text())]

        if self.data['link_linearspring'][count][1] != "" and self.data['link_linearspring'][count][2] != "":
            LinkLinearspringEdit.accept(self)
        else:
            link_linearspring_error_dialog = QtGui.QMessageBox()
            link_linearspring_error_dialog.setWindowTitle(__("Error!"))
            link_linearspring_error_dialog.setText(__("bodies are necesary!"))
            link_linearspring_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_linearspring_error_dialog.exec_()


class LinkSphericEdit(QtGui.QDialog):
    """ Defines Link spheric window dialog """

    def __init__(self, data, temp_data, link_spheric_id):
        super(LinkSphericEdit, self).__init__()

        self.data = data
        self.temp_data = temp_data
        self.link_spheric_id = link_spheric_id

        # Title
        self.setWindowTitle(__("Link spheric configuration"))
        self.link_spheric_edit_layout = QtGui.QVBoxLayout()

        # Find the link spheric for which the button was pressed
        target_link_spheric = None

        for link_spheric in self.data['link_spheric']:
            if link_spheric[0] == self.link_spheric_id:
                target_link_spheric = link_spheric

        # This should not happen but if no link spheric is found with reference id, it spawns an error.
        if target_link_spheric is None:
            guiutils.error_dialog("There was an error opnening the link spheric to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        if str(target_link_spheric[1]) != '':
            self.body_one_line_edit.insertItems(0, ['', str(target_link_spheric[1])])
            self.body_one_line_edit.setCurrentIndex(1)
        else:
            self.body_one_line_edit.insertItems(0, [str(target_link_spheric[1])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_spheric[1]):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_two_label = QtGui.QLabel(__("Body 2: "))
        self.body_two_line_edit = QtGui.QComboBox()
        if str(target_link_spheric[2]) != '':
            self.body_two_line_edit.insertItems(0, ['', str(target_link_spheric[2])])
            self.body_two_line_edit.setCurrentIndex(1)
        else:
            self.body_two_line_edit.insertItems(0, [str(target_link_spheric[2])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_spheric[2]):
                self.body_two_line_edit.insertItems(0, [body.object_name])
        self.body_to_body_label = QtGui.QLabel(__("to"))

        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addWidget(self.body_to_body_label)
        self.body_layout.addWidget(self.body_two_label)
        self.body_layout.addWidget(self.body_two_line_edit)
        self.body_layout.addStretch(1)

        self.link_spheric_edit_layout.addLayout(self.body_layout)

        # Points where the elements interact
        self.points_layout = QtGui.QHBoxLayout()
        self.points_label = QtGui.QLabel(__("Points: "))
        self.point_x_label = QtGui.QLabel(__("X"))
        self.point_x_line_edit = QtGui.QLineEdit(str(target_link_spheric[3][0]))
        self.point_y_label = QtGui.QLabel(__("Y"))
        self.point_y_line_edit = QtGui.QLineEdit(str(target_link_spheric[3][1]))
        self.point_z_label = QtGui.QLabel(__("Z"))
        self.point_z_line_edit = QtGui.QLineEdit(str(target_link_spheric[3][2]))

        self.points_layout.addWidget(self.points_label)
        self.points_layout.addWidget(self.point_x_label)
        self.points_layout.addWidget(self.point_x_line_edit)
        self.points_layout.addWidget(self.point_y_label)
        self.points_layout.addWidget(self.point_y_line_edit)
        self.points_layout.addWidget(self.point_z_label)
        self.points_layout.addWidget(self.point_z_line_edit)

        self.link_spheric_edit_layout.addLayout(self.points_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness"))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_spheric[4]))
        self.damping_label = QtGui.QLabel(__("Damping"))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_spheric[5]))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_spheric_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_spheric_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_spheric_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_spheric_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link Spheric edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link Spheric save button behaviour"""
        count = -1
        for link_spheric_value in self.data['link_spheric']:
            count += 1
            if link_spheric_value[0] == self.link_spheric_id:
                self.data['link_spheric'][count][1] = str(self.body_one_line_edit.currentText())
                self.data['link_spheric'][count][2] = str(self.body_two_line_edit.currentText())
                self.data['link_spheric'][count][3] = [float(self.point_x_line_edit.text()),
                                                       float(self.point_y_line_edit.text()),
                                                       float(self.point_z_line_edit.text())]
                self.data['link_spheric'][count][4] = float(self.stiffness_line_edit.text())
                self.data['link_spheric'][count][5] = float(self.damping_line_edit.text())

        if self.data['link_spheric'][count][1] != "":
            LinkSphericEdit.accept(self)
        else:
            link_spheric_error_dialog = QtGui.QMessageBox()
            link_spheric_error_dialog.setWindowTitle(__("Error!"))
            link_spheric_error_dialog.setText(__("body 1 is necesary!"))
            link_spheric_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_spheric_error_dialog.exec_()


class LinkPointlineEdit(QtGui.QDialog):
    """ Defines Link pontline window dialog """

    def __init__(self, data, temp_data, link_pointline_id):
        super(LinkPointlineEdit, self).__init__()

        self.data = data
        self.temp_data = temp_data
        self.link_pointline_id = link_pointline_id

        # Title
        self.setWindowTitle(__("Link pointline configuration"))
        self.link_pointline_edit_layout = QtGui.QVBoxLayout()

        # Find the link pointline for which the button was pressed
        target_link_pointline = None

        for link_pointline in self.data['link_pointline']:
            if link_pointline[0] == self.link_pointline_id:
                target_link_pointline = link_pointline

        # This should not happen but if no link pointline is found with reference id, it spawns an error.
        if target_link_pointline is None:
            guiutils.error_dialog("There was an error opnening the link pointline to edit")
            return

        # Elements that interact
        self.body_layout = QtGui.QHBoxLayout()
        self.body_one_label = QtGui.QLabel(__("Body 1: "))
        self.body_one_line_edit = QtGui.QComboBox()
        if str(target_link_pointline[1]) != '':
            self.body_one_line_edit.insertItems(0, ['', str(target_link_pointline[1])])
            self.body_one_line_edit.setCurrentIndex(1)
        else:
            self.body_one_line_edit.insertItems(0, [str(target_link_pointline[1])])
        for body in self.temp_data:
            if body.object_check.isChecked() and body.object_name != str(target_link_pointline[1]):
                self.body_one_line_edit.insertItems(0, [body.object_name])
        self.body_layout.addWidget(self.body_one_label)
        self.body_layout.addWidget(self.body_one_line_edit)
        self.body_layout.addStretch(1)

        self.link_pointline_edit_layout.addLayout(self.body_layout)

        # Vector direction for sliding axis
        self.sliding_vector_layout = QtGui.QHBoxLayout()
        self.sliding_vector_label = QtGui.QLabel(__("Sliding Vector: "))
        self.sliding_vector_x_label = QtGui.QLabel(__("X"))
        self.sliding_vector_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[2][0]))
        self.sliding_vector_y_label = QtGui.QLabel(__("Y"))
        self.sliding_vector_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[2][1]))
        self.sliding_vector_z_label = QtGui.QLabel(__("Z"))
        self.sliding_vector_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[2][2]))

        self.sliding_vector_layout.addWidget(self.sliding_vector_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_x_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_x_line_edit)
        self.sliding_vector_layout.addWidget(self.sliding_vector_y_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_y_line_edit)
        self.sliding_vector_layout.addWidget(self.sliding_vector_z_label)
        self.sliding_vector_layout.addWidget(self.sliding_vector_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.sliding_vector_layout)

        # Point for rotation
        self.rotpoint_layout = QtGui.QHBoxLayout()
        self.rotpoint_label = QtGui.QLabel(__("Point for rotation: "))
        self.rotpoint_x_label = QtGui.QLabel(__("X"))
        self.rotpoint_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[3][0]))
        self.rotpoint_y_label = QtGui.QLabel(__("Y"))
        self.rotpoint_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[3][1]))
        self.rotpoint_z_label = QtGui.QLabel(__("Z"))
        self.rotpoint_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[3][2]))

        self.rotpoint_layout.addWidget(self.rotpoint_label)
        self.rotpoint_layout.addWidget(self.rotpoint_x_label)
        self.rotpoint_layout.addWidget(self.rotpoint_x_line_edit)
        self.rotpoint_layout.addWidget(self.rotpoint_y_label)
        self.rotpoint_layout.addWidget(self.rotpoint_y_line_edit)
        self.rotpoint_layout.addWidget(self.rotpoint_z_label)
        self.rotpoint_layout.addWidget(self.rotpoint_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotpoint_layout)

        # Vector direction for rotation
        self.rotvector_layout = QtGui.QHBoxLayout()
        self.rotvector_label = QtGui.QLabel(__("Vector direction: "))
        self.rotvector_x_label = QtGui.QLabel(__("X"))
        self.rotvector_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[4][0]))
        self.rotvector_y_label = QtGui.QLabel(__("Y"))
        self.rotvector_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[4][1]))
        self.rotvector_z_label = QtGui.QLabel(__("Z"))
        self.rotvector_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[4][2]))

        self.rotvector_layout.addWidget(self.rotvector_label)
        self.rotvector_layout.addWidget(self.rotvector_x_label)
        self.rotvector_layout.addWidget(self.rotvector_x_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_y_label)
        self.rotvector_layout.addWidget(self.rotvector_y_line_edit)
        self.rotvector_layout.addWidget(self.rotvector_z_label)
        self.rotvector_layout.addWidget(self.rotvector_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotvector_layout)

        # Second vector to avoid rotation
        self.rotvector2_layout = QtGui.QHBoxLayout()
        self.rotvector2_label = QtGui.QLabel(__("Second vector: "))
        self.rotvector2_x_label = QtGui.QLabel(__("X"))
        self.rotvector2_x_line_edit = QtGui.QLineEdit(str(target_link_pointline[5][0]))
        self.rotvector2_y_label = QtGui.QLabel(__("Y"))
        self.rotvector2_y_line_edit = QtGui.QLineEdit(str(target_link_pointline[5][1]))
        self.rotvector2_z_label = QtGui.QLabel(__("Z"))
        self.rotvector2_z_line_edit = QtGui.QLineEdit(str(target_link_pointline[5][2]))

        self.rotvector2_layout.addWidget(self.rotvector2_label)
        self.rotvector2_layout.addWidget(self.rotvector2_x_label)
        self.rotvector2_layout.addWidget(self.rotvector2_x_line_edit)
        self.rotvector2_layout.addWidget(self.rotvector2_y_label)
        self.rotvector2_layout.addWidget(self.rotvector2_y_line_edit)
        self.rotvector2_layout.addWidget(self.rotvector2_z_label)
        self.rotvector2_layout.addWidget(self.rotvector2_z_line_edit)

        self.link_pointline_edit_layout.addLayout(self.rotvector2_layout)

        # Torsion options
        self.torsion_stiffness_layout = QtGui.QHBoxLayout()
        self.torsion_damping_layout = QtGui.QHBoxLayout()
        self.stiffness_label = QtGui.QLabel(__("Stiffness"))
        self.stiffness_line_edit = QtGui.QLineEdit(str(target_link_pointline[6]))
        self.damping_label = QtGui.QLabel(__("Damping"))
        self.damping_line_edit = QtGui.QLineEdit(str(target_link_pointline[7]))

        self.torsion_stiffness_layout.addWidget(self.stiffness_label)
        self.torsion_stiffness_layout.addWidget(self.stiffness_line_edit)
        self.torsion_damping_layout.addWidget(self.damping_label)
        self.torsion_damping_layout.addWidget(self.damping_line_edit)

        self.link_pointline_edit_layout.addLayout(self.torsion_stiffness_layout)
        self.link_pointline_edit_layout.addLayout(self.torsion_damping_layout)

        # Buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.ok_button.clicked.connect(self.on_save)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.link_pointline_edit_layout.addLayout(self.button_layout)

        # Add the elements to the window
        self.setLayout(self.link_pointline_edit_layout)
        self.exec_()

    def on_cancel(self):
        """ Link pointline edit cancel button behaviour."""
        self.reject()

    def on_save(self):
        """ Link pointline save button behaviour"""
        count = -1
        for link_pointline_value in self.data['link_pointline']:
            count += 1
            if link_pointline_value[0] == self.link_pointline_id:
                self.data['link_pointline'][count][1] = str(self.body_one_line_edit.currentText())
                self.data['link_pointline'][count][2] = [float(self.sliding_vector_x_line_edit.text()),
                                                         float(self.sliding_vector_y_line_edit.text()),
                                                         float(self.sliding_vector_z_line_edit.text())]
                self.data['link_pointline'][count][3] = [float(self.rotpoint_x_line_edit.text()),
                                                         float(self.rotpoint_y_line_edit.text()),
                                                         float(self.rotpoint_z_line_edit.text())]
                self.data['link_pointline'][count][4] = [float(self.rotvector_x_line_edit.text()),
                                                         float(self.rotvector_y_line_edit.text()),
                                                         float(self.rotvector_z_line_edit.text())]
                self.data['link_pointline'][count][5] = [float(self.rotvector2_x_line_edit.text()),
                                                         float(self.rotvector2_y_line_edit.text()),
                                                         float(self.rotvector2_z_line_edit.text())]
                self.data['link_pointline'][count][6] = float(self.stiffness_line_edit.text())
                self.data['link_pointline'][count][7] = float(self.damping_line_edit.text())

        if self.data['link_pointline'][count][1] != "":
            LinkPointlineEdit.accept(self)
        else:
            link_pointline_error_dialog = QtGui.QMessageBox()
            link_pointline_error_dialog.setWindowTitle(__("Error!"))
            link_pointline_error_dialog.setText(__("body 1 is necesary!"))
            link_pointline_error_dialog.setIcon(QtGui.QMessageBox.Critical)
            link_pointline_error_dialog.exec_()


class ObjectIsShowed(QtGui.QWidget):
    """ Widget shows an object """

    def __init__(self, key, object_name="No name", object_mk=-1, mktype="fluid"):
        super(ObjectIsShowed, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.key = key
        self.object_name = object_name
        self.object_mk = object_mk + 1
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.mk_label = QtGui.QLabel(
            "<b>{}{}</b>".format(mktype[0].upper(), str(self.object_mk)))
        self.name_label = QtGui.QLabel(str(self.object_name))

        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)


class InletConfigDialog(QtGui.QDialog):
    """ Defines the Inlet/Outlet dialog window.
       Modifies data dictionary passed as parameter. """

    def __init__(self, data):
        super(InletConfigDialog, self).__init__()

        self.data = data

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet configuration")
        self.main_layout = QtGui.QVBoxLayout()

        # Creates use refilling option
        self.refilling_layout = QtGui.QHBoxLayout()
        self.refilling_option = QtGui.QLabel(__("Use refilling: "))
        self.refilling_combobox = QtGui.QComboBox()
        self.refilling_combobox.insertItems(0, [__("False"), __("True")])

        self.refilling_layout.addWidget(self.refilling_option)
        self.refilling_layout.addWidget(self.refilling_combobox)
        self.refilling_layout.addStretch(1)

        # Creates 2 main buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        # Create the list for inlet/outlet objects
        self.main_inlet = QtGui.QGroupBox("Inlet/Outler objects (only objects defined with 'Faces')")
        self.inlet_layout = QtGui.QVBoxLayout()

        self.objectlist_table = QtGui.QTableWidget(0, 2)
        self.objectlist_table.setObjectName("Inlet/Outler objects table")
        self.objectlist_table.verticalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setVisible(False)
        self.objectlist_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.objectlist_table.setEnabled(True)

        # Create the necessary spaces in the list
        self.count = 0
        for key in self.data['simobjects'].keys():
            self.context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
            if self.data['simobjects'][self.context_object.Name][1] == "Fluid" and \
                    self.context_object.Name != "Case_Limits" and \
                    self.data['simobjects'][self.context_object.Name][2] == "Face":
                self.count += 1
        self.objectlist_table.setRowCount(self.count)
        self.current_row = 0
        self.objects_with_parent = list()
        self.is_floating = ""
        # TODO: LOW PRIORITY, CHANGE THIS FOR GLOBAL TEMP_TADA
        self.temp_data = list()

        # Select the objects that are going to be listed
        for key, value in self.data['simobjects'].items():
            self.context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
            if self.context_object.InList != list():
                self.objects_with_parent.append(self.context_object.Name)
                continue
            if self.context_object.Name == "Case_Limits":
                continue
            if self.data['simobjects'][self.context_object.Name][1] == "Bound":
                continue
            if self.data['simobjects'][self.context_object.Name][2] != "Face":
                continue

            # Collects the information of the object
            self.target_widget = ObjectIsShowed(
                key=key,
                object_mk=self.data['simobjects'][self.context_object.Name][0],
                mktype=self.data['simobjects'][self.context_object.Name][1],
                object_name=self.context_object.Label
            )

            # Save the current object
            self.temp_data.append(self.target_widget)

            self.inlet_button = QtGui.QPushButton(__("Add"))
            self.inlet_button.clicked.connect(self.on_add_zone)

            # Shows the object in table
            self.objectlist_table.setCellWidget(self.current_row, 0, self.target_widget)
            self.objectlist_table.setCellWidget(self.current_row, 1, self.inlet_button)

            self.current_row += 1

        # Add table to the layout
        self.inlet_layout.addWidget(self.objectlist_table)

        self.main_inlet.setLayout(self.inlet_layout)

        # Create the list for zones
        self.main_zones = QtGui.QGroupBox("Inlet/Outler zones")
        self.zones_layout = QtGui.QVBoxLayout()

        self.main_zones.setLayout(self.zones_layout)

        # Adds all layouts to main
        self.main_layout.addLayout(self.refilling_layout)
        self.main_layout.addWidget(self.main_inlet)
        self.main_layout.addWidget(self.main_zones)

        # Adds scroll area
        self.main_layout_dialog = QtGui.QVBoxLayout()
        self.main_layout_scroll = QtGui.QScrollArea()
        self.main_layout_scroll.setMinimumWidth(400)
        self.main_layout_scroll.setWidgetResizable(True)
        self.main_layout_scroll_widget = QtGui.QWidget()
        self.main_layout_scroll_widget.setMinimumWidth(400)

        self.main_layout_scroll_widget.setLayout(self.main_layout)
        self.main_layout_scroll.setWidget(self.main_layout_scroll_widget)
        self.main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout_dialog.addWidget(self.main_layout_scroll)
        self.main_layout_dialog.addLayout(self.button_layout)

        self.setLayout(self.main_layout_dialog)

        self.exec_()

    def on_add_zone(self):
        """ """

        if self.target_widget in self.data['inlet_object']:
            # Warning window about save_case
            self.zone_warning_dialog = QtGui.QMessageBox()
            self.zone_warning_dialog.setWindowTitle(__("Warning!"))
            self.zone_warning_dialog.setText(__("This zone already exists..."))
            self.zone_warning_dialog.setIcon(QtGui.QMessageBox.Warning)
            self.refresh_zones()
            self.zone_warning_dialog.exec_()
        else:
            self.data['inlet_object'].append(self.target_widget)
            self.refresh_zones()

    def refresh_zones(self):
        """ Refreshes the zones list """
        while self.zones_layout.count() > 0:
            target = self.zones_layout.takeAt(0)
            target.setParent(None)

        for inletObject in self.data['inlet_object']:
            to_add_layout = QtGui.QHBoxLayout()
            to_add_layout2 = QtGui.QHBoxLayout()
            to_add_label2 = QtGui.QLabel(" ")
            to_add_layout2.addWidget(to_add_label2)
            to_add_label = QtGui.QLabel(inletObject.object_name)
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda io=inletObject: self.zone_edit(io))
            to_add_deletebutton.clicked.connect(lambda io=inletObject: self.zone_delete(io))
            self.zones_layout.addLayout(to_add_layout2)
            self.zones_layout.addLayout(to_add_layout)

    def zone_delete(self, io):
        """ Delete one zone from the list """
        self.data['inlet_object'].remove(io)
        self.refresh_zones()

    def zone_edit(self, io):
        """"""
        InletZoneEdit(self.data, io)

    def on_cancel(self):
        self.reject()

    def on_ok(self):
        """ Save data """
        # TODO: NEED TO FINISH THIS
        InletConfigDialog.accept(self)


class InletZoneEdit(QtGui.QDialog):
    """  """
    def __init__(self, data, inlet_object_id):
        super(InletZoneEdit, self).__init__()

        self.data = data
        self.inlet_object_id = inlet_object_id

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet object edit")
        self.main_layout = QtGui.QVBoxLayout()

        self.edit_layout = QtGui.QGroupBox("Inlet/Outler edit")

        self.main_layout.addWidget(self.edit_layout)

        self.setLayout(self.main_layout)

        self.exec_()


class RunDialog(QtGui.QDialog):
    """ Defines run window dialog """

    def __init__(self):
        super(RunDialog, self).__init__()

        self.run_watcher = QtCore.QFileSystemWatcher()
        # Title and size
        self.setModal(False)
        self.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
        self.run_dialog_layout = QtGui.QVBoxLayout()

        # Information GroupBox
        self.run_group = QtGui.QGroupBox(__("Simulation Data"))
        self.run_group_layout = QtGui.QVBoxLayout()

        self.run_group_label_case = QtGui.QLabel(__("Case name: "))
        self.run_group_label_proc = QtGui.QLabel(__("Simulation processor: "))
        self.run_group_label_part = QtGui.QLabel(__("Number of particles: "))
        self.run_group_label_partsout = QtGui.QLabel(__("Total particles out: "))
        self.run_group_label_eta = QtGui.QLabel(self)
        self.run_group_label_eta.setText(__("Estimated time to complete simulation: {}").format("Calculating..."))

        self.run_group_layout.addWidget(self.run_group_label_case)
        self.run_group_layout.addWidget(self.run_group_label_proc)
        self.run_group_layout.addWidget(self.run_group_label_part)
        self.run_group_layout.addWidget(self.run_group_label_partsout)
        self.run_group_layout.addWidget(self.run_group_label_eta)
        self.run_group_layout.addStretch(1)

        self.run_group.setLayout(self.run_group_layout)

        # Progress Bar
        self.run_progbar_layout = QtGui.QHBoxLayout()
        self.run_progbar_bar = QtGui.QProgressBar()
        self.run_progbar_bar.setRange(0, 100)
        self.run_progbar_bar.setTextVisible(False)
        self.run_progbar_layout.addWidget(self.run_progbar_bar)

        # Buttons
        self.run_button_layout = QtGui.QHBoxLayout()
        self.run_button_details = QtGui.QPushButton(__("Details"))
        self.run_button_cancel = QtGui.QPushButton(__("Cancel Simulation"))
        self.run_button_layout.addStretch(1)
        self.run_button_layout.addWidget(self.run_button_details)
        self.run_button_layout.addWidget(self.run_button_cancel)

        self.run_dialog_layout.addWidget(self.run_group)
        self.run_dialog_layout.addLayout(self.run_progbar_layout)
        self.run_dialog_layout.addLayout(self.run_button_layout)

        self.setLayout(self.run_dialog_layout)

        # Defines run details
        self.run_details = QtGui.QDialog()
        self.run_details.setMinimumWidth(650)
        self.run_details.setModal(False)
        self.run_details.setWindowTitle(__("Simulation details"))
        self.run_details_layout = QtGui.QVBoxLayout()

        self.run_details_text = QtGui.QTextEdit()
        self.run_details_text.setReadOnly(True)
        self.run_details_layout.addWidget(self.run_details_text)

        self.run_details.setLayout(self.run_details_layout)


class FloatStateDialog(QtGui.QDialog):
    """ Defines a window with floating properties. """

    def __init__(self, data):
        super(FloatStateDialog, self).__init__()

        self.data = data

        self.setWindowTitle(__("Floating configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))

        self.target_mk = int(self.data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.is_floating_layout = QtGui.QHBoxLayout()
        self.is_floating_label = QtGui.QLabel(__("Set floating: "))
        self.is_floating_label.setToolTip(__("Sets the current MKBound selected as floating."))
        self.is_floating_selector = QtGui.QComboBox()
        self.is_floating_selector.insertItems(0, ["True", "False"])
        self.is_floating_selector.currentIndexChanged.connect(self.on_floating_change)
        self.is_floating_targetlabel = QtGui.QLabel(__("Target MKBound: ") + str(self.target_mk))
        self.is_floating_layout.addWidget(self.is_floating_label)
        self.is_floating_layout.addWidget(self.is_floating_selector)
        self.is_floating_layout.addStretch(1)

        self.is_floating_layout.addWidget(self.is_floating_targetlabel)
        self.floating_props_group = QtGui.QGroupBox(__("Floating properties"))
        self.floating_props_layout = QtGui.QVBoxLayout()
        self.floating_props_massrhop_layout = QtGui.QHBoxLayout()
        self.floating_props_massrhop_label = QtGui.QLabel(__("Mass/Density: "))
        self.floating_props_massrhop_label.setToolTip(__("Selects an mass/density calculation method and its value."))
        self.floating_props_massrhop_selector = QtGui.QComboBox()
        self.floating_props_massrhop_selector.insertItems(0, ['massbody (kg)', 'rhopbody (kg/m^3)'])
        self.floating_props_massrhop_input = QtGui.QLineEdit()
        self.floating_props_massrhop_selector.currentIndexChanged.connect(self.on_massrhop_change)
        self.floating_props_massrhop_layout.addWidget(self.floating_props_massrhop_label)

        self.floating_props_massrhop_layout.addWidget(self.floating_props_massrhop_selector)
        self.floating_props_massrhop_layout.addWidget(self.floating_props_massrhop_input)
        self.floating_center_layout = QtGui.QHBoxLayout()
        self.floating_center_label = QtGui.QLabel(__("Gravity center (m): "))
        self.floating_center_label.setToolTip(__("Sets the mk group gravity center."))
        self.floating_center_label_x = QtGui.QLabel("X")
        self.floating_center_input_x = QtGui.QLineEdit()
        self.floating_center_label_y = QtGui.QLabel("Y")
        self.floating_center_input_y = QtGui.QLineEdit()
        self.floating_center_label_z = QtGui.QLabel("Z")
        self.floating_center_input_z = QtGui.QLineEdit()
        self.floating_center_auto = QtGui.QCheckBox("Auto ")
        self.floating_center_auto.toggled.connect(self.on_gravity_auto)
        self.floating_center_layout.addWidget(self.floating_center_label)
        self.floating_center_layout.addWidget(self.floating_center_label_x)
        self.floating_center_layout.addWidget(self.floating_center_input_x)
        self.floating_center_layout.addWidget(self.floating_center_label_y)
        self.floating_center_layout.addWidget(self.floating_center_input_y)
        self.floating_center_layout.addWidget(self.floating_center_label_z)
        self.floating_center_layout.addWidget(self.floating_center_input_z)
        self.floating_center_layout.addWidget(self.floating_center_auto)

        self.floating_inertia_layout = QtGui.QHBoxLayout()
        self.floating_inertia_label = QtGui.QLabel(__("Inertia (kg*m<sup>2</sup>): "))
        self.floating_inertia_label.setToolTip(__("Sets the MK group inertia."))
        self.floating_inertia_label_x = QtGui.QLabel("X")
        self.floating_inertia_input_x = QtGui.QLineEdit()
        self.floating_inertia_label_y = QtGui.QLabel("Y")
        self.floating_inertia_input_y = QtGui.QLineEdit()
        self.floating_inertia_label_z = QtGui.QLabel("Z")
        self.floating_inertia_input_z = QtGui.QLineEdit()
        self.floating_inertia_auto = QtGui.QCheckBox("Auto ")
        self.floating_inertia_auto.toggled.connect(self.on_inertia_auto)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label_x)
        self.floating_inertia_layout.addWidget(self.floating_inertia_input_x)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label_y)
        self.floating_inertia_layout.addWidget(self.floating_inertia_input_y)
        self.floating_inertia_layout.addWidget(self.floating_inertia_label_z)
        self.floating_inertia_layout.addWidget(self.floating_inertia_input_z)
        self.floating_inertia_layout.addWidget(self.floating_inertia_auto)

        self.floating_velini_layout = QtGui.QHBoxLayout()
        self.floating_velini_label = QtGui.QLabel(__("Initial linear velocity: "))
        self.floating_velini_label.setToolTip(__("Sets the MK group initial linear velocity"))
        self.floating_velini_label_x = QtGui.QLabel("X")
        self.floating_velini_input_x = QtGui.QLineEdit()
        self.floating_velini_label_y = QtGui.QLabel("Y")
        self.floating_velini_input_y = QtGui.QLineEdit()
        self.floating_velini_label_z = QtGui.QLabel("Z")
        self.floating_velini_input_z = QtGui.QLineEdit()
        self.floating_velini_auto = QtGui.QCheckBox("Auto ")
        self.floating_velini_auto.toggled.connect(self.on_velini_auto)
        self.floating_velini_layout.addWidget(self.floating_velini_label)
        self.floating_velini_layout.addWidget(self.floating_velini_label_x)
        self.floating_velini_layout.addWidget(self.floating_velini_input_x)
        self.floating_velini_layout.addWidget(self.floating_velini_label_y)
        self.floating_velini_layout.addWidget(self.floating_velini_input_y)
        self.floating_velini_layout.addWidget(self.floating_velini_label_z)
        self.floating_velini_layout.addWidget(self.floating_velini_input_z)
        self.floating_velini_layout.addWidget(self.floating_velini_auto)

        self.floating_omegaini_layout = QtGui.QHBoxLayout()
        self.floating_omegaini_label = QtGui.QLabel(__("Initial angular velocity: "))
        self.floating_omegaini_label.setToolTip(__("Sets the MK group initial angular velocity"))
        self.floating_omegaini_label_x = QtGui.QLabel("X")
        self.floating_omegaini_input_x = QtGui.QLineEdit()
        self.floating_omegaini_label_y = QtGui.QLabel("Y")
        self.floating_omegaini_input_y = QtGui.QLineEdit()
        self.floating_omegaini_label_z = QtGui.QLabel("Z")
        self.floating_omegaini_input_z = QtGui.QLineEdit()
        self.floating_omegaini_auto = QtGui.QCheckBox("Auto ")
        self.floating_omegaini_auto.toggled.connect(self.on_omegaini_auto)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label_x)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_input_x)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label_y)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_input_y)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_label_z)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_input_z)
        self.floating_omegaini_layout.addWidget(self.floating_omegaini_auto)

        self.floating_translation_layout = QtGui.QHBoxLayout()
        self.floating_translation_label = QtGui.QLabel(__("Traslation restriction: "))
        self.floating_translation_label.setToolTip(__("Use 0 for translation restriction in the movement (default=(1,1,1))"))
        self.floating_translation_label_x = QtGui.QLabel("X")
        self.floating_translation_input_x = QtGui.QComboBox()
        self.floating_translation_input_x.insertItems(1, ['0', '1'])
        self.floating_translation_label_y = QtGui.QLabel("Y")
        self.floating_translation_input_y = QtGui.QComboBox()
        self.floating_translation_input_y.insertItems(1, ['0', '1'])
        self.floating_translation_label_z = QtGui.QLabel("Z")
        self.floating_translation_input_z = QtGui.QComboBox()
        self.floating_translation_input_z.insertItems(1, ['0', '1'])
        self.floating_translation_auto = QtGui.QCheckBox("Auto ")
        self.floating_translation_auto.toggled.connect(self.on_translation_auto)
        self.floating_translation_layout.addWidget(self.floating_translation_label)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_label_x)
        self.floating_translation_layout.addWidget(self.floating_translation_input_x)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_label_y)
        self.floating_translation_layout.addWidget(self.floating_translation_input_y)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_label_z)
        self.floating_translation_layout.addWidget(self.floating_translation_input_z)
        self.floating_translation_layout.addStretch(1)
        self.floating_translation_layout.addWidget(self.floating_translation_auto)

        self.floating_rotation_layout = QtGui.QHBoxLayout()
        self.floating_rotation_label = QtGui.QLabel(__("Rotation restriction: "))
        self.floating_rotation_label.setToolTip(__("Use 0 for rotation restriction in the movement (default=(1,1,1))"))
        self.floating_rotation_label_x = QtGui.QLabel("X")
        self.floating_rotation_input_x = QtGui.QComboBox()
        self.floating_rotation_input_x.insertItems(1, ['0', '1'])
        self.floating_rotation_label_y = QtGui.QLabel("Y")
        self.floating_rotation_input_y = QtGui.QComboBox()
        self.floating_rotation_input_y.insertItems(1, ['0', '1'])
        self.floating_rotation_label_z = QtGui.QLabel("Z")
        self.floating_rotation_input_z = QtGui.QComboBox()
        self.floating_rotation_input_z.insertItems(1, ['0', '1'])
        self.floating_rotation_auto = QtGui.QCheckBox("Auto ")
        self.floating_rotation_auto.toggled.connect(self.on_rotation_auto)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label_x)
        self.floating_rotation_layout.addWidget(self.floating_rotation_input_x)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label_y)
        self.floating_rotation_layout.addWidget(self.floating_rotation_input_y)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_label_z)
        self.floating_rotation_layout.addWidget(self.floating_rotation_input_z)
        self.floating_rotation_layout.addStretch(1)
        self.floating_rotation_layout.addWidget(self.floating_rotation_auto)

        self.floating_material_layout = QtGui.QHBoxLayout()
        self.floating_material_label = QtGui.QLabel(__("Material: "))
        #self.floating_material_label.setToolTip(__(""))
        self.floating_material_line_edit = QtGui.QLineEdit()
        self.floating_material_auto = QtGui.QCheckBox("Auto ")
        self.floating_material_auto.toggled.connect(self.on_material_auto)
        self.floating_material_layout.addWidget(self.floating_material_label)
        self.floating_material_layout.addWidget(self.floating_material_line_edit)
        self.floating_material_layout.addStretch(1)
        self.floating_material_layout.addWidget(self.floating_material_auto)

        self.floating_props_layout.addLayout(self.floating_props_massrhop_layout)
        self.floating_props_layout.addLayout(self.floating_center_layout)
        self.floating_props_layout.addLayout(self.floating_inertia_layout)
        self.floating_props_layout.addLayout(self.floating_velini_layout)
        self.floating_props_layout.addLayout(self.floating_omegaini_layout)
        self.floating_props_layout.addLayout(self.floating_rotation_layout)
        self.floating_props_layout.addLayout(self.floating_translation_layout)
        self.floating_props_layout.addLayout(self.floating_material_layout)
        self.floating_props_layout.addStretch(1)
        self.floating_props_group.setLayout(self.floating_props_layout)

        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.floatings_window_layout = QtGui.QVBoxLayout()
        self.floatings_window_layout.addLayout(self.is_floating_layout)
        self.floatings_window_layout.addWidget(self.floating_props_group)
        self.floatings_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.floatings_window_layout)

        if str(self.target_mk) in self.data['floating_mks'].keys():
            self.is_floating_selector.setCurrentIndex(0)
            self.on_floating_change(0)
            self.floating_props_group.setEnabled(True)
            self.floating_props_massrhop_selector.setCurrentIndex(self.data['floating_mks'][str(self.target_mk)].mass_density_type)
            self.floating_props_massrhop_input.setText(str(self.data['floating_mks'][str(self.target_mk)].mass_density_value))
            if len(self.data['floating_mks'][str(self.target_mk)].gravity_center) == 0:
                self.floating_center_input_x.setText("0")
                self.floating_center_input_y.setText("0")
                self.floating_center_input_z.setText("0")
            else:
                self.floating_center_input_x.setText(str(self.data['floating_mks'][str(self.target_mk)].gravity_center[0]))
                self.floating_center_input_y.setText(str(self.data['floating_mks'][str(self.target_mk)].gravity_center[1]))
                self.floating_center_input_z.setText(str(self.data['floating_mks'][str(self.target_mk)].gravity_center[2]))

            if len(self.data['floating_mks'][str(self.target_mk)].inertia) == 0:
                self.floating_inertia_input_x.setText("0")
                self.floating_inertia_input_y.setText("0")
                self.floating_inertia_input_z.setText("0")
            else:
                self.floating_inertia_input_x.setText(str(self.data['floating_mks'][str(self.target_mk)].inertia[0]))
                self.floating_inertia_input_y.setText(str(self.data['floating_mks'][str(self.target_mk)].inertia[1]))
                self.floating_inertia_input_z.setText(str(self.data['floating_mks'][str(self.target_mk)].inertia[2]))

            if len(self.data['floating_mks'][str(self.target_mk)].initial_linear_velocity) == 0:
                self.floating_velini_input_x.setText("0")
                self.floating_velini_input_y.setText("0")
                self.floating_velini_input_z.setText("0")
            else:
                self.floating_velini_input_x.setText(
                    str(self.data['floating_mks'][str(self.target_mk)].initial_linear_velocity[0]))
                self.floating_velini_input_y.setText(str(self.data['floating_mks'][str(self.target_mk)].initial_linear_velocity[1]))
                self.floating_velini_input_z.setText(str(self.data['floating_mks'][str(self.target_mk)].initial_linear_velocity[2]))

            if len(self.data['floating_mks'][str(self.target_mk)].initial_angular_velocity) == 0:
                self.floating_omegaini_input_x.setText("0")
                self.floating_omegaini_input_y.setText("0")
                self.floating_omegaini_input_z.setText("0")
            else:
                self.floating_omegaini_input_x.setText(
                    str(self.data['floating_mks'][str(self.target_mk)].initial_angular_velocity[0]))
                self.floating_omegaini_input_y.setText(str(self.data['floating_mks'][str(self.target_mk)].initial_angular_velocity[1]))
                self.floating_omegaini_input_z.setText(str(self.data['floating_mks'][str(self.target_mk)].initial_angular_velocity[2]))

            if len(self.data['floating_mks'][str(self.target_mk)].translation_restriction) == 0:
                self.floating_translation_input_x.setCurrentIndex(1)
                self.floating_translation_input_y.setCurrentIndex(1)
                self.floating_translation_input_z.setCurrentIndex(1)
            else:
                self.floating_translation_input_x.setCurrentIndex(
                    self.data['floating_mks'][str(self.target_mk)].translation_restriction[0])
                self.floating_translation_input_y.setCurrentIndex(
                    self.data['floating_mks'][str(self.target_mk)].translation_restriction[1])
                self.floating_translation_input_z.setCurrentIndex(
                    self.data['floating_mks'][str(self.target_mk)].translation_restriction[2])

            if len(self.data['floating_mks'][str(self.target_mk)].rotation_restriction) == 0:
                self.floating_rotation_input_x.setCurrentIndex(1)
                self.floating_rotation_input_y.setCurrentIndex(1)
                self.floating_rotation_input_z.setCurrentIndex(1)
            else:
                self.floating_rotation_input_x.setCurrentIndex(
                    self.data['floating_mks'][str(self.target_mk)].rotation_restriction[0])
                self.floating_rotation_input_y.setCurrentIndex(
                    self.data['floating_mks'][str(self.target_mk)].rotation_restriction[1])
                self.floating_rotation_input_z.setCurrentIndex(
                    self.data['floating_mks'][str(self.target_mk)].rotation_restriction[2])

            if len(self.data['floating_mks'][str(self.target_mk)].material) == 0:
                self.floating_material_line_edit.setText("")
            else:
                self.floating_material_line_edit.setText(self.data['floating_mks'][str(self.target_mk)].material)

            self.floating_center_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(self.target_mk)].gravity_center) == 0 else QtCore.Qt.Unchecked
            )
            self.floating_inertia_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(self.target_mk)].inertia) == 0 else QtCore.Qt.Unchecked
            )
            self.floating_velini_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(self.target_mk)].initial_linear_velocity) == 0 else QtCore.Qt.Unchecked
            )
            self.floating_omegaini_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(self.target_mk)].initial_angular_velocity) == 0 else QtCore.Qt.Unchecked
            )
            self.floating_translation_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(
                    self.target_mk)].translation_restriction) == 0 else QtCore.Qt.Unchecked
            )
            self.floating_rotation_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(
                    self.target_mk)].rotation_restriction) == 0 else QtCore.Qt.Unchecked
            )
            self.floating_material_auto.setCheckState(
                QtCore.Qt.Checked if len(self.data['floating_mks'][str(self.target_mk)].material) == 0 else
                QtCore.Qt.Unchecked
            )
        else:
            self.is_floating_selector.setCurrentIndex(1)
            self.on_floating_change(1)
            self.floating_props_group.setEnabled(False)
            self.is_floating_selector.setCurrentIndex(1)
            self.floating_props_massrhop_selector.setCurrentIndex(1)
            self.floating_props_massrhop_input.setText("1000")
            self.floating_center_input_x.setText("0")
            self.floating_center_input_y.setText("0")
            self.floating_center_input_z.setText("0")
            self.floating_inertia_input_x.setText("0")
            self.floating_inertia_input_y.setText("0")
            self.floating_inertia_input_z.setText("0")
            self.floating_velini_input_x.setText("0")
            self.floating_velini_input_y.setText("0")
            self.floating_velini_input_z.setText("0")
            self.floating_omegaini_input_x.setText("0")
            self.floating_omegaini_input_y.setText("0")
            self.floating_omegaini_input_z.setText("0")
            self.floating_translation_input_x.setCurrentIndex(1)
            self.floating_translation_input_y.setCurrentIndex(1)
            self.floating_translation_input_z.setCurrentIndex(1)
            self.floating_rotation_input_x.setCurrentIndex(1)
            self.floating_rotation_input_y.setCurrentIndex(1)
            self.floating_rotation_input_z.setCurrentIndex(1)
            self.floating_material_line_edit.setText("")

            self.floating_center_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_inertia_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_velini_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_omegaini_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_translation_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_rotation_auto.setCheckState(QtCore.Qt.Checked)
            self.floating_material_auto.setCheckState(QtCore.Qt.Checked)

        self.exec_()

    def on_ok(self):
        guiutils.info_dialog(
            __("This will apply the floating properties to all objects with mkbound = ") + str(self.target_mk))
        if self.is_floating_selector.currentIndex() == 1:
            # Floating false
            if str(self.target_mk) in self.data['floating_mks'].keys():
                self.data['floating_mks'].pop(str(self.target_mk), None)
        else:
            # Floating true
            # Structure: 'mk': [massrhop, center, inertia, velini, omegaini]
            # Structure: 'mk': FloatProperty
            fp = FloatProperty()  # FloatProperty to be inserted
            fp.mk = self.target_mk
            fp.mass_density_type = self.floating_props_massrhop_selector.currentIndex()
            fp.mass_density_value = float(self.floating_props_massrhop_input.text())

            if self.floating_center_auto.isChecked():
                fp.gravity_center = list()
            else:
                fp.gravity_center = [
                    float(self.floating_center_input_x.text()),
                    float(self.floating_center_input_y.text()),
                    float(self.floating_center_input_z.text())
                ]

            if self.floating_center_auto.isChecked():
                fp.gravity_center = list()
            else:
                fp.gravity_center = [
                    float(self.floating_center_input_x.text()),
                    float(self.floating_center_input_y.text()),
                    float(self.floating_center_input_z.text())
                ]

            if self.floating_inertia_auto.isChecked():
                fp.inertia = list()
            else:
                fp.inertia = [
                    float(self.floating_inertia_input_x.text()),
                    float(self.floating_inertia_input_y.text()),
                    float(self.floating_inertia_input_z.text())
                ]

            if self.floating_velini_auto.isChecked():
                fp.initial_linear_velocity = list()
            else:
                fp.initial_linear_velocity = [
                    float(self.floating_velini_input_x.text()),
                    float(self.floating_velini_input_y.text()),
                    float(self.floating_velini_input_z.text())
                ]

            if self.floating_omegaini_auto.isChecked():
                fp.initial_angular_velocity = list()
            else:
                fp.initial_angular_velocity = [
                    float(self.floating_omegaini_input_x.text()),
                    float(self.floating_omegaini_input_y.text()),
                    float(self.floating_omegaini_input_z.text())
                ]

            if self.floating_translation_auto.isChecked():
                fp.translation_restriction = list()
            else:
                fp.translation_restriction = [
                    int(self.floating_translation_input_x.currentIndex()),
                    int(self.floating_translation_input_y.currentIndex()),
                    int(self.floating_translation_input_z.currentIndex())
                ]

            if self.floating_rotation_auto.isChecked():
                fp.rotation_restriction = list()
            else:
                fp.rotation_restriction = [
                    int(self.floating_rotation_input_x.currentIndex()),
                    int(self.floating_rotation_input_y.currentIndex()),
                    int(self.floating_rotation_input_z.currentIndex())
                ]

            if self.floating_material_auto.isChecked():
                fp.material = ""
            else:
                fp.material = str(self.floating_material_line_edit.text())

            self.data['floating_mks'][str(self.target_mk)] = fp

        self.accept()

    def on_cancel(self):
        self.reject()

    def on_floating_change(self, index):
        if index == 0:
            self.floating_props_group.setEnabled(True)
        else:
            self.floating_props_group.setEnabled(False)

    def on_massrhop_change(self, index):
        if index == 0:
            self.floating_props_massrhop_input.setText("0.0")
        else:
            self.floating_props_massrhop_input.setText("0.0")

    def on_gravity_auto(self):
        if self.floating_center_auto.isChecked():
            self.floating_center_input_x.setEnabled(False)
            self.floating_center_input_y.setEnabled(False)
            self.floating_center_input_z.setEnabled(False)
        else:
            self.floating_center_input_x.setEnabled(True)
            self.floating_center_input_y.setEnabled(True)
            self.floating_center_input_z.setEnabled(True)

    def on_inertia_auto(self):
        if self.floating_inertia_auto.isChecked():
            self.floating_inertia_input_x.setEnabled(False)
            self.floating_inertia_input_y.setEnabled(False)
            self.floating_inertia_input_z.setEnabled(False)
        else:
            self.floating_inertia_input_x.setEnabled(True)
            self.floating_inertia_input_y.setEnabled(True)
            self.floating_inertia_input_z.setEnabled(True)

    def on_velini_auto(self):
        if self.floating_velini_auto.isChecked():
            self.floating_velini_input_x.setEnabled(False)
            self.floating_velini_input_y.setEnabled(False)
            self.floating_velini_input_z.setEnabled(False)
        else:
            self.floating_velini_input_x.setEnabled(True)
            self.floating_velini_input_y.setEnabled(True)
            self.floating_velini_input_z.setEnabled(True)

    def on_omegaini_auto(self):
        if self.floating_omegaini_auto.isChecked():
            self.floating_omegaini_input_x.setEnabled(False)
            self.floating_omegaini_input_y.setEnabled(False)
            self.floating_omegaini_input_z.setEnabled(False)
        else:
            self.floating_omegaini_input_x.setEnabled(True)
            self.floating_omegaini_input_y.setEnabled(True)
            self.floating_omegaini_input_z.setEnabled(True)

    def on_translation_auto(self):
        if self.floating_translation_auto.isChecked():
            self.floating_translation_input_x.setEnabled(False)
            self.floating_translation_input_y.setEnabled(False)
            self.floating_translation_input_z.setEnabled(False)
        else:
            self.floating_translation_input_x.setEnabled(True)
            self.floating_translation_input_y.setEnabled(True)
            self.floating_translation_input_z.setEnabled(True)

    def on_rotation_auto(self):
        if self.floating_rotation_auto.isChecked():
            self.floating_rotation_input_x.setEnabled(False)
            self.floating_rotation_input_y.setEnabled(False)
            self.floating_rotation_input_z.setEnabled(False)
        else:
            self.floating_rotation_input_x.setEnabled(True)
            self.floating_rotation_input_y.setEnabled(True)
            self.floating_rotation_input_z.setEnabled(True)

    def on_material_auto(self):
        if self.floating_material_auto.isChecked():
            self.floating_material_line_edit.setEnabled(False)
        else:
            self.floating_material_line_edit.setEnabled(True)


class InitialsDialog(QtGui.QDialog):
    """ Defines a window with initials properties. """
    def __init__(self, data):
        super(InitialsDialog, self).__init__()

        self.data = data

        self.setWindowTitle(__("Initials configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.target_mk = int(self.data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_initials_layout = QtGui.QHBoxLayout()
        self.has_initials_label = QtGui.QLabel(__("Set initials: "))
        self.has_initials_label.setToolTip(__("Sets the current initial movement vector."))
        self.has_initials_selector = QtGui.QComboBox()
        self.has_initials_selector.insertItems(0, ['True', 'False'])
        self.has_initials_selector.currentIndexChanged.connect(self.on_initials_change)
        self.has_initials_targetlabel = QtGui.QLabel(__("Target MKFluid: ") + str(self.target_mk))
        self.has_initials_layout.addWidget(self.has_initials_label)
        self.has_initials_layout.addWidget(self.has_initials_selector)
        self.has_initials_layout.addStretch(1)
        self.has_initials_layout.addWidget(self.has_initials_targetlabel)

        self.initials_props_group = QtGui.QGroupBox(__("Initials properties"))
        self.initials_props_layout = QtGui.QVBoxLayout()

        self.initials_vector_layout = QtGui.QHBoxLayout()
        self.initials_vector_label = QtGui.QLabel(__("Movement vector: "))
        self.initials_vector_label.setToolTip(__("Sets the mk group movement vector."))
        self.initials_vector_label_x = QtGui.QLabel("X")
        self.initials_vector_input_x = QtGui.QLineEdit()
        self.initials_vector_label_y = QtGui.QLabel("Y")
        self.initials_vector_input_y = QtGui.QLineEdit()
        self.initials_vector_label_z = QtGui.QLabel("Z")
        self.initials_vector_input_z = QtGui.QLineEdit()
        self.initials_vector_layout.addWidget(self.initials_vector_label)
        self.initials_vector_layout.addWidget(self.initials_vector_label_x)
        self.initials_vector_layout.addWidget(self.initials_vector_input_x)
        self.initials_vector_layout.addWidget(self.initials_vector_label_y)
        self.initials_vector_layout.addWidget(self.initials_vector_input_y)
        self.initials_vector_layout.addWidget(self.initials_vector_label_z)
        self.initials_vector_layout.addWidget(self.initials_vector_input_z)

        self.initials_props_layout.addLayout(self.initials_vector_layout)
        self.initials_props_layout.addStretch(1)
        self.initials_props_group.setLayout(self.initials_props_layout)

        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.initials_window_layout = QtGui.QVBoxLayout()
        self.initials_window_layout.addLayout(self.has_initials_layout)
        self.initials_window_layout.addWidget(self.initials_props_group)
        self.initials_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.initials_window_layout)

        if str(self.target_mk) in self.data['initials_mks'].keys():
            self.has_initials_selector.setCurrentIndex(0)
            self.on_initials_change(0)
            self.initials_props_group.setEnabled(True)
            self.initials_vector_input_x.setText(str(self.data['initials_mks'][str(self.target_mk)].force[0]))
            self.initials_vector_input_y.setText(str(self.data['initials_mks'][str(self.target_mk)].force[1]))
            self.initials_vector_input_z.setText(str(self.data['initials_mks'][str(self.target_mk)].force[2]))
        else:
            self.has_initials_selector.setCurrentIndex(1)
            self.on_initials_change(1)
            self.initials_props_group.setEnabled(False)
            self.has_initials_selector.setCurrentIndex(1)
            self.initials_vector_input_x.setText("0")
            self.initials_vector_input_y.setText("0")
            self.initials_vector_input_z.setText("0")

        self.exec_()

    # Ok button handler
    def on_ok(self):
        guiutils.info_dialog(__("This will apply the initials properties to all objects with mkfluid = ") + str(self.target_mk))
        if self.has_initials_selector.currentIndex() == 1:
            # Initials false
            if str(self.target_mk) in self.data['initials_mks'].keys():
                self.data['initials_mks'].pop(str(self.target_mk), None)
        else:
            # Initials true
            # Structure: InitialsProperty Object
            self.data['initials_mks'][str(self.target_mk)] = InitialsProperty(
                mk=self.target_mk,
                force=[
                    float(self.initials_vector_input_x.text()),
                    float(self.initials_vector_input_y.text()),
                    float(self.initials_vector_input_z.text())
                ])
        self.accept()

    # Cancel button handler
    def on_cancel(self):
        self.reject()

    # Initials enable/disable dropdown handler
    def on_initials_change(self, index):
        if index == 0:
            self.initials_props_group.setEnabled(True)
        else:
            self.initials_props_group.setEnabled(False)


class MovementDialog(QtGui.QDialog):
    """ Defines a window with motion properties. """

    def __init__(self, data):
        super(MovementDialog, self).__init__()

        self.data = data

        self.setMinimumSize(1400, 650)
        self.setWindowTitle(__("Motion configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.notice_label = QtGui.QLabel("")
        self.notice_label.setStyleSheet("QLabel { color : red; }")
        self.target_mk = int(self.data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])
        self.movements_selected = list(self.data["motion_mks"].get(self.target_mk, list()))

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.has_motion_layout = QtGui.QHBoxLayout()
        self.has_motion_label = QtGui.QLabel(__("Set motion: "))
        self.has_motion_label.setToolTip(__("Enables motion for the selected MKBound"))
        self.has_motion_selector = QtGui.QComboBox()
        self.has_motion_selector.insertItems(0, ["True", "False"])
        self.has_motion_selector.currentIndexChanged.connect(self.on_motion_change)

        ##############################################################################

        self.create_new_movement_button = QtGui.QToolButton()
        self.create_new_movement_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.create_new_movement_button.setText(" {}".format(__("Create New")))

        self.create_new_movement_menu = QtGui.QMenu()
        self.create_new_movement_menu.addAction(guiutils.get_icon("movement.png"), __("Movement"))
        self.create_new_movement_menu.addAction(guiutils.get_icon("regular_wave.png"), __("Regular wave generator (Piston)"))
        self.create_new_movement_menu.addAction(guiutils.get_icon("irregular_wave.png"),
                                           __("Irregular wave generator (Piston)"))
        self.create_new_movement_menu.addAction(guiutils.get_icon("regular_wave.png"), __("Regular wave generator (Flap)"))
        self.create_new_movement_menu.addAction(guiutils.get_icon("irregular_wave.png"),
                                           __("Irregular wave generator (Flap)"))
        self.create_new_movement_menu.addAction(guiutils.get_icon("file_mov.png"), __("Linear motion from a file"))
        self.create_new_movement_menu.addAction(guiutils.get_icon("file_mov.png"), __("Rotation from a file"))
        self.create_new_movement_button.setMenu(self.create_new_movement_menu)

        ##############################################################################


        self.has_motion_helplabel = QtGui.QLabel(
            "<a href='http://design.sphysics.org/wiki/doku.php?id=featreference#configure_object_motion'>{}</a>".format(
                __("Movement Help")))
        self.has_motion_helplabel.setTextFormat(QtCore.Qt.RichText)
        self.has_motion_helplabel.setTextInteractionFlags(
            QtCore.Qt.TextBrowserInteraction)
        self.has_motion_helplabel.setOpenExternalLinks(True)
        self.has_motion_targetlabel = QtGui.QLabel(__("Target MKBound: ") + str(self.target_mk))
        self.has_motion_layout.addWidget(self.has_motion_label)
        self.has_motion_layout.addWidget(self.has_motion_selector)
        self.has_motion_layout.addStretch(1)
        self.has_motion_layout.addWidget(self.has_motion_helplabel)
        self.has_motion_layout.addWidget(self.has_motion_targetlabel)

        self.motion_features_layout = QtGui.QVBoxLayout()
        self.motion_features_splitter = QtGui.QSplitter()

        self.movement_list_groupbox = QtGui.QGroupBox(__("Global Movements"))
        self.movement_list_groupbox_layout = QtGui.QVBoxLayout()

        self.movement_list_table = QtGui.QTableWidget(1, 2)
        self.movement_list_table.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectItems)
        self.movement_list_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.movement_list_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.movement_list_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.movement_list_table.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

        self.movement_list_table.verticalHeader().setVisible(False)
        self.movement_list_table.horizontalHeader().setVisible(False)

        self.movement_list_groupbox_layout.addWidget(self.create_new_movement_button)
        self.movement_list_groupbox_layout.addWidget(self.movement_list_table)
        self.movement_list_groupbox.setLayout(self.movement_list_groupbox_layout)

        self.timeline_groupbox = QtGui.QGroupBox(__("Timeline for the selected movement"))
        self.timeline_groupbox_layout = QtGui.QVBoxLayout()

        self.timeline_list_table = QtGui.QTableWidget(0, 1)
        self.timeline_list_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.timeline_list_table.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.timeline_list_table.verticalHeader().setVisible(False)
        self.timeline_list_table.horizontalHeader().setVisible(False)
        self.timeline_list_table.resizeRowsToContents()

        self.timeline_groupbox_layout.addWidget(self.timeline_list_table)
        self.timeline_groupbox.setLayout(self.timeline_groupbox_layout)

        self.actions_groupbox = QtGui.QGroupBox(__("Available actions"))
        self.actions_groupbox_layout = QtGui.QVBoxLayout()

        self.actions_groupbox_table = QtGui.QTableWidget(0, 1)
        self.actions_groupbox_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.actions_groupbox_table.verticalHeader().setVisible(False)
        self.actions_groupbox_table.horizontalHeader().setVisible(False)

        self.actions_groupbox_layout.addWidget(self.actions_groupbox_table)
        self.actions_groupbox.setLayout(self.actions_groupbox_layout)

        self.motion_features_splitter.addWidget(self.movement_list_groupbox)
        self.motion_features_splitter.addWidget(self.timeline_groupbox)
        self.motion_features_splitter.addWidget(self.actions_groupbox)
        self.motion_features_splitter.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.motion_features_layout.addWidget(self.motion_features_splitter)

        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.addWidget(self.notice_label)
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.motion_window_layout = QtGui.QVBoxLayout()
        self.motion_window_layout.addLayout(self.has_motion_layout)
        self.motion_window_layout.addLayout(self.motion_features_layout)
        self.motion_window_layout.addLayout(self.buttons_layout)

        self.setLayout(self.motion_window_layout)

        self.refresh_movements_table()
        self.movement_list_table.cellChanged.connect(self.on_movement_name_change)
        self.movement_list_table.cellClicked.connect(self.on_movement_selected)

        self.actions_groupbox_table.setRowCount(9)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add a delay"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_delay)
        self.actions_groupbox_table.setCellWidget(0, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add a rectilinear motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_rectilinear)
        self.actions_groupbox_table.setCellWidget(1, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add an accelerated rectilinear motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_accrectilinear)
        self.actions_groupbox_table.setCellWidget(2, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add a rotational motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_rotational)
        self.actions_groupbox_table.setCellWidget(3, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add an accelerated rotational motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_acc_rotational)
        self.actions_groupbox_table.setCellWidget(4, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add an accelerated circular motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_acc_circular)
        self.actions_groupbox_table.setCellWidget(5, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add a sinusoidal rotational motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_sinu_rot)
        self.actions_groupbox_table.setCellWidget(6, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add a sinusoidal circular motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_sinu_cir)
        self.actions_groupbox_table.setCellWidget(7, 0, self.bt_to_add)
        self.bt_to_add = QtGui.QPushButton(guiutils.get_icon("left-arrow.png"), __("Add a sinusoidal rectilinear motion"))
        self.bt_to_add.setStyleSheet("text-align: left")
        self.bt_to_add.clicked.connect(self.on_add_sinu_rect)
        self.actions_groupbox_table.setCellWidget(8, 0, self.bt_to_add)

        # Set motion suscription for this mk
        if self.data["motion_mks"].get(self.target_mk, None) is None:
            self.has_motion_selector.setCurrentIndex(1)
        else:
            self.has_motion_selector.setCurrentIndex(0)

        self.exec_()

    def on_ok(self):
        guiutils.info_dialog(
            __("This will apply the motion properties to all objects with mkbound = ") + str(self.target_mk))
        if self.has_motion_selector.currentIndex() == 0:
            # True has been selected
            # Reinstance the list and copy every movement selected to avoid referencing problems.
            self.data["motion_mks"][self.target_mk] = list()
            for movement in self.movements_selected:
                self.data["motion_mks"][self.target_mk].append(movement)
        elif self.has_motion_selector.currentIndex() == 1:
            # False has been selected
            self.data["motion_mks"].pop(self.target_mk, None)
        self.accept()

    def on_cancel(self):
        self.reject()

    def on_motion_change(self, index):
        """ Set motion action. Enables or disables parts of the window depending
        on what option was selected. """
        if index == 0:
            self.movement_list_groupbox.setEnabled(True)
            self.timeline_groupbox.setEnabled(True)
            self.actions_groupbox.setEnabled(True)
            self.timeline_list_table.setEnabled(False)
            self.actions_groupbox_table.setEnabled(False)

            # Put a placeholder in the table
            self.timeline_list_table.clearContents()
            self.timeline_list_table.setRowCount(1)
            self.timeline_list_table.setCellWidget(0, 0, MovementTimelinePlaceholder())
        else:
            self.movement_list_groupbox.setEnabled(False)
            self.timeline_groupbox.setEnabled(False)
            self.actions_groupbox.setEnabled(False)

    def check_movement_compatibility(self, target_movement):
        # Wave generators are exclusive
        if isinstance(target_movement, properties.SpecialMovement):
            self.notice_label.setText("Notice: Wave generators and file movements are exclusive. "
                                      "All movements are disabled when using one.")
            del self.movements_selected[:]
        elif isinstance(target_movement, properties.Movement):
            for index, ms in enumerate(self.movements_selected):
                if isinstance(ms, properties.SpecialMovement):
                    self.movements_selected.pop(index)
                    self.notice_label.setText(
                        "Notice: Regular movements are not compatible with wave generators and file movements.")

    # Movements table actions
    def on_check_movement(self, index, checked):
        """ Add or delete a movement from the temporal list of selected movements. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        target_movement = self.data["global_movements"][index]
        if checked:
            self.check_movement_compatibility(target_movement)
            self.movements_selected.append(target_movement)
        else:
            self.movements_selected.remove(target_movement)
        self.refresh_movements_table()

    def on_loop_movement(self, index, checked):
        """ Make a movement loop itself """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        self.data["global_movements"][index].set_loop(checked)

    def on_delete_movement(self, index):
        """ Remove a movement from the project. """
        try:
            self.movements_selected.remove(self.data["global_movements"][index])
            # Reset the notice label if a valid change is made
            self.notice_label.setText("")
        except ValueError:
            # Movement wasn't selected
            pass
        self.data["global_movements"].pop(index)
        self.refresh_movements_table()
        self.on_movement_selected(self.timeline_list_table.rowCount() - 1, None)

    def on_new_movement(self):
        """ Creates a movement on the project. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        to_add = properties.Movement(name="New Movement")
        self.data["global_movements"].append(to_add)
        self.movements_selected.append(to_add)
        self.check_movement_compatibility(to_add)

        self.refresh_movements_table()

    def on_new_wave_generator(self, action):
        """ Creates a movement on the project. """

        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if utils.__("Movement") in action.text():
            self.on_new_movement()
            return
        if utils.__("Regular wave generator (Piston)") in action.text():
            to_add = properties.SpecialMovement(name="Regular Wave Generator (Piston)", generator=properties.RegularPistonWaveGen())
        if utils.__("Irregular wave generator (Piston)") in action.text():
            to_add = properties.SpecialMovement(name="Irregular Wave Generator (Piston)", generator=properties.IrregularPistonWaveGen())
        if utils.__("Regular wave generator (Flap)") in action.text():
            to_add = properties.SpecialMovement(name="Regular Wave Generator (Flap)", generator=properties.RegularFlapWaveGen())
        if utils.__("Irregular wave generator (Flap)") in action.text():
            to_add = properties.SpecialMovement(name="Irregular Wave Generator (Flap)", generator=properties.IrregularFlapWaveGen())
        if utils.__("Linear motion from a file") in action.text():
            to_add = properties.SpecialMovement(name="Linear motion from a file", generator=properties.FileGen())
        if utils.__("Rotation from a file") in action.text():
            to_add = properties.SpecialMovement(name="Rotation from a file", generator=properties.RotationFileGen())

        to_add.generator.parent_movement = to_add
        self.data["global_movements"].append(to_add)
        self.check_movement_compatibility(to_add)
        self.movements_selected.append(to_add)

        self.refresh_movements_table()

    def on_movement_name_change(self, row, column):
        """ Changes the name of a movement on the project. """
        target_item = self.movement_list_table.item(row, column)
        if target_item is not None and self.data["global_movements"][row].name != target_item.text():
            # Reset the notice label if a valid change is made
            self.notice_label.setText("")
            self.data["global_movements"][row].name = target_item.text()

    def on_timeline_item_change(self, index, motion_object):
        """ Changes the values of an item on the timeline. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if isinstance(motion_object, properties.WaveGen):
            motion_object.parent_movement.set_wavegen(motion_object)
        else:
            motion_object.parent_movement.motion_list[index] = motion_object

    def on_timeline_item_delete(self, index, motion_object):
        """ Deletes an item from the timeline. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        motion_object.parent_movement.motion_list.pop(index)
        self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_timeline_item_order_up(self, index):
        # Reset the notice label if a valid change is made
        self.notice_label.setText("")
        movement = self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()]
        self.movement.motion_list.insert(index - 1, self.movement.motion_list.pop(index))
        self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_timeline_item_order_down(self, index):
        # Reset the notice label if a valid change is made
        self.notice_label.setText("")
        movement = self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()]
        movement.motion_list.insert(index + 1, movement.motion_list.pop(index))
        self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)


    def on_movement_selected(self, row, _):
        """ Shows the timeline for the selected movement. """
        try:
            target_movement = self.data["global_movements"][row]
        except IndexError:
            self.timeline_list_table.clearContents()
            self.timeline_list_table.setEnabled(False)
            self.timeline_list_table.setRowCount(1)
            self.timeline_list_table.setCellWidget(0, 0, MovementTimelinePlaceholder())
            return
        self.timeline_list_table.clearContents()

        # Reset the notice label if a valid change is made
        self.notice_label.setText("")

        if isinstance(target_movement, properties.Movement):
            self.timeline_list_table.setRowCount(len(target_movement.motion_list))
            self.timeline_list_table.setEnabled(True)
            self.actions_groupbox_table.setEnabled(True)

            current_row = 0
            for motion in target_movement.motion_list:
                if isinstance(motion, properties.RectMotion):
                    target_to_put = RectilinearMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.WaitMotion):
                    target_to_put = WaitMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.AccRectMotion):
                    target_to_put = AccRectilinearMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.RotMotion):
                    target_to_put = RotationalMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.AccRotMotion):
                    target_to_put = AccRotationalMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.AccCirMotion):
                    target_to_put = AccCircularMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.RotSinuMotion):
                    target_to_put = RotSinuMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.CirSinuMotion):
                    target_to_put = CirSinuMotionTimeline(current_row, motion)
                elif isinstance(motion, properties.RectSinuMotion):
                    target_to_put = RectSinuMotionTimeline(current_row, motion)
                else:
                    raise NotImplementedError("The type of movement: {} is not implemented.".format(
                        str(motion.__class__.__name__)))

                target_to_put.changed.connect(self.on_timeline_item_change)
                target_to_put.deleted.connect(self.on_timeline_item_delete)
                target_to_put.order_up.connect(self.on_timeline_item_order_up)
                target_to_put.order_down.connect(self.on_timeline_item_order_down)
                self.timeline_list_table.setCellWidget(current_row, 0, target_to_put)

                if current_row is 0:
                    target_to_put.disable_order_up_button()
                elif current_row is len(target_movement.motion_list) - 1:
                    target_to_put.disable_order_down_button()

                current_row += 1
        elif isinstance(target_movement, properties.SpecialMovement):
            self.timeline_list_table.setRowCount(1)
            self.timeline_list_table.setEnabled(True)
            self.actions_groupbox_table.setEnabled(False)

            if isinstance(target_movement.generator, properties.RegularPistonWaveGen):
                target_to_put = RegularPistonWaveMotionTimeline(target_movement.generator)
            elif isinstance(target_movement.generator, properties.IrregularPistonWaveGen):
                target_to_put = IrregularPistonWaveMotionTimeline(target_movement.generator)
            if isinstance(target_movement.generator, properties.RegularFlapWaveGen):
                target_to_put = RegularFlapWaveMotionTimeline(target_movement.generator)
            elif isinstance(target_movement.generator, properties.IrregularFlapWaveGen):
                target_to_put = IrregularFlapWaveMotionTimeline(target_movement.generator)
            elif isinstance(target_movement.generator, properties.FileGen):
                target_to_put = FileMotionTimeline(target_movement.generator, self.data['project_path'])
            elif isinstance(target_movement.generator, properties.RotationFileGen):
                target_to_put = RotationFileMotionTimeline(target_movement.generator, self.data['project_path'])

            target_to_put.changed.connect(self.on_timeline_item_change)
            self.timeline_list_table.setCellWidget(0, 0, target_to_put)

    # Populate case defined movements
    def refresh_movements_table(self):
        """ Refreshes the movement table. """
        self.movement_list_table.clearContents()
        self.movement_list_table.setRowCount(len(self.data["global_movements"]) + 1)
        current_row = 0
        for movement in self.data["global_movements"]:
            self.movement_list_table.setItem(current_row, 0, QtGui.QTableWidgetItem(movement.name))
            try:
                has_loop = movement.loop
            except AttributeError:
                has_loop = False
            if isinstance(movement, properties.Movement):
                movement_actions = MovementActions(current_row, movement in self.movements_selected, has_loop)
                movement_actions.loop.connect(self.on_loop_movement)
            elif isinstance(movement, properties.SpecialMovement):
                movement_actions = WaveMovementActions(current_row, movement in self.movements_selected)

            movement_actions.delete.connect(self.on_delete_movement)
            movement_actions.use.connect(self.on_check_movement)
            self.movement_list_table.setCellWidget(current_row, 1, movement_actions)

            current_row += 1
        #create_new_movement_button = QtGui.QToolButton()
        #create_new_movement_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        #create_new_movement_button.setText(__("Create New"))

        #create_new_movement_menu = QtGui.QMenu()
        #create_new_movement_menu.addAction(guiutils.get_icon("movement.png"), __("Movement"))
        #create_new_movement_menu.addAction(guiutils.get_icon("regular_wave.png"), __("Regular wave generator (Piston)"))
        #create_new_movement_menu.addAction(guiutils.get_icon("irregular_wave.png"), __("Irregular wave generator (Piston)"))
        #create_new_movement_menu.addAction(guiutils.get_icon("regular_wave.png"), __("Regular wave generator (Flap)"))
        #create_new_movement_menu.addAction(guiutils.get_icon("irregular_wave.png"), __("Irregular wave generator (Flap)"))
        #create_new_movement_menu.addAction(guiutils.get_icon("file_mov.png"), __("Linear motion from a file"))
        #create_new_movement_menu.addAction(guiutils.get_icon("file_mov.png"), __("Rotation from a file"))
        #create_new_movement_button.setMenu(create_new_movement_menu)
        self.create_new_movement_button.clicked.connect(self.on_new_movement)
        self.create_new_movement_menu.triggered.connect(self.on_new_wave_generator)

        #self.movement_list_table.setCellWidget(current_row, 1, self.create_new_movement_button)
        self.movement_list_table.setCellWidget(current_row, 0, QtGui.QWidget())
    # Possible actions for adding motions to a movement

    def on_add_delay(self):
        """ Adds a WaitMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.WaitMotion())
                self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_rectilinear(self):
        """ Adds a RectMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.RectMotion())
                self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_accrectilinear(self):
        """ Adds a AccRectMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.AccRectMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_rotational(self):
        """ Adds a RotMotion to the timeline of the selected movement. """
        self.notice_label.setText(
            "")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.RotMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_acc_rotational(self):
        """ Adds a AccRotMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.AccRotMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_acc_circular(self):
        """ Adds a AccCirMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.AccCirMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_sinu_rot(self):
        """ Adds a RotSinuMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.RotSinuMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_sinu_cir(self):
        """ Adds a CirSinuMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.CirSinuMotion())
                self.on_movement_selected(
                    self.movement_list_table.selectedIndexes()[0].row(), None)

    def on_add_sinu_rect(self):
        """ Adds a RectSinuMotion to the timeline of the selected movement. """
        self.notice_label.setText("")  # Reset the notice label if a valid change is made
        if len(self.movement_list_table.selectedIndexes()) > 0:
            if self.movement_list_table.selectedIndexes()[0].row() is not len(self.data["global_movements"]):
                self.data["global_movements"][self.movement_list_table.selectedIndexes()[0].row()].add_motion(properties.RectSinuMotion())
                self.on_movement_selected(self.movement_list_table.selectedIndexes()[0].row(), None)


class FacesDialog(QtGui.QDialog):
    """  """
    def __init__(self, data):
        super(FacesDialog, self).__init__()

        self.data = data

        self.setWindowTitle(__("Faces configuration"))
        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))
        self.main_faces_layout = QtGui.QVBoxLayout()

        self.target_mk = int(self.data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])
        self.name = FreeCADGui.Selection.getSelection()[0].Label

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.faces_layout = QtGui.QVBoxLayout()

        self.all_faces = QtGui.QCheckBox(__("All faces"))
        self.all_faces.toggled.connect(self.on_faces_checkbox)

        self.front_face = QtGui.QCheckBox(__("Front face"))

        self.back_face = QtGui.QCheckBox(__("Back face"))

        self.top_face = QtGui.QCheckBox(__("Top face"))

        self.bottom_face = QtGui.QCheckBox(__("Bottom face"))

        self.left_face = QtGui.QCheckBox(__("Left face"))

        self.right_face = QtGui.QCheckBox(__("Right face"))

        try:
            if (str(self.target_mk), self.name) in self.data['faces'].keys():
                if self.data['faces'][str(self.target_mk), self.name].all_faces:
                    self.all_faces.setCheckState(QtCore.Qt.Checked)
                else:
                    self.all_faces.setCheckState(QtCore.Qt.Unchecked)
                self.all_faces.toggled.connect(self.on_faces_checkbox)

                if self.data['faces'][str(self.target_mk), self.name].front_face:
                    self.front_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.front_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].back_face:
                    self.back_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.back_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].top_face:
                    self.top_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.top_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].bottom_face:
                    self.bottom_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.bottom_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].left_face:
                    self.left_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.left_face.setCheckState(QtCore.Qt.Unchecked)

                if self.data['faces'][str(self.target_mk), self.name].right_face:
                    self.right_face.setCheckState(QtCore.Qt.Checked)
                else:
                    self.right_face.setCheckState(QtCore.Qt.Unchecked)
        except:
            pass

        self.faces_layout.addWidget(self.all_faces)
        self.faces_layout.addWidget(self.front_face)
        self.faces_layout.addWidget(self.back_face)
        self.faces_layout.addWidget(self.top_face)
        self.faces_layout.addWidget(self.bottom_face)
        self.faces_layout.addWidget(self.left_face)
        self.faces_layout.addWidget(self.right_face)

        self.main_faces_layout.addLayout(self.faces_layout)
        self.main_faces_layout.addLayout(self.button_layout)

        self.setLayout(self.main_faces_layout)

        self.on_faces_checkbox()

        self.exec_()

    def on_ok(self):

        fp = FacesProperty()
        fp.mk = self.target_mk

        if self.all_faces.isChecked():
            fp.all_faces = True
            fp.back_face = False
            fp.front_face = False
            fp.top_face = False
            fp.bottom_face = False
            fp.left_face = False
            fp.right_face = False
            fp.face_print = 'all'
        else:
            fp.all_faces = False

            if self.front_face.isChecked():
                fp.front_face = True
                fp.face_print = 'front'
            else:
                fp.front_face = False

            if self.back_face.isChecked():
                fp.back_face = True
                if fp.face_print != '':
                    fp.face_print += ' | back'
                else:
                    fp.face_print = 'back'
            else:
                fp.back_face = False

            if self.top_face.isChecked():
                fp.top_face = True
                if fp.face_print != '':
                    fp.face_print += ' | top'
                else:
                    fp.face_print = 'top'
            else:
                fp.top_face = False

            if self.bottom_face.isChecked():
                fp.bottom_face = True
                if fp.face_print != '':
                    fp.face_print += ' | bottom'
                else:
                    fp.face_print = 'bottom'
            else:
                fp.bottom_face = False

            if self.left_face.isChecked():
                fp.left_face = True
                if fp.face_print != '':
                    fp.face_print += ' | left'
                else:
                    fp.face_print = 'left'
            else:
                fp.left_face = False

            if self.right_face.isChecked():
                fp.right_face = True
                if fp.face_print != '':
                    fp.face_print += ' | right'
                else:
                    fp.face_print = 'right'
            else:
                fp.right_face = False

        self.data['faces'][str(self.target_mk), self.name] = fp

        self.accept()

    def on_cancel(self):
        self.reject()

    def on_faces_checkbox(self):
        """ Checks the faces state """
        if self.all_faces.isChecked():
            self.front_face.setEnabled(False)
            self.back_face.setEnabled(False)
            self.top_face.setEnabled(False)
            self.bottom_face.setEnabled(False)
            self.left_face.setEnabled(False)
            self.right_face.setEnabled(False)
        else:
            self.front_face.setEnabled(True)
            self.back_face.setEnabled(True)
            self.top_face.setEnabled(True)
            self.bottom_face.setEnabled(True)
            self.left_face.setEnabled(True)
            self.right_face.setEnabled(True)