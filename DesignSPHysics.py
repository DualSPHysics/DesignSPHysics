#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''
Initializes a complete interface with DualSPHysics suite related operations.

It allows an user to create DualSPHysics compatible cases, automating a bunch of things needed to use them.

More info in http://design.sphysics.org/
'''

import time
import threading

import FreeCAD
import FreeCADGui

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.freecad_tools import get_fc_view_object, check_compatibility, document_count, prompt_close_all_documents, get_fc_main_window
from mod.freecad_tools import delete_existing_docks
from mod.stdout_tools import print_license, error, log
from mod.gui_tools import widget_state_config

from mod.enums import ObjectType, ObjectFillMode, FreeCADDisplayMode, FreeCADObjectType
from mod.constants import WIDTH_2D, VERSION, CASE_LIMITS_OBJ_NAME, DEFAULT_WORKBENCH

from mod.dataobjects.case import Case

from mod.widgets.designsphysics_dock import DesignSPHysicsDock
from mod.widgets.properties_dock_widget import PropertiesDockWidget


data = {}  # TODO: Delete this

__author__ = "Andrés Vieira"
__copyright__ = "Copyright 2016-2019, DualSHPysics Team"
__credits__ = ["Andrés Vieira", "Lorena Docasar", "Alejandro Jacobo Cabrera Crespo", "Orlando García Feal"]
__license__ = "GPL"
__version__ = VERSION
__maintainer__ = "Andrés Vieira"
__email__ = "avieira@uvigo.es"
__status__ = "Development"

# Used to store widgets that will be disabled/enabled, so they are centralized
# FIXME: This should not be managed this way
widget_state_elements = dict()

print_license()
check_compatibility()

if document_count() > 0:
    success = prompt_close_all_documents()
    if not success:
        quit()

# Tries to delete docks created by a previous execution of DesignSPHysics
delete_existing_docks()

Case.instance().reset()

dsph_main_dock = DesignSPHysicsDock()
properties_widget = PropertiesDockWidget()

get_fc_main_window().addDockWidget(QtCore.Qt.RightDockWidgetArea, dsph_main_dock)
get_fc_main_window().addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)


# Find treewidgets of freecad.
trees = list()
for item in get_fc_main_window().findChildren(QtGui.QTreeWidget):
    if item.objectName() != "DSPH Objects":
        trees.append(item)


def on_tree_item_selection_change():
    ''' Refreshes relevant parts of DesignsPHysics under an important change event. '''

    selection = FreeCADGui.Selection.getSelection()
    object_names = list()
    for each in FreeCAD.ActiveDocument.Objects:
        object_names.append(each.Name)

    properties_widget.set_add_button_enabled(True)

    if selection:
        if len(selection) > 1:
            # Multiple objects selected
            properties_widget.set_add_button_text(__("Add all possible objects to DSPH Simulation"))
            properties_widget.set_property_table_visibility(False)
            properties_widget.set_add_button_visibility(True)
            properties_widget.set_remove_button_visibility(False)
            properties_widget.set_damping_button_visibility(False)
        else:
            # One object selected
            if selection[0].Name == "Case_Limits" or "_internal_" in selection[0].Name:
                properties_widget.set_property_table_visibility(False)
                properties_widget.set_add_button_visibility(False)
                properties_widget.set_remove_button_visibility(False)
                properties_widget.set_damping_button_visibility(False)
            elif "dampingzone" in selection[0].Name.lower() and selection[0].Name in data['damping'].keys():
                properties_widget.set_property_table_visibility(False)
                properties_widget.set_add_button_visibility(False)
                properties_widget.set_remove_button_visibility(False)
                properties_widget.set_damping_button_visibility(True)
            elif Case.instance().is_object_in_simulation(selection[0].Name):
                # Show properties on table
                properties_widget.set_property_table_visibility(True)
                properties_widget.set_add_button_visibility(False)
                properties_widget.set_remove_button_visibility(True)
                properties_widget.set_damping_button_visibility(False)

                # Reference to the object inside the simulation
                sim_object = Case.instance().get_simulation_object(selection[0].Name)

                # MK config
                properties_widget.set_mkgroup_range(ObjectType.BOUND)
                to_change = properties_widget.get_cell_widget(1, 1)
                to_change.setValue(sim_object.obj_mk)

                # type config
                to_change = properties_widget.get_cell_widget(0, 1)
                if selection[0].TypeId in Case.SUPPORTED_TYPES:
                    # Supported object
                    to_change.setEnabled(True)
                    if sim_object.type is ObjectType.FLUID:
                        to_change.setCurrentIndex(0)
                        properties_widget.set_mkgroup_range(ObjectType.FLUID)
                        properties_widget.set_mkgroup_text("&nbsp;&nbsp;&nbsp;" + __("MKFluid") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>")
                    elif sim_object.type is ObjectType.BOUND:
                        to_change.setCurrentIndex(1)
                        properties_widget.set_mkgroup_range(ObjectType.BOUND)
                        properties_widget.set_mkgroup_text("&nbsp;&nbsp;&nbsp;" + __("MKBound") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>")
                elif "part" in selection[0].TypeId.lower() or "mesh" in selection[0].TypeId.lower() or (
                        selection[0].TypeId == FreeCADObjectType.FOLDER and "fillbox" in selection[0].Name.lower()):
                    # Is an object that will be exported to STL
                    to_change.setEnabled(True)
                    if sim_object.type is ObjectType.FLUID:
                        to_change.setCurrentIndex(0)
                        properties_widget.set_mkgroup_range(ObjectType.FLUID)
                        properties_widget.set_mkgroup_text("&nbsp;&nbsp;&nbsp;" + __("MKFluid") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>")
                    elif sim_object.type is ObjectType.BOUND:
                        to_change.setCurrentIndex(1)
                        properties_widget.set_mkgroup_range(ObjectType.BOUND)
                        properties_widget.set_mkgroup_text("&nbsp;&nbsp;&nbsp;" + __("MKBound") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>")
                else:
                    # Everything else
                    to_change.setCurrentIndex(1)
                    to_change.setEnabled(False)

                # fill mode config
                to_change = properties_widget.get_cell_widget(2, 1)
                if selection[0].TypeId in Case.SUPPORTED_TYPES:
                    # Object is a supported type. Fill with its type and enable selector.
                    to_change.setEnabled(True)
                    if sim_object.fillmode is ObjectFillMode.FULL:
                        to_change.setCurrentIndex(0)
                    elif sim_object.fillmode is ObjectFillMode.SOLID:
                        to_change.setCurrentIndex(1)
                    elif sim_object.fillmode is ObjectFillMode.FACE:
                        to_change.setCurrentIndex(2)
                    elif sim_object.fillmode is ObjectFillMode.WIRE:
                        to_change.setCurrentIndex(3)
                elif selection[0].TypeId == 'App::DocumentObjectGroup':
                    # Is a fillbox. Set fill mode to solid and disable
                    to_change.setCurrentIndex(1)
                    to_change.setEnabled(False)
                else:
                    # Not supported. Probably face
                    to_change.setCurrentIndex(2)
                    to_change.setEnabled(False)

                # float state config
                to_change = properties_widget.get_cell_widget(3, 1)
                if selection[0].TypeId in Case.SUPPORTED_TYPES or (selection[0].TypeId == FreeCADObjectType.FOLDER
                                                                   and "fillbox" in selection[0].Name.lower()):
                    if sim_object.type is ObjectType.FLUID:
                        to_change.setEnabled(False)
                    else:
                        to_change.setEnabled(True)

                # initials restrictions
                to_change = properties_widget.get_cell_widget(4, 1)
                if sim_object.type is ObjectType.FLUID:
                    to_change.setEnabled(True)
                else:
                    to_change.setEnabled(False)

                # motion restrictions
                to_change = properties_widget.get_cell_widget(5, 1)
                if selection[0].TypeId in Case.SUPPORTED_TYPES or FreeCADObjectType.CUSTOM_MESH in str(selection[0].TypeId) or \
                        (selection[0].TypeId == FreeCADObjectType.FOLDER and "fillbox" in selection[0].Name.lower()):
                    if sim_object.type is ObjectType.FLUID:
                        to_change.setEnabled(False)
                    else:
                        to_change.setEnabled(True)

            else:
                if selection[0].InList == list():
                    # Show button to add to simulation
                    properties_widget.set_add_button_text(__("Add to DSPH Simulation"))
                    properties_widget.set_property_table_visibility(False)
                    properties_widget.set_add_button_visibility(True)
                    properties_widget.set_remove_button_visibility(False)
                    properties_widget.set_damping_button_visibility(False)
                else:
                    properties_widget.set_add_button_text(__("Can't add this object to the simulation"))
                    properties_widget.set_property_table_visibility(False)
                    properties_widget.set_add_button_visibility(True)
                    properties_widget.set_add_button_enabled(False)
                    properties_widget.set_remove_button_visibility(False)
                    properties_widget.set_damping_button_visibility(False)
    else:
        properties_widget.set_property_table_visibility(False)
        properties_widget.set_add_button_visibility(False)
        properties_widget.set_remove_button_visibility(False)
        properties_widget.set_damping_button_visibility(False)

    # Delete invalid or already deleted (in FreeCAD) objects
    Case.instance().delete_invalid_objects()

    # Update dsph objects list
    dsph_main_dock.refresh_object_list()
    properties_widget.fit_size()


# Subscribe the trees to the item selection change function. This helps FreeCAD notify DesignSPHysics for the
# deleted and changed objects to get updated correctly.
for item in trees:
    item.itemSelectionChanged.connect(on_tree_item_selection_change)

properties_widget.need_refresh.connect(on_tree_item_selection_change)


def selection_monitor():
    ''' Watches and fixes unwanted changes in the current selection. '''
    time.sleep(2.0)
    while True:
        # ensure everything is fine when objects are not selected
        try:
            if not FreeCADGui.Selection.getSelection():
                properties_widget.set_property_table_visibility(False)
                properties_widget.set_add_button_visibility(False)
                properties_widget.set_remove_button_visibility(False)
                properties_widget.set_damping_button_visibility(False)
        except AttributeError:
            # No object is selected so the selection has no length. Ignore it
            pass
        try:
            # watch fillbox rotations and prevent them
            for o in FreeCAD.ActiveDocument.Objects:
                if o.TypeId == FreeCADObjectType.FOLDER and "fillbox" in o.Name.lower():
                    for subelem in o.OutList:
                        if subelem.Placement.Rotation.Angle != 0.0:
                            subelem.Placement.Rotation.Angle = 0.0
                            error(__("Can't change rotation!"))
                if o.Name == CASE_LIMITS_OBJ_NAME:
                    if o.Placement.Rotation.Angle != 0.0:
                        o.Placement.Rotation.Angle = 0.0
                        error(__("Can't change rotation!"))
                    if not Case.instance().mode3d and o.Width.Value != WIDTH_2D:
                        o.Width.Value = WIDTH_2D
                        error(__("Can't change width if the case is in 2D Mode!"))

            # Prevent some view properties of Case Limits to be changed
            case_limits_obj = get_fc_view_object(CASE_LIMITS_OBJ_NAME)
            if case_limits_obj is not None:
                if case_limits_obj.DisplayMode != FreeCADDisplayMode.WIREFRAME:
                    case_limits_obj.DisplayMode = FreeCADDisplayMode.WIREFRAME
                if case_limits_obj.LineColor != (1.00, 0.00, 0.00):
                    case_limits_obj.LineColor = (1.00, 0.00, 0.00)
                if case_limits_obj.Selectable:
                    case_limits_obj.Selectable = False

            for sim_object in Case.instance().get_all_objects_with_damping():
                damping_group = FreeCAD.ActiveDocument.getObject(sim_object)
                sim_object.damping.overlimit = damping_group.OutList[1].Length.Value

        except (NameError, AttributeError):
            # DSPH Case not opened, disable things
            widget_state_config(widget_state_elements, "no case")
            time.sleep(2.0)
            continue
        time.sleep(0.5)


# Launch a monitor thread that ensures some things are not changed.
monitor_thread = threading.Thread(target=selection_monitor)
monitor_thread.start()

FreeCADGui.activateWorkbench(DEFAULT_WORKBENCH)
log(__("Loading data is done."))
