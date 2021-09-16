#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Inlet Zone Configuration Dialog."""

from mod.freecad_tools import get_fc_main_window
from PySide2.QtWidgets import QVBoxLayout
from mod.dataobjects.awas_correction import AWASCorrection
from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.stdout_tools import debug

from mod.enums import InletOutletElevationType, InletOutletVelocitySpecType, InletOutletVelocityType, InletOutletZSurfMode, InletOutletZoneGeneratorType, InletOutletZoneType, InletOutletDirection

from mod.dataobjects.case import Case
from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone
from mod.dataobjects.inletoutlet.velocities.linear_velocity import LinearVelocity
from mod.dataobjects.inletoutlet.velocities.parabolic_velocity import ParabolicVelocity


class MKZoneGeneratorWidget(QtGui.QWidget):
    """ A widget to show options for the MK zone generator. """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.zone2d3d_mk_label = QtGui.QLabel("MK fluid: ")
        self.zone2d3d_mk_line_edit = QtGui.QLineEdit(str(0))  # FIXME
        self.zone2d3d_combobox_label = QtGui.QLabel(__("Direction: "))
        self.zone2d3d_combobox = QtGui.QComboBox()
        self.zone2d3d_combobox.insertItems(0, [__("Left"), __("Right"), __("Front"), __("Back"), __("Top"), __("Bottom")])

        self.main_layout.addWidget(self.zone2d3d_mk_label)
        self.main_layout.addWidget(self.zone2d3d_mk_line_edit)
        self.main_layout.addWidget(self.zone2d3d_combobox_label)
        self.main_layout.addWidget(self.zone2d3d_combobox)


class LineZoneGeneratorWidget(QtGui.QWidget):
    """ A widget to show options for the Line zone generator. """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.point_layout = QtGui.QHBoxLayout()
        self.point_label = QtGui.QLabel(__("Point 1 [X, Z]"))
        self.point_value_x = QtGui.QLineEdit()
        self.point_value_y = QtGui.QLineEdit()
        self.point_value_z = QtGui.QLineEdit()
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_value_x)
        self.point_layout.addWidget(self.point_value_y)
        self.point_layout.addWidget(self.point_value_z)

        self.point_value_y.setVisible(False) # Lines are 2d only!

        self.point2_layout = QtGui.QHBoxLayout()
        self.point2_label = QtGui.QLabel(__("Point 2 [X, Z]"))
        self.point2_value_x = QtGui.QLineEdit()
        self.point2_value_y = QtGui.QLineEdit()
        self.point2_value_z = QtGui.QLineEdit()
        self.point2_layout.addWidget(self.point2_label)
        self.point2_layout.addWidget(self.point2_value_x)
        self.point2_layout.addWidget(self.point2_value_y)
        self.point2_layout.addWidget(self.point2_value_z)

        self.point2_value_y.setVisible(False) # Lines are 2d only!

        self.direction_enabled_checkbox = QtGui.QCheckBox(__("Enable direction"))
        self.direction_enabled_checkbox.stateChanged.connect(self.on_direction_enabled_checked)

        self.direction_layout = QtGui.QHBoxLayout()
        self.direction_label = QtGui.QLabel(__("Direction [X, Z]"))
        self.direction_value_x = QtGui.QLineEdit()
        self.direction_value_y = QtGui.QLineEdit()
        self.direction_value_z = QtGui.QLineEdit()
        self.direction_layout.addWidget(self.direction_label)
        self.direction_layout.addWidget(self.direction_value_x)
        self.direction_layout.addWidget(self.direction_value_y)
        self.direction_layout.addWidget(self.direction_value_z)

        self.direction_value_y.setVisible(False) # Lines are 2d only!

        self.rotation_enabled_checkbox = QtGui.QCheckBox(__("Enable rotation"))
        self.rotation_enabled_checkbox.stateChanged.connect(self.on_rotation_enabled_checked)

        self.rotation_angle_layout = QtGui.QHBoxLayout()
        self.rotation_angle_label = QtGui.QLabel(__("Rotation Angle (degrees)"))
        self.rotation_angle_value = QtGui.QLineEdit()
        self.rotation_angle_layout.addWidget(self.rotation_angle_label)
        self.rotation_angle_layout.addWidget(self.rotation_angle_value)

        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.point2_layout)
        self.main_layout.addWidget(self.direction_enabled_checkbox)
        self.main_layout.addLayout(self.direction_layout)
        self.main_layout.addWidget(self.rotation_enabled_checkbox)
        self.main_layout.addLayout(self.rotation_angle_layout)

    def on_direction_enabled_checked(self):
        if self.direction_enabled_checkbox.isChecked():
            self.direction_label.setEnabled(True)
            self.direction_value_x.setEnabled(True)
            self.direction_value_y.setEnabled(True)
            self.direction_value_z.setEnabled(True)
        else:
            self.direction_label.setEnabled(False)
            self.direction_value_x.setEnabled(False)
            self.direction_value_y.setEnabled(False)
            self.direction_value_z.setEnabled(False)

    def on_rotation_enabled_checked(self):
        if self.rotation_enabled_checkbox.isChecked():
            self.rotation_angle_label.setEnabled(True)
            self.rotation_angle_value.setEnabled(True)
        else:
            self.rotation_angle_label.setEnabled(False)
            self.rotation_angle_value.setEnabled(False)


class BoxZoneGeneratorWidget(QtGui.QWidget):
    """ A widget to show options for the Box zone generator. """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.point_layout = QtGui.QHBoxLayout()
        self.point_label = QtGui.QLabel(__("Point [X, Y, Z]"))
        self.point_value_x = QtGui.QLineEdit()
        self.point_value_y = QtGui.QLineEdit()
        self.point_value_z = QtGui.QLineEdit()
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_value_x)
        self.point_layout.addWidget(self.point_value_y)
        self.point_layout.addWidget(self.point_value_z)

        self.size_layout = QtGui.QHBoxLayout()
        self.size_label = QtGui.QLabel(__("Size [X, Y, Z]"))
        self.size_value_x = QtGui.QLineEdit()
        self.size_value_y = QtGui.QLineEdit()
        self.size_value_z = QtGui.QLineEdit()
        self.size_layout.addWidget(self.size_label)
        self.size_layout.addWidget(self.size_value_x)
        self.size_layout.addWidget(self.size_value_y)
        self.size_layout.addWidget(self.size_value_z)

        self.direction_layout = QtGui.QHBoxLayout()
        self.direction_label = QtGui.QLabel(__("Direction Vector [X, Y, Z]"))
        self.direction_value_x = QtGui.QLineEdit()
        self.direction_value_y = QtGui.QLineEdit()
        self.direction_value_z = QtGui.QLineEdit()
        self.direction_layout.addWidget(self.direction_label)
        self.direction_layout.addWidget(self.direction_value_x)
        self.direction_layout.addWidget(self.direction_value_y)
        self.direction_layout.addWidget(self.direction_value_z)

        self.rotateaxis_enabled_checkbox = QtGui.QCheckBox(__("Enable rotation"))
        self.rotateaxis_enabled_checkbox.stateChanged.connect(self.on_rotateaxis_check)

        self.rotateaxis_angle_layout = QtGui.QHBoxLayout()
        self.rotateaxis_angle_label = QtGui.QLabel(__("Rotation angle (degrees)"))
        self.rotateaxis_angle_value = QtGui.QLineEdit()
        self.rotateaxis_angle_layout.addWidget(self.rotateaxis_angle_label)
        self.rotateaxis_angle_layout.addWidget(self.rotateaxis_angle_value)

        self.rotateaxis_point1_layout = QtGui.QHBoxLayout()
        self.rotateaxis_point1_label = QtGui.QLabel(__("Rotation Point 1 [X, Y, Z]"))
        self.rotateaxis_point1_value_x = QtGui.QLineEdit()
        self.rotateaxis_point1_value_y = QtGui.QLineEdit()
        self.rotateaxis_point1_value_z = QtGui.QLineEdit()
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_label)
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_value_x)
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_value_y)
        self.rotateaxis_point1_layout.addWidget(self.rotateaxis_point1_value_z)

        self.rotateaxis_point2_layout = QtGui.QHBoxLayout()
        self.rotateaxis_point2_label = QtGui.QLabel(__("Rotation point 2 [X, Y, Z]"))
        self.rotateaxis_point2_value_x = QtGui.QLineEdit()
        self.rotateaxis_point2_value_y = QtGui.QLineEdit()
        self.rotateaxis_point2_value_z = QtGui.QLineEdit()
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_label)
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_value_x)
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_value_y)
        self.rotateaxis_point2_layout.addWidget(self.rotateaxis_point2_value_z)

        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.size_layout)
        self.main_layout.addLayout(self.direction_layout)
        self.main_layout.addWidget(self.rotateaxis_enabled_checkbox)
        self.main_layout.addLayout(self.rotateaxis_angle_layout)
        self.main_layout.addLayout(self.rotateaxis_point1_layout)
        self.main_layout.addLayout(self.rotateaxis_point2_layout)

    def on_rotateaxis_check(self):
        should_enable: bool = self.rotateaxis_enabled_checkbox.isChecked()
        self.rotateaxis_angle_label.setEnabled(should_enable)
        self.rotateaxis_angle_value.setEnabled(should_enable)
        self.rotateaxis_point1_label.setEnabled(should_enable)
        self.rotateaxis_point1_value_x.setEnabled(should_enable)
        self.rotateaxis_point1_value_y.setEnabled(should_enable)
        self.rotateaxis_point1_value_z.setEnabled(should_enable)
        self.rotateaxis_point2_label.setEnabled(should_enable)
        self.rotateaxis_point2_value_x.setEnabled(should_enable)
        self.rotateaxis_point2_value_y.setEnabled(should_enable)
        self.rotateaxis_point2_value_z.setEnabled(should_enable)


