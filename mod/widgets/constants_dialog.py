#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Constants Configuration Dialog.'''


from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log

from mod.constants import HELP_GRAVITYX, HELP_GRAVITYY, HELP_GRAVITYZ, HELP_RHOP0, HELP_HSWL, HELP_GAMMA, HELP_SPEEDSYSTEM
from mod.constants import HELP_COEFSOUND, HELP_SPEEDSOUND, HELP_COEFH, HELP_CFLNUMBER

from mod.widgets.hoverable_label import HoverableLabel
from mod.widgets.focusable_line_edit import FocusableLineEdit

from mod.dataobjects.case import Case


class ConstantsDialog(QtGui.QDialog):
    ''' A window to define and configure the constants of the case for later execution
        in the DualSPHysics simulator. '''
    def __init__(self):
        super(ConstantsDialog, self).__init__()

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
        self.lattice_input.setCurrentIndex(Case.instance().constants.lattice_bound - 1)

        self.lattice_layout.addWidget(self.lattice_label)
        self.lattice_layout.addWidget(self.lattice_input)
        self.lattice_layout.addStretch(1)

        # Lattice for fluids layout and components
        self.lattice2_layout = QtGui.QHBoxLayout()
        self.lattice2_label = QtGui.QLabel("Lattice for Fluids: ")
        self.lattice2_input = QtGui.QComboBox()
        self.lattice2_input.insertItems(0, ['Lattice 1', 'Lattice 2'])
        self.lattice2_input.setCurrentIndex(Case.instance().constants.lattice_fluid - 1)

        self.lattice2_layout.addWidget(self.lattice2_label)
        self.lattice2_layout.addWidget(self.lattice2_input)
        self.lattice2_layout.addStretch(1)

        # Gravity
        self.gravity_layout = QtGui.QHBoxLayout()
        self.gravity_label = HoverableLabel("Gravity [X, Y, Z]: ")

        self.gravityx_input = QtGui.QLineEdit()
        self.gravityx_input = FocusableLineEdit()
        self.gravityx_input.setHelpText(__(HELP_GRAVITYX))
        self.gravityx_input.setMaxLength(10)

        self.gravityx_input.focus.connect(self.on_help_focus)

        self.gravityx_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityx_input)
        self.gravityx_input.setText(str(Case.instance().constants.gravity[0]))
        self.gravityx_input.setValidator(self.gravityx_validator)

        self.gravityy_input = QtGui.QLineEdit()
        self.gravityy_input = FocusableLineEdit()
        self.gravityy_input.setHelpText(__(HELP_GRAVITYY))
        self.gravityy_input.setMaxLength(10)

        self.gravityy_input.focus.connect(self.on_help_focus)

        self.gravityy_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityy_input)
        self.gravityy_input.setText(str(Case.instance().constants.gravity[1]))
        self.gravityy_input.setValidator(self.gravityy_validator)

        self.gravityz_input = QtGui.QLineEdit()
        self.gravityz_input = FocusableLineEdit()
        self.gravityz_input.setHelpText(__(HELP_GRAVITYZ))
        self.gravityz_input.setMaxLength(10)

        self.gravityz_input.focus.connect(self.on_help_focus)

        self.gravityz_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityz_input)
        self.gravityz_input.setText(str(Case.instance().constants.gravity[2]))
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
        self.rhop0_input.setHelpText(__(HELP_RHOP0))
        self.rhop0_input.setMaxLength(10)

        self.rhop0_input.focus.connect(self.on_help_focus)

        self.rhop0_validator = QtGui.QIntValidator(0, 10000, self.rhop0_input)
        self.rhop0_input.setText(str(Case.instance().constants.rhop0))
        self.rhop0_input.setValidator(self.rhop0_validator)
        self.rhop0_label2 = QtGui.QLabel(
            "kg/m<span style='vertical-align:super'>3<span>")

        self.rhop0_layout.addWidget(self.rhop0_label)
        self.rhop0_layout.addWidget(self.rhop0_input)
        self.rhop0_layout.addWidget(self.rhop0_label2)

        # Maximum still water level to calc.  spdofsound using coefsound: layout and
        # components
        self.hswlauto_layout = QtGui.QHBoxLayout()
        self.hswlauto_chk = QtGui.QCheckBox("Auto HSWL ")
        if Case.instance().constants.hswl_auto:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hswlauto_chk.toggled.connect(self.on_hswlauto_check)
        self.hswlauto_layout.addWidget(self.hswlauto_chk)

        self.hswl_layout = QtGui.QHBoxLayout()
        self.hswl_label = QtGui.QLabel("HSWL: ")
        self.hswl_input = QtGui.QLineEdit()
        self.hswl_input = FocusableLineEdit()
        self.hswl_input.setHelpText(__(HELP_HSWL))
        self.hswl_input.setMaxLength(10)

        self.hswl_input.focus.connect(self.on_help_focus)

        self.hswl_validator = QtGui.QIntValidator(0, 10000, self.hswl_input)
        self.hswl_input.setText(str(Case.instance().constants.hswl))
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
        self.gamma_input.setHelpText(__(HELP_GAMMA))
        self.gamma_input.setMaxLength(3)

        self.gamma_input.focus.connect(self.on_help_focus)

        self.gamma_validator = QtGui.QIntValidator(0, 999, self.gamma_input)
        self.gamma_input.setText(str(Case.instance().constants.gamma))
        self.gamma_input.setValidator(self.gamma_validator)
        self.gamma_label2 = QtGui.QLabel("units")

        self.gamma_layout.addWidget(self.gamma_label)
        self.gamma_layout.addWidget(self.gamma_input)
        self.gamma_layout.addWidget(self.gamma_label2)

        # Speedsystem: layout and components
        self.speedsystemauto_layout = QtGui.QHBoxLayout()
        self.speedsystemauto_chk = QtGui.QCheckBox("Auto Speedsystem ")
        if Case.instance().constants.speedsystem_auto:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsystemauto_chk.toggled.connect(self.on_speedsystemauto_check)
        self.speedsystemauto_layout.addWidget(self.speedsystemauto_chk)

        self.speedsystem_layout = QtGui.QHBoxLayout()
        self.speedsystem_label = QtGui.QLabel("Speedsystem: ")
        self.speedsystem_input = QtGui.QLineEdit()
        self.speedsystem_input = FocusableLineEdit()
        self.speedsystem_input.setHelpText(__(HELP_SPEEDSYSTEM))
        self.speedsystem_input.setMaxLength(10)

        self.speedsystem_input.focus.connect(self.on_help_focus)

        self.speedsystem_validator = QtGui.QIntValidator(0, 10000, self.speedsystem_input)
        self.speedsystem_input.setText(str(Case.instance().constants.speedsystem))
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
        self.coefsound_input.setHelpText(__(HELP_COEFSOUND))
        self.coefsound_input.setMaxLength(3)

        self.coefsound_input.focus.connect(self.on_help_focus)

        self.coefsound_validator = QtGui.QIntValidator(0, 999, self.coefsound_input)
        self.coefsound_input.setText(str(Case.instance().constants.coefsound))
        self.coefsound_input.setValidator(self.coefsound_validator)
        self.coefsound_label2 = QtGui.QLabel("units")

        self.coefsound_layout.addWidget(self.coefsound_label)
        self.coefsound_layout.addWidget(self.coefsound_input)
        self.coefsound_layout.addWidget(self.coefsound_label2)

        # Speedsound: layout and components
        self.speedsoundauto_layout = QtGui.QHBoxLayout()
        self.speedsoundauto_chk = QtGui.QCheckBox("Auto Speedsound ")
        if Case.instance().constants.speedsound_auto:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsoundauto_chk.toggled.connect(self.on_speedsoundauto_check)
        self.speedsoundauto_layout.addWidget(self.speedsoundauto_chk)

        self.speedsound_layout = QtGui.QHBoxLayout()
        self.speedsound_label = QtGui.QLabel("Speedsound: ")
        self.speedsound_input = QtGui.QLineEdit()
        self.speedsound_input = FocusableLineEdit()
        self.speedsound_input.setHelpText(__(HELP_SPEEDSOUND))
        self.speedsound_input.setMaxLength(10)

        self.speedsound_input.focus.connect(self.on_help_focus)

        self.speedsound_validator = QtGui.QIntValidator(0, 10000, self.speedsound_input)
        self.speedsound_input.setText(str(Case.instance().constants.speedsound))
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
        self.coefh_input.setHelpText(__(HELP_COEFH))
        self.coefh_input.setMaxLength(10)

        self.coefh_input.focus.connect(self.on_help_focus)

        self.coefh_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.coefh_input.setText(str(Case.instance().constants.coefh))
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
        self.cflnumber_input.setHelpText(__(HELP_CFLNUMBER))
        self.cflnumber_input.setMaxLength(10)

        self.cflnumber_input.focus.connect(self.on_help_focus)

        self.cflnumber_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.cflnumber_input.setText(str(Case.instance().constants.cflnumber))
        self.cflnumber_input.setValidator(self.cflnumber_validator)
        self.cflnumber_label2 = QtGui.QLabel("units")

        self.cflnumber_layout.addWidget(self.cflnumber_label)
        self.cflnumber_layout.addWidget(self.cflnumber_input)
        self.cflnumber_layout.addWidget(self.cflnumber_label2)

        # h: layout and components
        self.hauto_layout = QtGui.QHBoxLayout()
        self.hauto_chk = QtGui.QCheckBox("Auto Smoothing length ")
        if Case.instance().constants.h_auto:
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
        self.h_input.setText(str(Case.instance().constants.h))
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
        if Case.instance().constants.b_auto:
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
        self.b_input.setText(str(Case.instance().constants.b))
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
        self.cw_helpText_layout.setStretchFactor(self.help_window, 0)

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
        Case.instance().constants.lattice_bound = self.lattice_input.currentIndex() + 1
        Case.instance().constants.lattice_fluid = self.lattice2_input.currentIndex() + 1
        Case.instance().constants.gravity = [
            float(self.gravityx_input.text()),
            float(self.gravityy_input.text()),
            float(self.gravityz_input.text())
        ]
        Case.instance().constants.rhop0 = float(self.rhop0_input.text())
        Case.instance().constants.hswl = float(self.hswl_input.text())
        Case.instance().constants.hswl_auto = self.hswlauto_chk.isChecked()
        Case.instance().constants.gamma = float(self.gamma_input.text())
        Case.instance().constants.speedsystem = float(self.speedsystem_input.text())
        Case.instance().constants.speedsystem_auto = self.speedsystemauto_chk.isChecked()
        Case.instance().constants.coefsound = float(self.coefsound_input.text())
        Case.instance().constants.speedsound = float(self.speedsound_input.text())
        Case.instance().constants.speedsound_auto = self.speedsoundauto_chk.isChecked()
        Case.instance().constants.coefh = float(self.coefh_input.text())
        Case.instance().constants.cflnumber = float(self.cflnumber_input.text())
        Case.instance().constants.h = float(self.h_input.text())
        Case.instance().constants.h_auto = self.hauto_chk.isChecked()
        Case.instance().constants.b = float(self.b_input.text())
        Case.instance().constants.b_auto = self.bauto_chk.isChecked()
        log("Constants changed")
        self.accept()

    def on_cancel(self):
        log("Constants not changed")
        self.reject()
