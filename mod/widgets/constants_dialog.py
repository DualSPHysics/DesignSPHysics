#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Constants Configuration Dialog."""


# from PySide import QtCore, QtGui
from PySide6 import QtCore, QtWidgets, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
from mod.enums import HelpText

from mod.widgets.hoverable_label import HoverableLabel
from mod.widgets.focusable_line_edit import FocusableLineEdit

from mod.dataobjects.case import Case


class ConstantsDialog(QtWidgets.QDialog):
    """ A window to define and configure the constants of the case for later execution
        in the DualSPHysics simulator. """

    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 415
    MINIMUM_HEIGHT = 500

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Constants definition"))
        self.help_label: QtWidgets.QLabel = QtWidgets.QLabel(self.LABEL_DEFAULT_TEXT)

        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))

        # Pointref
        self.pointref_layout = QtWidgets.QHBoxLayout()
        self.pointref_label = HoverableLabel(__("Pointref [X, Y, Z]:"))

        self.pointrefx_input = QtWidgets.QLineEdit()
        self.pointrefx_input = FocusableLineEdit()
        self.pointrefx_input.set_help_text(HelpText.POINTREFX)
        self.pointrefx_input.setMaxLength(10)

        self.pointrefx_input.focus.connect(self.on_help_focus)

        self.pointrefx_validator = QtGui.QDoubleValidator(-200, 200, 8, self.pointrefx_input)
        self.pointrefx_input.setText(str(Case.the().constants.pointref[0]))
        self.pointrefx_input.setValidator(self.pointrefx_validator)

        self.pointrefy_input = QtWidgets.QLineEdit()
        self.pointrefy_input = FocusableLineEdit()
        self.pointrefy_input.set_help_text(HelpText.POINTREFY)
        self.pointrefy_input.setMaxLength(10)

        self.pointrefy_input.focus.connect(self.on_help_focus)

        self.pointrefy_validator = QtGui.QDoubleValidator(-200, 200, 8, self.pointrefy_input)
        self.pointrefy_input.setText(str(Case.the().constants.pointref[1]))
        self.pointrefy_input.setValidator(self.pointrefy_validator)

        self.pointrefz_input = QtWidgets.QLineEdit()
        self.pointrefz_input = FocusableLineEdit()
        self.pointrefz_input.set_help_text(HelpText.POINTREFZ)
        self.pointrefz_input.setMaxLength(10)

        self.pointrefz_input.focus.connect(self.on_help_focus)

        self.pointrefz_validator = QtGui.QDoubleValidator(-200, 200, 8, self.pointrefz_input)
        self.pointrefz_input.setText(str(Case.the().constants.pointref[2]))
        self.pointrefz_input.setValidator(self.pointrefz_validator)

        self.pointref_label2 = QtWidgets.QLabel("metres")

        self.pointref_layout.addWidget(self.pointref_label)
        self.pointref_layout.addWidget(self.pointrefx_input)  # For X
        self.pointref_layout.addWidget(self.pointrefy_input)  # For Y
        self.pointref_layout.addWidget(self.pointrefz_input)  # For Z
        self.pointref_layout.addWidget(self.pointref_label2)

        # Lattice for boundaries layout and components
        self.lattice_layout = QtWidgets.QHBoxLayout()
        self.lattice_label = QtWidgets.QLabel(__("Lattice for Boundaries:"))
        self.lattice_input = QtWidgets.QComboBox()
        self.lattice_input.insertItems(0, [__("Lattice 1"), __("Lattice 2")])
        self.lattice_input.setCurrentIndex(Case.the().constants.lattice_bound - 1)

        self.lattice_layout.addWidget(self.lattice_label)
        self.lattice_layout.addWidget(self.lattice_input)
        self.lattice_layout.addStretch(1)

        # Lattice for fluids layout and components
        self.lattice2_layout = QtWidgets.QHBoxLayout()
        self.lattice2_label = QtWidgets.QLabel(__("Lattice for Fluids: "))
        self.lattice2_input = QtWidgets.QComboBox()
        self.lattice2_input.insertItems(0, [__("Lattice 1"), __("Lattice 2")])
        self.lattice2_input.setCurrentIndex(Case.the().constants.lattice_fluid - 1)

        self.lattice2_layout.addWidget(self.lattice2_label)
        self.lattice2_layout.addWidget(self.lattice2_input)
        self.lattice2_layout.addStretch(1)

        # Gravity
        self.gravity_layout = QtWidgets.QHBoxLayout()
        self.gravity_label = HoverableLabel(__("Gravity [X, Y, Z]:"))

        self.gravityx_input = QtWidgets.QLineEdit()
        self.gravityx_input = FocusableLineEdit()
        self.gravityx_input.set_help_text(HelpText.GRAVITYX)
        self.gravityx_input.setMaxLength(10)

        self.gravityx_input.focus.connect(self.on_help_focus)

        self.gravityx_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityx_input)
        self.gravityx_input.setText(str(Case.the().constants.gravity[0]))
        self.gravityx_input.setValidator(self.gravityx_validator)

        self.gravityy_input = QtWidgets.QLineEdit()
        self.gravityy_input = FocusableLineEdit()
        self.gravityy_input.set_help_text(HelpText.GRAVITYY)
        self.gravityy_input.setMaxLength(10)

        self.gravityy_input.focus.connect(self.on_help_focus)

        self.gravityy_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityy_input)
        self.gravityy_input.setText(str(Case.the().constants.gravity[1]))
        self.gravityy_input.setValidator(self.gravityy_validator)

        self.gravityz_input = QtWidgets.QLineEdit()
        self.gravityz_input = FocusableLineEdit()
        self.gravityz_input.set_help_text(HelpText.GRAVITYZ)
        self.gravityz_input.setMaxLength(10)

        self.gravityz_input.focus.connect(self.on_help_focus)

        self.gravityz_validator = QtGui.QDoubleValidator(-200, 200, 8, self.gravityz_input)
        self.gravityz_input.setText(str(Case.the().constants.gravity[2]))
        self.gravityz_input.setValidator(self.gravityz_validator)

        self.gravity_label2 = QtWidgets.QLabel("m/s<span style='vertical-align:super'>2</span>")

        self.gravity_layout.addWidget(self.gravity_label)
        self.gravity_layout.addWidget(self.gravityx_input)  # For X
        self.gravity_layout.addWidget(self.gravityy_input)  # For Y
        self.gravity_layout.addWidget(self.gravityz_input)  # For Z
        self.gravity_layout.addWidget(self.gravity_label2)

        # Reference density of the fluid: layout and components
        self.rhop0_layout = QtWidgets.QHBoxLayout()
        self.rhop0_label = QtWidgets.QLabel(__("Fluid reference density:"))

        self.rhop0_input = QtWidgets.QLineEdit()
        self.rhop0_input = FocusableLineEdit()
        self.rhop0_input.set_help_text(HelpText.RHOP0)
        self.rhop0_input.setMaxLength(10)

        self.rhop0_input.focus.connect(self.on_help_focus)

        self.rhop0_validator = QtGui.QDoubleValidator(0, 10000, 8, self.rhop0_input)
        self.rhop0_input.setText(str(Case.the().constants.rhop0))
        self.rhop0_input.setValidator(self.rhop0_validator)
        self.rhop0_label2 = QtWidgets.QLabel("kg/m<span style='vertical-align:super'>3<span>")

        self.rhop0_layout.addWidget(self.rhop0_label)
        self.rhop0_layout.addWidget(self.rhop0_input)
        self.rhop0_layout.addWidget(self.rhop0_label2)

        # Initial density gradient: layout and components
        self.rhopgradient_layout = QtWidgets.QHBoxLayout()
        self.rhopgradient_label = QtWidgets.QLabel(__("Initial density gradient:"))

        self.rhopgradient_input = QtWidgets.QLineEdit()
        self.rhopgradient_input = FocusableLineEdit()
        self.rhopgradient_input.set_help_text(HelpText.RHOPGRADIENT)
        self.rhopgradient_input.setMaxLength(1)

        self.rhopgradient_input.focus.connect(self.on_help_focus)

        self.rhopgradient_validator = QtGui.QIntValidator(0, 10000, self.rhopgradient_input)
        self.rhopgradient_input.setText(str(Case.the().constants.rhopgradient))
        self.rhopgradient_input.setValidator(self.rhopgradient_validator)

        self.rhopgradient_layout.addWidget(self.rhopgradient_label)
        self.rhopgradient_layout.addWidget(self.rhopgradient_input)

        # Maximum still water level to calc.  spdofsound using coefsound: layout and
        # components
        self.hswlauto_layout = QtWidgets.QHBoxLayout()
        self.hswlauto_chk = QtWidgets.QCheckBox(__("Auto HSWL"))
        if Case.the().constants.hswl_auto:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hswlauto_chk.toggled.connect(self.on_hswlauto_check)
        self.hswlauto_layout.addWidget(self.hswlauto_chk)

        self.hswl_layout = QtWidgets.QHBoxLayout()
        self.hswl_label = QtWidgets.QLabel(__("HSWL:"))
        self.hswl_input = QtWidgets.QLineEdit()
        self.hswl_input = FocusableLineEdit()
        self.hswl_input.set_help_text(HelpText.HSWL)
        self.hswl_input.setMaxLength(10)

        self.hswl_input.focus.connect(self.on_help_focus)

        self.hswl_validator = QtGui.QIntValidator(0, 10000, self.hswl_input)
        self.hswl_input.setText(str(Case.the().constants.hswl))
        self.hswl_input.setValidator(self.hswl_validator)
        self.hswl_label2 = QtWidgets.QLabel(__("metres"))

        self.hswl_layout.addWidget(self.hswl_label)
        self.hswl_layout.addWidget(self.hswl_input)
        self.hswl_layout.addWidget(self.hswl_label2)

        # Manually trigger check for the first time
        self.on_hswlauto_check()

        # gamma: layout and components
        self.gamma_layout = QtWidgets.QHBoxLayout()
        self.gamma_label = QtWidgets.QLabel(__("Gamma:"))
        self.gamma_input = QtWidgets.QLineEdit()
        self.gamma_input = FocusableLineEdit()
        self.gamma_input.set_help_text(HelpText.GAMMA)
        self.gamma_input.setMaxLength(3)

        self.gamma_input.focus.connect(self.on_help_focus)

        self.gamma_validator = QtGui.QDoubleValidator(0, 999, 8, self.gamma_input)
        self.gamma_input.setText(str(Case.the().constants.gamma))
        self.gamma_input.setValidator(self.gamma_validator)
        self.gamma_label2 = QtWidgets.QLabel("units")

        self.gamma_layout.addWidget(self.gamma_label)
        self.gamma_layout.addWidget(self.gamma_input)
        self.gamma_layout.addWidget(self.gamma_label2)

        # Speedsystem: layout and components
        self.speedsystemauto_layout = QtWidgets.QHBoxLayout()
        self.speedsystemauto_chk = QtWidgets.QCheckBox(__("Auto Speedsystem"))
        if Case.the().constants.speedsystem_auto:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsystemauto_chk.toggled.connect(self.on_speedsystemauto_check)
        self.speedsystemauto_layout.addWidget(self.speedsystemauto_chk)

        self.speedsystem_layout = QtWidgets.QHBoxLayout()
        self.speedsystem_label = QtWidgets.QLabel(__("Speedsystem:"))
        self.speedsystem_input = QtWidgets.QLineEdit()
        self.speedsystem_input = FocusableLineEdit()
        self.speedsystem_input.set_help_text(HelpText.SPEEDSYSTEM)
        self.speedsystem_input.setMaxLength(10)

        self.speedsystem_input.focus.connect(self.on_help_focus)

        self.speedsystem_validator = QtGui.QIntValidator(0, 10000, self.speedsystem_input)
        self.speedsystem_input.setText(str(Case.the().constants.speedsystem))
        self.speedsystem_input.setValidator(self.speedsystem_validator)
        self.speedsystem_label2 = QtWidgets.QLabel("m/s")

        self.speedsystem_layout.addWidget(self.speedsystem_label)
        self.speedsystem_layout.addWidget(self.speedsystem_input)
        self.speedsystem_layout.addWidget(self.speedsystem_label2)

        # Manually trigger check for the first time
        self.on_speedsystemauto_check()

        # coefsound: layout and components
        self.coefsound_layout = QtWidgets.QHBoxLayout()
        self.coefsound_label = QtWidgets.QLabel(__("Coefsound:"))
        self.coefsound_input = QtWidgets.QLineEdit()
        self.coefsound_input = FocusableLineEdit()
        self.coefsound_input.set_help_text(HelpText.COEFSOUND)
        self.coefsound_input.setMaxLength(3)

        self.coefsound_input.focus.connect(self.on_help_focus)

        self.coefsound_validator = QtGui.QDoubleValidator(0, 999, 8, self.coefsound_input)
        self.coefsound_input.setText(str(Case.the().constants.coefsound))
        self.coefsound_input.setValidator(self.coefsound_validator)
        self.coefsound_label2 = QtWidgets.QLabel("units")

        self.coefsound_layout.addWidget(self.coefsound_label)
        self.coefsound_layout.addWidget(self.coefsound_input)
        self.coefsound_layout.addWidget(self.coefsound_label2)

        # Speedsound: layout and components
        self.speedsoundauto_layout = QtWidgets.QHBoxLayout()
        self.speedsoundauto_chk = QtWidgets.QCheckBox(__("Auto Speedsound "))
        if Case.the().constants.speedsound_auto:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.speedsoundauto_chk.toggled.connect(self.on_speedsoundauto_check)
        self.speedsoundauto_layout.addWidget(self.speedsoundauto_chk)

        self.speedsound_layout = QtWidgets.QHBoxLayout()
        self.speedsound_label = QtWidgets.QLabel(__("Speedsound:"))
        self.speedsound_input = QtWidgets.QLineEdit()
        self.speedsound_input = FocusableLineEdit()
        self.speedsound_input.set_help_text(HelpText.SPEEDSOUND)
        self.speedsound_input.setMaxLength(10)

        self.speedsound_input.focus.connect(self.on_help_focus)

        self.speedsound_validator = QtGui.QIntValidator(0, 10000, self.speedsound_input)
        self.speedsound_input.setText(str(Case.the().constants.speedsound))
        self.speedsound_input.setValidator(self.speedsound_validator)
        self.speedsound_label2 = QtWidgets.QLabel("m/s")

        self.speedsound_layout.addWidget(self.speedsound_label)
        self.speedsound_layout.addWidget(self.speedsound_input)
        self.speedsound_layout.addWidget(self.speedsound_label2)

        # Manually trigger check for the first time
        self.on_speedsoundauto_check()

        # coefh: layout and components
        self.coefh_layout = QtWidgets.QHBoxLayout()
        self.coefh_label = QtWidgets.QLabel(__("CoefH:"))
        self.coefh_input = QtWidgets.QLineEdit()
        self.coefh_input = FocusableLineEdit()
        self.coefh_input.set_help_text(HelpText.COEFH)
        self.coefh_input.setMaxLength(10)

        self.coefh_input.focus.connect(self.on_help_focus)

        self.coefh_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.coefh_input.setText(str(Case.the().constants.coefh))
        self.coefh_input.setValidator(self.coefh_validator)
        self.coefh_label2 = QtWidgets.QLabel(__("units"))

        self.coefh_layout.addWidget(self.coefh_label)
        self.coefh_layout.addWidget(self.coefh_input)
        self.coefh_layout.addWidget(self.coefh_label2)

        # cflnumber: layout and components
        self.cflnumber_layout = QtWidgets.QHBoxLayout()
        self.cflnumber_label = QtWidgets.QLabel(__("cflnumber: "))
        self.cflnumber_input = QtWidgets.QLineEdit()
        self.cflnumber_input = FocusableLineEdit()
        self.cflnumber_input.set_help_text(HelpText.CFLNUMBER)
        self.cflnumber_input.setMaxLength(10)

        self.cflnumber_input.focus.connect(self.on_help_focus)

        self.cflnumber_validator = QtGui.QDoubleValidator(0, 10, 8, self.coefh_input)
        self.cflnumber_input.setText(str(Case.the().constants.cflnumber))
        self.cflnumber_input.setValidator(self.cflnumber_validator)
        self.cflnumber_label2 = QtWidgets.QLabel(__("units"))

        self.cflnumber_layout.addWidget(self.cflnumber_label)
        self.cflnumber_layout.addWidget(self.cflnumber_input)
        self.cflnumber_layout.addWidget(self.cflnumber_label2)

        # h: layout and components
        self.hauto_layout = QtWidgets.QHBoxLayout()
        self.hauto_chk = QtWidgets.QCheckBox(__("Auto Smoothing length"))
        if Case.the().constants.h_auto:
            self.hauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.hauto_chk.toggled.connect(self.on_hauto_check)
        self.hauto_layout.addWidget(self.hauto_chk)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_label = QtWidgets.QLabel(__("Smoothing Length:"))
        self.h_input = QtWidgets.QLineEdit()
        self.h_input = FocusableLineEdit()
        self.h_input.set_help_text(__("Smoothing Length"))
        self.h_input.setMaxLength(10)

        self.h_input.focus.connect(self.on_help_focus)

        self.h_validator = QtGui.QDoubleValidator(0, 100, 8, self.h_input)
        self.h_input.setText(str(Case.the().constants.h))
        self.h_input.setValidator(self.h_validator)
        self.h_label2 = QtWidgets.QLabel(__("metres"))

        self.h_layout.addWidget(self.h_label)
        self.h_layout.addWidget(self.h_input)
        self.h_layout.addWidget(self.h_label2)

        # Manually trigger check for the first time
        self.on_hauto_check()

        # b: layout and components
        self.bauto_layout = QtWidgets.QHBoxLayout()
        self.bauto_chk = QtWidgets.QCheckBox(__("Auto b constant for EOS"))
        if Case.the().constants.b_auto:
            self.bauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.bauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.bauto_chk.toggled.connect(self.on_bauto_check)
        self.bauto_layout.addWidget(self.bauto_chk)

        self.b_layout = QtWidgets.QHBoxLayout()
        self.b_label = QtWidgets.QLabel(__("B constant:"))
        self.b_input = QtWidgets.QLineEdit()
        self.b_input = FocusableLineEdit()
        self.b_input.set_help_text(__("B constant"))
        self.b_input.setMaxLength(10)

        self.b_input.focus.connect(self.on_help_focus)

        self.b_validator = QtGui.QDoubleValidator(0, 100, 8, self.b_input)
        self.b_input.setText(str(Case.the().constants.b))
        self.b_input.setValidator(self.b_validator)
        self.b_label2 = QtWidgets.QLabel(__("Pascal"))

        self.b_layout.addWidget(self.b_label)
        self.b_layout.addWidget(self.b_input)
        self.b_layout.addWidget(self.b_label2)

        # Manually trigger check for the first time
        self.on_bauto_check()

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Button layout definition
        self.cw_button_layout = QtWidgets.QHBoxLayout()
        self.cw_button_layout.addStretch(1)
        self.cw_button_layout.addWidget(self.ok_button)
        self.cw_button_layout.addWidget(self.cancel_button)

        # START Main layout definition and composition.
        self.cw_main_layout_scroll = QtWidgets.QScrollArea()
        self.cw_main_layout_scroll.setWidgetResizable(True)
        self.cw_main_layout_scroll_widget = QtWidgets.QWidget()
        self.cw_main_layout = QtWidgets.QVBoxLayout()

        # Lattice was removed on 0.3Beta - 1 of June
        # self.cw_main_layout.addLayout(self.lattice_layout)
        # self.cw_main_layout.addLayout(self.lattice2_layout)
        self.cw_main_layout.addLayout(self.pointref_layout)
        self.cw_main_layout.addLayout(self.gravity_layout)
        self.cw_main_layout.addLayout(self.rhop0_layout)
        self.cw_main_layout.addLayout(self.rhopgradient_layout)
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

        self.constants_window_layout = QtWidgets.QVBoxLayout()
        self.constants_window_layout.addWidget(self.cw_main_layout_scroll)
        self.constants_window_layout.addWidget(self.help_label)
        self.constants_window_layout.addLayout(self.cw_button_layout)

        self.setLayout(self.constants_window_layout)
        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)

        self.exec_()

    def on_hswlauto_check(self):
        """ Reacts to the user selecting auto HSWL. """
        if self.hswlauto_chk.isChecked():
            self.hswl_input.setEnabled(False)
        else:
            self.hswl_input.setEnabled(True)

    def on_help_focus(self, help_text):
        """ Reacts to focus signal setting a help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))

    def on_speedsystemauto_check(self):
        """ Reacts to the speedsystemauto checkbox enabling/disabling its input. """
        if self.speedsystemauto_chk.isChecked():
            self.speedsystem_input.setEnabled(False)
        else:
            self.speedsystem_input.setEnabled(True)

    def on_speedsoundauto_check(self):
        """ Reacts to the speedsoundauto checkbos enabling/disabling its inputs. """
        if self.speedsoundauto_chk.isChecked():
            self.speedsound_input.setEnabled(False)
        else:
            self.speedsound_input.setEnabled(True)

    def on_hauto_check(self):
        """ Reacts to the hauto checkbox being pressed enabling/disabling its inputs. """
        if self.hauto_chk.isChecked():
            self.h_input.setEnabled(False)
        else:
            self.h_input.setEnabled(True)

    def on_bauto_check(self):
        """ Reacts to the bauto checkbox being pressed enabling/disabling its inputs. """
        if self.bauto_chk.isChecked():
            self.b_input.setEnabled(False)
        else:
            self.b_input.setEnabled(True)

    def on_ok(self):
        """ Applies the current dialog data onto the main data structure. """
        Case.the().constants.lattice_bound = self.lattice_input.currentIndex() + 1
        Case.the().constants.lattice_fluid = self.lattice2_input.currentIndex() + 1
        Case.the().constants.pointref = [float(self.pointrefx_input.text()), float(self.pointrefy_input.text()), float(self.pointrefz_input.text())]
        Case.the().constants.gravity = [float(self.gravityx_input.text()), float(self.gravityy_input.text()), float(self.gravityz_input.text())]
        Case.the().constants.rhop0 = float(self.rhop0_input.text())
        Case.the().constants.rhopgradient = float(self.rhopgradient_input.text())
        Case.the().constants.hswl = float(self.hswl_input.text())
        Case.the().constants.hswl_auto = self.hswlauto_chk.isChecked()
        Case.the().constants.gamma = float(self.gamma_input.text())
        Case.the().constants.speedsystem = float(self.speedsystem_input.text())
        Case.the().constants.speedsystem_auto = self.speedsystemauto_chk.isChecked()
        Case.the().constants.coefsound = float(self.coefsound_input.text())
        Case.the().constants.speedsound = float(self.speedsound_input.text())
        Case.the().constants.speedsound_auto = self.speedsoundauto_chk.isChecked()
        Case.the().constants.coefh = float(self.coefh_input.text())
        Case.the().constants.cflnumber = float(self.cflnumber_input.text())
        Case.the().constants.h = float(self.h_input.text())
        Case.the().constants.h_auto = self.hauto_chk.isChecked()
        Case.the().constants.b = float(self.b_input.text())
        Case.the().constants.b_auto = self.bauto_chk.isChecked()
        log("Constants changed")
        self.accept()

    def on_cancel(self):
        """ Closes the dialog rejecting it. """
        log("Constants not changed")
        self.reject()
