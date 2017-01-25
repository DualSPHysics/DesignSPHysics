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
from utils import __
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
    use = QtCore.Signal(int)

    def __init__(self, index):
        super(MovementActions, self).__init__()
        self.index = index
        self.use_checkbox = QtGui.QCheckBox(__("Use"))
        self.use_checkbox.stateChanged.connect(self.on_use)
        self.delete_button = QtGui.QPushButton(QtGui.QIcon(FreeCAD.getUserAppDataDir()
                                                           + "Macro/DSPH_Images/trash.png"), None)
        self.delete_button.clicked.connect(self.on_delete)
        self.setContentsMargins(0, 0, 0, 0)
        temp_layout = QtGui.QHBoxLayout()
        temp_layout.setContentsMargins(10, 0, 10, 0)
        temp_layout.addWidget(self.use_checkbox)
        temp_layout.addWidget(self.delete_button)
        self.setLayout(temp_layout)

    def on_delete(self):
        self.delete.emit(self.index)

    def on_use(self):
        self.use.emit(self.index)


class RectilinearMotionTimeline(QtGui.QWidget):
    """ A Rectilinear motion grapihcal representation for a table-based timeline """

    def __init__(self, rect_motion):
        if not isinstance(rect_motion, RectMotion):
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if rect_motion is None:
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline without a motion object")
        super(RectilinearMotionTimeline, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.label = QtGui.QLabel("Rect  ")
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.x_input = QtGui.QLineEdit()
        self.x_label = QtGui.QLabel("X ")
        self.x_input.setStyleSheet("width: 5px;")
        self.y_input = QtGui.QLineEdit()
        self.y_label = QtGui.QLabel("Y ")
        self.y_input.setStyleSheet("width: 5px;")
        self.z_input = QtGui.QLineEdit()
        self.z_input.setStyleSheet("width: 5px;")
        self.z_label = QtGui.QLabel("Z")
        self.time_icon = QtGui.QPushButton(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/new.png"), None)
        self.time_icon.setEnabled(False)
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/trash.png"), None)

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

        self.setLayout(self.main_layout)
        self._fill_values(rect_motion)

    def _fill_values(self, rect_motion):
        self.x_input.setText(str(rect_motion.velocity[0]))
        self.y_input.setText(str(rect_motion.velocity[1]))
        self.z_input.setText(str(rect_motion.velocity[2]))
        self.time_input.setText(str(rect_motion.duration))


class WaitMotionTimeline(QtGui.QWidget):
    """ A wait motion grapihcal representation for a table-based timeline """

    def __init__(self, wait_motion):
        if not isinstance(wait_motion, WaitMotion):
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline with a wrong object")
        if wait_motion is None:
            raise TypeError("You tried to spawn a rectilinear motion widget in the timeline without a motion object")

        super(WaitMotionTimeline, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)

        self.label = QtGui.QLabel("Wait")
        self.time_icon = QtGui.QPushButton(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/new.png"), None)
        self.time_icon.setEnabled(False)
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/trash.png"), None)

        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_icon)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)

        self.setLayout(self.main_layout)
        self._fill_values(wait_motion)

    def _fill_values(self, wait_motion):
        self.time_input.setText(str(wait_motion.duration))
