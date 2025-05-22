#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics Special Options Selection Dialog. """

import FreeCAD
import FreeCADGui

from PySide2 import QtWidgets


from mod.tools.translation_tools import __
from mod.tools.dialog_tools import error_dialog, warning_dialog, ok_cancel_dialog
from mod.enums import ObjectType, DampingType
from mod.constants import APP_NAME
from mod.tools.freecad_tools import setup_damping_environment, delete_group
from mod.widgets.dock.special_widgets.damping.damping_box_config_dialog import DampingBoxConfigDialog
from mod.widgets.dock.special_widgets.damping.damping_cylinder_dialog import DampingCylinderConfigDialog
from mod.widgets.dock.special_widgets.flex_struct_dialog import FlexStructDialog
from mod.widgets.dock.special_widgets.gauges.gauges_list_dialog import GaugesListDialog

from mod.widgets.dock.special_widgets.ml_piston_1d_config_dialog import MLPiston1DConfigDialog
from mod.widgets.dock.special_widgets.ml_piston_2d_config_dialog import MLPiston2DConfigDialog
from mod.widgets.dock.special_widgets.outfilters.outparts_dialog import OutpartsDialog
from mod.widgets.dock.special_widgets.relaxation_zone.relaxation_zone_regular_config_dialog import RelaxationZoneRegularConfigDialog
from mod.widgets.dock.special_widgets.relaxation_zone.relaxation_zone_irregular_config_dialog import RelaxationZoneIrregularConfigDialog
from mod.widgets.dock.special_widgets.relaxation_zone.relaxation_zone_file_config_dialog import RelaxationZoneFileConfigDialog
from mod.widgets.dock.special_widgets.relaxation_zone.relaxation_zone_uniform_config_dialog import RelaxationZoneUniformConfigDialog
from mod.widgets.dock.special_widgets.acceleration_input_dialog import AccelerationInputDialog
from mod.widgets.dock.special_widgets.damping.damping_zone_config_dialog import DampingZoneConfigDialog
from mod.widgets.dock.special_widgets.inout.inlet_config_dialog import InletConfigDialog
from mod.widgets.dock.special_widgets.chrono.chrono_config_dialog import ChronoConfigDialog
from mod.widgets.dock.special_widgets.moorings.moorings_configuration_dialog import MooringsConfigurationDialog

from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.dataobjects.properties.mk_based_properties import MKBasedProperties
from mod.dataobjects.properties.ml_piston.ml_piston_1d import MLPiston1D
from mod.dataobjects.properties.ml_piston.ml_piston_2d import MLPiston2D
from mod.dataobjects.relaxation_zone.relaxation_zone_regular import RelaxationZoneRegular
from mod.dataobjects.relaxation_zone.relaxation_zone_irregular import RelaxationZoneIrregular
from mod.dataobjects.relaxation_zone.relaxation_zone_file import RelaxationZoneFile
from mod.dataobjects.relaxation_zone.relaxation_zone_uniform import RelaxationZoneUniform
from mod.widgets.dock.special_widgets.variable_res.variable_res_config_dialog import VariableResConfigDialog


