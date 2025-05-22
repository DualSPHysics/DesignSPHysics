#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Execution Parameters Configuration Dialog."""
import FreeCADGui
from PySide2 import QtCore, QtWidgets

from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import draw_simulation_domain, update_simulation_domain

from mod.tools.translation_tools import __
from mod.tools.stdout_tools import log
from mod.enums import HelpText, SDPositionPropertyType
from mod.widgets.custom_widgets.density_input import DensityInput
from mod.widgets.dock.dock_widgets.simulation_domain_widget import SimulationDomainWidget
from mod.widgets.custom_widgets.value_input import ValueInput

from mod.widgets.custom_widgets.focusable_combo_box import FocusableComboBox

from mod.dataobjects.case import Case
from mod.dataobjects.configuration.periodicity import Periodicity
from mod.dataobjects.configuration.periodicity_info import PeriodicityInfo
from mod.dataobjects.configuration.sd_position_property import SDPositionProperty
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput


class ExecutionParametersDialog(QtWidgets.QDialog):
    """Defines the execution parameters window.
    Modifies the data dictionary passed as parameter."""

    LABEL_DEFAULT_TEXT = "<i>{}</i>".format(__("Select an input to show help about it."))
    MINIMUM_WIDTH = 860
    MINIMUM_HEIGHT = 768

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Creates a dialog and 2 main buttons
        self.setWindowTitle(__("Execution Parameters"))
        self.help_label = QtWidgets.QLabel(self.LABEL_DEFAULT_TEXT)
        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))
        ########### Save pos double #######################
        self.saveposdouble_layout = QtWidgets.QHBoxLayout()
        self.saveposdouble_label = QtWidgets.QLabel(__("Save particle position with double precision:"))
        self.saveposdouble_input = FocusableComboBox()
        self.saveposdouble_input.insertItems(0, [__("No"), __("Yes")])
        self.saveposdouble_input.setCurrentIndex(int(Case.the().execution_parameters.saveposdouble))
        self.saveposdouble_input.set_help_text(HelpText.SAVEPOSDOUBLE)
        self.saveposdouble_input.focus.connect(self.on_help_focus)
        self.saveposdouble_layout.addWidget(self.saveposdouble_label)
        self.saveposdouble_layout.addWidget(self.saveposdouble_input)
        self.saveposdouble_widget=QtWidgets.QWidget()
        self.saveposdouble_widget.setLayout(self.saveposdouble_layout)
        self.saveposdouble_layout.setContentsMargins(10,0,10,0)

        ######################### KERNEL ##############################
        self.kernel_layout = QtWidgets.QHBoxLayout()
        self.kernel_label = QtWidgets.QLabel(__("Interaction kernel:"))
        self.kernel_input = FocusableComboBox()
        self.kernel_input.insertItems(0, [__("Cubic spline"), __("Wendland")])
        self.kernel_input.set_help_text(HelpText.KERNEL)
        self.kernel_input.setCurrentIndex(int(Case.the().execution_parameters.kernel) - 1)
        self.kernel_input.focus.connect(self.on_help_focus)
        self.kernel_layout.addWidget(self.kernel_label)
        self.kernel_layout.addWidget(self.kernel_input)
        self.kernel_widget = QtWidgets.QWidget()
        self.kernel_widget.setLayout(self.kernel_layout)
        self.kernel_layout.setContentsMargins(10, 0, 10, 0)

        ########################### Rigid algorithm (Solid-solid interaction) ##################################
        self.rigidalgorithm_layout = QtWidgets.QHBoxLayout()
        self.rigidalgorithm_label = QtWidgets.QLabel(__("Solid-solid interaction:"))
        self.rigidalgorithm_input = FocusableComboBox()
        self.rigidalgorithm_input.insertItems(0, ["SPH", "DEM", "CHRONO"])
        self.rigidalgorithm_input.set_help_text(HelpText.RIGIDALGORITHM)
        self.rigidalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.rigidalgorithm) - 1)
        self.rigidalgorithm_input.focus.connect(self.on_help_focus)
        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_label)
        self.rigidalgorithm_layout.addWidget(self.rigidalgorithm_input)
        self.rigidalgorithm_widget = QtWidgets.QWidget()
        self.rigidalgorithm_widget.setLayout(self.rigidalgorithm_layout)
        self.rigidalgorithm_layout.setContentsMargins(10, 0, 10, 0)

        ########################### BOUNDARY CONFIGURATION #######################################
        self.boundary_configuration_layout = QtWidgets.QVBoxLayout()
        self.boundary_configuration_group = QtWidgets.QGroupBox("Boundary algorithm configuration")
        self.boundary_configuration_group.setLayout(self.boundary_configuration_layout)
        #Boundary method
        self.boundary_layout = QtWidgets.QHBoxLayout()
        self.boundary_label = QtWidgets.QLabel(__("Boundary Method:"))
        self.boundary_input = FocusableComboBox()
        self.boundary_input.insertItems(0, [__("DBC"), __("mDBC")])
        self.boundary_input.setCurrentIndex(int(Case.the().execution_parameters.boundary) - 1)
        self.boundary_input.set_help_text(HelpText.BOUNDARY)
        self.boundary_input.focus.connect(self.on_help_focus)
        self.boundary_input.currentIndexChanged.connect(self.on_boundary_type_change)
        self.boundary_layout.addWidget(self.boundary_label)
        self.boundary_layout.addWidget(self.boundary_input)
        self.boundary_configuration_layout.addLayout(self.boundary_layout)
        #Slipmode
        self.slipmode_layout = QtWidgets.QHBoxLayout()
        self.slipmode_label = QtWidgets.QLabel(__("Slip Mode:"))
        self.slipmode_input = FocusableComboBox()
        self.slipmode_input.insertItems(0, [__("DBC vel=0"), __("No-slip"), __("Free slip")])
        if Case.the().execution_parameters.slipmode:
            self.slipmode_input.setCurrentIndex(int(Case.the().execution_parameters.slipmode) - 1)
        self.slipmode_input.focus.connect(self.on_help_focus)
        self.slipmode_layout.addWidget(self.slipmode_label)
        self.slipmode_layout.addWidget(self.slipmode_input)
        self.boundary_configuration_layout.addLayout(self.slipmode_layout)
        #NoPenetration
        self.nopenetration_layout = QtWidgets.QHBoxLayout()
        self.nopenetration_label = QtWidgets.QLabel(__("No-Penetration active:"))
        self.nopenetration_input = FocusableComboBox()
        self.nopenetration_input.insertItems(0, [__("Off"), __("On")])
        if Case.the().execution_parameters.nopenetration:
            self.nopenetration_input.setCurrentIndex(int(Case.the().execution_parameters.nopenetration))
        self.nopenetration_input.focus.connect(self.on_help_focus)
        self.nopenetration_layout.addWidget(self.nopenetration_label)
        self.nopenetration_layout.addWidget(self.nopenetration_input)
        self.boundary_configuration_layout.addLayout(self.nopenetration_layout)
        ###################################### STEP ALGORITHM ###########################################
        self.stepalgorithm_configuration_layout = QtWidgets.QVBoxLayout()
        self.stepalgorithm_configuration_group = QtWidgets.QGroupBox("Step algorithm configuration")
        self.stepalgorithm_configuration_group.setLayout(self.stepalgorithm_configuration_layout)

        self.stepalgorithm_layout = QtWidgets.QHBoxLayout()
        self.stepalgorithm_label = QtWidgets.QLabel(__("Step Algorithm:"))
        self.stepalgorithm_input = FocusableComboBox()
        self.stepalgorithm_input.insertItems(0, [__("Verlet"), __("Symplectic")])
        self.stepalgorithm_input.setCurrentIndex(int(Case.the().execution_parameters.stepalgorithm) - 1)
        self.stepalgorithm_input.set_help_text(HelpText.STEPALGORITHM)
        self.stepalgorithm_input.focus.connect(self.on_help_focus)
        self.stepalgorithm_input.currentIndexChanged.connect(self.on_step_change) #test
        self.stepalgorithm_layout.addWidget(self.stepalgorithm_label)
        self.stepalgorithm_layout.addWidget(self.stepalgorithm_input)
        self.stepalgorithm_configuration_layout.addLayout(self.stepalgorithm_layout)

        self.verletsteps_layout = QtWidgets.QHBoxLayout()
        self.verletsteps_label = QtWidgets.QLabel(__("Verlet Steps:"))
        self.verletsteps_input = IntValueInput(min_val=0,max_val=9999)
        self.verletsteps_input.set_help_text(HelpText.VERLETSTEPS)
        self.verletsteps_input.focus.connect(self.on_help_focus)
        self.verletsteps_input.setValue(Case.the().execution_parameters.verletsteps)
        self.verletsteps_layout.addWidget(self.verletsteps_label)
        self.verletsteps_layout.addWidget(self.verletsteps_input)
        # Enable/Disable fields depending on selection
        self.on_step_change(self.stepalgorithm_input.currentIndex)
        self.stepalgorithm_configuration_layout.addLayout(self.verletsteps_layout)

        ################################### VISCOSITY ###############################################################
        self.viscosity_configuration_layout = QtWidgets.QVBoxLayout()
        self.viscosity_configuration_group = QtWidgets.QGroupBox("Viscosity configuration")
        self.viscosity_configuration_group.setLayout(self.viscosity_configuration_layout)
        #Viscosity treatment
        self.viscotreatment_layout = QtWidgets.QHBoxLayout()
        self.viscotreatment_label = QtWidgets.QLabel(__("Viscosity Formulation:"))
        self.viscotreatment_input = FocusableComboBox()
        self.viscotreatment_input.insertItems(0, [__("Artificial"), __("Laminar + SPS"), __("Laminar")])
        self.viscotreatment_input.set_help_text(HelpText.VISCOTREATMENT)
        self.viscotreatment_input.setCurrentIndex(int(Case.the().execution_parameters.viscotreatment) - 1)
        self.viscotreatment_input.focus.connect(self.on_help_focus)
        self.viscotreatment_layout.addWidget(self.viscotreatment_label)
        self.viscotreatment_layout.addWidget(self.viscotreatment_input)
        self.viscosity_configuration_layout.addLayout((self.viscotreatment_layout))
        # Viscosity value
        self.visco_layout = QtWidgets.QHBoxLayout()
        self.visco_label = QtWidgets.QLabel(__("Viscosity value:"))
        self.visco_input = ValueInput(min_val=0,max_val=1,decimals=7)
        self.visco_input.set_help_text(HelpText.VISCO)
        self.visco_input.focus.connect(self.on_help_focus)
        self.visco_layout.addWidget(self.visco_label)
        self.visco_layout.addWidget(self.visco_input)
        self.viscosity_configuration_layout.addLayout(self.visco_layout)
        self.on_viscotreatment_change(int(Case.the().execution_parameters.viscotreatment) - 1)
        self.visco_input.setValue(Case.the().execution_parameters.visco)
        self.viscotreatment_input.currentIndexChanged.connect(self.on_viscotreatment_change)
        # Viscosity with boundary
        self.viscoboundfactor_layout = QtWidgets.QHBoxLayout()
        self.viscoboundfactor_label = QtWidgets.QLabel(__("Viscosity factor with boundary: "))
        self.viscoboundfactor_input = ValueInput()#MIN AND MAX???
        self.viscoboundfactor_input.set_help_text(HelpText.VISCOBOUNDFACTOR)
        self.viscoboundfactor_input.focus.connect(self.on_help_focus)
        self.viscoboundfactor_input.setValue(Case.the().execution_parameters.viscoboundfactor)
        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_label)
        self.viscoboundfactor_layout.addWidget(self.viscoboundfactor_input)
        self.viscosity_configuration_layout.addLayout(self.viscoboundfactor_layout)

        #############################################DENSITY#################################################
        self.density_configuration_layout = QtWidgets.QVBoxLayout()
        self.density_configuration_group = QtWidgets.QGroupBox("Density configuration")
        self.density_configuration_group.setLayout(self.density_configuration_layout)
        #Density type
        self.densitydt_type_layout = QtWidgets.QHBoxLayout()
        self.densitydt_type_label = QtWidgets.QLabel(__("Density Diffusion Term:"))
        self.densitydt_type_input = QtWidgets.QComboBox()
        densitydt_option_list = [__('None'), __('Molteni'), __('Fourtakas'), __('Fourtakas (Full)')]
        self.densitydt_type_input.insertItems(0, densitydt_option_list)
        self.densitydt_type_input.setCurrentIndex(Case.the().execution_parameters.densitydt_type)
        self.densitydt_type_input.currentIndexChanged.connect(self.on_densitydt_type_change)
        self.densitydt_type_layout.addWidget(self.densitydt_type_label)
        self.densitydt_type_layout.addWidget(self.densitydt_type_input)
        self.density_configuration_layout.addLayout((self.densitydt_type_layout))
        # densitydt value
        self.densitydt_layout = QtWidgets.QHBoxLayout()
        self.densitydt_label = QtWidgets.QLabel(__("DDT value:"))
        self.densitydt_input = ValueInput(decimals=3)
        self.densitydt_input.set_help_text(HelpText.DENSITYDT)
        self.densitydt_input.focus.connect(self.on_help_focus)
        self.densitydt_input.setValue(Case.the().execution_parameters.densitydt_value)
        self.densitydt_layout.addWidget(self.densitydt_label)
        self.densitydt_layout.addWidget(self.densitydt_input)
        self.density_configuration_layout.addLayout((self.densitydt_layout))
        #change
        if self.densitydt_type_input.currentIndex() == 0:
            self.densitydt_input.setEnabled(False)
        else:
            self.densitydt_input.setEnabled(True)

        ###################################### SHIFTING ############################################
        self.shifting_options_layout = QtWidgets.QVBoxLayout()
        self.shifting_options_groupbox = QtWidgets.QGroupBox("Shifting configuration")
        self.shifting_options_groupbox.setLayout(self.shifting_options_layout)
        #shifting mode
        self.shifting_layout = QtWidgets.QHBoxLayout()
        self.shifting_label = QtWidgets.QLabel(__("Shifting mode:"))
        self.shifting_input = FocusableComboBox()
        self.shifting_input.insertItems(0, [__("0.None"), __("1.Ignore bound"), __("2.Ignore fixed"), __("3.Full"),__("4.Full advanced")])
        self.shifting_input.set_help_text(HelpText.SHIFTING)
        self.shifting_input.focus.connect(self.on_help_focus)
        self.shifting_layout.addWidget(self.shifting_label)
        self.shifting_layout.addWidget(self.shifting_input)
        self.shifting_options_layout.addLayout(self.shifting_layout)
        # Coefficient for shifting
        self.shiftcoef_layout = QtWidgets.QHBoxLayout()
        self.shiftcoef_label = QtWidgets.QLabel(__("Coefficient for shifting:"))
        self.shiftcoef_input = ValueInput()
        self.shiftcoef_input.set_help_text(HelpText.SHIFTINGCOEF)
        self.shiftcoef_input.focus.connect(self.on_help_focus)
        self.shiftcoef_input.setValue(Case.the().execution_parameters.shiftcoef)
        self.shiftcoef_layout.addWidget(self.shiftcoef_label)
        self.shiftcoef_layout.addWidget(self.shiftcoef_input)
        self.shifting_options_layout.addLayout(self.shiftcoef_layout)
        # Free surface detection threshold
        self.shifttfs_layout = QtWidgets.QHBoxLayout()
        self.shifttfs_label = QtWidgets.QLabel(__("Free surface detection threshold:"))
        self.shifttfs_input = ValueInput()
        self.shifttfs_input.set_help_text(HelpText.SHIFTINGTFS)
        self.shifttfs_input.focus.connect(self.on_help_focus)
        self.shifttfs_input.setValue(Case.the().execution_parameters.shifttfs)
        self.shifttfs_layout.addWidget(self.shifttfs_label)
        self.shifttfs_layout.addWidget(self.shifttfs_input)
        self.shifting_options_layout.addLayout(self.shifttfs_layout)
        # Advanced shifting coefficient
        self.shiftadvcoef_layout = QtWidgets.QHBoxLayout()
        self.shiftadvcoef_label = QtWidgets.QLabel(__("Coefficient for advanced shifting computation:"))
        self.shiftadvcoef_input = ValueInput()
        self.shiftadvcoef_input.set_help_text(HelpText.SHIFTINGTFS)
        self.shiftadvcoef_input.focus.connect(self.on_help_focus)
        self.shiftadvcoef_input.setValue(Case.the().execution_parameters.shiftadvcoef)
        self.shiftadvcoef_layout.addWidget(self.shiftadvcoef_label)
        self.shiftadvcoef_layout.addWidget(self.shiftadvcoef_input)
        self.shifting_options_layout.addLayout(self.shiftadvcoef_layout)
        # Advanced shifting ALE
        self.shiftadvale_layout = QtWidgets.QHBoxLayout()
        self.shiftadvale_label = QtWidgets.QLabel(__("ALE for advanced shifting computation:"))
        self.shiftadvale_input = ValueInput()
        self.shiftadvale_input.set_help_text(HelpText.SHIFTINGTFS)
        self.shiftadvale_input.focus.connect(self.on_help_focus)
        self.shiftadvale_input.setValue(Case.the().execution_parameters.shiftadvale)
        self.shiftadvale_layout.addWidget(self.shiftadvale_label)
        self.shiftadvale_layout.addWidget(self.shiftadvale_input)
        self.shifting_options_layout.addLayout(self.shiftadvale_layout)
        # Advanced shifting no conservative pressure formulation
        self.shiftadvncpress_layout = QtWidgets.QHBoxLayout()
        self.shiftadvncpress_label = QtWidgets.QLabel(__("Non conservative pressure formulation"))
        self.shiftadvncpress_input = ValueInput()
        self.shiftadvncpress_input.set_help_text(HelpText.SHIFTINGTFS)
        self.shiftadvncpress_input.focus.connect(self.on_help_focus)
        self.shiftadvncpress_input.setValue(Case.the().execution_parameters.shiftadvncpress)
        self.shiftadvncpress_layout.addWidget(self.shiftadvncpress_label)
        self.shiftadvncpress_layout.addWidget(self.shiftadvncpress_input)
        self.shifting_options_layout.addLayout(self.shiftadvncpress_layout)
        #change
        self.shifting_input.currentIndexChanged.connect(self.on_shifting_change)
        self.shifting_input.setCurrentIndex(int(Case.the().execution_parameters.shifting))
        self.on_shifting_change(int(Case.the().execution_parameters.shifting))



        ################################################## TIMESTEP ############################################
        self.timestep_configuration_layout = QtWidgets.QVBoxLayout()
        self.timestep_configuration_group = QtWidgets.QGroupBox("Timestep configuration")
        self.timestep_configuration_group.setLayout(self.timestep_configuration_layout)
        # Initial time step
        self.dtiniauto_layout = QtWidgets.QHBoxLayout()
        self.dtiniauto_chk = QtWidgets.QCheckBox(__("Initial time step auto"))
        if Case.the().execution_parameters.dtini_auto:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)
        self.dtiniauto_chk.toggled.connect(self.on_dtiniauto_check)
        self.dtiniauto_layout.addWidget(self.dtiniauto_chk)
        self.dtini_layout = QtWidgets.QHBoxLayout()
        self.dtini_label = QtWidgets.QLabel(__("Initial time step:"))
        self.dtini_input = TimeInput()
        self.dtini_input.set_help_text(HelpText.DTINI)
        self.dtini_input.focus.connect(self.on_help_focus)
        self.dtini_input.setValue(Case.the().execution_parameters.dtini)
        self.dtini_layout.addWidget(self.dtini_label)
        self.dtini_layout.addWidget(self.dtini_input)
        self.timestep_configuration_layout.addLayout(self.dtini_layout)
        self.on_dtiniauto_check()
        # Minimum time step
        self.dtminauto_layout = QtWidgets.QHBoxLayout()
        self.dtminauto_chk = QtWidgets.QCheckBox(__("Minimum time step auto"))
        if Case.the().execution_parameters.dtmin_auto:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Checked)
        else:
            self.dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)
        self.dtminauto_chk.toggled.connect(self.on_dtminauto_check)
        self.dtminauto_layout.addWidget(self.dtminauto_chk)
        self.dtminauto_layout.addWidget(self.dtminauto_chk)
        self.timestep_configuration_layout.addLayout(self.dtminauto_layout)
        self.dtmin_layout = QtWidgets.QHBoxLayout()
        self.dtmin_label = QtWidgets.QLabel(__("Minimum time step:"))
        self.dtmin_input = TimeInput()
        self.dtmin_input.set_help_text(HelpText.DTMIN)
        self.dtmin_input.focus.connect(self.on_help_focus)
        self.dtmin_input.setValue(Case.the().execution_parameters.dtmin)
        self.dtmin_layout.addWidget(self.dtmin_label)
        self.dtmin_layout.addWidget(self.dtmin_input)
        self.timestep_configuration_layout.addLayout(self.dtmin_layout)
        self.on_dtminauto_check()
        # Coefficient to calculate DT
        self.coefdtmin_layout = QtWidgets.QHBoxLayout()
        self.coefdtmin_label = QtWidgets.QLabel(__("Coefficient for minimum time step:"))
        self.coefdtmin_input = ValueInput()
        self.coefdtmin_input.set_help_text(HelpText.COEFDTMIN)
        self.coefdtmin_input.focus.connect(self.on_help_focus)
        self.coefdtmin_input.setValue(Case.the().execution_parameters.coefdtmin)
        self.coefdtmin_layout.addWidget(self.coefdtmin_label)
        self.coefdtmin_layout.addWidget(self.coefdtmin_input)
        self.timestep_configuration_layout.addLayout(self.coefdtmin_layout)

        ####################################### TIME CONFIGURATION ################################
        self.time_configuration_layout = QtWidgets.QVBoxLayout()
        self.time_configuration_group = QtWidgets.QGroupBox("Time configuration")
        self.time_configuration_group.setLayout(self.time_configuration_layout)
        # Time of simulation
        self.timemax_layout = QtWidgets.QHBoxLayout()
        self.timemax_label = QtWidgets.QLabel(__("Time of simulation: "))
        self.timemax_input = TimeInput()
        self.timemax_input.set_help_text(HelpText.TIMEMAX)
        self.timemax_input.focus.connect(self.on_help_focus)
        self.timemax_input.setValue(Case.the().execution_parameters.timemax)
        self.timemax_layout.addWidget(self.timemax_label)
        self.timemax_layout.addWidget(self.timemax_input)
        self.time_configuration_layout.addLayout(self.timemax_layout)
        # Time out data
        self.timeout_layout = QtWidgets.QHBoxLayout()
        self.timeout_label = QtWidgets.QLabel(__("Time out data: "))
        self.timeout_input = TimeInput()
        self.timeout_input.set_help_text(HelpText.TIMEOUT)
        self.timeout_input.focus.connect(self.on_help_focus)
        self.timeout_input.setValue(Case.the().execution_parameters.timeout)
        self.timeout_layout.addWidget(self.timeout_label)
        self.timeout_layout.addWidget(self.timeout_input)
        self.time_configuration_layout.addLayout(self.timeout_layout)
        # Sim start freeze time (ftpause)
        self.ftpause_layout = QtWidgets.QHBoxLayout()
        self.ftpause_label = QtWidgets.QLabel(__("Floating freeze time:"))
        self.ftpause_input = TimeInput()
        self.ftpause_input.set_help_text(HelpText.FTPAUSE)
        self.ftpause_input.focus.connect(self.on_help_focus)
        self.ftpause_input.setValue(Case.the().execution_parameters.ftpause)
        self.ftpause_layout.addWidget(self.ftpause_label)
        self.ftpause_layout.addWidget(self.ftpause_input)
        self.time_configuration_layout.addLayout(self.ftpause_layout)

        ########################### Min fluid stop ########################################################
        self.simulation_values_configuration_layout = QtWidgets.QVBoxLayout()
        self.simulation_values_configuration_group = QtWidgets.QGroupBox("Simulation max/min values configuration")
        self.simulation_values_configuration_group.setLayout(self.simulation_values_configuration_layout)
        #minfluid stop
        self.minfluidstop_layout = QtWidgets.QHBoxLayout()
        self.minfluidstop_label = QtWidgets.QLabel(__("Min parts remaining fom going out allowed (%):"))
        self.minfluidstop_input = ValueInput(min_val=0,max_val=100)
        self.minfluidstop_input.set_help_text(HelpText.PARTSOUTMAX)
        self.minfluidstop_input.focus.connect(self.on_help_focus)
        self.minfluidstop_input.setValue(float(Case.the().execution_parameters.minfluidstop) * 100)
        self.minfluidstop_layout.addWidget(self.minfluidstop_label)
        self.minfluidstop_layout.addWidget(self.minfluidstop_input)
        self.simulation_values_configuration_layout.addLayout(self.minfluidstop_layout)
        # Minimum rhop valid
        self.rhopoutmin_layout = QtWidgets.QHBoxLayout()
        self.rhopoutmin_label = QtWidgets.QLabel(__("Minimum rhop valid:"))
        self.rhopoutmin_input = DensityInput()
        self.rhopoutmin_input.set_help_text(HelpText.RHOPOUTMIN)
        self.rhopoutmin_input.focus.connect(self.on_help_focus)
        self.rhopoutmin_input.setValue(Case.the().execution_parameters.rhopoutmin)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_label)
        self.rhopoutmin_layout.addWidget(self.rhopoutmin_input)
        self.simulation_values_configuration_layout.addLayout(self.rhopoutmin_layout)
        # Maximum rhop valid
        self.rhopoutmax_layout = QtWidgets.QHBoxLayout()
        self.rhopoutmax_label = QtWidgets.QLabel(__("Maximum rhop valid:"))
        self.rhopoutmax_input = DensityInput()
        self.rhopoutmax_input.set_help_text(HelpText.RHOPOUTMAX)
        self.rhopoutmax_input.focus.connect(self.on_help_focus)
        self.rhopoutmax_input.setValue(Case.the().execution_parameters.rhopoutmax)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_label)
        self.rhopoutmax_layout.addWidget(self.rhopoutmax_input)
        self.simulation_values_configuration_layout.addLayout(self.rhopoutmax_layout)

        ############################### MDBC options group ##########################################
        self.mdbc_options_layout=QtWidgets.QVBoxLayout()
        self.mdbc_options_groupbox=QtWidgets.QGroupBox("Mdbc configuration for external geometry")
        self.mdbc_options_groupbox.setLayout(self.mdbc_options_layout)
        #Normals disth
        self.normals_disth_layout = QtWidgets.QHBoxLayout()
        self.normals_disth_label = QtWidgets.QLabel(__("Normals dist_h:"))
        self.normals_disth_input = ValueInput()
        self.normals_disth_input.setValue(Case.the().execution_parameters.mdbc_disth)
        self.normals_disth_input.focus.connect(self.on_help_focus)
        self.normals_disth_layout.addWidget(self.normals_disth_label)
        self.normals_disth_layout.addWidget(self.normals_disth_input)
        #normals maxsizeh
        self.normals_maxsizeh_layout = QtWidgets.QHBoxLayout()
        self.normals_maxsizeh_label = QtWidgets.QLabel(__("Normals max size h:"))
        self.normals_maxsizeh_input = ValueInput()
        self.normals_maxsizeh_input.setValue(Case.the().execution_parameters.mdbc_maxsizeh)
        #self.normals_maxsizeh_input.set_help_text(HelpText.BOUNDARY)
        self.normals_maxsizeh_input.focus.connect(self.on_help_focus)
        self.normals_maxsizeh_layout.addWidget(self.normals_maxsizeh_label)
        self.normals_maxsizeh_layout.addWidget(self.normals_maxsizeh_input)
        self.mdbc_options_layout.addLayout(self.normals_disth_layout)
        self.mdbc_options_layout.addLayout(self.normals_maxsizeh_layout)
        self.on_boundary_type_change(self.boundary_input.currentIndex())

        ################################### PERIODICITY OPTIONS ######################################
        self.period_layout=QtWidgets.QVBoxLayout()
        self.period_groupbox=QtWidgets.QGroupBox("Periodicity options")
        self.period_groupbox.setLayout(self.period_layout)

        self.period_x_layout = QtWidgets.QVBoxLayout()
        self.period_x_chk = QtWidgets.QCheckBox(__("X periodicity"))
        self.period_x_inc_layout = QtWidgets.QHBoxLayout()
        self.period_x_inc_x_label = QtWidgets.QLabel(__("X Increment"))
        self.period_x_inc_x_input = SizeInput()
        self.period_x_inc_y_label = QtWidgets.QLabel(__("Y Increment"))
        self.period_x_inc_y_input = SizeInput()
        self.period_x_inc_y_input.set_help_text(HelpText.YINCREMENTX)
        self.period_x_inc_y_input.focus.connect(self.on_help_focus)
        self.period_x_inc_z_label = QtWidgets.QLabel(__("Z Increment"))
        self.period_x_inc_z_input = SizeInput()
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
        self.period_x_inc_x_input.setValue(Case.the().periodicity.x_periodicity.x_increment)
        self.period_x_inc_y_input.setValue(Case.the().periodicity.x_periodicity.y_increment)
        self.period_x_inc_z_input.setValue(Case.the().periodicity.x_periodicity.z_increment)

        # Change the state of periodicity input on window open
        self.on_period_x_chk()

        self.period_y_layout = QtWidgets.QVBoxLayout()
        self.period_y_chk = QtWidgets.QCheckBox(__("Y periodicity"))
        self.period_y_inc_layout = QtWidgets.QHBoxLayout()
        self.period_y_inc_x_label = QtWidgets.QLabel(__("X Increment"))
        self.period_y_inc_x_input = SizeInput()
        self.period_y_inc_x_input.set_help_text(HelpText.XINCREMENTY)
        self.period_y_inc_x_input.focus.connect(self.on_help_focus)
        self.period_y_inc_y_label = QtWidgets.QLabel(__("Y Increment"))
        self.period_y_inc_y_input = SizeInput()
        self.period_y_inc_z_label = QtWidgets.QLabel(__("Z Increment"))
        self.period_y_inc_z_input = SizeInput()
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
        self.period_y_inc_x_input.setValue(Case.the().periodicity.y_periodicity.x_increment)
        self.period_y_inc_y_input.setValue(Case.the().periodicity.y_periodicity.y_increment)
        self.period_y_inc_z_input.setValue(Case.the().periodicity.y_periodicity.z_increment)

        # Change the state of periodicity input on window open
        self.on_period_y_chk()

        self.period_z_layout = QtWidgets.QVBoxLayout()
        self.period_z_chk = QtWidgets.QCheckBox(__("Z periodicity"))
        self.period_z_inc_layout = QtWidgets.QHBoxLayout()
        self.period_z_inc_x_label = QtWidgets.QLabel(__("X Increment"))
        self.period_z_inc_x_input = SizeInput()
        self.period_z_inc_x_input.set_help_text(HelpText.XINCREMENTZ)
        self.period_z_inc_x_input.focus.connect(self.on_help_focus)
        self.period_z_inc_y_label = QtWidgets.QLabel(__("Y Increment"))
        self.period_z_inc_y_input = SizeInput()
        self.period_z_inc_y_input.set_help_text(HelpText.YINCREMENTZ)
        self.period_z_inc_y_input.focus.connect(self.on_help_focus)
        self.period_z_inc_z_label = QtWidgets.QLabel(__("Z Increment"))
        self.period_z_inc_z_input = SizeInput()
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
        self.period_z_inc_x_input.setValue(Case.the().periodicity.z_periodicity.x_increment)
        self.period_z_inc_y_input.setValue(Case.the().periodicity.z_periodicity.y_increment)
        self.period_z_inc_z_input.setValue(Case.the().periodicity.z_periodicity.z_increment)

        # Change the state of periodicity input on window open
        self.on_period_z_chk()

        self.period_layout.addLayout(self.period_x_layout)
        self.period_layout.addLayout(self.period_y_layout)
        self.period_layout.addLayout(self.period_z_layout)

        ################################# SIMULATION DOMAIN ##########################################
        self.simulation_domain_layout = QtWidgets.QVBoxLayout()
        self.simulation_domain_groupbox=QtWidgets.QGroupBox("Simulation domain definition")
        self.simulation_domain_groupbox.setLayout(self.simulation_domain_layout)
        self.sim_domain_widget=SimulationDomainWidget(Case.the().domain,False)
        self.simulation_domain_layout.addWidget(self.sim_domain_widget)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Button layout definition
        self.ep_button_layout = QtWidgets.QHBoxLayout()
        self.ep_button_layout.addStretch(1)
        self.ep_button_layout.addWidget(self.ok_button)
        self.ep_button_layout.addWidget(self.cancel_button)

        # START Main layout definition and composition.
        self.ep_main_layout_scroll = QtWidgets.QScrollArea()
        self.ep_main_layout_scroll.setWidgetResizable(True)
        self.ep_main_layout_scroll_widget = QtWidgets.QWidget()

        self.ep_main_layout = QtWidgets.QVBoxLayout()
        
        self.full_widget_list=[
         self.saveposdouble_widget
        ,self.kernel_widget
        ,self.rigidalgorithm_widget
        ,self.boundary_configuration_group
        ,self.mdbc_options_groupbox
        ,self.stepalgorithm_configuration_group
        ,self.viscosity_configuration_group
        ,self.density_configuration_group
        ,self.shifting_options_groupbox
        ,self.timestep_configuration_group
        ,self.time_configuration_group
        ,self.simulation_values_configuration_group
        ,self.period_groupbox
        ,self.simulation_domain_groupbox]

        self.basic_widget_list=[
              self.kernel_widget
            , self.rigidalgorithm_widget
            , self.boundary_configuration_group
            , self.mdbc_options_groupbox
            , self.stepalgorithm_configuration_group
            , self.viscosity_configuration_group
            , self.density_configuration_group
            , self.shifting_options_groupbox
            , self.time_configuration_group
            , self.simulation_values_configuration_group
            , self.period_groupbox
            , self.simulation_domain_groupbox
        ]
        if ApplicationSettings.the().basic_visualization :
            self.widgetlist=self.basic_widget_list
        else:
            self.widgetlist=self.full_widget_list
        for widget in self.widgetlist:
            self.ep_main_layout.addWidget(widget)
        #Scroll
        self.ep_main_layout_scroll_widget.setLayout(self.ep_main_layout)
        self.ep_main_layout_scroll.setWidget(self.ep_main_layout_scroll_widget)
        self.ep_main_layout_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.execparams_window_layout = QtWidgets.QVBoxLayout()
        self.execparams_window_layout.addWidget(self.ep_main_layout_scroll)
        self.execparams_window_layout.addWidget(self.help_label)
        self.execparams_window_layout.addLayout(self.ep_button_layout)
        self.setLayout(self.execparams_window_layout)

        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setMinimumHeight(self.MINIMUM_HEIGHT)
        self.resize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)


    def on_help_focus(self, help_text):
        """ Reacts to focusing the help setting the corresponding help text. """
        self.help_label.setText("<b>{}: </b>{}".format(__("Help"), help_text))

    def on_boundary_type_change(self, index):
        """ Reacts to densitydt type change enabling/disabling the input. """
        if index == 0:
            self.mdbc_options_groupbox.setEnabled(False)
        else:
            self.mdbc_options_groupbox.setEnabled(True)

    def on_step_change(self, index):
        """ Reacts to step algorithm changing enabling/disabling the verletsteps option. """
        self.verletsteps_input.setEnabled(index == 0)

    def on_viscotreatment_change(self, index):
        """ Reacts to viscotreatment change. """
        self.visco_input.setValue(0.01 if index == 0 else 0.000001)
        self.visco_label.setText(__("Viscosity value (alpha):") if index == 0 else __("Kinematic viscosity: (m<span style='vertical-align:super'>2</span>/s)"))

    def on_densitydt_type_change(self, index):
        """ Reacts to densitydt type change enabling/disabling the input. """
        if index == 0:
            self.densitydt_input.setEnabled(False)
        else:
            self.densitydt_input.setEnabled(True)
            self.densitydt_input.setValue(0.1)

    def on_shifting_change(self, index):
        """ Reacts to the shifting mode change enabling/disabling its input. """
        self.shiftcoef_input.setEnabled(0 < index < 4)
        self.shifttfs_input.setEnabled(0 < index < 4)
        self.shiftadvcoef_input.setEnabled(index == 4)
        self.shiftadvale_input.setEnabled(index == 4)
        self.shiftadvncpress_input.setEnabled(index == 4)

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



    # ------------ Button behaviour definition --------------
    def on_ok(self):
        """ Applies the data from the dialog onto the main data structure. """
        Case.the().execution_parameters.saveposdouble = int(self.saveposdouble_input.currentIndex())
        Case.the().execution_parameters.boundary = int(self.boundary_input.currentIndex() + 1)

        Case.the().execution_parameters.slipmode = int(self.slipmode_input.currentIndex() + 1)
        Case.the().execution_parameters.nopenetration = int(self.nopenetration_input.currentIndex())
        Case.the().execution_parameters.stepalgorithm = int(self.stepalgorithm_input.currentIndex() + 1)
        Case.the().execution_parameters.verletsteps = self.verletsteps_input.value()
        Case.the().execution_parameters.kernel = int(self.kernel_input.currentIndex() + 1)
        Case.the().execution_parameters.viscotreatment = int(self.viscotreatment_input.currentIndex() + 1)
        Case.the().execution_parameters.visco = self.visco_input.value()
        Case.the().execution_parameters.viscoboundfactor = self.viscoboundfactor_input.value()
        Case.the().execution_parameters.densitydt_type = int(self.densitydt_type_input.currentIndex())
        Case.the().execution_parameters.densitydt_value = self.densitydt_input.value()
        Case.the().execution_parameters.shifting = int(self.shifting_input.currentIndex())
        Case.the().execution_parameters.shiftcoef = self.shiftcoef_input.value()
        Case.the().execution_parameters.shifttfs = self.shifttfs_input.value()
        Case.the().execution_parameters.shiftadvcoef = self.shiftadvcoef_input.value()
        Case.the().execution_parameters.shiftadvale = self.shiftadvale_input.value()
        Case.the().execution_parameters.shiftadvncpress = self.shiftadvncpress_input.value()

        Case.the().execution_parameters.rigidalgorithm = int(self.rigidalgorithm_input.currentIndex() + 1)
        Case.the().execution_parameters.ftpause = self.ftpause_input.value()
        Case.the().execution_parameters.coefdtmin = self.coefdtmin_input.value()
        Case.the().execution_parameters.dtini = self.dtini_input.value()
        Case.the().execution_parameters.dtini_auto = self.dtiniauto_chk.isChecked()
        Case.the().execution_parameters.dtmin = self.dtmin_input.value()
        Case.the().execution_parameters.dtmin_auto = self.dtminauto_chk.isChecked()
        #Case.the().execution_parameters.dtfixed = str(self.dtfixed_input.text())
        #Case.the().execution_parameters.dtallparticles = self.dtallparticles_input.value()
        Case.the().execution_parameters.timemax = self.timemax_input.value()
        Case.the().execution_parameters.timeout = self.timeout_input.value()
        #Case.the().execution_parameters.partsoutmax = self.partsoutmax_input.value() / 100
        Case.the().execution_parameters.minfluidstop = self.minfluidstop_input.value() / 100
        Case.the().execution_parameters.rhopoutmin = self.rhopoutmin_input.value()
        Case.the().execution_parameters.rhopoutmax = self.rhopoutmax_input.value()

        Case.the().execution_parameters.mdbc_disth = self.normals_disth_input.value()
        Case.the().execution_parameters.mdbc_maxsizeh = self.normals_maxsizeh_input.value()

        Case.the().periodicity = Periodicity()
        Case.the().periodicity.x_periodicity = PeriodicityInfo(
            self.period_x_chk.isChecked(),
            self.period_x_inc_x_input.value(),
            self.period_x_inc_y_input.value(),
            self.period_x_inc_z_input.value()
        )

        Case.the().periodicity.y_periodicity = PeriodicityInfo(
            self.period_y_chk.isChecked(),
            self.period_y_inc_x_input.value(),
            self.period_y_inc_y_input.value(),
            self.period_y_inc_z_input.value()
        )

        Case.the().periodicity.z_periodicity = PeriodicityInfo(
            self.period_z_chk.isChecked(),
            self.period_z_inc_x_input.value(),
            self.period_z_inc_y_input.value(),
            self.period_z_inc_z_input.value()
        )

        Case.the().domain=self.sim_domain_widget.save()
        if Case.the().domain.enabled:
            Case.the().execution_parameters.incz = 0
        if Case.the().domain.posmin_x.type==SDPositionPropertyType.VALUE and \
            Case.the().domain.posmin_y.type == SDPositionPropertyType.VALUE and \
            Case.the().domain.posmin_z.type == SDPositionPropertyType.VALUE and \
            Case.the().domain.posmax_x.type == SDPositionPropertyType.VALUE and \
            Case.the().domain.posmax_y.type == SDPositionPropertyType.VALUE and \
            Case.the().domain.posmax_z.type == SDPositionPropertyType.VALUE :
                update_simulation_domain(Case.the().domain.posmin_x.value,
                                       Case.the().domain.posmin_y.value,
                                       Case.the().domain.posmin_z.value,
                                       Case.the().domain.posmax_x.value,
                                       Case.the().domain.posmax_y.value,
                                       Case.the().domain.posmax_z.value,)

        FreeCADGui.Selection.clearSelection() #Clear selection to refresh
        #self.update_properties()
        log("Execution Parameters changed")
        self.accept()

    def on_cancel(self):
        """ Cancels the dialog rejecting it. """
        log("Execution Parameters not changed")
        self.reject()


    '''   def update_properties(self):
        selection = FreeCADGui.Selection.getSelection()
        properties_widget=FreeCADGui.getMainWindow().findChildren(QtWidgets.QWidget,"DSPH_Properties")[0]
        if selection:
            if len(selection) > 1:
                # Multiple objects selected
                properties_widget.configure_to_add_multiple_selection()
            else:
                # One object selected
                if selection[0].Name == "Case_Limits" or "_internal_" in selection[0].Name:
                    properties_widget.configure_to_no_selection()
                elif Case.the().is_damping_bound_to_object(selection[0].Name):
                    properties_widget.configure_to_damping_selection()
                elif Case.the().is_object_in_simulation(selection[0].Name):
                    # Show properties on table
                    properties_widget.configure_to_regular_selection()
                    properties_widget.adapt_to_simulation_object(Case.the().get_simulation_object(selection[0].Name),
                                                                 selection[0])
    '''