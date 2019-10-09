#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Inlet Zone Configuration Dialog."""

from PySide import QtCore, QtGui

from mod.translation_tools import __

from mod.dataobjects.case import Case

class InletZoneEdit(QtGui.QDialog):
    """ Defines Inlet/Outlet window dialog """

    def __init__(self, inlet_object_id):
        super(InletZoneEdit, self).__init__()
        self.inlet_object_id = inlet_object_id
        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet object edit")
        self.main_layout = QtGui.QVBoxLayout()

        # Find the zone for which button was pressed
        target_inlet_zone = None

        for inlet_zone in Case.instance().inlet_outlet.zones:
            if inlet_zone.id == self.inlet_object_id:
                target_inlet_zone = inlet_zone

        # Add Convert Fluid option
        self.convertfluid_layout = QtGui.QHBoxLayout()
        self.convertfluid_option = QtGui.QLabel(__("Convertfluid: "))
        self.convertfluid_combobox = QtGui.QComboBox()
        self.convertfluid_combobox.insertItems(0, [__("True"), __("False")])

        if target_inlet_zone.convertfluid == "True":
            self.convertfluid_combobox.setCurrentIndex(0)
        else:
            self.convertfluid_combobox.setCurrentIndex(1)

        self.convertfluid_layout.addWidget(self.convertfluid_option)
        self.convertfluid_layout.addWidget(self.convertfluid_combobox)
        self.convertfluid_layout.addStretch(1)

        # Add Layers option
        self.layers_layout = QtGui.QHBoxLayout()
        self.layers_option = QtGui.QLabel(__("Layers: "))
        self.layers_line_edit = QtGui.QLineEdit(str(target_inlet_zone.layers))

        self.layers_layout.addWidget(self.layers_option)
        self.layers_layout.addWidget(self.layers_line_edit)

        # Add Zone 2d or 3d
        self.zone2d3d_main_layout = QtGui.QGroupBox("Zone 2D/3D")
        self.zone2d3d_layout = QtGui.QVBoxLayout()
        self.zone2d3d_zones_layout = QtGui.QHBoxLayout()
        self.zone2d3d_mk_layout = QtGui.QHBoxLayout()
        self.zone2d3d_combobox_layout = QtGui.QHBoxLayout()
        self.zone2d_option = QtGui.QCheckBox("Zone 2D")
        self.zone3d_option = QtGui.QCheckBox("Zone 3D")
        self.zone2d3d_mk_label = QtGui.QLabel("MK fluid: ")
        self.zone2d3d_mk_line_edit = QtGui.QLineEdit(str(target_inlet_zone.zone_info.convertfluid))
        self.zone2d3d_mk_line_edit.setEnabled(False)
        self.zone2d3d_combobox_label = QtGui.QLabel(__("Direction: "))
        self.zone2d3d_combobox = QtGui.QComboBox()
        self.zone2d3d_combobox.setEnabled(False)
        self.zone2d3d_combobox.insertItems(0, [__("Left"), __("Right"), __("Front"), __("Back"), __("Top"), __("Bottom")])

        self.zone2d_option.toggled.connect(self.on_zone_check)
        self.zone3d_option.toggled.connect(self.on_zone_check)

        if target_inlet_zone.zone_info.zone_type == "zone2d":
            self.zone2d_option.setCheckState(QtCore.Qt.Checked)
        else:
            self.zone3d_option.setCheckState(QtCore.Qt.Checked)

        if target_inlet_zone.zone_info.layers == "Left":
            self.zone2d3d_combobox.setCurrentIndex(0)
        elif target_inlet_zone.zone_info.layers == "Right":
            self.zone2d3d_combobox.setCurrentIndex(1)
        elif target_inlet_zone.zone_info.layers == "Front":
            self.zone2d3d_combobox.setCurrentIndex(2)
        elif target_inlet_zone.zone_info.layers == "Back":
            self.zone2d3d_combobox.setCurrentIndex(3)
        elif target_inlet_zone.zone_info.layers == "Top":
            self.zone2d3d_combobox.setCurrentIndex(4)
        elif target_inlet_zone.zone_info.layers == "Bottom":
            self.zone2d3d_combobox.setCurrentIndex(5)

        self.zone2d3d_zones_layout.addWidget(self.zone2d_option)
        self.zone2d3d_zones_layout.addWidget(self.zone3d_option)
        self.zone2d3d_zones_layout.addStretch(1)
        self.zone2d3d_mk_layout.addWidget(self.zone2d3d_mk_label)
        self.zone2d3d_mk_layout.addWidget(self.zone2d3d_mk_line_edit)
        self.zone2d3d_combobox_layout.addWidget(self.zone2d3d_combobox_label)
        self.zone2d3d_combobox_layout.addWidget(self.zone2d3d_combobox)
        self.zone2d3d_combobox_layout.addStretch(1)

        self.zone2d3d_layout.addLayout(self.zone2d3d_zones_layout)
        self.zone2d3d_layout.addLayout(self.zone2d3d_mk_layout)
        self.zone2d3d_layout.addLayout(self.zone2d3d_combobox_layout)

        self.zone2d3d_main_layout.setLayout(self.zone2d3d_layout)

        # Add Imposed velocity option
        self.imposevelocity_layout = QtGui.QGroupBox("Velocity")
        self.imposevelocity_options_layout = QtGui.QVBoxLayout()
        self.imposevelocity_velocity_layout = QtGui.QHBoxLayout()
        self.imposevelocity_value_layout = QtGui.QHBoxLayout()
        self.imposevelocity_combobox_label = QtGui.QLabel(__("Velocity: "))
        self.imposevelocity_combobox = QtGui.QComboBox()
        self.imposevelocity_combobox.insertItems(0, [__("Fixed"), __("Variable"), __("Extrapolated"), __("Interpolated")])
        self.imposevelocity_velocity_label = QtGui.QLabel("Value: ")
        self.imposevelocity_velocity_line_edit = QtGui.QLineEdit(str(target_inlet_zone.velocity_info.convertfluid))
        self.imposevelocity_velocity_units = QtGui.QLabel(__("m/s"))

        self.imposevelocity_combobox.currentIndexChanged.connect(self.on_imposevelocity_change)

        if target_inlet_zone.velocity_info.velocity_type == 0:
            self.imposevelocity_combobox.setCurrentIndex(0)
        elif target_inlet_zone.velocity_info.velocity_type == 1:
            self.imposevelocity_combobox.setCurrentIndex(1)
        elif target_inlet_zone.velocity_info.velocity_type == 2:
            self.imposevelocity_combobox.setCurrentIndex(2)
        elif target_inlet_zone.velocity_info.velocity_type == 3:
            self.imposevelocity_combobox.setCurrentIndex(3)

        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_combobox_label)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_combobox)
        self.imposevelocity_velocity_layout.addStretch(1)
        self.imposevelocity_value_layout.addWidget(self.imposevelocity_velocity_label)
        self.imposevelocity_value_layout.addWidget(self.imposevelocity_velocity_line_edit)
        self.imposevelocity_value_layout.addWidget(self.imposevelocity_velocity_units)

        self.imposevelocity_options_layout.addLayout(self.imposevelocity_velocity_layout)
        self.imposevelocity_options_layout.addLayout(self.imposevelocity_value_layout)
        self.imposevelocity_layout.setLayout(self.imposevelocity_options_layout)

        # Add Outlet rhop option
        self.imposerhop_layout = QtGui.QGroupBox("Density")
        self.imposerhop_combobox_layout = QtGui.QHBoxLayout()
        self.imposerhop_value_layout = QtGui.QHBoxLayout()
        self.imposerhop_options_layout = QtGui.QVBoxLayout()
        self.imposerhop_label = QtGui.QLabel(__("Density: "))
        self.imposerhop_combobox = QtGui.QComboBox()
        self.imposerhop_combobox.insertItems(0, [__("Fixed"), __("Hydrostatic"), __("Extrapolated")])
        self.imposerhop_value_label = QtGui.QLabel("Value: ")
        self.imposerhop_value_line_edit = QtGui.QLineEdit(str(target_inlet_zone.density_info.convertfluid))

        self.imposerhop_combobox.currentIndexChanged.connect(self.on_imposerhop_change)

        if target_inlet_zone.density_info.density_type == 0:
            self.imposerhop_combobox.setCurrentIndex(0)
        elif target_inlet_zone.density_info.density_type == 1:
            self.imposerhop_combobox.setCurrentIndex(1)
        elif target_inlet_zone.density_info.density_type == 2:
            self.imposerhop_combobox.setCurrentIndex(2)

        self.imposerhop_combobox_layout.addWidget(self.imposerhop_label)
        self.imposerhop_combobox_layout.addWidget(self.imposerhop_combobox)
        self.imposerhop_combobox_layout.addStretch(1)
        self.imposerhop_value_layout.addWidget(self.imposerhop_value_label)
        self.imposerhop_value_layout.addWidget(self.imposerhop_value_line_edit)

        self.imposerhop_options_layout.addLayout(self.imposerhop_combobox_layout)
        self.imposerhop_options_layout.addLayout(self.imposerhop_value_layout)
        self.imposerhop_layout.setLayout(self.imposerhop_options_layout)

        # Add Inlet Z-surface option
        self.imposezsurf_layout = QtGui.QGroupBox("Elevation")
        self.imposezsurf_options_layout = QtGui.QVBoxLayout()
        self.imposezsurf_combobox_layout = QtGui.QHBoxLayout()
        self.imposezsurf_fixed_layout = QtGui.QHBoxLayout()
        self.imposezsurf_combobox_label = QtGui.QLabel("Elevation: ")
        self.imposezsurf_combobox = QtGui.QComboBox()
        self.imposezsurf_combobox.insertItems(0, [__("Fixed"), __("Variable"), __("Automatic")])

        self.imposezsurf_fixed_zbottom_label = QtGui.QLabel("Zbottom: ")
        self.imposezsurf_fixed_zbottom = QtGui.QLineEdit(str(target_inlet_zone.elevation_info.convertfluid))
        self.imposezsurf_fixed_zbottom_units = QtGui.QLabel("metres")
        self.imposezsurf_fixed_zsurf_label = QtGui.QLabel("Zsurf: ")
        self.imposezsurf_fixed_zsurf = QtGui.QLineEdit(str(target_inlet_zone.elevation_info.layers))
        self.imposezsurf_fixed_zsurf_units = QtGui.QLabel("metres")

        self.imposezsurf_fixed_zbottom.setEnabled(True)
        self.imposezsurf_fixed_zsurf.setEnabled(True)

        self.imposezsurf_combobox.currentIndexChanged.connect(self.on_imposezsurf_change)

        if target_inlet_zone.elevation_info.elevation_type == 0:
            self.imposezsurf_combobox.setCurrentIndex(0)
        elif target_inlet_zone.elevation_info.elevation_type == 1:
            self.imposezsurf_combobox.setCurrentIndex(1)
        elif target_inlet_zone.elevation_info.elevation_type == 2:
            self.imposezsurf_combobox.setCurrentIndex(2)

        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_combobox_label)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_combobox)
        self.imposezsurf_combobox_layout.addStretch(1)
        self.imposezsurf_fixed_layout.addWidget(self.imposezsurf_fixed_zbottom_label)
        self.imposezsurf_fixed_layout.addWidget(self.imposezsurf_fixed_zbottom)
        self.imposezsurf_fixed_layout.addWidget(self.imposezsurf_fixed_zbottom_units)
        self.imposezsurf_fixed_layout.addStretch(1)
        self.imposezsurf_fixed_layout.addWidget(self.imposezsurf_fixed_zsurf_label)
        self.imposezsurf_fixed_layout.addWidget(self.imposezsurf_fixed_zsurf)
        self.imposezsurf_fixed_layout.addWidget(self.imposezsurf_fixed_zsurf_units)

        self.imposezsurf_options_layout.addLayout(self.imposezsurf_combobox_layout)
        self.imposezsurf_options_layout.addLayout(self.imposezsurf_fixed_layout)

        self.imposezsurf_layout.setLayout(self.imposezsurf_options_layout)

        # Creates 2 main buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(self.convertfluid_layout)
        self.main_layout.addLayout(self.layers_layout)
        self.main_layout.addWidget(self.zone2d3d_main_layout)
        self.main_layout.addWidget(self.imposevelocity_layout)
        self.main_layout.addWidget(self.imposerhop_layout)
        self.main_layout.addWidget(self.imposezsurf_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.exec_()

    def on_imposerhop_change(self):
        """ Checks for imposerhop changes """
        if self.imposerhop_combobox.currentIndex() == 0:
            self.imposerhop_value_line_edit.setEnabled(True)
        else:
            self.imposerhop_value_line_edit.setEnabled(False)

    def on_imposevelocity_change(self):
        """ Checks for imposevelocity changes """
        if self.imposevelocity_combobox.currentIndex() == 0:
            self.imposevelocity_velocity_line_edit.setEnabled(True)
        else:
            self.imposevelocity_velocity_line_edit.setEnabled(False)

    def on_imposezsurf_change(self):
        """ Checks for imposezsurf changes """
        if self.imposezsurf_combobox.currentIndex() == 0 or self.imposezsurf_combobox.currentIndex() == 2:
            self.imposezsurf_fixed_zbottom.setEnabled(True)
            self.imposezsurf_fixed_zsurf.setEnabled(True)
        else:
            self.imposezsurf_fixed_zbottom.setEnabled(False)
            self.imposezsurf_fixed_zsurf.setEnabled(False)

    def on_zone_check(self):
        """ Checks for 2D or 3D options """
        if self.zone2d_option.isChecked() or self.zone3d_option.isChecked():
            self.zone2d3d_mk_line_edit.setEnabled(True)
            self.zone2d3d_combobox.setEnabled(True)
            if self.zone2d_option.isChecked():
                self.zone3d_option.setEnabled(False)
            elif not self.zone2d_option.isChecked():
                self.zone3d_option.setEnabled(True)

            if self.zone3d_option.isChecked():
                self.zone2d_option.setEnabled(False)
            elif not self.zone3d_option.isChecked():
                self.zone2d_option.setEnabled(True)
        else:
            self.zone2d3d_mk_line_edit.setEnabled(False)
            self.zone2d3d_combobox.setEnabled(False)
            if self.zone2d_option.isChecked():
                self.zone3d_option.setEnabled(False)
            elif not self.zone2d_option.isChecked():
                self.zone3d_option.setEnabled(True)

            if self.zone3d_option.isChecked():
                self.zone2d_option.setEnabled(False)
            elif not self.zone3d_option.isChecked():
                self.zone2d_option.setEnabled(True)

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """
        self.reject()

    def on_ok(self):
        """ Save data """
        count = -1

        for inlet_zone in Case.instance().inlet_outlet.zones:
            count += 1
            if inlet_zone.id == self.inlet_object_id:
                # [id, convertfluid, layers, [zone2 / 3D, mk, direction], [velocity, value], [density, value],[elevation, zbottom, zsurf]]
                Case.instance().inlet_outlet.zones[count].convertfluid = str(self.convertfluid_combobox.currentText())
                Case.instance().inlet_outlet.zones[count].layers = int(self.layers_line_edit.text())

                if self.zone2d_option.isChecked():
                    Case.instance().inlet_outlet.zones[count].zone_info = ["zone2d", int(self.zone2d3d_mk_line_edit.text()), str(self.zone2d3d_combobox.currentText())]
                elif self.zone3d_option.isChecked():
                    Case.instance().inlet_outlet.zones[count].zone_info = ["zone3d", int(self.zone2d3d_mk_line_edit.text()), str(self.zone2d3d_combobox.currentText())]

                Case.instance().inlet_outlet.zones[count].velocity_info = [int(self.imposevelocity_combobox.currentIndex()), float(self.imposevelocity_velocity_line_edit.text())]
                Case.instance().inlet_outlet.zones[count].density_info = [int(self.imposerhop_combobox.currentIndex()), float(self.imposerhop_value_line_edit.text())]
                Case.instance().inlet_outlet.zones[count].elevation_info = [int(self.imposezsurf_combobox.currentIndex()), float(self.imposezsurf_fixed_zbottom.text()), float(self.imposezsurf_fixed_zsurf.text())]
        InletZoneEdit.accept(self)
