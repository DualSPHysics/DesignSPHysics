#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Execution Parameters Configuration Dialog."""

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import log
from mod.enums import HelpText

from mod.widgets.focusable_combo_box import FocusableComboBox
from mod.widgets.focusable_line_edit import FocusableLineEdit

from mod.dataobjects.case import Case
from mod.dataobjects.periodicity import Periodicity
from mod.dataobjects.periodicity_info import PeriodicityInfo
from mod.dataobjects.sd_position_property import SDPositionProperty


class ExecutionParametersDialog(QtGui.QDialog):
    """Defines the execution parameters window.
    Modifies the data dictionary passed as parameter."""

    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Creates a dialog and 2 main buttons
        self.setWindowTitle("DSPH Execution Parameters")
        self.help_label = QtGui.QLabel(self.LABEL_DEFAULT_TEXT)
        self.ok_button = QtGui.QPushButton("Ok")
        self.cancel_button = QtGui.QPushButton("Cancel")

        # Precision in particle interaction
        self.posdouble_layout = QtGui.QHBoxLayout()
        self.posdouble_label = QtGui.QLabel("Precision in particle interaction: ")
        self.posdouble_input = FocusableComboBox()
        self.posdouble_input.insertItems(0, ["Simple", "Double", "Uses and saves double"])
        self.posdouble_input.setCurrentIndex(int(Case.the().execution_parameters.posdouble))
        self.posdouble_input.set_help_text(HelpText.POSDOUBLE)

        self.posdouble_input.focus.connect(self.on_help_focus)

        self.posdouble_layout.addWidget(self.posdouble_label)
        self.posdouble_layout.addWidget(self.posdouble_input)
        self.posdouble_layout.addStretch(1)

        self.stepalgorithm_layout = QtGui.QHBoxLayout()
        self.stepalgorithm_label = QtGui.QLabel("Step Algorithm: ")
        self.stepalgorithm_input = FocusableComboBox()
        self.stepalgorithm_input.insertItems(0, ["Verlet", "Symplectic"])
        self.stepalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.stepalgorithm) - 1)
        self.stepalgorithm_input.set_help_text(HelpText.STEPALGORITHM)

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
        self.verletsteps_input.set_help_text(HelpText.VERLETSTEPS)
        self.verletsteps_input.setMaxLength(4)

        self.verletsteps_input.focus.connect(self.on_help_focus)

        self.verletsteps_validator = QtGui.QIntValidator(0, 9999, self.verletsteps_input)
        self.verletsteps_input.setText(str(Case.the().execution_parameters.verletsteps))
        self.verletsteps_input.setValidator(self.verletsteps_validator)

        self.verletsteps_layout.addWidget(self.verletsteps_label)
        self.verletsteps_layout.addWidget(self.verletsteps_input)

        # Enable/Disable fields depending on selection
        self.on_step_change(self.stepalgorithm_input.currentIndex)

        # Kernel
        self.kernel_layout = QtGui.QHBoxLayout()
        self.kernel_label = QtGui.QLabel("Interaction kernel: ")
        self.kernel_input = FocusableComboBox()
        self.kernel_input.insertItems(0, ["Cubic spline", "Wendland"])
        self.kernel_input.set_help_text(HelpText.KERNEL)
        self.kernel_input.setCurrentIndex(int(Case.the().execution_parameters.kernel) - 1)

        self.kernel_input.focus.connect(self.on_help_focus)

        self.kernel_layout.addWidget(self.kernel_label)
        self.kernel_layout.addWidget(self.kernel_input)
        self.kernel_layout.addStretch(1)

        # Viscosity formulation
        self.viscotreatment_layout = QtGui.QHBoxLayout()
        self.viscotreatment_label = QtGui.QLabel("Viscosity Formulation: ")
        self.viscotreatment_input = FocusableComboBox()
        self.viscotreatment_input.insertItems(0, ["Artificial", "Laminar + SPS"])
        self.viscotreatment_input.set_help_text(HelpText.VISCOTREATMENT)
        self.viscotreatment_input.setCurrentIndex(int(Case.the().execution_parameters.viscotreatment) - 1)

        self.viscotreatment_input.focus.connect(self.on_help_focus)

        self.viscotreatment_layout.addWidget(self.viscotreatment_label)
        self.viscotreatment_layout.addWidget(self.viscotreatment_input)
        self.viscotreatment_layout.addStretch(1)

        # Viscosity value
        self.visco_layout = QtGui.QHBoxLayout()
        self.visco_label = QtGui.QLabel("Viscosity value: ")
        self.visco_input = FocusableLineEdit()
        self.visco_input.set_help_text(HelpText.VISCO)
        self.visco_input.setMaxLength(10)

        self.visco_input.focus.connect(self.on_help_focus)

        self.visco_units_label = QtGui.QLabel("")
        self.visco_layout.addWidget(self.visco_label)
        self.visco_layout.addWidget(self.visco_input)
        self.visco_layout.addWidget(self.visco_units_label)

        self.on_viscotreatment_change(int(Case.the().execution_parameters.viscotreatment) - 1)
        self.visco_input.setText(str(Case.the().execution_parameters.visco))

        self.viscotreatment_input.currentIndexChanged.connect(self.on_viscotreatment_change)

        # Viscosity with boundary
        self.viscoboundfactor_layout = QtGui.QHBoxLayout()
        self.viscoboundfactor_label = QtGui.QLabel("Viscosity factor with boundary: ")
        self.viscoboundfactor_input = FocusableLineEdit()

        self.viscoboundfactor_input.set_help_text(HelpText.VISCOBOUNDFACTOR)

        self.viscoboundfactor_input.setMaxLength(10)

        self.viscoboundfactor_input.focus.connect(self.on_help_focus)

        self.viscoboundfactor_input.setText(str(Case.the().execution_parameters.viscoboundfactor))

        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_label)
        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_input)

        self.densitydt_type_layout = QtGui.QHBoxLayout()
        self.densitydt_type_label = QtGui.QLabel("Density Diffusion Term: ")
        self.densitydt_type_input = QtGui.QComboBox()
        self.densitydt_type_input.insertItems(0, ['None', 'Molteni', 'Fourtakas', 'Fourtakas (Full)'])
        self.densitydt_type_input.setCurrentIndex(Case.the().execution_parameters.densitydt_type)
        self.densitydt_type_input.currentIndexChanged.connect(self.on_densitydt_type_change)

        self.densitydt_type_layout.addWidget(self.densitydt_type_label)
        self.densitydt_type_layout.addWidget(self.densitydt_type_input)
        self.densitydt_type_layout.addStretch(1)

        # densitydt value
        self.densitydt_layout = QtGui.QHBoxLayout()
        self.densitydt_label = QtGui.QLabel("DDT value: ")
        self.densitydt_input = FocusableLineEdit()
        self.densitydt_input.set_help_text(HelpText.DENSITYDT)
        self.densitydt_input.setMaxLength(10)

        self.densitydt_input.focus.connect(self.on_help_focus)

        self.densitydt_input.setText(str(Case.the().execution_parameters.densitydt_value))
        self.densitydt_layout.addWidget(self.densitydt_label)
        self.densitydt_layout.addWidget(self.densitydt_input)

        if self.densitydt_type_input.currentIndex() == 0:
            self.densitydt_input.setEnabled(False)
        else:
            self.densitydt_input.setEnabled(True)

        self.shifting_layout = QtGui.QHBoxLayout()
        self.shifting_label = QtGui.QLabel("Shifting mode: ")
        self.shifting_input = FocusableComboBox()
        self.shifting_input.insertItems(
            0, ["None", "Ignore bound", "Ignore fixed", "Full"])
        self.shifting_input.set_help_text(HelpText.SHIFTING)

        self.shifting_input.focus.connect(self.on_help_focus)

        self.shifting_input.setCurrentIndex(int(Case.the().execution_parameters.shifting))
        self.shifting_input.currentIndexChanged.connect(self.on_shifting_change)

        self.shifting_layout.addWidget(self.shifting_label)
        self.shifting_layout.addWidget(self.shifting_input)
        self.shifting_layout.addStretch(1)

        # Coefficient for shifting
        self.shiftcoef_layout = QtGui.QHBoxLayout()
        self.shiftcoef_label = QtGui.QLabel("Coefficient for shifting: ")
        self.shiftcoef_input = FocusableLineEdit()
        self.shiftcoef_input.set_help_text(HelpText.SHIFTINGCOEF)
        self.shiftcoef_input.setMaxLength(10)

        self.shiftcoef_input.focus.connect(self.on_help_focus)

        self.shiftcoef_input.setText(str(Case.the().execution_parameters.shiftcoef))
        self.shiftcoef_layout.addWidget(self.shiftcoef_label)
        self.shiftcoef_layout.addWidget(self.shiftcoef_input)

        # Free surface detection threshold
        self.shifttfs_layout = QtGui.QHBoxLayout()
        self.shifttfs_label = QtGui.QLabel("Free surface detection threshold: ")
        self.shifttfs_input = FocusableLineEdit()
        self.shifttfs_input.set_help_text(HelpText.SHIFTINGTFS)
        self.shifttfs_input.setMaxLength(10)

        self.shifttfs_input.focus.connect(self.on_help_focus)

        self.shifttfs_input.setText(str(Case.the().execution_parameters.shifttfs))
        self.shifttfs_layout.addWidget(self.shifttfs_label)
        self.shifttfs_layout.addWidget(self.shifttfs_input)

        # Enable/Disable fields depending on Shifting mode on window creation.
        self.on_shifting_change(self.shifting_input.currentIndex())

        # Rigid algorithm
        self.rigidalgorithm_layout = QtGui.QHBoxLayout()
        self.rigidalgorithm_label = QtGui.QLabel("Solid-solid interaction: ")
        self.rigidalgorithm_input = FocusableComboBox()
        self.rigidalgorithm_input.insertItems(0, ["SPH", "DEM", "CHRONO"])
        self.rigidalgorithm_input.set_help_text(HelpText.RIGIDALGORITHM)
        self.rigidalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.rigidalgorithm) - 1)

        self.rigidalgorithm_input.focus.connect(self.on_help_focus)

        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_label)
        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_input)
        self.rigidalgorithm_layout.addStretch(1)

        # Sim start freeze time
        self.ftpause_layout = QtGui.QHBoxLayout()
        self.ftpause_label = QtGui.QLabel("Floating freeze time: ")
        self.ftpause_input = FocusableLineEdit()
        self.ftpause_input.set_help_text(HelpText.FTPAUSE)
        self.ftpause_input.setMaxLength(10)

        self.ftpause_input.focus.connect(self.on_help_focus)

        self.ftpause_input.setText(str(Case.the().execution_parameters.ftpause))
        self.ftpause_label2 = QtGui.QLabel("seconds")
        self.ftpause_layout.addWidget(self.ftpause_label)
        self.ftpause_layout.addWidget(self.ftpause_input)
        self.ftpause_layout.addWidget(self.ftpause_label2)

        # Coefficient to calculate DT
        self.coefdtmin_layout = QtGui.QHBoxLayout()
        self.coefdtmin_label = QtGui.QLabel("Coefficient for minimum time step: ")
        self.coefdtmin_input = FocusableLineEdit()
        self.coefdtmin_input.set_help_text(HelpText.COEFDTMIN)
        self.coefdtmin_input.setMaxLength(10)

        self.coefdtmin_input.focus.connect(self.on_help_focus)

        self.coefdtmin_input.setText(str(Case.the().execution_parameters.coefdtmin))
        self.coefdtmin_layout.addWidget(self.coefdtmin_label)
        self.coefdtmin_layout.addWidget(self.coefdtmin_input)

        # Initial time step
        self.dtiniauto_layout = QtGui.QHBoxLayout()
        self.dtiniauto_chk = QtGui.QCheckBox("Initial time step auto")
        if Case.the().execution_parameters.dtini_auto:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.dtiniauto_chk.toggled.connect(self.on_dtiniauto_check)
        self.dtiniauto_layout.addWidget(self.dtiniauto_chk)
        self.dtini_layout = QtGui.QHBoxLayout()
        self.dtini_label = QtGui.QLabel("Initial time step: ")
        self.dtini_input = FocusableLineEdit()
        self.dtini_input.set_help_text(HelpText.DTINI)
        self.dtini_input.setMaxLength(10)

        self.dtini_input.focus.connect(self.on_help_focus)

        self.dtini_input.setText(str(Case.the().execution_parameters.dtini))
        self.dtini_label2 = QtGui.QLabel("seconds")
        self.dtini_layout.addWidget(self.dtini_label)
        self.dtini_layout.addWidget(self.dtini_input)
        self.dtini_layout.addWidget(self.dtini_label2)
        self.on_dtiniauto_check()

        # Minimum time step
        self.dtminauto_layout = QtGui.QHBoxLayout()
        self.dtminauto_chk = QtGui.QCheckBox("Minimum time step: ")
        if Case.the().execution_parameters.dtmin_auto:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)

        self.dtminauto_chk.toggled.connect(self.on_dtminauto_check)
        self.dtminauto_layout.addWidget(self.dtminauto_chk)
        self.dtmin_layout = QtGui.QHBoxLayout()
        self.dtmin_label = QtGui.QLabel("Minimum time step: ")
        self.dtmin_input = FocusableLineEdit()
        self.dtmin_input.set_help_text(HelpText.DTMIN)
        self.dtmin_input.setMaxLength(10)

        self.dtmin_input.focus.connect(self.on_help_focus)

        self.dtmin_input.setText(str(Case.the().execution_parameters.dtmin))
        self.dtmin_label2 = QtGui.QLabel("seconds")
        self.dtmin_layout.addWidget(self.dtmin_label)
        self.dtmin_layout.addWidget(self.dtmin_input)
        self.dtmin_layout.addWidget(self.dtmin_label2)
        self.on_dtminauto_check()

        # Fixed DT file
        self.dtfixed_layout = QtGui.QHBoxLayout()
        self.dtfixed_label = QtGui.QLabel("Fixed DT file: ")
        self.dtfixed_input = QtGui.QLineEdit()
        self.dtfixed_input.setText(str(Case.the().execution_parameters.dtfixed))
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
        self.dtallparticles_input.setText(str(Case.the().execution_parameters.dtallparticles))
        self.dtallparticles_input.setValidator(self.dtallparticles_validator)
        self.dtallparticles_label2 = QtGui.QLabel("[0,1]")
        self.dtallparticles_layout.addWidget(self.dtallparticles_label)
        self.dtallparticles_layout.addWidget(self.dtallparticles_input)
        self.dtallparticles_layout.addWidget(self.dtallparticles_label2)

        # Time of simulation
        self.timemax_layout = QtGui.QHBoxLayout()
        self.timemax_label = QtGui.QLabel("Time of simulation: ")
        self.timemax_input = FocusableLineEdit()
        self.timemax_input.set_help_text(HelpText.TIMEMAX)
        self.timemax_input.setMaxLength(10)

        self.timemax_input.focus.connect(self.on_help_focus)

        self.timemax_input.setText(str(Case.the().execution_parameters.timemax))
        self.timemax_label2 = QtGui.QLabel("seconds")
        self.timemax_layout.addWidget(self.timemax_label)
        self.timemax_layout.addWidget(self.timemax_input)
        self.timemax_layout.addWidget(self.timemax_label2)

        # Time out data
        self.timeout_layout = QtGui.QHBoxLayout()
        self.timeout_label = QtGui.QLabel("Time out data: ")
        self.timeout_input = FocusableLineEdit()
        self.timeout_input.set_help_text(HelpText.TIMEOUT)
        self.timeout_input.setMaxLength(10)

        self.timeout_input.focus.connect(self.on_help_focus)

        self.timeout_input.setText(str(Case.the().execution_parameters.timeout))
        self.timeout_label2 = QtGui.QLabel("seconds")
        self.timeout_layout.addWidget(self.timeout_label)
        self.timeout_layout.addWidget(self.timeout_input)
        self.timeout_layout.addWidget(self.timeout_label2)

        # Max parts out allowed
        self.partsoutmax_layout = QtGui.QHBoxLayout()
        self.partsoutmax_label = QtGui.QLabel("Max parts out allowed (%): ")
        self.partsoutmax_input = FocusableLineEdit()
        self.partsoutmax_input.set_help_text(HelpText.PARTSOUTMAX)
        self.partsoutmax_input.setMaxLength(10)

        self.partsoutmax_input.focus.connect(self.on_help_focus)

        self.partsoutmax_input.setText(str(float(Case.the().execution_parameters.partsoutmax) * 100))
        self.partsoutmax_layout.addWidget(self.partsoutmax_label)
        self.partsoutmax_layout.addWidget(self.partsoutmax_input)

        # Minimum rhop valid
        self.rhopoutmin_layout = QtGui.QHBoxLayout()
        self.rhopoutmin_label = QtGui.QLabel("Minimum rhop valid: ")
        self.rhopoutmin_input = FocusableLineEdit()
        self.rhopoutmin_input.set_help_text(HelpText.RHOPOUTMIN)
        self.rhopoutmin_input.setMaxLength(10)

        self.rhopoutmin_input.focus.connect(self.on_help_focus)

        self.rhopoutmin_input.setText(str(Case.the().execution_parameters.rhopoutmin))
        self.rhopoutmin_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_input)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label2)

        # Maximum rhop valid
        self.rhopoutmax_layout = QtGui.QHBoxLayout()
        self.rhopoutmax_label = QtGui.QLabel("Maximum rhop valid: ")
        self.rhopoutmax_input = FocusableLineEdit()
        self.rhopoutmax_input.set_help_text(HelpText.RHOPOUTMAX)
        self.rhopoutmax_input.setMaxLength(10)

        self.rhopoutmax_input.focus.connect(self.on_help_focus)

        self.rhopoutmax_input.setText(str(Case.the().execution_parameters.rhopoutmax))
        self.rhopoutmax_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_input)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label2)

        self.period_x_layout = QtGui.QVBoxLayout()
        self.period_x_chk = QtGui.QCheckBox("X periodicity")
        self.period_x_inc_layout = QtGui.QHBoxLayout()
        self.period_x_inc_x_label = QtGui.QLabel("X Increment")
        self.period_x_inc_x_input = FocusableLineEdit()
        self.period_x_inc_y_label = QtGui.QLabel("Y Increment")
        self.period_x_inc_y_input = FocusableLineEdit()
        self.period_x_inc_y_input.set_help_text(HelpText.YINCREMENTX)
        self.period_x_inc_y_input.focus.connect(self.on_help_focus)
        self.period_x_inc_z_label = QtGui.QLabel("Z Increment")
        self.period_x_inc_z_input = FocusableLineEdit()
        self.period_x_inc_z_input.set_help_text(HelpText.ZINCREMENTX)
        self.period_x_inc_z_input.focus.connect(self.on_help_focus)
        self.period_x_inc_layout.addWidget(self.period_x_inc_x_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_x_input)
        self.period_x_inc_layout.addWidget(self.period_x_inc_y_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_y_input)
        self.period_x_inc_layout.addWidget(self.period_x_inc_z_label)
        self.period_x_inc_layout.addWidget(self.period_x_inc_z_input)
        self.period_x_layout.addWidget(self.period_x_chk)
        self.period_x_layout.addLayout(self.period_x_inc_layout)
        self.period_x_chk.stateChanged.connect(self.on_period_x_chk)

        self.period_x_chk.setChecked(Case.the().periodicity.x_periodicity.enabled)
        self.period_x_inc_x_input.setText(str(Case.the().periodicity.x_periodicity.x_increment))
        self.period_x_inc_y_input.setText(str(Case.the().periodicity.x_periodicity.y_increment))
        self.period_x_inc_z_input.setText(str(Case.the().periodicity.x_periodicity.z_increment))

        # Change the state of periodicity input on window open
        self.on_period_x_chk()

        self.period_y_layout = QtGui.QVBoxLayout()
        self.period_y_chk = QtGui.QCheckBox("Y periodicity")
        self.period_y_inc_layout = QtGui.QHBoxLayout()
        self.period_y_inc_x_label = QtGui.QLabel("X Increment")
        self.period_y_inc_x_input = FocusableLineEdit()
        self.period_y_inc_x_input.set_help_text(HelpText.XINCREMENTY)
        self.period_y_inc_x_input.focus.connect(self.on_help_focus)
        self.period_y_inc_y_label = QtGui.QLabel("Y Increment")
        self.period_y_inc_y_input = FocusableLineEdit()
        self.period_y_inc_z_label = QtGui.QLabel("Z Increment")
        self.period_y_inc_z_input = FocusableLineEdit()
        self.period_y_inc_z_input.set_help_text(HelpText.ZINCREMENTY)
        self.period_y_inc_z_input.focus.connect(self.on_help_focus)
        self.period_y_inc_layout.addWidget(self.period_y_inc_x_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_x_input)
        self.period_y_inc_layout.addWidget(self.period_y_inc_y_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_y_input)
        self.period_y_inc_layout.addWidget(self.period_y_inc_z_label)
        self.period_y_inc_layout.addWidget(self.period_y_inc_z_input)
        self.period_y_layout.addWidget(self.period_y_chk)
        self.period_y_layout.addLayout(self.period_y_inc_layout)
        self.period_y_chk.stateChanged.connect(self.on_period_y_chk)

        self.period_y_chk.setChecked(Case.the().periodicity.y_periodicity.enabled)
        self.period_y_inc_x_input.setText(str(Case.the().periodicity.y_periodicity.x_increment))
        self.period_y_inc_y_input.setText(str(Case.the().periodicity.y_periodicity.y_increment))
        self.period_y_inc_z_input.setText(str(Case.the().periodicity.y_periodicity.z_increment))

        # Change the state of periodicity input on window open
        self.on_period_y_chk()

        self.period_z_layout = QtGui.QVBoxLayout()
        self.period_z_chk = QtGui.QCheckBox("Z periodicity")
        self.period_z_inc_layout = QtGui.QHBoxLayout()
        self.period_z_inc_x_label = QtGui.QLabel("X Increment")
        self.period_z_inc_x_input = FocusableLineEdit()
        self.period_z_inc_x_input.set_help_text(HelpText.XINCREMENTZ)
        self.period_z_inc_x_input.focus.connect(self.on_help_focus)
        self.period_z_inc_y_label = QtGui.QLabel("Y Increment")
        self.period_z_inc_y_input = FocusableLineEdit()
        self.period_z_inc_y_input.set_help_text(HelpText.YINCREMENTZ)
        self.period_z_inc_y_input.focus.connect(self.on_help_focus)
        self.period_z_inc_z_label = QtGui.QLabel("Z Increment")
        self.period_z_inc_z_input = FocusableLineEdit()
        self.period_z_inc_layout.addWidget(self.period_z_inc_x_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_x_input)
        self.period_z_inc_layout.addWidget(self.period_z_inc_y_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_y_input)
        self.period_z_inc_layout.addWidget(self.period_z_inc_z_label)
        self.period_z_inc_layout.addWidget(self.period_z_inc_z_input)
        self.period_z_layout.addWidget(self.period_z_chk)
        self.period_z_layout.addLayout(self.period_z_inc_layout)
        self.period_z_chk.stateChanged.connect(self.on_period_z_chk)

        self.period_z_chk.setChecked(Case.the().periodicity.z_periodicity.enabled)
        self.period_z_inc_x_input.setText(str(Case.the().periodicity.z_periodicity.x_increment))
        self.period_z_inc_y_input.setText(str(Case.the().periodicity.z_periodicity.y_increment))
        self.period_z_inc_z_input.setText(str(Case.the().periodicity.z_periodicity.z_increment))

        # Change the state of periodicity input on window open
        self.on_period_z_chk()

        # Simulation domain
        self.simdomain_layout = QtGui.QVBoxLayout()
        self.simdomain_chk = QtGui.QCheckBox("Simulation Domain")

        self.simdomain_chk.setChecked(Case.the().domain.enabled)

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
        self.simdomain_posminx_combobox.insertItems(0, ["Default", "Value", "Default - value", "Default + %"])
        self.simdomain_posminx_line_edit = FocusableLineEdit()
        self.simdomain_posminx_line_edit.set_help_text(HelpText.POSMINX)
        self.simdomain_posminx_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posminx_line_edit.setText(str(Case.the().domain.posmin_x.value))
        self.simdomain_posminy_combobox = QtGui.QComboBox()
        self.simdomain_posminy_combobox.insertItems(0, ["Default", "Value", "Default - value", "Default + %"])
        self.simdomain_posminy_line_edit = FocusableLineEdit()
        self.simdomain_posminy_line_edit.set_help_text(HelpText.POSMINY)
        self.simdomain_posminy_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posminy_line_edit.setText(str(Case.the().domain.posmin_y.value))
        self.simdomain_posminz_combobox = QtGui.QComboBox()
        self.simdomain_posminz_combobox.insertItems(0, ["Default", "Value", "Default - value", "Default + %"])
        self.simdomain_posminz_line_edit = FocusableLineEdit()
        self.simdomain_posminz_line_edit.set_help_text(HelpText.POSMINZ)
        self.simdomain_posminz_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posminz_line_edit.setText(str(Case.the().domain.posmin_z.value))
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
        self.simdomain_posmaxx_combobox.insertItems(0, ["Default", "Value", "Default + value", "Default + %"])
        self.simdomain_posmaxx_line_edit = FocusableLineEdit()
        self.simdomain_posmaxx_line_edit.set_help_text(HelpText.POSMAXX)
        self.simdomain_posmaxx_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posmaxx_line_edit.setText(str(Case.the().domain.posmax_x.value))
        self.simdomain_posmaxy_combobox = QtGui.QComboBox()
        self.simdomain_posmaxy_combobox.insertItems(0, ["Default", "Value", "Default + value", "Default + %"])
        self.simdomain_posmaxy_line_edit = FocusableLineEdit()
        self.simdomain_posmaxy_line_edit.set_help_text(HelpText.POSMAXY)
        self.simdomain_posmaxy_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posmaxy_line_edit.setText(str(Case.the().domain.posmax_y.value))
        self.simdomain_posmaxz_combobox = QtGui.QComboBox()
        self.simdomain_posmaxz_combobox.insertItems(0, ["Default", "Value", "Default + value", "Default + %"])
        self.simdomain_posmaxz_line_edit = FocusableLineEdit()
        self.simdomain_posmaxz_line_edit.set_help_text(HelpText.POSMAXZ)
        self.simdomain_posmaxz_line_edit.focus.connect(self.on_help_focus)
        self.simdomain_posmaxz_line_edit.setText(str(Case.the().domain.posmax_z.value))
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

        self.simdomain_posminx_combobox.setCurrentIndex(Case.the().domain.posmin_x.type)
        self.simdomain_posminy_combobox.setCurrentIndex(Case.the().domain.posmin_y.type)
        self.simdomain_posminz_combobox.setCurrentIndex(Case.the().domain.posmin_z.type)
        self.simdomain_posmaxx_combobox.setCurrentIndex(Case.the().domain.posmax_x.type)
        self.simdomain_posmaxy_combobox.setCurrentIndex(Case.the().domain.posmax_y.type)
        self.simdomain_posmaxz_combobox.setCurrentIndex(Case.the().domain.posmax_z.type)

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
        self.ep_main_layout.addLayout(self.densitydt_type_layout)
        self.ep_main_layout.addLayout(self.densitydt_layout)
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
        self.execparams_window_layout.addWidget(self.help_label)
        self.execparams_window_layout.addLayout(self.ep_button_layout)
        self.setLayout(self.execparams_window_layout)

        self.resize(800, 600)
        self.exec_()

    def on_help_focus(self, help_text):
        """ Reacts to focusing the help setting the corresponding help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))

    def on_step_change(self, index):
        """ Reacts to step algorithm changing enabling/disabling the verletsteps option. """
        self.verletsteps_input.setEnabled(index == 0)

    def on_viscotreatment_change(self, index):
        """ Reacts to viscotreatment change. """
        self.visco_input.setText("0.01" if index == 0 else "0.000001")
        self.visco_label.setText("Viscosity value (alpha): " if index == 0 else "Kinematic viscosity: ")
        self.visco_units_label.setText("" if index == 0 else "m<span style='vertical-align:super'>2</span>/s")

    def on_densitydt_type_change(self, index):
        """ Reacts to densitydt type change enabling/disabling the input. """
        if index == 0:
            self.densitydt_input.setEnabled(False)
        else:
            self.densitydt_input.setEnabled(True)
            self.densitydt_input.setText("0.1")

    def on_shifting_change(self, index):
        """ Reacts to the shifting mode change enabling/disabling its input. """
        if index == 0:
            self.shiftcoef_input.setEnabled(False)
            self.shifttfs_input.setEnabled(False)
        else:
            self.shiftcoef_input.setEnabled(True)
            self.shifttfs_input.setEnabled(True)

    def on_dtiniauto_check(self):
        """ Reacts to the dtini automatic checkbox enabling/disabling its input. """
        if self.dtiniauto_chk.isChecked():
            self.dtini_input.setEnabled(False)
        else:
            self.dtini_input.setEnabled(True)

    def on_dtminauto_check(self):
        """ Reacts to the dtminauto checkbox enabling disabling its input. """
        if self.dtminauto_chk.isChecked():
            self.dtmin_input.setEnabled(False)
        else:
            self.dtmin_input.setEnabled(True)

    def on_period_x_chk(self):
        """ Reacts to the period_x checkbox being pressed enabling/disabling its inputs. """
        if self.period_x_chk.isChecked():
            self.period_x_inc_x_input.setEnabled(False)
            self.period_x_inc_y_input.setEnabled(True)
            self.period_x_inc_z_input.setEnabled(True)
        else:
            self.period_x_inc_x_input.setEnabled(False)
            self.period_x_inc_y_input.setEnabled(False)
            self.period_x_inc_z_input.setEnabled(False)

    def on_period_y_chk(self):
        """ Reacts to the period y checkbox being pressed enabling/disabling its inputs. """
        if self.period_y_chk.isChecked():
            self.period_y_inc_x_input.setEnabled(True)
            self.period_y_inc_y_input.setEnabled(False)
            self.period_y_inc_z_input.setEnabled(True)
        else:
            self.period_y_inc_x_input.setEnabled(False)
            self.period_y_inc_y_input.setEnabled(False)
            self.period_y_inc_z_input.setEnabled(False)

    def on_period_z_chk(self):
        """ Reacts to the period y checkbox being pressed enabling/disabling its inputs. """
        if self.period_z_chk.isChecked():
            self.period_z_inc_x_input.setEnabled(True)
            self.period_z_inc_y_input.setEnabled(True)
            self.period_z_inc_z_input.setEnabled(False)
        else:
            self.period_z_inc_x_input.setEnabled(False)
            self.period_z_inc_y_input.setEnabled(False)
            self.period_z_inc_z_input.setEnabled(False)

    def on_simdomain_chk(self):
        """ Reacts to the simdomain checkbox being pressed enabling/disabling its inputs. """
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
        """ Reacts to the posminx combobox being changed enabling/disabling its input. """
        if self.simdomain_posminx_combobox.currentIndex() == 0:
            self.simdomain_posminx_line_edit.setEnabled(False)
        else:
            self.simdomain_posminx_line_edit.setEnabled(True)

    def on_posminy_changed(self):
        """ Reacts to the posminy combobox being changed enabling/disabling its input. """
        if self.simdomain_posminy_combobox.currentIndex() == 0:
            self.simdomain_posminy_line_edit.setEnabled(False)
        else:
            self.simdomain_posminy_line_edit.setEnabled(True)

    def on_posminz_changed(self):
        """ Reacts to the posminz combobox being changed enabling/disabling its input. """
        if self.simdomain_posminz_combobox.currentIndex() == 0:
            self.simdomain_posminz_line_edit.setEnabled(False)
        else:
            self.simdomain_posminz_line_edit.setEnabled(True)

    def on_posmaxx_changed(self):
        """ Reacts to the posmaxx combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxx_combobox.currentIndex() == 0:
            self.simdomain_posmaxx_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxx_line_edit.setEnabled(True)

    def on_posmaxy_changed(self):
        """ Reacts to the posmaxy combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxy_combobox.currentIndex() == 0:
            self.simdomain_posmaxy_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxy_line_edit.setEnabled(True)

    def on_posmaxz_changed(self):
        """ Reacts to the posmaxz combobox being changed enabling/disabling its input. """
        if self.simdomain_posmaxz_combobox.currentIndex() == 0:
            self.simdomain_posmaxz_line_edit.setEnabled(False)
        else:
            self.simdomain_posmaxz_line_edit.setEnabled(True)

    # ------------ Button behaviour definition --------------
    def on_ok(self):
        """ Applies the data from the dialog onto the main data structure. """
        Case.the().execution_parameters.posdouble = int(self.posdouble_input.currentIndex())
        Case.the().execution_parameters.stepalgorithm = int(self.stepalgorithm_input.currentIndex() + 1)
        Case.the().execution_parameters.verletsteps = int(self.verletsteps_input.text())
        Case.the().execution_parameters.kernel = int(self.kernel_input.currentIndex() + 1)
        Case.the().execution_parameters.viscotreatment = int(self.viscotreatment_input.currentIndex() + 1)
        Case.the().execution_parameters.visco = float(self.visco_input.text())
        Case.the().execution_parameters.viscoboundfactor = int(self.viscoboundfactor_input.text())
        Case.the().execution_parameters.densitydt_type = int(self.densitydt_type_input.currentIndex())
        Case.the().execution_parameters.densitydt_value = float(self.densitydt_input.text())
        Case.the().execution_parameters.shifting = int(self.shifting_input.currentIndex())
        Case.the().execution_parameters.shiftcoef = float(self.shiftcoef_input.text())
        Case.the().execution_parameters.shifttfs = float(self.shifttfs_input.text())
        Case.the().execution_parameters.rigidalgorithm = int(self.rigidalgorithm_input.currentIndex() + 1)
        Case.the().execution_parameters.ftpause = float(self.ftpause_input.text())
        Case.the().execution_parameters.coefdtmin = float(self.coefdtmin_input.text())
        Case.the().execution_parameters.dtini = float(self.dtini_input.text())
        Case.the().execution_parameters.dtini_auto = self.dtiniauto_chk.isChecked()
        Case.the().execution_parameters.dtmin = float(self.dtmin_input.text())
        Case.the().execution_parameters.dtmin_auto = self.dtminauto_chk.isChecked()
        Case.the().execution_parameters.dtfixed = str(self.dtfixed_input.text())
        Case.the().execution_parameters.dtallparticles = int(self.dtallparticles_input.text())
        Case.the().execution_parameters.timemax = float(self.timemax_input.text())
        Case.the().execution_parameters.timeout = float(self.timeout_input.text())
        Case.the().execution_parameters.partsoutmax = float(self.partsoutmax_input.text()) / 100
        Case.the().execution_parameters.rhopoutmin = int(self.rhopoutmin_input.text())
        Case.the().execution_parameters.rhopoutmax = int(self.rhopoutmax_input.text())

        Case.the().periodicity = Periodicity()
        Case.the().periodicity.x_periodicity = PeriodicityInfo(
            self.period_x_chk.isChecked(),
            float(self.period_x_inc_x_input.text()),
            float(self.period_x_inc_y_input.text()),
            float(self.period_x_inc_z_input.text())
        )

        Case.the().periodicity.y_periodicity = PeriodicityInfo(
            self.period_y_chk.isChecked(),
            float(self.period_y_inc_x_input.text()),
            float(self.period_y_inc_y_input.text()),
            float(self.period_y_inc_z_input.text())
        )

        Case.the().periodicity.z_periodicity = PeriodicityInfo(
            self.period_z_chk.isChecked(),
            float(self.period_z_inc_x_input.text()),
            float(self.period_z_inc_y_input.text()),
            float(self.period_z_inc_z_input.text())
        )

        if self.simdomain_chk.isChecked():
            Case.the().domain.enabled = True
            # IncZ must be 0 in simulations with specified domain
            Case.the().execution_parameters.incz = 0

            Case.the().domain.posmin_x = SDPositionProperty(self.simdomain_posminx_combobox.currentIndex(), float(self.simdomain_posminx_line_edit.text()))
            Case.the().domain.posmin_y = SDPositionProperty(self.simdomain_posminy_combobox.currentIndex(), float(self.simdomain_posminy_line_edit.text()))
            Case.the().domain.posmin_z = SDPositionProperty(self.simdomain_posminz_combobox.currentIndex(), float(self.simdomain_posminz_line_edit.text()))

            Case.the().domain.posmax_x = SDPositionProperty(self.simdomain_posmaxx_combobox.currentIndex(), float(self.simdomain_posmaxx_line_edit.text()))
            Case.the().domain.posmax_y = SDPositionProperty(self.simdomain_posmaxy_combobox.currentIndex(), float(self.simdomain_posmaxy_line_edit.text()))
            Case.the().domain.posmax_z = SDPositionProperty(self.simdomain_posmaxz_combobox.currentIndex(), float(self.simdomain_posmaxz_line_edit.text()))
        else:
            Case.the().domain.enabled = False
            Case.the().reset_simulation_domain()

        log("Execution Parameters changed")
        self.accept()

    def on_cancel(self):
        """ Canceles the dialog rejecting it. """
        log("Execution Parameters not changed")
        self.reject()