class CircleZoneGeneratorWidget(QtGui.QWidget):
    """ A widget to show options for the Circle zone generator. """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.point_layout = QtGui.QHBoxLayout()
        self.point_label = QtGui.QLabel(__("Point [X, Y, Z]"))
        self.point_value_x = QtGui.QLineEdit()
        self.point_value_y = QtGui.QLineEdit()
        self.point_value_z = QtGui.QLineEdit()
        self.point_layout.addWidget(self.point_label)
        self.point_layout.addWidget(self.point_value_x)
        self.point_layout.addWidget(self.point_value_y)
        self.point_layout.addWidget(self.point_value_z)

        self.radius_layout = QtGui.QHBoxLayout()
        self.radius_label = QtGui.QLabel(__("Radius (m)"))
        self.radius_value = QtGui.QLineEdit()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_value)

        self.direction_layout = QtGui.QHBoxLayout()
        self.direction_label = QtGui.QLabel(__("Direction Vector [X, Y, Z]"))
        self.direction_value_x = QtGui.QLineEdit()
        self.direction_value_y = QtGui.QLineEdit()
        self.direction_value_z = QtGui.QLineEdit()
        self.direction_layout.addWidget(self.direction_label)
        self.direction_layout.addWidget(self.direction_value_x)
        self.direction_layout.addWidget(self.direction_value_y)
        self.direction_layout.addWidget(self.direction_value_z)

        self.main_layout.addLayout(self.point_layout)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.direction_layout)


class VelocityTypeFixedConstantWidget(QtGui.QWidget):
    """ A widget to show options for Fixed Constant velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.row = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel(__("Constant Velocity (m/s):"))
        self.input = QtGui.QLineEdit()
        self.row.addWidget(self.label)
        self.row.addWidget(self.input)

        self.main_layout.addLayout(self.row)
        self.setLayout(self.main_layout)


class VelocityTypeFixedLinearWidget(QtGui.QWidget):
    """ A widget to show options for Fixed Linear velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.v_layout = QtGui.QHBoxLayout()
        self.v_label = QtGui.QLabel(__("V (m/s):"))
        self.v_input = QtGui.QLineEdit()
        self.v_layout.addWidget(self.v_label)
        self.v_layout.addWidget(self.v_input)

        self.v2_layout = QtGui.QHBoxLayout()
        self.v2_label = QtGui.QLabel(__("V2 (m/s):"))
        self.v2_input = QtGui.QLineEdit()
        self.v2_layout.addWidget(self.v2_label)
        self.v2_layout.addWidget(self.v2_input)

        self.z_layout = QtGui.QHBoxLayout()
        self.z_label = QtGui.QLabel(__("Z (m/s):"))
        self.z_input = QtGui.QLineEdit()
        self.z_layout.addWidget(self.z_label)
        self.z_layout.addWidget(self.z_input)

        self.z2_layout = QtGui.QHBoxLayout()
        self.z2_label = QtGui.QLabel(__("Z2 (m/s):"))
        self.z2_input = QtGui.QLineEdit()
        self.z2_layout.addWidget(self.z2_label)
        self.z2_layout.addWidget(self.z2_input)

        self.main_layout.addLayout(self.v_layout)
        self.main_layout.addLayout(self.v2_layout)
        self.main_layout.addLayout(self.z_layout)
        self.main_layout.addLayout(self.z2_layout)
        self.setLayout(self.main_layout)


class VelocityTypeFixedParabolicWidget(QtGui.QWidget):
    """ A widget to show options for Fixed Parabolic velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.v_layout = QtGui.QHBoxLayout()
        self.v_label = QtGui.QLabel(__("V (m/s):"))
        self.v_input = QtGui.QLineEdit()
        self.v_layout.addWidget(self.v_label)
        self.v_layout.addWidget(self.v_input)

        self.v2_layout = QtGui.QHBoxLayout()
        self.v2_label = QtGui.QLabel(__("V2 (m/s):"))
        self.v2_input = QtGui.QLineEdit()
        self.v2_layout.addWidget(self.v2_label)
        self.v2_layout.addWidget(self.v2_input)

        self.v3_layout = QtGui.QHBoxLayout()
        self.v3_label = QtGui.QLabel(__("v3 (m/s):"))
        self.v3_input = QtGui.QLineEdit()
        self.v3_layout.addWidget(self.v3_label)
        self.v3_layout.addWidget(self.v3_input)

        self.z_layout = QtGui.QHBoxLayout()
        self.z_label = QtGui.QLabel(__("Z (m/s):"))
        self.z_input = QtGui.QLineEdit()
        self.z_layout.addWidget(self.z_label)
        self.z_layout.addWidget(self.z_input)

        self.z2_layout = QtGui.QHBoxLayout()
        self.z2_label = QtGui.QLabel(__("Z2 (m/s):"))
        self.z2_input = QtGui.QLineEdit()
        self.z2_layout.addWidget(self.z2_label)
        self.z2_layout.addWidget(self.z2_input)

        self.z3_layout = QtGui.QHBoxLayout()
        self.z3_label = QtGui.QLabel(__("z3 (m/s):"))
        self.z3_input = QtGui.QLineEdit()
        self.z3_layout.addWidget(self.z3_label)
        self.z3_layout.addWidget(self.z3_input)

        self.main_layout.addLayout(self.v_layout)
        self.main_layout.addLayout(self.v2_layout)
        self.main_layout.addLayout(self.v3_layout)
        self.main_layout.addLayout(self.z_layout)
        self.main_layout.addLayout(self.z2_layout)
        self.main_layout.addLayout(self.z3_layout)
        self.setLayout(self.main_layout)


class VelocityTypeVariableUniformWidget(QtGui.QWidget):
    """ A widget to show options for Variable Uniform velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.table = QtGui.QTableWidget(60, 2)
        self.table.setHorizontalHeaderLabels([__("Time (s)"), __("Velocity (m/s)")])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)


