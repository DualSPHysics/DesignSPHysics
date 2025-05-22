#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Initializes a complete interface with DualSPHysics suite related operations.

It allows an user to create DualSPHysics compatible cases, automating a bunch of things needed to use them.

More info in http://design.sphysics.org/
"""
from urllib.error import URLError
from urllib.request import urlopen

import FreeCADGui

from PySide2 import QtCore, QtWidgets

from mod.constants import APP_NAME, VERSION, REVISION, DEFAULT_WORKBENCH, GITHUB_MASTER_CONSTANTS_URL, \
    DAMPING_GROUP_NAME, SIMULATION_DOMAIN_NAME

from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings

from mod.tools.dialog_tools import info_dialog, warning_dialog
from mod.tools.freecad_tools import check_compatibility, document_count, prompt_close_all_documents, get_fc_main_window, \
    get_fc_object
from mod.tools.freecad_tools import delete_existing_docks
from mod.tools.main_loop_tools import  MainLoopManager, MainLoopEmiter, UnitWatcher
from mod.tools.stdout_tools import print_license, log, debug
from mod.tools.translation_tools import __
from mod.widgets.designsphysics_dock import DesignSPHysicsDock
from mod.widgets.properties_dock_widget import PropertiesDockWidget

__author__ = "Iván Martínez Estévez, Andrés Vieira"
__copyright__ = "Copyright 2016-2023, DualSHPysics Team"
__credits__ = ["Iván Martínez Estévez", "Andrés Vieira", "Irene Fernandez Mariño", "Lorena Docasar", "Alejandro Jacobo Cabrera Crespo",
               "Orlando García Feal"]
__license__ = "GPL"
__version__ = VERSION
__maintainer__ = "Iván Martínez Estévez"
__email__ = "ivan.martinez.estevez@uvigo.es"
__status__ = "Development"

def on_tree_item_selection_change(properties_widget, designsphysics_dock):
    """ Refreshes relevant parts of DesignsPHysics under an important change event. """
    log("Synchronizing FreeCAD data structures with DesignSPHysics")
    selection = FreeCADGui.Selection.getSelection()
    properties_widget.set_add_button_enabled(True)

    if selection:
        if len(selection) > 1:
            # Multiple objects selected
            properties_widget.configure_to_add_multiple_selection()
        else:
            # One object selected
            #NO ADDABLE NOR CONFIGURABLE OBJECTS: (CaseLimits,SimulationDomain, HelperObjects, Groups except DampingZones and FillBoxes, FillBox members, Spreadsheets
            if selection[0].Name == "Case_Limits" or "_internal_" in selection[0].Name or "Helper" in selection[0].Name or \
                    selection[0].TypeId == 'Spreadsheet::Sheet' or (selection[0].TypeId == 'App::DocumentObjectGroup' and not "FillBox" in selection[0].Name  and not "Damping" in selection[0].Name)\
                    or "FillLimit" in selection[0].Name or "FillPoint" in selection[0].Name or SIMULATION_DOMAIN_NAME in selection[0].Name:
                properties_widget.configure_to_no_selection()
            elif "Damping" in selection[0].Name:    #DAMPING ZONES
                if Case.the().is_damping_bound_to_object(selection[0].Name):
                    properties_widget.configure_to_damping_selection()
                else:
                    if selection[0].Name==DAMPING_GROUP_NAME: #DAMPING HELPER GROUP
                        properties_widget.configure_to_no_selection()
            elif Case.the().is_object_in_simulation(selection[0].Name): #ALREADY IN SIMULATION OBJECTS
                # Show properties on table
                properties_widget.configure_to_regular_selection()
                properties_widget.adapt_to_simulation_object(Case.the().get_simulation_object(selection[0].Name),
                                                             selection[0])
            else:   #OBJECTS CHOSABLE TO BE ADDED TO THE SIMULATION
                #if not selection[0].InList: NOT ACEPTING LINKED OBJECTS , WHY?, DISABLED
                    # Show button to add to simulation
                properties_widget.configure_to_add_single_selection()
                #else:
                #    properties_widget.configure_to_incompatible_object()
    else:   #NO SELECTION
        properties_widget.configure_to_no_selection()
    names_list = Case.the().get_all_simulation_object_names()
    for object_name in names_list:
        fc_object = get_fc_object(object_name)
        if not fc_object: #or fc_object.InList:
            Case.the().remove_object(object_name)
    designsphysics_dock.refresh_object_list()

def on_unit_change():
    boot()

def boot():
    """ Boots the application. """
    print_license()
    check_compatibility()

    try:
        master_branch_version = str(urlopen(GITHUB_MASTER_CONSTANTS_URL).read()).split("VERSION = \"")[-1].split("\"")[
            0]
        if VERSION < master_branch_version and ApplicationSettings.the().notify_on_outdated_version_enabled:
            info_dialog(
                __("Your version of DesignSPHyiscs is outdated. Please go to the Addon Manager and update it. New versions include bug fixes, new features and new DualSPHysics executables, among other things."),
                __("The version you're using is {} while the version that you can update to is {}").format(VERSION,
                                                                                                           master_branch_version)
            )
    except URLError:
        log("No network connection or Git repo is down. Skipping version check.")

    if document_count() > 0:
        success = prompt_close_all_documents()
        if not success:
            warning_dialog("User chose not to close the currently opened documents. Aborting startup")
            quit()

    # Tries to delete docks created by a previous execution of DesignSPHysics
    delete_existing_docks()

    designsphysics_dock = DesignSPHysicsDock(get_fc_main_window())
    properties_widget = PropertiesDockWidget(parent=get_fc_main_window())

    get_fc_main_window().addDockWidget(QtCore.Qt.RightDockWidgetArea, designsphysics_dock)
    get_fc_main_window().addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)

    for child in get_fc_main_window().findChildren(QtWidgets.QSplitter):
        widget = child.findChildren(QtWidgets.QTreeWidget)
        if widget:
            fc_object_tree: QtWidgets.QTreeWidget = widget[0]
            break
    fc_object_tree.itemSelectionChanged.connect(lambda p=properties_widget, d=designsphysics_dock: on_tree_item_selection_change(p, d))

    selection_view = get_fc_main_window().findChild(QtWidgets.QDockWidget,"Selection view")

    log("Subscribing selection change monitor handler to freecad object tree item changed.")

    properties_widget.need_refresh.connect(
        lambda p=properties_widget, d=designsphysics_dock: on_tree_item_selection_change(p, d))
    designsphysics_dock.need_refresh.connect(
        lambda p=properties_widget, d=designsphysics_dock: on_tree_item_selection_change(p, d))

    # Launch a monitor thread that ensures some things are not changed.
    manager = MainLoopManager(designsphysics_dock,properties_widget)
    emitter: MainLoopEmiter = MainLoopEmiter()
    # watcher: UnitWatcher = UnitWatcher()

    emitter.check_deleted.connect(manager.deleted)
    emitter.check_selection.connect(manager.slot_selection)

    # watcher.unit_changed.connect(on_unit_change)
    
    emitter.start()
    # watcher.start()

    FreeCADGui.activateWorkbench(DEFAULT_WORKBENCH)
    if "DsphWorkbench" in FreeCADGui.listWorkbenches().keys():
        FreeCADGui.activateWorkbench("DsphWorkbench")
    elif "DsphWorkbench" in FreeCADGui.listWorkbenches().keys():
        FreeCADGui.activateWorkbench("Part")
    log(__("Initialization finished for {} v{}.{}").format(APP_NAME, VERSION, REVISION))
    Case.manager = manager