#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Initializes a complete interface with DualSPHysics suite related operations.

It allows an user to create DualSPHysics compatible cases, automating a bunch of things needed to use them.

More info in http://design.sphysics.org/
"""

import time
import threading

import FreeCAD
import FreeCADGui

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.freecad_tools import check_compatibility, document_count, prompt_close_all_documents, get_fc_main_window, get_fc_object
from mod.freecad_tools import delete_existing_docks, valid_document_environment, enforce_case_limits_restrictions, enforce_fillbox_restrictions
from mod.stdout_tools import print_license, log, debug

from mod.constants import APP_NAME, VERSION, DEFAULT_WORKBENCH, DIVIDER

from mod.dataobjects.case import Case

from mod.widgets.dock.designsphysics_dock import DesignSPHysicsDock
from mod.widgets.properties_dock_widget import PropertiesDockWidget

__author__ = "Andrés Vieira"
__copyright__ = "Copyright 2016-2019, DualSHPysics Team"
__credits__ = ["Andrés Vieira", "Lorena Docasar", "Alejandro Jacobo Cabrera Crespo", "Orlando García Feal"]
__license__ = "GPL"
__version__ = VERSION
__maintainer__ = "Andrés Vieira"
__email__ = "avieira@uvigo.es"
__status__ = "Development"


print_license()
check_compatibility()

if document_count() > 0:
    success = prompt_close_all_documents()
    if not success:
        debug("User chose not to close the currently opened documents. Aborting startup")
        quit()

# Tries to delete docks created by a previous execution of DesignSPHysics
delete_existing_docks()

dualsphysics_dock = DesignSPHysicsDock(get_fc_main_window())
properties_widget = PropertiesDockWidget(parent=get_fc_main_window())

get_fc_main_window().addDockWidget(QtCore.Qt.RightDockWidgetArea, dualsphysics_dock)
get_fc_main_window().addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)


def on_tree_item_selection_change():
    """ Refreshes relevant parts of DesignsPHysics under an important change event. """
    debug("Syncronizing FreeCAD data structures with DesignSPHysics")
    selection = FreeCADGui.Selection.getSelection()
    properties_widget.set_add_button_enabled(True)

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
                properties_widget.adapt_to_simulation_object(Case.the().get_simulation_object(selection[0].Name), selection[0])
            else:
                if not selection[0].InList:
                    # Show button to add to simulation
                    properties_widget.configure_to_add_single_selection()
                else:
                    properties_widget.configure_to_incompatible_object()
    else:
        properties_widget.configure_to_no_selection()

    # Delete invalid or already deleted (in FreeCAD) objects
    for object_name in Case.the().get_all_simulation_object_names():
        fc_object = get_fc_object(object_name)
        if not fc_object or fc_object.InList:
            Case.the().remove_object(object_name)

    for damping_to_delete in list(filter(lambda x: not get_fc_object(x), Case.the().damping_zones)):
        Case.the().remove_damping_zone(damping_to_delete)

    # Update dsph objects list
    dualsphysics_dock.refresh_object_list()
    properties_widget.fit_size()


# Subscribe the FreeCAD Objects tree to the item selection change function.
# This helps FreeCAD notify DesignSPHysics for the deleted and changed objects to get updated correctly.
fc_object_tree: QtGui.QTreeWidget = None
for item in get_fc_main_window().findChildren(QtGui.QTreeWidget):
    if "attr" in item.headerItem().text(0).lower():
        fc_object_tree = item

fc_object_tree.itemSelectionChanged.connect(on_tree_item_selection_change)
debug("Subscribing selection change monitor handler to freecad object tree item changed.")

properties_widget.need_refresh.connect(on_tree_item_selection_change)
dualsphysics_dock.need_refresh.connect(on_tree_item_selection_change)


def selection_monitor():
    """ Watches and fixes unwanted changes in the current selection. """
    time.sleep(2.0)
    while True:
        try:
            if not valid_document_environment():
                log("Invalid document environment found. Disabling case-related tools.")
                dualsphysics_dock.adapt_to_no_case()
                time.sleep(1.0)
                continue

            if not FreeCADGui.Selection.getSelection():
                properties_widget.configure_to_no_selection()

            enforce_case_limits_restrictions(Case.the().mode3d)
            enforce_fillbox_restrictions()

            # Adjust damping properties when freecad related properties change
            for name, damping_zone in Case.the().damping_zones.items():
                if FreeCAD.ActiveDocument:
                    damping_group = FreeCAD.ActiveDocument.getObject(name)
                    if len(damping_group.OutList) == 2:
                        damping_zone.overlimit = damping_group.OutList[1].Length.Value / DIVIDER

            time.sleep(0.5)
        except AttributeError:
            time.sleep(1.0)


# Launch a monitor thread that ensures some things are not changed.
monitor_thread = threading.Thread(target=selection_monitor)
monitor_thread.start()

FreeCADGui.activateWorkbench(DEFAULT_WORKBENCH)
log(__("Initialization finished for {} v{}").format(APP_NAME, VERSION))
