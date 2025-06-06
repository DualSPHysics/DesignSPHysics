#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDynPlus Line Configuration Dialog. """


from PySide2 import QtWidgets
from mod.dataobjects.moorings.moordynplus.moordynplus_fix_connection import MoorDynPlusFixConnection
from mod.dataobjects.moorings.moordynplus.moordynplus_line import MoorDynPlusLine
from mod.dataobjects.moorings.moordynplus.moordynplus_vessel_connection import MoorDynPlusVesselConnection
from mod.tools.dialog_tools import warning_dialog
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.int_value_input import IntValueInput


class MoorDynPlusLineConfigurationDialog(QtWidgets.QDialog):
    """ DesignSPHysics MoorDynPlus Line Configuration Dialog. """

    def __init__(self, line, stored_configuration):
        super().__init__()
        self.line: MoorDynPlusLine = line
        self.stored_configuration = stored_configuration

        self.setWindowTitle(__("MoorDynPlus Line Configuration"))
        self.setMinimumWidth(440)
        self.root_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        # Label
        self.reference_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Editing settings for line: <b>{}</b>").format(line.line_id))

        # Basic configuration group
        self.basic_configuration_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Basic configuration"))
        self.basic_configuration_groupbox_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()

        self.connection_type_combobox: QtWidgets.QComboBox = QtWidgets.QComboBox()
        self.connection_type_combobox.addItems([
            "Vessel to Fix connection",
            "Vessel to Vessel connection"
        ])

        self.vessel_connection_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Vessel Connection: "))
        self.vessel_connection_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.vessel_connection_body_combo: QtWidgets.QComboBox = QtWidgets.QComboBox()
        self.vessel_connection_point_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Point (X, Y, Z):"))
        self.vessel_connection_point_x  = SizeInput()
        self.vessel_connection_point_y  = SizeInput()
        self.vessel_connection_point_z  = SizeInput()

        self.vessel_connection_layout.addWidget(self.vessel_connection_body_combo)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_label)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_x)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_y)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_z)

        self.vessel2_connection_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Vessel Connection (2nd): "))
        self.vessel2_connection_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.vessel2_connection_body_combo: QtWidgets.QComboBox = QtWidgets.QComboBox()
        self.vessel2_connection_point_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Point (X, Y, Z):"))
        self.vessel2_connection_point_x  = SizeInput()
        self.vessel2_connection_point_y  = SizeInput()
        self.vessel2_connection_point_z  = SizeInput()

        self.vessel2_connection_layout.addWidget(self.vessel2_connection_body_combo)
        self.vessel2_connection_layout.addWidget(self.vessel2_connection_point_label)
        self.vessel2_connection_layout.addWidget(self.vessel2_connection_point_x)
        self.vessel2_connection_layout.addWidget(self.vessel2_connection_point_y)
        self.vessel2_connection_layout.addWidget(self.vessel2_connection_point_z)

        self.fix_connection_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Fix Connection (X, Y, Z): "))
        self.fix_connection_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.fix_connection_point_x  = SizeInput()
        self.fix_connection_point_y  = SizeInput()
        self.fix_connection_point_z  = SizeInput()

        self.fix_connection_layout.addWidget(self.fix_connection_point_x)
        self.fix_connection_layout.addWidget(self.fix_connection_point_y)
        self.fix_connection_layout.addWidget(self.fix_connection_point_z)

        self.length_input  = SizeInput()
        self.segments_input  = IntValueInput(min_val=1)

        self.basic_configuration_groupbox_layout.addRow(__("Type of connection: "), self.connection_type_combobox)
        self.basic_configuration_groupbox_layout.addRow(self.vessel_connection_label, self.vessel_connection_layout)
        self.basic_configuration_groupbox_layout.addRow(self.vessel2_connection_label, self.vessel2_connection_layout)
        self.basic_configuration_groupbox_layout.addRow(self.fix_connection_label, self.fix_connection_layout)
        self.basic_configuration_groupbox_layout.addRow(h_line_generator())
        self.basic_configuration_groupbox_layout.addRow(__("Line Length:"), self.length_input)
        self.basic_configuration_groupbox_layout.addRow(__("Number of Segments:"), self.segments_input)
        self.basic_configuration_groupbox.setLayout(self.basic_configuration_groupbox_layout)

        # Override configuration group
        self.override_configuration_groupbox: QtWidgets.QGroupBox = QtWidgets.QGroupBox(__("Configuration Overrides"))
        self.override_configuration_groupbox_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout()

        self.ea_input  = ValueInput()
        self.ea_input_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        self.ea_input_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.ea_input_layout.addWidget(self.ea_input)
        self.ea_input_layout.addWidget(self.ea_input_check)

        self.diameter_input  = SizeInput()
        self.diameter_input_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        self.diameter_input_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.diameter_input_layout.addWidget(self.diameter_input)
        self.diameter_input_layout.addWidget(self.diameter_input_check)

        self.massDenInAir_input  = ValueInput()
        self.massDenInAir_input_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        self.massDenInAir_input_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.massDenInAir_input_layout.addWidget(self.massDenInAir_input)
        self.massDenInAir_input_layout.addWidget(self.massDenInAir_input_check)

        self.ba_input  = ValueInput()
        self.ba_input_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        self.ba_input_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.ba_input_layout.addWidget(self.ba_input)
        self.ba_input_layout.addWidget(self.ba_input_check)

        self.override_configuration_groupbox_layout.addRow(__("Stiffness (N):"), self.ea_input_layout)
        self.override_configuration_groupbox_layout.addRow(__("Diameter:"), self.diameter_input_layout)
        self.override_configuration_groupbox_layout.addRow(__("Mass in Air (kg/m):"), self.massDenInAir_input_layout)
        self.override_configuration_groupbox_layout.addRow(__("Line internal damping (Ns):"), self.ba_input_layout)

        self.override_configuration_groupbox.setLayout(self.override_configuration_groupbox_layout)

        # Bottom button row
        self.button_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.ok_button: QtWidgets.QPushButton = QtWidgets.QPushButton(__("OK"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)

        # Main layout composition
        self.root_layout.addWidget(self.reference_label)
        self.root_layout.addWidget(h_line_generator())
        self.root_layout.addWidget(self.basic_configuration_groupbox)
        # self.root_layout.addWidget(self.override_configuration_groupbox)
        self.root_layout.addStretch(1)
        self.root_layout.addLayout(self.button_layout)
        self.setLayout(self.root_layout)

        # Connections
        self.ok_button.clicked.connect(self._on_ok)
        self.ea_input_check.stateChanged.connect(self._on_ea_check)
        self.diameter_input_check.stateChanged.connect(self._on_diameter_check)
        self.massDenInAir_input_check.stateChanged.connect(self._on_massDenInAir_check)
        self.ba_input_check.stateChanged.connect(self._on_ba_check)
        self.connection_type_combobox.currentIndexChanged.connect(self._on_type_of_connection_change)

        self._fill_data()
        self._on_type_of_connection_change(self.connection_type_combobox.currentIndex())
        self.exec_()

    def _fill_data(self):

        if  self.line.vessel2_connection is None:
            self.connection_type_combobox.setCurrentIndex(0)
        else:
            self.connection_type_combobox.setCurrentIndex(1)

        fix_connection_to_fill = self.line.fix_connection
        if not fix_connection_to_fill:
            fix_connection_to_fill = MoorDynPlusFixConnection()

        self.fix_connection_point_x.setValue(fix_connection_to_fill.point[0])
        self.fix_connection_point_y.setValue(fix_connection_to_fill.point[1])
        self.fix_connection_point_z.setValue(fix_connection_to_fill.point[2])

        vessel_connection_to_fill = self.line.vessel_connection
        if not vessel_connection_to_fill:
            vessel_connection_to_fill = MoorDynPlusVesselConnection()
        self.vessel_connection_point_x.setValue(vessel_connection_to_fill.point[0])
        self.vessel_connection_point_y.setValue(vessel_connection_to_fill.point[1])
        self.vessel_connection_point_z.setValue(vessel_connection_to_fill.point[2])

        vessel2_connection_to_fill = self.line.vessel2_connection
        if not vessel2_connection_to_fill:
            vessel2_connection_to_fill = MoorDynPlusVesselConnection()
        self.vessel2_connection_point_x.setValue(vessel2_connection_to_fill.point[0])
        self.vessel2_connection_point_y.setValue(vessel2_connection_to_fill.point[1])
        self.vessel2_connection_point_z.setValue(vessel2_connection_to_fill.point[2])

        self.length_input.setValue(self.line.length)
        self.segments_input.setValue(self.line.segments)

        self.ea_input.setEnabled(bool(self.line.ea))
        self.ea_input.setValue(self.line.ea) if self.line.ea else ""
        self.ea_input_check.setChecked(bool(self.line.ea))

        self.diameter_input.setEnabled(bool(self.line.diameter))
        self.diameter_input.setValue(self.line.diameter) if self.line.diameter else ""
        self.diameter_input_check.setChecked(bool(self.line.diameter))

        self.massDenInAir_input.setEnabled(bool(self.line.massDenInAir))
        self.massDenInAir_input.setValue(self.line.massDenInAir) if self.line.massDenInAir else ""
        self.massDenInAir_input_check.setChecked(bool(self.line.massDenInAir))

        self.ba_input.setEnabled(bool(self.line.ba))
        self.ba_input.setValue(self.line.ba) if self.line.ba else ""
        self.ba_input_check.setChecked(bool(self.line.ba))

        self.vessel_connection_body_combo.addItems(["None"] + list(map(lambda body: "MKBound: {}".format(body.ref), self.stored_configuration.bodies)))
        current_body_enumerated_tuple: tuple = next(filter(lambda index_body_tuple: index_body_tuple[1].ref == vessel_connection_to_fill, enumerate(self.stored_configuration.bodies)), None)
        self.vessel_connection_body_combo.setCurrentIndex(current_body_enumerated_tuple[0] + 1 if current_body_enumerated_tuple else 0)
        
        # Load the moored floating body for vessel connection 1
        self.vessel_connection_body_combo.setCurrentIndex(0) # 0: None by default
        body_ref1 = vessel_connection_to_fill.bodyref
        for i in range(len(self.stored_configuration.bodies)):
            body=self.stored_configuration.bodies[i]
            if body.ref == body_ref1:
                self.vessel_connection_body_combo.setCurrentIndex(i+1) # Increase one index since the first item is 1 (0: None)  
                break

        self.vessel2_connection_body_combo.addItems(["None"] + list(map(lambda body: "MKBound: {}".format(body.ref), self.stored_configuration.bodies)))
        current_body_enumerated_tuple: tuple = next(filter(lambda index_body_tuple: index_body_tuple[1].ref == vessel2_connection_to_fill, enumerate(self.stored_configuration.bodies)), None)
        self.vessel2_connection_body_combo.setCurrentIndex(current_body_enumerated_tuple[0] + 1 if current_body_enumerated_tuple else 0)
      
        # Load the moored floating body for vessel connection 2
        self.vessel2_connection_body_combo.setCurrentIndex(0) # 0: None by default
        body_ref2 = vessel2_connection_to_fill.bodyref
        for i in range(len(self.stored_configuration.bodies)):
            body=self.stored_configuration.bodies[i]
            if body.ref == body_ref2:
                self.vessel2_connection_body_combo.setCurrentIndex(i+1) # Increase one index since the first item is 1 (0: None) 
                break

    def _on_type_of_connection_change(self, new_index):
        if new_index == 0:
            self.vessel_connection_label.setVisible(True)
            self.vessel_connection_point_label.setVisible(True)
            self.vessel_connection_point_x.setVisible(True)
            self.vessel_connection_point_y.setVisible(True)
            self.vessel_connection_point_z.setVisible(True)
            self.vessel_connection_body_combo.setVisible(True)

            self.vessel2_connection_label.setVisible(False)
            self.vessel2_connection_point_label.setVisible(False)
            self.vessel2_connection_point_x.setVisible(False)
            self.vessel2_connection_point_y.setVisible(False)
            self.vessel2_connection_point_z.setVisible(False)
            self.vessel2_connection_body_combo.setVisible(False)

            self.fix_connection_label.setVisible(True)
            self.fix_connection_point_x.setVisible(True)
            self.fix_connection_point_y.setVisible(True)
            self.fix_connection_point_z.setVisible(True)
        if new_index == 1:
            self.vessel_connection_label.setVisible(True)
            self.vessel_connection_point_label.setVisible(True)
            self.vessel_connection_point_x.setVisible(True)
            self.vessel_connection_point_y.setVisible(True)
            self.vessel_connection_point_z.setVisible(True)
            self.vessel_connection_body_combo.setVisible(True)

            self.vessel2_connection_label.setVisible(True)
            self.vessel2_connection_point_label.setVisible(True)
            self.vessel2_connection_point_x.setVisible(True)
            self.vessel2_connection_point_y.setVisible(True)
            self.vessel2_connection_point_z.setVisible(True)
            self.vessel2_connection_body_combo.setVisible(True)

            self.fix_connection_label.setVisible(False)
            self.fix_connection_point_x.setVisible(False)
            self.fix_connection_point_y.setVisible(False)
            self.fix_connection_point_z.setVisible(False)

    def _on_ea_check(self):
        self.ea_input.setEnabled(self.ea_input_check.isChecked())

    def _on_diameter_check(self):
        self.diameter_input.setEnabled(self.diameter_input_check.isChecked())

    def _on_massDenInAir_check(self):
        self.massDenInAir_input.setEnabled(self.massDenInAir_input_check.isChecked())

    def _on_ba_check(self):
        self.ba_input.setEnabled(self.ba_input_check.isChecked())

    def _on_ok(self):
        self.line.length = self.length_input.value()
        self.line.segments = self.segments_input.value()

        self.line.ea = str(self.ea_input.text()) if self.ea_input_check.isChecked() else None
        self.line.diameter = str(self.diameter_input.text()) if self.diameter_input_check.isChecked() else None
        self.line.massDenInAir = str(self.massDenInAir_input.text()) if self.massDenInAir_input_check.isChecked() else None
        self.line.ba = str(self.ba_input.text()) if self.ba_input_check.isChecked() else None

        self.line.vessel_connection = MoorDynPlusVesselConnection()
        self.line.vessel_connection.bodyref = int(self.vessel_connection_body_combo.currentText().split("MKBound: ")[1]) if self.vessel_connection_body_combo.currentIndex() > 0 else -1
        self.line.vessel_connection.point = [self.vessel_connection_point_x.value(),self.vessel_connection_point_y.value(),self.vessel_connection_point_z.value()]

        self.line.vessel2_connection = MoorDynPlusVesselConnection()
        self.line.vessel2_connection.bodyref = int(self.vessel2_connection_body_combo.currentText().split("MKBound: ")[1]) if self.vessel2_connection_body_combo.currentIndex() > 0 else -1
        self.line.vessel2_connection.point = [self.vessel2_connection_point_x.value(),self.vessel2_connection_point_y.value(),self.vessel2_connection_point_z.value()]

        self.line.fix_connection = MoorDynPlusFixConnection()
        self.line.fix_connection.point = [self.fix_connection_point_x.value(),self.fix_connection_point_y.value(),self.fix_connection_point_z.value()]

        if self.connection_type_combobox.currentIndex() == 0:
            self.line.vessel2_connection = None
        elif self.connection_type_combobox.currentIndex() == 1:
            self.line.fix_connection = None

        if self.line.vessel_connection.bodyref==-1:
            warning_dialog("A floating object MkBound must be selected for vessel connection")
        elif self.line.vessel2_connection and self.line.vessel2_connection.bodyref == -1:
            warning_dialog("A floating object MkBound must be selected for vessel2 connection")
        else: #Compulsory mkbound, to make it optional delete this else
            self.accept()