class VelocityTypeVariableLinearWidget(QtGui.QWidget):
    """ A widget to show options for Variable Linear velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.table = QtGui.QTableWidget(60, 5)
        self.table.setHorizontalHeaderLabels([__("Time (s)"), __("V (m/s)"), __("V2 (m/s)"), __("Z (m/s)"), __("Z2 (m/s)")])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)


class VelocityTypeVariableParabolicWidget(QtGui.QWidget):
    """ A widget to show options for Variable Parabolic velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.table = QtGui.QTableWidget(60, 7)
        self.table.setHorizontalHeaderLabels([__("Time (s)"), __("V (m/s)"), __("V2 (m/s)"), __("V3 (m/s)"), __("Z (m/s)"), __("Z2 (m/s)"), __("Z3 (m/s)")])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)


class VelocityTypeFileWidget(QtGui.QWidget):
    """ A widget to show options for File based velocity. """

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(__("File Path:"))
        self.input = QtGui.QLineEdit()
        self.button = QtGui.QPushButton(__("Browse"))

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.input)
        self.main_layout.addWidget(self.button)

        self.button.clicked.connect(self.on_browse_buton)

        self.setLayout(self.main_layout)

    def on_browse_buton(self):
        file_name_temp, _ = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"), Case.the().info.last_used_directory, "CSV Files (*.csv)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.input.setText(file_name_temp)


class ImposezsurfFixedWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.zbottom_layout = QtGui.QHBoxLayout()
        self.zbottom_label = QtGui.QLabel(__("Bottom level of water (m)"))
        self.zbottom_input = QtGui.QLineEdit()
        self.zbottom_layout.addWidget(self.zbottom_label)
        self.zbottom_layout.addWidget(self.zbottom_input)

        self.zsurf_layout = QtGui.QHBoxLayout()
        self.zsurf_label = QtGui.QLabel(__("Surface (m)"))
        self.zsurf_input = QtGui.QLineEdit()
        self.zsurf_layout.addWidget(self.zsurf_label)
        self.zsurf_layout.addWidget(self.zsurf_input)

        self.main_layout.addLayout(self.zbottom_layout)
        self.main_layout.addLayout(self.zsurf_layout)

        self.setLayout(self.main_layout)


class ImposezsurfVariableWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.savevtk_checkbox = QtGui.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtGui.QCheckBox(__("Remove particles above surface"))

        self.zbottom_layout = QtGui.QHBoxLayout()
        self.zbottom_label = QtGui.QLabel(__("Bottom level of water (m)"))
        self.zbottom_input = QtGui.QLineEdit()
        self.zbottom_layout.addWidget(self.zbottom_label)
        self.zbottom_layout.addWidget(self.zbottom_input)

        self.zsurf_table = QtGui.QTableWidget(60, 2)
        self.zsurf_table.setHorizontalHeaderLabels([__("Time (s)"), __("Surface level (m)")])
        self.zsurf_table.verticalHeader().setVisible(False)
        self.zsurf_table.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        self.main_layout.addLayout(self.zbottom_layout)
        self.main_layout.addWidget(self.zsurf_table)

        self.setLayout(self.main_layout)


class ImposezsurfVariableFromFileWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.savevtk_checkbox = QtGui.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtGui.QCheckBox(__("Remove particles above surface"))

        self.zbottom_layout = QtGui.QHBoxLayout()
        self.zbottom_label = QtGui.QLabel(__("Bottom level of water (m)"))
        self.zbottom_input = QtGui.QLineEdit()
        self.zbottom_layout.addWidget(self.zbottom_label)
        self.zbottom_layout.addWidget(self.zbottom_input)

        self.zsurf_layout = QtGui.QHBoxLayout()
        self.zsurf_label = QtGui.QLabel(__("File Path"))
        self.zsurf_input = QtGui.QLineEdit()
        self.zsurf_button = QtGui.QPushButton(__("Browse..."))
        self.zsurf_layout.addWidget(self.zsurf_label)
        self.zsurf_layout.addWidget(self.zsurf_input)
        self.zsurf_layout.addWidget(self.zsurf_button)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        self.main_layout.addLayout(self.zbottom_layout)
        self.main_layout.addLayout(self.zsurf_layout)

        self.zsurf_button.clicked.connect(self.on_browse_button)

        self.setLayout(self.main_layout)

    def on_browse_button(self):
        file_name_temp, _ = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select a file"), Case.the().info.last_used_directory, "CSV Files (*.csv)")
        Case.the().info.update_last_used_directory(file_name_temp)
        if file_name_temp:
            self.zsurf_input.setText(file_name_temp)


class ImposezsurfCalculatedWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.savevtk_checkbox = QtGui.QCheckBox(__("Save VTK files"))
        self.remove_checkbox = QtGui.QCheckBox(__("Remove particles above surface"))

        self.zbottom_layout = QtGui.QHBoxLayout()
        self.zbottom_label = QtGui.QLabel(__("Bottom level of water (m)"))
        self.zbottom_input = QtGui.QLineEdit()
        self.zbottom_layout.addWidget(self.zbottom_label)
        self.zbottom_layout.addWidget(self.zbottom_input)

        self.zsurf_layout = QtGui.QHBoxLayout()
        self.zsurf_label = QtGui.QLabel(__("Surface (m)"))
        self.zsurf_input = QtGui.QLineEdit()
        self.zsurf_layout.addWidget(self.zsurf_label)
        self.zsurf_layout.addWidget(self.zsurf_input)

        self.main_layout.addWidget(self.savevtk_checkbox)
        self.main_layout.addWidget(self.remove_checkbox)
        self.main_layout.addLayout(self.zbottom_layout)
        self.main_layout.addLayout(self.zsurf_layout)

        self.setLayout(self.main_layout)


