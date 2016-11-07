# -*- coding: utf-8 -*-

'''
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DualSPHysics for FreeCAD.

DualSPHysics for FreeCAD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DualSPHysics for FreeCAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DualSPHysics for FreeCAD.  If not, see <http://www.gnu.org/licenses/>.
'''

import FreeCAD, FreeCADGui
import sys, os, pickle, threading, math, webbrowser, traceback, glob, numpy
from PySide import QtGui, QtCore
from datetime import datetime
import utils

def warning_dialog(warn_text):
    '''Spawns a warning dialog with the text passed.'''

    warning_messagebox = QtGui.QMessageBox()
    warning_messagebox.setText(warn_text)
    warning_messagebox.setIcon(QtGui.QMessageBox.Warning)
    warning_messagebox.exec_()

def info_dialog(info_text):
    '''Spawns an info dialog with the text passed.'''

    info_messagebox = QtGui.QMessageBox()
    info_messagebox.setText(info_text)
    info_messagebox.setIcon(QtGui.QMessageBox.Information)
    info_messagebox.exec_()

def ok_cancel_dialog(title, text):
    '''Spawns an okay/cancel dialog with the title and text passed'''

    openConfirmDialog = QtGui.QMessageBox()
    openConfirmDialog.setText(title)
    openConfirmDialog.setInformativeText(text)
    openConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    openConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
    return openConfirmDialog.exec_()

