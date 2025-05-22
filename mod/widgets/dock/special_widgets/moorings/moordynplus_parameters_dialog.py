#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus Parameters Configuration Dialog. """

from uuid import UUID

from PySide2 import QtWidgets, QtCore
from mod.dataobjects.moorings.moordynplus.moordynplus_configuration import MoorDynPlusConfiguration
from mod.dataobjects.moorings.moordynplus.moordynplus_line import MoorDynPlusLine
from mod.dataobjects.moorings.moordynplus.moordynplus_line_default_configuration import MoorDynPlusLineDefaultConfiguration
from mod.dataobjects.moorings.moordynplus.moordynplus_solver_options import MoorDynPlusSolverOptions
from mod.enums import ObjectType
from mod.tools.gui_tools import get_icon
from mod.tools.stdout_tools import log
from mod.tools.dialog_tools import warning_dialog
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.dock.special_widgets.moorings.moordynplus_body_configuration_dialog import MoorDynPlusBodyConfigurationDialog
from mod.widgets.dock.special_widgets.moorings.moordynplus_line_configuration_dialog import MoorDynPlusLineConfigurationDialog

class MoorDynPlusBodyWidget(QtWidgets.QWidget):
    """ Widget to embed in each element of the body list for the MoorDynPlus configuration dialog. """

    configure_clicked = QtCore.Signal(int)

    def __init__(self, obj_type: ObjectType, mk: int):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.root_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.root_layout.setContentsMargins(5, 1, 5, 1)
        self.mk = mk

        self.mk_label: QtWidgets.QLabel = QtWidgets.QLabel("{} - <b>{}</b>".format(obj_type.capitalize(), str(self.mk)))

        self.configure_button: QtWidgets.QPushButton = QtWidgets.QPushButton(__("Configure"))

        self.root_layout.addWidget(self.mk_label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.configure_button)

        self.configure_button.clicked.connect(lambda _=False, mk=self.mk: self.configure_clicked.emit(mk))

        self.setLayout(self.root_layout)


class MoorDynPlusLineWidget(QtWidgets.QWidget):
    """ Widget to embed in each element of the line list for the MoorDynPlus configuration dialog. """

    configure_clicked = QtCore.Signal(UUID)
    delete_clicked = QtCore.Signal(UUID)

    def __init__(self, line_id, row):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.root_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.root_layout.setContentsMargins(5, 1, 5, 1)

        self.line_id = line_id
        self.row = row

        self.label: QtWidgets.QLabel = QtWidgets.QLabel("Line {}".format(self.line_id))

        self.configure_button: QtWidgets.QPushButton = QtWidgets.QPushButton(__("Configure"))
        self.delete_button = QtWidgets.QPushButton(get_icon("trash.png"), None)

        self.root_layout.addWidget(self.label)
        self.root_layout.addStretch(1)
        self.root_layout.addWidget(self.configure_button)
        self.root_layout.addWidget(self.delete_button)

        self.configure_button.clicked.connect(lambda _=False, line_id=self.line_id: self.configure_clicked.emit(line_id))
        self.delete_button.clicked.connect(lambda _=False, line_id=self.line_id: self.delete_clicked.emit(line_id))

        self.setLayout(self.root_layout)