class SpecialOptionsSelectorDialog(QtWidgets.QDialog):
    """ A dialog with different buttons to access special DesignSPHysics options for a case. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(__("Special"))
        self.setMinimumWidth(200)
        self.sp_window_layout = QtWidgets.QVBoxLayout()

        self.sp_damping_button = QtWidgets.QPushButton(__("Damping"))
        self.sp_damping_menu = QtWidgets.QMenu()
        self.sp_damping_menu.addAction(__("Damping Zone"))
        self.sp_damping_menu.addAction(__("Damping Box"))
        self.sp_damping_menu.addAction(__("Damping Cylinder"))
        self.sp_damping_button.setMenu(self.sp_damping_menu)

        self.sp_gauges_button = QtWidgets.QPushButton(__("Gauges"))
        self.sp_vres_button = QtWidgets.QPushButton(__("Variable Resolution"))

        self.sp_inlet_button = QtWidgets.QPushButton(__("Inlet/Outlet"))
        self.sp_chrono_button = QtWidgets.QPushButton(__("Project Chrono"))
        self.sp_multilayeredmb_button = QtWidgets.QPushButton(__("Multi-layered Piston"))
        self.sp_multilayeredmb_menu = QtWidgets.QMenu()
        self.sp_multilayeredmb_menu.addAction(__("1 Dimension"))
        self.sp_multilayeredmb_menu.addAction(__("2 Dimensions"))
        self.sp_multilayeredmb_button.setMenu(self.sp_multilayeredmb_menu)

        self.sp_relaxationzone_button = QtWidgets.QPushButton(__("Relaxation Zone"))
        self.sp_relaxationzone_menu = QtWidgets.QMenu()
        self.sp_relaxationzone_menu.addAction(__("Regular waves"))
        self.sp_relaxationzone_menu.addAction(__("Irregular waves"))
        self.sp_relaxationzone_menu.addAction(__("External Input"))
        self.sp_relaxationzone_menu.addAction(__("Uniform velocity"))
        self.sp_relaxationzone_button.setMenu(self.sp_relaxationzone_menu)

        self.sp_accinput_button = QtWidgets.QPushButton(__("Acceleration Inputs"))

        self.sp_moorings_button = QtWidgets.QPushButton(__("MoorDynPlus"))

        self.sp_flex_struct_button=QtWidgets.QPushButton(__("Flexible Structure"))

        self.sp_outparts_button = QtWidgets.QPushButton(__("Output particle filters"))

        self.gui_test_tool = QtWidgets.QPushButton(__("Gui test tool"))

        self.sp_damping_menu.triggered.connect(self.on_damping_menu)
        self.sp_inlet_button.clicked.connect(self.on_inlet_option)
        self.sp_chrono_button.clicked.connect(self.on_chrono_option)
        self.sp_gauges_button.clicked.connect(self.on_gauges_option)
        self.sp_multilayeredmb_menu.triggered.connect(self.on_multilayeredmb_menu)
        self.sp_relaxationzone_menu.triggered.connect(self.on_relaxationzone_menu)
        self.sp_accinput_button.clicked.connect(self.on_accinput_button)
        self.sp_moorings_button.clicked.connect(self.on_moorings_button)
        self.sp_flex_struct_button.clicked.connect(self.on_flex_struct_button)
        self.sp_vres_button.clicked.connect(self.on_vres_button)
        self.sp_outparts_button.clicked.connect(self.on_outparts_button)

        # Add buttons to the special window
        self.full_widget_list=[
            self.sp_inlet_button,
            self.sp_vres_button, #VRES hidden provisionally
            self.sp_gauges_button,
            self.sp_outparts_button,
            self.sp_accinput_button,
            self.sp_chrono_button,
            self.sp_moorings_button,
            self.sp_flex_struct_button,
            self.sp_damping_button,
            self.sp_multilayeredmb_button,
            self.sp_relaxationzone_button
        ]

        self.basic_widget_list=[
            self.sp_inlet_button,
            self.sp_vres_button, #VRES hidden provisionally
            self.sp_damping_button,
            self.sp_chrono_button,
            self.sp_moorings_button,
            self.sp_flex_struct_button
        ]
        if ApplicationSettings.the().basic_visualization :
            self.widget_list=self.basic_widget_list
        else:
            self.widget_list = self.full_widget_list
        for widget in self.widget_list:
            self.sp_window_layout.addWidget(widget)
        self.setLayout(self.sp_window_layout)

        if not Case.the().executable_paths.supports_chrono():
            self.sp_chrono_button.hide()

        if not Case.the().executable_paths.supports_moorings() and not ApplicationSettings.the().force_moordynplus_support_enabled:
            self.sp_moorings_button.hide()

        self.exec_()

    def on_damping_menu(self,action):
        """ Defines damping menu behaviour"""
        if __("Damping Zone") in action.text():
            damping_type: DampingType = DampingType.ZONE
        elif __("Damping Box") in action.text():
            damping_type: DampingType = DampingType.BOX
        else: #if __("Damping Cylinder") in action.text():
            damping_type: DampingType = DampingType.CYLINDER

        damping_group_name = setup_damping_environment(damping_type)
        Case.the().add_damping_group(damping_group_name)
        damping=Case.the().get_damping_zone(damping_group_name)
        damping.damping_type=damping_type
        group=FreeCAD.ActiveDocument.getObject(damping_group_name)
        if damping.damping_type==DampingType.ZONE :
            ret=DampingZoneConfigDialog(damping=damping,group=group ,parent=None).exec_()
        elif damping.damping_type==DampingType.BOX :
            ret=DampingBoxConfigDialog(damping=damping, group=group, parent=None).exec_()
        elif damping.damping_type == DampingType.CYLINDER:
            ret=DampingCylinderConfigDialog(damping=damping, group=group, parent=None).exec_()
        if ret != QtWidgets.QDialog.Accepted:
            Case.the().remove_damping_zone(damping_group_name)
            delete_group(damping_group_name)
        self.accept()




    def on_inlet_option(self):
        """ Defines Inlet/Outlet behaviour """
        InletConfigDialog(parent=None).exec_()
        self.accept()

    def on_chrono_option(self):
        """ Defines Coupling CHRONO behaviour"""
        ChronoConfigDialog(parent=None).exec_()
        self.accept()

    def on_multilayeredmb_menu(self, action):
        """ Defines MLPiston menu behaviour"""
        # Get currently selected object
        try:
            selection = FreeCADGui.Selection.getSelection()[0]
        except IndexError:
            error_dialog(__("You must select an object"))
            return

        # Check if object is in the simulation
        if not Case.the().is_object_in_simulation(selection.Name):
            error_dialog(__("The selected object must be added to the simulation"))
            return

        # Check if it is fluid and warn the user.
        if Case.the().get_simulation_object(selection.Name).type == ObjectType.FLUID:
            error_dialog(__("You cannot apply a piston movement to a fluid.\nPlease select a boundary and try again"))
            return

        # Get selection mk
        selection_obj = Case.the().get_simulation_object(selection.Name)
        selection_mk: int = selection_obj.obj_mk
        selection_real_mk:int = selection_obj.real_mk()
        mk_properties: MKBasedProperties = Case.the().get_mk_based_properties(selection_real_mk)

        # Check that this mk has no other motions applied
        if mk_properties.has_movements():
            # MK has motions applied. Warn the user and delete them
            motion_delete_warning = ok_cancel_dialog(APP_NAME, __("This mk already has motions applied. Setting a Multi-layered piston will delete all of its movement. Are you sure?"))
            if motion_delete_warning == QtWidgets.QMessageBox.Cancel:
                return
            mk_properties.remove_all_movements()

        # 1D or 2D piston
        if __("1 Dimension") in action.text():
            if mk_properties.mlayerpiston and not isinstance(mk_properties.mlayerpiston, MLPiston1D):
                overwrite_warn = ok_cancel_dialog(APP_NAME, __("You're about to overwrite a previous coupling movement for this mk. Are you sure?"))
                if overwrite_warn == QtWidgets.QMessageBox.Cancel:
                    return

            config_dialog = MLPiston1DConfigDialog(selection_mk, mk_properties.mlayerpiston, parent=None)
            if config_dialog.result() == QtWidgets.QDialog.Accepted:
                warning_dialog(__("All changes have been applied for mk = {}").format(selection_mk))
            mk_properties.mlayerpiston = config_dialog.mlpiston1d

        if __("2 Dimensions") in action.text():
            # Check that there's no other multilayered piston for this mk
            if mk_properties.mlayerpiston and not isinstance(mk_properties.mlayerpiston, MLPiston2D):
                overwrite_warn = ok_cancel_dialog(APP_NAME, __("You're about to overwrite a previous coupling movement for this mk. Are you sure?"))
                if overwrite_warn == QtWidgets.QMessageBox.Cancel:
                    return

            config_dialog = MLPiston2DConfigDialog(selection_mk, mk_properties.mlayerpiston, parent=None)
            if config_dialog.result() == QtWidgets.QDialog.Accepted:
                warning_dialog(__("All changes have been applied for mk = {}").format(selection_mk))
            mk_properties.mlayerpiston = config_dialog.mlpiston2d

        self.accept()

    def on_relaxationzone_menu(self, action):
        """ Defines Relaxation Zone menu behaviour."""

        # Check which type of relaxationzone it is
        if action.text() == __("Regular waves"):
            if Case.the().relaxation_zone is not None:
                if not isinstance(Case.the().relaxation_zone, RelaxationZoneRegular):
                    overwrite_warn = ok_cancel_dialog(__("Relaxation Zone"), __("There's already another type of Relaxation Zone defined. Continuing will overwrite it. Are you sure?"))
                    if overwrite_warn == QtWidgets.QMessageBox.Cancel:
                        return
                    Case.the().relaxation_zone = RelaxationZoneRegular()

            config_dialog = RelaxationZoneRegularConfigDialog(Case.the().relaxation_zone, parent=None)

            # Set the relaxation zone. Can be an object or be None
            Case.the().relaxation_zone = config_dialog.relaxationzone
        if action.text() == __("Irregular waves"):
            if Case.the().relaxation_zone is not None:
                if not isinstance(Case.the().relaxation_zone, RelaxationZoneIrregular):
                    overwrite_warn = ok_cancel_dialog(__("Relaxation Zone"), __("There's already another type of Relaxation Zone defined. Continuing will overwrite it. Are you sure?"))
                    if overwrite_warn == QtWidgets.QMessageBox.Cancel:
                        return
                    Case.the().relaxation_zone = RelaxationZoneIrregular()

            config_dialog = RelaxationZoneIrregularConfigDialog(Case.the().relaxation_zone, parent=None)

            # Set the relaxation zone. Can be an object or be None
            Case.the().relaxation_zone = config_dialog.relaxationzone
        if action.text() == __("External Input"):
            if Case.the().relaxation_zone is not None:
                if not isinstance(Case.the().relaxation_zone, RelaxationZoneFile):
                    overwrite_warn = ok_cancel_dialog(__("Relaxation Zone"), __("There's already another type of Relaxation Zone defined. Continuing will overwrite it. Are you sure?"))
                    if overwrite_warn == QtWidgets.QMessageBox.Cancel:
                        return
                    Case.the().relaxation_zone = RelaxationZoneFile()

            config_dialog = RelaxationZoneFileConfigDialog(Case.the().relaxation_zone, parent=None)

            # Set the relaxation zone. Can be an object or be None
            Case.the().relaxation_zone = config_dialog.relaxationzone

        if action.text() == __("Uniform velocity"):
            if Case.the().relaxation_zone is not None:
                if not isinstance(Case.the().relaxation_zone, RelaxationZoneUniform):
                    overwrite_warn = ok_cancel_dialog(__("Relaxation Zone"), __("There's already another type of Relaxation Zone defined. Continuing will overwrite it. Are you sure?"))
                    if overwrite_warn == QtWidgets.QMessageBox.Cancel:
                        return
                    Case.the().relaxation_zone = RelaxationZoneUniform()

            config_dialog = RelaxationZoneUniformConfigDialog(Case.the().relaxation_zone, parent=None)

            # Set the relaxation zone. Can be an object or be None
            Case.the().relaxation_zone = config_dialog.relaxationzone

        self.accept()

    def on_accinput_button(self):
        """ Acceleration input button behaviour."""
        accinput_dialog = AccelerationInputDialog(Case.the().acceleration_input, parent=None)
        result = accinput_dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            Case.the().acceleration_input = accinput_dialog.get_result()
        self.accept()

    def on_moorings_button(self):
        """ Moorings button behaviour."""
        MooringsConfigurationDialog(parent=None)
        self.accept()

    def on_flex_struct_button(self):
        """Flex Structure dialog open"""
        try:
            selection = FreeCADGui.Selection.getSelection()[0]
        except IndexError:
            error_dialog(__("You must select an object"))
            return

        # Check if object is in the simulation
        if not Case.the().is_object_in_simulation(selection.Name):
            error_dialog(__("The selected object must be added to the simulation"))
            return

        # Check if it is fluid and warn the user.
        if Case.the().get_simulation_object(selection.Name).type == ObjectType.FLUID:
            error_dialog(__("You cannot apply flexible structure to a fluid.\nPlease select a boundary and try again"))
            return

        # Get selection mk
        selection_obj = Case.the().get_simulation_object(selection.Name)
        selection_mk: int = selection_obj.obj_mk
        mk_properties = Case.the().get_mk_based_properties(selection_obj.real_mk())
        flex_struct_dialog = FlexStructDialog(mkbound=selection_mk, dataobj=mk_properties.flex_struct,parent=None)
        result = flex_struct_dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            mk_properties.flex_struct=flex_struct_dialog.dataobj
        self.accept()

    def on_gauges_option(self):
        m_gauge_dialog=GaugesListDialog(parent=None)
        result=m_gauge_dialog.exec_()
        self.accept()

    def on_vres_button(self):
        vres_dialog = VariableResConfigDialog(parent=None)
        result = vres_dialog.exec_()
        self.accept()

    def on_outparts_button(self):
        outparts_dialog = OutpartsDialog(parent=None)
        result = outparts_dialog.exec_()
        self.accept()