def def_constants_window(data):
    '''Defines the constants window creation and functonality.
    Modifies the passed data dictionary to update data if ok is pressed.'''

    #Creates a dialog and 2 main buttons
    constants_window = QtGui.QDialog()
    constants_window.setWindowTitle("DSPH Constant definition")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    #Lattice for boundaries layout and components
    lattice_layout = QtGui.QHBoxLayout()
    lattice_label = QtGui.QLabel("Lattice for Boundaries: ")
    lattice_input = QtGui.QLineEdit()
    lattice_input.setMaxLength(1)    
    lattice_validator = QtGui.QIntValidator(1, 2, lattice_input)
    lattice_input.setText(str(data['lattice_bound']))
    lattice_input.setValidator(lattice_validator)
    lattice_label2 = QtGui.QLabel("units")

    lattice_layout.addWidget(lattice_label)
    lattice_layout.addWidget(lattice_input)
    lattice_layout.addWidget(lattice_label2)

    #Lattice for fluids layout and components
    lattice2_layout = QtGui.QHBoxLayout()
    lattice2_label = QtGui.QLabel("Lattice for Fluids: ")
    lattice2_input = QtGui.QLineEdit()
    lattice2_input.setMaxLength(1)    
    lattice2_validator = QtGui.QIntValidator(1, 2, lattice2_input)
    lattice2_input.setText(str(data['lattice_bound']))
    lattice2_input.setValidator(lattice2_validator)
    lattice2_label2 = QtGui.QLabel("units")

    lattice2_layout.addWidget(lattice2_label)
    lattice2_layout.addWidget(lattice2_input)
    lattice2_layout.addWidget(lattice2_label2)

    #Gravity
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
    
    gravity_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

    gravity_layout.addWidget(gravity_label)
    gravity_layout.addWidget(gravityx_input) #For X
    gravity_layout.addWidget(gravityy_input) #For Y
    gravity_layout.addWidget(gravityz_input) #For Z
    gravity_layout.addWidget(gravity_label2)
    
    #Reference density of the fluid: layout and components
    rhop0_layout = QtGui.QHBoxLayout()
    rhop0_label = QtGui.QLabel("Fluid reference density: ")
    rhop0_input = QtGui.QLineEdit()
    rhop0_input.setMaxLength(10)    
    rhop0_validator = QtGui.QIntValidator(0, 10000, rhop0_input)
    rhop0_input.setText(str(data['rhop0']))
    rhop0_input.setValidator(rhop0_validator)
    rhop0_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3<span>")

    rhop0_layout.addWidget(rhop0_label)
    rhop0_layout.addWidget(rhop0_input)
    rhop0_layout.addWidget(rhop0_label2)

    #Maximum still water lavel to calc. spdofsound using coefsound: layout and components
    hswlauto_layout = QtGui.QHBoxLayout()
    hswlauto_chk = QtGui.QCheckBox("Auto HSWL ")
    if data['hswl_auto']:
        hswlauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_hswlauto_check(): #Controls if user selected auto HSWL or not enabling/disablen HSWL custom value introduction
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

    #Manually trigger check for the first time
    on_hswlauto_check()

    #gamma: layout and components
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

    #Speedsystem: layout and components
    speedsystemauto_layout = QtGui.QHBoxLayout()
    speedsystemauto_chk = QtGui.QCheckBox("Auto Speedsystem ")
    if data['speedsystem_auto']:
        speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_speedsystemauto_check(): #Controls if user selected auto speedsystem or not enabling/disablen speedsystem custom value introduction
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
    speedsystem_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

    speedsystem_layout.addWidget(speedsystem_label)
    speedsystem_layout.addWidget(speedsystem_input)
    speedsystem_layout.addWidget(speedsystem_label2)

    #Manually trigger check for the first time
    on_speedsystemauto_check()

    #coefsound: layout and components
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

    #Speedsound: layout and components
    speedsoundauto_layout = QtGui.QHBoxLayout()
    speedsoundauto_chk = QtGui.QCheckBox("Auto Speedsound ")
    if data['speedsound_auto']:
        speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_speedsoundauto_check(): #Controls if user selected auto speedsound or not enabling/disablen speedsound custom value introduction
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
    speedsound_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

    speedsound_layout.addWidget(speedsound_label)
    speedsound_layout.addWidget(speedsound_input)
    speedsound_layout.addWidget(speedsound_label2)

    #Manually trigger check for the first time
    on_speedsoundauto_check()

    #coefh: layout and components
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

    #cflnumber: layout and components
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

    #h: layout and components
    hauto_layout = QtGui.QHBoxLayout()
    hauto_chk = QtGui.QCheckBox("Auto Smoothing length ")
    if data['h_auto']:
        hauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        hauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_hauto_check(): #Controls if user selected auto h or not enabling/disablen h custom value introduction
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

    #Manually trigger check for the first time
    on_hauto_check()

    #b: layout and components
    bauto_layout = QtGui.QHBoxLayout()
    bauto_chk = QtGui.QCheckBox("Auto b constant for EOS ")
    if data['b_auto']:
        bauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        bauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_bauto_check(): #Controls if user selected auto b or not enabling/disablen b custom value introduction
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
    b_label2 = QtGui.QLabel("metres")

    b_layout.addWidget(b_label)
    b_layout.addWidget(b_input)
    b_layout.addWidget(b_label2)

    #Manually trigger check for the first time
    on_bauto_check()


    #------------ Button behaviour definition --------------
    def on_ok():
        data['lattice_bound'] = lattice_input.text()
        data['lattice_fluid'] = lattice2_input.text()
        data['gravity'] = [gravityx_input.text(), gravityy_input.text(), gravityz_input.text()]
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
        print "DualSPHysics for FreeCAD: Constants changed"
        constants_window.accept()

    def on_cancel():
        print "DualSPHysics for FreeCAD: Constants not changed"
        constants_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    #Button layout definition    
    cw_button_layout = QtGui.QHBoxLayout()
    cw_button_layout.addStretch(1)
    cw_button_layout.addWidget(ok_button)
    cw_button_layout.addWidget(cancel_button)

    #START Main layout definition and composition.
    cw_main_layout = QtGui.QVBoxLayout()
    
    cw_main_layout.addLayout(lattice_layout)
    cw_main_layout.addLayout(lattice2_layout)
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
    #END Main layout definition and composition.

    #Constant definition window behaviour and general composing
    constants_window.resize(600,400)
    ret_val = constants_window.exec_()

