#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Line Configuration Dialog. """

from PySide import QtGui

from mod.translation_tools import __
from mod.gui_tools import h_line_generator

from mod.dataobjects.moorings.moordyn.moordyn_line import MoorDynLine


class MoorDynLineConfigurationDialog(QtGui.QDialog):
    """ DesignSPHysics MoorDyn Line Configuration Dialog. """

    def __init__(self, line, stored_configuration):
        self.line: MoorDynLine = line
        self.stored_configuration = stored_configuration

        self.setWindowTitle(__("MoorDyn Line Configuration"))
        self.setMinimumWidth(440)
        self.root_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()

        # Label
        self.reference_label: QtGui.QLable = QtGui.QLabel(__("Editing settings for line: <b>{}</b>").format(line.line_id))

        # Basic configuration group
        self.basic_configuration_groupbox: QtGui.QGroupBox = QtGui.QGroupBox(__("Basic configuration"))
        self.basic_configuration_groupbox_layout: QtGui.QFormLayout = QtGui.QFormLayout()

        self.vessel_connection_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.vessel_connection_body_combo: QtGui.QComboBox = QtGui.QComboBox()
        self.vessel_connection_point_label: QtGui.QLabel = QtGui.QLabel(__("Point (X, Y, Z):"))
        self.vessel_connection_point_x: QtGui.QLineEdit = QtGui.QLineEdit()
        self.vessel_connection_point_y: QtGui.QLineEdit = QtGui.QLineEdit()
        self.vessel_connection_point_z: QtGui.QLineEdit = QtGui.QLineEdit()

        self.vessel_connection_layout.addWidget(self.vessel_connection_body_combo)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_label)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_x)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_y)
        self.vessel_connection_layout.addWidget(self.vessel_connection_point_z)

        self.fix_connection_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.fix_connection_point_label: QtGui.QLabel = QtGui.QLabel(__("Point (X, Y, Z):"))
        self.fix_connection_point_x: QtGui.QLineEdit = QtGui.QLineEdit()
        self.fix_connection_point_y: QtGui.QLineEdit = QtGui.QLineEdit()
        self.fix_connection_point_z: QtGui.QLineEdit = QtGui.QLineEdit()

        self.fix_connection_layout.addWidget(self.fix_connection_point_label)
        self.fix_connection_layout.addWidget(self.fix_connection_point_x)
        self.fix_connection_layout.addWidget(self.fix_connection_point_y)
        self.fix_connection_layout.addWidget(self.fix_connection_point_z)

        self.length_input: QtGui.QLineEdit = QtGui.QLineEdit()
        self.segments_input: QtGui.QLineEdit = QtGui.QLineEdit()

        self.basic_configuration_groupbox_layout.addRow(__("Vessel Connection: "), self.vessel_connection_layout)
        self.basic_configuration_groupbox_layout.addRow(__("Fix Connection: "), self.fix_connection_layout)
        self.basic_configuration_groupbox_layout.addRow(__("Line Length (m):"), self.length_input)
        self.basic_configuration_groupbox_layout.addRow(__("Number of Segments:"), self.segments_input)
        self.basic_configuration_groupbox.setLayout(self.basic_configuration_groupbox_layout)

        # Override configuration group
        self.override_configuration_groupbox: QtGui.QGroupBox = QtGui.QGroupBox(__("Configuration Overrides"))
        self.override_configuration_groupbox_layout: QtGui.QFormLayout = QtGui.QFormLayout()

        self.ea_input: QtGui.QLineEdit = QtGui.QLineEdit()
        self.ea_input_check: QtGui.QCheckBox = QtGui.QCheckBox()
        self.ea_input_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.ea_input_layout.addWidget(self.ea_input)
        self.ea_input_layout.addWidget(self.ea_input_check)

        self.diameter_input: QtGui.QLineEdit = QtGui.QLineEdit()
        self.diameter_input_check: QtGui.QCheckBox = QtGui.QCheckBox()
        self.diameter_input_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.diameter_input_layout.addWidget(self.diameter_input)
        self.diameter_input_layout.addWidget(self.diameter_input_check)

        self.massDenInAir_input: QtGui.QLineEdit = QtGui.QLineEdit()
        self.massDenInAir_input_check: QtGui.QCheckBox = QtGui.QCheckBox()
        self.massDenInAir_input_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.massDenInAir_input_layout.addWidget(self.massDenInAir_input)
        self.massDenInAir_input_layout.addWidget(self.massDenInAir_input_check)

        self.ba_input: QtGui.QLineEdit = QtGui.QLineEdit()
        self.ba_input_check: QtGui.QCheckBox = QtGui.QCheckBox()
        self.ba_input_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.ba_input_layout.addWidget(self.ba_input)
        self.ba_input_layout.addWidget(self.ba_input_check)

        self.override_configuration_groupbox_layout.addRow(__("Stiffness (N):"), self.ea_input_layout)
        self.override_configuration_groupbox_layout.addRow(__("Diameter (m):"), self.diameter_input_layout)
        self.override_configuration_groupbox_layout.addRow(__("Mass in Air (kg/m):"), self.massDenInAir_input_layout)
        self.override_configuration_groupbox_layout.addRow(__("Line internal damping (Ns):"), self.ba_input_layout)

        self.override_configuration_groupbox.setLayout(self.override_configuration_groupbox_layout)

        # Bottom button row
        self.button_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.ok_button: QtGui.QPushButton = QtGui.QPushButton(__("OK"))
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

        self._fill_data()
        self.exec_()

    def _fill_data(self):
        self.fix_connection_point_x.setText(str(self.line.fix_connection.point[0]))
        self.fix_connection_point_y.setText(str(self.line.fix_connection.point[1]))
        self.fix_connection_point_z.setText(str(self.line.fix_connection.point[2]))

        self.vessel_connection_point_x.setText(str(self.line.vessel_connection.point[0]))
        self.vessel_connection_point_y.setText(str(self.line.vessel_connection.point[1]))
        self.vessel_connection_point_z.setText(str(self.line.vessel_connection.point[2]))

        self.length_input.setText(str(self.line.length))
        self.segments_input.setText(str(self.line.segments))

        self.ea_input.setEnabled(bool(self.line.ea))
        self.ea_input.setText(str(self.line.ea) if self.line.ea else "")
        self.ea_input_check.setChecked(bool(self.line.ea))

        self.diameter_input.setEnabled(bool(self.line.diameter))
        self.diameter_input.setText(str(self.line.diameter) if self.line.diameter else "")
        self.diameter_input_check.setChecked(bool(self.line.diameter))

        self.massDenInAir_input.setEnabled(bool(self.line.massDenInAir))
        self.massDenInAir_input.setText(str(self.line.massDenInAir) if self.line.massDenInAir else "")
        self.massDenInAir_input_check.setChecked(bool(self.line.massDenInAir))

        self.ba_input.setEnabled(bool(self.line.ba))
        self.ba_input.setText(str(self.line.ba) if self.line.ba else "")
        self.ba_input_check.setChecked(bool(self.line.ba))

        self.vessel_connection_body_combo.addItems(["None"] + list(map(lambda body: "MKBound: {}".format(body.ref), self.stored_configuration.bodies)))
        current_body_enumerated_tuple: tuple = next(filter(lambda index_body_tuple: index_body_tuple[1].ref == self.line.vessel_connection.bodyref, enumerate(self.stored_configuration.bodies)), None)
        self.vessel_connection_body_combo.setCurrentIndex(current_body_enumerated_tuple[0] + 1 if current_body_enumerated_tuple else 0)

    def _on_ea_check(self):
        self.ea_input.setEnabled(self.ea_input_check.isChecked())

    def _on_diameter_check(self):
        self.diameter_input.setEnabled(self.diameter_input_check.isChecked())

    def _on_massDenInAir_check(self):
        self.massDenInAir_input.setEnabled(self.massDenInAir_input_check.isChecked())

    def _on_ba_check(self):
        self.ba_input.setEnabled(self.ba_input_check.isChecked())

    def _on_ok(self):
        self.line.length = float(self.length_input.text())
        self.line.segments = int(self.segments_input.text())

        self.line.ea = str(self.ea_input.text()) if self.ea_input_check.isChecked() else None
        self.line.diameter = str(self.diameter_input.text()) if self.diameter_input_check.isChecked() else None
        self.line.massDenInAir = str(self.massDenInAir_input.text()) if self.massDenInAir_input_check.isChecked() else None
        self.line.ba = str(self.ba_input.text()) if self.ba_input_check.isChecked() else None

        self.line.vessel_connection.bodyref = int(self.vessel_connection_body_combo.currentText().split("MKBound: ")[1]) if self.vessel_connection_body_combo.currentIndex() > 0 else -1
        self.line.vessel_connection.point = [float(self.vessel_connection_point_x.text()), float(self.vessel_connection_point_y.text()), float(self.vessel_connection_point_z.text())]

        self.line.fix_connection.point = [float(self.fix_connection_point_x.text()), float(self.fix_connection_point_y.text()), float(self.fix_connection_point_z.text())]

        self.accept()
