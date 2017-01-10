#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DesignSPHysics.

This is the main script (or Macro) meant to be used
with FreeCAD. Initializes a complete interface with
DualSPHysics suite related operations.

It allows an user to create DualSPHysics compatible
cases, automating a bunch of things needed to use
them.

"""

import FreeCAD
import FreeCADGui
import glob
import os
import sys
import time
import pickle
import threading
from PySide import QtGui, QtCore
from dsphfc.properties import FloatProperty, InitialsProperty

sys.path.append(FreeCAD.getUserAppDataDir() + "Macro/")
from dsphfc import utils, guiutils, xmlimporter
from dsphfc.utils import __

# Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
#
# This file is part of DesignSPHysics.
#
# DesignSPHysics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DesignSPHysics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Andrés Vieira"
__copyright__ = "Copyright 2016, DualSHPysics Team"
__credits__ = ["Andrés Vieira", "Alejandro Jacobo Cabrera Crespo", "Orlando García Feal"]
__license__ = "GPL"
__version__ = "v0.1 BETA-10J17"
__maintainer__ = "Andrés Vieira"
__email__ = "anvieiravazquez@gmail.com"
__status__ = "Development"

# General To-Do to use with PyCharm
# TODO: High priority - Try to pack all in one executable for installing
# TODO: High priority - Delete settings file if cannot be loaded
# TODO: High priority - Simulation buttons not triggering on when saving


# TODO: 0.2Beta - Make DSPH Object Properties bigger by default
# TODO: 0.2Beta - Toolbox (Fillbox, wave, periodicity, imports...) to clean the UI
# TODO: 0.2Beta - Wave generator
# - Show plane to represent wave generator
# TODO: 0.2Beta - Periodicity support
# - Show arrows (bounds) to show periodicity
# TODO: 0.2Beta - Create Material support
# TODO: 0.2Beta - Material creator and assigner
# TODO: 0.2Beta - Object Motion
# TODO: 0.2Beta - Refactor all code
# TODO: 0.2Beta - Documentation of the code
# End general To-Do

# Print license at macro start
try:
    utils.print_license()
except EnvironmentError:
    guiutils.warning_dialog(__("LICENSE file could not be found. Are you sure you didn't delete it?"))

# Version check. This script is only compatible with FreeCAD 0.16 or higher
is_compatible = utils.is_compatible_version()
if not is_compatible:
    guiutils.error_dialog(__("This FreeCAD version is not compatible. "
                             "Please update FreeCAD to version 0.16 or higher."))
    raise EnvironmentError(__("This FreeCAD version is not compatible. "
                              "Please update FreeCAD to version 0.16 or higher."))

# Main data structure
data = dict()  # Used to save on disk case parameters and related data
temp_data = dict()  # Used to store temporal useful items (like processes)
widget_state_elements = dict()  # Used to store widgets that will be disabled/enabled, so they are centralized
# Establishing references for the different elements that
# the script will use later.
fc_main_window = FreeCADGui.getMainWindow()  # FreeCAD main window
dsph_main_dock = QtGui.QDockWidget()  # DSPH main dock
dsph_main_dock_scaff_widget = QtGui.QWidget()  # Scaffolding widget, only useful to apply to the dsph_dock widget
# Executes the default data function the first time
# and merges results with current data structure.
default_data, default_temp_data = utils.get_default_data()
data.update(default_data)
temp_data.update(default_temp_data)

# The script needs only one document open, called DSPH_Case.
# This section tries to close all the current documents.
if utils.document_count() > 0:
    success = utils.prompt_close_all_documents()
    if not success:
        quit()

# If the script is executed even when a previous DSPH Dock is created
# it makes sure that it's deleted before.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, __("DSPH Widget"))
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

# Creation of the DSPH Widget.
# Creates a widget with a series of layouts added, to apply
# to the DSPH dock at the end.
dsph_main_dock.setObjectName("DSPH Widget")
dsph_main_dock.setWindowTitle(utils.APP_NAME + " " + str(__version__))
main_layout = QtGui.QVBoxLayout()  # Main Widget layout.  Vertical ordering

# Component layouts definition
logo_layout = QtGui.QHBoxLayout()
logo_layout.setSpacing(0)
logo_layout.setContentsMargins(0, 0, 0, 20)
intro_layout = QtGui.QVBoxLayout()

# DSPH dock first section.
# Includes constant definition, help, etc.
constants_label = QtGui.QLabel(
    "<b>" + __("Configuration") + "</b>")
constants_label.setWordWrap(True)
constants_button = QtGui.QPushButton(__("Define\nConstants"))
constants_button.setToolTip(
    __("Use this button to define case constants,\nsuch as lattice, gravity or fluid reference density."))
constants_button.clicked.connect(lambda: guiutils.def_constants_window(data))
widget_state_elements['constants_button'] = constants_button
help_button = QtGui.QPushButton("Help: DesignSPHysics Wiki")
help_button.setToolTip(__("Push this button to open a browser with help\non how to use this tool."))
help_button.clicked.connect(utils.open_help)
setup_button = QtGui.QPushButton(__("Setup\nPlugin"))
setup_button.setToolTip(__("Setup of the simulator executables"))
setup_button.clicked.connect(lambda: guiutils.def_setup_window(data))
execparams_button = QtGui.QPushButton(__("Execution\nParameters"))
execparams_button.setToolTip(__("Change execution parameters, such as\ntime of simulation, viscosity, etc."))
execparams_button.clicked.connect(lambda: guiutils.def_execparams_window(data))
widget_state_elements['execparams_button'] = execparams_button
constants_separator = QtGui.QFrame()
constants_separator.setFrameStyle(QtGui.QFrame.HLine)
crucialvars_separator = QtGui.QFrame()
crucialvars_separator.setFrameStyle(QtGui.QFrame.HLine)
logo_label = QtGui.QLabel()
logo_label.setPixmap(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/logo.png")


def on_dp_changed():
    """ DP Introduction.
    Changes the dp at the moment the user changes the text. """
    data['dp'] = float(dp_input.text())


dp_layout = QtGui.QHBoxLayout()
dp_label = QtGui.QLabel(__("Inter-particle distance: "))
dp_label.setToolTip(__(
    "Lower DP to have more particles in the case."
    "\nIncrease it to ease times of simulation."
    "\nNote that more DP implies more quality in the final result."))
dp_input = QtGui.QLineEdit()
dp_input.setToolTip(__(
    "Lower DP to have more particles in the case."
    "\nIncrease it to ease times of simulation."
    "\nNote that more DP implies more quality in the final result."))
dp_label2 = QtGui.QLabel(" meters")
dp_input.setMaxLength(10)
dp_input.setText(str(data['dp']))
dp_input.textChanged.connect(on_dp_changed)
widget_state_elements['dp_input'] = dp_input
dp_validator = QtGui.QDoubleValidator(0.0, 100, 8, dp_input)
dp_input.setValidator(dp_validator)
dp_layout.addWidget(dp_label)
dp_layout.addWidget(dp_input)
dp_layout.addWidget(dp_label2)

# Case control definition.
# Includes things like New Case, Save, etc...
cc_layout = QtGui.QVBoxLayout()
cclabel_layout = QtGui.QHBoxLayout()
ccfilebuttons_layout = QtGui.QHBoxLayout()
ccaddbuttons_layout = QtGui.QHBoxLayout()
casecontrols_label = QtGui.QLabel("<b>" + __("File and GenCase tools") + "<b>")
casecontrols_bt_newdoc = QtGui.QPushButton("  " + __("New\n  Case"))
casecontrols_bt_newdoc.setToolTip(__("Creates a new case. \nThe current documents opened will be closed."))
casecontrols_bt_newdoc.setIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/new.png"))
casecontrols_bt_newdoc.setIconSize(QtCore.QSize(28, 28))
casecontrols_bt_savedoc = QtGui.QPushButton("  " + __("Save\n  Case"))
casecontrols_bt_savedoc.setToolTip(__(
    "Saves the case and executes GenCase over.\nIf GenCase fails or is not set up, only the case\nwill be saved."))
casecontrols_bt_savedoc.setIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/save.png"))
casecontrols_bt_savedoc.setIconSize(QtCore.QSize(28, 28))
widget_state_elements['casecontrols_bt_savedoc'] = casecontrols_bt_savedoc
casecontrols_bt_loaddoc = QtGui.QPushButton("  " + __("Load\n  Case"))
casecontrols_bt_loaddoc.setToolTip(__("Loads a case from disk. All the current documents\nwill be closed."))
casecontrols_bt_loaddoc.setIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/load.png"))
casecontrols_bt_loaddoc.setIconSize(QtCore.QSize(28, 28))
casecontrols_bt_addfillbox = QtGui.QPushButton(__("Add fillbox"))
casecontrols_bt_addfillbox.setToolTip(__(
    "Adds a FillBox. A FillBox is able to fill an empty space\n"
    "within limits of geometry and a maximum bounding\nbox placed by the user."))
casecontrols_bt_addfillbox.setEnabled(False)
widget_state_elements['casecontrols_bt_addfillbox'] = casecontrols_bt_addfillbox
casecontrols_bt_addstl = QtGui.QPushButton("Import STL")
casecontrols_bt_addstl.setToolTip(__(
    "Imports a STL with postprocessing. This way you can set the scale of the imported object."))
casecontrols_bt_addstl.setEnabled(False)
widget_state_elements['casecontrols_bt_addstl'] = casecontrols_bt_addstl
casecontrols_bt_importxml = QtGui.QPushButton(__("Import XML"))
casecontrols_bt_importxml.setToolTip(__("Imports an already created XML case from disk."))
casecontrols_bt_importxml.setEnabled(True)


def on_new_case():
    """ Defines what happens when new case is clicked. Closes all documents
        if possible and creates a FreeCAD document with Case Limits object. """
    if utils.document_count() > 0:
        new_case_success = utils.prompt_close_all_documents()
        if not new_case_success:
            return

    utils.create_dsph_document()
    new_case_default_data, new_case_temp_data = utils.get_default_data()
    data.update(new_case_default_data)
    temp_data.update(new_case_temp_data)
    guiutils.widget_state_config(widget_state_elements, "new case")
    data['simobjects']['Case_Limits'] = ["mkspecial", "typespecial", "fillspecial"]
    on_tree_item_selection_change()


def on_save_case():
    """Defines what happens when save case button is clicked.
    Saves a freecad scene definition, a dump of dsph data useful for this macro
    and tries to generate a case with gencase."""

    # Watch if save path is available.  Prompt the user if not.
    if data['project_path'] == "" and data['project_name'] == "":
        # noinspection PyArgumentList
        save_name, _ = QtGui.QFileDialog.getSaveFileName(dsph_main_dock, __("Save Case"), QtCore.QDir.homePath())
    else:
        save_name = data['project_path']

    if " " in save_name:  # Spawn error if path contains any spaces.
        guiutils.error_dialog(__(
            "The path you selected contains spaces. Due to DualSPHysics restrictions, "
            "you'll need to use a folder path without any spaces. Sorry for the inconvenience"))
        return

    if save_name != '':
        if not os.path.exists(save_name):
            os.makedirs(save_name)
        data['project_path'] = save_name
        data['project_name'] = save_name.split('/')[-1]

        # Watch if folder already exists or create it
        if not os.path.exists(save_name + "/" + save_name.split('/')[-1] + "_Out"):
            os.makedirs(save_name + "/" + save_name.split('/')[-1] + "_Out")

        utils.dump_to_xml(data, save_name)  # Dumps all the case data to an XML file.

        # Generate batch file in disk
        if (data['gencase_path'] == "") or (data['dsphysics_path'] == "") or (data['partvtk4_path'] == ""):
            utils.warning(__("Can't create executable bat file! One or more of the paths in plugin setup is not set"))
        else:
            bat_file = open(save_name + "/run.bat", 'w')
            utils.log(__("Creating ") + save_name + "/run.bat")
            bat_file.write("@echo off\n")
            bat_file.write('echo "------- Autoexported by ' + utils.APP_NAME + ' -------"\n')
            bat_file.write(
                'echo "This script executes GenCase for the case saved, that generates output files in the *_Out dir.'
                ' Then, executes a simulation on CPU of the case. Last, '
                'it exports all the geometry generated in VTK files for viewing with ParaView."\n')
            bat_file.write('pause\n')
            bat_file.write('"' + data['gencase_path'] + '" ' + save_name + "/" + save_name.split('/')[
                -1] + "_Def " + save_name + "/" + save_name.split('/')[-1] + "_Out/" + save_name.split('/')[
                               -1] + ' -save:+all' + '\n')
            bat_file.write('"' + data['dsphysics_path'] + '" ' + save_name + "/" + save_name.split('/')[-1] + "_Out/" +
                           save_name.split('/')[-1] + ' ' + save_name + "/" + save_name.split('/')[
                               -1] + "_Out" + ' -svres -' + str(ex_selector_combo.currentText()).lower() + '\n')
            bat_file.write('"' + data['partvtk4_path'] + '" -dirin ' + save_name + "/" + save_name.split('/')[
                -1] + "_Out -savevtk " + save_name + "/" + save_name.split('/')[-1] + "_Out/PartAll" + '\n')
            bat_file.write(
                'echo "------- Execution complete. If results were not the exepected ones check for errors.'
                ' Make sure your case has a correct DP specification. -------"\n')
            bat_file.write('pause\n')
            bat_file.close()

            bat_file = open(save_name + "/run.sh", 'w')
            utils.log("Creating " + save_name + "/run.sh")
            bat_file.write('echo "------- Autoexported by ' + utils.APP_NAME + ' -------"\n')
            bat_file.write(
                'echo "This script executes GenCase for the case saved, that generates output files in the *_Out dir.'
                ' Then, executes a simulation on CPU of the case. Last,'
                ' it exports all the geometry generated in VTK files for viewing with ParaView."\n')
            bat_file.write('read -rsp $"Press any key to continue..." -n 1 key\n')
            bat_file.write('"' + data['gencase_path'] + '" ' + save_name + "/" + save_name.split('/')[
                -1] + "_Def " + save_name + "/" + save_name.split('/')[-1] + "_Out/" + save_name.split('/')[
                               -1] + ' -save:+all' + '\n')
            bat_file.write('"' + data['dsphysics_path'] + '" ' + save_name + "/" + save_name.split('/')[-1] + "_Out/" +
                           save_name.split('/')[-1] + ' ' + save_name + "/" + save_name.split('/')[
                               -1] + "_Out" + ' -svres -' + str(ex_selector_combo.currentText()).lower() + '\n')
            bat_file.write('"' + data['partvtk4_path'] + '" -dirin ' + save_name + "/" + save_name.split('/')[
                -1] + "_Out -savevtk " + save_name + "/" + save_name.split('/')[-1] + "_Out/PartAll" + '\n')
            bat_file.write(
                'echo "------- Execution complete.'
                ' If results were not the exepected ones check for errors.'
                ' Make sure your case has a correct DP specification. -------"\n')
            bat_file.write('read -rsp $"Press any key to continue..." -n 1 key\n')
            bat_file.close()

        data['gencase_done'] = False
        # Use gencase if possible to generate the case final definition
        if data['gencase_path'] != "":
            os.chdir(data['project_path'])
            process = QtCore.QProcess(fc_main_window)
            process.start(data['gencase_path'], [data['project_path'] + '/' + data['project_name'] + '_Def',
                                                 data['project_path'] + '/' + data['project_name'] + '_Out/' + data[
                                                     'project_name'], '-save:+all'])
            process.waitForFinished()
            output = str(process.readAllStandardOutput())
            error_in_gen_case = False
            if str(process.exitCode()) == "0":
                try:
                    total_particles_text = output[output.index("Total particles: "):output.index(" (bound=")]
                    total_particles = int(total_particles_text[total_particles_text.index(": ") + 2:])
                    data['total_particles'] = total_particles

                    utils.log(__("Total number of particles exported: ") + str(total_particles))
                    if total_particles < 300:
                        utils.warning(__(
                            "Are you sure all the parameters are set right? "
                            "The number of particles is very low ({}). "
                            "Lower the DP to increase number of particles")).format(
                            str(total_particles))
                    elif total_particles > 200000:
                        utils.warning(__(
                            "Number of particles is pretty high ({}) and "
                            "it could take a lot of time to simulate.")).format(
                            str(total_particles))
                    data['gencase_done'] = True
                    guiutils.widget_state_config(widget_state_elements, "gencase done")
                    gencase_infosave_dialog = QtGui.QMessageBox()
                    gencase_infosave_dialog.setText(__("Gencase exported {} particles. "
                                                       "Press View Details to check the output.\n").format(
                        str(total_particles)))
                    gencase_infosave_dialog.setDetailedText(output.split("================================")[1])
                    gencase_infosave_dialog.setIcon(QtGui.QMessageBox.Information)
                    gencase_infosave_dialog.exec_()
                except ValueError:
                    error_in_gen_case = True

            if str(process.exitCode()) != "0" or error_in_gen_case:
                # Multiple causes
                gencase_out_file = open(
                    data['project_path'] + '/' + data['project_name'] + '_Out/' + data['project_name'] + ".out", "rb")
                gencase_failed_dialog = QtGui.QMessageBox()
                gencase_failed_dialog.setText(__(
                    "Error executing gencase. Did you add objects to the case?. "
                    "Another reason could be memory issues. View details for more info."))
                gencase_failed_dialog.setDetailedText(
                    gencase_out_file.read().split("================================")[1])
                gencase_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
                gencase_out_file.close()
                gencase_failed_dialog.exec_()
                utils.warning(__("GenCase Failed. Probably because nothing is in the scene."))

        # Save data array on disk
        try:
            with open(save_name + "/casedata.dsphdata", 'wb') as picklefile:
                pickle.dump(data, picklefile, utils.PICKLE_PROTOCOL)
        except Exception:
            guiutils.error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))

    else:
        utils.log(__("Saving cancelled."))


def on_load_case():
    """Defines loading case mechanism.
    Load points to a dsphdata custom file, that stores all the relevant info.
    If FCStd file is not found the project is considered corrupt."""
    # noinspection PyArgumentList
    load_name, _ = QtGui.QFileDialog.getOpenFileName(dsph_main_dock, __("Load Case"), QtCore.QDir.homePath(),
                                                     "casedata.dsphdata")
    if load_name == "":
        # User pressed cancel.  No path is selected.
        return
    load_path_project_folder = "/".join(load_name.split("/")[:-1])
    if not os.path.isfile(load_path_project_folder + "/DSPH_Case.FCStd"):
        guiutils.warning_dialog(__("DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."))
        utils.error(__("DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."))
        return

    # Tries to close all documents
    if utils.document_count() > 0:
        load_success = utils.prompt_close_all_documents()
        if not load_success:
            return

    # Opens the case freecad document
    FreeCAD.open(load_path_project_folder + "/DSPH_Case.FCStd")

    # Loads own file and sets data and button behaviour
    global data
    global dp_input
    try:
        # Previous versions of DesignSPHysics saved the data on disk in an ASCII way (pickle protocol 0), so sometimes
        # due to OS changes files would be corrupted. Now it is saved in binary mode so that wouldn't happen. This bit
        # of code is to open files which have an error (or corrupted binary files!).
        with open(load_name, 'rb') as load_picklefile:
            load_disk_data = pickle.load(load_picklefile)
        data.update(load_disk_data)
    except (EOFError, ValueError):
        guiutils.error_dialog(__("There was an error importing the case properties. "
                                 "You probably need to set them again."
                                 "\n\nThis could be caused due to file corruption, "
                                 "caused by operating system based line "
                                 "endings or ends-of-file, or other related aspects."))

    dp_input.setText(str(data['dp']))
    data['project_path'] = load_path_project_folder
    data['project_name'] = load_path_project_folder.split("/")[-1]

    # Compatibility code. Transform content from previous version to this one.
    # Make FloatProperty compatible
    data['floating_mks'] = utils.float_list_to_float_property(data['floating_mks'])
    data['initials_mks'] = utils.initials_list_to_initials_property(data['initials_mks'])

    guiutils.widget_state_config(widget_state_elements, "load base")
    if data['gencase_done']:
        guiutils.widget_state_config(widget_state_elements, "gencase done")
    else:
        guiutils.widget_state_config(widget_state_elements, "gencase not done")

    if data['simulation_done']:
        guiutils.widget_state_config(widget_state_elements, "simulation done")
    else:
        guiutils.widget_state_config(widget_state_elements, "simulation not done")

    os.chdir(data['project_path'])
    data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'], correct_execs = utils.check_executables(
        data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'])
    if not correct_execs:
        guiutils.widget_state_config(widget_state_elements, "execs not correct")

    on_tree_item_selection_change()


def on_add_fillbox():
    """ Add fillbox group. It consists
    in a group with 2 objects inside: a point and a box.
    The point represents the fill seed and the box sets
    the bounds for the filling"""
    fillbox_gp = FreeCAD.getDocument("DSPH_Case").addObject("App::DocumentObjectGroup", "FillBox")
    fillbox_point = FreeCAD.ActiveDocument.addObject("Part::Sphere", "FillPoint")
    fillbox_limits = FreeCAD.ActiveDocument.addObject("Part::Box", "FillLimit")
    fillbox_limits.ViewObject.DisplayMode = "Wireframe"
    fillbox_limits.ViewObject.LineColor = (0.00, 0.78, 1.00)
    fillbox_point.Radius.Value = 0.2
    fillbox_point.Placement.Base = FreeCAD.Vector(5, 5, 5)
    fillbox_point.ViewObject.ShapeColor = (0.00, 0.00, 0.00)
    fillbox_gp.addObject(fillbox_limits)
    fillbox_gp.addObject(fillbox_point)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def on_add_stl():
    """ Add STL file. Opens a file opener and allows
    the user to set parameters for the import process"""
    filedialog = QtGui.QFileDialog()
    # noinspection PyArgumentList
    file_name, _ = filedialog.getOpenFileName(fc_main_window, __("Select STL to import"), QtCore.QDir.homePath(),
                                              "STL Files (*.stl)")
    # Defines import stl dialog
    stl_dialog = QtGui.QDialog()
    stl_dialog.setModal(True)
    stl_dialog.setWindowTitle(__("Import STL"))
    stl_dialog_layout = QtGui.QVBoxLayout()
    stl_group = QtGui.QGroupBox(__("Import STL options"))
    stl_group_layout = QtGui.QVBoxLayout()

    # STL File selection
    stl_file_layout = QtGui.QHBoxLayout()
    stl_file_label = QtGui.QLabel(__("STL File: "))
    stl_file_path = QtGui.QLineEdit()
    stl_file_path.setText(file_name)
    stl_file_browse = QtGui.QPushButton(__("Browse"))
    [stl_file_layout.addWidget(x) for x in [stl_file_label, stl_file_path, stl_file_browse]]
    # END STL File selection

    # Scaling factor
    stl_scaling_layout = QtGui.QHBoxLayout()
    stl_scaling_label = QtGui.QLabel(__("Scaling factor: "))
    stl_scaling_x_l = QtGui.QLabel("X: ")
    stl_scaling_x_e = QtGui.QLineEdit("1")
    stl_scaling_y_l = QtGui.QLabel("Y: ")
    stl_scaling_y_e = QtGui.QLineEdit("1")
    stl_scaling_z_l = QtGui.QLabel("Z: ")
    stl_scaling_z_e = QtGui.QLineEdit("1")
    [stl_scaling_layout.addWidget(x) for x in
     [stl_scaling_label, stl_scaling_x_l, stl_scaling_x_e, stl_scaling_y_l, stl_scaling_y_e,
      stl_scaling_z_l, stl_scaling_z_e, ]]
    # END Scaling factor

    # Import object name
    stl_objname_layout = QtGui.QHBoxLayout()
    stl_objname_label = QtGui.QLabel(__("Import object name: "))
    stl_objname_text = QtGui.QLineEdit("ImportedSTL")
    [stl_objname_layout.addWidget(x) for x in [stl_objname_label, stl_objname_text]]
    # End object name

    # Add component layouts to group layout
    [stl_group_layout.addLayout(x) for x in [stl_file_layout, stl_scaling_layout, stl_objname_layout]]
    stl_group_layout.addStretch(1)
    stl_group.setLayout(stl_group_layout)

    # Create button layout
    stl_button_layout = QtGui.QHBoxLayout()
    stl_button_ok = QtGui.QPushButton(__("Import"))
    stl_button_cancel = QtGui.QPushButton(__("Cancel"))
    stl_button_cancel.clicked.connect(lambda: stl_dialog.reject())
    stl_button_layout.addStretch(1)
    stl_button_layout.addWidget(stl_button_cancel)
    stl_button_layout.addWidget(stl_button_ok)

    # Compose main window layout
    stl_dialog_layout.addWidget(stl_group)
    stl_dialog_layout.addStretch(1)
    stl_dialog_layout.addLayout(stl_button_layout)

    stl_dialog.setLayout(stl_dialog_layout)

    # STL Dialog function definition and connections
    def stl_ok_clicked():
        utils.import_stl(filename=str(stl_file_path.text()),
                         scale_x=int(stl_scaling_x_e.text()),
                         scale_y=int(stl_scaling_y_e.text()),
                         scale_z=int(stl_scaling_z_e.text()),
                         name=str(stl_objname_text.text()))
        stl_dialog.accept()

    def stl_dialog_browse():
        file_name_temp, _ = filedialog.getOpenFileName(fc_main_window, __("Select STL to import"),
                                                       QtCore.QDir.homePath(),
                                                       "STL Files (*.stl)")
        stl_file_path.setText(file_name_temp)
        stl_dialog.raise_()
        stl_dialog.activateWindow()

    stl_button_cancel.clicked.connect(lambda: stl_dialog.reject())
    stl_button_ok.clicked.connect(stl_ok_clicked)
    stl_file_browse.clicked.connect(stl_dialog_browse)

    stl_dialog.exec_()


def on_import_xml():
    """ Imports an already created GenCase/DSPH compatible
    file and loads it in the scene. """

    # noinspection PyArgumentList
    import_name, _ = QtGui.QFileDialog.getOpenFileName(dsph_main_dock, __("Import XML"), QtCore.QDir.homePath(),
                                                       "XML Files (*.xml)")
    if import_name == "":
        # User pressed cancel.  No path is selected.
        return
    else:
        if utils.get_number_of_documents() > 0:
            if utils.prompt_close_all_documents():
                on_new_case()
            else:
                return
        else:
            on_new_case()
        config, objects = xmlimporter.import_xml_file(import_name)

        # Set Config
        dp_input.setText(str(config['dp']))
        limits_point_min = config['limits_min']
        limits_point_max = config['limits_max']
        # noinspection PyArgumentList
        FreeCAD.ActiveDocument.getObject('Case_Limits').Placement = FreeCAD.Placement(
            FreeCAD.Vector(limits_point_min[0] * 1000, limits_point_min[1] * 1000, limits_point_min[2] * 1000),
            FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1),
                             0))
        FreeCAD.ActiveDocument.getObject("Case_Limits").Length = str(limits_point_max[0] - limits_point_min[0]) + ' m'
        FreeCAD.ActiveDocument.getObject("Case_Limits").Width = str(limits_point_max[1] - limits_point_min[1]) + ' m'
        FreeCAD.ActiveDocument.getObject("Case_Limits").Height = str(limits_point_max[2] - limits_point_min[2]) + ' m'

        # Merges and updates current data with the imported one.
        data.update(config)

        # Add results to DSPH objects
        for key, value in objects.iteritems():
            add_object_to_sim(key)
            data['simobjects'][key] = value
            # Change visual properties based on fill mode and type
            target_object = FreeCADGui.ActiveDocument.getObject(key)
            if "bound" in value[1]:
                if "full" in value[2]:
                    target_object.ShapeColor = (0.80, 0.80, 0.80)
                    target_object.Transparency = 0
                elif "solid" in value[2]:
                    target_object.ShapeColor = (0.80, 0.80, 0.80)
                    target_object.Transparency = 0
                elif "face" in value[2]:
                    target_object.ShapeColor = (0.80, 0.80, 0.80)
                    target_object.Transparency = 80
                elif "wire" in value[2]:
                    target_object.ShapeColor = (0.80, 0.80, 0.80)
                    target_object.Transparency = 85
            if "fluid" in value[1]:
                if "full" in value[2]:
                    target_object.ShapeColor = (0.00, 0.45, 1.00)
                    target_object.Transparency = 30
                elif "solid" in value[2]:
                    target_object.ShapeColor = (0.00, 0.45, 1.00)
                    target_object.Transparency = 30
                elif "face" in value[2]:
                    target_object.ShapeColor = (0.00, 0.45, 1.00)
                    target_object.Transparency = 80
                elif "wire" in value[2]:
                    target_object.ShapeColor = (0.00, 0.45, 1.00)
                    target_object.Transparency = 85

            # Notify change to refresh UI elements related.
            on_tree_item_selection_change()
    guiutils.info_dialog(__("Importing successful. Note that some objects may not be automatically added to the case,"
                            " and other may not have its properties correctly applied."))


# Connect case control buttons
casecontrols_bt_newdoc.clicked.connect(on_new_case)
casecontrols_bt_savedoc.clicked.connect(on_save_case)
casecontrols_bt_loaddoc.clicked.connect(on_load_case)
casecontrols_bt_addfillbox.clicked.connect(on_add_fillbox)
casecontrols_bt_addstl.clicked.connect(on_add_stl)
casecontrols_bt_importxml.clicked.connect(on_import_xml)

# Defines case control scaffolding
cclabel_layout.addWidget(casecontrols_label)
ccfilebuttons_layout.addWidget(casecontrols_bt_newdoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_savedoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_loaddoc)
ccaddbuttons_layout.addWidget(casecontrols_bt_addfillbox)
ccaddbuttons_layout.addWidget(casecontrols_bt_addstl)
ccaddbuttons_layout.addWidget(casecontrols_bt_importxml)
cc_layout.addLayout(cclabel_layout)
cc_layout.addLayout(ccfilebuttons_layout)
cc_layout.addLayout(ccaddbuttons_layout)
cc_separator = QtGui.QFrame()
cc_separator.setFrameStyle(QtGui.QFrame.HLine)

# Defines run window dialog
run_dialog = QtGui.QDialog(None, QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
run_watcher = QtCore.QFileSystemWatcher()

run_dialog.setModal(False)
run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
run_dialog.setFixedSize(550, 273)
run_dialog_layout = QtGui.QVBoxLayout()

run_group = QtGui.QGroupBox(__("Simulation Data"))
run_group_layout = QtGui.QVBoxLayout()
run_group_label_case = QtGui.QLabel(__("Case name: "))
run_group_label_proc = QtGui.QLabel(__("Simulation processor: "))
run_group_label_part = QtGui.QLabel(__("Number of particles: "))
run_group_label_partsout = QtGui.QLabel(__("Total particles out: "))
run_group_label_eta = QtGui.QLabel(run_dialog)
run_group_label_eta.setText(__("Estimated time to complete simulation: {}").format("Calculating..."))
run_group_layout.addWidget(run_group_label_case)
run_group_layout.addWidget(run_group_label_proc)
run_group_layout.addWidget(run_group_label_part)
run_group_layout.addWidget(run_group_label_partsout)
run_group_layout.addWidget(run_group_label_eta)
run_group_layout.addStretch(1)
run_group.setLayout(run_group_layout)

run_progbar_layout = QtGui.QHBoxLayout()
run_progbar_bar = QtGui.QProgressBar()
run_progbar_bar.setRange(0, 100)
run_progbar_bar.setTextVisible(False)
run_progbar_layout.addWidget(run_progbar_bar)

run_button_layout = QtGui.QHBoxLayout()
run_button_cancel = QtGui.QPushButton(__("Cancel Simulation"))
run_button_layout.addStretch(1)
run_button_layout.addWidget(run_button_cancel)

run_dialog_layout.addWidget(run_group)
run_dialog_layout.addLayout(run_progbar_layout)
run_dialog_layout.addLayout(run_button_layout)

run_dialog.setLayout(run_dialog_layout)


def on_ex_simulate():
    """Defines what happens on simulation button press.
    It shows the run window and starts a background process
    with dualsphysics running. Updates the window with useful info."""
    run_progbar_bar.setValue(0)
    data['simulation_done'] = False
    guiutils.widget_state_config(widget_state_elements, "sim start")
    run_button_cancel.setText(__("Cancel Simulation"))
    run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
    run_group_label_case.setText(__("Case name: ") + data['project_name'])
    run_group_label_proc.setText(__("Simulation processor: ") + str(ex_selector_combo.currentText()))
    run_group_label_part.setText(__("Number of particles: ") + str(data['total_particles']))
    run_group_label_partsout.setText(__("Total particles out: ") + "0")
    run_group_label_eta.setText(__("Estimated time to complete simulation: ") + __("Calculating..."))

    def on_cancel():
        utils.log(__("Stopping simulation"))
        if temp_data['current_process'] is not None:
            temp_data['current_process'].kill()
        run_dialog.hide()
        guiutils.widget_state_config(widget_state_elements, "sim cancel")

    run_button_cancel.clicked.connect(on_cancel)

    # Launch simulation and watch filesystem to monitor simulation
    filelist = [f for f in os.listdir(data['project_path'] + '/' + data['project_name'] + "_Out/") if
                f.startswith("Part")]
    for f in filelist:
        os.remove(data['project_path'] + '/' + data['project_name'] + "_Out/" + f)

    def on_dsph_sim_finished(exit_code):
        output = temp_data['current_process'].readAllStandardOutput()
        run_watcher.removePath(data['project_path'] + '/' + data['project_name'] + "_Out/")
        run_dialog.setWindowTitle(__("DualSPHysics Simulation: Complete"))
        run_progbar_bar.setValue(100)
        run_button_cancel.setText(__("Close"))
        if exit_code == 0:
            data['simulation_done'] = True
            guiutils.widget_state_config(widget_state_elements, "sim finished")
        else:
            if "exception" in str(output).lower():
                utils.error(__("Exception in execution."))
                run_dialog.setWindowTitle(__("DualSPHysics Simulation: Error"))
                run_progbar_bar.setValue(0)
                run_dialog.hide()
                guiutils.widget_state_config(widget_state_elements, "sim error")
                execution_error_dialog = QtGui.QMessageBox()
                execution_error_dialog.setText(__(
                    "There was an error in execution. Make sure you set the parameters right (and they exist)."
                    " Also, make sure that your computer has the right hardware to simulate."
                    " Check the details for more information."))
                execution_error_dialog.setDetailedText(str(output).split("================================")[1])
                execution_error_dialog.setIcon(QtGui.QMessageBox.Critical)
                execution_error_dialog.exec_()

    # Launches a QProcess in background
    process = QtCore.QProcess(run_dialog)
    process.finished.connect(on_dsph_sim_finished)
    temp_data['current_process'] = process
    static_params_exe = [data['project_path'] + '/' + data['project_name'] + "_Out/" + data['project_name'],
                         data['project_path'] + '/' + data['project_name'] + "_Out/", "-svres",
                         "-" + str(ex_selector_combo.currentText()).lower()]
    if len(data['additional_parameters']) < 2:
        additional_params_ex = list()
    else:
        additional_params_ex = data['additional_parameters'].split(" ")
    final_params_ex = static_params_exe + additional_params_ex
    temp_data['current_process'].start(data['dsphysics_path'], final_params_ex)

    def on_fs_change():
        run_file_data = ''
        try:
            run_file = open(data['project_path'] + '/' + data['project_name'] + "_Out/Run.out", "r")
            run_file_data = run_file.readlines()
            run_file.close()
        except Exception as e:
            utils.debug(e)

        # Set percentage scale based on timemax
        for l in run_file_data:
            if data['timemax'] == -1:
                if "TimeMax=" in l:
                    data['timemax'] = float(l.split("=")[1])

        if "Part_" in run_file_data[-1]:
            last_line_parttime = run_file_data[-1].split(".")
            if "Part_" in last_line_parttime[0]:
                current_value = (float(last_line_parttime[0].split(" ")[-1] + "." + last_line_parttime[1][:2]) * float(
                    100)) / float(data['timemax'])
                run_progbar_bar.setValue(current_value)
                run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format(str(format(current_value, ".2f"))))

            last_line_time = run_file_data[-1].split("  ")[-1]
            if ("===" not in last_line_time) and ("CellDiv" not in last_line_time) and (
                        "memory" not in last_line_time) and ("-" in last_line_time):
                # update time field
                try:
                    run_group_label_eta.setText(__("Estimated time to complete simulation: ") + last_line_time)
                except RuntimeError:
                    run_group_label_eta.setText(__("Estimated time to complete simulation: ") + "Calculating...")
                    pass
        elif "Particles out:" in run_file_data[-1]:
            totalpartsout = int(run_file_data[-1].split("(total: ")[1].split(")")[0])
            data['total_particles_out'] = totalpartsout
            run_group_label_partsout.setText(__("Total particles out: {}").format(str(data['total_particles_out'])))

    run_watcher.addPath(data['project_path'] + '/' + data['project_name'] + "_Out/")
    run_watcher.directoryChanged.connect(on_fs_change)
    if temp_data['current_process'].state() == QtCore.QProcess.NotRunning:
        # Probably error happened.
        run_watcher.removePath(data['project_path'] + '/' + data['project_name'] + "_Out/")

        temp_data['current_process'] = ""
        exec_not_correct_dialog = QtGui.QMessageBox()
        exec_not_correct_dialog.setText(__("Error on simulation start. Is the path of DualSPHysics correctly placed?"))
        exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Critical)
        exec_not_correct_dialog.exec_()
    else:
        run_dialog.show()


def on_additional_parameters():
    additional_parameters_window = QtGui.QDialog()
    additional_parameters_window.setWindowTitle(__("Additional parameters"))
    ok_button = QtGui.QPushButton(__("Ok"))
    cancel_button = QtGui.QPushButton(__("Cancel"))

    def on_ok():
        data['additional_parameters'] = export_params.text()
        additional_parameters_window.accept()

    def on_cancel():
        additional_parameters_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    # Button layout definition
    eo_button_layout = QtGui.QHBoxLayout()
    eo_button_layout.addStretch(1)
    eo_button_layout.addWidget(ok_button)
    eo_button_layout.addWidget(cancel_button)

    paramintro_layout = QtGui.QHBoxLayout()
    paramintro_label = QtGui.QLabel(__("Additional Parameters: "))
    export_params = QtGui.QLineEdit()
    export_params.setText(data['additional_parameters'])
    paramintro_layout.addWidget(paramintro_label)
    paramintro_layout.addWidget(export_params)

    additional_parameters_layout = QtGui.QVBoxLayout()
    additional_parameters_layout.addLayout(paramintro_layout)
    additional_parameters_layout.addStretch(1)
    additional_parameters_layout.addLayout(eo_button_layout)

    additional_parameters_window.setFixedSize(600, 110)
    additional_parameters_window.setLayout(additional_parameters_layout)
    additional_parameters_window.exec_()


# Execution section scaffolding
ex_layout = QtGui.QVBoxLayout()
ex_label = QtGui.QLabel(
    "<b>" + __("Simulation control") + "</b> ")
ex_label.setWordWrap(True)
ex_selector_layout = QtGui.QHBoxLayout()
ex_selector_label = QtGui.QLabel(__("Simulation processor:"))
ex_selector_combo = QtGui.QComboBox()
ex_selector_combo.addItem("CPU")
ex_selector_combo.addItem("GPU")
widget_state_elements['ex_selector_combo'] = ex_selector_combo
ex_selector_layout.addWidget(ex_selector_label)
ex_selector_layout.addWidget(ex_selector_combo)
ex_button = QtGui.QPushButton(__("Simulate Case"))
ex_button.setToolTip(__(
    "Starts the case simulation. "
    "From the simulation\nwindow you can see the current progress and\nuseful information."))
ex_button.clicked.connect(on_ex_simulate)
widget_state_elements['ex_button'] = ex_button
ex_additional = QtGui.QPushButton(__("Additional parameters"))
ex_additional.setToolTip("__(Sets simulation additional parameters for execution.)")
ex_additional.clicked.connect(on_additional_parameters)
widget_state_elements['ex_additional'] = ex_additional
ex_button_layout = QtGui.QHBoxLayout()
ex_button_layout.addWidget(ex_button)
ex_button_layout.addWidget(ex_additional)
ex_layout.addWidget(ex_label)
ex_layout.addLayout(ex_selector_layout)
ex_layout.addLayout(ex_button_layout)

ex_separator = QtGui.QFrame()
ex_separator.setFrameStyle(QtGui.QFrame.HLine)

# Defines export window dialog
export_dialog = QtGui.QDialog(None, QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)

export_dialog.setModal(False)
export_dialog.setWindowTitle(__("Export to VTK: {}%").format("0"))
export_dialog.setFixedSize(550, 143)
export_dialog_layout = QtGui.QVBoxLayout()

export_progbar_layout = QtGui.QHBoxLayout()
export_progbar_bar = QtGui.QProgressBar()
export_progbar_bar.setRange(0, 100)
export_progbar_bar.setTextVisible(False)
export_progbar_layout.addWidget(export_progbar_bar)

export_button_layout = QtGui.QHBoxLayout()
export_button_cancel = QtGui.QPushButton(__("Cancel Exporting"))
export_button_layout.addStretch(1)
export_button_layout.addWidget(export_button_cancel)

export_dialog_layout.addLayout(export_progbar_layout)
export_dialog_layout.addLayout(export_button_layout)

export_dialog.setLayout(export_dialog_layout)


def on_export():
    """Export VTK button behaviour.
    Launches a process while disabling the button."""
    guiutils.widget_state_config(widget_state_elements, "export start")
    temp_data['export_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_Out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]),
                                              temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
        temp_data['export_button'].setText(__("Export data to VTK"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    def on_export_finished():
        temp_data['export_button'].setText(__("Export data to VTK"))
        guiutils.widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()

    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)
    static_params_exp = ['-dirin ' + data['project_path'] + '/' + data['project_name'] + '_Out/',
                         '-savevtk ' + data['project_path'] + '/' + data['project_name'] + '_Out/PartAll']
    if len(data['export_options']) < 2:
        additional_params_exp = list()
    else:
        additional_params_exp = data['additional_parameters'].split(" ")

    final_params_exp = static_params_exp + additional_params_exp
    export_process.start(data['partvtk4_path'], final_params_exp)
    temp_data['current_export_process'] = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        try:
            current_part = int(current_output.split("PartAll_")[1].split(".vtk")[0])
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(current_part)
        export_dialog.setWindowTitle(
            __("Export to VTK: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(on_stdout_ready)


def on_exportopts():
    export_options_window = QtGui.QDialog()
    export_options_window.setWindowTitle(__("Export options"))
    ok_button = QtGui.QPushButton(__("Ok"))
    cancel_button = QtGui.QPushButton(__("Cancel"))

    def on_ok():
        data['export_options'] = export_params.text()
        export_options_window.accept()

    def on_cancel():
        export_options_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    # Button layout definition
    eo_button_layout = QtGui.QHBoxLayout()
    eo_button_layout.addStretch(1)
    eo_button_layout.addWidget(ok_button)
    eo_button_layout.addWidget(cancel_button)

    export_params_layout = QtGui.QHBoxLayout()
    export_params_label = QtGui.QLabel(__("Export parameters: "))
    export_params = QtGui.QLineEdit()
    export_params.setText(data['export_options'])
    export_params_layout.addWidget(export_params_label)
    export_params_layout.addWidget(export_params)

    export_options_layout = QtGui.QVBoxLayout()
    export_options_layout.addLayout(export_params_layout)
    export_options_layout.addStretch(1)
    export_options_layout.addLayout(eo_button_layout)

    export_options_window.setFixedSize(600, 110)
    export_options_window.setLayout(export_options_layout)
    export_options_window.exec_()


# Export to VTK section scaffolding
export_layout = QtGui.QVBoxLayout()
export_label = QtGui.QLabel(
    "<b>" + __("Export and visualization") + "</b>")
export_label.setWordWrap(True)
export_buttons_layout = QtGui.QHBoxLayout()
export_button = QtGui.QPushButton(__("Export data to VTK"))
widget_state_elements['export_button'] = export_button
exportopts_button = QtGui.QPushButton(__("Options"))
exportopts_button.setToolTip(__("Sets additional parameters for exporting."))
widget_state_elements['exportopts_button'] = exportopts_button
export_button.setToolTip(__("Exports the simulation data to VTK format."))
export_button.clicked.connect(on_export)
exportopts_button.clicked.connect(on_exportopts)
temp_data['export_button'] = export_button
temp_data['exportopts_button'] = exportopts_button
export_layout.addWidget(export_label)
export_buttons_layout.addWidget(export_button)
export_buttons_layout.addWidget(exportopts_button)
export_layout.addLayout(export_buttons_layout)

export_separator = QtGui.QFrame()
export_separator.setFrameStyle(QtGui.QFrame.HLine)

# Object list table scaffolding
objectlist_layout = QtGui.QVBoxLayout()
objectlist_label = QtGui.QLabel("<b>" + __("Simulation object order") + "</b>")
objectlist_label.setWordWrap(True)
objectlist_table = QtGui.QTableWidget(0, 3)
objectlist_table.setToolTip(__(
    "Press 'Move up' to move an object up in the hirearchy."
    "\nPress 'Move down' to move an object down in the hirearchy."))
objectlist_table.setObjectName("DSPH Objects")
objectlist_table.verticalHeader().setVisible(False)
objectlist_table.setHorizontalHeaderLabels([__("Object Name"), __("Order up"), __("Order down")])
objectlist_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
widget_state_elements['objectlist_table'] = objectlist_table
temp_data['objectlist_table'] = objectlist_table
objectlist_layout.addWidget(objectlist_label)
objectlist_layout.addWidget(objectlist_table)

objectlist_separator = QtGui.QFrame()
objectlist_separator.setFrameStyle(QtGui.QFrame.HLine)

# Layout adding and ordering
logo_layout.addStretch(0.5)
logo_layout.addWidget(logo_label)
logo_layout.addStretch(0.5)

# Adding things here and there
intro_layout.addWidget(constants_label)
constantsandsetup_layout = QtGui.QHBoxLayout()
constantsandsetup_layout.addWidget(constants_button)
constantsandsetup_layout.addWidget(execparams_button)
constantsandsetup_layout.addWidget(setup_button)
intro_layout.addWidget(help_button)
intro_layout.addLayout(constantsandsetup_layout)
intro_layout.addWidget(constants_separator)
main_layout.addLayout(logo_layout)
main_layout.addLayout(intro_layout)
main_layout.addLayout(dp_layout)
main_layout.addWidget(crucialvars_separator)
main_layout.addLayout(cc_layout)
main_layout.addWidget(cc_separator)
main_layout.addLayout(ex_layout)
main_layout.addWidget(ex_separator)
main_layout.addLayout(export_layout)
main_layout.addWidget(export_separator)
main_layout.addLayout(objectlist_layout)

# Default disabled widgets
guiutils.widget_state_config(widget_state_elements, "no case")

# You can't apply layouts to a QDockWidget,
# so creating a standard widget, applying the layouts,
# and then setting it as the QDockWidget
dsph_main_dock_scaff_widget.setLayout(main_layout)
dsph_main_dock.setWidget(dsph_main_dock_scaff_widget)

# And docking it at right side of screen
fc_main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dsph_main_dock)

# DSPH OBJECT PROPERTIES DOCK RELATED CODE
# ----------------------------
# Tries to find and close previous instances of the widget.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, "DSPH_Properties")
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

# Creation of the widget and scaffolding
properties_widget = QtGui.QDockWidget()
properties_widget.setMinimumHeight(100)
properties_widget.setObjectName("DSPH_Properties")
properties_widget.setWindowTitle(__("DSPH Object Properties"))
properties_scaff_widget = QtGui.QWidget()  # Scaffolding widget, only useful to apply to the properties_dock widget
property_widget_layout = QtGui.QVBoxLayout()
property_table = QtGui.QTableWidget(6, 2)
property_table.setHorizontalHeaderLabels([__("Property Name"), __("Value")])
property_table.verticalHeader().setVisible(False)
property_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
addtodsph_button = QtGui.QPushButton(__("Add to DSPH Simulation"))
addtodsph_button.setToolTip(__("Adds the current selection to\nthe case. Objects not included will not be exported."))
removefromdsph_button = QtGui.QPushButton(__("Remove from DSPH Simulation"))
removefromdsph_button.setToolTip(__(
    "Removes the current selection from the case.\nObjects not included in the case will not be exported."))
property_widget_layout.addWidget(property_table)
property_widget_layout.addWidget(addtodsph_button)
property_widget_layout.addWidget(removefromdsph_button)
properties_scaff_widget.setLayout(property_widget_layout)

properties_widget.setWidget(properties_scaff_widget)
mkgroup_label = QtGui.QLabel("   " + __("MKGroup"))
mkgroup_label.setToolTip(__("Establishes the object group."))
objtype_label = QtGui.QLabel("   " + __("Type of object"))
objtype_label.setToolTip(__("Establishes the object type, fluid or bound"))
fillmode_label = QtGui.QLabel("   " + __("Fill mode"))
fillmode_label.setToolTip(__(
    "Sets fill mode.\nFull: generates filling and external mesh."
    "\nSolid: generates only filling.\nFace: generates only external mesh."
    "\nWire: generates only external mesh polygon edges."))
floatstate_label = QtGui.QLabel("   " + __("Float state"))
floatstate_label.setToolTip(__("Sets floating state for this object MK."))
initials_label = QtGui.QLabel("   " + __("Initials"))
initials_label.setToolTip(__("Sets initials options for this object"))
material_label = QtGui.QLabel("   " + __("Material"))
material_label.setToolTip(__("Sets material for this object"))
mkgroup_label.setAlignment(QtCore.Qt.AlignLeft)
material_label.setAlignment(QtCore.Qt.AlignLeft)
objtype_label.setAlignment(QtCore.Qt.AlignLeft)
fillmode_label.setAlignment(QtCore.Qt.AlignLeft)
floatstate_label.setAlignment(QtCore.Qt.AlignLeft)
initials_label.setAlignment(QtCore.Qt.AlignLeft)
property_table.setCellWidget(0, 0, mkgroup_label)
property_table.setCellWidget(1, 0, objtype_label)
property_table.setCellWidget(2, 0, fillmode_label)
property_table.setCellWidget(3, 0, floatstate_label)
property_table.setCellWidget(4, 0, initials_label)
property_table.setCellWidget(5, 0, material_label)


def mkgroup_change(value):
    """Defines what happens when MKGroup is changed."""
    selection = FreeCADGui.Selection.getSelection()[0]
    data['simobjects'][selection.Name][0] = value


def objtype_change(index):
    """Defines what happens when type of object is changed"""
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
    data['simobjects'][selection.Name][1] = objtype_prop.itemText(index)
    if "fillbox" in selection.Name.lower():
        return
    if objtype_prop.itemText(index).lower() == "bound":
        mkgroup_prop.setRange(0, 240)
        selectiongui.ShapeColor = (0.80, 0.80, 0.80)
        selectiongui.Transparency = 0
        floatstate_prop.setEnabled(True)
        initials_prop.setEnabled(False)
        mkgroup_label.setText("   " + __("MKBound"))
    elif objtype_prop.itemText(index).lower() == "fluid":
        mkgroup_prop.setRange(0, 10)
        selectiongui.ShapeColor = (0.00, 0.45, 1.00)
        selectiongui.Transparency = 30
        if str(str(data['simobjects'][selection.Name][0])) in data['floating_mks'].keys():
            data['floating_mks'].pop(str(data['simobjects'][selection.Name][0]), None)
        floatstate_prop.setEnabled(False)
        initials_prop.setEnabled(True)
        mkgroup_label.setText("   " + __("MKFluid"))


def fillmode_change(index):
    """Defines what happens when fill mode is changed"""
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
    data['simobjects'][selection.Name][2] = fillmode_prop.itemText(index)
    if fillmode_prop.itemText(index).lower() == "full":
        if objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "fluid":
            selectiongui.Transparency = 30
        elif objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "bound":
            selectiongui.Transparency = 0
    elif fillmode_prop.itemText(index).lower() == "solid":
        if objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "fluid":
            selectiongui.Transparency = 30
        elif objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "bound":
            selectiongui.Transparency = 0
    elif fillmode_prop.itemText(index).lower() == "face":
        selectiongui.Transparency = 80
    elif fillmode_prop.itemText(index).lower() == "wire":
        selectiongui.Transparency = 85


def floatstate_change():
    """Defines a window with floating properties."""
    floatings_window = QtGui.QDialog()
    floatings_window.setWindowTitle(__("Floating configuration"))
    ok_button = QtGui.QPushButton(__("Ok"))
    cancel_button = QtGui.QPushButton(__("Cancel"))
    target_mk = int(data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])

    def on_ok():
        guiutils.info_dialog(
            __("This will apply the floating properties to all objects with mkbound = ") + str(target_mk))
        if is_floating_selector.currentIndex() == 1:
            # Floating false
            if str(target_mk) in data['floating_mks'].keys():
                data['floating_mks'].pop(str(target_mk), None)
        else:
            # Floating true
            # Structure: 'mk': [massrhop, center, inertia, velini, omegaini]
            # Structure: 'mk': FloatProperty
            fp = FloatProperty()  # FloatProperty to be inserted
            fp.mk = target_mk
            fp.mass_density_type = floating_props_massrhop_selector.currentIndex()
            fp.mass_density_value = float(floating_props_massrhop_input.text())

            if floating_center_auto.isChecked():
                fp.gravity_center = list()
            else:
                fp.gravity_center = [float(floating_center_input_x.text()),
                                     float(floating_center_input_y.text()),
                                     float(floating_center_input_z.text())]

            if floating_center_auto.isChecked():
                fp.gravity_center = list()
            else:
                fp.gravity_center = [float(floating_center_input_x.text()),
                                     float(floating_center_input_y.text()),
                                     float(floating_center_input_z.text())]

            if floating_inertia_auto.isChecked():
                fp.inertia = list()
            else:
                fp.inertia = [float(floating_inertia_input_x.text()),
                              float(floating_inertia_input_y.text()),
                              float(floating_inertia_input_z.text())]

            if floating_velini_auto.isChecked():
                fp.initial_linear_velocity = list()
            else:
                fp.initial_linear_velocity = [float(floating_velini_input_x.text()),
                                              float(floating_velini_input_y.text()),
                                              float(floating_velini_input_z.text())]

            if floating_omegaini_auto.isChecked():
                fp.initial_angular_velocity = list()
            else:
                fp.initial_angular_velocity = [float(floating_omegaini_input_x.text()),
                                               float(floating_omegaini_input_y.text()),
                                               float(floating_omegaini_input_z.text())]

            data['floating_mks'][str(target_mk)] = fp

        floatings_window.accept()

    def on_cancel():
        floatings_window.reject()

    def on_floating_change(index):
        if index == 0:
            floating_props_group.setEnabled(True)
        else:
            floating_props_group.setEnabled(False)

    def on_massrhop_change(index):
        if index == 0:
            floating_props_massrhop_input.setText("0.0")
        else:
            floating_props_massrhop_input.setText("0.0")

    def on_gravity_auto():
        if floating_center_auto.isChecked():
            floating_center_input_x.setEnabled(False)
            floating_center_input_y.setEnabled(False)
            floating_center_input_z.setEnabled(False)
        else:
            floating_center_input_x.setEnabled(True)
            floating_center_input_y.setEnabled(True)
            floating_center_input_z.setEnabled(True)

    def on_inertia_auto():
        if floating_inertia_auto.isChecked():
            floating_inertia_input_x.setEnabled(False)
            floating_inertia_input_y.setEnabled(False)
            floating_inertia_input_z.setEnabled(False)
        else:
            floating_inertia_input_x.setEnabled(True)
            floating_inertia_input_y.setEnabled(True)
            floating_inertia_input_z.setEnabled(True)

    def on_velini_auto():
        if floating_velini_auto.isChecked():
            floating_velini_input_x.setEnabled(False)
            floating_velini_input_y.setEnabled(False)
            floating_velini_input_z.setEnabled(False)
        else:
            floating_velini_input_x.setEnabled(True)
            floating_velini_input_y.setEnabled(True)
            floating_velini_input_z.setEnabled(True)

    def on_omegaini_auto():
        if floating_omegaini_auto.isChecked():
            floating_omegaini_input_x.setEnabled(False)
            floating_omegaini_input_y.setEnabled(False)
            floating_omegaini_input_z.setEnabled(False)
        else:
            floating_omegaini_input_x.setEnabled(True)
            floating_omegaini_input_y.setEnabled(True)
            floating_omegaini_input_z.setEnabled(True)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    is_floating_layout = QtGui.QHBoxLayout()
    is_floating_label = QtGui.QLabel(__("Set floating: "))
    is_floating_label.setToolTip(__("Sets the current MKBound selected as floating."))
    is_floating_selector = QtGui.QComboBox()
    is_floating_selector.insertItems(0, ["True", "False"])
    is_floating_selector.currentIndexChanged.connect(on_floating_change)
    is_floating_targetlabel = QtGui.QLabel(__("Target MKBound: ") + str(target_mk))
    is_floating_layout.addWidget(is_floating_label)
    is_floating_layout.addWidget(is_floating_selector)
    is_floating_layout.addStretch(1)
    is_floating_layout.addWidget(is_floating_targetlabel)

    floating_props_group = QtGui.QGroupBox(__("Floating properties"))
    floating_props_layout = QtGui.QVBoxLayout()
    floating_props_massrhop_layout = QtGui.QHBoxLayout()
    floating_props_massrhop_label = QtGui.QLabel(__("Mass/Density: "))
    floating_props_massrhop_label.setToolTip(__("Selects an mass/density calculation method and its value."))
    floating_props_massrhop_selector = QtGui.QComboBox()
    floating_props_massrhop_selector.insertItems(0, ['massbody', 'rhopbody'])
    floating_props_massrhop_selector.currentIndexChanged.connect(on_massrhop_change)
    floating_props_massrhop_input = QtGui.QLineEdit()
    floating_props_massrhop_layout.addWidget(floating_props_massrhop_label)
    floating_props_massrhop_layout.addWidget(floating_props_massrhop_selector)
    floating_props_massrhop_layout.addWidget(floating_props_massrhop_input)

    floating_center_layout = QtGui.QHBoxLayout()
    floating_center_label = QtGui.QLabel(__("Gravity center: "))
    floating_center_label.setToolTip(__("Sets the mk group gravity center."))
    floating_center_label_x = QtGui.QLabel("X")
    floating_center_input_x = QtGui.QLineEdit()
    floating_center_label_y = QtGui.QLabel("Y")
    floating_center_input_y = QtGui.QLineEdit()
    floating_center_label_z = QtGui.QLabel("Z")
    floating_center_input_z = QtGui.QLineEdit()
    floating_center_auto = QtGui.QCheckBox("Auto ")
    floating_center_auto.toggled.connect(on_gravity_auto)
    floating_center_layout.addWidget(floating_center_label)
    floating_center_layout.addWidget(floating_center_label_x)
    floating_center_layout.addWidget(floating_center_input_x)
    floating_center_layout.addWidget(floating_center_label_y)
    floating_center_layout.addWidget(floating_center_input_y)
    floating_center_layout.addWidget(floating_center_label_z)
    floating_center_layout.addWidget(floating_center_input_z)
    floating_center_layout.addWidget(floating_center_auto)

    floating_inertia_layout = QtGui.QHBoxLayout()
    floating_inertia_label = QtGui.QLabel(__("Inertia: "))
    floating_inertia_label.setToolTip(__("Sets the mk group inertia."))
    floating_inertia_label_x = QtGui.QLabel("X")
    floating_inertia_input_x = QtGui.QLineEdit()
    floating_inertia_label_y = QtGui.QLabel("Y")
    floating_inertia_input_y = QtGui.QLineEdit()
    floating_inertia_label_z = QtGui.QLabel("Z")
    floating_inertia_input_z = QtGui.QLineEdit()
    floating_inertia_auto = QtGui.QCheckBox("Auto ")
    floating_inertia_auto.toggled.connect(on_inertia_auto)
    floating_inertia_layout.addWidget(floating_inertia_label)
    floating_inertia_layout.addWidget(floating_inertia_label_x)
    floating_inertia_layout.addWidget(floating_inertia_input_x)
    floating_inertia_layout.addWidget(floating_inertia_label_y)
    floating_inertia_layout.addWidget(floating_inertia_input_y)
    floating_inertia_layout.addWidget(floating_inertia_label_z)
    floating_inertia_layout.addWidget(floating_inertia_input_z)
    floating_inertia_layout.addWidget(floating_inertia_auto)

    floating_velini_layout = QtGui.QHBoxLayout()
    floating_velini_label = QtGui.QLabel(__("Initial linear velocity: "))
    floating_velini_label.setToolTip(__("Sets the mk group initial linear velocity"))
    floating_velini_label_x = QtGui.QLabel("X")
    floating_velini_input_x = QtGui.QLineEdit()
    floating_velini_label_y = QtGui.QLabel("Y")
    floating_velini_input_y = QtGui.QLineEdit()
    floating_velini_label_z = QtGui.QLabel("Z")
    floating_velini_input_z = QtGui.QLineEdit()
    floating_velini_auto = QtGui.QCheckBox("Auto ")
    floating_velini_auto.toggled.connect(on_velini_auto)
    floating_velini_layout.addWidget(floating_velini_label)
    floating_velini_layout.addWidget(floating_velini_label_x)
    floating_velini_layout.addWidget(floating_velini_input_x)
    floating_velini_layout.addWidget(floating_velini_label_y)
    floating_velini_layout.addWidget(floating_velini_input_y)
    floating_velini_layout.addWidget(floating_velini_label_z)
    floating_velini_layout.addWidget(floating_velini_input_z)
    floating_velini_layout.addWidget(floating_velini_auto)

    floating_omegaini_layout = QtGui.QHBoxLayout()
    floating_omegaini_label = QtGui.QLabel(__("Initial angular velocity: "))
    floating_omegaini_label.setToolTip(__("Sets the mk group initial angular velocity"))
    floating_omegaini_label_x = QtGui.QLabel("X")
    floating_omegaini_input_x = QtGui.QLineEdit()
    floating_omegaini_label_y = QtGui.QLabel("Y")
    floating_omegaini_input_y = QtGui.QLineEdit()
    floating_omegaini_label_z = QtGui.QLabel("Z")
    floating_omegaini_input_z = QtGui.QLineEdit()
    floating_omegaini_auto = QtGui.QCheckBox("Auto ")
    floating_omegaini_auto.toggled.connect(on_omegaini_auto)
    floating_omegaini_layout.addWidget(floating_omegaini_label)
    floating_omegaini_layout.addWidget(floating_omegaini_label_x)
    floating_omegaini_layout.addWidget(floating_omegaini_input_x)
    floating_omegaini_layout.addWidget(floating_omegaini_label_y)
    floating_omegaini_layout.addWidget(floating_omegaini_input_y)
    floating_omegaini_layout.addWidget(floating_omegaini_label_z)
    floating_omegaini_layout.addWidget(floating_omegaini_input_z)
    floating_omegaini_layout.addWidget(floating_omegaini_auto)

    floating_props_layout.addLayout(floating_props_massrhop_layout)
    floating_props_layout.addLayout(floating_center_layout)
    floating_props_layout.addLayout(floating_inertia_layout)
    floating_props_layout.addLayout(floating_velini_layout)
    floating_props_layout.addLayout(floating_omegaini_layout)
    floating_props_layout.addStretch(1)
    floating_props_group.setLayout(floating_props_layout)

    buttons_layout = QtGui.QHBoxLayout()
    buttons_layout.addStretch(1)
    buttons_layout.addWidget(ok_button)
    buttons_layout.addWidget(cancel_button)

    floatings_window_layout = QtGui.QVBoxLayout()
    floatings_window_layout.addLayout(is_floating_layout)
    floatings_window_layout.addWidget(floating_props_group)
    floatings_window_layout.addLayout(buttons_layout)

    floatings_window.setLayout(floatings_window_layout)

    if str(target_mk) in data['floating_mks'].keys():
        is_floating_selector.setCurrentIndex(0)
        on_floating_change(0)
        floating_props_group.setEnabled(True)
        floating_props_massrhop_selector.setCurrentIndex(data['floating_mks'][str(target_mk)].mass_density_type)
        floating_props_massrhop_input.setText(str(data['floating_mks'][str(target_mk)].mass_density_value))
        if len(data['floating_mks'][str(target_mk)].gravity_center) == 0:
            floating_center_input_x.setText("0")
            floating_center_input_y.setText("0")
            floating_center_input_z.setText("0")
        else:
            floating_center_input_x.setText(str(data['floating_mks'][str(target_mk)].gravity_center[0]))
            floating_center_input_y.setText(str(data['floating_mks'][str(target_mk)].gravity_center[1]))
            floating_center_input_z.setText(str(data['floating_mks'][str(target_mk)].gravity_center[2]))

        if len(data['floating_mks'][str(target_mk)].inertia) == 0:
            floating_inertia_input_x.setText("0")
            floating_inertia_input_y.setText("0")
            floating_inertia_input_z.setText("0")
        else:
            floating_inertia_input_x.setText(str(data['floating_mks'][str(target_mk)].inertia[0]))
            floating_inertia_input_y.setText(str(data['floating_mks'][str(target_mk)].inertia[1]))
            floating_inertia_input_z.setText(str(data['floating_mks'][str(target_mk)].inertia[2]))

        if len(data['floating_mks'][str(target_mk)].initial_linear_velocity) == 0:
            floating_velini_input_x.setText("0")
            floating_velini_input_y.setText("0")
            floating_velini_input_z.setText("0")
        else:
            floating_velini_input_x.setText(str(data['floating_mks'][str(target_mk)].initial_linear_velocity[0]))
            floating_velini_input_y.setText(str(data['floating_mks'][str(target_mk)].initial_linear_velocity[1]))
            floating_velini_input_z.setText(str(data['floating_mks'][str(target_mk)].initial_linear_velocity[2]))

        if len(data['floating_mks'][str(target_mk)].initial_angular_velocity) == 0:
            floating_omegaini_input_x.setText("0")
            floating_omegaini_input_y.setText("0")
            floating_omegaini_input_z.setText("0")
        else:
            floating_omegaini_input_x.setText(str(data['floating_mks'][str(target_mk)].initial_angular_velocity[0]))
            floating_omegaini_input_y.setText(str(data['floating_mks'][str(target_mk)].initial_angular_velocity[1]))
            floating_omegaini_input_z.setText(str(data['floating_mks'][str(target_mk)].initial_angular_velocity[2]))

        floating_center_auto.setCheckState(
            QtCore.Qt.Checked if len(data['floating_mks'][str(target_mk)].gravity_center) == 0
            else QtCore.Qt.Unchecked)
        floating_inertia_auto.setCheckState(
            QtCore.Qt.Checked if len(data['floating_mks'][str(target_mk)].inertia) == 0
            else QtCore.Qt.Unchecked)
        floating_velini_auto.setCheckState(
            QtCore.Qt.Checked if len(data['floating_mks'][str(target_mk)].initial_linear_velocity) == 0
            else QtCore.Qt.Unchecked)
        floating_omegaini_auto.setCheckState(
            QtCore.Qt.Checked if len(data['floating_mks'][str(target_mk)].initial_angular_velocity) == 0
            else QtCore.Qt.Unchecked)
    else:
        is_floating_selector.setCurrentIndex(1)
        on_floating_change(1)
        floating_props_group.setEnabled(False)
        is_floating_selector.setCurrentIndex(1)
        floating_props_massrhop_selector.setCurrentIndex(0)
        floating_props_massrhop_input.setText("100")
        floating_center_input_x.setText("0")
        floating_center_input_y.setText("0")
        floating_center_input_z.setText("0")
        floating_inertia_input_x.setText("0")
        floating_inertia_input_y.setText("0")
        floating_inertia_input_z.setText("0")
        floating_velini_input_x.setText("0")
        floating_velini_input_y.setText("0")
        floating_velini_input_z.setText("0")
        floating_omegaini_input_x.setText("0")
        floating_omegaini_input_y.setText("0")
        floating_omegaini_input_z.setText("0")

        floating_center_auto.setCheckState(QtCore.Qt.Checked)
        floating_inertia_auto.setCheckState(QtCore.Qt.Checked)
        floating_velini_auto.setCheckState(QtCore.Qt.Checked)
        floating_omegaini_auto.setCheckState(QtCore.Qt.Checked)

    floatings_window.exec_()


def initials_change():
    """Defines a window with initials properties."""
    initials_window = QtGui.QDialog()
    initials_window.setWindowTitle(__("Initials configuration"))
    ok_button = QtGui.QPushButton(__("Ok"))
    cancel_button = QtGui.QPushButton(__("Cancel"))
    target_mk = int(data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])

    def on_ok():
        guiutils.info_dialog(
            __("This will apply the initials properties to all objects with mkfluid = ") + str(target_mk))
        if has_initials_selector.currentIndex() == 1:
            # Initials false
            if str(target_mk) in data['initials_mks'].keys():
                data['initials_mks'].pop(str(target_mk), None)
        else:
            # Initials true
            # Structure: InitialsProperty Object
            data['initials_mks'][str(target_mk)] = InitialsProperty(mk=target_mk,
                                                                    force=[float(initials_vector_input_x.text()),
                                                                           float(initials_vector_input_y.text()),
                                                                           float(initials_vector_input_z.text())])
        initials_window.accept()

    def on_cancel():
        initials_window.reject()

    def on_initials_change(index):
        if index == 0:
            initials_props_group.setEnabled(True)
        else:
            initials_props_group.setEnabled(False)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    has_initials_layout = QtGui.QHBoxLayout()
    has_initials_label = QtGui.QLabel(__("Set initials: "))
    has_initials_label.setToolTip(__("Sets the current initial movement vector."))
    has_initials_selector = QtGui.QComboBox()
    has_initials_selector.insertItems(0, ['True', 'False'])
    has_initials_selector.currentIndexChanged.connect(on_initials_change)
    has_initials_targetlabel = QtGui.QLabel(__("Target MKFluid: ") + str(target_mk))
    has_initials_layout.addWidget(has_initials_label)
    has_initials_layout.addWidget(has_initials_selector)
    has_initials_layout.addStretch(1)
    has_initials_layout.addWidget(has_initials_targetlabel)

    initials_props_group = QtGui.QGroupBox(__("Initials properties"))
    initials_props_layout = QtGui.QVBoxLayout()

    initials_vector_layout = QtGui.QHBoxLayout()
    initials_vector_label = QtGui.QLabel(__("Movement vector: "))
    initials_vector_label.setToolTip(__("Sets the mk group movement vector."))
    initials_vector_label_x = QtGui.QLabel("X")
    initials_vector_input_x = QtGui.QLineEdit()
    initials_vector_label_y = QtGui.QLabel("Y")
    initials_vector_input_y = QtGui.QLineEdit()
    initials_vector_label_z = QtGui.QLabel("Z")
    initials_vector_input_z = QtGui.QLineEdit()
    initials_vector_layout.addWidget(initials_vector_label)
    initials_vector_layout.addWidget(initials_vector_label_x)
    initials_vector_layout.addWidget(initials_vector_input_x)
    initials_vector_layout.addWidget(initials_vector_label_y)
    initials_vector_layout.addWidget(initials_vector_input_y)
    initials_vector_layout.addWidget(initials_vector_label_z)
    initials_vector_layout.addWidget(initials_vector_input_z)

    initials_props_layout.addLayout(initials_vector_layout)
    initials_props_layout.addStretch(1)
    initials_props_group.setLayout(initials_props_layout)

    buttons_layout = QtGui.QHBoxLayout()
    buttons_layout.addStretch(1)
    buttons_layout.addWidget(ok_button)
    buttons_layout.addWidget(cancel_button)

    initials_window_layout = QtGui.QVBoxLayout()
    initials_window_layout.addLayout(has_initials_layout)
    initials_window_layout.addWidget(initials_props_group)
    initials_window_layout.addLayout(buttons_layout)

    initials_window.setLayout(initials_window_layout)

    if str(target_mk) in data['initials_mks'].keys():
        has_initials_selector.setCurrentIndex(0)
        on_initials_change(0)
        initials_props_group.setEnabled(True)
        initials_vector_input_x.setText(str(data['initials_mks'][str(target_mk)].force[0]))
        initials_vector_input_y.setText(str(data['initials_mks'][str(target_mk)].force[1]))
        initials_vector_input_z.setText(str(data['initials_mks'][str(target_mk)].force[2]))
    else:
        has_initials_selector.setCurrentIndex(1)
        on_initials_change(1)
        initials_props_group.setEnabled(False)
        has_initials_selector.setCurrentIndex(1)
        initials_vector_input_x.setText("0")
        initials_vector_input_y.setText("0")
        initials_vector_input_z.setText("0")

    initials_window.exec_()


def material_change():
    """Defines a window with initials properties."""
    material_window = QtGui.QDialog()
    material_window.setWindowTitle(__("Initials configuration"))
    ok_button = QtGui.QPushButton(__("Ok"))
    cancel_button = QtGui.QPushButton(__("Cancel"))
    target_mk = int(data['simobjects'][FreeCADGui.Selection.getSelection()[0].Name][0])

    # TODO: (Material management) Material related code
    def on_ok():
        guiutils.info_dialog(
            __("This will apply the material properties to all objects with mkbound = ") + str(target_mk))
        if has_material_selector.currentIndex() == 1:
            # Material default
            pass
        else:
            # Material custom
            pass

        materials_window.accept()

    def on_cancel():
        materials_window.reject()

    def on_material_change():
        pass

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    has_material_layout = QtGui.QHBoxLayout()
    has_material_label = QtGui.QLabel(__("Set material: "))
    has_material_label.setToolTip(__("Sets the current material."))
    has_material_selector = QtGui.QComboBox()
    has_material_selector.insertItems(0, ['Default', 'Custom'])
    has_material_selector.currentIndexChanged.connect(on_material_change)
    has_material_targetlabel = QtGui.QLabel(__("Target MKGroup: ") + str(target_mk))
    has_material_layout.addWidget(has_material_label)
    has_material_layout.addWidget(has_material_selector)
    has_material_layout.addStretch(1)
    has_material_layout.addWidget(has_material_targetlabel)

    material_props_group = QtGui.QGroupBox(__("Material properties"))

    buttons_layout = QtGui.QHBoxLayout()
    buttons_layout.addStretch(1)
    buttons_layout.addWidget(ok_button)
    buttons_layout.addWidget(cancel_button)

    material_window_layout = QtGui.QVBoxLayout()
    material_window_layout.addLayout(has_material_layout)
    material_window_layout.addWidget(material_props_group)
    material_window_layout.addLayout(buttons_layout)

    material_window.setLayout(material_window_layout)

    material_window.exec_()


# Property change widgets
mkgroup_prop = QtGui.QSpinBox()
objtype_prop = QtGui.QComboBox()
fillmode_prop = QtGui.QComboBox()
floatstate_prop = QtGui.QPushButton(__("Configure"))
initials_prop = QtGui.QPushButton(__("Configure"))
material_prop = QtGui.QPushButton(__("Material"))
# TODO: Enable material.
material_prop.setEnabled(False)
mkgroup_prop.setRange(0, 240)
objtype_prop.insertItems(0, ['Fluid', 'Bound'])
fillmode_prop.insertItems(1, ['Full', 'Solid', 'Face', 'Wire'])
mkgroup_prop.valueChanged.connect(mkgroup_change)
objtype_prop.currentIndexChanged.connect(objtype_change)
fillmode_prop.currentIndexChanged.connect(fillmode_change)
floatstate_prop.clicked.connect(floatstate_change)
initials_prop.clicked.connect(initials_change)
material_prop.clicked.connect(material_change)
property_table.setCellWidget(0, 1, mkgroup_prop)
property_table.setCellWidget(1, 1, objtype_prop)
property_table.setCellWidget(2, 1, fillmode_prop)
property_table.setCellWidget(3, 1, floatstate_prop)
property_table.setCellWidget(4, 1, initials_prop)
property_table.setCellWidget(5, 1, material_prop)

# Dock the widget to the left side of screen
fc_main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)

# By default all is hidden in the widget
property_table.hide()
addtodsph_button.hide()
removefromdsph_button.hide()


def add_object_to_sim(name=None):
    """Defines what happens when "Add object to sim" button is presseed.
    Takes the selection of FreeCAD and watches what type of thing it is adding"""
    if name is None:
        selection = FreeCADGui.Selection.getSelection()
    else:
        selection = list()
        selection.append(FreeCAD.ActiveDocument.getObject(name))

    for each in selection:
        if each.Name == "Case_Limits":
            continue
        if len(each.InList) > 0:
            continue
        if each.Name not in data['simobjects'].keys():
            if "fillbox" in each.Name.lower():
                mktoput = utils.get_first_mk_not_used("fluid", data)
                if not mktoput:
                    mktoput = 0
                data['simobjects'][each.Name] = [mktoput, 'fluid', 'full']
                data['mkfluidused'].append(mktoput)
            else:
                mktoput = utils.get_first_mk_not_used("bound", data)
                if not mktoput:
                    mktoput = 0
                data['simobjects'][each.Name] = [mktoput, 'bound', 'full']
                data['mkboundused'].append(mktoput)
            data['export_order'].append(each.Name)
    on_tree_item_selection_change()


def remove_object_from_sim():
    """Defines what happens when removing objects from
    the simulation"""
    selection = FreeCADGui.Selection.getSelection()
    for each in selection:
        if each.Name == "Case_Limits":
            continue
        if each.Name in data['export_order']:
            data['export_order'].remove(each.Name)
        data['simobjects'].pop(each.Name, None)
    on_tree_item_selection_change()


# Connects buttons to its functions
addtodsph_button.clicked.connect(add_object_to_sim)
removefromdsph_button.clicked.connect(remove_object_from_sim)

# Find treewidgets of freecad.
trees = list()
for item in fc_main_window.findChildren(QtGui.QTreeWidget):
    if item.objectName() != "DSPH Objects":
        trees.append(item)


def on_tree_item_selection_change():
    selection = FreeCADGui.Selection.getSelection()
    object_names = list()
    for each in FreeCAD.getDocument("DSPH_Case").Objects:
        object_names.append(each.Name)

    # Detect object deletion
    for key in data['simobjects'].keys():
        if key not in object_names:
            data['simobjects'].pop(key, None)
            data['export_order'].remove(key)

    addtodsph_button.setEnabled(True)
    if len(selection) > 0:
        if len(selection) > 1:
            # Multiple objects selected
            addtodsph_button.setText(__("Add all possible to DSPH Simulation"))
            property_table.hide()
            addtodsph_button.show()
            removefromdsph_button.hide()
            pass
        else:
            # One object selected
            if selection[0].Name == "Case_Limits":
                property_table.hide()
                addtodsph_button.hide()
                removefromdsph_button.hide()
                properties_widget.setMinimumHeight(100)
                properties_widget.setMaximumHeight(100)
                return
            if selection[0].Name in data['simobjects'].keys():
                # Show properties on table
                property_table.show()
                addtodsph_button.hide()
                removefromdsph_button.show()
                properties_widget.setMinimumHeight(300)
                properties_widget.setMaximumHeight(300)
                to_change = property_table.cellWidget(0, 1)
                to_change.setValue(data['simobjects'][selection[0].Name][0])

                to_change = property_table.cellWidget(1, 1)
                if selection[0].TypeId in temp_data['supported_types']:
                    to_change.setEnabled(True)
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        to_change.setCurrentIndex(0)
                        mkgroup_prop.setRange(0, 10)
                        mkgroup_label.setText("   " + __("MKFluid"))
                    elif data['simobjects'][selection[0].Name][1].lower() == "bound":
                        to_change.setCurrentIndex(1)
                        mkgroup_prop.setRange(0, 240)
                        mkgroup_label.setText("   " + __("MKBound"))
                elif selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower():
                    to_change.setEnabled(False)
                    to_change.setCurrentIndex(0)
                else:
                    to_change.setCurrentIndex(1)
                    to_change.setEnabled(False)

                to_change = property_table.cellWidget(2, 1)
                if selection[0].TypeId in temp_data['supported_types']:
                    to_change.setEnabled(True)
                    if data['simobjects'][selection[0].Name][2].lower() == "full":
                        to_change.setCurrentIndex(0)
                    elif data['simobjects'][selection[0].Name][2].lower() == "solid":
                        to_change.setCurrentIndex(1)
                    elif data['simobjects'][selection[0].Name][2].lower() == "face":
                        to_change.setCurrentIndex(2)
                    elif data['simobjects'][selection[0].Name][2].lower() == "wire":
                        to_change.setCurrentIndex(3)
                else:
                    to_change.setCurrentIndex(2)
                    to_change.setEnabled(False)

                # float state config
                to_change = property_table.cellWidget(3, 1)
                if selection[0].TypeId in temp_data['supported_types']:
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        to_change.setEnabled(False)
                    else:
                        to_change.setEnabled(True)
                elif selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower():
                    to_change.setEnabled(False)

                # initials restrictions
                to_change = property_table.cellWidget(4, 1)
                if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                    to_change.setEnabled(True)
                else:
                    to_change.setEnabled(False)
                if selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower():
                    to_change.setEnabled(True)

                    # initials restrictions
                    # to_change = property_table.cellWidget(5, 1)
                    # No restrictions for now

            else:
                properties_widget.setMinimumHeight(100)
                properties_widget.setMaximumHeight(100)
                if selection[0].InList == list():
                    # Show button to add to simulation
                    addtodsph_button.setText(__("Add to DSPH Simulation"))
                    property_table.hide()
                    addtodsph_button.show()
                    removefromdsph_button.hide()
                else:
                    addtodsph_button.setText(__("Can't add this object to the simulation"))
                    property_table.hide()
                    addtodsph_button.show()
                    addtodsph_button.setEnabled(False)
                    removefromdsph_button.hide()
    else:
        property_table.hide()
        addtodsph_button.hide()
        removefromdsph_button.hide()

    # Update dsph objects list
    objectlist_table.clear()
    objectlist_table.setEnabled(True)
    if len(data['export_order']) == 0:
        data['export_order'] = data['simobjects'].keys()
    # Substract one that represent case limits object
    objectlist_table.setRowCount(len(data['export_order']) - 1)
    objectlist_table.setHorizontalHeaderLabels([__('Object Name'), __('Order up'), __('Order down')])
    current_row = 0
    objects_with_parent = list()
    for key in data['export_order']:
        context_object = FreeCAD.getDocument("DSPH_Case").getObject(key)
        if not context_object:
            data['export_order'].remove(key)
            continue
        if context_object.InList != list():
            objects_with_parent.append(context_object.Name)
            continue
        if context_object.Name == "Case_Limits":
            continue
        objectlist_table.setCellWidget(current_row, 0, QtGui.QLabel("   " + context_object.Label))
        up = QtGui.QLabel("   " + __("Move Up"))
        up.setAlignment(QtCore.Qt.AlignLeft)
        up.setStyleSheet(
            "QLabel { background-color : rgb(225,225,225); color : black; margin: 2px;}"
            " QLabel:hover { background-color : rgb(215,215,255); color : black; }")

        down = QtGui.QLabel("   " + __("Move Down"))
        down.setAlignment(QtCore.Qt.AlignLeft)
        down.setStyleSheet(
            "QLabel { background-color : rgb(225,225,225); color : black; margin: 2px;}"
            " QLabel:hover { background-color : rgb(215,215,255); color : black; }")

        if current_row != 0:
            objectlist_table.setCellWidget(current_row, 1, up)
        if (current_row + 2) != len(data['export_order']):
            objectlist_table.setCellWidget(current_row, 2, down)

        current_row += 1
    for each in objects_with_parent:
        try:
            data['simobjects'].pop(each, None)
        except ValueError:
            # Not in list, probably because now is part of a compound object
            pass
        data['export_order'].remove(each)


for item in trees:
    item.itemSelectionChanged.connect(on_tree_item_selection_change)


def on_cell_click(row, column):
    new_order = list()
    if column == 1:
        # order up
        curr_elem = data['export_order'][row + 1]
        prev_elem = data['export_order'][row]

        data['export_order'].remove(curr_elem)

        for element in data['export_order']:
            if element == prev_elem:
                new_order.append(curr_elem)
            new_order.append(element)

        data['export_order'] = new_order
    elif column == 2:
        # order down
        curr_elem = data['export_order'][row + 1]
        next_elem = data['export_order'][row + 2]

        data['export_order'].remove(curr_elem)

        for element in data['export_order']:
            new_order.append(element)
            if element == next_elem:
                new_order.append(curr_elem)

        data['export_order'] = new_order
    else:
        # ignore
        pass
    on_tree_item_selection_change()


objectlist_table.cellClicked.connect(on_cell_click)


# Watch if no object is selected and prevent fillbox rotations
def selection_monitor():
    while True:
        # ensure everything is fine when objects are not selected
        if len(FreeCADGui.Selection.getSelection()) == 0:
            property_table.hide()
            addtodsph_button.hide()
            removefromdsph_button.hide()
        # watch fillbox rotations and prevent them
        try:
            for o in FreeCAD.getDocument("DSPH_Case").Objects:
                if o.TypeId == "App::DocumentObjectGroup" and "fillbox" in o.Name.lower():
                    for subelem in o.OutList:
                        if subelem.Placement.Rotation.Angle != 0.0:
                            subelem.Placement.Rotation.Angle = 0.0
                            utils.error(__("Can't change fillbox contents rotation!"))
        except NameError:
            # DSPH Case not opened, disable things
            guiutils.widget_state_config(widget_state_elements, "no case")
            time.sleep(2.0)
            continue
        time.sleep(0.5)


monitor_thread = threading.Thread(target=selection_monitor)
monitor_thread.start()

FreeCADGui.activateWorkbench("PartWorkbench")
utils.log(__("Done loading data."))