def def_execparams_window(data):
    '''Defines the execution parameters window.
    Modifies the data dictionary passed as parameter.'''

    #Creates a dialog and 2 main buttons
    execparams_window = QtGui.QDialog()
    execparams_window.setWindowTitle("DSPH Execution Parameters")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    #Precision in particle interaction
    posdouble_layout = QtGui.QHBoxLayout()
    posdouble_label = QtGui.QLabel("Precision in particle interaction: ")
    posdouble_input = QtGui.QLineEdit()
    posdouble_input.setMaxLength(1)    
    posdouble_validator = QtGui.QIntValidator(0, 2, posdouble_input)
    posdouble_input.setText(str(data['posdouble']))
    posdouble_input.setValidator(posdouble_validator)
    posdouble_label2 = QtGui.QLabel("[0,2]")

    posdouble_layout.addWidget(posdouble_label)
    posdouble_layout.addWidget(posdouble_input)
    posdouble_layout.addWidget(posdouble_label2)

    #Step Algorithm
    stepalgorithm_layout = QtGui.QHBoxLayout()
    stepalgorithm_label = QtGui.QLabel("Step Algorithm: ")
    stepalgorithm_input = QtGui.QLineEdit()
    stepalgorithm_input.setMaxLength(1)    
    stepalgorithm_validator = QtGui.QIntValidator(0, 2, stepalgorithm_input)
    stepalgorithm_input.setText(str(data['stepalgorithm']))
    stepalgorithm_input.setValidator(stepalgorithm_validator)
    stepalgorithm_label2 = QtGui.QLabel("[1,2]")

    stepalgorithm_layout.addWidget(stepalgorithm_label)
    stepalgorithm_layout.addWidget(stepalgorithm_input)
    stepalgorithm_layout.addWidget(stepalgorithm_label2)

    #Verlet steps
    verletsteps_layout = QtGui.QHBoxLayout()
    verletsteps_label = QtGui.QLabel("Verlet Steps: ")
    verletsteps_input = QtGui.QLineEdit()
    verletsteps_input.setMaxLength(4)    
    verletsteps_validator = QtGui.QIntValidator(0, 9999, verletsteps_input)
    verletsteps_input.setText(str(data['verletsteps']))
    verletsteps_input.setValidator(verletsteps_validator)

    verletsteps_layout.addWidget(verletsteps_label)
    verletsteps_layout.addWidget(verletsteps_input)

    #Kernel
    kernel_layout = QtGui.QHBoxLayout()
    kernel_label = QtGui.QLabel("Interaction kernel: ")
    kernel_input = QtGui.QLineEdit()
    kernel_input.setMaxLength(1)    
    kernel_validator = QtGui.QIntValidator(0, 2, kernel_input)
    kernel_input.setText(str(data['kernel']))
    kernel_input.setValidator(kernel_validator)
    kernel_label2 = QtGui.QLabel("[1,2]")

    kernel_layout.addWidget(kernel_label)
    kernel_layout.addWidget(kernel_input)
    kernel_layout.addWidget(kernel_label2)

    #Viscosity formulation
    def on_viscotreatment_change():
        if viscotreatment_input.text() == "1":
            visco_input.setText("0.01")
            
        elif viscotreatment_input.text() == "2":            
            visco_input.setText("0.000001")

    viscotreatment_layout = QtGui.QHBoxLayout()
    viscotreatment_label = QtGui.QLabel("Viscosity Formulation: ")
    viscotreatment_input = QtGui.QLineEdit()
    viscotreatment_input.setMaxLength(1)    
    viscotreatment_validator = QtGui.QIntValidator(0, 2, viscotreatment_input)
    viscotreatment_input.setText(str(data['viscotreatment']))
    viscotreatment_input.setValidator(viscotreatment_validator)
    viscotreatment_input.textChanged.connect(on_viscotreatment_change)
    viscotreatment_label2 = QtGui.QLabel("[1,2]")
    viscotreatment_layout.addWidget(viscotreatment_label)
    viscotreatment_layout.addWidget(viscotreatment_input)
    viscotreatment_layout.addWidget(viscotreatment_label2)

    #Viscosity value
    visco_layout = QtGui.QHBoxLayout()
    visco_label = QtGui.QLabel("Viscosity value: ")
    visco_input = QtGui.QLineEdit()
    visco_input.setMaxLength(10)    
    visco_input.setText(str(data['visco']))
    visco_layout.addWidget(visco_label)
    visco_layout.addWidget(visco_input)

    #Viscosity with boundary
    viscoboundfactor_layout = QtGui.QHBoxLayout()
    viscoboundfactor_label = QtGui.QLabel("Viscosity with boundary: ")
    viscoboundfactor_input = QtGui.QLineEdit()
    viscoboundfactor_input.setMaxLength(10)    
    viscoboundfactor_input.setText(str(data['viscoboundfactor']))

    viscoboundfactor_layout.addWidget(viscoboundfactor_label)
    viscoboundfactor_layout.addWidget(viscoboundfactor_input)

    #DeltaSPH value
    deltasph_layout = QtGui.QHBoxLayout()
    deltasph_label = QtGui.QLabel("DeltaSPH value: ")
    deltasph_input = QtGui.QLineEdit()
    deltasph_input.setMaxLength(10)    
    deltasph_input.setText(str(data['deltasph']))
    deltasph_layout.addWidget(deltasph_label)
    deltasph_layout.addWidget(deltasph_input)

    #Shifting mode
    shifting_layout = QtGui.QHBoxLayout()
    shifting_label = QtGui.QLabel("Shifting mode: ")
    shifting_input = QtGui.QLineEdit()
    shifting_input.setMaxLength(1)    
    shifting_validator = QtGui.QIntValidator(1, 3, shifting_input)
    shifting_input.setText(str(data['shifting']))
    shifting_input.setValidator(shifting_validator)
    shifting_label2 = QtGui.QLabel("[1,3]")
    shifting_layout.addWidget(shifting_label)
    shifting_layout.addWidget(shifting_input)
    shifting_layout.addWidget(shifting_label2)    

    #Coefficient for shifting
    shiftcoef_layout = QtGui.QHBoxLayout()
    shiftcoef_label = QtGui.QLabel("Coefficient for shifting: ")
    shiftcoef_input = QtGui.QLineEdit()
    shiftcoef_input.setMaxLength(10)    
    shiftcoef_input.setText(str(data['shiftcoef']))
    shiftcoef_layout.addWidget(shiftcoef_label)
    shiftcoef_layout.addWidget(shiftcoef_input)

    #Free surface detection threshold
    shifttfs_layout = QtGui.QHBoxLayout()
    shifttfs_label = QtGui.QLabel("Free surface detection threshold: ")
    shifttfs_input = QtGui.QLineEdit()
    shifttfs_input.setMaxLength(10)    
    shifttfs_input.setText(str(data['shifttfs']))
    shifttfs_layout.addWidget(shifttfs_label)
    shifttfs_layout.addWidget(shifttfs_input)

    #Rigid algorithm
    rigidalgorithm_layout = QtGui.QHBoxLayout()
    rigidalgorithm_label = QtGui.QLabel("Rigid algorithm: ")
    rigidalgorithm_input = QtGui.QLineEdit()
    rigidalgorithm_input.setMaxLength(1)    
    rigidalgorithm_validator = QtGui.QIntValidator(1, 2, rigidalgorithm_input)
    rigidalgorithm_input.setText(str(data['rigidalgorithm']))
    rigidalgorithm_input.setValidator(rigidalgorithm_validator)
    rigidalgorithm_label2 = QtGui.QLabel("[1,2]")
    rigidalgorithm_layout.addWidget(rigidalgorithm_label)
    rigidalgorithm_layout.addWidget(rigidalgorithm_input)
    rigidalgorithm_layout.addWidget(rigidalgorithm_label2)

    #Sim start freeze time
    ftpause_layout = QtGui.QHBoxLayout()
    ftpause_label = QtGui.QLabel("Sim start freeze time: ")
    ftpause_input = QtGui.QLineEdit()
    ftpause_input.setMaxLength(10)    
    ftpause_input.setText(str(data['ftpause']))
    ftpause_label2 = QtGui.QLabel("seconds")
    ftpause_layout.addWidget(ftpause_label)
    ftpause_layout.addWidget(ftpause_input)
    ftpause_layout.addWidget(ftpause_label2)


    #Coefficient to calculate DT
    coefdtmin_layout = QtGui.QHBoxLayout()
    coefdtmin_label = QtGui.QLabel("Coefficient to calculate DT: ")
    coefdtmin_input = QtGui.QLineEdit()
    coefdtmin_input.setMaxLength(10)    
    coefdtmin_input.setText(str(data['coefdtmin']))
    coefdtmin_layout.addWidget(coefdtmin_label)
    coefdtmin_layout.addWidget(coefdtmin_input)

    #Initial time step
    dtiniauto_layout = QtGui.QHBoxLayout()
    dtiniauto_chk = QtGui.QCheckBox("Initial time step auto")
    if data['dtini_auto']:
        dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)
    def on_dtiniauto_check(): #Controls if user selected auto b or not enabling/disablen b custom value introduction
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

    #Minimium time step
    dtminauto_layout = QtGui.QHBoxLayout()
    dtminauto_chk = QtGui.QCheckBox("Minimum time step: ")
    if data['dtmin_auto']:
        dtminauto_chk.setCheckState(QtCore.Qt.Checked)
    else:
        dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)

    def on_dtminauto_check(): #Controls if user selected auto b or not enabling/disablen b custom value introduction
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

    #Fixed DT file
    dtfixed_layout = QtGui.QHBoxLayout()
    dtfixed_label = QtGui.QLabel("Fixed DT file: ")
    dtfixed_input = QtGui.QLineEdit()
    dtfixed_input.setText(str(data['dtfixed']))
    dtfixed_label2 = QtGui.QLabel("file")
    dtfixed_layout.addWidget(dtfixed_label)
    dtfixed_layout.addWidget(dtfixed_input)
    dtfixed_layout.addWidget(dtfixed_label2)

    #Velocity of particles
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

    #Time of simulation
    timemax_layout = QtGui.QHBoxLayout()
    timemax_label = QtGui.QLabel("Time of simulation: ")
    timemax_input = QtGui.QLineEdit()
    timemax_input.setMaxLength(10)    
    timemax_input.setText(str(data['timemax']))
    timemax_label2 = QtGui.QLabel("seconds")
    timemax_layout.addWidget(timemax_label)
    timemax_layout.addWidget(timemax_input)
    timemax_layout.addWidget(timemax_label2)

    #Time out data
    timeout_layout = QtGui.QHBoxLayout()
    timeout_label = QtGui.QLabel("Time out data: ")
    timeout_input = QtGui.QLineEdit()
    timeout_input.setMaxLength(10)    
    timeout_input.setText(str(data['timeout']))
    timeout_label2 = QtGui.QLabel("seconds")
    timeout_layout.addWidget(timeout_label)
    timeout_layout.addWidget(timeout_input)
    timeout_layout.addWidget(timeout_label2)

    #Increase of Z+
    incz_layout = QtGui.QHBoxLayout()
    incz_label = QtGui.QLabel("Increase of Z+: ")
    incz_input = QtGui.QLineEdit()
    incz_input.setMaxLength(10)    
    incz_input.setText(str(data['incz']))
    incz_layout.addWidget(incz_label)
    incz_layout.addWidget(incz_input)

    #Max parts out allowed
    partsoutmax_layout = QtGui.QHBoxLayout()
    partsoutmax_label = QtGui.QLabel("Max parts out allowed: ")
    partsoutmax_input = QtGui.QLineEdit()
    partsoutmax_input.setMaxLength(10)    
    partsoutmax_input.setText(str(data['partsoutmax']))
    partsoutmax_layout.addWidget(partsoutmax_label)
    partsoutmax_layout.addWidget(partsoutmax_input)

    #Minimum rhop valid
    rhopoutmin_layout = QtGui.QHBoxLayout()
    rhopoutmin_label = QtGui.QLabel("Minimum rhop valid: ")
    rhopoutmin_input = QtGui.QLineEdit()
    rhopoutmin_input.setMaxLength(10)    
    rhopoutmin_input.setText(str(data['rhopoutmin']))
    rhopoutmin_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")
    rhopoutmin_layout.addWidget(rhopoutmin_label)
    rhopoutmin_layout.addWidget(rhopoutmin_input)
    rhopoutmin_layout.addWidget(rhopoutmin_label2)

    #Maximum rhop valid
    rhopoutmax_layout = QtGui.QHBoxLayout()
    rhopoutmax_label = QtGui.QLabel("Maximum rhop valid: ")
    rhopoutmax_input = QtGui.QLineEdit()
    rhopoutmax_input.setMaxLength(10)    
    rhopoutmax_input.setText(str(data['rhopoutmax']))
    rhopoutmax_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")
    rhopoutmax_layout.addWidget(rhopoutmax_label)
    rhopoutmax_layout.addWidget(rhopoutmax_input)
    rhopoutmax_layout.addWidget(rhopoutmax_label2)    

    #------------ Button behaviour definition --------------
    def on_ok():
        data['posdouble'] = posdouble_input.text()
        data['stepalgorithm'] = stepalgorithm_input.text()
        data['verletsteps'] = verletsteps_input.text()
        data['kernel'] = kernel_input.text()
        data['viscotreatment'] = viscotreatment_input.text()
        data['visco'] = visco_input.text()
        data['viscoboundfactor'] = viscoboundfactor_input.text()
        data['deltasph'] = deltasph_input.text()
        data['shifting'] = shifting_input.text()
        data['shiftcoef'] = shiftcoef_input.text()
        data['shifttfs'] = shifttfs_input.text()
        data['rigidalgorithm'] = rigidalgorithm_input.text()
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
        data['incz'] = incz_input.text()
        data['partsoutmax'] = partsoutmax_input.text()
        data['rhopoutmin'] = rhopoutmin_input.text()
        data['rhopoutmax'] = rhopoutmax_input.text()
        print "DualSPHysics for FreeCAD: Execution Parameters changed"
        execparams_window.accept()

    def on_cancel():
        print "DualSPHysics for FreeCAD: Execution Parameters not changed"
        execparams_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    #Button layout definition    
    ep_button_layout = QtGui.QHBoxLayout()
    ep_button_layout.addStretch(1)
    ep_button_layout.addWidget(ok_button)
    ep_button_layout.addWidget(cancel_button)

    #START Main layout definition and composition.
    ep_main_layout = QtGui.QVBoxLayout()
    ep_main_layout.addLayout(posdouble_layout)
    ep_main_layout.addLayout(stepalgorithm_layout)
    ep_main_layout.addLayout(verletsteps_layout)
    ep_main_layout.addLayout(kernel_layout)
    ep_main_layout.addLayout(viscotreatment_layout)
    ep_main_layout.addLayout(visco_layout)
    ep_main_layout.addLayout(viscoboundfactor_layout)
    ep_main_layout.addLayout(deltasph_layout)
    ep_main_layout.addLayout(shifting_layout)
    ep_main_layout.addLayout(shiftcoef_layout)
    ep_main_layout.addLayout(shifttfs_layout)
    ep_main_layout.addLayout(rigidalgorithm_layout)
    ep_main_layout.addLayout(ftpause_layout)
    ep_main_layout.addLayout(coefdtmin_layout)
    ep_main_layout.addLayout(dtiniauto_layout)
    ep_main_layout.addLayout(dtini_layout)
    ep_main_layout.addLayout(dtminauto_layout)
    ep_main_layout.addLayout(dtmin_layout)
    #ep_main_layout.addLayout(dtallparticles_layout)
    ep_main_layout.addLayout(timemax_layout)
    ep_main_layout.addLayout(timeout_layout)
    ep_main_layout.addLayout(incz_layout)
    ep_main_layout.addLayout(partsoutmax_layout)
    ep_main_layout.addLayout(rhopoutmin_layout)
    ep_main_layout.addLayout(rhopoutmax_layout)

    ep_main_layout.addStretch(1)

    ep_groupbox = QtGui.QGroupBox("Execution Parameters")
    ep_groupbox.setLayout(ep_main_layout)
    execparams_window_layout = QtGui.QVBoxLayout()
    execparams_window_layout.addWidget(ep_groupbox)    
    execparams_window_layout.addLayout(ep_button_layout)
    execparams_window.setLayout(execparams_window_layout)
    #END Main layout definition and composition.

    execparams_window.resize(600,400)
    ret_val = execparams_window.exec_()

