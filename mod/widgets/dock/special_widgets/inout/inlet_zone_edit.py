#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Inlet Zone Configuration Dialog."""

# from PySide2.QtWidgets import QVBoxLayout
from PySide2 import QtWidgets, QtCore
from mod.dataobjects.case import Case
from mod.dataobjects.inletoutlet.inlet_outlet_zone import InletOutletZone
from mod.enums import InletOutletElevationType, InletOutletVelocitySpecType, InletOutletVelocityType, \
    InletOutletZSurfMode, InletOutletZoneGeneratorType, InletOutletZoneType, ObjectType
from mod.tools.dialog_tools import warning_dialog
from mod.tools.freecad_tools import update_inout_zone_box, update_inout_zone_circle, update_inout_zone_line, \
    update_inout_zone_3d_mk_object, change_mk_inout_zone_3d, update_inout_zone_2d_mk_object
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.int_value_input import IntValueInput
from mod.widgets.dock.special_widgets.inout.velocity_widgets import VelocityTypeFixedConstantWidget, VelocityTypeFixedLinearWidget, \
    VelocityTypeFixedParabolicWidget, VelocityTypeVariableUniformWidget, VelocityTypeVariableLinearWidget, \
    VelocityTypeVariableParabolicWidget, VelocityTypeFileWidget, FlowVelocityWidget, \
    VelocityTypeJetCircleWidget, VelocityMeshDataWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.box_zone_generator_widget import BoxZoneGeneratorWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.circle_zone_generator_widget import CircleZoneGeneratorWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.line_zone_generator_widget import LineZoneGeneratorWidget
from mod.widgets.dock.special_widgets.inout.zone_generator_widgets.mk_zone_generator_widget import MKZone2DGeneratorWidget,MKZone3DGeneratorWidget

from mod.widgets.dock.special_widgets.inout.zsurf_widgets import ImposezsurfFixedWidget, ImposezsurfVariableWidget, \
    ImposezsurfVariableFromFileWidget, ImposezsurfCalculatedWidget, ImposezsurfVariableMeshDataWidget