class MoorDynPlusParametersDialog(QtWidgets.QDialog):
    """ DesignSPHysics MoorDynPlus Parameters Configuration Dialog. """

    def __init__(self, moordynplus_parameters_data: MoorDynPlusConfiguration):
        super().__init__()
        self.setWindowTitle(__("MoorDynPlus Parameters Configuration"))

        self.stored_configuration: MoorDynPlusConfiguration = moordynplus_parameters_data  # Can be None

        self.setMinimumSize(640, 480)
        self.root_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.root_scroll: QtWidgets.QScrollArea = QtWidgets.QScrollArea()
        self.root_scroll.setMinimumWidth(400)
        self.root_scroll.setWidgetResizable(True)
        self.scroll_widget: QtWidgets.QWidget = QtWidgets.QWidget()
        self.scroll_widget.setMinimumWidth(400)
        self.scroll_widget_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        # Solver options groupbox
        self.solver_options_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Solver Options"))
        self.solver_options_groupbox_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.solver_options_groupbox.setLayout(self.solver_options_groupbox_layout)


        #MAin solver options
        self.dtM_line_edit  = ValueInput(decimals=7)
        self.dtM_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.dtM_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.dtM_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.dtM_line_edit_layout.addWidget(self.dtM_line_edit)
        self.dtM_line_edit_layout.addWidget(self.dtM_line_check)

        self.tmaxIC_line_edit = ValueInput()
        self.water_depth_line_edit  = ValueInput()
        self.freesurface_line_edit  = ValueInput()

        self.dtM_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Mooring model time step. (s):"))
        self.dtM_label.setToolTip(__("Desired mooring model time step. (default=1e-4)\nXML Name: dtM"))
        self.tmaxIC_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Max. time for initial conditions (s):"))
        self.tmaxIC_label.setToolTip(
            __("Maximum time for initial conditions without convergence. (default=0.5)\nXML Name: tmaxIC"))

        self.water_depth_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Water Depth (m):"))
        self.water_depth_label.setToolTip(__("Gravitational constant. (default=9.81)\nXML Name: waterDepth"))
        self.freesurface_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Free Surface (m):"))
        self.freesurface_label.setToolTip(__("Z position of the water free surface.(default=0\nXML Name: waterDepth"))

        self.solver_options_groupbox_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.solver_options_groupbox_layout.addRow(self.dtM_label, self.dtM_line_edit_layout)
        self.solver_options_groupbox_layout.addRow(self.tmaxIC_label, self.tmaxIC_line_edit)
        self.solver_options_groupbox_layout.addRow(self.water_depth_label, self.water_depth_line_edit)
        self.solver_options_groupbox_layout.addRow(self.freesurface_label, self.freesurface_line_edit)

        #Advanced solvver options (hiddeable)
        self.solver_advanced_options_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Advanced Solver Options"))
        self.solver_advanced_options_groupbox.setCheckable(True)
        self.solver_advanced_options_groupbox.setChecked(False)
        self.solver_advanced_options_widget = QtWidgets.QWidget()
        self.solver_advanced_options_layout = QtWidgets.QFormLayout()
        self.solver_advanced_options_groupbox_layout = QtWidgets.QVBoxLayout()
        self.solver_advanced_options_groupbox.setLayout(self.solver_advanced_options_groupbox_layout)
        self.solver_advanced_options_widget.setLayout(self.solver_advanced_options_layout)
        self.solver_advanced_options_widget.setVisible(False)
        self.solver_advanced_options_groupbox_layout.addWidget(self.solver_advanced_options_widget)


        self.kBot_line_edit  = ValueInput()
        self.kBot_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.kBot_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.kBot_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.kBot_line_edit_layout.addWidget(self.kBot_line_edit)
        self.kBot_line_edit_layout.addWidget(self.kBot_line_check)

        self.cBot_line_edit  = ValueInput()
        self.cBot_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.cBot_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.cBot_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.cBot_line_edit_layout.addWidget(self.cBot_line_edit)
        self.cBot_line_edit_layout.addWidget(self.cBot_line_check)

        self.fricdamp_line_edit  = ValueInput()
        self.statdynfricscale_line_edit  = ValueInput()
        self.dtIC_line_edit  = ValueInput()
        self.cdScaleIC_line_edit  = ValueInput()

        # self.timeMax_line_edit  = ValueInput() Not in use

        self.kBot_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Bottom stiffness constant (Pa/m):"))
        self.kBot_label.setToolTip(__("Bottom stiffness constant. (default=3.0e6)\nXML Name: kBot"))
        self.cBot_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Bottom damping constant (Pa*s/m):"))
        self.cBot_label.setToolTip(__("Bottom damping constant. (default=3.0e5)\nXML Name: cBot"))
        self.fricdamp_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Damping coefficient:"))
        self.fricdamp_label.setToolTip(__("Damping coefficient used to model the friction at speeds near zero. (default=200.0)\nXML Name: fricDamp"))
        self.statdynfricscale_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Ratio between static/dynamic friction:"))
        self.statdynfricscale_label.setToolTip(__("Ratio between static and dynamic friction (mu_static/mu_dynamic). (default=1.0)\nXML Name: statDynFricScale"))
        self.dtIC_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Convergence analysis time step (s):"))
        self.dtIC_label.setToolTip(__("Period to analyze convergence of dynamic relaxation for initial conditions. (default=1.0)\nXML Name: dtIC"))
        self.cdScaleIC_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Factor to scale drag coefficients:"))
        self.cdScaleIC_label.setToolTip(__("Factor to scale drag coefficients during dynamic relaxation for initial conditions. (default=5)\nXML Name: cdScaleIC"))
        #self.timeMax_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Simulation Time (s):"))
        #self.timeMax_label.setToolTip(__("Time of simulation(s)\nXML Name: timeMax"))

        self.solver_advanced_options_widgets_list=[
            (self.kBot_label, self.kBot_line_edit_layout),
            (self.cBot_label, self.cBot_line_edit_layout),
            (self.fricdamp_label, self.fricdamp_line_edit),
            (self.statdynfricscale_label, self.statdynfricscale_line_edit),
            (self.dtIC_label, self.dtIC_line_edit),
            (self.cdScaleIC_label, self.cdScaleIC_line_edit)
        ]

        self.solver_advanced_options_layout.setLabelAlignment(QtCore.Qt.AlignLeft)

        for row in self.solver_advanced_options_widgets_list:
            self.solver_advanced_options_layout.addRow(*row)
        self.solver_advanced_options_groupbox.setLayout(self.solver_advanced_options_groupbox_layout)

        # Body configuration groupbox
        self.body_configuration_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Body configuration"))
        self.body_configuration_groupbox_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.body_configuration_table: QtWidgets.QTableWidget = QtWidgets.QTableWidget()
        self.body_configuration_table.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)
        self.body_configuration_table.horizontalHeader().hide()
        self.body_configuration_table.verticalHeader().hide()
        self.body_configuration_table.setRowCount(0)
        self.body_configuration_table.setColumnCount(1)
        self.body_configuration_groupbox_layout.addWidget(self.body_configuration_table)
        self.body_configuration_groupbox.setLayout(self.body_configuration_groupbox_layout)

        # Line default configuration groupbox
        self.line_default_configuration_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Line default configuration"))
        self.line_default_configuration_groupbox_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.ea_line_edit  = ValueInput()
        self.diameter_line_edit  = ValueInput(decimals=6)
        self.massDenInAir_line_edit  = ValueInput(decimals=6)

        self.ea_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Line Stiffness (N):"))
        self.ea_label.setToolTip(
            __("Line stiffness, product of elasticity modulus and cross-sectional area.\nXML Name: ea"))
        self.diameter_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Diameter (m):"))
        self.diameter_label.setToolTip(__("Volume-equivalent diameter of the line.\nXML Name: diameter"))
        self.massDenInAir_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Mass per unit length (kg/m):"))
        self.massDenInAir_label.setToolTip(__("Mass per unit length of the line.\nXML Name: massDenInAir"))

        self.line_default_configuration_groupbox_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.line_default_configuration_groupbox_layout.addRow(self.ea_label, self.ea_line_edit)
        self.line_default_configuration_groupbox_layout.addRow(self.diameter_label, self.diameter_line_edit)
        self.line_default_configuration_groupbox_layout.addRow(self.massDenInAir_label, self.massDenInAir_line_edit)
        self.line_default_configuration_groupbox.setLayout(self.line_default_configuration_groupbox_layout)

        #Advanced line configuration (hideable)
        self.line_default_advanced_configuration_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        self.line_default_advanced_configuration_widget: QtWidgets.QWidget = QtWidgets.QWidget()
        self.line_default_advanced_configuration_widget.setVisible(False)
        self.line_default_advanced_configuration_widget.setLayout(self.line_default_advanced_configuration_layout)
        self.line_default_advanced_configuration_groupbox_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.line_default_advanced_configuration_groupbox_layout.addWidget(self.line_default_advanced_configuration_widget)
        self.line_default_advanced_configuration_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(
            __("Advanced line configuration"))
        self.line_default_advanced_configuration_groupbox.setCheckable(True)
        self.line_default_advanced_configuration_groupbox.setChecked(False)
        self.line_default_advanced_configuration_groupbox.setLayout(
            self.line_default_advanced_configuration_groupbox_layout)

        self.ba_line_edit  = ValueInput()
        self.ba_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.ba_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.ba_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.ba_line_edit_layout.addWidget(self.ba_line_edit)
        self.ba_line_edit_layout.addWidget(self.ba_line_check)

        self.can_line_edit  = ValueInput()
        self.can_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.can_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.can_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.can_line_edit_layout.addWidget(self.can_line_edit)
        self.can_line_edit_layout.addWidget(self.can_line_check)

        self.cat_line_edit  = ValueInput()
        self.cat_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.cat_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.cat_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_line_edit_layout.addWidget(self.cat_line_edit)
        self.cat_line_edit_layout.addWidget(self.cat_line_check)

        self.cdn_line_edit  = ValueInput()
        self.cdn_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.cdn_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.cdn_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.cdn_line_edit_layout.addWidget(self.cdn_line_edit)
        self.cdn_line_edit_layout.addWidget(self.cdn_line_check)

        self.cdt_line_edit  = ValueInput()
        self.cdt_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.cdt_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.cdt_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.cdt_line_edit_layout.addWidget(self.cdt_line_edit)
        self.cdt_line_edit_layout.addWidget(self.cdt_line_check)

        self.breaktension_line_edit  = ValueInput()
        self.breaktension_line_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Auto"))
        self.breaktension_line_edit_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.breaktension_line_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.breaktension_line_edit_layout.addWidget(self.breaktension_line_edit)
        self.breaktension_line_edit_layout.addWidget(self.breaktension_line_check)


        self.ba_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Line internal damping (Ns):"))
        self.ba_label.setToolTip(__("Line internal damping (BA/-zeta). (default=-0.8)\nXML Name: ba"))
        self.can_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Transverse added mass coefficient:"))
        self.can_label.setToolTip(__("Transverse added mass coefficient (with respect to line displacement). (default=1.0)\nXML Name: can"))
        self.cat_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Tangential added mass coefficient:"))
        self.cat_label.setToolTip(__("Tangential added mass coefficient (with respect to line displacement). (default=0.0)\nXML Name: cat"))
        self.cdn_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Transverse drag coefficient:"))
        self.cdn_label.setToolTip(__("Transverse drag coefficient (with respect to frontal area, d*l). (default=1.6)\nXML Name: cdn"))
        self.cdt_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Tangential drag coefficient:"))
        self.cdt_label.setToolTip(__("Tangential drag coefficient (with respect to surface area, π*d*l). (default=0.05)\nXML Name: cdt"))
        self.breaktension_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Maximum tension for the lines (N):"))
        self.breaktension_label.setToolTip(__("Maximum value of tension for the lines. value=0 Break Tension is not used. (default=0)\nXML Name: breaktension"))

        self.line_default_advanced_configuration_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.line_default_advanced_configuration_layout.addRow(self.ba_label, self.ba_line_edit_layout)
        self.line_default_advanced_configuration_layout.addRow(self.can_label, self.can_line_edit_layout)
        self.line_default_advanced_configuration_layout.addRow(self.cat_label, self.cat_line_edit_layout)
        self.line_default_advanced_configuration_layout.addRow(self.cdn_label, self.cdn_line_edit_layout)
        self.line_default_advanced_configuration_layout.addRow(self.cdt_label, self.cdt_line_edit_layout)
        self.line_default_advanced_configuration_layout.addRow(self.breaktension_label, self.breaktension_line_edit_layout)



        # Lines groupbox
        self.lines_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Lines"))
        self.lines_groupbox_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.lines_table: QtWidgets.QTableWidget = QtWidgets.QTableWidget()
        self.lines_table.setRowCount(0)
        self.lines_table.setColumnCount(1)
        self.lines_table.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)
        self.lines_table.horizontalHeader().hide()
        self.lines_table.verticalHeader().hide()
        self.add_line_button: QtWidgets.QPushButton = QtWidgets.QPushButton(__("Add a new Line"))
        self.lines_groupbox_layout.addWidget(self.lines_table)
        self.lines_groupbox_layout.addWidget(self.add_line_button)
        self.lines_groupbox.setLayout(self.lines_groupbox_layout)

        # Bottom button row
        self.bottom_button_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.ok_button: QtWidgets.QPushButton = QtWidgets.QPushButton(__("OK"))

        self.bottom_button_layout.addStretch(1)
        self.bottom_button_layout.addWidget(self.ok_button)

        # Root layout composition
        self.scroll_widget_layout.addWidget(self.solver_options_groupbox)
        self.scroll_widget_layout.addWidget(self.solver_advanced_options_groupbox)
        self.scroll_widget_layout.addWidget(self.body_configuration_groupbox)
        self.scroll_widget_layout.addWidget(self.line_default_configuration_groupbox)
        self.scroll_widget_layout.addWidget(self.line_default_advanced_configuration_groupbox)
        self.scroll_widget_layout.addWidget(self.lines_groupbox)

        self.scroll_widget.setLayout(self.scroll_widget_layout)

        self.root_scroll.setWidget(self.scroll_widget)
        self.root_layout.addWidget(self.root_scroll)
        self.root_layout.addLayout(self.bottom_button_layout)
        self.setLayout(self.root_layout)

        # Bind connections
        self.dtM_line_check.stateChanged.connect(self._on_dtM_check)
        self.kBot_line_check.stateChanged.connect(self._on_kBot_check)
        self.cBot_line_check.stateChanged.connect(self._on_cBot_check)
        self.ba_line_check.stateChanged.connect(self._on_ba_check)
        self.can_line_check.stateChanged.connect(self._on_can_check)
        self.cat_line_check.stateChanged.connect(self._on_cat_check)
        self.cdn_line_check.stateChanged.connect(self._on_cdn_check)
        self.cdt_line_check.stateChanged.connect(self._on_cdt_check)
        self.breaktension_line_check.stateChanged.connect(self._on_breaktension_check)
        self.ok_button.clicked.connect(self._on_ok)
        self.add_line_button.clicked.connect(self._on_add_new_line)
        self.solver_advanced_options_groupbox.clicked.connect(self._on_advanced_options_check)
        self.line_default_advanced_configuration_groupbox.clicked.connect(self._on_line_advanced_options_check)

        # Populate data
        self._fill_data()
        self.exec_()

    def _on_ok(self):
        # Solver options
        default_solver_options = MoorDynPlusSolverOptions()
        self.stored_configuration.solver_options.dtM = default_solver_options.dtM if self.dtM_line_check.isChecked() else self.dtM_line_edit.value()
        self.stored_configuration.solver_options.dtMauto = self.dtM_line_check.isChecked()
        self.stored_configuration.solver_options.kBot = default_solver_options.kBot if self.kBot_line_check.isChecked() else self.kBot_line_edit.value()
        self.stored_configuration.solver_options.cBot = default_solver_options.cBot if self.cBot_line_check.isChecked() else self.cBot_line_edit.value()
        self.stored_configuration.solver_options.water_depth = self.water_depth_line_edit.value()
        self.stored_configuration.solver_options.freesurface = self.freesurface_line_edit.value()
        self.stored_configuration.solver_options.fricDamp = self.fricdamp_line_edit.value()
        self.stored_configuration.solver_options.statDynFricScale = self.statdynfricscale_line_edit.value()
        self.stored_configuration.solver_options.dtIC = self.dtIC_line_edit.value()
        self.stored_configuration.solver_options.cdScaleIC = self.cdScaleIC_line_edit.value()
        self.stored_configuration.solver_options.tmaxIC = self.tmaxIC_line_edit.value()
        #self.stored_configuration.solver_options.timeMax = self.timeMax_line_edit.value()

        # Line default config
        default_line_default_configuration = MoorDynPlusLineDefaultConfiguration()
        self.stored_configuration.line_default_configuration.ea = self.ea_line_edit.value()
        self.stored_configuration.line_default_configuration.diameter = self.diameter_line_edit.value()
        self.stored_configuration.line_default_configuration.massDenInAir = self.massDenInAir_line_edit.value()
        self.stored_configuration.line_default_configuration.ba = default_line_default_configuration.ba if self.ba_line_check.isChecked() else self.ba_line_edit.value()
        self.stored_configuration.line_default_configuration.can = default_line_default_configuration.can if self.can_line_check.isChecked() else self.can_line_edit.value()
        self.stored_configuration.line_default_configuration.cat = default_line_default_configuration.cat if self.cat_line_check.isChecked() else self.cat_line_edit.value()
        self.stored_configuration.line_default_configuration.cdn = default_line_default_configuration.cdn if self.cdn_line_check.isChecked() else self.cdn_line_edit.value()
        self.stored_configuration.line_default_configuration.cdt = default_line_default_configuration.cdt if self.cdt_line_check.isChecked() else self.cdt_line_edit.value()
        self.stored_configuration.line_default_configuration.breaktension = default_line_default_configuration.breaktension if self.breaktension_line_check.isChecked() else self.breaktension_line_edit.value()

        if len(self.stored_configuration.lines)<=0:
            warning_dialog("No mooring lines have been defined.")
        else:
            # Bodies and lines are references to lists, so they're already modified in memory :)
            self.accept()

    def _on_dtM_check(self):
        self.dtM_line_edit.setEnabled(not self.dtM_line_check.isChecked())

    def _on_kBot_check(self):
        self.kBot_line_edit.setEnabled(not self.kBot_line_check.isChecked())

    def _on_cBot_check(self):
        self.cBot_line_edit.setEnabled(not self.cBot_line_check.isChecked())

    def _on_ba_check(self):
        self.ba_line_edit.setEnabled(not self.ba_line_check.isChecked())

    def _on_can_check(self):
        self.can_line_edit.setEnabled(not self.can_line_check.isChecked())

    def _on_cat_check(self):
        self.cat_line_edit.setEnabled(not self.cat_line_check.isChecked())

    def _on_cdn_check(self):
        self.cdn_line_edit.setEnabled(not self.cdn_line_check.isChecked())

    def _on_cdt_check(self):
        self.cdt_line_edit.setEnabled(not self.cdt_line_check.isChecked())

    def _on_breaktension_check(self):
        self.breaktension_line_edit.setEnabled(not self.breaktension_line_check.isChecked())

    def _on_add_new_line(self):
        used_line_ids = list(map(lambda line: line.line_id, self.stored_configuration.lines))
        log("Line ids currently in use: {}".format(used_line_ids))
        for i in range(0, 999):  # Note: I hope no one tries to create more lines...
            if i not in used_line_ids:
                break
        log("Found this appropriate int for a new line id: {}".format(i))

        new_line: MoorDynPlusLine = MoorDynPlusLine(i)
        self.stored_configuration.lines.append(new_line)
        self.lines_table.setRowCount(self.lines_table.rowCount() + 1)
        widget: MoorDynPlusLineWidget = MoorDynPlusLineWidget(new_line.line_id, self.lines_table.rowCount() - 1)
        widget.configure_clicked.connect(lambda line_id=None: self._on_configure_line(line_id))
        widget.delete_clicked.connect(lambda line_id=None: self._on_delete_line(line_id))
        self.lines_table.setCellWidget(self.lines_table.rowCount() - 1, 0, widget)

    def _on_delete_line(self, line_id):
        log("Deleting line {}".format(line_id))
        self.stored_configuration.lines = list(filter(lambda line: line.line_id != line_id, self.stored_configuration.lines))

        index_to_delete: int = 0
        for i in range(0, self.lines_table.rowCount()):
            if self.lines_table.cellWidget(i, 0).line_id == line_id:
                index_to_delete = i
                break

        self.lines_table.removeRow(index_to_delete)

        for index in range(0, self.lines_table.rowCount()):
            target_widget: MoorDynPlusLineWidget = self.lines_table.cellWidget(index, 0)
            target_widget.row = index
            self.lines_table.setCellWidget(index, 0, target_widget)

    def _on_configure_line(self, line_id):
        selected_line = next(filter(lambda line: line.line_id == line_id, self.stored_configuration.lines), None)
        if not selected_line:
            raise RuntimeError("The specified line to configure does not exist in the list of lines.")
        MoorDynPlusLineConfigurationDialog(selected_line, self.stored_configuration)

    def _on_configure_body(self, mkbound):
        selected_body = next(filter(lambda body: body.ref == mkbound, self.stored_configuration.bodies), None)
        if not selected_body:
            raise RuntimeError("The specified body to configure does not exist in the list of bodies.")
        MoorDynPlusBodyConfigurationDialog(selected_body)

    def _on_advanced_options_check(self,check):
        self.solver_advanced_options_widget.setVisible(check)



    def _on_line_advanced_options_check(self,check):
        self.line_default_advanced_configuration_widget.setVisible(check)

    def _fill_data(self):
        # Solver options
        default_solver_options = MoorDynPlusSolverOptions()
        self.dtM_line_edit.setValue(self.stored_configuration.solver_options.dtM)
        self.dtM_line_check.setChecked(self.stored_configuration.solver_options.dtM == default_solver_options.dtM)
        self.kBot_line_edit.setValue(self.stored_configuration.solver_options.kBot)
        self.kBot_line_check.setChecked(self.stored_configuration.solver_options.kBot == default_solver_options.kBot)
        self.cBot_line_edit.setValue(self.stored_configuration.solver_options.cBot)
        self.cBot_line_check.setChecked(self.stored_configuration.solver_options.cBot == default_solver_options.cBot)
        self.water_depth_line_edit.setValue(self.stored_configuration.solver_options.water_depth)
        self.freesurface_line_edit.setValue(self.stored_configuration.solver_options.freesurface)
        self.fricdamp_line_edit.setValue(self.stored_configuration.solver_options.fricDamp)
        self.statdynfricscale_line_edit.setValue(self.stored_configuration.solver_options.statDynFricScale)
        self.dtIC_line_edit.setValue(self.stored_configuration.solver_options.dtIC)
        self.cdScaleIC_line_edit.setValue(self.stored_configuration.solver_options.cdScaleIC)
        self.tmaxIC_line_edit.setValue(self.stored_configuration.solver_options.tmaxIC)
        #self.timeMax_line_edit.setValue(self.stored_configuration.solver_options.timeMax)

        # Bodies
        self.body_configuration_table.setRowCount(len(self.stored_configuration.bodies))
        for index, body in enumerate(self.stored_configuration.bodies):
            widget: MoorDynPlusBodyWidget = MoorDynPlusBodyWidget(ObjectType.BOUND, body.ref)
            widget.configure_clicked.connect(lambda mkbound=None: self._on_configure_body(mkbound))
            self.body_configuration_table.setCellWidget(index, 0, widget)

        # Line default config
        default_line_default_configuration = MoorDynPlusLineDefaultConfiguration()
        self.ea_line_edit.setValue(self.stored_configuration.line_default_configuration.ea)
        self.diameter_line_edit.setValue(self.stored_configuration.line_default_configuration.diameter)
        self.massDenInAir_line_edit.setValue(self.stored_configuration.line_default_configuration.massDenInAir)
        self.ba_line_edit.setValue(self.stored_configuration.line_default_configuration.ba)
        self.ba_line_check.setChecked(self.stored_configuration.line_default_configuration.ba == default_line_default_configuration.ba)
        self.can_line_edit.setValue(self.stored_configuration.line_default_configuration.can)
        self.can_line_check.setChecked(self.stored_configuration.line_default_configuration.can == default_line_default_configuration.can)
        self.cat_line_edit.setValue(self.stored_configuration.line_default_configuration.cat)
        self.cat_line_check.setChecked(self.stored_configuration.line_default_configuration.cat == default_line_default_configuration.cat)
        self.cdn_line_edit.setValue(self.stored_configuration.line_default_configuration.cdn)
        self.cdn_line_check.setChecked(self.stored_configuration.line_default_configuration.cdn == default_line_default_configuration.cdn)
        self.cdt_line_edit.setValue(self.stored_configuration.line_default_configuration.cdt)
        self.cdt_line_check.setChecked(self.stored_configuration.line_default_configuration.cdt == default_line_default_configuration.cdt)
        self.breaktension_line_edit.setValue(self.stored_configuration.line_default_configuration.breaktension)
        self.breaktension_line_check.setChecked(self.stored_configuration.line_default_configuration.breaktension == default_line_default_configuration.breaktension)

        # Lines
        self.lines_table.setRowCount(len(self.stored_configuration.lines))
        for index, line in enumerate(self.stored_configuration.lines):
            widget: MoorDynPlusLineWidget = MoorDynPlusLineWidget(line.line_id, index)
            widget.configure_clicked.connect(lambda line_id=None: self._on_configure_line(line_id))
            widget.delete_clicked.connect(lambda line_id=None: self._on_delete_line(line_id))
            self.lines_table.setCellWidget(index, 0, widget)

        # Refresh appropriate widgets
        self._on_dtM_check()
        self._on_kBot_check()
        self._on_cBot_check()
        self._on_ba_check()
        self._on_can_check()
        self._on_cat_check()
        self._on_cdn_check()
        self._on_cdt_check()
        self._on_breaktension_check()