def def_setup_window(data):
    '''Defines the setup window.
    Modifies data dictionary passed as parameter.'''

    #Creates a dialog and 2 main buttons
    setup_window = QtGui.QDialog()
    setup_window.setWindowTitle("DSPH Setup")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    #GenCase path
    gencasepath_layout = QtGui.QHBoxLayout()
    gencasepath_label = QtGui.QLabel("GenCase Path: ")
    gencasepath_input = QtGui.QLineEdit()
    gencasepath_input.setText(data["gencase_path"])
    gencasepath_input.setPlaceholderText("Put GenCase path here")
    gencasepath_browse = QtGui.QPushButton("...")

    gencasepath_layout.addWidget(gencasepath_label)
    gencasepath_layout.addWidget(gencasepath_input)
    gencasepath_layout.addWidget(gencasepath_browse)

    #DualSPHyisics path
    dsphpath_layout = QtGui.QHBoxLayout()
    dsphpath_label = QtGui.QLabel("DualSPHysics Path: ")
    dsphpath_input = QtGui.QLineEdit()
    dsphpath_input.setText(data["dsphysics_path"])
    dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
    dsphpath_browse = QtGui.QPushButton("...")

    dsphpath_layout.addWidget(dsphpath_label)
    dsphpath_layout.addWidget(dsphpath_input)
    dsphpath_layout.addWidget(dsphpath_browse)

    #PartVTK4 path
    partvtk4path_layout = QtGui.QHBoxLayout()
    partvtk4path_label = QtGui.QLabel("PartVTK4 Path: ")
    partvtk4path_input = QtGui.QLineEdit()
    partvtk4path_input.setText(data["partvtk4_path"])
    partvtk4path_input.setPlaceholderText("Put PartVTK4 path here")
    partvtk4path_browse = QtGui.QPushButton("...")

    partvtk4path_layout.addWidget(partvtk4path_label)
    partvtk4path_layout.addWidget(partvtk4path_input)
    partvtk4path_layout.addWidget(partvtk4path_browse)

    #------------ Button behaviour definition --------------
    def on_ok():
        data['gencase_path'] = gencasepath_input.text()
        data['dsphysics_path'] = dsphpath_input.text()
        data['partvtk4_path'] = partvtk4path_input.text()
        picklefile = open(FreeCAD.getUserAppDataDir()+'/dsph_data.dsphdata', 'wb')
        pickle.dump(data, picklefile)
        print "DualSPHysics for FreeCAD: Setup changed. Saved to "+FreeCAD.getUserAppDataDir()+"/dsph_data.dsphdata"
        data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'], state = utils.check_executables(data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'])
        if not state:
            ex_selector_combo.setEnabled(False)
            ex_button.setEnabled(False)
            ex_additional.setEnabled(False)
        setup_window.accept()

    def on_cancel():
        print "DualSPHysics for FreeCAD: Setup not changed"
        setup_window.reject()

    def on_gencase_browse():
        filedialog = QtGui.QFileDialog()
        fileName, _ = filedialog.getOpenFileName(setup_window, "Select GenCase path", QtCore.QDir.homePath())
        if fileName != "":
            #Verify if exe is indeed gencase
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start(fileName)
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "gencase" in output[0:15].lower():
                gencasepath_input.setText(fileName)
            else:
                print "ERROR: I can't recognize GenCase in that exe!"
                warning_dialog("I can't recognize GenCase in that exe!")

    def on_dualsphysics_browse():
        filedialog = QtGui.QFileDialog()
        fileName, _ = filedialog.getOpenFileName(setup_window, "Select DualSPHysics path", QtCore.QDir.homePath())
        if fileName != "":
            #Verify if exe is indeed dualsphysics
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start(fileName)
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "dualsphysics" in output[0:20].lower():
                dsphpath_input.setText(fileName)
            else:
                print "ERROR: I can't recognize DualSPHysics in that exe!"
                warning_dialog("I can't recognize DualSPHysics in that exe!")

    def on_partvtk4_browse():
        filedialog = QtGui.QFileDialog()
        fileName, _ = filedialog.getOpenFileName(setup_window, "Select PartVTK4 path", QtCore.QDir.homePath())
        if fileName != "":
            #Verify if exe is indeed dualsphysics
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start(fileName)
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "partvtk4" in output[0:20].lower():
                partvtk4path_input.setText(fileName)
            else:
                print "ERROR: I can't recognize PartVTK4 in that exe!"
                warning_dialog("I can't recognize PartVTK4 in that exe!")

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    gencasepath_browse.clicked.connect(on_gencase_browse)
    dsphpath_browse.clicked.connect(on_dualsphysics_browse)
    partvtk4path_browse.clicked.connect(on_partvtk4_browse)
    #Button layout definition    
    stp_button_layout = QtGui.QHBoxLayout()
    stp_button_layout.addStretch(1)
    stp_button_layout.addWidget(ok_button)
    stp_button_layout.addWidget(cancel_button)

    #START Main layout definition and composition.
    stp_main_layout = QtGui.QVBoxLayout()
    stp_main_layout.addLayout(gencasepath_layout)
    stp_main_layout.addLayout(dsphpath_layout)
    stp_main_layout.addLayout(partvtk4path_layout)
    stp_main_layout.addStretch(1)

    stp_groupbox = QtGui.QGroupBox("Setup parameters")
    stp_groupbox.setLayout(stp_main_layout)
    setup_window_layout = QtGui.QVBoxLayout()
    setup_window_layout.addWidget(stp_groupbox)    
    setup_window_layout.addLayout(stp_button_layout)
    setup_window.setLayout(setup_window_layout)
    #END Main layout definition and composition.

    setup_window.resize(600,400)
    ret_val = setup_window.exec_()