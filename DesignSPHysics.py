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
from mod.freecad_tools import get_fc_view_object, is_compatible_version, document_count, prompt_close_all_documents
from mod.stdout_tools import print_license, error, log
from mod.gui_tools import widget_state_config
from mod.dialog_tools import error_dialog, warning_dialog

from mod.enums import ObjectType, ObjectFillMode, FreeCADDisplayMode, FreeCADObjectType
from mod.constants import WIDTH_2D, VERSION, CASE_LIMITS_OBJ_NAME, MAIN_WIDGET_INTERNAL_NAME, PROP_WIDGET_INTERNAL_NAME, DEFAULT_WORKBENCH

from mod.dataobjects.case import Case

from mod.widgets.designsphysics_dock import DesignSPHysicsDock
from mod.widgets.object_order_widget import ObjectOrderWidget
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

# Print license at macro start
try:
    print_license()
except EnvironmentError:
    warning_dialog(__("LICENSE file could not be found. Are you sure you didn't delete it?"))

# Version check. This script is only compatible with FreeCAD 0.17 or higher
is_compatible = is_compatible_version()
if not is_compatible:
    error_dialog(__("This FreeCAD version is not compatible. Please update FreeCAD to version 0.17 or higher."))
    raise EnvironmentError(__("This FreeCAD version is not compatible. Please update FreeCAD to version 0.17 or higher."))

# Used to store widgets that will be disabled/enabled, so they are centralized
widget_state_elements = dict()

# Establishing references for the different elements that the script will use later.
fc_main_window = FreeCADGui.getMainWindow()  # FreeCAD main window

# Resets data structure to default values
Case.instance().reset()

# The script needs only one document open, called DSPH_Case.
# This section tries to close all the current documents.
if document_count() > 0:
    success = prompt_close_all_documents()
    if not success:
        quit()

# If the script is executed even when a previous DSPH Dock is created it makes sure that it's deleted before.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, MAIN_WIDGET_INTERNAL_NAME)
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

dsph_main_dock = DesignSPHysicsDock()  # DSPH main dock

# And docking it at right side of screen
fc_main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dsph_main_dock)

# DSPH OBJECT PROPERTIES DOCK RELATED CODE
# This is the dock widget that by default appears at the bottom-right corner.
# ----------------------------
# Tries to find and close previous instances of the widget.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, PROP_WIDGET_INTERNAL_NAME)
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

# Creation of the widget and scaffolding
properties_widget = PropertiesDockWidget()

# Dock the widget to the left side of screen
fc_main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)


# Find treewidgets of freecad.
trees = list()
for item in fc_main_window.findChildren(QtGui.QTreeWidget):
    if item.objectName() != "DSPH Objects":
        trees.append(item)


def on_up_objectorder(index):
    ''' Defines behaviour on pressing the button to order an DSPH object up in the hirearchy. '''

    new_order = list()

    # order up
    curr_elem = data['export_order'][index]
    prev_elem = data['export_order'][index - 1]

    data['export_order'].remove(curr_elem)

    for element in data['export_order']:
        if element == prev_elem:
            new_order.append(curr_elem)
        new_order.append(element)

    data['export_order'] = new_order

    on_tree_item_selection_change()


def on_down_objectorder(index):
    ''' Defines behaviour on pressing the button to order an DSPH object up in the hirearchy. '''

    new_order = list()

    # order down
    curr_elem = data['export_order'][index]
    next_elem = data['export_order'][index + 1]

    data['export_order'].remove(curr_elem)

    for element in data['export_order']:
        new_order.append(element)
        if element == next_elem:
            new_order.append(curr_elem)

    data['export_order'] = new_order

    on_tree_item_selection_change()


def on_tree_item_selection_change():
    ''' Refreshes relevant parts of DesignsPHysics under an important change event. '''

    selection = FreeCADGui.Selection.getSelection()
    object_names = list()
    for each in FreeCAD.ActiveDocument.Objects:
        object_names.append(each.Name)

    # Detect object deletion
    for sim_object_name in Case.instance().get_all_simulation_object_names():
        if sim_object_name not in object_names:
            Case.instance().remove_object(sim_object_name)

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

    # Update dsph objects list
    dsph_main_dock.dock_object_list_table_widget.clear_table_contents()
    dsph_main_dock.dock_object_list_table_widget.set_table_enabled(True)

    dsph_main_dock.dock_object_list_table_widget.set_table_row_count(Case.instance().number_of_objects_in_simulation())
    current_row = 0
    objects_with_parent = list()
    for object_name in Case.instance().get_all_simulation_object_names():
        context_object = FreeCAD.ActiveDocument.getObject(object_name)
        if not context_object:
            Case.instance().remove_object(object_name)
            continue
        if context_object.InList != list():
            objects_with_parent.append(context_object.Name)
            continue
        if context_object.Name == "Case_Limits":
            continue
        target_widget = ObjectOrderWidget(
            index=current_row,
            object_mk=Case.instance().get_simulation_object(context_object.Name).obj_mk,
            mktype=Case.instance().get_simulation_object(context_object.Name).type,
            object_name=context_object.Label
        )

        target_widget.up.connect(on_up_objectorder)
        target_widget.down.connect(on_down_objectorder)

        if current_row is 0:
            target_widget.disable_up()
        if current_row is Case.instance().number_of_objects_in_simulation() - 1:
            target_widget.disable_down()

        dsph_main_dock.dock_object_list_table_widget.set_table_cell_widget(current_row, 0, target_widget)

        current_row += 1
    for object_name in objects_with_parent:
        try:
            Case.instance().remove_object(object_name)
        except ValueError:
            # Not in list, probably because now is part of a compound object
            pass
    properties_widget.fit_size()


# Subscribe the trees to the item selection change function. This helps FreeCAD notify DesignSPHysics for the
# deleted and changed objects to get updated correctly.
for item in trees:
    item.itemSelectionChanged.connect(on_tree_item_selection_change)

properties_widget.need_refresh.connect(on_tree_item_selection_change)

# Watch if no object is selected and prevent fillbox rotations


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
