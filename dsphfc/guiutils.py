#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""DesignSPHysics GUI Utils.

This module stores functionality useful for GUI
operations in DesignSPHysics.

"""

import FreeCAD
import FreeCADGui
import pickle
import sys
import os
import utils
import subprocess
from sys import platform
from PySide import QtGui, QtCore
"""
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DesignSPHysics.

DesignSPHysics is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DesignSPHysics is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.
"""


def h_line_generator():
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.HLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def v_line_generator():
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.VLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def warning_dialog(warn_text, detailed_text=None):
    """Spawns a warning dialog with the text passed."""

    warning_messagebox = QtGui.QMessageBox()
    warning_messagebox.setText(warn_text)
    warning_messagebox.setIcon(QtGui.QMessageBox.Warning)
    if detailed_text is not None:
        warning_messagebox.setDetailedText(str(detailed_text))
    warning_messagebox.exec_()


def error_dialog(error_text, detailed_text=None):
    """Spawns an error dialog with the text passed."""

    error_messagebox = QtGui.QMessageBox()
    error_messagebox.setText(error_text)
    error_messagebox.setIcon(QtGui.QMessageBox.Critical)
    if detailed_text is not None:
        error_messagebox.setDetailedText(str(detailed_text))
    error_messagebox.exec_()


def info_dialog(info_text, detailed_text=None):
    """Spawns an info dialog with the text passed."""

    info_messagebox = QtGui.QMessageBox()
    info_messagebox.setText(info_text)
    info_messagebox.setIcon(QtGui.QMessageBox.Information)
    if detailed_text is not None:
        info_messagebox.setDetailedText(str(detailed_text))
    info_messagebox.exec_()


def ok_cancel_dialog(title, text):
    """Spawns an okay/cancel dialog with the title and text passed"""

    open_confirm_dialog = QtGui.QMessageBox()
    open_confirm_dialog.setText(title)
    open_confirm_dialog.setInformativeText(text)
    open_confirm_dialog.setStandardButtons(QtGui.QMessageBox.Ok |
                                           QtGui.QMessageBox.Cancel)
    open_confirm_dialog.setDefaultButton(QtGui.QMessageBox.Ok)
    return open_confirm_dialog.exec_()


def get_icon(file_name):
    """ Returns a QIcon to use with DesignSPHysics.
    Retrieves a file with filename (like image.png) from the DSPH_Images folder. """
    file_to_load = os.path.dirname(
        os.path.abspath(__file__)) + "/../DSPH_Images/{}".format(file_name)
    if os.path.isfile(file_to_load):
        return QtGui.QIcon(file_to_load)
    else:
        raise IOError(
            "File {} not found in DSPH_Images folder".format(file_name))


def get_fc_main_window():
    return FreeCADGui.getMainWindow()


def def_constants_window(data):
    """Defines the constants window creation and functonality.
    Modifies the passed data dictionary to update data if ok is pressed."""

    # Creates a dialog and 2 main buttons
    constants_window = QtGui.QDialog()
    constants_window.setWindowTitle("DSPH Constant definition")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    # Lattice for boundaries layout and components
    lattice_layout = QtGui.QHBoxLayout()
    lattice_label = QtGui.QLabel("Lattice for Boundaries: ")
    lattice_input = QtGui.QComboBox()
    lattice_input.insertItems(0, ['Lattice 1', 'Lattice 2'])
    lattice_input.setCurrentIndex(int(data['lattice_bound']) - 1)

    lattice_layout.addWidget(lattice_label)
    lattice_layout.addWidget(lattice_input)
    lattice_layout.addStretch(1)

    # Lattice for fluids layout and components
    lattice2_layout = QtGui.QHBoxLayout()
    lattice2_label = QtGui.QLabel("Lattice for Fluids: ")
    lattice2_input = QtGui.QComboBox()
    lattice2_input.insertItems(0, ['Lattice 1', 'Lattice 2'])
    lattice2_input.setCurrentIndex(int(data['lattice_fluid']) - 1)

    lattice2_layout.addWidget(lattice2_label)
    lattice2_layout.addWidget(lattice2_input)
    lattice2_layout.addStretch(1)

    # Gravity
    gravity_layout = QtGui.QHBoxLayout()
    gravity_label = QtGui.QLabel("Gravity [X, Y, Z]: ")

    gravityx_input = QtGui.QLineEdit()
    gravityx_input.setMaxLength(10)
    gravityx_validator = QtGui.QDoubleValidator(-200, 200, 8, gravityx_input)
    gravityx_input.setText(str(data['gravity'][0]))
    gravityx_input.setValidator(gravityx_validator)

    gravityy_input = QtGui.QLineEdit()
    gravityy_input.setMaxLength(10)
    gravityy_validator = QtGui.QDoubleValidator(-200, 200, 8, gravityy_input)
    gravityy_input.setText(str(data['gravity'][1]))
    gravityy_input.setValidator(gravityy_validator)

    gravityz_input = QtGui.QLineEdit()
    gravityz_input.setMaxLength(10)
    gravityz_validator = QtGui.QDoubleValidator(-200, 200, 8, gravityz_input)
    gravityz_input.setText(str(data['gravity'][2]))
    gravityz_input.setValidator(gravityz_validator)

    gravity_label2 = QtGui.QLabel(
        "m/s<span style='vertical-align:super'>2</span>")

    gravity_layout.addWidget(gravity_label)
    gravity_layout.addWidget(gravityx_input)  # For X
    gravity_layout.addWidget(gravityy_input)  # For Y
    gravity_layout.addWidget(gravityz_input)  # For Z
    gravity_layout.addWidget(gravity_label2)

    # Reference density of the fluid: layout and components
    rhop0_layout = QtGui.QHBoxLayout()
    rhop0_label = QtGui.QLabel("Fluid reference density: ")
    rhop0_input = QtGui.QLineEdit()
    rhop0_input.setMaxLength(10)
    rhop0_validator = QtGui.QIntValidator(0, 10000, rhop0_input)
    rhop0_input.setText(str(data['rhop0']))
    rhop0_input.setValidator(rhop0_validator)
    rhop0_label2 = QtGui.QLabel(
        "kg/m<span style='vertical-align:super'>3<span>")

    rhop0_layout.addWidget(rhop0_label)
    rhop0_layout.addWidget(rhop0_input)
    rhop0_layout.addWidget(rhop0_label2)

    # Maximum still water lavel to calc.  spdofsound using coefsound: layout and
    # components
    hswlauto_layout = QtGui.QHBoxLayout()
    hswlauto_chk = QtGui.QCheckBox("Auto HSWL ")
    if data['hswl_auto']:
        hswlauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_hswlauto_check(
    ):  # Controls if user selected auto HSWL or not enabling/disablen HSWL custom
        # value introduction
        if hswlauto_chk.isChecked():
            hswl_input.setEnabled(False)
        else:
            hswl_input.setEnabled(True)

    hswlauto_chk.toggled.connect(on_hswlauto_check)
    hswlauto_layout.addWidget(hswlauto_chk)

    hswl_layout = QtGui.QHBoxLayout()
    hswl_label = QtGui.QLabel("HSWL: ")
    hswl_input = QtGui.QLineEdit()
    hswl_input.setMaxLength(10)
    hswl_validator = QtGui.QIntValidator(0, 10000, hswl_input)
    hswl_input.setText(str(data['hswl']))
    hswl_input.setValidator(hswl_validator)
    hswl_label2 = QtGui.QLabel("metres")

    hswl_layout.addWidget(hswl_label)
    hswl_layout.addWidget(hswl_input)
    hswl_layout.addWidget(hswl_label2)

    # Manually trigger check for the first time
    on_hswlauto_check()

    # gamma: layout and components
    gamma_layout = QtGui.QHBoxLayout()
    gamma_label = QtGui.QLabel("Gamma: ")
    gamma_input = QtGui.QLineEdit()
    gamma_input.setMaxLength(3)
    gamma_validator = QtGui.QIntValidator(0, 999, gamma_input)
    gamma_input.setText(str(data['gamma']))
    gamma_input.setValidator(gamma_validator)
    gamma_label2 = QtGui.QLabel("units")

    gamma_layout.addWidget(gamma_label)
    gamma_layout.addWidget(gamma_input)
    gamma_layout.addWidget(gamma_label2)

    # Speedsystem: layout and components
    speedsystemauto_layout = QtGui.QHBoxLayout()
    speedsystemauto_chk = QtGui.QCheckBox("Auto Speedsystem ")
    if data['speedsystem_auto']:
        speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_speedsystemauto_check(
    ):  # Controls if user selected auto speedsystem or not enabling/disablen
        # speedsystem custom value introduction
        if speedsystemauto_chk.isChecked():
            speedsystem_input.setEnabled(False)
        else:
            speedsystem_input.setEnabled(True)

    speedsystemauto_chk.toggled.connect(on_speedsystemauto_check)
    speedsystemauto_layout.addWidget(speedsystemauto_chk)

    speedsystem_layout = QtGui.QHBoxLayout()
    speedsystem_label = QtGui.QLabel("Speedsystem: ")
    speedsystem_input = QtGui.QLineEdit()
    speedsystem_input.setMaxLength(10)
    speedsystem_validator = QtGui.QIntValidator(0, 10000, speedsystem_input)
    speedsystem_input.setText(str(data['speedsystem']))
    speedsystem_input.setValidator(speedsystem_validator)
    speedsystem_label2 = QtGui.QLabel("m/s")

    speedsystem_layout.addWidget(speedsystem_label)
    speedsystem_layout.addWidget(speedsystem_input)
    speedsystem_layout.addWidget(speedsystem_label2)

    # Manually trigger check for the first time
    on_speedsystemauto_check()

    # coefsound: layout and components
    coefsound_layout = QtGui.QHBoxLayout()
    coefsound_label = QtGui.QLabel("Coefsound: ")
    coefsound_input = QtGui.QLineEdit()
    coefsound_input.setMaxLength(3)
    coefsound_validator = QtGui.QIntValidator(0, 999, coefsound_input)
    coefsound_input.setText(str(data['coefsound']))
    coefsound_input.setValidator(coefsound_validator)
    coefsound_label2 = QtGui.QLabel("units")

    coefsound_layout.addWidget(coefsound_label)
    coefsound_layout.addWidget(coefsound_input)
    coefsound_layout.addWidget(coefsound_label2)

    # Speedsound: layout and components
    speedsoundauto_layout = QtGui.QHBoxLayout()
    speedsoundauto_chk = QtGui.QCheckBox("Auto Speedsound ")
    if data['speedsound_auto']:
        speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_speedsoundauto_check(
    ):  # Controls if user selected auto speedsound or not enabling/disablen speedsound
        # custom value introduction
        if speedsoundauto_chk.isChecked():
            speedsound_input.setEnabled(False)
        else:
            speedsound_input.setEnabled(True)

    speedsoundauto_chk.toggled.connect(on_speedsoundauto_check)
    speedsoundauto_layout.addWidget(speedsoundauto_chk)

    speedsound_layout = QtGui.QHBoxLayout()
    speedsound_label = QtGui.QLabel("Speedsound: ")
    speedsound_input = QtGui.QLineEdit()
    speedsound_input.setMaxLength(10)
    speedsound_validator = QtGui.QIntValidator(0, 10000, speedsound_input)
    speedsound_input.setText(str(data['speedsound']))
    speedsound_input.setValidator(speedsound_validator)
    speedsound_label2 = QtGui.QLabel("m/s")

    speedsound_layout.addWidget(speedsound_label)
    speedsound_layout.addWidget(speedsound_input)
    speedsound_layout.addWidget(speedsound_label2)

    # Manually trigger check for the first time
    on_speedsoundauto_check()

    # coefh: layout and components
    coefh_layout = QtGui.QHBoxLayout()
    coefh_label = QtGui.QLabel("CoefH: ")
    coefh_input = QtGui.QLineEdit()
    coefh_input.setMaxLength(10)
    coefh_validator = QtGui.QDoubleValidator(0, 10, 8, coefh_input)
    coefh_input.setText(str(data['coefh']))
    coefh_input.setValidator(coefh_validator)
    coefh_label2 = QtGui.QLabel("units")

    coefh_layout.addWidget(coefh_label)
    coefh_layout.addWidget(coefh_input)
    coefh_layout.addWidget(coefh_label2)

    # cflnumber: layout and components
    cflnumber_layout = QtGui.QHBoxLayout()
    cflnumber_label = QtGui.QLabel("cflnumber: ")
    cflnumber_input = QtGui.QLineEdit()
    cflnumber_input.setMaxLength(10)
    cflnumber_validator = QtGui.QDoubleValidator(0, 10, 8, coefh_input)
    cflnumber_input.setText(str(data['cflnumber']))
    cflnumber_input.setValidator(cflnumber_validator)
    cflnumber_label2 = QtGui.QLabel("units")

    cflnumber_layout.addWidget(cflnumber_label)
    cflnumber_layout.addWidget(cflnumber_input)
    cflnumber_layout.addWidget(cflnumber_label2)

    # h: layout and components
    hauto_layout = QtGui.QHBoxLayout()
    hauto_chk = QtGui.QCheckBox("Auto Smoothing length ")
    if data['h_auto']:
        hauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        hauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_hauto_check(
    ):  # Controls if user selected auto h or not enabling/disablen h custom value
        # introduction
        if hauto_chk.isChecked():
            h_input.setEnabled(False)
        else:
            h_input.setEnabled(True)

    hauto_chk.toggled.connect(on_hauto_check)
    hauto_layout.addWidget(hauto_chk)

    h_layout = QtGui.QHBoxLayout()
    h_label = QtGui.QLabel("Smoothing Length: ")
    h_input = QtGui.QLineEdit()
    h_input.setMaxLength(10)
    h_validator = QtGui.QDoubleValidator(0, 100, 8, h_input)
    h_input.setText(str(data['h']))
    h_input.setValidator(h_validator)
    h_label2 = QtGui.QLabel("metres")

    h_layout.addWidget(h_label)
    h_layout.addWidget(h_input)
    h_layout.addWidget(h_label2)

    # Manually trigger check for the first time
    on_hauto_check()

    # b: layout and components
    bauto_layout = QtGui.QHBoxLayout()
    bauto_chk = QtGui.QCheckBox("Auto b constant for EOS ")
    if data['b_auto']:
        bauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        bauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_bauto_check(
    ):  # Controls if user selected auto b or not enabling/disablen b custom value
        # introduction
        if bauto_chk.isChecked():
            b_input.setEnabled(False)
        else:
            b_input.setEnabled(True)

    bauto_chk.toggled.connect(on_bauto_check)
    bauto_layout.addWidget(bauto_chk)

    b_layout = QtGui.QHBoxLayout()
    b_label = QtGui.QLabel("B constant: ")
    b_input = QtGui.QLineEdit()
    b_input.setMaxLength(10)
    b_validator = QtGui.QDoubleValidator(0, 100, 8, b_input)
    b_input.setText(str(data['b']))
    b_input.setValidator(b_validator)
    b_label2 = QtGui.QLabel("")

    b_layout.addWidget(b_label)
    b_layout.addWidget(b_input)
    b_layout.addWidget(b_label2)

    # Manually trigger check for the first time
    on_bauto_check()

    # ------------ Button behaviour definition --------------
    def on_ok():
        data['lattice_bound'] = str(lattice_input.currentIndex() + 1)
        data['lattice_fluid'] = str(lattice2_input.currentIndex() + 1)
        data['gravity'] = [
            gravityx_input.text(),
            gravityy_input.text(),
            gravityz_input.text()
        ]
        data['rhop0'] = rhop0_input.text()
        data['hswl'] = hswl_input.text()
        data['hswl_auto'] = hswlauto_chk.isChecked()
        data['gamma'] = gamma_input.text()
        data['speedsystem'] = speedsystem_input.text()
        data['speedsystem_auto'] = speedsystemauto_chk.isChecked()
        data['coefsound'] = coefsound_input.text()
        data['speedsound'] = speedsound_input.text()
        data['speedsound_auto'] = speedsoundauto_chk.isChecked()
        data['coefh'] = coefh_input.text()
        data['cflnumber'] = cflnumber_input.text()
        data['h'] = h_input.text()
        data['h_auto'] = hauto_chk.isChecked()
        data['b'] = b_input.text()
        data['b_auto'] = bauto_chk.isChecked()
        utils.log("Constants changed")
        constants_window.accept()

    def on_cancel():
        utils.log("Constants not changed")
        constants_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    # Button layout definition
    cw_button_layout = QtGui.QHBoxLayout()
    cw_button_layout.addStretch(1)
    cw_button_layout.addWidget(ok_button)
    cw_button_layout.addWidget(cancel_button)

    # START Main layout definition and composition.
    cw_main_layout = QtGui.QVBoxLayout()

    # Lattice was removed on 0.3Beta - 1 of June
    # cw_main_layout.addLayout(lattice_layout)
    # cw_main_layout.addLayout(lattice2_layout)
    cw_main_layout.addLayout(gravity_layout)
    cw_main_layout.addLayout(rhop0_layout)
    cw_main_layout.addLayout(hswlauto_layout)
    cw_main_layout.addLayout(hswl_layout)
    cw_main_layout.addLayout(gamma_layout)
    cw_main_layout.addLayout(speedsystemauto_layout)
    cw_main_layout.addLayout(speedsystem_layout)
    cw_main_layout.addLayout(coefsound_layout)
    cw_main_layout.addLayout(speedsoundauto_layout)
    cw_main_layout.addLayout(speedsound_layout)
    cw_main_layout.addLayout(coefh_layout)
    cw_main_layout.addLayout(cflnumber_layout)
    cw_main_layout.addLayout(hauto_layout)
    cw_main_layout.addLayout(h_layout)
    cw_main_layout.addLayout(bauto_layout)
    cw_main_layout.addLayout(b_layout)

    cw_main_layout.addStretch(1)

    cw_groupbox = QtGui.QGroupBox("Case constants")
    cw_groupbox.setLayout(cw_main_layout)
    constants_window_layout = QtGui.QVBoxLayout()
    constants_window_layout.addWidget(cw_groupbox)
    constants_window_layout.addLayout(cw_button_layout)
    constants_window.setLayout(constants_window_layout)
    # END Main layout definition and composition.

    # Constant definition window behaviour and general composing
    constants_window.resize(600, 400)
    constants_window.exec_()


def def_execparams_window(data):
    """Defines the execution parameters window.
    Modifies the data dictionary passed as parameter."""

    # Creates a dialog and 2 main buttons
    execparams_window = QtGui.QDialog()
    execparams_window.setWindowTitle("DSPH Execution Parameters")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    # Precision in particle interaction
    posdouble_layout = QtGui.QHBoxLayout()
    posdouble_label = QtGui.QLabel("Precision in particle interaction: ")
    posdouble_input = QtGui.QComboBox()
    posdouble_input.insertItems(0,
                                ['Simple', 'Double', 'Uses and saves double'])
    posdouble_input.setCurrentIndex(int(data['posdouble']))

    posdouble_layout.addWidget(posdouble_label)
    posdouble_layout.addWidget(posdouble_input)
    posdouble_layout.addStretch(1)

    # Step Algorithm
    def on_step_change(index):
        if index == 0:
            verletsteps_input.setEnabled(True)
        else:
            verletsteps_input.setEnabled(False)

    stepalgorithm_layout = QtGui.QHBoxLayout()
    stepalgorithm_label = QtGui.QLabel("Step Algorithm: ")
    stepalgorithm_input = QtGui.QComboBox()
    stepalgorithm_input.insertItems(0, ['Verlet', 'Symplectic'])
    stepalgorithm_input.setCurrentIndex(int(data['stepalgorithm']) - 1)
    stepalgorithm_input.currentIndexChanged.connect(on_step_change)

    stepalgorithm_layout.addWidget(stepalgorithm_label)
    stepalgorithm_layout.addWidget(stepalgorithm_input)
    stepalgorithm_layout.addStretch(1)

    # Verlet steps
    verletsteps_layout = QtGui.QHBoxLayout()
    verletsteps_label = QtGui.QLabel("Verlet Steps: ")
    verletsteps_input = QtGui.QLineEdit()
    verletsteps_input.setMaxLength(4)
    verletsteps_validator = QtGui.QIntValidator(0, 9999, verletsteps_input)
    verletsteps_input.setText(str(data['verletsteps']))
    verletsteps_input.setValidator(verletsteps_validator)

    # Enable/Disable fields depending on selection
    on_step_change(stepalgorithm_input.currentIndex())

    verletsteps_layout.addWidget(verletsteps_label)
    verletsteps_layout.addWidget(verletsteps_input)

    # Kernel
    kernel_layout = QtGui.QHBoxLayout()
    kernel_label = QtGui.QLabel("Interaction kernel: ")
    kernel_input = QtGui.QComboBox()
    kernel_input.insertItems(0, ['Cubic spline', 'Wendland'])
    kernel_input.setCurrentIndex(int(data['kernel']) - 1)

    kernel_layout.addWidget(kernel_label)
    kernel_layout.addWidget(kernel_input)
    kernel_layout.addStretch(1)

    # Viscosity formulation
    viscotreatment_layout = QtGui.QHBoxLayout()
    viscotreatment_label = QtGui.QLabel("Viscosity Formulation: ")
    viscotreatment_input = QtGui.QComboBox()
    viscotreatment_input.insertItems(0, ['Artificial', 'Laminar + SPS'])
    viscotreatment_input.setCurrentIndex(int(data['viscotreatment']) - 1)

    viscotreatment_layout.addWidget(viscotreatment_label)
    viscotreatment_layout.addWidget(viscotreatment_input)
    viscotreatment_layout.addStretch(1)

    # Viscosity value
    visco_layout = QtGui.QHBoxLayout()
    visco_label = QtGui.QLabel("Viscosity value: ")
    visco_input = QtGui.QLineEdit()
    visco_input.setMaxLength(10)
    visco_units_label = QtGui.QLabel("")
    visco_layout.addWidget(visco_label)
    visco_layout.addWidget(visco_input)
    visco_layout.addWidget(visco_units_label)

    def on_viscotreatment_change(index):
        visco_input.setText("0.01" if index == 0 else "0.000001")
        visco_label.setText("Viscosity value (alpha): "
                            if index == 0 else "Kinematic viscosity: ")
        visco_units_label.setText(
            "" if index == 0 else
            "m<span style='vertical-align:super'>2</span>/s")

    on_viscotreatment_change(int(data['viscotreatment']) - 1)
    visco_input.setText(str(data['visco']))

    viscotreatment_input.currentIndexChanged.connect(on_viscotreatment_change)

    # Viscosity with boundary
    viscoboundfactor_layout = QtGui.QHBoxLayout()
    viscoboundfactor_label = QtGui.QLabel("Viscosity factor with boundary: ")
    viscoboundfactor_input = QtGui.QLineEdit()
    viscoboundfactor_input.setMaxLength(10)
    viscoboundfactor_input.setText(str(data['viscoboundfactor']))

    viscoboundfactor_layout.addWidget(viscoboundfactor_label)
    viscoboundfactor_layout.addWidget(viscoboundfactor_input)

    # DeltaSPH enabled selector
    def on_deltasph_en_change(index):
        if index == 0:
            deltasph_input.setEnabled(False)
        else:
            deltasph_input.setEnabled(True)
            deltasph_input.setText("0.1")

    deltasph_en_layout = QtGui.QHBoxLayout()
    deltasph_en_label = QtGui.QLabel("Enable DeltaSPH: ")
    deltasph_en_input = QtGui.QComboBox()
    deltasph_en_input.insertItems(0, ['No', 'Yes'])
    deltasph_en_input.setCurrentIndex(int(data['deltasph_en']))
    deltasph_en_input.currentIndexChanged.connect(on_deltasph_en_change)

    deltasph_en_layout.addWidget(deltasph_en_label)
    deltasph_en_layout.addWidget(deltasph_en_input)
    deltasph_en_layout.addStretch(1)

    # DeltaSPH value
    deltasph_layout = QtGui.QHBoxLayout()
    deltasph_label = QtGui.QLabel("DeltaSPH value: ")
    deltasph_input = QtGui.QLineEdit()
    deltasph_input.setMaxLength(10)
    deltasph_input.setText(str(data['deltasph']))
    deltasph_layout.addWidget(deltasph_label)
    deltasph_layout.addWidget(deltasph_input)

    if deltasph_en_input.currentIndex() == 0:
        deltasph_input.setEnabled(False)
    else:
        deltasph_input.setEnabled(True)

    # Shifting mode
    def on_shifting_change(index):
        if index == 0:
            shiftcoef_input.setEnabled(False)
            shifttfs_input.setEnabled(False)
        else:
            shiftcoef_input.setEnabled(True)
            shifttfs_input.setEnabled(True)

    shifting_layout = QtGui.QHBoxLayout()
    shifting_label = QtGui.QLabel("Shifting mode: ")
    shifting_input = QtGui.QComboBox()
    shifting_input.insertItems(
        0, ['None', 'Ignore bound', 'Ignore fixed', 'Full'])
    shifting_input.setCurrentIndex(int(data['shifting']))
    shifting_input.currentIndexChanged.connect(on_shifting_change)

    shifting_layout.addWidget(shifting_label)
    shifting_layout.addWidget(shifting_input)
    shifting_layout.addStretch(1)

    # Coefficient for shifting
    shiftcoef_layout = QtGui.QHBoxLayout()
    shiftcoef_label = QtGui.QLabel("Coefficient for shifting: ")
    shiftcoef_input = QtGui.QLineEdit()
    shiftcoef_input.setMaxLength(10)
    shiftcoef_input.setText(str(data['shiftcoef']))
    shiftcoef_layout.addWidget(shiftcoef_label)
    shiftcoef_layout.addWidget(shiftcoef_input)

    # Free surface detection threshold
    shifttfs_layout = QtGui.QHBoxLayout()
    shifttfs_label = QtGui.QLabel("Free surface detection threshold: ")
    shifttfs_input = QtGui.QLineEdit()
    shifttfs_input.setMaxLength(10)
    shifttfs_input.setText(str(data['shifttfs']))
    shifttfs_layout.addWidget(shifttfs_label)
    shifttfs_layout.addWidget(shifttfs_input)

    # Enable/Disable fields depending on Shifting mode on window creation.
    on_shifting_change(shifting_input.currentIndex())

    # Rigid algorithm
    rigidalgorithm_layout = QtGui.QHBoxLayout()
    rigidalgorithm_label = QtGui.QLabel("Solid-solid interaction: ")
    rigidalgorithm_input = QtGui.QComboBox()
    rigidalgorithm_input.insertItems(0, ['SPH', 'DEM'])
    rigidalgorithm_input.setCurrentIndex(int(data['rigidalgorithm']) - 1)

    rigidalgorithm_layout.addWidget(rigidalgorithm_label)
    rigidalgorithm_layout.addWidget(rigidalgorithm_input)
    rigidalgorithm_layout.addStretch(1)

    # Sim start freeze time
    ftpause_layout = QtGui.QHBoxLayout()
    ftpause_label = QtGui.QLabel("Floating freeze time: ")
    ftpause_input = QtGui.QLineEdit()
    ftpause_input.setMaxLength(10)
    ftpause_input.setText(str(data['ftpause']))
    ftpause_label2 = QtGui.QLabel("seconds")
    ftpause_layout.addWidget(ftpause_label)
    ftpause_layout.addWidget(ftpause_input)
    ftpause_layout.addWidget(ftpause_label2)

    # Coefficient to calculate DT
    coefdtmin_layout = QtGui.QHBoxLayout()
    coefdtmin_label = QtGui.QLabel("Coefficient for minimum time step: ")
    coefdtmin_input = QtGui.QLineEdit()
    coefdtmin_input.setMaxLength(10)
    coefdtmin_input.setText(str(data['coefdtmin']))
    coefdtmin_layout.addWidget(coefdtmin_label)
    coefdtmin_layout.addWidget(coefdtmin_input)

    # Initial time step
    dtiniauto_layout = QtGui.QHBoxLayout()
    dtiniauto_chk = QtGui.QCheckBox("Initial time step auto")
    if data['dtini_auto']:
        dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_dtiniauto_check(
    ):  # Controls if user selected auto b or not enabling/disablen b custom value
        # introduction
        if dtiniauto_chk.isChecked():
            dtini_input.setEnabled(False)
        else:
            dtini_input.setEnabled(True)

    dtiniauto_chk.toggled.connect(on_dtiniauto_check)
    dtiniauto_layout.addWidget(dtiniauto_chk)
    dtini_layout = QtGui.QHBoxLayout()
    dtini_label = QtGui.QLabel("Initial time step: ")
    dtini_input = QtGui.QLineEdit()
    dtini_input.setMaxLength(10)
    dtini_input.setText(str(data['dtini']))
    dtini_label2 = QtGui.QLabel("seconds")
    dtini_layout.addWidget(dtini_label)
    dtini_layout.addWidget(dtini_input)
    dtini_layout.addWidget(dtini_label2)
    on_dtiniauto_check()

    # Minimium time step
    dtminauto_layout = QtGui.QHBoxLayout()
    dtminauto_chk = QtGui.QCheckBox("Minimum time step: ")
    if data['dtmin_auto']:
        dtminauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_dtminauto_check(
    ):  # Controls if user selected auto b or not enabling/disablen b custom value
        # introduction
        if dtminauto_chk.isChecked():
            dtmin_input.setEnabled(False)
        else:
            dtmin_input.setEnabled(True)

    dtminauto_chk.toggled.connect(on_dtminauto_check)
    dtminauto_layout.addWidget(dtminauto_chk)
    dtmin_layout = QtGui.QHBoxLayout()
    dtmin_label = QtGui.QLabel("Minimium time step: ")
    dtmin_input = QtGui.QLineEdit()
    dtmin_input.setMaxLength(10)
    dtmin_input.setText(str(data['dtmin']))
    dtmin_label2 = QtGui.QLabel("seconds")
    dtmin_layout.addWidget(dtmin_label)
    dtmin_layout.addWidget(dtmin_input)
    dtmin_layout.addWidget(dtmin_label2)
    on_dtminauto_check()

    # Fixed DT file
    dtfixed_layout = QtGui.QHBoxLayout()
    dtfixed_label = QtGui.QLabel("Fixed DT file: ")
    dtfixed_input = QtGui.QLineEdit()
    dtfixed_input.setText(str(data['dtfixed']))
    dtfixed_label2 = QtGui.QLabel("file")
    dtfixed_layout.addWidget(dtfixed_label)
    dtfixed_layout.addWidget(dtfixed_input)
    dtfixed_layout.addWidget(dtfixed_label2)

    # Velocity of particles
    dtallparticles_layout = QtGui.QHBoxLayout()
    dtallparticles_label = QtGui.QLabel("Velocity of particles: ")
    dtallparticles_input = QtGui.QLineEdit()
    dtallparticles_input.setMaxLength(1)
    dtallparticles_validator = QtGui.QIntValidator(0, 1, dtallparticles_input)
    dtallparticles_input.setText(str(data['dtallparticles']))
    dtallparticles_input.setValidator(dtallparticles_validator)
    dtallparticles_label2 = QtGui.QLabel("[0,1]")
    dtallparticles_layout.addWidget(dtallparticles_label)
    dtallparticles_layout.addWidget(dtallparticles_input)
    dtallparticles_layout.addWidget(dtallparticles_label2)

    # Time of simulation
    timemax_layout = QtGui.QHBoxLayout()
    timemax_label = QtGui.QLabel("Time of simulation: ")
    timemax_input = QtGui.QLineEdit()
    timemax_input.setMaxLength(10)
    timemax_input.setText(str(data['timemax']))
    timemax_label2 = QtGui.QLabel("seconds")
    timemax_layout.addWidget(timemax_label)
    timemax_layout.addWidget(timemax_input)
    timemax_layout.addWidget(timemax_label2)

    # Time out data
    timeout_layout = QtGui.QHBoxLayout()
    timeout_label = QtGui.QLabel("Time out data: ")
    timeout_input = QtGui.QLineEdit()
    timeout_input.setMaxLength(10)
    timeout_input.setText(str(data['timeout']))
    timeout_label2 = QtGui.QLabel("seconds")
    timeout_layout.addWidget(timeout_label)
    timeout_layout.addWidget(timeout_input)
    timeout_layout.addWidget(timeout_label2)

    # Increase of Z+
    incz_layout = QtGui.QHBoxLayout()
    incz_label = QtGui.QLabel("Increase of Z+ (%): ")
    incz_input = QtGui.QLineEdit()
    incz_input.setMaxLength(10)
    incz_input.setText(str(float(data['incz']) * 100))
    incz_layout.addWidget(incz_label)
    incz_layout.addWidget(incz_input)

    # Max parts out allowed
    partsoutmax_layout = QtGui.QHBoxLayout()
    partsoutmax_label = QtGui.QLabel("Max parts out allowed (%): ")
    partsoutmax_input = QtGui.QLineEdit()
    partsoutmax_input.setMaxLength(10)
    partsoutmax_input.setText(str(float(data['partsoutmax']) * 100))
    partsoutmax_layout.addWidget(partsoutmax_label)
    partsoutmax_layout.addWidget(partsoutmax_input)

    # Minimum rhop valid
    rhopoutmin_layout = QtGui.QHBoxLayout()
    rhopoutmin_label = QtGui.QLabel("Minimum rhop valid: ")
    rhopoutmin_input = QtGui.QLineEdit()
    rhopoutmin_input.setMaxLength(10)
    rhopoutmin_input.setText(str(data['rhopoutmin']))
    rhopoutmin_label2 = QtGui.QLabel(
        "kg/m<span style='vertical-align:super'>3</span>")
    rhopoutmin_layout.addWidget(rhopoutmin_label)
    rhopoutmin_layout.addWidget(rhopoutmin_input)
    rhopoutmin_layout.addWidget(rhopoutmin_label2)

    # Maximum rhop valid
    rhopoutmax_layout = QtGui.QHBoxLayout()
    rhopoutmax_label = QtGui.QLabel("Maximum rhop valid: ")
    rhopoutmax_input = QtGui.QLineEdit()
    rhopoutmax_input.setMaxLength(10)
    rhopoutmax_input.setText(str(data['rhopoutmax']))
    rhopoutmax_label2 = QtGui.QLabel(
        "kg/m<span style='vertical-align:super'>3</span>")
    rhopoutmax_layout.addWidget(rhopoutmax_label)
    rhopoutmax_layout.addWidget(rhopoutmax_input)
    rhopoutmax_layout.addWidget(rhopoutmax_label2)

    # Periodicity in X
    def on_period_x_chk():
        if period_x_chk.isChecked():
            period_x_inc_x_input.setEnabled(False)
            period_x_inc_y_input.setEnabled(True)
            period_x_inc_z_input.setEnabled(True)
        else:
            period_x_inc_x_input.setEnabled(False)
            period_x_inc_y_input.setEnabled(False)
            period_x_inc_z_input.setEnabled(False)

    period_x_layout = QtGui.QVBoxLayout()
    period_x_chk = QtGui.QCheckBox("X periodicity")
    period_x_inc_layout = QtGui.QHBoxLayout()
    period_x_inc_x_label = QtGui.QLabel("X Increment")
    period_x_inc_x_input = QtGui.QLineEdit("0")
    period_x_inc_y_label = QtGui.QLabel("Y Increment")
    period_x_inc_y_input = QtGui.QLineEdit("0")
    period_x_inc_z_label = QtGui.QLabel("Z Increment")
    period_x_inc_z_input = QtGui.QLineEdit("0")
    period_x_inc_layout.addWidget(period_x_inc_x_label)
    period_x_inc_layout.addWidget(period_x_inc_x_input)
    period_x_inc_layout.addWidget(period_x_inc_y_label)
    period_x_inc_layout.addWidget(period_x_inc_y_input)
    period_x_inc_layout.addWidget(period_x_inc_z_label)
    period_x_inc_layout.addWidget(period_x_inc_z_input)
    period_x_layout.addWidget(period_x_chk)
    period_x_layout.addLayout(period_x_inc_layout)
    period_x_chk.stateChanged.connect(on_period_x_chk)

    try:
        period_x_chk.setChecked(data["period_x"][0])
        period_x_inc_x_input.setText(str(data["period_x"][1]))
        period_x_inc_y_input.setText(str(data["period_x"][2]))
        period_x_inc_z_input.setText(str(data["period_x"][3]))
    except:
        pass

    # Change the state of periodicity input on window open
    on_period_x_chk()

    # Periodicity in Y
    def on_period_y_chk():
        if period_y_chk.isChecked():
            period_y_inc_x_input.setEnabled(True)
            period_y_inc_y_input.setEnabled(False)
            period_y_inc_z_input.setEnabled(True)
        else:
            period_y_inc_x_input.setEnabled(False)
            period_y_inc_y_input.setEnabled(False)
            period_y_inc_z_input.setEnabled(False)

    period_y_layout = QtGui.QVBoxLayout()
    period_y_chk = QtGui.QCheckBox("Y periodicity")
    period_y_inc_layout = QtGui.QHBoxLayout()
    period_y_inc_x_label = QtGui.QLabel("X Increment")
    period_y_inc_x_input = QtGui.QLineEdit("0")
    period_y_inc_y_label = QtGui.QLabel("Y Increment")
    period_y_inc_y_input = QtGui.QLineEdit("0")
    period_y_inc_z_label = QtGui.QLabel("Z Increment")
    period_y_inc_z_input = QtGui.QLineEdit("0")
    period_y_inc_layout.addWidget(period_y_inc_x_label)
    period_y_inc_layout.addWidget(period_y_inc_x_input)
    period_y_inc_layout.addWidget(period_y_inc_y_label)
    period_y_inc_layout.addWidget(period_y_inc_y_input)
    period_y_inc_layout.addWidget(period_y_inc_z_label)
    period_y_inc_layout.addWidget(period_y_inc_z_input)
    period_y_layout.addWidget(period_y_chk)
    period_y_layout.addLayout(period_y_inc_layout)
    period_y_chk.stateChanged.connect(on_period_y_chk)

    try:
        period_y_chk.setChecked(data["period_y"][0])
        period_y_inc_x_input.setText(str(data["period_y"][1]))
        period_y_inc_y_input.setText(str(data["period_y"][2]))
        period_y_inc_z_input.setText(str(data["period_y"][3]))
    except:
        pass

    # Change the state of periodicity input on window open
    on_period_y_chk()

    # Periodicity in X
    def on_period_z_chk():
        if period_z_chk.isChecked():
            period_z_inc_x_input.setEnabled(True)
            period_z_inc_y_input.setEnabled(True)
            period_z_inc_z_input.setEnabled(False)
        else:
            period_z_inc_x_input.setEnabled(False)
            period_z_inc_y_input.setEnabled(False)
            period_z_inc_z_input.setEnabled(False)

    period_z_layout = QtGui.QVBoxLayout()
    period_z_chk = QtGui.QCheckBox("Z periodicity")
    period_z_inc_layout = QtGui.QHBoxLayout()
    period_z_inc_x_label = QtGui.QLabel("X Increment")
    period_z_inc_x_input = QtGui.QLineEdit("0")
    period_z_inc_y_label = QtGui.QLabel("Y Increment")
    period_z_inc_y_input = QtGui.QLineEdit("0")
    period_z_inc_z_label = QtGui.QLabel("Z Increment")
    period_z_inc_z_input = QtGui.QLineEdit("0")
    period_z_inc_layout.addWidget(period_z_inc_x_label)
    period_z_inc_layout.addWidget(period_z_inc_x_input)
    period_z_inc_layout.addWidget(period_z_inc_y_label)
    period_z_inc_layout.addWidget(period_z_inc_y_input)
    period_z_inc_layout.addWidget(period_z_inc_z_label)
    period_z_inc_layout.addWidget(period_z_inc_z_input)
    period_z_layout.addWidget(period_z_chk)
    period_z_layout.addLayout(period_z_inc_layout)
    period_z_chk.stateChanged.connect(on_period_z_chk)

    try:
        period_z_chk.setChecked(data["period_z"][0])
        period_z_inc_x_input.setText(str(data["period_z"][1]))
        period_z_inc_y_input.setText(str(data["period_z"][2]))
        period_z_inc_z_input.setText(str(data["period_z"][3]))
    except:
        pass

    # Change the state of periodicity input on window open
    on_period_z_chk()

    # ------------ Button behaviour definition --------------
    def on_ok():
        data['posdouble'] = str(posdouble_input.currentIndex())
        data['stepalgorithm'] = str(stepalgorithm_input.currentIndex() + 1)
        data['verletsteps'] = verletsteps_input.text()
        data['kernel'] = str(kernel_input.currentIndex() + 1)
        data['viscotreatment'] = viscotreatment_input.currentIndex() + 1
        data['visco'] = visco_input.text()
        data['viscoboundfactor'] = viscoboundfactor_input.text()
        data['deltasph'] = deltasph_input.text()
        data['deltasph_en'] = deltasph_en_input.currentIndex()
        data['shifting'] = str(shifting_input.currentIndex())
        data['shiftcoef'] = shiftcoef_input.text()
        data['shifttfs'] = shifttfs_input.text()
        data['rigidalgorithm'] = str(rigidalgorithm_input.currentIndex() + 1)
        data['ftpause'] = ftpause_input.text()
        data['coefdtmin'] = coefdtmin_input.text()
        data['dtini'] = dtini_input.text()
        data['dtini_auto'] = dtiniauto_chk.isChecked()
        data['dtmin'] = dtmin_input.text()
        data['dtmin_auto'] = dtminauto_chk.isChecked()
        data['dtfixed'] = dtfixed_input.text()
        data['dtallparticles'] = dtallparticles_input.text()
        data['timemax'] = timemax_input.text()
        data['timeout'] = timeout_input.text()
        data['incz'] = str(float(incz_input.text()) / 100)
        data['partsoutmax'] = str(float(partsoutmax_input.text()) / 100)
        data['rhopoutmin'] = rhopoutmin_input.text()
        data['rhopoutmax'] = rhopoutmax_input.text()
        data['period_x'] = [
            period_x_chk.isChecked(),
            float(period_x_inc_x_input.text()),
            float(period_x_inc_y_input.text()),
            float(period_x_inc_z_input.text())
        ]
        data['period_y'] = [
            period_y_chk.isChecked(),
            float(period_y_inc_x_input.text()),
            float(period_y_inc_y_input.text()),
            float(period_y_inc_z_input.text())
        ]
        data['period_z'] = [
            period_z_chk.isChecked(),
            float(period_z_inc_x_input.text()),
            float(period_z_inc_y_input.text()),
            float(period_z_inc_z_input.text())
        ]
        utils.log("Execution Parameters changed")
        execparams_window.accept()

    def on_cancel():
        utils.log("Execution Parameters not changed")
        execparams_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    # Button layout definition
    ep_button_layout = QtGui.QHBoxLayout()
    ep_button_layout.addStretch(1)
    ep_button_layout.addWidget(ok_button)
    ep_button_layout.addWidget(cancel_button)

    # START Main layout definition and composition.
    ep_main_layout_scroll = QtGui.QScrollArea()
    ep_main_layout_scroll_widget = QtGui.QWidget()
    ep_main_layout = QtGui.QVBoxLayout()
    ep_main_layout.addLayout(posdouble_layout)
    ep_main_layout.addLayout(stepalgorithm_layout)
    ep_main_layout.addLayout(verletsteps_layout)
    ep_main_layout.addLayout(kernel_layout)
    ep_main_layout.addLayout(viscotreatment_layout)
    ep_main_layout.addLayout(visco_layout)
    ep_main_layout.addLayout(viscoboundfactor_layout)
    ep_main_layout.addLayout(deltasph_en_layout)
    ep_main_layout.addLayout(deltasph_layout)
    ep_main_layout.addLayout(shifting_layout)
    ep_main_layout.addLayout(shiftcoef_layout)
    ep_main_layout.addLayout(shifttfs_layout)
    ep_main_layout.addLayout(rigidalgorithm_layout)
    ep_main_layout.addLayout(ftpause_layout)
    ep_main_layout.addLayout(dtiniauto_layout)
    ep_main_layout.addLayout(dtini_layout)
    ep_main_layout.addLayout(dtminauto_layout)
    ep_main_layout.addLayout(dtmin_layout)
    ep_main_layout.addLayout(coefdtmin_layout)
    # ep_main_layout.addLayout(dtallparticles_layout)
    ep_main_layout.addLayout(timemax_layout)
    ep_main_layout.addLayout(timeout_layout)
    ep_main_layout.addLayout(incz_layout)
    ep_main_layout.addLayout(partsoutmax_layout)
    ep_main_layout.addLayout(rhopoutmin_layout)
    ep_main_layout.addLayout(rhopoutmax_layout)
    ep_main_layout.addLayout(period_x_layout)
    ep_main_layout.addLayout(period_y_layout)
    ep_main_layout.addLayout(period_z_layout)

    ep_main_layout_scroll_widget.setLayout(ep_main_layout)
    ep_main_layout_scroll.setWidget(ep_main_layout_scroll_widget)
    ep_main_layout_scroll.setHorizontalScrollBarPolicy(
        QtCore.Qt.ScrollBarAlwaysOff)

    execparams_window_layout = QtGui.QVBoxLayout()
    execparams_window_layout.addWidget(ep_main_layout_scroll)
    execparams_window_layout.addLayout(ep_button_layout)
    execparams_window.setLayout(execparams_window_layout)
    # END Main layout definition and composition.

    execparams_window.resize(800, 600)
    execparams_window.exec_()


def def_setup_window(data):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    # Creates a dialog and 2 main buttons
    setup_window = QtGui.QDialog()
    setup_window.setWindowTitle("DSPH Setup")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    # GenCase path
    gencasepath_layout = QtGui.QHBoxLayout()
    gencasepath_label = QtGui.QLabel("GenCase Path: ")
    gencasepath_input = QtGui.QLineEdit()
    gencasepath_input.setText(data["gencase_path"])
    gencasepath_input.setPlaceholderText("Put GenCase path here")
    gencasepath_browse = QtGui.QPushButton("...")

    gencasepath_layout.addWidget(gencasepath_label)
    gencasepath_layout.addWidget(gencasepath_input)
    gencasepath_layout.addWidget(gencasepath_browse)

    # DualSPHyisics path
    dsphpath_layout = QtGui.QHBoxLayout()
    dsphpath_label = QtGui.QLabel("DualSPHysics Path: ")
    dsphpath_input = QtGui.QLineEdit()
    dsphpath_input.setText(data["dsphysics_path"])
    dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
    dsphpath_browse = QtGui.QPushButton("...")

    dsphpath_layout.addWidget(dsphpath_label)
    dsphpath_layout.addWidget(dsphpath_input)
    dsphpath_layout.addWidget(dsphpath_browse)

    # PartVTK4 path
    partvtk4path_layout = QtGui.QHBoxLayout()
    partvtk4path_label = QtGui.QLabel("PartVTK Path: ")
    partvtk4path_input = QtGui.QLineEdit()
    partvtk4path_input.setText(data["partvtk4_path"])
    partvtk4path_input.setPlaceholderText("Put PartVTK4 path here")
    partvtk4path_browse = QtGui.QPushButton("...")

    partvtk4path_layout.addWidget(partvtk4path_label)
    partvtk4path_layout.addWidget(partvtk4path_input)
    partvtk4path_layout.addWidget(partvtk4path_browse)

    # ComputeForces path
    computeforces_layout = QtGui.QHBoxLayout()
    computeforces_label = QtGui.QLabel("ComputeForces Path: ")
    computeforces_input = QtGui.QLineEdit()
    try:
        computeforces_input.setText(data["computeforces_path"])
    except KeyError:
        computeforces_input.setText("")
    computeforces_input.setPlaceholderText("Put ComputeForces path here")
    computeforces_browse = QtGui.QPushButton("...")

    computeforces_layout.addWidget(computeforces_label)
    computeforces_layout.addWidget(computeforces_input)
    computeforces_layout.addWidget(computeforces_browse)

    # FloatingInfo path
    floatinginfo_layout = QtGui.QHBoxLayout()
    floatinginfo_label = QtGui.QLabel("FloatingInfo Path: ")
    floatinginfo_input = QtGui.QLineEdit()
    try:
        floatinginfo_input.setText(data["floatinginfo_path"])
    except KeyError:
        floatinginfo_input.setText("")
    floatinginfo_input.setPlaceholderText("Put FloatingInfo path here")
    floatinginfo_browse = QtGui.QPushButton("...")

    floatinginfo_layout.addWidget(floatinginfo_label)
    floatinginfo_layout.addWidget(floatinginfo_input)
    floatinginfo_layout.addWidget(floatinginfo_browse)

    # MeasureTool path
    measuretool_layout = QtGui.QHBoxLayout()
    measuretool_label = QtGui.QLabel("MeasureTool Path: ")
    measuretool_input = QtGui.QLineEdit()
    try:
        measuretool_input.setText(data["measuretool_path"])
    except KeyError:
        measuretool_input.setText("")
    measuretool_input.setPlaceholderText("Put MeasureTool path here")
    measuretool_browse = QtGui.QPushButton("...")

    measuretool_layout.addWidget(measuretool_label)
    measuretool_layout.addWidget(measuretool_input)
    measuretool_layout.addWidget(measuretool_browse)

    # IsoSurface path
    isosurface_layout = QtGui.QHBoxLayout()
    isosurface_label = QtGui.QLabel("IsoSurface Path: ")
    isosurface_input = QtGui.QLineEdit()
    try:
        isosurface_input.setText(data["isosurface_path"])
    except KeyError:
        isosurface_input.setText("")
    isosurface_input.setPlaceholderText("Put IsoSurface path here")
    isosurface_browse = QtGui.QPushButton("...")

    isosurface_layout.addWidget(isosurface_label)
    isosurface_layout.addWidget(isosurface_input)
    isosurface_layout.addWidget(isosurface_browse)

    # BoundaryVTK path
    boundaryvtk_layout = QtGui.QHBoxLayout()
    boundaryvtk_label = QtGui.QLabel("BoundaryVTK Path: ")
    boundaryvtk_input = QtGui.QLineEdit()
    try:
        boundaryvtk_input.setText(data["boundaryvtk_path"])
    except KeyError:
        boundaryvtk_input.setText("")
    boundaryvtk_input.setPlaceholderText("Put BoundaryVTK path here")
    boundaryvtk_browse = QtGui.QPushButton("...")

    boundaryvtk_layout.addWidget(boundaryvtk_label)
    boundaryvtk_layout.addWidget(boundaryvtk_input)
    boundaryvtk_layout.addWidget(boundaryvtk_browse)

    # ParaView path
    paraview_layout = QtGui.QHBoxLayout()
    paraview_label = QtGui.QLabel("ParaView Path: ")
    paraview_input = QtGui.QLineEdit()
    try:
        paraview_input.setText(data["paraview_path"])
    except KeyError:
        paraview_input.setText("")
    paraview_input.setPlaceholderText("Put ParaView path here")
    paraview_browse = QtGui.QPushButton("...")

    paraview_layout.addWidget(paraview_label)
    paraview_layout.addWidget(paraview_input)
    paraview_layout.addWidget(paraview_browse)

    # ------------ Button behaviour definition --------------
    def on_ok():
        data['gencase_path'] = gencasepath_input.text()
        data['dsphysics_path'] = dsphpath_input.text()
        data['partvtk4_path'] = partvtk4path_input.text()
        data['computeforces_path'] = computeforces_input.text()
        data['floatinginfo_path'] = floatinginfo_input.text()
        data['measuretool_path'] = measuretool_input.text()
        data['isosurface_path'] = isosurface_input.text()
        data['boundaryvtk_path'] = boundaryvtk_input.text()
        data['paraview_path'] = paraview_input.text()
        with open(FreeCAD.getUserAppDataDir() + '/dsph_data-{}.dsphdata'.format(utils.VERSION),
                  'wb') as picklefile:
            pickle.dump(data, picklefile, utils.PICKLE_PROTOCOL)
        utils.log("Setup changed. Saved to " + FreeCAD.getUserAppDataDir() +
                  '/dsph_data-{}.dsphdata'.format(utils.VERSION))
        data_to_merge, state = utils.check_executables(data)
        data.update(data_to_merge)
        setup_window.accept()

    def on_cancel():
        utils.log("Setup not changed")
        setup_window.reject()

    def on_gencase_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select GenCase path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed gencase
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "gencase" in output[0:15].lower():
                gencasepath_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize GenCase in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize GenCase in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_dualsphysics_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select DualSPHysics path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed dualsphysics
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            if platform == "linux" or platform == "linux2":
                os.environ["LD_LIBRARY_PATH"] = "{}/".format(
                    "/".join(file_name.split("/")[:-1]))
                process.start('"{}"'.format(file_name))
            else:
                process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())
            if "dualsphysics" in output[0:20].lower():
                dsphpath_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize DualSPHysics in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize DualSPHysics in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_partvtk4_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select PartVTK4 path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed dualsphysics
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "partvtk4" in output[0:20].lower():
                partvtk4path_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize PartVTK4 in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize PartVTK4 in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_computeforces_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select ComputeForces path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed computeforces
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "computeforces" in output[0:22].lower():
                computeforces_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize ComputeForces in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize ComputeForces in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_floatinginfo_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select FloatingInfo path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed floatinginfo
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "floatinginfo" in output[0:22].lower():
                floatinginfo_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize FloatingInfo in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize FloatingInfo in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_measuretool_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select MeasureTool path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "measuretool" in output[0:22].lower():
                measuretool_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize MeasureTool in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize MeasureTool in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_isosurface_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select IsoSurface path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "isosurface" in output[0:22].lower():
                isosurface_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize IsoSurface in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize IsoSurface in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_boundaryvtk_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select BoundaryVTK path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "boundaryvtk" in output[0:22].lower():
                boundaryvtk_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize BoundaryVTK in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize BoundaryVTK in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                    "with: chmod +x /path/to/the/executable"
                )

    def on_paraview_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select ParaView path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            paraview_input.setText(file_name)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    gencasepath_browse.clicked.connect(on_gencase_browse)
    dsphpath_browse.clicked.connect(on_dualsphysics_browse)
    partvtk4path_browse.clicked.connect(on_partvtk4_browse)
    computeforces_browse.clicked.connect(on_computeforces_browse)
    floatinginfo_browse.clicked.connect(on_floatinginfo_browse)
    measuretool_browse.clicked.connect(on_measuretool_browse)
    boundaryvtk_browse.clicked.connect(on_boundaryvtk_browse)
    isosurface_browse.clicked.connect(on_isosurface_browse)
    paraview_browse.clicked.connect(on_paraview_browse)

    # Button layout definition
    stp_button_layout = QtGui.QHBoxLayout()
    stp_button_layout.addStretch(1)
    stp_button_layout.addWidget(ok_button)
    stp_button_layout.addWidget(cancel_button)

    # START Main layout definition and composition.
    stp_main_layout = QtGui.QVBoxLayout()
    stp_main_layout.addLayout(gencasepath_layout)
    stp_main_layout.addLayout(dsphpath_layout)
    stp_main_layout.addLayout(partvtk4path_layout)
    stp_main_layout.addLayout(computeforces_layout)
    stp_main_layout.addLayout(floatinginfo_layout)
    stp_main_layout.addLayout(measuretool_layout)
    stp_main_layout.addLayout(isosurface_layout)
    stp_main_layout.addLayout(boundaryvtk_layout)
    stp_main_layout.addLayout(paraview_layout)
    stp_main_layout.addStretch(1)

    stp_groupbox = QtGui.QGroupBox("Setup parameters")
    stp_groupbox.setLayout(stp_main_layout)
    setup_window_layout = QtGui.QVBoxLayout()
    setup_window_layout.addWidget(stp_groupbox)
    setup_window_layout.addLayout(stp_button_layout)
    setup_window.setLayout(setup_window_layout)
    # END Main layout definition and composition.

    setup_window.resize(600, 400)
    setup_window.exec_()


def widget_state_config(widgets, config):
    """ Takes an widget dictionary and a config string to
        enable and disable certain widgets base on a case. """
    if config == "no case":
        widgets["casecontrols_bt_savedoc"].setEnabled(False)
        widgets["constants_button"].setEnabled(False)
        widgets["execparams_button"].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(False)
        widgets["casecontrols_bt_addstl"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets["objectlist_table"].setEnabled(False)
        widgets["dp_input"].setEnabled(False)
        widgets["summary_bt"].setEnabled(False)
        widgets["toggle3dbutton"].setEnabled(False)
    elif config == "new case":
        widgets["constants_button"].setEnabled(True)
        widgets["execparams_button"].setEnabled(True)
        widgets["casecontrols_bt_savedoc"].setEnabled(True)
        widgets["dp_input"].setEnabled(True)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addstl"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["properties_bt"].setEnabled(True)
    elif config == "gencase done":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
    elif config == "gencase not done":
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
    elif config == "load base":
        widgets["constants_button"].setEnabled(True)
        widgets["execparams_button"].setEnabled(True)
        widgets["casecontrols_bt_savedoc"].setEnabled(True)
        widgets["dp_input"].setEnabled(True)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addstl"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["properties_bt"].setEnabled(True)
    elif config == "simulation done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
    elif config == "simulation not done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
    elif config == "execs not correct":
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
    elif config == "sim start":
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
    elif config == "sim cancel":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
        # Post-proccessing is enabled on cancel, to evaluate only currently exported parts
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
    elif config == "sim finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
    elif config == "sim error":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
    elif config == "export start":
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
    elif config == "export cancel":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
    elif config == "export finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)


def case_summary(orig_data):
    """ Displays a dialog with a summary of the current opened case. """

    if not utils.valid_document_environment():
        return

    # Data copy to avoid referencing issues
    data = dict(orig_data)

    # Preprocess data to show in data copy
    data['gravity'] = "({}, {}, {})".format(*data['gravity'])
    if data['project_name'] == "":
        data['project_name'] = "<i>{}</i>".format(utils.__("Not yet saved"))

    if data['project_path'] == "":
        data['project_path'] = "<i>{}</i>".format(utils.__("Not yet saved"))

    for k in ['gencase_path', 'dsphysics_path', 'partvtk4_path']:
        if data[k] == "":
            data[k] = "<i>{}</i>".format(
                utils.__("Executable not correctly set"))

    data['stepalgorithm'] = {
        '1': 'Verlet',
        '2': 'Symplectic'
    }[str(data['stepalgorithm'])]
    data['project_mode'] = '3D' if data['3dmode'] else '2D'

    data['incz'] = float(data['incz']) * 100
    data['partsoutmax'] = float(data['partsoutmax']) * 100

    # Setting certain values to automatic
    for x in [
            'hswl', 'speedsystem', 'speedsound', 'h', 'b', 'massfluid',
            'massbound'
    ]:
        data[x] = '<u>Automatic</u>' if data[x + '_auto'] else data[x]

    # region Formatting objects info
    data['objects_info'] = ""
    if len(data['simobjects']) > 1:
        data['objects_info'] += "<ul>"
        # data['simobjects'] is a dict with format
        # {'key': ['mk', 'type', 'fill']} where key is an internal name.
        for key, value in data['simobjects'].iteritems():
            if key.lower() == 'case_limits':
                continue
            fc_object = utils.get_fc_object(key)
            is_floating = utils.__('Yes') if str(
                value[0]) in data['floating_mks'].keys() else utils.__('No')
            is_floating = utils.__('No') if value[
                1].lower() == "fluid" else is_floating
            has_initials = utils.__('Yes') if str(
                value[0]) in data['initials_mks'].keys() else utils.__('No')
            has_initials = utils.__('No') if value[
                1].lower() == "bound" else has_initials
            real_mk = value[0] + 11 if value[
                1].lower() == "bound" else value[0] + 1
            data['objects_info'] += "<li><b>{label}</b> (<i>{iname}</i>): <br/>" \
                                    "Type: {type} (MK{type}: <b>{mk}</b> ; MK: <b>{real_mk}</b>)<br/>" \
                                    "Fill mode: {fillmode}<br/>" \
                                    "Floating: {floats}<br/>" \
                                    "Initials: {initials}</li><br/>".format(label=fc_object.Label, iname=key,
                                                                            type=value[1].title(), mk=value[0],
                                                                            real_mk=str(
                                                                                real_mk),
                                                                            fillmode=value[2].title(
                                                                            ),
                                                                            floats=is_floating,
                                                                            initials=has_initials)
        data['objects_info'] += "</ul>"
    else:
        data['objects_info'] += utils.__(
            "No objects were added to the simulation yet.")
    # endregion Formatting objects info

    # region Formatting movement info
    data['movement_info'] = ""
    if len(data['simobjects']) > 1:
        data['movement_info'] += "<ul>"
        for mov in data['global_movements']:
            try:
                movtype = mov.type
            except AttributeError:
                movtype = mov.__class__.__name__

            mklist = list()
            for key, value in data['motion_mks'].iteritems():
                if mov in value:
                    mklist.append(str(key))

            data['movement_info'] += "<li>{movtype} <u>{movname}</u><br/>" \
                                     "Applied to MKBound: {mklist}</li><br/>".format(
                                         movtype=movtype, movname=mov.name, mklist=', '.join(mklist))

        data['movement_info'] += "</ul>"
    else:
        data['movement_info'] += "No movements were defined in this case."

    # Create a string with MK used (of each type)
    data['mkboundused'] = list()
    data['mkfluidused'] = list()
    for element in data['simobjects'].values():
        if element[1].lower() == 'bound':
            data['mkboundused'].append(str(element[0]))
        elif element[1].lower() == 'fluid':
            data['mkfluidused'].append(str(element[0]))

    data['mkboundused'] = ", ".join(
        data['mkboundused']) if len(data['mkboundused']) > 0 else "None"
    data['mkfluidused'] = ", ".join(
        data['mkfluidused']) if len(data['mkfluidused']) > 0 else "None"

    # endregion Formatting movement info

    # Dialog creation and template filling
    main_window = QtGui.QDialog()
    main_layout = QtGui.QVBoxLayout()
    info = QtGui.QTextEdit()

    lib_folder = os.path.dirname(os.path.realpath(__file__))

    try:
        with open("{}/templates/case_summary_template.html".format(lib_folder),
                  "r") as input_template:
            info_text = input_template.read().format(**data)
    except:
        error_dialog(
            "An error occurred trying to load the template file and format it.")
        return

    info.setText(info_text)
    info.setReadOnly(True)

    main_layout.addWidget(info)
    main_window.setLayout(main_layout)
    main_window.setModal(True)
    main_window.setMinimumSize(500, 650)
    main_window.exec_()


def get_fc_view_object(internal_name):
    """ Returns a FreeCADGui View provider object by a name. """
    return FreeCADGui.getDocument("DSPH_Case").getObject(internal_name)


def gencase_completed_dialog(particle_count=0, detail_text="No details", data=dict()):
    """ Creates a gencase save dialog with different options, like
    open the results with paraview, show details or dismiss. """

    # Window Creation
    window = QtGui.QDialog()
    window.setWindowTitle(utils.__("Save & GenCase"))

    # Main Layout creation
    main_layout = QtGui.QVBoxLayout()

    # Main Layout elements
    info_message = QtGui.QLabel(
        utils.__("Gencase exported {} particles. Press View Details to check the output").format(str(particle_count)))

    button_layout = QtGui.QHBoxLayout()
    bt_open_with_paraview = QtGui.QPushButton(utils.__("Open with Paraview"))
    bt_details = QtGui.QPushButton(utils.__("View Details"))
    bt_ok = QtGui.QPushButton(utils.__("Ok"))
    button_layout.addWidget(bt_open_with_paraview)
    button_layout.addWidget(bt_details)
    button_layout.addWidget(bt_ok)

    ck_mkcells = QtGui.QRadioButton(
        utils.__("Open {}_MkCells").format(data['project_name']))
    ck_all = QtGui.QRadioButton(
        utils.__("Open {}_All").format(data['project_name']))
    ck_fluid = QtGui.QRadioButton(
        utils.__("Open {}_Fluid").format(data['project_name']))
    ck_bound = QtGui.QRadioButton(
        utils.__("Open {}_Bound").format(data['project_name']))

    horizontal_separator = h_line_generator()

    detail_text_area = QtGui.QTextEdit()
    detail_text_area.setText(detail_text)

    # Main Layout scaffolding
    main_layout.addWidget(info_message)
    main_layout.addWidget(ck_mkcells)
    main_layout.addWidget(ck_all)
    main_layout.addWidget(ck_fluid)
    main_layout.addWidget(ck_bound)
    main_layout.addLayout(button_layout)
    main_layout.addWidget(horizontal_separator)
    main_layout.addWidget(detail_text_area)

    # Window logic
    horizontal_separator.hide()
    detail_text_area.hide()
    ck_mkcells.setChecked(True)

    if len(data["paraview_path"]) > 1:
        bt_open_with_paraview.show()
        ck_mkcells.show()
        ck_all.show()
        ck_fluid.show()
        ck_bound.show()
    else:
        bt_open_with_paraview.hide()
        ck_mkcells.hide()
        ck_all.hide()
        ck_fluid.hide()
        ck_bound.hide()

    def on_ok():
        window.accept()

    def on_view_details():
        if horizontal_separator.isVisible():
            horizontal_separator.hide()
            detail_text_area.hide()
            bt_details.setText(utils.__("View Details"))
        elif not horizontal_separator.isVisible():
            horizontal_separator.show()
            detail_text_area.show()
            bt_details.setText(utils.__("Hide Details"))

    def on_open_paraview():
        suffix = "All"
        if ck_mkcells.isChecked():
            suffix = "MkCells"
        if ck_all.isChecked():
            suffix = "All"
        if ck_fluid.isChecked():
            suffix = "Fluid"
        if ck_bound.isChecked():
            suffix = "Bound"

        subprocess.Popen(
            [
                data['paraview_path'],
                "--data={}\\{}".format(
                    data['project_path'] + '\\' +
                    data['project_name'] + '_Out',
                    data['project_name'] + "_{}.vtk".format(suffix)
                )
            ],
            stdout=subprocess.PIPE)
        window.accept()

    bt_ok.clicked.connect(on_ok)
    bt_details.clicked.connect(on_view_details)
    bt_open_with_paraview.clicked.connect(on_open_paraview)

    # Window scaffolding and execution
    window.setLayout(main_layout)
    window.exec_()