class InletZoneEdit(QtGui.QDialog):
    """ Defines Inlet/Outlet window dialog """

    DIRECTION_MAPPING: dict = {
        0: InletOutletDirection.LEFT,
        1: InletOutletDirection.RIGHT,
        2: InletOutletDirection.FRONT,
        3: InletOutletDirection.BACK,
        4: InletOutletDirection.TOP,
        5: InletOutletDirection.BOTTOM,
    }

    ZONE_COMBO_TYPES_2D = [__("MK"), __("Line")]
    ZONE_COMBO_TYPES_3D = [__("MK"), __("Box"), __("Circle")]

    VELOCITY_TYPES_FIXED_COMBO = [__("Constant"), __("Linear"), __("Parabolic")]
    VELOCITY_TYPES_VARIABLE_COMBO = [__("Uniform"), __("Linear"), __("Parabolic"), __("Uniform from a file"), __("Linear from a file"), __("Parabolic from a file")]

    def __init__(self, inlet_object_id, parent=None):
        super().__init__(parent=parent)

        # Find the zone for which button was pressed
        self.target_io_zone: InletOutletZone = Case.the().inlet_outlet.get_io_zone_for_id(inlet_object_id)

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet object edit")
        self.main_layout = QtGui.QVBoxLayout()

        # Add Layers option
        self.layers_layout = QtGui.QHBoxLayout()
        self.layers_option = QtGui.QLabel(__("Layers: "))
        self.layers_line_edit = QtGui.QLineEdit(str(self.target_io_zone.layers))

        self.layers_layout.addWidget(self.layers_option)
        self.layers_layout.addWidget(self.layers_line_edit)

        # Add refilling option selector
        self.refilling_layout = QtGui.QHBoxLayout()
        self.refilling_label = QtGui.QLabel(__("Refilling mode:"))
        self.refilling_selector = QtGui.QComboBox()
        self.refilling_selector.insertItems(0, [__("Simple full"), __("Simple below Z Surface"), __("Advanced for reverse flows")])
        self.refilling_selector.setCurrentIndex(self.target_io_zone.refilling)

        self.refilling_layout.addWidget(self.refilling_label)
        self.refilling_layout.addWidget(self.refilling_selector)

        # Add inputtreatment option selector
        self.inputtreatment_layout = QtGui.QHBoxLayout()
        self.inputtreatment_label = QtGui.QLabel(__("Input Treatment mode:"))
        self.inputtreatment_selector = QtGui.QComboBox()
        self.inputtreatment_selector.insertItems(0, [__("No changes"), __("Convert Fluid"), __("Remove fluid")])
        self.inputtreatment_selector.setCurrentIndex(self.target_io_zone.inputtreatment)

        self.inputtreatment_layout.addWidget(self.inputtreatment_label)
        self.inputtreatment_layout.addWidget(self.inputtreatment_selector)

        # Add Zone 2d or 3d
        self.zone2d3d_main_layout = QtGui.QGroupBox("Zone 2D/3D")
        self.zone2d3d_layout = QtGui.QVBoxLayout()
        self.zone2d3d_zones_layout = QtGui.QHBoxLayout()
        self.zone2d3d_generator_layout = QtGui.QHBoxLayout()
        self.zone2d_option = QtGui.QRadioButton("Zone 2D")
        self.zone3d_option = QtGui.QRadioButton("Zone 3D")
        self.zone2d_option.toggled.connect(self.on_zone2d3d_radio_toggled)
        self.zone2d_option.toggled.connect(self.on_zone2d3d_radio_toggled)
        self.zone_gen_type_label = QtGui.QLabel("Type")
        self.zone_gen_type_combo = QtGui.QComboBox()

        # Zone Generator widgets
        self.mk_zone_generator_widget = MKZoneGeneratorWidget()
        self.mk_zone_generator_widget.setVisible(False)
        self.line_zone_generator_widget = LineZoneGeneratorWidget()
        self.line_zone_generator_widget.setVisible(False)
        self.box_zone_generator_widget = BoxZoneGeneratorWidget()
        self.box_zone_generator_widget.setVisible(False)
        self.circle_zone_generator_widget = CircleZoneGeneratorWidget()
        self.circle_zone_generator_widget.setVisible(False)

        self.zone_gen_type_combo.clear()
        self.zone_gen_type_combo.currentIndexChanged.connect(self.on_zone_gen_type_change)
        if self.target_io_zone.zone_info.zone_type == InletOutletZoneType.ZONE_2D:
            self.zone2d_option.toggle()
            self.on_zone2d3d_radio_toggled()
            if self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.MK:
                self.zone_gen_type_combo.setCurrentIndex(0)
            elif self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.LINE:
                self.zone_gen_type_combo.setCurrentIndex(1)
        else:
            self.zone3d_option.toggle()
            self.on_zone2d3d_radio_toggled()
            if self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.MK:
                self.zone_gen_type_combo.setCurrentIndex(0)
            elif self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.BOX:
                self.zone_gen_type_combo.setCurrentIndex(1)
            elif self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
                self.zone_gen_type_combo.setCurrentIndex(2)

        self.on_zone_gen_type_change()

        # Fill zone generator widget options
        # MK Generator
        gen_widget = self.mk_zone_generator_widget
        zone_gen = self.target_io_zone.zone_info.zone_mk_generator
        gen_widget.zone2d3d_mk_line_edit.setText(str(zone_gen.mkfluid))
        index_to_put = 0
        for index, direction in self.DIRECTION_MAPPING.items():
            if direction == zone_gen.direction:
                index_to_put = index
        gen_widget.zone2d3d_combobox.setCurrentIndex(index_to_put)

        # Line Generator
        gen_widget = self.line_zone_generator_widget
        io_zone_gen = self.target_io_zone.zone_info.zone_line_generator
        gen_widget.point_value_x.setText(str(io_zone_gen.point[0]))
        gen_widget.point_value_y.setText(str(io_zone_gen.point[1]))
        gen_widget.point_value_z.setText(str(io_zone_gen.point[2]))

        gen_widget.point2_value_x.setText(str(io_zone_gen.point2[0]))
        gen_widget.point2_value_y.setText(str(io_zone_gen.point2[1]))
        gen_widget.point2_value_z.setText(str(io_zone_gen.point2[2]))

        gen_widget.direction_value_x.setText(str(io_zone_gen.direction[0]))
        gen_widget.direction_value_y.setText(str(io_zone_gen.direction[1]))
        gen_widget.direction_value_z.setText(str(io_zone_gen.direction[2]))

        gen_widget.rotation_angle_value.setText(str(io_zone_gen.rotate_angle))

        gen_widget.direction_enabled_checkbox.setChecked(io_zone_gen.direction_enabled)
        gen_widget.rotation_enabled_checkbox.setChecked(io_zone_gen.has_rotation)

        gen_widget.on_direction_enabled_checked()
        gen_widget.on_rotation_enabled_checked()

        # Box Generator
        gen_widget = self.box_zone_generator_widget
        io_zone_gen = self.target_io_zone.zone_info.zone_box_generator
        gen_widget.point_value_x.setText(str(io_zone_gen.point[0]))
        gen_widget.point_value_y.setText(str(io_zone_gen.point[1]))
        gen_widget.point_value_z.setText(str(io_zone_gen.point[2]))

        gen_widget.size_value_x.setText(str(io_zone_gen.size[0]))
        gen_widget.size_value_y.setText(str(io_zone_gen.size[1]))
        gen_widget.size_value_z.setText(str(io_zone_gen.size[2]))

        gen_widget.direction_value_x.setText(str(io_zone_gen.direction[0]))
        gen_widget.direction_value_y.setText(str(io_zone_gen.direction[1]))
        gen_widget.direction_value_z.setText(str(io_zone_gen.direction[2]))

        gen_widget.rotateaxis_enabled_checkbox.setChecked(io_zone_gen.rotateaxis_enabled)
        gen_widget.rotateaxis_angle_value.setText(str(io_zone_gen.rotateaxis_angle))

        gen_widget.rotateaxis_point1_value_x.setText(str(io_zone_gen.rotateaxis_point1[0]))
        gen_widget.rotateaxis_point1_value_y.setText(str(io_zone_gen.rotateaxis_point1[1]))
        gen_widget.rotateaxis_point1_value_z.setText(str(io_zone_gen.rotateaxis_point1[2]))

        gen_widget.rotateaxis_point2_value_x.setText(str(io_zone_gen.rotateaxis_point2[0]))
        gen_widget.rotateaxis_point2_value_y.setText(str(io_zone_gen.rotateaxis_point2[1]))
        gen_widget.rotateaxis_point2_value_z.setText(str(io_zone_gen.rotateaxis_point2[2]))

        gen_widget.on_rotateaxis_check()

        # Circle Generator
        gen_widget = self.circle_zone_generator_widget
        io_zone_gen = self.target_io_zone.zone_info.zone_circle_generator

        gen_widget.point_value_x.setText(str(io_zone_gen.point[0]))
        gen_widget.point_value_y.setText(str(io_zone_gen.point[1]))
        gen_widget.point_value_z.setText(str(io_zone_gen.point[2]))

        gen_widget.radius_value.setText(str(io_zone_gen.radius))

        gen_widget.direction_value_x.setText(str(io_zone_gen.direction[0]))
        gen_widget.direction_value_y.setText(str(io_zone_gen.direction[1]))
        gen_widget.direction_value_z.setText(str(io_zone_gen.direction[2]))

        self.zone2d3d_zones_layout.addWidget(self.zone2d_option)
        self.zone2d3d_zones_layout.addWidget(self.zone3d_option)
        self.zone2d3d_zones_layout.addWidget(self.zone_gen_type_label)
        self.zone2d3d_zones_layout.addWidget(self.zone_gen_type_combo)
        self.zone2d3d_zones_layout.addStretch(1)
        self.zone2d3d_generator_layout.addWidget(self.mk_zone_generator_widget)
        self.zone2d3d_generator_layout.addWidget(self.line_zone_generator_widget)
        self.zone2d3d_generator_layout.addWidget(self.box_zone_generator_widget)
        self.zone2d3d_generator_layout.addWidget(self.circle_zone_generator_widget)

        self.zone2d3d_layout.addLayout(self.zone2d3d_zones_layout)
        self.zone2d3d_layout.addLayout(self.zone2d3d_generator_layout)

        self.zone2d3d_main_layout.setLayout(self.zone2d3d_layout)

        # Add Imposed velocity option
        self.imposevelocity_layout = QtGui.QGroupBox("Velocity")
        self.imposevelocity_options_layout = QtGui.QVBoxLayout()

        self.imposevelocity_velocity_layout = QtGui.QHBoxLayout()
        self.imposevelocity_combobox_label = QtGui.QLabel(__("Velocity Mode: "))
        self.imposevelocity_combobox = QtGui.QComboBox()
        self.imposevelocity_combobox.insertItems(0, [__("Fixed"), __("Variable"), __("Extrapolated")])
        self.imposevelocity_type_combobox_label = QtGui.QLabel(__("Velocity Type: "))
        self.imposevelocity_type_combobox = QtGui.QComboBox()

        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_combobox_label)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_combobox)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_type_combobox_label)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_type_combobox)

        self.imposevelocity_fixed_constant_widget = VelocityTypeFixedConstantWidget()
        self.imposevelocity_fixed_linear_widget = VelocityTypeFixedLinearWidget()
        self.imposevelocity_fixed_parabolic_widget = VelocityTypeFixedParabolicWidget()
        self.imposevelocity_variable_uniform_widget = VelocityTypeVariableUniformWidget()
        self.imposevelocity_variable_linear_widget = VelocityTypeVariableLinearWidget()
        self.imposevelocity_variable_parabolic_widget = VelocityTypeVariableParabolicWidget()
        self.imposevelocity_file_widget = VelocityTypeFileWidget()

        self.imposevelocity_options_layout.addLayout(self.imposevelocity_velocity_layout)

        # Different widgets for the different options for imposevelocity
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_constant_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_linear_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_parabolic_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_variable_uniform_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_variable_linear_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_variable_parabolic_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_file_widget)

        self.imposevelocity_layout.setLayout(self.imposevelocity_options_layout)

        self.imposevelocity_combobox.currentIndexChanged.connect(self.on_imposevelocity_change)
        self.imposevelocity_type_combobox.currentIndexChanged.connect(self.on_imposevelocity_type_change)

        self.imposevelocity_combobox.setCurrentIndex(self.target_io_zone.velocity_info.velocity_type)
        self.on_imposevelocity_change()

        if self.target_io_zone.velocity_info.velocity_specification_type in [InletOutletVelocitySpecType.FIXED_CONSTANT, InletOutletVelocitySpecType.FIXED_LINEAR, InletOutletVelocitySpecType.FIXED_PARABOLIC]:
            self.imposevelocity_type_combobox.setCurrentIndex(self.target_io_zone.velocity_info.velocity_specification_type)
        else:
            self.imposevelocity_type_combobox.setCurrentIndex(self.target_io_zone.velocity_info.velocity_specification_type - 3)
        self.on_imposevelocity_type_change()

        # Fill imposevelocity widget options
        velocity_info = self.target_io_zone.velocity_info

        # Fixed Constant
        target_widget = self.imposevelocity_fixed_constant_widget
        target_widget.input.setText(str(velocity_info.fixed_constant_value))

        # Fixed Linear
        target_widget = self.imposevelocity_fixed_linear_widget
        target_widget.v_input.setText(str(velocity_info.fixed_linear_value.v1))
        target_widget.v2_input.setText(str(velocity_info.fixed_linear_value.v2))
        target_widget.z_input.setText(str(velocity_info.fixed_linear_value.z1))
        target_widget.z2_input.setText(str(velocity_info.fixed_linear_value.z2))

        # Fixed Linear
        target_widget = self.imposevelocity_fixed_parabolic_widget
        target_widget.v_input.setText(str(velocity_info.fixed_parabolic_value.v1))
        target_widget.v2_input.setText(str(velocity_info.fixed_parabolic_value.v2))
        target_widget.v3_input.setText(str(velocity_info.fixed_parabolic_value.v3))
        target_widget.z_input.setText(str(velocity_info.fixed_parabolic_value.z1))
        target_widget.z2_input.setText(str(velocity_info.fixed_parabolic_value.z2))
        target_widget.z3_input.setText(str(velocity_info.fixed_parabolic_value.z3))

        # Variable Uniform
        target_widget = self.imposevelocity_variable_uniform_widget
        currentTableRow = 0
        for time, value in velocity_info.variable_uniform_values:
            target_widget.table.setItem(currentTableRow, 0, QtGui.QTableWidgetItem(str(time)))
            target_widget.table.setItem(currentTableRow, 1, QtGui.QTableWidgetItem(str(value)))
            currentTableRow += 1

        # Variable Linear
        target_widget = self.imposevelocity_variable_linear_widget
        currentTableRow = 0
        for time, value in velocity_info.variable_linear_values:
            target_widget.table.setItem(currentTableRow, 0, QtGui.QTableWidgetItem(str(time)))
            target_widget.table.setItem(currentTableRow, 1, QtGui.QTableWidgetItem(str(value.v1)))
            target_widget.table.setItem(currentTableRow, 2, QtGui.QTableWidgetItem(str(value.v2)))
            target_widget.table.setItem(currentTableRow, 3, QtGui.QTableWidgetItem(str(value.z1)))
            target_widget.table.setItem(currentTableRow, 4, QtGui.QTableWidgetItem(str(value.z2)))
            currentTableRow += 1

        # Variable Parabolic
        target_widget = self.imposevelocity_variable_parabolic_widget
        currentTableRow = 0
        for time, value in velocity_info.variable_parabolic_values:
            target_widget.table.setItem(currentTableRow, 0, QtGui.QTableWidgetItem(str(time)))
            target_widget.table.setItem(currentTableRow, 1, QtGui.QTableWidgetItem(str(value.v1)))
            target_widget.table.setItem(currentTableRow, 2, QtGui.QTableWidgetItem(str(value.v2)))
            target_widget.table.setItem(currentTableRow, 3, QtGui.QTableWidgetItem(str(value.v3)))
            target_widget.table.setItem(currentTableRow, 4, QtGui.QTableWidgetItem(str(value.z1)))
            target_widget.table.setItem(currentTableRow, 5, QtGui.QTableWidgetItem(str(value.z2)))
            target_widget.table.setItem(currentTableRow, 6, QtGui.QTableWidgetItem(str(value.z3)))
            currentTableRow += 1

        # File based movement
        target_widget = self.imposevelocity_file_widget
        target_widget.input.setText(str(velocity_info.file_path))

        # Add Inlet density option
        self.density_groupbox = QtGui.QGroupBox("Density")
        self.density_options_layout = QtGui.QVBoxLayout()

        self.imposerhop_layout = QtGui.QHBoxLayout()
        self.imposerhop_label = QtGui.QLabel(__("Density mode:"))
        self.imposerhop_selector = QtGui.QComboBox()
        self.imposerhop_selector.insertItems(0, [__("Fixed value"), __("Hydrostatic"), __("Extrapolated from ghost nodes")])
        self.imposerhop_selector.setCurrentIndex(self.target_io_zone.density_info.density_type)

        self.imposerhop_layout.addWidget(self.imposerhop_label)
        self.imposerhop_layout.addWidget(self.imposerhop_selector)

        self.density_options_layout.addLayout(self.imposerhop_layout)

        self.density_groupbox.setLayout(self.density_options_layout)

        # Add Inlet Z-surface option
        self.imposezsurf_layout = QtGui.QGroupBox("Elevation")
        self.imposezsurf_options_layout = QtGui.QVBoxLayout()
        self.imposezsurf_combobox_layout = QtGui.QHBoxLayout()
        self.imposezsurf_combobox_label = QtGui.QLabel("Elevation Type:")
        self.imposezsurf_combobox = QtGui.QComboBox()
        self.imposezsurf_combobox.insertItems(0, [__("Fixed"), __("Variable"), __("Automatic")])

        self.imposezsurf_type_combobox_label = QtGui.QLabel("Mode:")
        self.imposezsurf_type_combobox = QtGui.QComboBox()
        self.imposezsurf_type_combobox.insertItems(0, [__("List of times"), __("From file")])

        self.imposezsurf_fixed_widget = ImposezsurfFixedWidget()
        self.imposezsurf_variable_widget = ImposezsurfVariableWidget()
        self.imposezsurf_variable_from_file_widget = ImposezsurfVariableFromFileWidget()
        self.imposezsurf_calculated_widget = ImposezsurfCalculatedWidget()

        self.imposezsurf_combobox.currentIndexChanged.connect(self.on_imposezsurf_change)
        self.imposezsurf_type_combobox.currentIndexChanged.connect(self.on_imposezsurf_change)
        self.imposezsurf_combobox.setCurrentIndex(self.target_io_zone.elevation_info.elevation_type)
        self.on_imposezsurf_change()
        self.imposezsurf_type_combobox.setCurrentIndex(self.target_io_zone.elevation_info.zsurf_mode - 1)
        self.on_imposezsurf_type_change()

        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_combobox_label)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_combobox)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_type_combobox_label)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_type_combobox)

        self.imposezsurf_options_layout.addLayout(self.imposezsurf_combobox_layout)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_fixed_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_variable_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_variable_from_file_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_calculated_widget)

        self.imposezsurf_layout.setLayout(self.imposezsurf_options_layout)

        # Fill zsurf widget options
        elevation_info = self.target_io_zone.elevation_info

        # Fixed
        target_widget = self.imposezsurf_fixed_widget
        target_widget.zbottom_input.setText(str(elevation_info.zbottom))
        target_widget.zsurf_input.setText(str(elevation_info.zsurf))

        # Variable table
        target_widget = self.imposezsurf_variable_widget
        target_widget.savevtk_checkbox.setChecked(elevation_info.savevtk)
        target_widget.remove_checkbox.setChecked(elevation_info.remove)
        target_widget.zbottom_input.setText(str(elevation_info.zbottom))
        currentTableRow = 0
        for time, value in elevation_info.zsurftimes:
            target_widget.zsurf_table.setItem(currentTableRow, 0, QtGui.QTableWidgetItem(str(time)))
            target_widget.zsurf_table.setItem(currentTableRow, 1, QtGui.QTableWidgetItem(str(value)))
            currentTableRow += 1

        # Variable File
        target_widget = self.imposezsurf_variable_from_file_widget
        target_widget.savevtk_checkbox.setChecked(elevation_info.savevtk)
        target_widget.remove_checkbox.setChecked(elevation_info.remove)
        target_widget.zbottom_input.setText(str(elevation_info.zbottom))
        target_widget.zsurf_input.setText(str(elevation_info.zsurffile))

        # Calculated
        target_widget = self.imposezsurf_calculated_widget
        target_widget.savevtk_checkbox.setChecked(elevation_info.savevtk)
        target_widget.remove_checkbox.setChecked(elevation_info.remove)
        target_widget.zbottom_input.setText(str(elevation_info.zbottom))
        target_widget.zsurf_input.setText(str(elevation_info.zsurf))

        self.on_imposezsurf_change()
        self.on_imposezsurf_type_change()

        # Creates 2 main buttons
        self.ok_button = QtGui.QPushButton("Save")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(self.layers_layout)
        self.main_layout.addLayout(self.refilling_layout)
        self.main_layout.addLayout(self.inputtreatment_layout)
        self.main_layout.addWidget(self.zone2d3d_main_layout)
        self.main_layout.addWidget(self.imposevelocity_layout)
        self.main_layout.addWidget(self.density_groupbox)
        self.main_layout.addWidget(self.imposezsurf_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.exec_()

    def on_zone_gen_type_change(self):
        """ Reacts to the zone type being changed in the combobox. """
        if self.zone2d_option.isChecked():
            if(self.zone_gen_type_combo.currentIndex() == 0):
                self.mk_zone_generator_widget.setVisible(True)
                self.line_zone_generator_widget.setVisible(False)
                self.box_zone_generator_widget.setVisible(False)
                self.circle_zone_generator_widget.setVisible(False)
            if(self.zone_gen_type_combo.currentIndex() == 1):
                self.mk_zone_generator_widget.setVisible(False)
                self.line_zone_generator_widget.setVisible(True)
                self.box_zone_generator_widget.setVisible(False)
                self.circle_zone_generator_widget.setVisible(False)
        else:
            if(self.zone_gen_type_combo.currentIndex() == 0):
                self.mk_zone_generator_widget.setVisible(True)
                self.line_zone_generator_widget.setVisible(False)
                self.box_zone_generator_widget.setVisible(False)
                self.circle_zone_generator_widget.setVisible(False)
            if(self.zone_gen_type_combo.currentIndex() == 1):
                self.mk_zone_generator_widget.setVisible(False)
                self.line_zone_generator_widget.setVisible(False)
                self.box_zone_generator_widget.setVisible(True)
                self.circle_zone_generator_widget.setVisible(False)
            if(self.zone_gen_type_combo.currentIndex() == 2):
                self.mk_zone_generator_widget.setVisible(False)
                self.line_zone_generator_widget.setVisible(False)
                self.box_zone_generator_widget.setVisible(False)
                self.circle_zone_generator_widget.setVisible(True)

    def on_zone2d3d_radio_toggled(self):
        """ Reacts to any of the zone 2d/3d radio buttons being toggled. """
        self.zone_gen_type_combo.clear()
        if self.zone2d_option.isChecked():
            self.zone_gen_type_combo.addItems(self.ZONE_COMBO_TYPES_2D)
        else:
            self.zone_gen_type_combo.addItems(self.ZONE_COMBO_TYPES_3D)

    def on_imposerhop_change(self):
        """ Checks for imposerhop changes """
        if self.imposerhop_combobox.currentIndex() == 0:
            self.imposerhop_value_line_edit.setEnabled(True)
        else:
            self.imposerhop_value_line_edit.setEnabled(False)

    def on_imposevelocity_change(self):
        """ Checks for imposevelocity changes """
        self.imposevelocity_type_combobox.clear()
        if self.imposevelocity_combobox.currentIndex() == 0:
            self.imposevelocity_type_combobox.setEnabled(True)
            self.imposevelocity_type_combobox.addItems(self.VELOCITY_TYPES_FIXED_COMBO)
        elif self.imposevelocity_combobox.currentIndex() == 1:
            self.imposevelocity_type_combobox.setEnabled(True)
            self.imposevelocity_type_combobox.addItems(self.VELOCITY_TYPES_VARIABLE_COMBO)
        else:
            self.imposevelocity_type_combobox.setEnabled(False)

    def on_imposevelocity_type_change(self):
        if self.imposevelocity_combobox.currentIndex() == 0:
            self.imposevelocity_fixed_constant_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 0)
            self.imposevelocity_fixed_linear_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 1)
            self.imposevelocity_fixed_parabolic_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 2)
            self.imposevelocity_variable_uniform_widget.setVisible(False)
            self.imposevelocity_variable_linear_widget.setVisible(False)
            self.imposevelocity_variable_parabolic_widget.setVisible(False)
            self.imposevelocity_file_widget.setVisible(False)
        elif self.imposevelocity_combobox.currentIndex() == 1:
            self.imposevelocity_fixed_constant_widget.setVisible(False)
            self.imposevelocity_fixed_linear_widget.setVisible(False)
            self.imposevelocity_fixed_parabolic_widget.setVisible(False)
            self.imposevelocity_variable_uniform_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 0)
            self.imposevelocity_variable_linear_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 1)
            self.imposevelocity_variable_parabolic_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 2)
            self.imposevelocity_file_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() in [3, 4, 5])
        else:
            self.imposevelocity_fixed_constant_widget.setVisible(False)
            self.imposevelocity_fixed_linear_widget.setVisible(False)
            self.imposevelocity_fixed_parabolic_widget.setVisible(False)
            self.imposevelocity_variable_uniform_widget.setVisible(False)
            self.imposevelocity_variable_linear_widget.setVisible(False)
            self.imposevelocity_variable_parabolic_widget.setVisible(False)
            self.imposevelocity_file_widget.setVisible(False)

    def on_imposezsurf_change(self):
        """ Checks for imposezsurf changes """
        if self.imposezsurf_combobox.currentIndex() == 0:
            self.imposezsurf_type_combobox.setEnabled(False)
            self.imposezsurf_fixed_widget.setVisible(True)
            self.imposezsurf_variable_widget.setVisible(False)
            self.imposezsurf_variable_from_file_widget.setVisible(False)
            self.imposezsurf_calculated_widget.setVisible(False)
        elif self.imposezsurf_combobox.currentIndex() == 1:
            self.imposezsurf_type_combobox.setEnabled(True)
            if self.imposezsurf_type_combobox.currentIndex() not in [0, 1]:
                self.imposezsurf_type_combobox.setCurrentIndex(0)
            self.imposezsurf_fixed_widget.setVisible(False)
            self.imposezsurf_variable_widget.setVisible(False)
            self.imposezsurf_variable_from_file_widget.setVisible(False)
            self.imposezsurf_calculated_widget.setVisible(False)
            if self.imposezsurf_type_combobox.currentIndex() == 0:
                self.imposezsurf_variable_from_file_widget.setVisible(False)
                self.imposezsurf_variable_widget.setVisible(True)
            else:
                self.imposezsurf_variable_widget.setVisible(False)
                self.imposezsurf_variable_from_file_widget.setVisible(True)
        elif self.imposezsurf_combobox.currentIndex() == 2:
            self.imposezsurf_type_combobox.setEnabled(False)
            self.imposezsurf_fixed_widget.setVisible(False)
            self.imposezsurf_variable_widget.setVisible(False)
            self.imposezsurf_variable_from_file_widget.setVisible(False)
            self.imposezsurf_calculated_widget.setVisible(True)

    def on_imposezsurf_type_change(self):
        if self.imposezsurf_combobox.currentIndex() == 1:
            if self.imposezsurf_type_combobox.currentIndex() == 0:
                self.imposezsurf_variable_from_file_widget.setVisible(False)
                self.imposezsurf_variable_widget.setVisible(True)
            else:
                self.imposezsurf_variable_widget.setVisible(False)
                self.imposezsurf_variable_from_file_widget.setVisible(True)

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """
        self.reject()

    def on_ok(self):
        """ Save data """
        self.target_io_zone.layers = int(self.layers_line_edit.text())
        self.target_io_zone.refilling = int(self.refilling_selector.currentIndex())
        self.target_io_zone.inputtreatment = int(self.inputtreatment_selector.currentIndex())
        self.target_io_zone.density_info.density_type = int(self.imposerhop_selector.currentIndex())

        # Zone info
        info = self.target_io_zone.zone_info
        info.zone_type = InletOutletZoneType.ZONE_2D if self.zone2d_option.isChecked() else InletOutletZoneType.ZONE_3D
        if info.zone_type == InletOutletZoneType.ZONE_2D:
            info.zone_generator_type = InletOutletZoneGeneratorType.MK if self.zone_gen_type_combo.currentIndex() == 0 else InletOutletZoneGeneratorType.LINE
        elif info.zone_type == InletOutletZoneType.ZONE_3D:
            if self.zone_gen_type_combo.currentIndex() == 0:
                info.zone_generator_type = InletOutletZoneGeneratorType.MK
            elif self.zone_gen_type_combo.currentIndex() == 1:
                info.zone_generator_type = InletOutletZoneGeneratorType.BOX
            elif self.zone_gen_type_combo.currentIndex() == 2:
                info.zone_generator_type = InletOutletZoneGeneratorType.CIRCLE

        if info.zone_generator_type == InletOutletZoneGeneratorType.MK:
            info.zone_mk_generator.mkfluid = int(self.mk_zone_generator_widget.zone2d3d_mk_line_edit.text())
            info.zone_mk_generator.direction = self.DIRECTION_MAPPING[self.mk_zone_generator_widget.zone2d3d_combobox.currentIndex()]
        elif info.zone_generator_type == InletOutletZoneGeneratorType.LINE:
            info.zone_line_generator.point = [float(self.line_zone_generator_widget.point_value_x.text()), float(self.line_zone_generator_widget.point_value_y.text()), float(self.line_zone_generator_widget.point_value_z.text())]
            info.zone_line_generator.point2 = [float(self.line_zone_generator_widget.point2_value_x.text()), float(self.line_zone_generator_widget.point2_value_y.text()), float(self.line_zone_generator_widget.point2_value_z.text())]
            info.zone_line_generator.direction_enabled = self.line_zone_generator_widget.direction_enabled_checkbox.isChecked()
            info.zone_line_generator.direction = [float(self.line_zone_generator_widget.direction_value_x.text()), float(self.line_zone_generator_widget.direction_value_y.text()), float(self.line_zone_generator_widget.direction_value_z.text())]
            info.zone_line_generator.has_rotation = self.line_zone_generator_widget.rotation_enabled_checkbox.isChecked()
            info.zone_line_generator.rotate_angle = float(self.line_zone_generator_widget.rotation_angle_value.text())
        elif info.zone_generator_type == InletOutletZoneGeneratorType.BOX:
            info.zone_box_generator.point = [float(self.box_zone_generator_widget.point_value_x.text()), float(self.box_zone_generator_widget.point_value_y.text()), float(self.box_zone_generator_widget.point_value_z.text())]
            info.zone_box_generator.size = [float(self.box_zone_generator_widget.size_value_x.text()), float(self.box_zone_generator_widget.size_value_y.text()), float(self.box_zone_generator_widget.size_value_z.text())]
            info.zone_box_generator.direction = [float(self.box_zone_generator_widget.direction_value_x.text()), float(self.box_zone_generator_widget.direction_value_y.text()), float(self.box_zone_generator_widget.direction_value_z.text())]
            info.zone_box_generator.rotateaxis_enabled = self.box_zone_generator_widget.rotateaxis_enabled_checkbox.isChecked()
            info.zone_box_generator.rotateaxis_angle = float(self.box_zone_generator_widget.rotateaxis_angle_value.text())
            info.zone_box_generator.rotateaxis_point1 = [float(self.box_zone_generator_widget.rotateaxis_point1_value_x.text()), float(self.box_zone_generator_widget.rotateaxis_point1_value_y.text()), float(self.box_zone_generator_widget.rotateaxis_point1_value_z.text())]
            info.zone_box_generator.rotateaxis_point2 = [float(self.box_zone_generator_widget.rotateaxis_point2_value_x.text()), float(self.box_zone_generator_widget.rotateaxis_point2_value_y.text()), float(self.box_zone_generator_widget.rotateaxis_point2_value_z.text())]
        elif info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
            info.zone_circle_generator.point = [float(self.circle_zone_generator_widget.point_value_x.text()), float(self.circle_zone_generator_widget.point_value_y.text()), float(self.circle_zone_generator_widget.point_value_z.text())]
            info.zone_circle_generator.radius = float(self.circle_zone_generator_widget.radius_value.text())
            info.zone_circle_generator.direction = [float(self.circle_zone_generator_widget.direction_value_x.text()), float(self.circle_zone_generator_widget.direction_value_y.text()), float(self.circle_zone_generator_widget.direction_value_z.text())]

        # Velocity info
        info = self.target_io_zone.velocity_info
        info.velocity_type = self.imposevelocity_combobox.currentIndex()
        if info.velocity_type == InletOutletVelocityType.FIXED:
            if self.imposevelocity_type_combobox.currentIndex() == 0:
                info.velocity_specification_type = InletOutletVelocitySpecType.FIXED_CONSTANT
            elif self.imposevelocity_type_combobox.currentIndex() == 1:
                info.velocity_specification_type = InletOutletVelocitySpecType.FIXED_LINEAR
            elif self.imposevelocity_type_combobox.currentIndex() == 2:
                info.velocity_specification_type = InletOutletVelocitySpecType.FIXED_PARABOLIC
        elif info.velocity_type == InletOutletVelocityType.VARIABLE:
            if self.imposevelocity_type_combobox.currentIndex() == 0:
                info.velocity_specification_type = InletOutletVelocitySpecType.VARIABLE_UNIFORM
            elif self.imposevelocity_type_combobox.currentIndex() == 1:
                info.velocity_specification_type = InletOutletVelocitySpecType.VARIABLE_LINEAR
            elif self.imposevelocity_type_combobox.currentIndex() == 2:
                info.velocity_specification_type = InletOutletVelocitySpecType.VARIABLE_PARABOLIC
            elif self.imposevelocity_type_combobox.currentIndex() == 3:
                info.velocity_specification_type = InletOutletVelocitySpecType.FILE_UNIFORM
            elif self.imposevelocity_type_combobox.currentIndex() == 4:
                info.velocity_specification_type = InletOutletVelocitySpecType.FILE_LINEAR
            elif self.imposevelocity_type_combobox.currentIndex() == 5:
                info.velocity_specification_type = InletOutletVelocitySpecType.FILE_PARABOLIC
        elif info.velocity_type == InletOutletVelocityType.EXTRAPOLATED:
            pass

        if info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_CONSTANT:
            widget = self.imposevelocity_fixed_constant_widget
            info.fixed_constant_value = float(widget.input.text())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_LINEAR:
            widget = self.imposevelocity_fixed_linear_widget
            info.fixed_linear_value.v1 = float(widget.v_input.text())
            info.fixed_linear_value.v2 = float(widget.v2_input.text())
            info.fixed_linear_value.z1 = float(widget.z_input.text())
            info.fixed_linear_value.z2 = float(widget.z2_input.text())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_PARABOLIC:
            widget = self.imposevelocity_fixed_parabolic_widget
            info.fixed_parabolic_value.v1 = float(widget.v_input.text())
            info.fixed_parabolic_value.v2 = float(widget.v2_input.text())
            info.fixed_parabolic_value.v3 = float(widget.v3_input.text())
            info.fixed_parabolic_value.z1 = float(widget.z_input.text())
            info.fixed_parabolic_value.z2 = float(widget.z2_input.text())
            info.fixed_parabolic_value.z3 = float(widget.z3_input.text())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.VARIABLE_UNIFORM:
            widget = self.imposevelocity_variable_uniform_widget
            info.variable_uniform_values = []
            table = widget.table
            for i in range(0, table.rowCount()):
                if not table.item(i, 0) or not table.item(i, 1):
                    continue
                time_as_string = table.item(i, 0).text()
                value_as_string = table.item(i, 1).text()
                if time_as_string != "" and value_as_string != "":
                    info.variable_uniform_values.append((float(time_as_string), float(value_as_string)))
        elif info.velocity_specification_type == InletOutletVelocitySpecType.VARIABLE_LINEAR:
            widget = self.imposevelocity_variable_linear_widget
            info.variable_linear_values = []
            table = widget.table
            for i in range(0, table.rowCount()):
                if not table.item(i, 0) or not table.item(i, 1) or not table.item(i, 2) or not table.item(i, 3) or not table.item(i, 4):
                    continue
                time_as_string = table.item(i, 0).text()
                v1_as_string = table.item(i, 1).text()
                v2_as_string = table.item(i, 2).text()
                z1_as_string = table.item(i, 3).text()
                z2_as_string = table.item(i, 4).text()
                if time_as_string != "" and v1_as_string != "" and v2_as_string != "" and z1_as_string != "" and z2_as_string != "":
                    value = LinearVelocity()
                    value.v1 = float(v1_as_string)
                    value.v2 = float(v2_as_string)
                    value.z1 = float(z1_as_string)
                    value.z2 = float(z2_as_string)
                    info.variable_linear_values.append((float(time_as_string), value))
        elif info.velocity_specification_type == InletOutletVelocitySpecType.VARIABLE_PARABOLIC:
            widget = self.imposevelocity_variable_parabolic_widget
            info.variable_parabolic_values = []
            table = widget.table
            for i in range(0, table.rowCount()):
                if not table.item(i, 0) or not table.item(i, 1) or not table.item(i, 2) or not table.item(i, 3) or not table.item(i, 4) or not table.item(i, 5) or not table.item(i, 6):
                    continue
                time_as_string = table.item(i, 0).text()
                v1_as_string = table.item(i, 1).text()
                v2_as_string = table.item(i, 2).text()
                v3_as_string = table.item(i, 3).text()
                z1_as_string = table.item(i, 4).text()
                z2_as_string = table.item(i, 5).text()
                z3_as_string = table.item(i, 6).text()
                if time_as_string != "" and v1_as_string != "" and v2_as_string != "" and v3_as_string != "" and z1_as_string != "" and z2_as_string != "" and z3_as_string != "":
                    value = ParabolicVelocity()
                    value.v1 = float(v1_as_string)
                    value.v2 = float(v2_as_string)
                    value.v3 = float(v3_as_string)
                    value.z1 = float(z1_as_string)
                    value.z2 = float(z2_as_string)
                    value.z3 = float(z3_as_string)
                    info.variable_parabolic_values.append((float(time_as_string), value))
        elif info.velocity_specification_type in [InletOutletVelocitySpecType.FILE_UNIFORM, InletOutletVelocitySpecType.FILE_LINEAR, InletOutletVelocitySpecType.FILE_PARABOLIC]:
            widget = self.imposevelocity_file_widget
            info.file_path = widget.input.text()

        # Elevation info
        info = self.target_io_zone.elevation_info
        info.elevation_type = self.imposezsurf_combobox.currentIndex()

        if info.elevation_type == InletOutletElevationType.FIXED:
            info.zbottom = float(self.imposezsurf_fixed_widget.zbottom_input.text())
            info.zsurf = float(self.imposezsurf_fixed_widget.zsurf_input.text())
        elif info.elevation_type == InletOutletElevationType.VARIABLE:
            info.zsurf_mode = self.imposezsurf_type_combobox.currentIndex() + 1
            if info.zsurf_mode == InletOutletZSurfMode.TIMELIST:
                info.savevtk = self.imposezsurf_variable_widget.savevtk_checkbox.isChecked()
                info.remove = self.imposezsurf_variable_widget.remove_checkbox.isChecked()
                info.zbottom = float(self.imposezsurf_variable_widget.zbottom_input.text())
                info.zsurftimes = []
                table = self.imposezsurf_variable_widget.zsurf_table
                for i in range(0, table.rowCount()):
                    if not table.item(i, 0) or not table.item(i, 1):
                        continue
                    time_as_string = table.item(i, 0).text()
                    value_as_string = table.item(i, 1).text()
                    if time_as_string != "" and value_as_string != "":
                        info.zsurftimes.append((float(time_as_string), float(value_as_string)))
            if info.zsurf_mode == InletOutletZSurfMode.FILE:
                info.savevtk = self.imposezsurf_variable_from_file_widget.savevtk_checkbox.isChecked()
                info.remove = self.imposezsurf_variable_from_file_widget.remove_checkbox.isChecked()
                info.zbottom = float(self.imposezsurf_variable_from_file_widget.zbottom_input.text())
                info.zsurffile = self.imposezsurf_variable_from_file_widget.zsurf_input.text()
        elif info.elevation_type == InletOutletElevationType.AUTOMATIC:
            info.savevtk = self.imposezsurf_calculated_widget.savevtk_checkbox.isChecked()
            info.remove = self.imposezsurf_calculated_widget.remove_checkbox.isChecked()
            info.zbottom = float(self.imposezsurf_calculated_widget.zbottom_input.text())
            info.zsurf = float(self.imposezsurf_calculated_widget.zsurf_input.text())

        debug(self.target_io_zone.velocity_info.variable_uniform_values)
        InletZoneEdit.accept(self)