class InletZoneEdit(QtWidgets.QDialog):
    """ Defines Inlet/Outlet window dialog """

    ZONE_COMBO_TYPES_2D = [__("MK"), __("Line")]
    ZONE_COMBO_TYPES_3D = [__("MK"), __("Box"), __("Circle")]

    VELOCITY_TYPES_FIXED_COMBO = [__("Constant"), __("Linear"), __("Parabolic")]
    VELOCITY_TYPES_VARIABLE_COMBO = [__("Uniform"), __("Linear"), __("Parabolic"), __("Uniform from a file"),
                                     __("Linear from a file"), __("Parabolic from a file")]

    INOUT_WIDGET_WIDTH=788

    def __init__(self, inlet_object_id, parent=None):
        super().__init__(parent=parent)
        # Find the zone for which button was pressed
        self.target_io_zone: InletOutletZone = Case.the().inlet_outlet.get_io_zone_for_id(inlet_object_id)

        # Creates a dialog
        self.setWindowTitle("Inlet/Outlet object edit")

        self.inlet_zone_scroll = QtWidgets.QScrollArea()
        self.inlet_zone_scroll.setMinimumWidth(self.INOUT_WIDGET_WIDTH+20)
        self.inlet_zone_scroll.setWidgetResizable(True)
        self.inlet_zone_scroll_widget = QtWidgets.QWidget()
        self.inlet_zone_scroll_widget.setMinimumWidth(self.INOUT_WIDGET_WIDTH)

        self.inlet_zone_scroll.setWidget(self.inlet_zone_scroll_widget)
        self.inlet_zone_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.inlet_layout=QtWidgets.QVBoxLayout()
        self.inlet_zone_scroll_widget.setLayout(self.inlet_layout)
        # Add Layers option
        self.layers_layout = QtWidgets.QHBoxLayout()
        self.layers_option = QtWidgets.QLabel(__("Layers: "))
        self.layers_line_edit = IntValueInput(min_val=1)
        self.layers_line_edit.setValue(self.target_io_zone.layers)

        self.layers_layout.addWidget(self.layers_option)
        self.layers_layout.addWidget(self.layers_line_edit)

        # Add refilling option selector
        self.refilling_layout = QtWidgets.QHBoxLayout()
        self.refilling_label = QtWidgets.QLabel(__("Refilling mode:"))
        self.refilling_selector = QtWidgets.QComboBox()
        self.refilling_selector.insertItems(0, [__("Simple full"), __("Simple below Z Surface"),
                                                __("Advanced for reverse flows")])
        self.refilling_selector.setCurrentIndex(self.target_io_zone.refilling)

        self.refilling_layout.addWidget(self.refilling_label)
        self.refilling_layout.addWidget(self.refilling_selector)

        # Add inputtreatment option selector
        self.inputtreatment_layout = QtWidgets.QHBoxLayout()
        self.inputtreatment_label = QtWidgets.QLabel(__("Input Treatment mode:"))
        self.inputtreatment_selector = QtWidgets.QComboBox()
        self.inputtreatment_selector.insertItems(0, [__("No changes"), __("Convert Fluid"), __("Remove fluid")])
        self.inputtreatment_selector.setCurrentIndex(self.target_io_zone.inputtreatment)

        self.inputtreatment_layout.addWidget(self.inputtreatment_label)
        self.inputtreatment_layout.addWidget(self.inputtreatment_selector)
        ################################ ZONES ###############################
        self.zone_groupbox = QtWidgets.QGroupBox("Inlet Zone")
        self.zone_layout = QtWidgets.QVBoxLayout()


        # Fill zone generator widget options (Moved to their classes)
        if self.target_io_zone.zone_info.zone_type == InletOutletZoneType.ZONE_2D:
            if self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.MK_2D:
                self.mk_zone_generator_widget = MKZone2DGeneratorWidget()
                self.mk_zone_generator_widget.fill_values(self.target_io_zone.zone_info.zone_mk_generator,self.target_io_zone.zone_info.zone_direction_2d,self.target_io_zone.zone_info.zone_rotation_2d)
                self.zone_layout.addWidget(self.mk_zone_generator_widget)
            elif self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.LINE:
                self.line_zone_generator_widget = LineZoneGeneratorWidget()
                self.line_zone_generator_widget.fill_values(self.target_io_zone.zone_info.zone_line_generator,
                                                            self.target_io_zone.zone_info.zone_direction_2d,self.target_io_zone.zone_info.zone_rotation_2d)
                self.zone_layout.addWidget(self.line_zone_generator_widget)
        else:
            if self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.MK_3D:
                self.mk_zone_generator_widget = MKZone3DGeneratorWidget()

                self.mk_zone_generator_widget.fill_values(self.target_io_zone.zone_info.zone_mk_generator,self.target_io_zone.zone_info.zone_direction_3d,self.target_io_zone.zone_info.zone_rotation_3d)
                self.zone_layout.addWidget(self.mk_zone_generator_widget)
            elif self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.BOX:
                self.box_zone_generator_widget = BoxZoneGeneratorWidget()
                self.box_zone_generator_widget.fill_values(self.target_io_zone.zone_info.zone_box_generator,self.target_io_zone.zone_info.zone_direction_3d,self.target_io_zone.zone_info.zone_rotation_3d)
                self.zone_layout.addWidget(self.box_zone_generator_widget)
            elif self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
                self.circle_zone_generator_widget = CircleZoneGeneratorWidget()
                self.circle_zone_generator_widget.fill_values(self.target_io_zone.zone_info.zone_circle_generator,self.target_io_zone.zone_info.zone_direction_3d,self.target_io_zone.zone_info.zone_rotation_3d)
                self.zone_layout.addWidget(self.circle_zone_generator_widget)
            #self.zone_layout.addWidget(self.direction_3d_widget)
            #self.zone_layout.addWidget(self.rotation_3d_widget)

        self.zone_groupbox.setLayout(self.zone_layout)
        #########################################VELOCITY###############################################
        # Add Imposed velocity option
        self.impose_velocity_groupbox = QtWidgets.QGroupBox("Velocity")
        self.imposevelocity_options_layout = QtWidgets.QVBoxLayout()

        self.imposevelocity_velocity_layout = QtWidgets.QHBoxLayout()
        self.imposevelocity_combobox_label = QtWidgets.QLabel(__("Velocity Mode: "))
        self.imposevelocity_combobox = QtWidgets.QComboBox()
        self.imposevelocity_combobox.insertItems(0,
                                                 [__("Fixed"), __("Variable"), __("Extrapolated"), __("Interpolated")])
        self.imposevelocity_type_combobox_label = QtWidgets.QLabel(__("Velocity Type: "))
        self.imposevelocity_type_combobox = QtWidgets.QComboBox()

        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_combobox_label)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_combobox)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_type_combobox_label)
        self.imposevelocity_velocity_layout.addWidget(self.imposevelocity_type_combobox)

        self.imposevelocity_fixed_constant_widget = VelocityTypeFixedConstantWidget()
        self.imposevelocity_fixed_linear_widget = VelocityTypeFixedLinearWidget()
        self.imposevelocity_fixed_parabolic_widget = VelocityTypeFixedParabolicWidget()
        self.imposevelocity_fixed_jetcircle_widget = VelocityTypeJetCircleWidget()
        self.imposevelocity_variable_uniform_widget = VelocityTypeVariableUniformWidget()
        self.imposevelocity_variable_linear_widget = VelocityTypeVariableLinearWidget()
        self.imposevelocity_variable_parabolic_widget = VelocityTypeVariableParabolicWidget()
        self.imposevelocity_file_widget = VelocityTypeFileWidget()
        # self.imposevelocity_interpolated_widget = VelocityTypeInterpolatedWidget()
        self.imposevelocity_interpolated_widget = VelocityMeshDataWidget()
        self.imposevelocity_flowvelocity_widget = FlowVelocityWidget()


        self.imposevelocity_options_layout.addLayout(self.imposevelocity_velocity_layout)

        # Different widgets for the different options for imposevelocity
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_constant_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_linear_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_parabolic_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_fixed_jetcircle_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_variable_uniform_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_variable_linear_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_variable_parabolic_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_file_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_file_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_interpolated_widget)
        self.imposevelocity_options_layout.addWidget(self.imposevelocity_flowvelocity_widget)

        self.impose_velocity_groupbox.setLayout(self.imposevelocity_options_layout)

        self.imposevelocity_combobox.currentIndexChanged.connect(self.on_imposevelocity_change)
        self.imposevelocity_type_combobox.currentIndexChanged.connect(self.on_imposevelocity_type_change)
        self.imposevelocity_flowvelocity_widget.unit_changed.connect(self.imposevelocity_fixed_constant_widget.set_units_label)
        self.imposevelocity_flowvelocity_widget.unit_changed.connect(
            self.imposevelocity_variable_uniform_widget.set_units_label)
        self.imposevelocity_combobox.setCurrentIndex(self.target_io_zone.velocity_info.velocity_type)
        self.on_imposevelocity_change()

        if self.target_io_zone.velocity_info.velocity_specification_type in [InletOutletVelocitySpecType.FIXED_CONSTANT,
                                                                             InletOutletVelocitySpecType.FIXED_LINEAR,
                                                                             InletOutletVelocitySpecType.FIXED_PARABOLIC,
                                                                             InletOutletVelocitySpecType.FIXED_JETCIRCLE]:
            self.imposevelocity_type_combobox.setCurrentIndex(
                self.target_io_zone.velocity_info.velocity_specification_type)
        elif self.target_io_zone.velocity_info.velocity_specification_type in [
            InletOutletVelocitySpecType.VARIABLE_UNIFORM,
            InletOutletVelocitySpecType.VARIABLE_LINEAR,
            InletOutletVelocitySpecType.VARIABLE_PARABOLIC,
            InletOutletVelocitySpecType.FILE_UNIFORM,
            InletOutletVelocitySpecType.FILE_LINEAR,
            InletOutletVelocitySpecType.FILE_PARABOLIC
        ]:
            self.imposevelocity_type_combobox.setCurrentIndex(
                self.target_io_zone.velocity_info.velocity_specification_type - 4)
        self.on_imposevelocity_type_change()

        # Fill imposevelocity widget options
        velocity_info = self.target_io_zone.velocity_info
        self.imposevelocity_fixed_constant_widget.fill_values(velocity_info)
        self.imposevelocity_fixed_linear_widget.fill_values(velocity_info)
        self.imposevelocity_fixed_parabolic_widget.fill_values(velocity_info)
        self.imposevelocity_fixed_jetcircle_widget.fill_values(velocity_info)
        self.imposevelocity_variable_uniform_widget.fill_values(velocity_info)
        self.imposevelocity_variable_linear_widget.fill_values(velocity_info)
        self.imposevelocity_variable_parabolic_widget.fill_values(velocity_info)
        self.imposevelocity_file_widget.fill_values(velocity_info)
        self.imposevelocity_interpolated_widget.fill_values(velocity_info)
        self.imposevelocity_flowvelocity_widget.fill_values(velocity_info)

        #######################################DENSITY######################################################
        # Add Inlet density option
        self.density_groupbox = QtWidgets.QGroupBox("Density")
        self.density_options_layout = QtWidgets.QVBoxLayout()

        self.imposerhop_layout = QtWidgets.QHBoxLayout()
        self.imposerhop_label = QtWidgets.QLabel(__("Density mode:"))
        self.imposerhop_selector = QtWidgets.QComboBox()
        self.imposerhop_selector.insertItems(0, [__("Fixed value"), __("Hydrostatic"),
                                                 __("Extrapolated from ghost nodes")])
        self.imposerhop_selector.setCurrentIndex(self.target_io_zone.density_info.density_type)

        self.imposerhop_layout.addWidget(self.imposerhop_label)
        self.imposerhop_layout.addWidget(self.imposerhop_selector)

        self.density_options_layout.addLayout(self.imposerhop_layout)

        self.density_groupbox.setLayout(self.density_options_layout)

        #####################################Z-SURF#########################################################
        # Add Inlet Z-surface option
        self.impose_zsurf_groupbox = QtWidgets.QGroupBox("Elevation")
        self.impose_zsurf_groupbox.setCheckable(True)
        self.impose_zsurf_groupbox.setChecked(self.target_io_zone.elevation_info.elevation_enabled)
        self.impose_zsurf_groupbox.clicked.connect(self.on_zsurf_check)
        self.imposezsurf_options_layout = QtWidgets.QVBoxLayout()
        self.imposezsurf_combobox_layout = QtWidgets.QHBoxLayout()
        self.imposezsurf_combobox_label = QtWidgets.QLabel("Elevation Type:")
        self.imposezsurf_combobox = QtWidgets.QComboBox()
        self.imposezsurf_combobox.insertItems(0, [__("Fixed"), __("Variable"), __("Automatic")])

        self.imposezsurf_type_combobox_label = QtWidgets.QLabel("Mode:")
        self.imposezsurf_type_combobox = QtWidgets.QComboBox()
        self.imposezsurf_type_combobox.insertItems(0, [__("List of times"), __("From csv file"), __("Meshdata file")])

        self.imposezsurf_fixed_widget = ImposezsurfFixedWidget()
        self.imposezsurf_variable_widget = ImposezsurfVariableWidget()
        self.imposezsurf_variable_from_file_widget = ImposezsurfVariableFromFileWidget()
        self.imposezsurf_variable_meshdata_widget = ImposezsurfVariableMeshDataWidget()
        self.imposezsurf_calculated_widget = ImposezsurfCalculatedWidget()

        self.imposezsurf_combobox.currentIndexChanged.connect(self.on_imposezsurf_change)
        self.imposezsurf_type_combobox.currentIndexChanged.connect(self.on_imposezsurf_change)
        self.imposezsurf_combobox.setCurrentIndex(self.target_io_zone.elevation_info.elevation_type)
        self.imposezsurf_type_combobox.setCurrentIndex(self.target_io_zone.elevation_info.zsurf_mode - 1)
        self.on_zsurf_check(self.impose_zsurf_groupbox.isChecked())

        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_combobox_label)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_combobox)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_type_combobox_label)
        self.imposezsurf_combobox_layout.addWidget(self.imposezsurf_type_combobox)

        self.imposezsurf_options_layout.addLayout(self.imposezsurf_combobox_layout)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_fixed_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_variable_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_variable_from_file_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_variable_meshdata_widget)
        self.imposezsurf_options_layout.addWidget(self.imposezsurf_calculated_widget)

        self.impose_zsurf_groupbox.setLayout(self.imposezsurf_options_layout)
        # Fill zsurf widget options
        elevation_info = self.target_io_zone.elevation_info
        self.imposezsurf_fixed_widget.fill_values(elevation_info)
        self.imposezsurf_variable_widget.fill_values(elevation_info)
        self.imposezsurf_variable_from_file_widget.fill_values(elevation_info)
        self.imposezsurf_variable_meshdata_widget.fill_values(elevation_info)
        self.imposezsurf_calculated_widget.fill_values(elevation_info)

        self.on_imposezsurf_change()
        self.on_imposezsurf_type_change()
        self.on_zsurf_check(self.impose_zsurf_groupbox.isChecked())

        # Creates 2 main buttons
        self.ok_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch(1)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.inlet_layout.addLayout(self.layers_layout)
        self.inlet_layout.addLayout(self.refilling_layout)
        self.inlet_layout.addLayout(self.inputtreatment_layout)
        self.inlet_layout.addWidget(self.zone_groupbox)
        self.inlet_layout.addWidget(self.impose_velocity_groupbox)
        self.inlet_layout.addWidget(self.density_groupbox)
        self.inlet_layout.addWidget(self.impose_zsurf_groupbox)

        self.main_layout.addWidget(self.inlet_zone_scroll)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)




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
            if self.target_io_zone.zone_info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
                self.imposevelocity_type_combobox.addItem(__("JetCircle"))
        elif self.imposevelocity_combobox.currentIndex() == 1:
            self.imposevelocity_type_combobox.setEnabled(True)
            self.imposevelocity_type_combobox.addItems(self.VELOCITY_TYPES_VARIABLE_COMBO)
        else:
            self.imposevelocity_type_combobox.setEnabled(False)
        self.on_imposevelocity_type_change()

    def on_imposevelocity_type_change(self):
        if self.imposevelocity_combobox.currentIndex() == 0:
            self.imposevelocity_fixed_constant_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 0)
            self.imposevelocity_fixed_linear_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 1)
            self.imposevelocity_fixed_parabolic_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 2)
            self.imposevelocity_fixed_jetcircle_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 3)
            self.imposevelocity_variable_uniform_widget.setVisible(False)
            self.imposevelocity_variable_linear_widget.setVisible(False)
            self.imposevelocity_variable_parabolic_widget.setVisible(False)
            self.imposevelocity_file_widget.setVisible(False)
            self.imposevelocity_interpolated_widget.setVisible(False)
            self.imposevelocity_flowvelocity_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 0)

        elif self.imposevelocity_combobox.currentIndex() == 1:
            self.imposevelocity_fixed_constant_widget.setVisible(False)
            self.imposevelocity_fixed_linear_widget.setVisible(False)
            self.imposevelocity_fixed_parabolic_widget.setVisible(False)
            self.imposevelocity_fixed_jetcircle_widget.setVisible(False)
            self.imposevelocity_variable_uniform_widget.setVisible(
                self.imposevelocity_type_combobox.currentIndex() == 0)
            self.imposevelocity_variable_linear_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 1)
            self.imposevelocity_variable_parabolic_widget.setVisible(
                self.imposevelocity_type_combobox.currentIndex() == 2)
            self.imposevelocity_file_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() in [3, 4, 5])
            self.imposevelocity_interpolated_widget.setVisible(False)
            self.imposevelocity_flowvelocity_widget.setVisible(self.imposevelocity_type_combobox.currentIndex() == 0)
        elif self.imposevelocity_combobox.currentIndex() == 2:
            self.imposevelocity_fixed_constant_widget.setVisible(False)
            self.imposevelocity_fixed_linear_widget.setVisible(False)
            self.imposevelocity_fixed_parabolic_widget.setVisible(False)
            self.imposevelocity_fixed_jetcircle_widget.setVisible(False)
            self.imposevelocity_variable_uniform_widget.setVisible(False)
            self.imposevelocity_variable_linear_widget.setVisible(False)
            self.imposevelocity_variable_parabolic_widget.setVisible(False)
            self.imposevelocity_file_widget.setVisible(False)
            self.imposevelocity_interpolated_widget.setVisible(False)
            self.imposevelocity_flowvelocity_widget.setVisible(False)
        elif self.imposevelocity_combobox.currentIndex() == 3:
            self.imposevelocity_fixed_constant_widget.setVisible(False)
            self.imposevelocity_fixed_linear_widget.setVisible(False)
            self.imposevelocity_fixed_parabolic_widget.setVisible(False)
            self.imposevelocity_fixed_jetcircle_widget.setVisible(False)
            self.imposevelocity_variable_uniform_widget.setVisible(False)
            self.imposevelocity_variable_linear_widget.setVisible(False)
            self.imposevelocity_variable_parabolic_widget.setVisible(False)
            self.imposevelocity_file_widget.setVisible(False)
            self.imposevelocity_interpolated_widget.setVisible(True)
            self.imposevelocity_flowvelocity_widget.setVisible(False)

    def on_zsurf_check(self, check):
        if not check:
            for x in [self.imposezsurf_combobox_label, self.imposezsurf_combobox, self.imposezsurf_type_combobox_label,
                     self.imposezsurf_type_combobox, self.imposezsurf_fixed_widget, self.imposezsurf_variable_widget,
                     self.imposezsurf_variable_from_file_widget, self.imposezsurf_variable_meshdata_widget,
                     self.imposezsurf_calculated_widget]:
                x.setVisible(check)
        else:
            for x in [self.imposezsurf_combobox_label, self.imposezsurf_combobox, self.imposezsurf_type_combobox_label,
                     self.imposezsurf_type_combobox]:
                x.setVisible(check)
            self.on_imposezsurf_change()
            self.on_imposezsurf_type_change()

    def on_imposezsurf_change(self):
        """ Checks for imposezsurf changes """
        if self.imposezsurf_combobox.currentIndex() == 0:
            self.imposezsurf_type_combobox.setEnabled(False)
            self.imposezsurf_fixed_widget.setVisible(True)
            self.imposezsurf_variable_widget.setVisible(False)
            self.imposezsurf_variable_from_file_widget.setVisible(False)
            self.imposezsurf_variable_meshdata_widget.setVisible(False)
            self.imposezsurf_calculated_widget.setVisible(False)
        elif self.imposezsurf_combobox.currentIndex() == 1:
            self.imposezsurf_type_combobox.setEnabled(True)
            if self.imposezsurf_type_combobox.currentIndex() not in [0, 1, 2]:
                self.imposezsurf_type_combobox.setCurrentIndex(0)
            self.imposezsurf_fixed_widget.setVisible(False)
            self.imposezsurf_variable_widget.setVisible(False)
            self.imposezsurf_variable_from_file_widget.setVisible(False)
            self.imposezsurf_variable_meshdata_widget.setVisible(False)
            self.imposezsurf_calculated_widget.setVisible(False)
            self.on_imposezsurf_type_change()
        elif self.imposezsurf_combobox.currentIndex() == 2:
            self.imposezsurf_type_combobox.setEnabled(False)
            self.imposezsurf_fixed_widget.setVisible(False)
            self.imposezsurf_variable_widget.setVisible(False)
            self.imposezsurf_variable_from_file_widget.setVisible(False)
            self.imposezsurf_variable_meshdata_widget.setVisible(False)
            self.imposezsurf_calculated_widget.setVisible(True)

    def on_imposezsurf_type_change(self):
        if self.imposezsurf_combobox.currentIndex() == 1:
            if self.imposezsurf_type_combobox.currentIndex() == 0:
                self.imposezsurf_variable_widget.setVisible(True)
                self.imposezsurf_variable_from_file_widget.setVisible(False)
                self.imposezsurf_variable_meshdata_widget.setVisible(False)
            elif self.imposezsurf_type_combobox.currentIndex() == 1:
                self.imposezsurf_variable_widget.setVisible(False)
                self.imposezsurf_variable_from_file_widget.setVisible(True)
                self.imposezsurf_variable_meshdata_widget.setVisible(False)
            elif self.imposezsurf_type_combobox.currentIndex() == 2:
                self.imposezsurf_variable_widget.setVisible(False)
                self.imposezsurf_variable_from_file_widget.setVisible(False)
                self.imposezsurf_variable_meshdata_widget.setVisible(True)

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """

        self.reject()

    def on_ok(self):
        """ Save data """
        self.target_io_zone.layers = self.layers_line_edit.value()
        self.target_io_zone.refilling = int(self.refilling_selector.currentIndex())
        self.target_io_zone.inputtreatment = int(self.inputtreatment_selector.currentIndex())
        self.target_io_zone.density_info.density_type = int(self.imposerhop_selector.currentIndex())

        # Zone info
        info = self.target_io_zone.zone_info
        if info.zone_generator_type == InletOutletZoneGeneratorType.MK_2D:
            if self.check_mk_inlet():
                mk = info.zone_mk_generator.mkfluid
                values = self.mk_zone_generator_widget.to_dict()
                info.zone_rotation_2d.save_values(self.mk_zone_generator_widget.rotation_2d_widget.to_dict())
                info.zone_direction_2d.save_values(self.mk_zone_generator_widget.direction_2d_widget.to_dict())
                info.zone_mk_generator.save_values(self.mk_zone_generator_widget.to_dict())
                if self.target_io_zone.fc_object_name:
                    original = Case.the().get_first_fc_object_from_mk(ObjectType.FLUID,values["mkfluid"])
                    if values["mkfluid"] != mk:
                        change_mk_inout_zone_3d(self.target_io_zone.fc_object_name,original)
                    update_inout_zone_2d_mk_object(self.target_io_zone.fc_object_name, info.zone_mk_generator, info.zone_direction_2d,
                                   info.zone_rotation_2d,original)
            else:
                return False
        elif info.zone_generator_type == InletOutletZoneGeneratorType.MK_3D:
            if self.check_mk_inlet():
                mk=info.zone_mk_generator.mkfluid
                values=self.mk_zone_generator_widget.to_dict()
                info.zone_rotation_3d.save_values(self.mk_zone_generator_widget.rotation_3d_widget.to_dict())
                info.zone_direction_3d.save_values(self.mk_zone_generator_widget.direction_3d_widget.to_dict())
                info.zone_mk_generator.save_values(values)
                if self.target_io_zone.fc_object_name:
                    if values["mkfluid"] != mk:
                        change_mk_inout_zone_3d(self.target_io_zone.fc_object_name,Case.the().get_first_fc_object_from_mk(ObjectType.FLUID,values["mkfluid"]))
                    update_inout_zone_3d_mk_object(self.target_io_zone.fc_object_name, info.zone_mk_generator, info.zone_direction_3d,
                                   info.zone_rotation_3d,Case.the().get_first_fc_object_from_mk(ObjectType.FLUID,values["mkfluid"]))
            else:
                return False
        elif info.zone_generator_type == InletOutletZoneGeneratorType.LINE:
            info.zone_line_generator.save_values(self.line_zone_generator_widget.to_dict())
            info.zone_rotation_2d.save_values(self.line_zone_generator_widget.rotation_widget.to_dict())
            info.zone_direction_2d.save_values(self.line_zone_generator_widget.direction_widget.to_dict())
            update_inout_zone_line(self.target_io_zone.fc_object_name, info.zone_line_generator, info.zone_direction_2d,
                                   info.zone_rotation_2d)
        elif info.zone_generator_type == InletOutletZoneGeneratorType.BOX:
            if self.check_box_inlet():
                info.zone_box_generator.save_values(self.box_zone_generator_widget.to_dict())
                info.zone_direction_3d.save_values(self.box_zone_generator_widget.direction_widget.to_dict())
                info.zone_rotation_3d.save_values(self.box_zone_generator_widget.rotation_widget.to_dict())
                update_inout_zone_box(self.target_io_zone.fc_object_name, info.zone_box_generator, info.zone_direction_3d,
                                      info.zone_rotation_3d)
            else:
                return False
        elif info.zone_generator_type == InletOutletZoneGeneratorType.CIRCLE:
            info.zone_circle_generator.save_values(self.circle_zone_generator_widget.to_dict())
            info.zone_rotation_3d.save_values(self.circle_zone_generator_widget.rotation_widget.to_dict())
            info.zone_direction_3d.save_values(self.circle_zone_generator_widget.direction_widget.to_dict())
            info.zone_circle_generator.save_values(self.circle_zone_generator_widget.to_dict())
            update_inout_zone_circle(self.target_io_zone.fc_object_name, info.zone_circle_generator,
                                     info.zone_direction_3d, info.zone_rotation_3d)

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
            elif self.imposevelocity_type_combobox.currentIndex() == 3:
                info.velocity_specification_type = InletOutletVelocitySpecType.FIXED_JETCIRCLE
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
        elif info.velocity_type == InletOutletVelocityType.INTERPOLATED:
            info.velocity_specification_type = InletOutletVelocitySpecType.FILE_MESHDATA

        if info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_CONSTANT:
            info.save_v_constant(self.imposevelocity_fixed_constant_widget.to_dict())
            info.save_flow_velocity(self.imposevelocity_flowvelocity_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_LINEAR:
            info.save_v_fixed_linear(self.imposevelocity_fixed_linear_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_PARABOLIC:
            info.save_v_fixed_parabolic(self.imposevelocity_fixed_parabolic_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.FIXED_JETCIRCLE:
            info.save_v_fixed_jetcircle(self.imposevelocity_fixed_jetcircle_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.VARIABLE_UNIFORM:
            info.save_v_variable_uniform(self.imposevelocity_variable_uniform_widget.to_dict())
            info.save_flow_velocity(self.imposevelocity_flowvelocity_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.VARIABLE_LINEAR:
            info.save_v_variable_linear(self.imposevelocity_variable_linear_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.VARIABLE_PARABOLIC:
            info.save_v_variable_parabolic(self.imposevelocity_variable_parabolic_widget.to_dict())
        elif info.velocity_specification_type in [InletOutletVelocitySpecType.FILE_UNIFORM,
                                                  InletOutletVelocitySpecType.FILE_LINEAR,
                                                  InletOutletVelocitySpecType.FILE_PARABOLIC]:
            info.save_v_file(self.imposevelocity_file_widget.to_dict())
        elif info.velocity_specification_type == InletOutletVelocitySpecType.FILE_MESHDATA:
            info.save_v_mesh_data(self.imposevelocity_interpolated_widget.to_dict())

        # Elevation info
        info = self.target_io_zone.elevation_info
        info.elevation_enabled = self.impose_zsurf_groupbox.isChecked()
        info.elevation_type = self.imposezsurf_combobox.currentIndex()

        if info.elevation_type == InletOutletElevationType.FIXED:
            info.save_fixed(self.imposezsurf_fixed_widget.to_dict())
        elif info.elevation_type == InletOutletElevationType.VARIABLE:
            info.zsurf_mode = self.imposezsurf_type_combobox.currentIndex() + 1
            if info.zsurf_mode == InletOutletZSurfMode.TIMELIST:
                info.save_variable_timelist(self.imposezsurf_variable_widget.to_dict())
            elif info.zsurf_mode == InletOutletZSurfMode.FILE:
                info.save_variable_csv_file(self.imposezsurf_variable_from_file_widget.to_dict())
            elif info.zsurf_mode == InletOutletZSurfMode.MESHDATA:
                info.save_variable_meshdata(self.imposezsurf_variable_meshdata_widget.to_dict())
        elif info.elevation_type == InletOutletElevationType.AUTOMATIC:
            info.save_automatic(self.imposezsurf_calculated_widget.to_dict())

        InletZoneEdit.accept(self)

    def check_box_inlet(self):
        box_axis=self.box_zone_generator_widget.get_axis()
        if box_axis is False:
            warning_dialog("Inlet box size must be zero in direction's axis and upper than 0 in the other axes")
            return False
        else:
            direction_axis=self.box_zone_generator_widget.direction_widget.get_axis()
            if direction_axis is False:
                warning_dialog("Inlet box direction must be parallel to one axis")
                return False
            else:
                if box_axis != direction_axis:
                    warning_dialog("Inlet box's zero size axis must be the same as direction axis")
                    return False
        return True

    def check_mk_inlet(self):
        mk=self.mk_zone_generator_widget.zone2d3d_mk_selector.get_mk_value()
        if mk==-1:
            warning_dialog("You need to select a fluid mk for Mk Inlet Zone. Make sure you have added some fluid to the simulation and chosen it in the selector")
            return False
        return True

