#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Constants Configuration Dialog."""


from PySide2 import QtCore, QtWidgets
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.enums import HelpText
from mod.tools.stdout_tools import log, debug
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.acceleration_input import AccelerationInput
from mod.widgets.custom_widgets.density_input import DensityInput
from mod.widgets.custom_widgets.focusable_combo_box import FocusableComboBox
from mod.widgets.custom_widgets.pressure_input import PressureInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.velocity_input import VelocityInput


class ConstantsDialog(QtWidgets.QDialog):
    """ A window to define and configure the constants of the case for later execution
        in the DualSPHysics simulator. """

    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 700
    MINIMUM_HEIGHT = 500

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Constants definition"))
        self.help_label: QtWidgets.QLabel = QtWidgets.QLabel(self.LABEL_DEFAULT_TEXT)

        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))

        # Pointref
        self.pointref_layout = QtWidgets.QHBoxLayout()
        self.pointref_label = QtWidgets.QLabel(__("Pointref [X, Y, Z]:"))
        #X
        self.pointrefx_input = SizeInput()
        self.pointrefx_input.set_help_text(HelpText.POINTREFX)
        self.pointrefx_input.focus.connect(self.on_help_focus)
        # Y
        self.pointrefy_input = SizeInput()
        self.pointrefy_input.set_help_text(HelpText.POINTREFY)
        self.pointrefy_input.focus.connect(self.on_help_focus)
        # Z
        self.pointrefz_input = SizeInput()
        self.pointrefz_input.set_help_text(HelpText.POINTREFZ)
        self.pointrefz_input.focus.connect(self.on_help_focus)

        if Case.the().constants.setpointref_hdp:
            #self.pointrefx_input.setValue(Case.the().dp/2)
            self.pointrefx_input.setEnabled(False)
            #self.pointrefy_input.setValue(Case.the().dp / 2)
            self.pointrefy_input.setEnabled(False)
            #self.pointrefz_input.setValue(Case.the().dp / 2)
            self.pointrefz_input.setEnabled(False)
        else:
            self.pointrefx_input.setValue(float(Case.the().constants.pointref[0]))
            self.pointrefx_input.setEnabled(True)
            self.pointrefy_input.setValue(float(Case.the().constants.pointref[1]))
            self.pointrefy_input.setEnabled(True)
            self.pointrefz_input.setValue(float(Case.the().constants.pointref[2]))
            self.pointrefz_input.setEnabled(True)

        self.pointref_layout.addWidget(self.pointref_label)
        self.pointref_layout.addWidget(self.pointrefx_input)  # For X
        self.pointref_layout.addWidget(self.pointrefy_input)  # For Y
        self.pointref_layout.addWidget(self.pointrefz_input)  # For Z

        self.pointref_hdp_layout = QtWidgets.QHBoxLayout()
        self.pointref_hdp_chk = QtWidgets.QCheckBox(__("Set pointref to Dp/2"))
        if Case.the().constants.setpointref_hdp:
            self.pointref_hdp_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.pointref_hdp_chk.setCheckState(QtCore.Qt.Unchecked)

        self.pointref_hdp_chk.toggled.connect(self.on_pointref_hdp_check)
        self.pointref_hdp_layout.addWidget(self.pointref_hdp_chk)

        # Gravity
        self.gravity_layout = QtWidgets.QHBoxLayout()
        self.gravity_label = QtWidgets.QLabel(__("Gravity [X, Y, Z]:"))
        #X
        self.gravityx_input = AccelerationInput()
        self.gravityx_input.set_help_text(HelpText.GRAVITYX)
        self.gravityx_input.focus.connect(self.on_help_focus)
        self.gravityx_input.setValue(Case.the().constants.gravity[0])

        self.gravityy_input = AccelerationInput()
        self.gravityy_input.set_help_text(HelpText.GRAVITYY)
        self.gravityy_input.focus.connect(self.on_help_focus)
        self.gravityy_input.setValue(Case.the().constants.gravity[1])

        self.gravityz_input = AccelerationInput()
        self.gravityz_input.set_help_text(HelpText.GRAVITYZ)
        self.gravityz_input.focus.connect(self.on_help_focus)
        self.gravityz_input.setValue(Case.the().constants.gravity[2])


        self.gravity_layout.addWidget(self.gravity_label)
        self.gravity_layout.addWidget(self.gravityx_input)  # For X
        self.gravity_layout.addWidget(self.gravityy_input)  # For Y
        self.gravity_layout.addWidget(self.gravityz_input)  # For Z


        # Reference density of the fluid: layout and components
        self.rhop0_layout = QtWidgets.QHBoxLayout()
        self.rhop0_label = QtWidgets.QLabel(__("Fluid reference density:"))

        self.rhop0_input =  DensityInput()
        self.rhop0_input.set_help_text(HelpText.RHOP0)
        self.rhop0_input.focus.connect(self.on_help_focus)
        self.rhop0_input.setValue(Case.the().constants.rhop0)

        self.rhop0_layout.addWidget(self.rhop0_label)
        self.rhop0_layout.addWidget(self.rhop0_input)

        # Initial density gradient: layout and components
        self.rhopgradient_layout = QtWidgets.QHBoxLayout()
        self.rhopgradient_label = QtWidgets.QLabel(__("Initial density gradient:"))

        self.rhopgradient_combo = FocusableComboBox()
        self.rhopgradient_combo.set_help_text(HelpText.RHOPGRADIENT)
        self.rhopgradient_combo.focus.connect(self.on_help_focus)
        self.rhopgradient_combo.addItems(['1. Reference density of fluid','2. Water column','3. Max water height '])
        self.rhopgradient_combo.setCurrentIndex(Case.the().constants.rhopgradient-1)

        self.rhopgradient_layout.addWidget(self.rhopgradient_label)
        self.rhopgradient_layout.addWidget(self.rhopgradient_combo)

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
        self.hswl_input = SizeInput()
        self.hswl_input.set_help_text(HelpText.HSWL)
        self.hswl_input.focus.connect(self.on_help_focus)
        self.hswl_input.setValue(Case.the().constants.hswl)

        self.hswl_layout.addWidget(self.hswl_label)
        self.hswl_layout.addWidget(self.hswl_input)
        # Manually trigger check for the first time
        self.on_hswlauto_check()

        # gamma: layout and components
        self.gamma_layout = QtWidgets.QHBoxLayout()
        self.gamma_label = QtWidgets.QLabel(__("Gamma:"))
        self.gamma_input = ValueInput(min_val=0,max_val=999)
        self.gamma_input.set_help_text(HelpText.GAMMA)
        self.gamma_input.focus.connect(self.on_help_focus)
        self.gamma_input.setValue(Case.the().constants.gamma)

        self.gamma_layout.addWidget(self.gamma_label)
        self.gamma_layout.addWidget(self.gamma_input)

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
        
        self.speedsystem_input = VelocityInput()
        self.speedsystem_input.set_help_text(HelpText.SPEEDSYSTEM)
        self.speedsystem_input.focus.connect(self.on_help_focus)
        self.speedsystem_input.setValue(Case.the().constants.speedsystem)
        # Add to layout
        self.speedsystem_layout.addWidget(self.speedsystem_label)
        self.speedsystem_layout.addWidget(self.speedsystem_input)
        # Manually trigger check for the first time
        self.on_speedsystemauto_check()

        # coefsound: layout and components
        self.coefsound_layout = QtWidgets.QHBoxLayout()
        self.coefsound_label = QtWidgets.QLabel(__("Coefsound:"))
        self.coefsound_input = ValueInput(min_val=0,max_val=999)
        self.coefsound_input.set_help_text(HelpText.COEFSOUND)
        self.coefsound_input.focus.connect(self.on_help_focus)
        self.coefsound_input.setValue(Case.the().constants.coefsound)
        #Add to layout
        self.coefsound_layout.addWidget(self.coefsound_label)
        self.coefsound_layout.addWidget(self.coefsound_input)

        # Speedsoundauto: layout and components
        self.speedsoundauto_layout = QtWidgets.QHBoxLayout()
        self.speedsoundauto_chk = QtWidgets.QCheckBox(__("Auto Speedsound "))
        if Case.the().constants.speedsound_auto:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)
        self.speedsoundauto_chk.toggled.connect(self.on_speedsoundauto_check)
        self.speedsoundauto_layout.addWidget(self.speedsoundauto_chk)

        # Speedsoundo: layout and components
        self.speedsound_layout = QtWidgets.QHBoxLayout()
        self.speedsound_label = QtWidgets.QLabel(__("Speedsound:"))
        self.speedsound_input = VelocityInput()
        self.speedsound_input.set_help_text(HelpText.SPEEDSOUND)
        self.speedsound_input.focus.connect(self.on_help_focus)
        self.speedsound_input.setValue(Case.the().constants.speedsound)
        #Add to layout
        self.speedsound_layout.addWidget(self.speedsound_label)
        self.speedsound_layout.addWidget(self.speedsound_input)
        # Manually trigger check for the first time
        self.on_speedsoundauto_check()

        # coefh: layout and components
        self.coefh_layout = QtWidgets.QHBoxLayout()
        self.coefh_hdp_combo = QtWidgets.QComboBox()
        self.coefh_hdp_combo.addItems(['coefh','hdp'])
        self.coefh_hdp_combo.setCurrentIndex(0 if Case.the().constants.use_hdp==False else 1)
        self.coefh_input = ValueInput(min_val=0,max_val=10)
        self.coefh_input.set_help_text(HelpText.COEFH)
        self.coefh_input.focus.connect(self.on_help_focus)
        self.coefh_input.setValue(Case.the().constants.coefh if Case.the().constants.use_hdp==False else Case.the().constants.hdp)
        # Add to layout
        self.coefh_layout.addWidget(self.coefh_hdp_combo)
        self.coefh_layout.addWidget(self.coefh_input)

        # cflnumber: layout and components
        self.cflnumber_layout = QtWidgets.QHBoxLayout()
        self.cflnumber_label = QtWidgets.QLabel(__("cflnumber: "))
        self.cflnumber_input = ValueInput(min_val=0,max_val=10)
        self.cflnumber_input.set_help_text(HelpText.CFLNUMBER)
        self.cflnumber_input.focus.connect(self.on_help_focus)
        self.cflnumber_input.setValue(Case.the().constants.cflnumber)
        #Add to layout
        self.cflnumber_layout.addWidget(self.cflnumber_label)
        self.cflnumber_layout.addWidget(self.cflnumber_input)

        # h auto: layout and components
        self.hauto_layout = QtWidgets.QHBoxLayout()
        self.hauto_chk = QtWidgets.QCheckBox(__("Auto Smoothing length"))
        if Case.the().constants.h_auto:
            self.hauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.hauto_chk.setCheckState(QtCore.Qt.Unchecked)
        #Add to layout
        self.hauto_chk.toggled.connect(self.on_hauto_check)
        self.hauto_layout.addWidget(self.hauto_chk)

        # h : layout and components
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_label = QtWidgets.QLabel(__("Smoothing Length:"))
        self.h_input =  SizeInput()
        self.h_input.set_help_text(__("Smoothing Length"))
        self.h_input.focus.connect(self.on_help_focus)
        self.h_input.setValue(Case.the().constants.h)
        #Add to layout
        self.h_layout.addWidget(self.h_label)
        self.h_layout.addWidget(self.h_input)
        # Manually trigger check for the first time
        self.on_hauto_check()

        # auto b: layout and components
        self.bauto_layout = QtWidgets.QHBoxLayout()
        self.bauto_chk = QtWidgets.QCheckBox(__("Auto b constant for EOS"))
        if Case.the().constants.b_auto:
            self.bauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.bauto_chk.setCheckState(QtCore.Qt.Unchecked)
        # Add to layout
        self.bauto_chk.toggled.connect(self.on_bauto_check)
        self.bauto_layout.addWidget(self.bauto_chk)
        # b: layout and components
        self.b_layout = QtWidgets.QHBoxLayout()
        self.b_label = QtWidgets.QLabel(__("B constant:"))
        self.b_input = PressureInput()
        self.b_input.set_help_text(__("B constant"))

        self.b_input.focus.connect(self.on_help_focus)
        self.b_input.setValue(Case.the().constants.b)
        #Add to layout
        self.b_layout.addWidget(self.b_label)
        self.b_layout.addWidget(self.b_input)
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

        self.full_layout_list=[
             self.pointref_layout ,
             self.pointref_hdp_layout ,
             self.gravity_layout ,
             self.rhop0_layout ,
             self.rhopgradient_layout ,
             self.hswlauto_layout ,
             self.hswl_layout ,
             self.gamma_layout ,
             self.speedsystemauto_layout ,
             self.speedsystem_layout ,
             self.coefsound_layout ,
             self.speedsoundauto_layout ,
             self.speedsound_layout ,
             self.coefh_layout ,
             self.cflnumber_layout ,
             self.hauto_layout ,
             self.h_layout ,
             self.bauto_layout ,
             self.b_layout
        ]

        self.basic_layout_list = [
            self.pointref_layout,
            self.pointref_hdp_layout,
            self.gravity_layout,
            self.rhop0_layout,
            self.rhopgradient_layout,
            self.hswlauto_layout,
            self.hswl_layout,
            self.gamma_layout,
            self.speedsystemauto_layout,
            self.speedsystem_layout,
            self.coefsound_layout,
            self.speedsoundauto_layout,
            self.speedsound_layout,
            self.coefh_layout,
            self.cflnumber_layout
        ]
        if ApplicationSettings.the().basic_visualization :
            self.layoutlist=self.basic_layout_list
        else:
            self.layoutlist=self.full_layout_list
        for layout in self.layoutlist:
            self.cw_main_layout.addLayout(layout)

        self.cw_main_layout.addStretch(1)

        self.cw_main_layout_scroll_widget.setLayout(self.cw_main_layout)
        self.cw_main_layout_scroll.setWidget(self.cw_main_layout_scroll_widget)
        self.cw_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.constants_window_layout = QtWidgets.QVBoxLayout()
        self.constants_window_layout.addWidget(self.cw_main_layout_scroll)
        self.constants_window_layout.addWidget(self.help_label)
        self.constants_window_layout.addLayout(self.cw_button_layout)

        self.setLayout(self.constants_window_layout)
        self.setFixedWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)

    def on_pointref_hdp_check(self):
        """ Reacts to the user selecting set pointref to Dp/2. """
        if self.pointref_hdp_chk.isChecked():
            self.pointrefx_input.setEnabled(False)
            self.pointrefy_input.setEnabled(False)
            self.pointrefz_input.setEnabled(False)
        else:
            self.pointrefx_input.setValue(Case.the().constants.pointref[0])
            self.pointrefx_input.setEnabled(True)
            self.pointrefy_input.setValue(Case.the().constants.pointref[1])
            self.pointrefy_input.setEnabled(True)
            self.pointrefz_input.setValue(Case.the().constants.pointref[2])
            self.pointrefz_input.setEnabled(True)

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
     #   Case.the().constants.lattice_bound = self.lattice_input.currentIndex() + 1
     #   Case.the().constants.lattice_fluid = self.lattice2_input.currentIndex() + 1
        Case.the().constants.pointref = [self.pointrefx_input.value(),self.pointrefy_input.value(),self.pointrefz_input.value()]
        Case.the().constants.setpointref_hdp=self.pointref_hdp_chk.isChecked()
        Case.the().constants.gravity = [self.gravityx_input.value(),self.gravityy_input.value(),self.gravityz_input.value()]
        Case.the().constants.rhop0 = self.rhop0_input.value()
        Case.the().constants.rhopgradient = self.rhopgradient_combo.currentIndex() + 1
        Case.the().constants.hswl = self.hswl_input.value()
        Case.the().constants.hswl_auto = self.hswlauto_chk.isChecked()
        Case.the().constants.gamma = self.gamma_input.value()
        Case.the().constants.speedsystem = self.speedsystem_input.value()
        Case.the().constants.speedsystem_auto = self.speedsystemauto_chk.isChecked()
        Case.the().constants.coefsound = self.coefsound_input.value()
        Case.the().constants.speedsound = self.speedsound_input.value()
        Case.the().constants.speedsound_auto = self.speedsoundauto_chk.isChecked()
        use_hdp = self.coefh_hdp_combo.currentText()=="hdp"
        Case.the().constants.use_hdp = use_hdp
        if use_hdp:
            Case.the().constants.hdp = self.coefh_input.value()
            Case.the().constants.h_constant_name = "hdp"
        else:
            Case.the().constants.coefh = self.coefh_input.value()
            Case.the().constants.h_constant_name = "coefh"
        Case.the().constants.h_constant = self.coefh_input.value()
        Case.the().constants.cflnumber = self.cflnumber_input.value()
        Case.the().constants.h = self.h_input.value()
        Case.the().constants.h_auto = self.hauto_chk.isChecked()
        Case.the().constants.b = self.b_input.value()
        Case.the().constants.b_auto = self.bauto_chk.isChecked()
        log("Constants changed")
        self.accept()

    def on_cancel(self):
        """ Closes the dialog rejecting it. """
        log("Constants not changed")
        self.reject()
