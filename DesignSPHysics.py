#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Initializes a complete interface with DualSPHysics suite related operations.

It allows an user to create DualSPHysics compatible cases, automating a bunch of things needed to use them.

More info in http://design.sphysics.org/
"""

import FreeCAD
import FreeCADGui
import Draft
import glob
import os
import sys
import time
import pickle
import threading
import traceback
import subprocess
import shutil
import uuid

from PySide import QtGui, QtCore

# Fix FreeCAD not searching in the user-set macro folder.
try:
    from ds_modules import properties
    from ds_modules.properties import *
    from ds_modules import utils, guiutils, xmlimporter, dsphwidgets
    from ds_modules.utils import __
except:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ds_modules.properties import *
    from ds_modules import utils, guiutils, xmlimporter, dsphwidgets
    from ds_modules.utils import __

# Copyright (C) 2019
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
# EPHYTECH Environmental Physics Technologies
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
__copyright__ = "Copyright 2016-2017, DualSHPysics Team"
__credits__ = ["Andrés Vieira", "Lorena Docasar",
               "Alejandro Jacobo Cabrera Crespo", "Orlando García Feal"]
__license__ = "GPL"
__version__ = utils.VERSION
__maintainer__ = "Lorena Docasar"
__email__ = "docasarlorena@gmail.com"
__status__ = "Development"

# Print license at macro start
try:
    utils.print_license()
except EnvironmentError:
    guiutils.warning_dialog(
        __("LICENSE file could not be found. Are you sure you didn't delete it?")
    )

# Version check. This script is only compatible with FreeCAD 0.17 or higher
is_compatible = utils.is_compatible_version()
if not is_compatible:
    guiutils.error_dialog(
        __("This FreeCAD version is not compatible. Please update FreeCAD to version 0.17 or higher.")
    )
    raise EnvironmentError(
        __("This FreeCAD version is not compatible. Please update FreeCAD to version 0.17 or higher.")
    )


# Main data structure
# TODO: Big Change: Data structures should be an instance of a class like CaseData() and TempCaseData(), not a dict()
data = dict()  # Used to save on disk case parameters and related data
temp_data = dict()  # Used to store temporal useful items (like processes)
# Used to store widgets that will be disabled/enabled, so they are centralized
widget_state_elements = dict()

# Establishing references for the different elements that the script will use later.
fc_main_window = FreeCADGui.getMainWindow()  # FreeCAD main window

# TODO: Big Change: This should definetly be a custom class like DesignSPHysicsDock(QtGui.QDockWidget)
dsph_main_dock = QtGui.QDockWidget()  # DSPH main dock
# Scaffolding widget, only useful to apply to the dsph_dock widget
dsph_main_dock_scaff_widget = QtGui.QWidget()

# Executes the default data function the first time and merges results with current data structure.
default_data, default_temp_data = utils.get_default_data()
data.update(default_data)
temp_data.update(default_temp_data)

# The script needs only one document open, called DSPH_Case.
# This section tries to close all the current documents.
if utils.document_count() > 0:
    success = utils.prompt_close_all_documents()
    if not success:
        quit()

# If the script is executed even when a previous DSPH Dock is created it makes sure that it's deleted before.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, utils.__("DSPH Widget"))
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

# Creation of the DSPH Widget.
# Creates a widget with a series of layouts added, to apply to the DSPH dock at the end.
dsph_main_dock.setObjectName("DSPH Widget")
dsph_main_dock.setWindowTitle("{} {}".format(utils.APP_NAME, str(__version__)))
main_layout = QtGui.QVBoxLayout()  # Main Widget layout.  Vertical ordering

# Component layouts definition
logo_layout = QtGui.QHBoxLayout()
logo_layout.setSpacing(0)
logo_layout.setContentsMargins(0, 0, 0, 0)
intro_layout = QtGui.QVBoxLayout()

# DSPH dock first section.
# Includes constant definition, help, etc.
constants_label = QtGui.QLabel("<b>{}</b>".format(__("Configuration")))
constants_label.setWordWrap(True)
constants_button = QtGui.QPushButton(__("Define\nConstants"))
constants_button.setToolTip(__("Use this button to define case constants,\nsuch as gravity or fluid reference density."))


# Opens constant definition window on button click
def on_constants_button_pressed():
    constants_window = dsphwidgets.ConstantsDialog(data)
    # Constant definition window behaviour and general composing
    constants_window.resize(600, 400)
    constants_window.exec_()


constants_button.clicked.connect(on_constants_button_pressed)
widget_state_elements['constants_button'] = constants_button

# Help button that opens a help URL for DesignSPHysics
help_button = QtGui.QPushButton("Help")
help_button.setToolTip(__("Push this button to open a browser with help\non how to use this tool."))
help_button.clicked.connect(utils.open_help)

# Setup window button.
setup_button = QtGui.QPushButton(__("Setup\nPlugin"))
setup_button.setToolTip(__("Setup of the simulator executables"))
setup_button.clicked.connect(lambda: guiutils.def_setup_window(data))

# Execution parameters button.
execparams_button = QtGui.QPushButton(__("Execution\nParameters"))
execparams_button.setToolTip(__("Change execution parameters, such as\ntime of simulation, viscosity, etc."))

# Opens execution parameters window on button click
def on_execparams_button_presed():
    execparams_window = dsphwidgets.ExecutionParametersDialog(data)
    # Execution parameters window behaviour and general composing
    execparams_window.resize(800, 600)
    execparams_window.exec_()

execparams_button.clicked.connect(on_execparams_button_presed)
widget_state_elements['execparams_button'] = execparams_button

# Logo. Made from a label. Labels can have image as well as text.
logo_label = QtGui.QLabel()
logo_label.setPixmap(guiutils.get_icon(file_name="logo.png", return_only_path=True))


def on_dp_changed():
    """ DP Introduction.
    Changes the dp at the moment the user changes the text. """
    data['dp'] = float(dp_input.text())


# DP Introduction layout
dp_layout = QtGui.QHBoxLayout()
dp_label = QtGui.QLabel(__("Inter-particle distance: "))
dp_label.setToolTip(__("Lower DP to have more particles in the case."))
dp_input = QtGui.QLineEdit()
dp_input.setToolTip(__("Lower DP to have more particles in the case."))
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
ccsecondrow_layout = QtGui.QHBoxLayout()
ccthirdrow_layout = QtGui.QHBoxLayout()
ccfourthrow_layout = QtGui.QHBoxLayout()
casecontrols_label = QtGui.QLabel("<b>{}</b>".format(__("Pre-processing")))

# New Case button
casecontrols_bt_newdoc = QtGui.QToolButton()
casecontrols_bt_newdoc.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
casecontrols_bt_newdoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
casecontrols_bt_newdoc.setText("  {}".format(__("New\n  Case")))
casecontrols_bt_newdoc.setToolTip(utils.__("Creates a new case. \nThe opened documents will be closed."))
casecontrols_bt_newdoc.setIcon(guiutils.get_icon("new.png"))
casecontrols_bt_newdoc.setIconSize(QtCore.QSize(28, 28))
casecontrols_menu_newdoc = QtGui.QMenu()
casecontrols_menu_newdoc.addAction(guiutils.get_icon("new.png"), __("New"))
casecontrols_menu_newdoc.addAction(guiutils.get_icon("new.png"), __("Import FreeCAD Document"))
casecontrols_bt_newdoc.setMenu(casecontrols_menu_newdoc)
casecontrols_menu_newdoc.resize(60, 60)

# Save Case button and dropdown
casecontrols_bt_savedoc = QtGui.QToolButton()
casecontrols_bt_savedoc.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
casecontrols_bt_savedoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
casecontrols_bt_savedoc.setText("  {}".format(__("Save\n  Case")))
casecontrols_bt_savedoc.setToolTip(__("Saves the case."))
casecontrols_bt_savedoc.setIcon(guiutils.get_icon("save.png"))
casecontrols_bt_savedoc.setIconSize(QtCore.QSize(28, 28))
casecontrols_menu_savemenu = QtGui.QMenu()
# casecontrols_menu_savemenu.addAction(guiutils.get_icon("save.png"), __("Save and run GenCase"))
casecontrols_menu_savemenu.addAction(guiutils.get_icon("save.png"), __("Save as..."))
casecontrols_bt_savedoc.setMenu(casecontrols_menu_savemenu)
widget_state_elements['casecontrols_bt_savedoc'] = casecontrols_bt_savedoc

# Load Case button
casecontrols_bt_loaddoc = QtGui.QToolButton()
casecontrols_bt_loaddoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
casecontrols_bt_loaddoc.setText("  {}".format(__("Load\n  Case")))
casecontrols_bt_loaddoc.setToolTip(__("Loads a case from disk. All the current documents\nwill be closed."))
casecontrols_bt_loaddoc.setIcon(guiutils.get_icon("load.png"))
casecontrols_bt_loaddoc.setIconSize(QtCore.QSize(28, 28))

# Add fillbox button
casecontrols_bt_addfillbox = QtGui.QPushButton(__("Add fillbox"))
casecontrols_bt_addfillbox.setToolTip(__("Adds a FillBox. A FillBox is able to fill an empty space\nwithin "
                                         "limits of geometry and a maximum bounding\nbox placed by the user."))
casecontrols_bt_addfillbox.setEnabled(False)
widget_state_elements['casecontrols_bt_addfillbox'] = casecontrols_bt_addfillbox

# Import GEO button
casecontrols_bt_addgeo = QtGui.QPushButton("Import GEO")
casecontrols_bt_addgeo.setToolTip(__("Imports a GEO object with postprocessing. "
                                     "This way you can set the scale of the imported object."))
casecontrols_bt_addgeo.setEnabled(False)
widget_state_elements['casecontrols_bt_addgeo'] = casecontrols_bt_addgeo

# Import XML button
casecontrols_bt_importxml = QtGui.QPushButton(__("Import XML"))
casecontrols_bt_importxml.setToolTip(__("Imports an already created XML case from disk."))
casecontrols_bt_importxml.setEnabled(True)

# Case summary button
summary_bt = QtGui.QPushButton(__("Case summary"))
summary_bt.setToolTip(__("Shows a complete case summary with objects, "
                         "configurations and settings in a brief view."))
widget_state_elements['summary_bt'] = summary_bt
summary_bt.setEnabled(False)

# Toggle 3D/2D button
toggle3dbutton = QtGui.QPushButton(__("Change 3D/2D"))
toggle3dbutton.setToolTip(__("Changes the case mode between 2D and 3D mode, switching the Case Limits between a plane or a cube"))
widget_state_elements['toggle3dbutton'] = toggle3dbutton

# Damping add button
casecontrols_bt_special = QtGui.QPushButton(__("Special"))
casecontrols_bt_special.setToolTip(__("Special actions for the case."))
widget_state_elements['dampingbutton'] = casecontrols_bt_special

# Run GenCase button
rungencase_bt = QtGui.QPushButton(__("Run GenCase"))
rungencase_bt.setStyleSheet("QPushButton {font-weight: bold; }")
rungencase_bt.setToolTip(__("This pre-processing tool creates the initial state of the particles (position, velocity "
                            "and density) and defines the different SPH parameters for the simulation."))
rungencase_bt.setIcon(guiutils.get_icon("run_gencase.png"))
rungencase_bt.setIconSize(QtCore.QSize(12, 12))
widget_state_elements['rungencase_bt'] = rungencase_bt


def on_new_case(prompt=True):
    """ Defines what happens when new case is clicked. Closes all documents
        if possible and creates a FreeCAD document with Case Limits object. """

    # Closes all documents as there can only be one open.
    if utils.document_count() > 0:
        new_case_success = utils.prompt_close_all_documents(prompt)
        if not new_case_success:
            return

    # Creates a new document and merges default data to the current data structure.
    new_case_default_data, new_case_temp_data = utils.get_default_data()
    data.update(new_case_default_data)
    temp_data.update(new_case_temp_data)
    utils.create_dsph_document()
    guiutils.widget_state_config(widget_state_elements, "new case")
    data['simobjects']['Case_Limits'] = ["mkspecial", "typespecial", "fillspecial"]
    dp_input.setText(str(data["dp"]))

    # Forces call to item selection change function so all changes are taken into account
    on_tree_item_selection_change()


def on_new_from_freecad_document(prompt=True):
    """ Creates a new case based on an existing FreeCAD document.
    This is specially useful for CAD users that want to use existing geometry for DesignSPHysics. """
    file_name, _ = QtGui.QFileDialog().getOpenFileName(guiutils.get_fc_main_window(), "Select document to import", QtCore.QDir.homePath())

    if utils.document_count() > 0:
        new_case_success = utils.prompt_close_all_documents(prompt)
        if not new_case_success:
            return

    # Creates a new document and merges default data to the current data structure.
    new_case_default_data, new_case_temp_data = utils.get_default_data()
    data.update(new_case_default_data)
    temp_data.update(new_case_temp_data)
    utils.create_dsph_document_from_fcstd(file_name)
    guiutils.widget_state_config(widget_state_elements, "new case")
    data['simobjects']['Case_Limits'] = ["mkspecial", "typespecial", "fillspecial"]
    dp_input.setText(str(data["dp"]))

    # Forces call to item selection change function so all changes are taken into account
    on_tree_item_selection_change()


def on_save_case(save_as=None):
    """ Defines what happens when save case button is clicked.
    Saves a freecad scene definition, and a dump of dsph data for the case."""
    # Watch if save path is available.  Prompt the user if not.
    if (data['project_path'] == "" and data['project_name'] == "") or save_as:
        # noinspection PyArgumentList
        save_name, _ = QtGui.QFileDialog.getSaveFileName(dsph_main_dock, __("Save Case"), QtCore.QDir.homePath())
    else:
        save_name = data['project_path']

    # Check if there is any path, a blank one meant the user cancelled the save file dialog
    if save_name != '':
        project_name = save_name.split('/')[-1]
        # Watch if folder already exists or create it
        if not os.path.exists(save_name):
            os.makedirs(save_name)
        data['project_path'] = save_name
        data['project_name'] = project_name

        # Create out folder for the case
        if not os.path.exists("{}/{}_out".format(save_name, project_name)):
            os.makedirs("{}/{}_out".format(save_name, project_name))

        # Copy files from movements and change its paths to be inside the project.
        for key, value in data["motion_mks"].items():
            for movement in value:
                if isinstance(movement, properties.SpecialMovement):
                    if isinstance(movement.generator, properties.FileGen) or isinstance(movement.generator, properties.RotationFileGen):
                        filename = movement.generator.filename
                        utils.debug("Copying {} to {}".format(filename, save_name))

                        # Change directory to de case one, so if file path is already relative it copies it to the
                        # out folder
                        os.chdir(save_name)

                        try:
                            # Copy to project root
                            shutil.copy2(filename, save_name)
                        except IOError:
                            utils.error("Unable to copy {} into {}".format(filename, save_name))
                        except shutil.Error:
                            # Probably already copied the file.
                            pass

                        try:
                            # Copy to project out folder
                            shutil.copy2(filename, save_name + "/" + project_name + "_out")

                            movement.generator.filename = "{}".format(filename.split("/")[-1])
                        except IOError:
                            utils.error("Unable to copy {} into {}".format(filename, save_name))
                        except shutil.Error:
                            # Probably already copied the file.
                            pass

        # Copy files from Acceleration input and change paths to be inside the project folder.
        for aid in data['accinput'].acclist:
            filename = aid.datafile
            utils.debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))

            # Change directory to de case one, so if file path is already relative it copies it to the
            # out folder
            os.chdir(save_name)

            try:
                # Copy to project root
                shutil.copy2(filename, save_name)
            except IOError:
                utils.error("Unable to copy {} into {}".format(filename, save_name))
            except shutil.Error:
                # Probably already copied the file.
                pass

            try:
                # Copy to project out folder
                shutil.copy2(filename, save_name + "/" + project_name + "_out")

                aid.datafile = filename.split("/")[-1]

            except IOError:
                utils.error("Unable to copy {} into {}".format(filename, save_name))
            except shutil.Error:
                # Probably already copied the file.
                pass

        # Copy files from pistons and change paths to be inside the project folder.
        for key, piston in data["mlayerpistons"].items():
            if isinstance(piston, MLPiston1D):
                filename = piston.filevelx
                utils.debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                # Change directory to de case one, so if file path is already relative it copies it to the
                # out folder
                os.chdir(save_name)

                try:
                    # Copy to project root
                    shutil.copy2(filename, save_name)
                except IOError:
                    utils.error("Unable to copy {} into {}".format(filename, save_name))
                except shutil.Error:
                    # Probably already copied the file.
                    pass

                try:
                    # Copy to project out folder
                    shutil.copy2(filename, save_name + "/" + project_name + "_out")

                    piston.filevelx = filename.split("/")[-1]
                except IOError:
                    utils.error("Unable to copy {} into {}".format(filename, save_name))
                except shutil.Error:
                    # Probably already copied the file.
                    pass

            if isinstance(piston, MLPiston2D):
                veldata = piston.veldata
                for v in veldata:
                    filename = v.filevelx
                    utils.debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                    # Change directory to de case one, so if file path is already relative it copies it to the
                    # out folder
                    os.chdir(save_name)

                    try:
                        # Copy to project root
                        shutil.copy2(filename, save_name)
                    except IOError:
                        utils.error("Unable to copy {} into {}".format(filename, save_name))
                    except shutil.Error:
                        # Probably already copied the file.
                        pass

                    try:
                        # Copy to project out folder
                        shutil.copy2(filename, save_name + "/" + project_name + "_out")

                        v.filevelx = filename.split("/")[-1]
                    except IOError:
                        utils.error("Unable to copy {} into {}".format(filename, save_name))
                    except shutil.Error:
                        # Probably already copied the file.
                        pass

        # Copies files needed for RelaxationZones into the project folder and changes data paths to relative ones.
        if isinstance(data['relaxationzone'], RelaxationZoneFile):
            # Need to copy the abc_x*_y*.csv file series to the out folder
            filename = data['relaxationzone'].filesvel

            # Change directory to de case one, so if file path is already relative it copies it to the
            # out folder
            os.chdir(save_name)

            for f in glob.glob("{}*".format(filename)):
                utils.debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                try:
                    # Copy to project root
                    shutil.copy2(f, save_name)
                except IOError:
                    utils.error("Unable to copy {} into {}".format(filename, save_name))
                except shutil.Error:
                    # Probably already copied the file.
                    pass

                try:
                    # Copy to project out folder
                    shutil.copy2(f, save_name + "/" + project_name + "_out")

                    data['relaxationzone'].filesvel = filename.split("/")[-1]

                except IOError:
                    utils.error("Unable to copy {} into {}".format(filename, save_name))
                except shutil.Error:
                    # Probably already copied the file.
                    pass

        # Dumps all the case data to an XML file.
        utils.dump_to_xml(data, save_name)

        # Generate batch file in disk
        # TODO: Batch file generation needs to be updated.
        # Batch files need to have all the data they can have into it. Also, users should have options to include
        # different post-processing tools in the batch files. It is disabled for now because it's not really useful.

        # if (data['gencase_path'] == "") or (data['dsphysics_path'] == "") or (data['partvtk4_path'] == ""):
        #     utils.warning(
        #         __("Can't create executable bat file! One or more of the paths in plugin setup is not set"))
        # else:
        #     # Export batch files
        #     utils.batch_generator(
        #         full_path=save_name,
        #         case_name=project_name,
        #         gcpath=data['gencase_path'],
        #         dsphpath=data['dsphysics_path'],
        #         pvtkpath=data['partvtk4_path'],
        #         exec_params="-{} {}".format(
        #             str(ex_selector_combo.currentText()).lower(), data['additional_parameters']),
        #         lib_path='/'.join(data['gencase_path'].split('/')[:-1]))

        data['run_gen_case_first'] = False

        # Save data array on disk. It is saved as a binary file with Pickle.
        try:
            with open(save_name + "/casedata.dsphdata", 'wb') as picklefile:
                pickle.dump(data, picklefile, utils.PICKLE_PROTOCOL)
        except Exception as e:
            traceback.print_exc()
            guiutils.error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))

        utils.refocus_cwd()
    else:
        utils.log(__("Saving cancelled."))


def on_save_with_gencase():
    """ Saves data into disk and uses GenCase to generate the case files."""

    # Check if the project is saved, if no shows the following message
    if data['project_path'] == '':
        # Warning window about save_case
        gencase_warning_dialog = QtGui.QMessageBox()
        gencase_warning_dialog.setWindowTitle(__("Warning!"))
        gencase_warning_dialog.setText(__("You need save first!"))
        gencase_warning_dialog.setIcon(QtGui.QMessageBox.Warning)
        gencase_warning_dialog.exec_()

    # Save Case as usual so all the data needed for GenCase is on disk
    on_save_case()

    # Ensure the current working directory is the DesignSPHysics directory
    utils.refocus_cwd()

    # Use gencase if possible to generate the case final definition
    data['gencase_done'] = False
    if data['gencase_path'] != "":
        # Tries to spawn a process with GenCase to generate the case

        process = QtCore.QProcess(fc_main_window)
        gencase_full_path = os.getcwd() + "/" + data['gencase_path']
        process.start(gencase_full_path, [
            data['project_path'] + '/' + data['project_name'] + '_Def', data['project_path'] +
            '/' + data['project_name'] + '_out/' + data['project_name'],
            '-save:+all'
        ])

        process.waitForFinished()

        output = str(process.readAllStandardOutput())

        error_in_gen_case = False
        # If GenCase was successful, check for internal errors
        # This is done because a "clean" exit (return 0) of GenCase does not mean that all went correct.
        if str(process.exitCode()) == "0":
            try:
                total_particles_text = output[output.index("Total particles: "):output.index(" (bound=")]
                total_particles = int(total_particles_text[total_particles_text.index(": ") + 2:])
                data['total_particles'] = total_particles
                utils.log(__("Total number of particles exported: ") + str(total_particles))
                if total_particles < 300:
                    utils.warning(__("Are you sure all the parameters are set right? The number of particles is very low ({}). "
                                     "Lower the DP to increase number of particles").format(str(total_particles)))
                elif total_particles > 200000:
                    utils.warning(__("Number of particles is pretty high ({}) "
                                     "and it could take a lot of time to simulate.").format(str(total_particles)))
                data['gencase_done'] = True
                guiutils.widget_state_config(widget_state_elements, "gencase done")
                data["last_number_particles"] = int(total_particles)
                guiutils.gencase_completed_dialog(particle_count=total_particles,
                                                  detail_text=output.split("================================")[1],
                                                  data=data, temp_data=temp_data)
            except ValueError:
                # Not an expected result. GenCase had a not handled error
                error_in_gen_case = True

    # Check if there is any path, a blank one meant the user cancelled the save file dialog
    if data['project_path'] != '':
        # If for some reason GenCase failed
        if str(process.exitCode()) != "0" or error_in_gen_case:
            # Multiple possible causes. Let the user know
            gencase_out_file = open(data['project_path'] + '/' + data['project_name'] + '_out/' + data['project_name'] + ".out", "rb")
            gencase_failed_dialog = QtGui.QMessageBox()
            gencase_failed_dialog.setText(__("Error executing GenCase. Did you add objects to the case?. "
                                             "Another reason could be memory issues. View details for more info."))
            gencase_failed_dialog.setDetailedText(gencase_out_file.read().split("================================")[1])
            gencase_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
            gencase_out_file.close()
            gencase_failed_dialog.exec_()
            utils.warning(__("GenCase Failed."))

        # Save results again so all the data is updated if something changes.
        on_save_case()
    else:
        utils.log(__("Saving cancelled."))

    data['run_gen_case_first'] = True


def on_newdoc_menu(action):
    """ Handles the new document button and its dropdown items. """
    if __("New") in action.text():
        on_new_case()
    if __("Import FreeCAD Document") in action.text():
        on_new_from_freecad_document()


def on_save_menu(action):
    """ Handles the save button and its dropdown items. """
    if __("Save as...") in action.text():
        on_save_case(save_as=True)


def on_load_button():
    """ Defines load case button behaviour. This is made so errors can be detected and handled. """
    try:
        on_load_case()
    except ImportError:
        guiutils.error_dialog(__("There was an error loading the case"),
                              __("The case you are trying to load has some data that DesignSPHysics could not"
                                 " load.\n\nDid you make the case in a previous version?"))
        on_new_case(prompt=False)


def on_load_case():
    """Defines loading case mechanism.
    Load points to a dsphdata custom file, that stores all the relevant info.
    If FCStd file is not found the project is considered corrupt."""
    # noinspection PyArgumentList
    load_name, _ = QtGui.QFileDialog.getOpenFileName(dsph_main_dock, __("Load Case"), QtCore.QDir.homePath(), "casedata.dsphdata")
    if load_name == "":
        # User pressed cancel.  No path is selected.
        return

    # Check if FCStd file is in there.
    load_path_project_folder = "/".join(load_name.split("/")[:-1])
    if not os.path.isfile(load_path_project_folder + "/DSPH_Case.FCStd"):
        guiutils.error_dialog(__("DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."))
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
            try:
                load_disk_data = pickle.load(load_picklefile)
            except AttributeError:
                guiutils.error_dialog(__("There was an error trying to load the case. This can be due to the project being "
                                         "from another version or an error while saving the case."))
                on_new_case(prompt=False)
                return

        # Remove exec paths from loaded data if user have already correct ones.
        _, already_correct = utils.check_executables(data)
        if already_correct:
            [load_disk_data.pop(x, None) for x in
             ['gencase_path', 'dsphysics_path', 'partvtk4_path', 'floatinginfo_path', 'computeforces_path',
              'measuretool_path', 'isosurface_path', 'boundaryvtk_path']]

        # Update data structure with disk loaded one
        data.update(load_disk_data)
    except (EOFError, ValueError):
        guiutils.error_dialog(
            __("There was an error importing the case properties. You probably need to set them again."
               "\n\n"
               "This could be caused due to file corruption, "
               "caused by operating system based line endings or ends-of-file, or other related aspects."))

    # Fill some data
    dp_input.setText(str(data['dp']))
    data['project_path'] = load_path_project_folder
    data['project_name'] = load_path_project_folder.split("/")[-1]

    # Compatibility code. Transform content from previous version to this one.
    # Make FloatProperty compatible
    data['floating_mks'] = utils.float_list_to_float_property(data['floating_mks'])
    data['initials_mks'] = utils.initials_list_to_initials_property(data['initials_mks'])

    # Adapt widget state to case info
    guiutils.widget_state_config(widget_state_elements, "load base")
    if data['gencase_done']:
        guiutils.widget_state_config(widget_state_elements, "gencase done")
    else:
        guiutils.widget_state_config(widget_state_elements, "gencase not done")

    if data['simulation_done']:
        guiutils.widget_state_config(widget_state_elements, "simulation done")
    else:
        guiutils.widget_state_config(widget_state_elements, "simulation not done")

    # Check executable paths
    utils.refocus_cwd()
    data, correct_execs = utils.check_executables(data)
    if not correct_execs:
        guiutils.widget_state_config(widget_state_elements, "execs not correct")

    # Update FreeCAD case state
    on_tree_item_selection_change()


def on_add_fillbox():
    """ Add fillbox group. It consists
    in a group with 2 objects inside: a point and a box.
    The point represents the fill seed and the box sets
    the bounds for the filling"""
    fillbox_gp = FreeCAD.getDocument("DSPH_Case").addObject("App::DocumentObjectGroup", "FillBox")
    fillbox_point = FreeCAD.ActiveDocument.addObject("Part::Sphere", "FillPoint")
    fillbox_limits = FreeCAD.ActiveDocument.addObject("Part::Box", "FillLimit")
    fillbox_limits.Length = '1000 mm'
    fillbox_limits.Width = '1000 mm'
    fillbox_limits.Height = '1000 mm'
    fillbox_limits.ViewObject.DisplayMode = "Wireframe"
    fillbox_limits.ViewObject.LineColor = (0.00, 0.78, 1.00)
    fillbox_point.Radius.Value = 10
    fillbox_point.Placement.Base = FreeCAD.Vector(500, 500, 500)
    fillbox_point.ViewObject.ShapeColor = (0.00, 0.00, 0.00)
    fillbox_gp.addObject(fillbox_limits)
    fillbox_gp.addObject(fillbox_point)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def on_add_damping_zone():
    """ Adds a damping zone into the case. It consist on a solid line that rempresents the damping vector
    and a dashed line representing the overlimit. It can be adjusted in the damping property window
    or changing the lines itselves."""
    damping_group = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", "DampingZone")

    # Limits line
    points = [FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1000, 1000, 1000)]
    limits = Draft.makeWire(points, closed=False, face=False, support=None)
    Draft.autogroup(limits)
    limits.Label = "Limits"
    limitsv = FreeCADGui.ActiveDocument.getObject(limits.Name)
    limitsv.ShapeColor = (0.32, 1.00, 0.00)
    limitsv.LineColor = (0.32, 1.00, 0.00)
    limitsv.PointColor = (0.32, 1.00, 0.00)
    limitsv.EndArrow = True
    limitsv.ArrowSize = "10 mm"
    limitsv.ArrowType = "Dot"

    # Overlimit line
    points = [FreeCAD.Vector(*limits.End), FreeCAD.Vector(1580, 1577.35, 1577.35)]
    overlimit = Draft.makeWire(points, closed=False, face=False, support=None)
    Draft.autogroup(overlimit)
    overlimit.Label = "Overlimit"
    overlimitv = FreeCADGui.ActiveDocument.getObject(overlimit.Name)
    overlimitv.DrawStyle = "Dotted"
    overlimitv.ShapeColor = (0.32, 1.00, 0.00)
    overlimitv.LineColor = (0.32, 1.00, 0.00)
    overlimitv.PointColor = (0.32, 1.00, 0.00)
    overlimitv.EndArrow = True
    overlimitv.ArrowSize = "10 mm"
    overlimitv.ArrowType = "Dot"

    # Add the two lines to the group
    damping_group.addObject(limits)
    damping_group.addObject(overlimit)

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    # Save damping in the main data structure.
    data["damping"][damping_group.Name] = Damping()
    # Opens damping configuration window to tweak the added damping zone.
    dsphwidgets.DampingConfigDialog(data, damping_group.Name)


def on_add_inlet():
    # Opens Inlet/Outlet configuration window to configurate the inlet/outlet options.
    dsphwidgets.InletConfigDialog(data)


def on_add_chrono():
    # Opens chrono configuration window to configurate the chrono options.
    dsphwidgets.ChronoConfigDialog(data)


def on_add_stl():
    """ Add STL file. Opens a file opener and allows
    the user to set parameters for the import process """

    # TODO: Low priority: This Dialog should be implemented and designed as a class like AddSTLDialog(QtGui.QDialog)
    filedialog = QtGui.QFileDialog()

    # noinspection PyArgumentList
    file_name, _ = filedialog.getOpenFileName(fc_main_window, __("Select GEO to import"), QtCore.QDir.homePath(),
                                              "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk)")

    if len(file_name) <= 1:
        # User didn't select any files
        return

    # Defines import stl dialog
    geo_dialog = QtGui.QDialog()
    geo_dialog.setModal(True)
    geo_dialog.setWindowTitle(__("Import GEO"))
    geo_dialog_layout = QtGui.QVBoxLayout()
    geo_group = QtGui.QGroupBox(__("Import GEO options"))
    geo_group_layout = QtGui.QVBoxLayout()

    # STL File selection
    geo_file_layout = QtGui.QHBoxLayout()
    geo_file_label = QtGui.QLabel(__("GEO File: "))
    geo_file_path = QtGui.QLineEdit()
    geo_file_path.setText(file_name)
    geo_file_browse = QtGui.QPushButton(__("Browse"))
    [geo_file_layout.addWidget(x) for x in [geo_file_label, geo_file_path, geo_file_browse]]
    # END STL File selection

    # Scaling factor
    geo_scaling_layout = QtGui.QHBoxLayout()
    geo_scaling_label = QtGui.QLabel(__("Scaling factor: "))
    geo_scaling_x_l = QtGui.QLabel("X: ")
    geo_scaling_x_e = QtGui.QLineEdit("1")
    geo_scaling_y_l = QtGui.QLabel("Y: ")
    geo_scaling_y_e = QtGui.QLineEdit("1")
    geo_scaling_z_l = QtGui.QLabel("Z: ")
    geo_scaling_z_e = QtGui.QLineEdit("1")
    [geo_scaling_layout.addWidget(x) for x in [
        geo_scaling_label,
        geo_scaling_x_l,
        geo_scaling_x_e,
        geo_scaling_y_l,
        geo_scaling_y_e,
        geo_scaling_z_l,
        geo_scaling_z_e,
    ]]
    # END Scaling factor

    # Import object name
    geo_objname_layout = QtGui.QHBoxLayout()
    geo_objname_label = QtGui.QLabel(__("Import object name: "))
    geo_objname_text = QtGui.QLineEdit("ImportedGEO")
    [geo_objname_layout.addWidget(x) for x in [geo_objname_label, geo_objname_text]]
    # End object name

    # Add component layouts to group layout
    [geo_group_layout.addLayout(x) for x in [geo_file_layout, geo_scaling_layout, geo_objname_layout]]
    geo_group_layout.addStretch(1)
    geo_group.setLayout(geo_group_layout)

    # Create button layout
    geo_button_layout = QtGui.QHBoxLayout()
    geo_button_ok = QtGui.QPushButton(__("Import"))
    geo_button_cancel = QtGui.QPushButton(__("Cancel"))
    geo_button_cancel.clicked.connect(lambda: geo_dialog.reject())
    geo_button_layout.addStretch(1)
    geo_button_layout.addWidget(geo_button_cancel)
    geo_button_layout.addWidget(geo_button_ok)

    # Compose main window layout
    geo_dialog_layout.addWidget(geo_group)
    geo_dialog_layout.addStretch(1)
    geo_dialog_layout.addLayout(geo_button_layout)

    geo_dialog.setLayout(geo_dialog_layout)

    # STL Dialog function definition and connections
    def geo_ok_clicked():
        """ Defines ok button behaviour"""
        [geo_scaling_edit.setText(geo_scaling_edit.text().replace(",", ".")) for geo_scaling_edit in [
            geo_scaling_x_e,
            geo_scaling_y_e,
            geo_scaling_z_e
        ]]
        try:
            utils.import_geo(
                filename=str(geo_file_path.text()),
                scale_x=float(geo_scaling_x_e.text()),
                scale_y=float(geo_scaling_y_e.text()),
                scale_z=float(geo_scaling_z_e.text()),
                name=str(geo_objname_text.text()))
            geo_dialog.accept()
        except ValueError:
            utils.error(__("There was an error. Are you sure you wrote correct float values in the scaling factor?"))
            guiutils.error_dialog(__("There was an error. Are you sure you wrote correct float values in the sacaling factor?"))

    def geo_dialog_browse():
        """ Defines the browse button behaviour."""
        # noinspection PyArgumentList
        file_name_temp, _ = filedialog.getOpenFileName(fc_main_window, __("Select GEO to import"),
                                                       QtCore.QDir.homePath(), "STL Files (*.stl);;PLY Files "
                                                                               "(*.ply);;VTK Files (*.vtk)")
        geo_file_path.setText(file_name_temp)
        geo_dialog.raise_()
        geo_dialog.activateWindow()

    geo_button_cancel.clicked.connect(lambda: geo_dialog.reject())
    geo_button_ok.clicked.connect(geo_ok_clicked)
    geo_file_browse.clicked.connect(geo_dialog_browse)

    geo_dialog.exec_()


def on_import_xml():
    """ Imports an already created GenCase/DSPH compatible
    file and loads it in the scene. """

    guiutils.warning_dialog(__("This feature is experimental. It's meant to help to build a case importing bits from"
                               "previous, non DesignSPHysics code. This is not intended neither to import all objects "
                               "nor its properties."))

    # noinspection PyArgumentList
    import_name, _ = QtGui.QFileDialog.getOpenFileName(dsph_main_dock, __("Import XML"), QtCore.QDir.homePath(), "XML Files (*.xml)")
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
            FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 0))
        FreeCAD.ActiveDocument.getObject("Case_Limits").Length = str(limits_point_max[0] - limits_point_min[0]) + ' m'
        FreeCAD.ActiveDocument.getObject("Case_Limits").Width = str(limits_point_max[1] - limits_point_min[1]) + ' m'
        FreeCAD.ActiveDocument.getObject("Case_Limits").Height = str(limits_point_max[2] - limits_point_min[2]) + ' m'

        # Merges and updates current data with the imported one.
        data.update(config)

        # Add results to DSPH objects
        for key, value in objects.items():
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
    guiutils.info_dialog(__("Importing successful. Note that some objects may not be automatically added to the case, "
                            "and other may not have its properties correctly applied."))


def on_summary():
    """ Handles Case Summary button """
    guiutils.case_summary(data)


def on_2d_toggle():
    """ Handles Toggle 3D/2D Button. Changes the Case Limits object accordingly. """
    if utils.valid_document_environment():
        if data['3dmode']:
            # Change to 2D

            # TODO: Low-priority: This dialog should be implemented as a class like 2DModeConfig(QtGui.QDialog)
            y_pos_2d_window = QtGui.QDialog()
            y_pos_2d_window.setWindowTitle(__("Set Y position"))

            ok_button = QtGui.QPushButton(__("Ok"))
            cancel_button = QtGui.QPushButton(__("Cancel"))

            # Ok Button handler
            def on_ok():
                temp_data['3d_width'] = utils.get_fc_object('Case_Limits').Width.Value

                try:
                    utils.get_fc_object('Case_Limits').Placement.Base.y = float(y2_pos_input.text())
                except ValueError:
                    guiutils.error_dialog(__("The Y position that was inserted is not valid."))

                utils.get_fc_object('Case_Limits').Width.Value = utils.WIDTH_2D
                guiutils.get_fc_view_object('Case_Limits').DisplayMode = 'Flat Lines'
                guiutils.get_fc_view_object('Case_Limits').ShapeColor = (1.00, 0.00, 0.00)
                guiutils.get_fc_view_object('Case_Limits').Transparency = 90
                # Toggle 3D Mode and change name
                data['3dmode'] = not data['3dmode']
                utils.get_fc_object('Case_Limits').Label = "Case Limits (3D)" if data['3dmode'] else "Case Limits (2D)"
                y_pos_2d_window.accept()

            # Cancel Button handler
            def on_cancel():
                y_pos_2d_window.reject()

            ok_button.clicked.connect(on_ok)
            cancel_button.clicked.connect(on_cancel)

            # Button layout definition
            y2d_button_layout = QtGui.QHBoxLayout()
            y2d_button_layout.addStretch(1)
            y2d_button_layout.addWidget(ok_button)
            y2d_button_layout.addWidget(cancel_button)

            y_pos_intro_layout = QtGui.QHBoxLayout()
            y_pos_intro_label = QtGui.QLabel(__("New Y position (mm): "))
            y2_pos_input = QtGui.QLineEdit()
            y2_pos_input.setText(str(utils.get_fc_object('Case_Limits').Placement.Base.y))
            y_pos_intro_layout.addWidget(y_pos_intro_label)
            y_pos_intro_layout.addWidget(y2_pos_input)

            y_pos_2d_layout = QtGui.QVBoxLayout()
            y_pos_2d_layout.addLayout(y_pos_intro_layout)
            y_pos_2d_layout.addStretch(1)
            y_pos_2d_layout.addLayout(y2d_button_layout)

            y_pos_2d_window.setLayout(y_pos_2d_layout)
            y_pos_2d_window.exec_()
        else:
            # Change to 3D
            try:
                # Try to restore original Width.
                utils.get_fc_object('Case_Limits').Width = temp_data['3d_width']
            except:
                # If its not saved just set it same as Length
                utils.get_fc_object('Case_Limits').Width = utils.get_fc_object('Case_Limits').Length

            guiutils.get_fc_view_object('Case_Limits').DisplayMode = 'Wireframe'
            guiutils.get_fc_view_object('Case_Limits').ShapeColor = (0.80, 0.80, 0.80)
            guiutils.get_fc_view_object('Case_Limits').Transparency = 0
            # Toggle 3D Mode and change name
            data['3dmode'] = not data['3dmode']
            utils.get_fc_object('Case_Limits').Label = "Case Limits (3D)" if data['3dmode'] else "Case Limits (2D)"
    else:
        utils.error("Not a valid case environment")


def on_special_button():
    """ Spawns a dialog with special options. This is only a selector """

    # TODO: Low-priority: This should be implemented in a class like SpecialOptionsSelector(QtGui.QDialog)
    sp_window = QtGui.QDialog()
    sp_window.setWindowTitle(__("Special"))
    sp_window.setMinimumWidth(200)
    sp_window_layout = QtGui.QVBoxLayout()

    sp_damping_button = QtGui.QPushButton(__("Damping"))
    sp_inlet_button = QtGui.QPushButton(__("Inlet/Outlet"))
    sp_inlet_button.setEnabled(False)
    sp_chrono_button = QtGui.QPushButton(__("Coupling CHRONO"))
    #sp_chrono_button.setEnabled(False)
    sp_multilayeredmb_button = QtGui.QPushButton(__("Multi-layered Piston"))
    sp_multilayeredmb_menu = QtGui.QMenu()
    sp_multilayeredmb_menu.addAction(__("1 Dimension"))
    sp_multilayeredmb_menu.addAction(__("2 Dimensions"))
    sp_multilayeredmb_button.setMenu(sp_multilayeredmb_menu)

    sp_relaxationzone_button = QtGui.QPushButton(__("Relaxation Zone"))
    sp_relaxationzone_menu = QtGui.QMenu()
    sp_relaxationzone_menu.addAction(__("Regular waves"))
    sp_relaxationzone_menu.addAction(__("Irregular waves"))
    sp_relaxationzone_menu.addAction(__("External Input"))
    sp_relaxationzone_menu.addAction(__("Uniform velocity"))
    sp_relaxationzone_button.setMenu(sp_relaxationzone_menu)

    sp_accinput_button = QtGui.QPushButton(__("Acceleration Inputs"))

    def on_damping_option():
        """ Defines damping button behaviour"""
        on_add_damping_zone()
        sp_window.accept()

    def on_inlet_option():
        """ Defines Inlet/Outlet behaviour """
        on_add_inlet()
        sp_window.accept()

    def on_chrono_option():
        """ Defines Coupling CHRONO behaviour"""
        on_add_chrono()
        sp_window.accept()

    def on_multilayeredmb_menu(action):
        """ Defines MLPiston menu behaviour"""
        # Get currently selected object
        try:
            selection = FreeCADGui.Selection.getSelection()[0]
        except IndexError:
            guiutils.error_dialog(__("You must select an object"))
            return

        # Check if object is in the simulation
        if selection.Name not in data['simobjects'].keys():
            guiutils.error_dialog(__("The selected object must be added to the simulation"))
            return

        # Check if it is fluid and warn the user.
        if "fluid" in data["simobjects"][selection.Name][1].lower():
            guiutils.error_dialog(__("You can't apply a piston movement to a fluid.\n"
                                     "Please select a boundary and try again"))
            return

        # Get selection mk
        selection_mk = data["simobjects"][selection.Name][0]

        # Check that this mk has no other motions applied
        if selection_mk in data['motion_mks'].keys():
            # MK has motions applied. Warn the user and delete them
            motion_delete_warning = guiutils.ok_cancel_dialog(
                utils.APP_NAME,
                __("This mk already has motions applied. "
                   "Setting a Multi-layered piston will delete all of its movement. "
                   "Are you sure?")
            )
            if motion_delete_warning == QtGui.QMessageBox.Cancel:
                return
            else:
                data['motion_mks'].pop(selection_mk, None)

        # 1D or 2D piston
        if __("1 Dimension") in action.text():
            # Check that there's no other multilayered piston for this mk
            if selection_mk in data['mlayerpistons'].keys():
                if not isinstance(data['mlayerpistons'][selection_mk], MLPiston1D):
                    overwrite_warn = guiutils.ok_cancel_dialog(
                        utils.APP_NAME,
                        __("You're about to overwrite a previous coupling movement for this mk. Are you sure?")
                    )
                    if overwrite_warn == QtGui.QMessageBox.Cancel:
                        return

            if selection_mk in data['mlayerpistons'].keys() and isinstance(data['mlayerpistons'][selection_mk], MLPiston1D):
                config_dialog = dsphwidgets.MLPiston1DConfigDialog(
                    selection_mk, data['mlayerpistons'][selection_mk]
                )
            else:
                config_dialog = dsphwidgets.MLPiston1DConfigDialog(
                    selection_mk, None
                )

            if config_dialog.result() == QtGui.QDialog.Accepted:
                guiutils.warning_dialog(__("All changes have been applied for mk = {}").format(selection_mk))

            if config_dialog.mlpiston1d is None:
                data['mlayerpistons'].pop(selection_mk, None)
            else:
                data['mlayerpistons'][selection_mk] = config_dialog.mlpiston1d

        if __("2 Dimensions") in action.text():
            # Check that there's no other multilayered piston for this mk
            if selection_mk in data['mlayerpistons'].keys():
                if not isinstance(data['mlayerpistons'][selection_mk], MLPiston2D):
                    overwrite_warn = guiutils.ok_cancel_dialog(
                        utils.APP_NAME,
                        __("You're about to overwrite a previous coupling movement for this mk. Are you sure?")
                    )
                    if overwrite_warn == QtGui.QMessageBox.Cancel:
                        return

            if selection_mk in data['mlayerpistons'].keys() and isinstance(data['mlayerpistons'][selection_mk],
                                                                           MLPiston2D):
                config_dialog = dsphwidgets.MLPiston2DConfigDialog(
                    selection_mk, data['mlayerpistons'][selection_mk]
                )
            else:
                config_dialog = dsphwidgets.MLPiston2DConfigDialog(
                    selection_mk, None
                )

            if config_dialog.result() == QtGui.QDialog.Accepted:
                guiutils.warning_dialog(__("All changes have been applied for mk = {}").format(selection_mk))

            if config_dialog.mlpiston2d is None:
                data['mlayerpistons'].pop(selection_mk, None)
            else:
                data['mlayerpistons'][selection_mk] = config_dialog.mlpiston2d

        sp_window.accept()

    def on_relaxationzone_menu(action):
        """ Defines Relaxation Zone menu behaviour."""

        # Check which type of relaxationzone it is
        if action.text() == __("Regular waves"):
            if data['relaxationzone'] is not None:
                if not isinstance(data['relaxationzone'], RelaxationZoneRegular):
                    overwrite_warn = guiutils.ok_cancel_dialog(
                        __("Relaxation Zone"),
                        __("There's already another type of Relaxation Zone defined. "
                           "Continuing will overwrite it. Are you sure?")
                    )
                    if overwrite_warn == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        data['relaxationzone'] = RelaxationZoneRegular()

            config_dialog = dsphwidgets.RelaxationZoneRegularConfigDialog(data['relaxationzone'])

            # Set the relaxation zone. Can be an object or be None
            data['relaxationzone'] = config_dialog.relaxationzone
        if action.text() == __("Irregular waves"):
            if data['relaxationzone'] is not None:
                if not isinstance(data['relaxationzone'], RelaxationZoneIrregular):
                    overwrite_warn = guiutils.ok_cancel_dialog(
                        __("Relaxation Zone"),
                        __("There's already another type of Relaxation Zone defined. "
                           "Continuing will overwrite it. Are you sure?")
                    )
                    if overwrite_warn == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        data['relaxationzone'] = RelaxationZoneIrregular()

            config_dialog = dsphwidgets.RelaxationZoneIrregularConfigDialog(
                data['relaxationzone']
            )

            # Set the relaxation zone. Can be an object or be None
            data['relaxationzone'] = config_dialog.relaxationzone
        if action.text() == __("External Input"):
            if data['relaxationzone'] is not None:
                if not isinstance(data['relaxationzone'], RelaxationZoneFile):
                    overwrite_warn = guiutils.ok_cancel_dialog(
                        __("Relaxation Zone"),
                        __("There's already another type of "
                           "Relaxation Zone defined. "
                           "Continuing will overwrite it. Are you sure?")
                    )
                    if overwrite_warn == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        data['relaxationzone'] = RelaxationZoneFile()

            config_dialog = dsphwidgets.RelaxationZoneFileConfigDialog(data['relaxationzone'])

            # Set the relaxation zone. Can be an object or be None
            data['relaxationzone'] = config_dialog.relaxationzone

        if action.text() == __("Uniform velocity"):
            if data['relaxationzone'] is not None:
                if not isinstance(data['relaxationzone'], RelaxationZoneUniform):
                    overwrite_warn = guiutils.ok_cancel_dialog(
                        __("Relaxation Zone"),
                        __("There's already another type of Relaxation Zone "
                           "defined. Continuing will overwrite it. "
                           "Are you sure?")
                    )
                    if overwrite_warn == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        data['relaxationzone'] = RelaxationZoneUniform()

            config_dialog = dsphwidgets.RelaxationZoneUniformConfigDialog(data['relaxationzone'])

            # Set the relaxation zone. Can be an object or be None
            data['relaxationzone'] = config_dialog.relaxationzone

        sp_window.accept()

    def on_accinput_button():
        """ Acceleration input button behaviour."""
        accinput_dialog = dsphwidgets.AccelerationInputDialog(data['accinput'])
        result = accinput_dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            data['accinput'] = accinput_dialog.get_result()

    sp_damping_button.clicked.connect(on_damping_option)
    sp_inlet_button.clicked.connect(on_inlet_option)
    sp_chrono_button.clicked.connect(on_chrono_option)
    sp_multilayeredmb_menu.triggered.connect(on_multilayeredmb_menu)
    sp_relaxationzone_menu.triggered.connect(on_relaxationzone_menu)
    sp_accinput_button.clicked.connect(on_accinput_button)

    [sp_window_layout.addWidget(x) for x in [
        sp_damping_button,
        sp_inlet_button,
        sp_chrono_button,
        sp_multilayeredmb_button,
        sp_relaxationzone_button,
        sp_accinput_button
    ]]
    sp_window.setLayout(sp_window_layout)
    sp_window.exec_()


# Connect case control buttons to respective handlers
casecontrols_bt_newdoc.clicked.connect(on_new_case)
casecontrols_bt_savedoc.clicked.connect(on_save_case)
rungencase_bt.clicked.connect(on_save_with_gencase)
casecontrols_menu_newdoc.triggered.connect(on_newdoc_menu)
casecontrols_menu_savemenu.triggered.connect(on_save_menu)
casecontrols_bt_loaddoc.clicked.connect(on_load_button)
casecontrols_bt_addfillbox.clicked.connect(on_add_fillbox)
casecontrols_bt_addgeo.clicked.connect(on_add_stl)
casecontrols_bt_importxml.clicked.connect(on_import_xml)
summary_bt.clicked.connect(on_summary)
toggle3dbutton.clicked.connect(on_2d_toggle)
casecontrols_bt_special.clicked.connect(on_special_button)

# Defines case control scaffolding
cclabel_layout.addWidget(casecontrols_label)
ccfilebuttons_layout.addWidget(casecontrols_bt_newdoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_savedoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_loaddoc)
ccsecondrow_layout.addWidget(summary_bt)
ccsecondrow_layout.addWidget(toggle3dbutton)
ccthirdrow_layout.addWidget(casecontrols_bt_addfillbox)
ccthirdrow_layout.addWidget(casecontrols_bt_addgeo)
ccthirdrow_layout.addWidget(casecontrols_bt_importxml)
ccfourthrow_layout.addWidget(casecontrols_bt_special)
ccfourthrow_layout.addWidget(rungencase_bt)

cc_layout.addLayout(cclabel_layout)
cc_layout.addLayout(ccfilebuttons_layout)
cc_layout.addLayout(ccthirdrow_layout)
cc_layout.addLayout(ccsecondrow_layout)
cc_layout.addLayout(ccfourthrow_layout)


def on_ex_simulate():
    """ Defines what happens on simulation button press.
    It shows the run window and starts a background process
    with dualsphysics running. Updates the window with useful info."""

    if data['run_gen_case_first'] != True:
        # Warning window about save_case
        run_warning_dialog = QtGui.QMessageBox()
        run_warning_dialog.setWindowTitle(__("Warning!"))
        run_warning_dialog.setText(__("It is necessary that you run Run GenCase again, otherwise, maybe the results "
                                      "obtained may not be as expected..."))
        run_warning_dialog.setIcon(QtGui.QMessageBox.Warning)
        run_warning_dialog.exec_()

    run_dialog = dsphwidgets.RunDialog()
    run_dialog.run_progbar_bar.setValue(0)
    data['simulation_done'] = False
    guiutils.widget_state_config(widget_state_elements, "sim start")
    run_dialog.run_button_cancel.setText(__("Cancel Simulation"))
    run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
    run_dialog.run_group_label_case.setText(__("Case name: ") + data['project_name'])
    run_dialog.run_group_label_proc.setText(__("Simulation processor: ") + str(ex_selector_combo.currentText()))
    run_dialog.run_group_label_part.setText(__("Number of particles: ") + str(data['total_particles']))
    run_dialog.run_group_label_partsout.setText(__("Total particles out: ") + "0")
    run_dialog.run_group_label_eta.setText(__("Estimated time to complete simulation: ") + __("Calculating..."))

    # Cancel button handler
    def on_cancel():
        utils.log(__("Stopping simulation"))
        if temp_data['current_process'] is not None:
            temp_data['current_process'].kill()
        run_dialog.hide()
        run_dialog.run_details.hide()
        data['simulation_done'] = False
        guiutils.widget_state_config(widget_state_elements, "sim cancel")

    run_dialog.run_button_cancel.clicked.connect(on_cancel)

    def on_details():
        """ Details button handler. Opens and closes the details pane on the execution window."""
        if run_dialog.run_details.isVisible():
            utils.debug('Hiding details pane on execution')
            run_dialog.run_details.hide()
        else:
            utils.debug('Showing details pane on execution')
            run_dialog.run_details.show()
            run_dialog.run_details.move(run_dialog.x() - run_dialog.run_details.width() - 15, run_dialog.y())

    # Ensure run button has no connections
    try:
        run_dialog.run_button_details.clicked.disconnect()
    except RuntimeError:
        pass

    run_dialog.run_button_details.clicked.connect(on_details)

    # Launch simulation and watch filesystem to monitor simulation
    filelist = [f for f in os.listdir(data['project_path'] + '/' + data['project_name'] + "_out/") if f.startswith("Part")]
    for f in filelist:
        os.remove(data['project_path'] + '/' + data['project_name'] + "_out/" + f)

    def on_dsph_sim_finished(exit_code):
        """ Simulation finish handler. Defines what happens when the process finishes."""

        # Reads output and completes the progress bar
        output = temp_data['current_process'].readAllStandardOutput()
        run_dialog.run_details_text.setText(str(output))
        run_dialog.run_details_text.moveCursor(QtGui.QTextCursor.End)
        run_dialog.run_watcher.removePath(data['project_path'] + '/' + data['project_name'] + "_out/")
        run_dialog.setWindowTitle(__("DualSPHysics Simulation: Complete"))
        run_dialog.run_progbar_bar.setValue(100)
        run_dialog.run_button_cancel.setText(__("Close"))

        if exit_code == 0:
            # Simulation went correctly
            data['simulation_done'] = True
            guiutils.widget_state_config(widget_state_elements, "sim finished")
        else:
            # In case of an error
            if "exception" in str(output).lower():
                utils.error(__("Exception in execution."))
                run_dialog.setWindowTitle(__("DualSPHysics Simulation: Error"))
                run_dialog.run_progbar_bar.setValue(0)
                run_dialog.hide()
                guiutils.widget_state_config(widget_state_elements, "sim error")
                execution_error_dialog = QtGui.QMessageBox()
                execution_error_dialog.setText(__("An error occurred during execution. Make sure that parameters exist and are properly defined. "
                                                  "You can also check your execution device (update the driver of your GPU). "
                                                  "Read the details for more information."))
                execution_error_dialog.setDetailedText(str(output).split("================================")[1])
                execution_error_dialog.setIcon(QtGui.QMessageBox.Critical)
                execution_error_dialog.exec_()

    # Launches a QProcess in background
    process = QtCore.QProcess(run_dialog)
    process.finished.connect(on_dsph_sim_finished)
    temp_data['current_process'] = process
    static_params_exe = [
        data['project_path'] + '/' + data['project_name'] + "_out/" +
        data['project_name'], data['project_path'] +
        '/' + data['project_name'] + "_out/",
        "-svres", "-" + str(ex_selector_combo.currentText()).lower()
    ]
    if len(data['additional_parameters']) < 2:
        additional_params_ex = list()
    else:
        additional_params_ex = data['additional_parameters'].split(" ")
    final_params_ex = static_params_exe + additional_params_ex
    temp_data['current_process'].start(data['dsphysics_path'], final_params_ex)

    def on_fs_change():
        """ Executed each time the filesystem changes. This updates the percentage of the simulation and its
        details."""
        run_file_data = ''
        try:
            with open(data['project_path'] + '/' + data['project_name'] + "_out/Run.out", "r") as run_file:
                run_file_data = run_file.readlines()
        except Exception as e:
            pass

        # Fill details window
        run_dialog.run_details_text.setText("".join(run_file_data))
        run_dialog.run_details_text.moveCursor(QtGui.QTextCursor.End)

        # Set percentage scale based on timemax
        for l in run_file_data:
            if data['timemax'] == -1:
                if "TimeMax=" in l:
                    data['timemax'] = float(l.split("=")[1])

        # Check how much of the simulation is done and fill estimated time
        if "Part_" in run_file_data[-1]:
            last_line_parttime = run_file_data[-1].split(".")
            if "Part_" in last_line_parttime[0]:
                current_value = (float(last_line_parttime[0].split(" ")[-1] + "." + last_line_parttime[1][:2]) * float(100)) / float(data['timemax'])
                run_dialog.run_progbar_bar.setValue(current_value)
                run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format(
                    str(format(current_value, ".2f"))))

            last_line_time = run_file_data[-1].split("  ")[-1]
            if ("===" not in last_line_time) and ("CellDiv" not in last_line_time) and ("memory" not in last_line_time) and ("-" in last_line_time):
                # Update time field
                try:
                    run_dialog.run_group_label_eta.setText(__("Estimated time to complete simulation: ") + last_line_time)
                except RuntimeError:
                    run_group_label_eta.setText(__("Estimated time to complete simulation: ") + "Calculating...")
        elif "Particles out:" in run_file_data[-1]:
            totalpartsout = int(run_file_data[-1].split("(total: ")[1].split(")")[0])
            data['total_particles_out'] = totalpartsout
            run_dialog.run_group_label_partsout.setText(__("Total particles out: {}").format(str(data['total_particles_out'])))

    # Set filesystem watcher to the out directory.
    run_dialog.run_watcher.addPath(data['project_path'] + '/' + data['project_name'] + "_out/")
    run_dialog.run_watcher.directoryChanged.connect(on_fs_change)

    data['run_gen_case_first'] = False

    # Handle error on simulation start
    if temp_data['current_process'].state() == QtCore.QProcess.NotRunning:
        # Probably error happened.
        run_watcher.removePath(data['project_path'] + '/' + data['project_name'] + "_out/")
        temp_data['current_process'] = ""
        exec_not_correct_dialog = QtGui.QMessageBox()
        exec_not_correct_dialog.setText(__("Error on simulation start. Is the path of DualSPHysics correctly placed?"))
        exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Critical)
        exec_not_correct_dialog.exec_()
    else:
        run_dialog.show()


def on_additional_parameters():
    """ Handles additional parameters button for execution """
    # TODO: This should be a custom implementation in a class like AdditionalParametersDialog(QtGui.QDialog)
    additional_parameters_window = QtGui.QDialog()
    additional_parameters_window.setWindowTitle(__("Additional parameters"))

    ok_button = QtGui.QPushButton(__("Ok"))
    cancel_button = QtGui.QPushButton(__("Cancel"))

    def on_ok():
        """ OK Button handler."""
        data['additional_parameters'] = export_params.text()
        additional_parameters_window.accept()

    def on_cancel():
        """ Cancel button handler."""
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

    additional_parameters_window.setLayout(additional_parameters_layout)
    additional_parameters_window.exec_()


# Execution section scaffolding
ex_layout = QtGui.QVBoxLayout()
ex_label = QtGui.QLabel("<b>" + __("Simulation control") + "</b> ")
ex_label.setWordWrap(True)

# Combobox for processor selection
ex_selector_combo = QtGui.QComboBox()
ex_selector_combo.addItem("CPU")
ex_selector_combo.addItem("GPU")
widget_state_elements['ex_selector_combo'] = ex_selector_combo

# Simulate case button
ex_button = QtGui.QPushButton(__("Run"))
ex_button.setStyleSheet("QPushButton {font-weight: bold; }")
ex_button.setToolTip(__("Starts the case simulation. From the simulation\n"
                        "window you can see the current progress and\n"
                        "useful information."))
ex_button.setIcon(guiutils.get_icon("run.png"))
ex_button.setIconSize(QtCore.QSize(12, 12))
ex_button.clicked.connect(on_ex_simulate)
widget_state_elements['ex_button'] = ex_button

# Additional parameters button
ex_additional = QtGui.QPushButton(__("Additional parameters"))
ex_additional.setToolTip("__(Sets simulation additional parameters for execution.)")
ex_additional.clicked.connect(on_additional_parameters)
widget_state_elements['ex_additional'] = ex_additional

ex_button_layout = QtGui.QHBoxLayout()
ex_button_layout.addWidget(ex_button)
ex_button_layout.addWidget(ex_selector_combo)
ex_button_layout.addWidget(ex_additional)

ex_layout.addWidget(ex_label)

ex_layout.addLayout(ex_button_layout)

# Defines export window dialog.
# This dialog is used in each <tool>_export function as a generic progress information
# TODO: This should be a custom implementation on a class like ExporProgressDialog(QtGui.QDialog)
export_dialog = QtGui.QDialog()

export_dialog.setModal(False)
export_dialog.setWindowTitle(__("Exporting: {}%").format("0"))
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


def partvtk_export(export_parameters):
    """ Export VTK button behaviour.
    Launches a process while disabling the button. """
    guiutils.widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_partvtk_button'].setText("Exporting...")

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
            widget_state_elements['post_proc_partvtk_button'].setText(
                __("PartVTK"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    # PartVTK export finish handler
    def on_export_finished(exit_code):
        widget_state_elements['post_proc_partvtk_button'].setText(__("PartVTK"))
        guiutils.widget_state_config(widget_state_elements, "export finished")

        export_dialog.hide()

        if exit_code == 0:
            # Exported correctly
            temp_data['current_info_dialog'] = dsphwidgets.InfoDialog(
                info_text=__("PartVTK finished successfully"),
                detailed_text=temp_data['current_output']
            )
        else:
            guiutils.error_dialog(
                __("There was an error on the post-processing. Show details to view the errors."),
                detailed_text=temp_data['current_output']
            )

        # Bit of code that tries to open ParaView if the option was selected.
        if export_parameters['open_paraview']:
            formats = {0: "vtk", 1: "csv", 2: "asc"}
            subprocess.Popen(
                [
                    data['paraview_path'],
                    "--data={}\\{}_..{}".format(data['project_path'] + '\\' + data['project_name'] + '_out',
                                                export_parameters['file_name'], formats[export_parameters['save_mode']])
                ],
                stdout=subprocess.PIPE)

    temp_data['current_output'] = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    # Set save mode according to the dropdown menu
    save_mode = '-savevtk '
    if export_parameters['save_mode'] == 0:
        save_mode = '-savevtk '
    elif export_parameters['save_mode'] == 1:
        save_mode = '-savecsv '
    elif export_parameters['save_mode'] == 2:
        save_mode = '-saveascii '

    # Build parameters
    static_params_exp = [
        '-dirin ' + data['project_path'] +
        '/' + data['project_name'] + '_out/',
        save_mode + data['project_path'] + '/' + data['project_name'] +
        '_out/' + export_parameters['file_name'],
        '-onlytype:' + export_parameters['save_types'] +
        " " + export_parameters['additional_parameters']
    ]

    utils.debug("Going to execute: {} {}".format(data['partvtk4_path'], " ".join(static_params_exp)))

    # Start process
    export_process.start(data['partvtk4_path'], static_params_exp)
    temp_data['current_export_process'] = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        temp_data['current_output'] += current_output
        try:
            current_part = current_output.split(
                "{}_".format(export_parameters['file_name']))[1]
            if export_parameters['save_mode'] == 0:
                current_part = int(current_part.split(".vtk")[0])
            elif export_parameters['save_mode'] == 1:
                current_part = int(current_part.split(".csv")[0])
            elif export_parameters['save_mode'] == 2:
                current_part = int(current_part.split(".asc")[0])
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(on_stdout_ready)


def on_partvtk():
    """ Opens a dialog with PartVTK exporting options """
    # TODO: This should be a custom implementation in a class like PartVTKDialog(QtGui.QDialog)
    partvtk_tool_dialog = QtGui.QDialog()

    partvtk_tool_dialog.setModal(False)
    partvtk_tool_dialog.setWindowTitle(__("PartVTK Tool"))
    partvtk_tool_layout = QtGui.QVBoxLayout()

    pvtk_format_layout = QtGui.QHBoxLayout()
    pvtk_types_groupbox = QtGui.QGroupBox(__("Types to export"))
    pvtk_filename_layout = QtGui.QHBoxLayout()
    pvtk_parameters_layout = QtGui.QHBoxLayout()
    pvtk_buttons_layout = QtGui.QHBoxLayout()

    outformat_label = QtGui.QLabel(__("Output format"))
    outformat_combobox = QtGui.QComboBox()
    outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
    pvtk_format_layout.addWidget(outformat_label)
    pvtk_format_layout.addStretch(1)
    pvtk_format_layout.addWidget(outformat_combobox)

    pvtk_types_groupbox_layout = QtGui.QVBoxLayout()
    pvtk_types_chk_all = QtGui.QCheckBox(__("All"))
    pvtk_types_chk_all.setCheckState(QtCore.Qt.Checked)
    pvtk_types_chk_bound = QtGui.QCheckBox(__("Bound"))
    pvtk_types_chk_fluid = QtGui.QCheckBox(__("Fluid"))
    pvtk_types_chk_fixed = QtGui.QCheckBox(__("Fixed"))
    pvtk_types_chk_moving = QtGui.QCheckBox(__("Moving"))
    pvtk_types_chk_floating = QtGui.QCheckBox(__("Floating"))
    [pvtk_types_groupbox_layout.addWidget(x) for x in [
        pvtk_types_chk_all,
        pvtk_types_chk_bound,
        pvtk_types_chk_fluid,
        pvtk_types_chk_fixed,
        pvtk_types_chk_moving,
        pvtk_types_chk_floating
    ]]
    pvtk_types_groupbox.setLayout(pvtk_types_groupbox_layout)

    pvtk_file_name_label = QtGui.QLabel(__("File name"))
    pvtk_file_name_text = QtGui.QLineEdit()
    pvtk_file_name_text.setText('ExportPart')
    pvtk_filename_layout.addWidget(pvtk_file_name_label)
    pvtk_filename_layout.addWidget(pvtk_file_name_text)

    pvtk_parameters_label = QtGui.QLabel(__("Additional Parameters"))
    pvtk_parameters_text = QtGui.QLineEdit()
    pvtk_parameters_layout.addWidget(pvtk_parameters_label)
    pvtk_parameters_layout.addWidget(pvtk_parameters_text)

    pvtk_open_at_end = QtGui.QCheckBox("Open with ParaView")
    pvtk_open_at_end.setEnabled(data['paraview_path'] != "")

    pvtk_export_button = QtGui.QPushButton(__("Export"))
    pvtk_cancel_button = QtGui.QPushButton(__("Cancel"))
    pvtk_buttons_layout.addWidget(pvtk_export_button)
    pvtk_buttons_layout.addWidget(pvtk_cancel_button)

    partvtk_tool_layout.addLayout(pvtk_format_layout)
    partvtk_tool_layout.addWidget(pvtk_types_groupbox)
    partvtk_tool_layout.addStretch(1)
    partvtk_tool_layout.addLayout(pvtk_filename_layout)
    partvtk_tool_layout.addLayout(pvtk_parameters_layout)
    partvtk_tool_layout.addWidget(pvtk_open_at_end)
    partvtk_tool_layout.addLayout(pvtk_buttons_layout)

    partvtk_tool_dialog.setLayout(partvtk_tool_layout)

    def on_pvtk_cancel():
        """ Cancel button behaviour """
        partvtk_tool_dialog.reject()

    def on_pvtk_export():
        """ Export button behaviour """
        export_parameters = dict()
        export_parameters['save_mode'] = outformat_combobox.currentIndex()
        export_parameters['save_types'] = '-all'
        if pvtk_types_chk_all.isChecked():
            export_parameters['save_types'] = '+all'
        else:
            if pvtk_types_chk_bound.isChecked():
                export_parameters['save_types'] += ',+bound'
            if pvtk_types_chk_fluid.isChecked():
                export_parameters['save_types'] += ',+fluid'
            if pvtk_types_chk_fixed.isChecked():
                export_parameters['save_types'] += ',+fixed'
            if pvtk_types_chk_moving.isChecked():
                export_parameters['save_types'] += ',+moving'
            if pvtk_types_chk_floating.isChecked():
                export_parameters['save_types'] += ',+floating'

        if export_parameters['save_types'] == '-all':
            export_parameters['save_types'] = '+all'

        export_parameters['open_paraview'] = pvtk_open_at_end.isChecked()

        if len(pvtk_file_name_text.text()) > 0:
            export_parameters['file_name'] = pvtk_file_name_text.text()
        else:
            export_parameters['file_name'] = 'ExportedPart'

        if len(pvtk_parameters_text.text()) > 0:
            export_parameters['additional_parameters'] = pvtk_parameters_text.text(
            )
        else:
            export_parameters['additional_parameters'] = ''

        partvtk_export(export_parameters)
        partvtk_tool_dialog.accept()

    def on_pvtk_type_all_change(state):
        """ 'All' type selection handler """
        if state == QtCore.Qt.Checked:
            [chk.setCheckState(QtCore.Qt.Unchecked) for chk in [
                pvtk_types_chk_bound,
                pvtk_types_chk_fluid,
                pvtk_types_chk_fixed,
                pvtk_types_chk_moving,
                pvtk_types_chk_floating
            ]]

    def on_pvtk_type_bound_change(state):
        """ 'Bound' type selection handler """
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_fluid_change(state):
        """ 'Fluid' type selection handler """
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_fixed_change(state):
        """ 'Fixed' type selection handler """
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_moving_change(state):
        """ 'Moving' type selection handler """
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_floating_change(state):
        """ 'Floating' type selection handler """
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_export_format_change(index):
        """ Export format combobox handler"""
        if "vtk" in outformat_combobox.currentText().lower() and data['paraview_path'] != "":
            pvtk_open_at_end.setEnabled(True)
        else:
            pvtk_open_at_end.setEnabled(False)

    outformat_combobox.currentIndexChanged.connect(on_pvtk_export_format_change)
    pvtk_types_chk_all.stateChanged.connect(on_pvtk_type_all_change)
    pvtk_types_chk_bound.stateChanged.connect(on_pvtk_type_bound_change)
    pvtk_types_chk_fluid.stateChanged.connect(on_pvtk_type_fluid_change)
    pvtk_types_chk_fixed.stateChanged.connect(on_pvtk_type_fixed_change)
    pvtk_types_chk_moving.stateChanged.connect(on_pvtk_type_moving_change)
    pvtk_types_chk_floating.stateChanged.connect(on_pvtk_type_floating_change)
    pvtk_export_button.clicked.connect(on_pvtk_export)
    pvtk_cancel_button.clicked.connect(on_pvtk_cancel)
    partvtk_tool_dialog.exec_()


def floatinginfo_export(export_parameters):
    """ FloatingInfo tool export. """
    guiutils.widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_floatinginfo_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
            widget_state_elements['post_proc_floatinginfo_button'].setText(__("FloatingInfo"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    def on_export_finished(exit_code):
        widget_state_elements['post_proc_floatinginfo_button'].setText(__("FloatingInfo"))
        guiutils.widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()
        if exit_code == 0:
            # Exported correctly
            temp_data['current_info_dialog'] = dsphwidgets.InfoDialog(
                info_text=__("FloatingInfo finished successfully"),
                detailed_text=temp_data['current_output'])
        else:
            guiutils.error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=temp_data['current_output']
            )

    temp_data['current_output'] = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    static_params_exp = [
        '-dirin ' + data['project_path'] + '/' + data['project_name'] +
        '_out/', '-savemotion',
        '-savedata ' + data['project_path'] + '/' + data['project_name'] + '_out/' +
        export_parameters['filename'], export_parameters['additional_parameters']
    ]

    if len(export_parameters['onlyprocess']) > 0:
        static_params_exp.append('-onlymk:' + export_parameters['onlyprocess'])

    export_process.start(data['floatinginfo_path'], static_params_exp)
    temp_data['current_export_process'] = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        temp_data['current_output'] += current_output
        try:
            current_part = current_output.split("Part_")[1].split("  ")[0]
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(on_stdout_ready)


def on_floatinginfo():
    """ Opens a dialog with FloatingInfo exporting options """
    # TODO: This should be implemented in a custom class like FloatingInfoDialog(QtCore.QDialog)
    floatinfo_tool_dialog = QtGui.QDialog()

    floatinfo_tool_dialog.setModal(False)
    floatinfo_tool_dialog.setWindowTitle(__("FloatingInfo Tool"))
    floatinfo_tool_layout = QtGui.QVBoxLayout()

    finfo_onlyprocess_layout = QtGui.QHBoxLayout()
    finfo_filename_layout = QtGui.QHBoxLayout()
    finfo_additional_parameters_layout = QtGui.QHBoxLayout()
    finfo_buttons_layout = QtGui.QHBoxLayout()

    finfo_onlyprocess_label = QtGui.QLabel(__("MK to process (empty for all)"))
    finfo_onlyprocess_text = QtGui.QLineEdit()
    finfo_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
    finfo_onlyprocess_layout.addWidget(finfo_onlyprocess_label)
    finfo_onlyprocess_layout.addWidget(finfo_onlyprocess_text)

    finfo_filename_label = QtGui.QLabel(__("File Name"))
    finfo_filename_text = QtGui.QLineEdit()
    finfo_filename_text.setText("FloatingMotion")
    finfo_filename_layout.addWidget(finfo_filename_label)
    finfo_filename_layout.addWidget(finfo_filename_text)

    finfo_additional_parameters_label = QtGui.QLabel(__("Additional Parameters"))
    finfo_additional_parameters_text = QtGui.QLineEdit()
    finfo_additional_parameters_layout.addWidget(finfo_additional_parameters_label)
    finfo_additional_parameters_layout.addWidget(finfo_additional_parameters_text)

    finfo_export_button = QtGui.QPushButton(__("Export"))
    finfo_cancel_button = QtGui.QPushButton(__("Cancel"))
    finfo_buttons_layout.addWidget(finfo_export_button)
    finfo_buttons_layout.addWidget(finfo_cancel_button)

    floatinfo_tool_layout.addLayout(finfo_onlyprocess_layout)
    floatinfo_tool_layout.addLayout(finfo_filename_layout)
    floatinfo_tool_layout.addLayout(finfo_additional_parameters_layout)
    floatinfo_tool_layout.addStretch(1)
    floatinfo_tool_layout.addLayout(finfo_buttons_layout)

    floatinfo_tool_dialog.setLayout(floatinfo_tool_layout)

    def on_finfo_cancel():
        """ Cancel button behaviour."""
        floatinfo_tool_dialog.reject()

    def on_finfo_export():
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters['onlyprocess'] = finfo_onlyprocess_text.text()
        export_parameters['filename'] = finfo_filename_text.text()
        export_parameters['additional_parameters'] = finfo_additional_parameters_text.text()
        floatinginfo_export(export_parameters)
        floatinfo_tool_dialog.accept()

    finfo_export_button.clicked.connect(on_finfo_export)
    finfo_cancel_button.clicked.connect(on_finfo_cancel)
    finfo_filename_text.setFocus()
    floatinfo_tool_dialog.exec_()


def computeforces_export(export_parameters):
    """ ComputeForces tool export. """
    guiutils.widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_computeforces_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
            widget_state_elements['post_proc_computeforces_button'].setText(__("ComputeForces"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    def on_export_finished(exit_code):
        widget_state_elements['post_proc_computeforces_button'].setText(__("ComputeForces"))
        guiutils.widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()
        if exit_code == 0:
            # Exported correctly
            temp_data['current_info_dialog'] = dsphwidgets.InfoDialog(
                info_text=__("ComputeForces finished successfully."),
                detailed_text=temp_data['current_output']
            )
        else:
            guiutils.error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=temp_data['current_output']
            )

    temp_data['current_output'] = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    save_mode = '-savevtk '
    if export_parameters['save_mode'] == 0:
        save_mode = '-savevtk '
    elif export_parameters['save_mode'] == 1:
        save_mode = '-savecsv '
    elif export_parameters['save_mode'] == 2:
        save_mode = '-saveascii '

    static_params_exp = [
        '-dirin ' + data['project_path'] +
        '/' + data['project_name'] + '_out/',
        '-filexml ' + data['project_path'] + '/' +
        data['project_name'] + '_out/' + data['project_name'] + '.xml',
        save_mode + data['project_path'] + '/' + data['project_name'] + '_out/' +
        export_parameters['filename'], export_parameters['additional_parameters']
    ]

    if len(export_parameters['onlyprocess']) > 0:
        static_params_exp.append(export_parameters['onlyprocess_tag'] + export_parameters['onlyprocess'])

    export_process.start(data['computeforces_path'], static_params_exp)
    temp_data['current_export_process'] = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        temp_data['current_output'] += current_output
        try:
            current_part = current_output.split("Part_")[1].split(".bi4")[0]
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(
        on_stdout_ready)


def on_computeforces():
    """ Opens a dialog with ComputeForces exporting options """
    # TODO: This should be implemented in a custom class like ComputerForcesDialog(QtGui.QDialog)
    compforces_tool_dialog = QtGui.QDialog()

    compforces_tool_dialog.setModal(False)
    compforces_tool_dialog.setWindowTitle(__("ComputeForces Tool"))
    compforces_tool_layout = QtGui.QVBoxLayout()

    cfces_format_layout = QtGui.QHBoxLayout()
    cfces_onlyprocess_layout = QtGui.QHBoxLayout()
    cfces_filename_layout = QtGui.QHBoxLayout()
    cfces_additional_parameters_layout = QtGui.QHBoxLayout()
    cfces_buttons_layout = QtGui.QHBoxLayout()

    outformat_label = QtGui.QLabel(__("Output format"))
    outformat_combobox = QtGui.QComboBox()
    outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
    outformat_combobox.setCurrentIndex(1)
    cfces_format_layout.addWidget(outformat_label)
    cfces_format_layout.addStretch(1)
    cfces_format_layout.addWidget(outformat_combobox)

    cfces_onlyprocess_selector = QtGui.QComboBox()
    cfces_onlyprocess_selector.insertItems(0, ["mk", "id", "position"])
    cfces_onlyprocess_label = QtGui.QLabel(__("to process (empty for all)"))
    cfces_onlyprocess_text = QtGui.QLineEdit()
    cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
    cfces_onlyprocess_layout.addWidget(cfces_onlyprocess_selector)
    cfces_onlyprocess_layout.addWidget(cfces_onlyprocess_label)
    cfces_onlyprocess_layout.addWidget(cfces_onlyprocess_text)

    cfces_filename_label = QtGui.QLabel(__("File Name"))
    cfces_filename_text = QtGui.QLineEdit()
    cfces_filename_text.setText("Force")
    cfces_filename_layout.addWidget(cfces_filename_label)
    cfces_filename_layout.addWidget(cfces_filename_text)

    cfces_additional_parameters_label = QtGui.QLabel(__("Additional Parameters"))
    cfces_additional_parameters_text = QtGui.QLineEdit()
    cfces_additional_parameters_layout.addWidget(cfces_additional_parameters_label)
    cfces_additional_parameters_layout.addWidget(cfces_additional_parameters_text)

    cfces_export_button = QtGui.QPushButton(__("Export"))
    cfces_cancel_button = QtGui.QPushButton(__("Cancel"))
    cfces_buttons_layout.addWidget(cfces_export_button)
    cfces_buttons_layout.addWidget(cfces_cancel_button)

    compforces_tool_layout.addLayout(cfces_format_layout)
    compforces_tool_layout.addLayout(cfces_onlyprocess_layout)
    compforces_tool_layout.addLayout(cfces_filename_layout)
    compforces_tool_layout.addLayout(cfces_additional_parameters_layout)
    compforces_tool_layout.addStretch(1)
    compforces_tool_layout.addLayout(cfces_buttons_layout)

    compforces_tool_dialog.setLayout(compforces_tool_layout)

    def on_cfces_cancel():
        """ Cancel button behaviour."""
        compforces_tool_dialog.reject()

    def on_cfces_export():
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters['save_mode'] = outformat_combobox.currentIndex()

        if "mk" in cfces_onlyprocess_selector.currentText().lower():
            export_parameters['onlyprocess_tag'] = "-onlymk:"
        elif "id" in cfces_onlyprocess_selector.currentText().lower():
            export_parameters['onlyprocess_tag'] = "-onlyid:"
        elif "position" in cfces_onlyprocess_selector.currentText().lower():
            export_parameters['onlyprocess_tag'] = "-onlypos:"

        export_parameters['onlyprocess'] = cfces_onlyprocess_text.text()
        export_parameters['filename'] = cfces_filename_text.text()
        export_parameters['additional_parameters'] = cfces_additional_parameters_text.text()
        computeforces_export(export_parameters)
        compforces_tool_dialog.accept()

    def on_cfces_onlyprocess_changed():
        if "mk" in cfces_onlyprocess_selector.currentText().lower():
            cfces_onlyprocess_text.setText("")
            cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        elif "id" in cfces_onlyprocess_selector.currentText().lower():
            cfces_onlyprocess_text.setText("")
            cfces_onlyprocess_text.setPlaceholderText("1,2,3 or 1-30")
        elif "position" in cfces_onlyprocess_selector.currentText().lower():
            cfces_onlyprocess_text.setText("")
            cfces_onlyprocess_text.setPlaceholderText("xmin:ymin:zmin:xmax:ymax:zmax (m)")

    cfces_onlyprocess_selector.currentIndexChanged.connect(on_cfces_onlyprocess_changed)
    cfces_export_button.clicked.connect(on_cfces_export)
    cfces_cancel_button.clicked.connect(on_cfces_cancel)
    compforces_tool_dialog.exec_()


def measuretool_export(export_parameters):
    """ MeasureTool tool export. """
    guiutils.widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_measuretool_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
            widget_state_elements['post_proc_measuretool_button'].setText(__("MeasureTool"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    def on_export_finished(exit_code):
        widget_state_elements['post_proc_measuretool_button'].setText(__("MeasureTool"))
        guiutils.widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()
        if exit_code == 0:
            # Exported correctly
            temp_data['current_info_dialog'] = dsphwidgets.InfoDialog(
                info_text=__("MeasureTool finished successfully."),
                detailed_text=temp_data['current_output']
            )
        else:
            guiutils.error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=temp_data['current_output']
            )

    temp_data['current_output'] = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    save_mode = '-savecsv '
    if export_parameters['save_mode'] == 0:
        save_mode = '-savevtk '
    elif export_parameters['save_mode'] == 1:
        save_mode = '-savecsv '
    elif export_parameters['save_mode'] == 2:
        save_mode = '-saveascii '

    # Save points to disk to later use them as parameter
    if len(temp_data['measuretool_points']) > len(temp_data['measuretool_grid']):
        # Save points
        with open(data['project_path'] + '/' + 'points.txt', 'w') as f:
            f.write("POINTS\n")
            for curr_point in temp_data['measuretool_points']:
                f.write("{}  {}  {}\n".format(*curr_point))
    else:
        # Save grid
        with open(data['project_path'] + '/' + 'points.txt', 'w') as f:
            for curr_point in temp_data['measuretool_grid']:
                f.write("POINTSLIST\n")
                f.write("{}  {}  {}\n{}  {}  {}\n{}  {}  {}\n".format(*curr_point))

    calculate_height = '-height' if export_parameters['calculate_water_elevation'] else ''

    static_params_exp = [
        '-dirin ' + data['project_path'] +
        '/' + data['project_name'] + '_out/',
        '-filexml ' + data['project_path'] + '/' +
        data['project_name'] + '_out/' + data['project_name'] + '.xml',
        save_mode + data['project_path'] + '/' +
        data['project_name'] + '_out/' + export_parameters['filename'],
        '-points ' + data['project_path'] + '/points.txt', '-vars:' +
        export_parameters['save_vars'], calculate_height,
        export_parameters['additional_parameters']
    ]

    export_process.start(data['measuretool_path'], static_params_exp)
    temp_data['current_export_process'] = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        temp_data['current_output'] += current_output
        try:
            current_part = current_output.split("/Part_")[1].split(".bi4")[0]
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(on_stdout_ready)


def on_measuretool():
    """ Opens a dialog with MeasureTool exporting options """
    # TODO: This should be implemented in a custom class like MeasureToolDialog(QtGui.QDialog)
    measuretool_tool_dialog = QtGui.QDialog()

    measuretool_tool_dialog.setModal(False)
    measuretool_tool_dialog.setWindowTitle(__("MeasureTool"))
    measuretool_tool_layout = QtGui.QVBoxLayout()

    mtool_format_layout = QtGui.QHBoxLayout()
    mtool_types_groupbox = QtGui.QGroupBox(__("Variables to export"))
    mtool_filename_layout = QtGui.QHBoxLayout()
    mtool_parameters_layout = QtGui.QHBoxLayout()
    mtool_buttons_layout = QtGui.QHBoxLayout()

    outformat_label = QtGui.QLabel(__("Output format"))
    outformat_combobox = QtGui.QComboBox()
    outformat_combobox.insertItems(0, ["VTK", "CSV", "ASCII"])
    outformat_combobox.setCurrentIndex(1)
    mtool_format_layout.addWidget(outformat_label)
    mtool_format_layout.addStretch(1)
    mtool_format_layout.addWidget(outformat_combobox)

    mtool_types_groupbox_layout = QtGui.QVBoxLayout()
    mtool_types_chk_all = QtGui.QCheckBox(__("All"))
    mtool_types_chk_all.setCheckState(QtCore.Qt.Checked)
    mtool_types_chk_vel = QtGui.QCheckBox(__("Velocity"))
    mtool_types_chk_rhop = QtGui.QCheckBox(__("Density"))
    mtool_types_chk_press = QtGui.QCheckBox(__("Pressure"))
    mtool_types_chk_mass = QtGui.QCheckBox(__("Mass"))
    mtool_types_chk_vol = QtGui.QCheckBox(__("Volume"))
    mtool_types_chk_idp = QtGui.QCheckBox(__("Particle ID"))
    mtool_types_chk_ace = QtGui.QCheckBox(__("Acceleration"))
    mtool_types_chk_vor = QtGui.QCheckBox(__("Vorticity"))
    mtool_types_chk_kcorr = QtGui.QCheckBox(__("KCorr"))
    [mtool_types_groupbox_layout.addWidget(x) for x in [
        mtool_types_chk_all,
        mtool_types_chk_vel,
        mtool_types_chk_rhop,
        mtool_types_chk_press,
        mtool_types_chk_mass,
        mtool_types_chk_vol,
        mtool_types_chk_idp,
        mtool_types_chk_ace,
        mtool_types_chk_vor,
        mtool_types_chk_kcorr
    ]]
    mtool_types_groupbox.setLayout(mtool_types_groupbox_layout)

    mtool_calculate_elevation = QtGui.QCheckBox(__("Calculate water elevation"))

    mtool_set_points_layout = QtGui.QHBoxLayout()
    mtool_set_points = QtGui.QPushButton("List of points")
    mtool_set_grid = QtGui.QPushButton("Grid of points")
    mtool_set_points_layout.addWidget(mtool_set_points)
    mtool_set_points_layout.addWidget(mtool_set_grid)

    mtool_file_name_label = QtGui.QLabel(__("File name"))
    mtool_file_name_text = QtGui.QLineEdit()
    mtool_file_name_text.setText('MeasurePart')
    mtool_filename_layout.addWidget(mtool_file_name_label)
    mtool_filename_layout.addWidget(mtool_file_name_text)

    mtool_parameters_label = QtGui.QLabel(__("Additional Parameters"))
    mtool_parameters_text = QtGui.QLineEdit()
    mtool_parameters_layout.addWidget(mtool_parameters_label)
    mtool_parameters_layout.addWidget(mtool_parameters_text)

    mtool_export_button = QtGui.QPushButton(__("Export"))
    mtool_cancel_button = QtGui.QPushButton(__("Cancel"))
    mtool_buttons_layout.addWidget(mtool_export_button)
    mtool_buttons_layout.addWidget(mtool_cancel_button)

    measuretool_tool_layout.addLayout(mtool_format_layout)
    measuretool_tool_layout.addWidget(mtool_types_groupbox)
    measuretool_tool_layout.addStretch(1)
    measuretool_tool_layout.addWidget(mtool_calculate_elevation)
    measuretool_tool_layout.addLayout(mtool_set_points_layout)
    measuretool_tool_layout.addLayout(mtool_filename_layout)
    measuretool_tool_layout.addLayout(mtool_parameters_layout)
    measuretool_tool_layout.addLayout(mtool_buttons_layout)

    measuretool_tool_dialog.setLayout(measuretool_tool_layout)

    def on_mtool_cancel():
        """ Cancel button behaviour."""
        measuretool_tool_dialog.reject()

    def on_mtool_export():
        """ Export button behaviour."""
        export_parameters = dict()
        export_parameters['save_mode'] = outformat_combobox.currentIndex()
        export_parameters['save_vars'] = '-all'
        if mtool_types_chk_all.isChecked():
            export_parameters['save_vars'] = '+all'
        else:
            if mtool_types_chk_vel.isChecked():
                export_parameters['save_vars'] += ',+vel'
            if mtool_types_chk_rhop.isChecked():
                export_parameters['save_vars'] += ',+rhop'
            if mtool_types_chk_press.isChecked():
                export_parameters['save_vars'] += ',+press'
            if mtool_types_chk_mass.isChecked():
                export_parameters['save_vars'] += ',+mass'
            if mtool_types_chk_vol.isChecked():
                export_parameters['save_vars'] += ',+vol'
            if mtool_types_chk_idp.isChecked():
                export_parameters['save_vars'] += ',+idp'
            if mtool_types_chk_ace.isChecked():
                export_parameters['save_vars'] += ',+ace'
            if mtool_types_chk_vor.isChecked():
                export_parameters['save_vars'] += ',+vor'
            if mtool_types_chk_kcorr.isChecked():
                export_parameters['save_vars'] += ',+kcorr'

        if export_parameters['save_vars'] == '-all':
            export_parameters['save_vars'] = '+all'

        export_parameters['calculate_water_elevation'] = mtool_calculate_elevation.isChecked()

        if len(mtool_file_name_text.text()) > 0:
            export_parameters['filename'] = mtool_file_name_text.text()
        else:
            export_parameters['filename'] = 'MeasurePart'

        if len(mtool_parameters_text.text()) > 0:
            export_parameters['additional_parameters'] = mtool_parameters_text.text()
        else:
            export_parameters['additional_parameters'] = ''

        measuretool_export(export_parameters)
        measuretool_tool_dialog.accept()

    def on_mtool_measure_all_change(state):
        """ 'All' checkbox behaviour"""
        if state == QtCore.Qt.Checked:
            [chk.setCheckState(QtCore.Qt.Unchecked) for chk in [
                mtool_types_chk_vel,
                mtool_types_chk_rhop,
                mtool_types_chk_press,
                mtool_types_chk_mass,
                mtool_types_chk_vol,
                mtool_types_chk_idp,
                mtool_types_chk_ace,
                mtool_types_chk_vor,
                mtool_types_chk_kcorr
            ]]

    def on_mtool_measure_single_change(state):
        """ Behaviour for all checkboxes except 'All' """
        if state == QtCore.Qt.Checked:
            mtool_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_set_points():
        """ Point list button behaviour."""
        # TODO: This should be implemented in a custom class like MeasureToolPointsDialog(QtGui.QDialog)
        measurepoints_tool_dialog = QtGui.QDialog()
        measurepoints_tool_dialog.setModal(False)
        measurepoints_tool_dialog.setWindowTitle(__("MeasureTool Points"))
        measurepoints_tool_layout = QtGui.QVBoxLayout()
        mpoints_table = QtGui.QTableWidget()
        mpoints_table.setRowCount(100)
        mpoints_table.setColumnCount(3)
        mpoints_table.verticalHeader().setVisible(False)
        mpoints_table.setHorizontalHeaderLabels(["X", "Y", "Z"])

        for i, point in enumerate(temp_data['measuretool_points']):
            mpoints_table.setItem(i, 0, QtGui.QTableWidgetItem(str(point[0])))
            mpoints_table.setItem(i, 1, QtGui.QTableWidgetItem(str(point[1])))
            mpoints_table.setItem(i, 2, QtGui.QTableWidgetItem(str(point[2])))

        def on_mpoints_accept():
            """ MeasureTool points dialog accept button behaviour. """
            temp_data['measuretool_points'] = list()
            for mtool_row in range(0, mpoints_table.rowCount()):
                try:
                    current_point = [
                        float(mpoints_table.item(mtool_row, 0).text()),
                        float(mpoints_table.item(mtool_row, 1).text()),
                        float(mpoints_table.item(mtool_row, 2).text())
                    ]
                    temp_data['measuretool_points'].append(current_point)
                except (ValueError, AttributeError):
                    pass

            # Deletes the grid points (not compatible together)
            temp_data['measuretool_grid'] = list()
            measurepoints_tool_dialog.accept()

        def on_mpoints_cancel():
            """ MeasureTool points dialog cancel button behaviour. """
            measurepoints_tool_dialog.reject()

        mpoints_bt_layout = QtGui.QHBoxLayout()
        mpoints_cancel = QtGui.QPushButton(__("Cancel"))
        mpoints_accept = QtGui.QPushButton(__("OK"))
        mpoints_accept.clicked.connect(on_mpoints_accept)
        mpoints_cancel.clicked.connect(on_mpoints_cancel)

        mpoints_bt_layout.addWidget(mpoints_accept)
        mpoints_bt_layout.addWidget(mpoints_cancel)

        measurepoints_tool_layout.addWidget(mpoints_table)
        measurepoints_tool_layout.addLayout(mpoints_bt_layout)

        measurepoints_tool_dialog.setLayout(measurepoints_tool_layout)
        measurepoints_tool_dialog.resize(350, 400)
        measurepoints_tool_dialog.exec_()

    def on_mtool_set_grid():

        measuregrid_tool_dialog = dsphwidgets.MeasureToolGridDialog(temp_data)
        measuregrid_tool_dialog.setModal(False)

    mtool_types_chk_all.stateChanged.connect(on_mtool_measure_all_change)
    mtool_types_chk_vel.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_rhop.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_press.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_mass.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_vol.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_idp.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_ace.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_vor.stateChanged.connect(on_mtool_measure_single_change)
    mtool_types_chk_kcorr.stateChanged.connect(on_mtool_measure_single_change)
    mtool_set_points.clicked.connect(on_mtool_set_points)
    mtool_set_grid.clicked.connect(on_mtool_set_grid)
    mtool_export_button.clicked.connect(on_mtool_export)
    mtool_cancel_button.clicked.connect(on_mtool_cancel)
    measuretool_tool_dialog.exec_()


def isosurface_export(export_parameters):
    """ Export IsoSurface button behaviour.
    Launches a process while disabling the button. """
    guiutils.widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_isosurface_button'].setText("Exporting...")

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
            widget_state_elements['post_proc_isosurface_button'].setText(__("IsoSurface"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    # IsoSurface export finish handler
    def on_export_finished(exit_code):
        widget_state_elements['post_proc_isosurface_button'].setText(__("IsoSurface"))
        guiutils.widget_state_config(widget_state_elements, "export finished")

        export_dialog.hide()

        if exit_code == 0:
            # Exported correctly
            temp_data['current_info_dialog'] = dsphwidgets.InfoDialog(
                info_text=__("IsoSurface finished successfully."),
                detailed_text=temp_data['current_output'])
        else:
            guiutils.error_dialog(
                __("There was an error on the post-processing."),
                detailed_text=temp_data['current_output']
            )

        # Bit of code that tries to open ParaView if the option was selected.
        if export_parameters['open_paraview']:
            subprocess.Popen(
                [data['paraview_path'], "--data={}\\{}_..{}".format(
                    data['project_path'] + '\\' + data['project_name'] + '_out',
                    export_parameters['file_name'], "vtk")],
                stdout=subprocess.PIPE)

    temp_data['current_output'] = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    # Build parameters
    static_params_exp = [
        '-dirin ' + data['project_path'] +
        '/' + data['project_name'] + '_out/',
        export_parameters["surface_or_slice"] + " " + data['project_path'] + '/' +
        data['project_name'] + '_out/' + export_parameters['file_name'] +
        " " + export_parameters['additional_parameters']
    ]

    # Start process
    export_process.start(data['isosurface_path'], static_params_exp)
    temp_data['current_export_process'] = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        temp_data['current_output'] += current_output
        try:
            current_part = current_output.split("{}_".format(export_parameters['file_name']))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(on_stdout_ready)


def on_isosurface():
    """ Opens a dialog with IsoSurface exporting options """
    # TODO: This should be implemented as a custom class like IsoSurfaceDialog(QtGui.QDialog)
    isosurface_tool_dialog = QtGui.QDialog()

    isosurface_tool_dialog.setModal(False)
    isosurface_tool_dialog.setWindowTitle(__("IsoSurface Tool"))
    isosurface_tool_layout = QtGui.QVBoxLayout()

    isosfc_filename_layout = QtGui.QHBoxLayout()
    isosfc_parameters_layout = QtGui.QHBoxLayout()
    isosfc_buttons_layout = QtGui.QHBoxLayout()

    isosfc_selector_layout = QtGui.QHBoxLayout()
    isosfc_selector_label = QtGui.QLabel(__("Save: "))
    isosfc_selector = QtGui.QComboBox()
    isosfc_selector.insertItems(0, ["Surface", "Slice"])
    isosfc_selector_layout.addWidget(isosfc_selector_label)
    isosfc_selector_layout.addWidget(isosfc_selector)

    isosfc_file_name_label = QtGui.QLabel(__("File name"))
    isosfc_file_name_text = QtGui.QLineEdit()
    isosfc_file_name_text.setText('FileIso')
    isosfc_filename_layout.addWidget(isosfc_file_name_label)
    isosfc_filename_layout.addWidget(isosfc_file_name_text)

    isosfc_parameters_label = QtGui.QLabel(__("Additional Parameters"))
    isosfc_parameters_text = QtGui.QLineEdit()
    isosfc_parameters_layout.addWidget(isosfc_parameters_label)
    isosfc_parameters_layout.addWidget(isosfc_parameters_text)

    isosfc_open_at_end = QtGui.QCheckBox("Open with ParaView")
    isosfc_open_at_end.setEnabled(data['paraview_path'] != "")

    isosfc_export_button = QtGui.QPushButton(__("Export"))
    isosfc_cancel_button = QtGui.QPushButton(__("Cancel"))
    isosfc_buttons_layout.addWidget(isosfc_export_button)
    isosfc_buttons_layout.addWidget(isosfc_cancel_button)

    isosurface_tool_layout.addLayout(isosfc_selector_layout)
    isosurface_tool_layout.addLayout(isosfc_filename_layout)
    isosurface_tool_layout.addLayout(isosfc_parameters_layout)
    isosurface_tool_layout.addWidget(isosfc_open_at_end)
    isosurface_tool_layout.addStretch(1)
    isosurface_tool_layout.addLayout(isosfc_buttons_layout)

    isosurface_tool_dialog.setLayout(isosurface_tool_layout)

    def on_isosfc_cancel():
        """ IsoSurface dialog cancel button behaviour."""
        isosurface_tool_dialog.reject()

    def on_isosfc_export():
        """ IsoSurface dialog export button behaviour."""
        export_parameters = dict()

        if "surface" in isosfc_selector.currentText().lower():
            export_parameters['surface_or_slice'] = '-saveiso'
        else:
            export_parameters['surface_or_slice'] = '-saveslice'

        if len(isosfc_file_name_text.text()) > 0:
            export_parameters['file_name'] = isosfc_file_name_text.text()
        else:
            export_parameters['file_name'] = 'IsoFile'

        if len(isosfc_parameters_text.text()) > 0:
            export_parameters['additional_parameters'] = isosfc_parameters_text.text()
        else:
            export_parameters['additional_parameters'] = ''

        export_parameters['open_paraview'] = isosfc_open_at_end.isChecked()

        isosurface_export(export_parameters)
        isosurface_tool_dialog.accept()

    isosfc_export_button.clicked.connect(on_isosfc_export)
    isosfc_cancel_button.clicked.connect(on_isosfc_cancel)
    isosurface_tool_dialog.exec_()


def flowtool_export(export_parameters):
    """ Export FlowTool button behaviour.
    Launches a process while disabling the button. """
    guiutils.widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_flowtool_button'].setText("Exporting...")

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(data['project_path'] + '/' + data['project_name'] + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data['total_export_parts'] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data['total_export_parts'])
    export_progbar_bar.setRange(0, temp_data['total_export_parts'])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        utils.log(__("Stopping export"))
        if temp_data['current_export_process'] is not None:
            temp_data['current_export_process'].kill()
            widget_state_elements['post_proc_flowtool_button'].setText(__("FlowTool"))
        guiutils.widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    # FlowTool export finish handler
    def on_export_finished(exit_code):
        widget_state_elements['post_proc_flowtool_button'].setText(__("FlowTool"))
        guiutils.widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()

        if exit_code == 0:
            # Exported correctly
            temp_data['current_info_dialog'] = dsphwidgets.InfoDialog(
                info_text=__("FlowTool finished successfully."),
                detailed_text=temp_data['current_output'])
        else:
            guiutils.error_dialog(
                __("There was an error on the post-processing."),
                detailed_text=temp_data['current_output']
            )

    temp_data['current_output'] = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    # Build parameters
    static_params_exp = [
        '-dirin ' + data['project_path'] +
        '/' + data['project_name'] + '_out/',
        '-fileboxes ' + data['project_path'] + '/' + 'fileboxes.txt',
        '-savecsv ' + data['project_path'] + '/' + data['project_name'] +
        '_out/' + '{}.csv'.format(export_parameters['csv_name']),
        '-savevtk ' + data['project_path'] + '/' + data['project_name'] + '_out/' + '{}.vtk'.format(
            export_parameters['vtk_name']) +
        " " + export_parameters['additional_parameters']
    ]

    # Start process
    export_process.start(data['flowtool_path'], static_params_exp)
    temp_data['current_export_process'] = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(temp_data['current_export_process'].readAllStandardOutput())
        temp_data['current_output'] += current_output
        try:
            current_part = current_output.split("{}_".format(export_parameters['vtk_name']))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_progbar_bar.value()
        export_progbar_bar.setValue(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(temp_data['total_export_parts']))

    temp_data['current_export_process'].readyReadStandardOutput.connect(on_stdout_ready)


def on_flowtool():
    """ Opens a dialog with FlowTool exporting options """
    # TODO: This should be implemented as a custom class like FlowToolDialog(QtGui.QDialog)
    flowtool_tool_dialog = QtGui.QDialog()

    flowtool_tool_dialog.setModal(False)
    flowtool_tool_dialog.setWindowTitle(__("FlowTool Tool"))
    flowtool_tool_layout = QtGui.QVBoxLayout()

    fltool_boxlist_groupbox = QtGui.QGroupBox(__("List of boxes"))
    fltool_csvname_layout = QtGui.QHBoxLayout()
    fltool_vtkname_layout = QtGui.QHBoxLayout()
    fltool_parameters_layout = QtGui.QHBoxLayout()
    fltool_buttons_layout = QtGui.QHBoxLayout()

    fltool_boxlist_groupbox_layout = QtGui.QVBoxLayout()

    fltool_addbox_layout = QtGui.QHBoxLayout()
    fltool_addbox_button = QtGui.QPushButton(__("New Box"))
    fltool_addbox_layout.addStretch(1)
    fltool_addbox_layout.addWidget(fltool_addbox_button)

    fltool_boxlist_layout = QtGui.QVBoxLayout()

    fltool_boxlist_groupbox_layout.addLayout(fltool_addbox_layout)
    fltool_boxlist_groupbox_layout.addLayout(fltool_boxlist_layout)
    fltool_boxlist_groupbox.setLayout(fltool_boxlist_groupbox_layout)

    fltool_csv_file_name_label = QtGui.QLabel(__("CSV file name"))
    fltool_csv_file_name_text = QtGui.QLineEdit()
    fltool_csv_file_name_text.setText('_ResultFlow')
    fltool_csvname_layout.addWidget(fltool_csv_file_name_label)
    fltool_csvname_layout.addWidget(fltool_csv_file_name_text)

    fltool_vtk_file_name_label = QtGui.QLabel(__("VTK file name"))
    fltool_vtk_file_name_text = QtGui.QLineEdit()
    fltool_vtk_file_name_text.setText('Boxes')
    fltool_vtkname_layout.addWidget(fltool_vtk_file_name_label)
    fltool_vtkname_layout.addWidget(fltool_vtk_file_name_text)

    fltool_parameters_label = QtGui.QLabel(__("Additional Parameters"))
    fltool_parameters_text = QtGui.QLineEdit()
    fltool_parameters_layout.addWidget(fltool_parameters_label)
    fltool_parameters_layout.addWidget(fltool_parameters_text)

    fltool_export_button = QtGui.QPushButton(__("Export"))
    fltool_cancel_button = QtGui.QPushButton(__("Cancel"))
    fltool_buttons_layout.addWidget(fltool_export_button)
    fltool_buttons_layout.addWidget(fltool_cancel_button)

    flowtool_tool_layout.addWidget(fltool_boxlist_groupbox)
    flowtool_tool_layout.addStretch(1)
    flowtool_tool_layout.addLayout(fltool_csvname_layout)
    flowtool_tool_layout.addLayout(fltool_vtkname_layout)
    flowtool_tool_layout.addLayout(fltool_parameters_layout)
    flowtool_tool_layout.addLayout(fltool_buttons_layout)

    flowtool_tool_dialog.setLayout(flowtool_tool_layout)

    def box_edit(box_id):
        """ Box edit button behaviour. Opens a dialog to edit the selected FlowTool Box"""
        # TODO: This should be implemented as a custom class like FlowToolBoxEditDialog(QtGui.QDialog)
        box_edit_dialog = QtGui.QDialog()
        box_edit_layout = QtGui.QVBoxLayout()

        # Find the box for which the button was pressed
        target_box = None

        for box in data['flowtool_boxes']:
            if box[0] == box_id:
                target_box = box

        # This should not happen but if no box is found with reference id, it spawns an error.
        if target_box is None:
            guiutils.error_dialog("There was an error opening the box to edit")
            return

        box_edit_name_layout = QtGui.QHBoxLayout()
        box_edit_name_label = QtGui.QLabel(__("Box Name"))
        box_edit_name_input = QtGui.QLineEdit(str(target_box[1]))
        box_edit_name_layout.addWidget(box_edit_name_label)
        box_edit_name_layout.addWidget(box_edit_name_input)

        box_edit_description = QtGui.QLabel(__("Using multiple boxes with the same name will produce only one volume to measure.\n"
                                               "Use that to create prisms and complex forms. "
                                               "All points are specified in meters."))
        box_edit_description.setAlignment(QtCore.Qt.AlignCenter)

        # Reference image
        box_edit_image = QtGui.QLabel()
        box_edit_image.setPixmap(guiutils.get_icon("flowtool_template.jpg", return_only_path=True))
        box_edit_image.setAlignment(QtCore.Qt.AlignCenter)

        # Point coords inputs
        box_edit_points_layout = QtGui.QVBoxLayout()

        box_edit_point_a_layout = QtGui.QHBoxLayout()
        box_edit_point_a_label = QtGui.QLabel(__("Point A (X, Y, Z)"))
        box_edit_point_a_x = QtGui.QLineEdit(str(target_box[2][0]))
        box_edit_point_a_y = QtGui.QLineEdit(str(target_box[2][1]))
        box_edit_point_a_z = QtGui.QLineEdit(str(target_box[2][2]))
        box_edit_point_a_layout.addWidget(box_edit_point_a_label)
        box_edit_point_a_layout.addWidget(box_edit_point_a_x)
        box_edit_point_a_layout.addWidget(box_edit_point_a_y)
        box_edit_point_a_layout.addWidget(box_edit_point_a_z)

        box_edit_point_b_layout = QtGui.QHBoxLayout()
        box_edit_point_b_label = QtGui.QLabel(__("Point B (X, Y, Z)"))
        box_edit_point_b_x = QtGui.QLineEdit(str(target_box[3][0]))
        box_edit_point_b_y = QtGui.QLineEdit(str(target_box[3][1]))
        box_edit_point_b_z = QtGui.QLineEdit(str(target_box[3][2]))
        box_edit_point_b_layout.addWidget(box_edit_point_b_label)
        box_edit_point_b_layout.addWidget(box_edit_point_b_x)
        box_edit_point_b_layout.addWidget(box_edit_point_b_y)
        box_edit_point_b_layout.addWidget(box_edit_point_b_z)

        box_edit_point_c_layout = QtGui.QHBoxLayout()
        box_edit_point_c_label = QtGui.QLabel(__("Point C (X, Y, Z)"))
        box_edit_point_c_x = QtGui.QLineEdit(str(target_box[4][0]))
        box_edit_point_c_y = QtGui.QLineEdit(str(target_box[4][1]))
        box_edit_point_c_z = QtGui.QLineEdit(str(target_box[4][2]))
        box_edit_point_c_layout.addWidget(box_edit_point_c_label)
        box_edit_point_c_layout.addWidget(box_edit_point_c_x)
        box_edit_point_c_layout.addWidget(box_edit_point_c_y)
        box_edit_point_c_layout.addWidget(box_edit_point_c_z)

        box_edit_point_d_layout = QtGui.QHBoxLayout()
        box_edit_point_d_label = QtGui.QLabel(__("Point D (X, Y, Z)"))
        box_edit_point_d_x = QtGui.QLineEdit(str(target_box[5][0]))
        box_edit_point_d_y = QtGui.QLineEdit(str(target_box[5][1]))
        box_edit_point_d_z = QtGui.QLineEdit(str(target_box[5][2]))
        box_edit_point_d_layout.addWidget(box_edit_point_d_label)
        box_edit_point_d_layout.addWidget(box_edit_point_d_x)
        box_edit_point_d_layout.addWidget(box_edit_point_d_y)
        box_edit_point_d_layout.addWidget(box_edit_point_d_z)

        box_edit_point_e_layout = QtGui.QHBoxLayout()
        box_edit_point_e_label = QtGui.QLabel(__("Point E (X, Y, Z)"))
        box_edit_point_e_x = QtGui.QLineEdit(str(target_box[6][0]))
        box_edit_point_e_y = QtGui.QLineEdit(str(target_box[6][1]))
        box_edit_point_e_z = QtGui.QLineEdit(str(target_box[6][2]))
        box_edit_point_e_layout.addWidget(box_edit_point_e_label)
        box_edit_point_e_layout.addWidget(box_edit_point_e_x)
        box_edit_point_e_layout.addWidget(box_edit_point_e_y)
        box_edit_point_e_layout.addWidget(box_edit_point_e_z)

        box_edit_point_f_layout = QtGui.QHBoxLayout()
        box_edit_point_f_label = QtGui.QLabel(__("Point F (X, Y, Z)"))
        box_edit_point_f_x = QtGui.QLineEdit(str(target_box[7][0]))
        box_edit_point_f_y = QtGui.QLineEdit(str(target_box[7][1]))
        box_edit_point_f_z = QtGui.QLineEdit(str(target_box[7][2]))
        box_edit_point_f_layout.addWidget(box_edit_point_f_label)
        box_edit_point_f_layout.addWidget(box_edit_point_f_x)
        box_edit_point_f_layout.addWidget(box_edit_point_f_y)
        box_edit_point_f_layout.addWidget(box_edit_point_f_z)

        box_edit_point_g_layout = QtGui.QHBoxLayout()
        box_edit_point_g_label = QtGui.QLabel(__("Point G (X, Y, Z)"))
        box_edit_point_g_x = QtGui.QLineEdit(str(target_box[8][0]))
        box_edit_point_g_y = QtGui.QLineEdit(str(target_box[8][1]))
        box_edit_point_g_z = QtGui.QLineEdit(str(target_box[8][2]))
        box_edit_point_g_layout.addWidget(box_edit_point_g_label)
        box_edit_point_g_layout.addWidget(box_edit_point_g_x)
        box_edit_point_g_layout.addWidget(box_edit_point_g_y)
        box_edit_point_g_layout.addWidget(box_edit_point_g_z)

        box_edit_point_h_layout = QtGui.QHBoxLayout()
        box_edit_point_h_label = QtGui.QLabel(__("Point H (X, Y, Z)"))
        box_edit_point_h_x = QtGui.QLineEdit(str(target_box[9][0]))
        box_edit_point_h_y = QtGui.QLineEdit(str(target_box[9][1]))
        box_edit_point_h_z = QtGui.QLineEdit(str(target_box[9][2]))
        box_edit_point_h_layout.addWidget(box_edit_point_h_label)
        box_edit_point_h_layout.addWidget(box_edit_point_h_x)
        box_edit_point_h_layout.addWidget(box_edit_point_h_y)
        box_edit_point_h_layout.addWidget(box_edit_point_h_z)

        box_edit_points_layout.addLayout(box_edit_point_a_layout)
        box_edit_points_layout.addLayout(box_edit_point_b_layout)
        box_edit_points_layout.addLayout(box_edit_point_c_layout)
        box_edit_points_layout.addLayout(box_edit_point_d_layout)
        box_edit_points_layout.addLayout(box_edit_point_e_layout)
        box_edit_points_layout.addLayout(box_edit_point_f_layout)
        box_edit_points_layout.addLayout(box_edit_point_g_layout)
        box_edit_points_layout.addLayout(box_edit_point_h_layout)

        # Ok and cancel buttons
        box_edit_button_layout = QtGui.QHBoxLayout()
        box_edit_button_ok = QtGui.QPushButton(__("OK"))
        box_edit_button_cancel = QtGui.QPushButton(__("Cancel"))

        box_edit_button_layout.addStretch(1)
        box_edit_button_layout.addWidget(box_edit_button_ok)
        box_edit_button_layout.addWidget(box_edit_button_cancel)

        box_edit_layout.addLayout(box_edit_name_layout)
        box_edit_layout.addWidget(box_edit_description)
        box_edit_layout.addWidget(box_edit_image)
        box_edit_layout.addStretch(1)
        box_edit_layout.addLayout(box_edit_points_layout)
        box_edit_layout.addLayout(box_edit_button_layout)

        box_edit_dialog.setLayout(box_edit_layout)

        def on_ok():
            """ FlowTool box edit ok behaviour."""
            box_to_edit_index = -1
            for box_index, box_value in enumerate(data['flowtool_boxes']):
                if box_value[0] == box_id:
                    box_to_edit_index = box_index

            data['flowtool_boxes'][box_to_edit_index][1] = str(box_edit_name_input.text())
            data['flowtool_boxes'][box_to_edit_index][2] = [float(box_edit_point_a_x.text()),
                                                            float(box_edit_point_a_y.text()),
                                                            float(box_edit_point_a_z.text())]
            data['flowtool_boxes'][box_to_edit_index][3] = [float(box_edit_point_b_x.text()),
                                                            float(box_edit_point_b_y.text()),
                                                            float(box_edit_point_b_z.text())]
            data['flowtool_boxes'][box_to_edit_index][4] = [float(box_edit_point_c_x.text()),
                                                            float(box_edit_point_c_y.text()),
                                                            float(box_edit_point_c_z.text())]
            data['flowtool_boxes'][box_to_edit_index][5] = [float(box_edit_point_d_x.text()),
                                                            float(box_edit_point_d_y.text()),
                                                            float(box_edit_point_d_z.text())]
            data['flowtool_boxes'][box_to_edit_index][6] = [float(box_edit_point_e_x.text()),
                                                            float(box_edit_point_e_y.text()),
                                                            float(box_edit_point_e_z.text())]
            data['flowtool_boxes'][box_to_edit_index][7] = [float(box_edit_point_f_x.text()),
                                                            float(box_edit_point_f_y.text()),
                                                            float(box_edit_point_f_z.text())]
            data['flowtool_boxes'][box_to_edit_index][8] = [float(box_edit_point_g_x.text()),
                                                            float(box_edit_point_g_y.text()),
                                                            float(box_edit_point_g_z.text())]
            data['flowtool_boxes'][box_to_edit_index][9] = [float(box_edit_point_h_x.text()),
                                                            float(box_edit_point_h_y.text()),
                                                            float(box_edit_point_h_z.text())]
            refresh_boxlist()
            box_edit_dialog.accept()

        def on_cancel():
            """ FlowTool box edit cancel button behaviour."""
            box_edit_dialog.reject()

        box_edit_button_ok.clicked.connect(on_ok)
        box_edit_button_cancel.clicked.connect(on_cancel)

        box_edit_dialog.exec_()

    def box_delete(box_id):
        """ Box delete button behaviour. Tries to find the box for which the button was pressed and deletes it."""
        box_to_remove = None
        for box in data['flowtool_boxes']:
            if box[0] == box_id:
                box_to_remove = box
        if box_to_remove is not None:
            data['flowtool_boxes'].remove(box_to_remove)
            refresh_boxlist()

    def refresh_boxlist():
        """ Refreshes the FlowTool box list."""
        while fltool_boxlist_layout.count() > 0:
            target = fltool_boxlist_layout.takeAt(0)
            target.setParent(None)

        for box in data['flowtool_boxes']:
            to_add_layout = QtGui.QHBoxLayout()
            to_add_label = QtGui.QLabel(str(box[1]))
            to_add_layout.addWidget(to_add_label)
            to_add_layout.addStretch(1)
            to_add_editbutton = QtGui.QPushButton("Edit")
            to_add_deletebutton = QtGui.QPushButton("Delete")
            to_add_layout.addWidget(to_add_editbutton)
            to_add_layout.addWidget(to_add_deletebutton)
            to_add_editbutton.clicked.connect(lambda b=box[0]: box_edit(b))
            to_add_deletebutton.clicked.connect(lambda b=box[0]: box_delete(b))
            fltool_boxlist_layout.addLayout(to_add_layout)

    def on_fltool_addbox():
        """ Adds a box to the data structure."""
        data['flowtool_boxes'].append([
            str(uuid.uuid4()),
            'BOX',
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ])
        refresh_boxlist()

    def on_fltool_cancel():
        """ FlowTool cancel button behaviour."""
        flowtool_tool_dialog.reject()

    def on_fltool_export():
        """ FlowTool export button behaviour."""
        export_parameters = dict()

        if len(fltool_csv_file_name_text.text()) > 0:
            export_parameters['csv_name'] = fltool_csv_file_name_text.text()
        else:
            export_parameters['csv_name'] = '_ResultFlow'

        if len(fltool_vtk_file_name_text.text()) > 0:
            export_parameters['vtk_name'] = fltool_vtk_file_name_text.text()
        else:
            export_parameters['vtk_name'] = 'Boxes'

        if len(fltool_parameters_text.text()) > 0:
            export_parameters['additional_parameters'] = fltool_parameters_text.text()
        else:
            export_parameters['additional_parameters'] = ''

        utils.create_flowtool_boxes(data['project_path'] + '/' + 'fileboxes.txt', data['flowtool_boxes'])

        flowtool_export(export_parameters)
        flowtool_tool_dialog.accept()

    fltool_addbox_button.clicked.connect(on_fltool_addbox)
    fltool_export_button.clicked.connect(on_fltool_export)
    fltool_cancel_button.clicked.connect(on_fltool_cancel)
    refresh_boxlist()
    flowtool_tool_dialog.exec_()


# TODO: Implement BoundaryVTK post-processing tool
def on_boundaryvtk():
    """ Opens a dialog with BoundaryVTK exporting options """
    # TODO: This should be implemented as a custom class like BoundaryVTKDialog(QtGui.QDialog)
    guiutils.warning_dialog("Not implemented yet")
    return


# Post processing section scaffolding
export_layout = QtGui.QVBoxLayout()
export_label = QtGui.QLabel("<b>" + __("Post-processing") + "</b>")
export_label.setWordWrap(True)
export_first_row_layout = QtGui.QHBoxLayout()
export_second_row_layout = QtGui.QHBoxLayout()

# Tool buttons
post_proc_partvtk_button = QtGui.QPushButton(__("PartVTK"))
post_proc_computeforces_button = QtGui.QPushButton(__("ComputeForces"))
post_proc_isosurface_button = QtGui.QPushButton(__("IsoSurface"))
post_proc_floatinginfo_button = QtGui.QPushButton(__("FloatingInfo"))
post_proc_measuretool_button = QtGui.QPushButton(__("MeasureTool"))
post_proc_boundaryvtk_button = QtGui.QPushButton(__("BoundaryVTK"))
post_proc_flowtool_button = QtGui.QPushButton(__("FlowTool"))

post_proc_partvtk_button.setToolTip(__("Opens the PartVTK tool."))
post_proc_computeforces_button.setToolTip(__("Opens the ComputeForces tool."))
post_proc_floatinginfo_button.setToolTip(__("Opens the FloatingInfo tool."))
post_proc_measuretool_button.setToolTip(__("Opens the MeasureTool tool."))
post_proc_isosurface_button.setToolTip(__("Opens the IsoSurface tool."))
post_proc_boundaryvtk_button.setToolTip(__("Opens the BoundaryVTK tool."))
post_proc_flowtool_button.setToolTip(__("Opens the FlowTool tool."))

widget_state_elements['post_proc_partvtk_button'] = post_proc_partvtk_button
widget_state_elements['post_proc_computeforces_button'] = post_proc_computeforces_button
widget_state_elements['post_proc_floatinginfo_button'] = post_proc_floatinginfo_button
widget_state_elements['post_proc_measuretool_button'] = post_proc_measuretool_button
widget_state_elements['post_proc_isosurface_button'] = post_proc_isosurface_button
widget_state_elements['post_proc_boundaryvtk_button'] = post_proc_boundaryvtk_button
widget_state_elements['post_proc_flowtool_button'] = post_proc_flowtool_button

post_proc_partvtk_button.clicked.connect(on_partvtk)
post_proc_computeforces_button.clicked.connect(on_computeforces)
post_proc_floatinginfo_button.clicked.connect(on_floatinginfo)
post_proc_measuretool_button.clicked.connect(on_measuretool)
post_proc_isosurface_button.clicked.connect(on_isosurface)
post_proc_boundaryvtk_button.clicked.connect(on_boundaryvtk)
post_proc_flowtool_button.clicked.connect(on_flowtool)

export_layout.addWidget(export_label)
export_first_row_layout.addWidget(post_proc_partvtk_button)
export_first_row_layout.addWidget(post_proc_computeforces_button)
export_first_row_layout.addWidget(post_proc_isosurface_button)
export_second_row_layout.addWidget(post_proc_floatinginfo_button)
export_second_row_layout.addWidget(post_proc_measuretool_button)
# TODO: Enable this when boundaryvtk is implemented
# export_second_row_layout.addWidget(post_proc_boundaryvtk_button)
export_second_row_layout.addWidget(post_proc_flowtool_button)
export_layout.addLayout(export_first_row_layout)
export_layout.addLayout(export_second_row_layout)

# Object list table scaffolding
# TODO: This should be implemented as a custom class like ObjectListTable(QtGui.QWidget) or something like that.
objectlist_layout = QtGui.QVBoxLayout()
objectlist_label = QtGui.QLabel("<b>" + __("Object order") + "</b>")
objectlist_label.setWordWrap(True)
objectlist_table = QtGui.QTableWidget(0, 1)
objectlist_table.setObjectName("DSPH Objects")
objectlist_table.verticalHeader().setVisible(False)
objectlist_table.horizontalHeader().setVisible(False)
objectlist_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
widget_state_elements['objectlist_table'] = objectlist_table
temp_data['objectlist_table'] = objectlist_table
objectlist_layout.addWidget(objectlist_label)
objectlist_layout.addWidget(objectlist_table)

# ++++++++++++ Main Layout construction ++++++++++++
logo_layout.addStretch(0.5)
logo_layout.addWidget(logo_label)
logo_layout.addStretch(0.5)
logo_layout.addWidget(help_button)

# Adding things here and there
intro_layout.addWidget(constants_label)

constantsandsetup_layout = QtGui.QHBoxLayout()
constantsandsetup_layout.addWidget(constants_button)
constantsandsetup_layout.addWidget(execparams_button)
constantsandsetup_layout.addWidget(setup_button)

intro_layout.addLayout(constantsandsetup_layout)

main_layout.addLayout(logo_layout)
main_layout.addWidget(guiutils.h_line_generator())
main_layout.addLayout(intro_layout)
main_layout.addWidget(guiutils.h_line_generator())
main_layout.addLayout(dp_layout)
main_layout.addWidget(guiutils.h_line_generator())
main_layout.addLayout(cc_layout)
main_layout.addWidget(guiutils.h_line_generator())
main_layout.addLayout(ex_layout)
main_layout.addWidget(guiutils.h_line_generator())
main_layout.addLayout(export_layout)
main_layout.addWidget(guiutils.h_line_generator())
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
# This is the dock widget that by default appears at the bottom-right corner.
# ----------------------------
# Tries to find and close previous instances of the widget.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, "DSPH_Properties")
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

# Creation of the widget and scaffolding
# TODO: This should be implemented as a custom class like DesignSPHysicsPropertiesDock(QtGui.QDockWidget)
properties_widget = QtGui.QDockWidget()
properties_widget.setObjectName("DSPH_Properties")
properties_widget.setWindowTitle(__("DSPH Object Properties"))

# Scaffolding widget, only useful to apply to the properties_dock widget
properties_scaff_widget = QtGui.QWidget()
property_widget_layout = QtGui.QVBoxLayout()

# Property table
object_property_table = QtGui.QTableWidget(7, 2)
object_property_table.setMinimumHeight(220)
object_property_table.setHorizontalHeaderLabels([__("Property Name"), __("Value")])
object_property_table.verticalHeader().setVisible(False)
object_property_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

# Add an object to DSPH. Only appears when an object is not part of the simulation
addtodsph_button = QtGui.QPushButton(__("Add to DSPH Simulation"))
addtodsph_button.setToolTip(__("Adds the current selection to\nthe case. Objects not included will not be exported."))

# Same as above, this time with remove
removefromdsph_button = QtGui.QPushButton(__("Remove from DSPH Simulation"))
removefromdsph_button.setToolTip(__("Removes the current selection from the case.\n"
                                    "Objects not included in the case will not be exported."))

# Damping configuration button
damping_config_button = QtGui.QPushButton(__("Damping configuration"))
damping_config_button.setToolTip(__("Opens the damping configuration for the selected object"))

property_widget_layout.addWidget(object_property_table)
property_widget_layout.addWidget(addtodsph_button)
property_widget_layout.addWidget(removefromdsph_button)
property_widget_layout.addWidget(damping_config_button)

properties_scaff_widget.setLayout(property_widget_layout)

properties_widget.setWidget(properties_scaff_widget)

# Different labels to add to the property table
mkgroup_label = QtGui.QLabel("   {}".format(__("MKGroup")))
mkgroup_label.setOpenExternalLinks(True)
mkgroup_label.setToolTip(__("Establishes the object group."))
objtype_label = QtGui.QLabel("   {}".format(__("Type of object")))
objtype_label.setToolTip(__("Establishes the object type: Fluid or bound"))
fillmode_label = QtGui.QLabel("   {}".format(__("Fill mode")))
fillmode_label.setToolTip(__("Sets fill mode.\nFull: generates internal volume and external mesh."
                             "\nSolid: generates only internal volume."
                             "\nFace: generates only external mesh."
                             "\nWire: generates only external mesh polygon edges."))
floatstate_label = QtGui.QLabel("   {}".format(__("Float state")))
floatstate_label.setToolTip(__("Sets floating state for this object MK."))
initials_label = QtGui.QLabel("   {}".format(__("Initials")))
initials_label.setToolTip(__("Sets initials options for this object"))
material_label = QtGui.QLabel("   {}".format(__("Material")))
material_label.setToolTip(__("Sets material for this object"))
motion_label = QtGui.QLabel("   {}".format(__("Motion")))
motion_label.setToolTip(__("Sets motion for this object"))
simplewall_label = QtGui.QLabel("   {}".format(__("Faces")))
simplewall_label.setToolTip(__("Adds faces"))

mkgroup_label.setAlignment(QtCore.Qt.AlignLeft)
material_label.setAlignment(QtCore.Qt.AlignLeft)
objtype_label.setAlignment(QtCore.Qt.AlignLeft)
fillmode_label.setAlignment(QtCore.Qt.AlignLeft)
floatstate_label.setAlignment(QtCore.Qt.AlignLeft)
initials_label.setAlignment(QtCore.Qt.AlignLeft)
motion_label.setAlignment(QtCore.Qt.AlignLeft)

object_property_table.setCellWidget(0, 0, objtype_label)
object_property_table.setCellWidget(1, 0, mkgroup_label)
object_property_table.setCellWidget(2, 0, fillmode_label)
object_property_table.setCellWidget(3, 0, floatstate_label)
object_property_table.setCellWidget(4, 0, initials_label)
object_property_table.setCellWidget(5, 0, motion_label)
object_property_table.setCellWidget(6, 0, simplewall_label)


def mkgroup_change(value):
    """ Defines what happens when MKGroup is changed. """
    selection = FreeCADGui.Selection.getSelection()[0]
    data['simobjects'][selection.Name][0] = value


def objtype_change(index):
    """ Defines what happens when type of object is changed """
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)

    if objtype_prop.itemText(index).lower() == "bound":
        mkgroup_prop.setRange(0, 240)
        if data['simobjects'][selection.Name][1].lower() != "bound":
            mkgroup_prop.setValue(int(utils.get_first_mk_not_used("bound", data)))
        try:
            selectiongui.ShapeColor = (0.80, 0.80, 0.80)
            selectiongui.Transparency = 0
        except AttributeError:
            # Can't change attributes
            pass
        floatstate_prop.setEnabled(True)
        initials_prop.setEnabled(False)
        mkgroup_label.setText(
            "&nbsp;&nbsp;&nbsp;" + __("MKBound") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>"
        )
    elif objtype_prop.itemText(index).lower() == "fluid":
        mkgroup_prop.setRange(0, 10)
        if data['simobjects'][selection.Name][1].lower() != "fluid":
            mkgroup_prop.setValue(int(utils.get_first_mk_not_used("fluid", data)))
        try:
            selectiongui.ShapeColor = (0.00, 0.45, 1.00)
            selectiongui.Transparency = 30
        except AttributeError:
            # Can't change attributes
            pass
        # Remove floating properties if it is changed to fluid
        if str(data['simobjects'][selection.Name][0]) in data['floating_mks'].keys():
            data['floating_mks'].pop(str(data['simobjects'][selection.Name][0]), None)
        # Remove motion properties if it is changed to fluid
        if data['simobjects'][selection.Name][0] in data['motion_mks'].keys():
            data['motion_mks'].pop(data['simobjects'][selection.Name][0], None)
        floatstate_prop.setEnabled(False)
        initials_prop.setEnabled(True)
        mkgroup_label.setText(
            "&nbsp;&nbsp;&nbsp;" + __("MKFluid") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>"
        )

    data['simobjects'][selection.Name][1] = objtype_prop.itemText(index)
    on_tree_item_selection_change()


def fillmode_change(index):
    """ Defines what happens when fill mode is changed """
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
    data['simobjects'][selection.Name][2] = fillmode_prop.itemText(index)

    if fillmode_prop.itemText(index).lower() == "full":
        if objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "fluid":
            try:
                selectiongui.Transparency = 30
            except AttributeError:
                # Cannot change transparency. Just ignore
                pass
        elif objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "bound":
            try:
                selectiongui.Transparency = 0
            except AttributeError:
                # Cannot change transparency. Just ignore
                pass
        wall_prop.setEnabled(False)
        faces_status(selection)
    elif fillmode_prop.itemText(index).lower() == "solid":
        if objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "fluid":
            try:
                selectiongui.Transparency = 30
            except AttributeError:
                # Cannot change transparency (fillbox?). Just ignore
                pass
        elif objtype_prop.itemText(objtype_prop.currentIndex()).lower() == "bound":
            try:
                selectiongui.Transparency = 0
            except AttributeError:
                # Cannot change transparency (fillbox?). Just ignore
                pass
        wall_prop.setEnabled(False)
        faces_status(selection)
    elif fillmode_prop.itemText(index).lower() == "face":
        try:
            selectiongui.Transparency = 80
        except AttributeError:
            # Cannot change transparency. Just ignore
            pass
        wall_prop.setEnabled(True)
        faces_status(selection)
    elif fillmode_prop.itemText(index).lower() == "wire":
        try:
            selectiongui.Transparency = 85
        except AttributeError:
            # Cannot change transparency. Just ignore
            pass
        wall_prop.setEnabled(False)
        faces_status(selection)


def initials_change():
    dsphwidgets.InitialsDialog(data)


def motion_change():
    dsphwidgets.MovementDialog(data)


def floatstate_change():
    dsphwidgets.FloatStateDialog(data)


def faces_change():
    dsphwidgets.FacesDialog(data)


def faces_status(selection):

    if wall_prop.isEnabled():
        pass
    else:
        target_mk = int(data['simobjects'][selection.Name][0])
        name = selection.Label

        if (str(target_mk), name) in data['faces'].keys():
            data['faces'].pop((str(target_mk), name), None)


# Property change widgets
mkgroup_prop = QtGui.QSpinBox()
objtype_prop = QtGui.QComboBox()
fillmode_prop = QtGui.QComboBox()
floatstate_prop = QtGui.QPushButton(__("Configure"))
initials_prop = QtGui.QPushButton(__("Configure"))
motion_prop = QtGui.QPushButton(__("Configure"))
wall_prop = QtGui.QPushButton(__("Configure"))
wall_prop.setEnabled(False)
mkgroup_prop.setRange(0, 240)
objtype_prop.insertItems(0, ['Fluid', 'Bound'])
fillmode_prop.insertItems(1, ['Full', 'Solid', 'Face', 'Wire'])
mkgroup_prop.valueChanged.connect(mkgroup_change)
objtype_prop.currentIndexChanged.connect(objtype_change)
fillmode_prop.currentIndexChanged.connect(fillmode_change)
floatstate_prop.clicked.connect(floatstate_change)
initials_prop.clicked.connect(initials_change)
motion_prop.clicked.connect(motion_change)
wall_prop.clicked.connect(faces_change)
object_property_table.setCellWidget(0, 1, objtype_prop)
object_property_table.setCellWidget(1, 1, mkgroup_prop)
object_property_table.setCellWidget(2, 1, fillmode_prop)
object_property_table.setCellWidget(3, 1, floatstate_prop)
object_property_table.setCellWidget(4, 1, initials_prop)
object_property_table.setCellWidget(5, 1, motion_prop)
object_property_table.setCellWidget(6, 1, wall_prop)


# Dock the widget to the left side of screen
fc_main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)

# By default all is hidden in the widget
object_property_table.hide()
addtodsph_button.hide()
removefromdsph_button.hide()
damping_config_button.hide()


def add_object_to_sim(name=None):
    """ Defines what happens when "Add object to sim" button is presseed.
    Takes the selection of FreeCAD and watches what type of thing it is adding """
    if name is None:
        selection = FreeCADGui.Selection.getSelection()
    else:
        selection = list()
        selection.append(FreeCAD.ActiveDocument.getObject(name))

    for each in selection:
        if each.Name == "Case_Limits" or "_internal_" in each.Name:
            continue
        if len(each.InList) > 0:
            continue
        if each.Name not in data['simobjects'].keys():
            if "fillbox" in each.Name.lower():
                mktoput = utils.get_first_mk_not_used("fluid", data)
                if not mktoput:
                    mktoput = 0
                data['simobjects'][each.Name] = [mktoput, 'fluid', 'solid']
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
    """ Defines what happens when removing objects from
    the simulation """
    selection = FreeCADGui.Selection.getSelection()
    for each in selection:
        if each.Name == "Case_Limits":
            continue
        if each.Name in data['export_order']:
            data['export_order'].remove(each.Name)
        data['simobjects'].pop(each.Name, None)
    on_tree_item_selection_change()


def on_damping_config():
    """ Configures the damping configuration for the selected obejct """
    selection = FreeCADGui.Selection.getSelection()
    guiutils.damping_config_window(data, selection[0].Name)


# Connects buttons to its functions
addtodsph_button.clicked.connect(add_object_to_sim)
removefromdsph_button.clicked.connect(remove_object_from_sim)
damping_config_button.clicked.connect(on_damping_config)

# Find treewidgets of freecad.
trees = list()
for item in fc_main_window.findChildren(QtGui.QTreeWidget):
    if item.objectName() != "DSPH Objects":
        trees.append(item)


def on_up_objectorder(index):
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
    selection = FreeCADGui.Selection.getSelection()
    object_names = list()
    for each in FreeCAD.getDocument("DSPH_Case").Objects:
        object_names.append(each.Name)

    # Detect object deletion
    for key in data['simobjects'].keys():
        if key not in object_names:
            data['simobjects'].pop(key, None)
            data['export_order'].remove(key)

    # Detect damping deletion
    for key in data['damping'].keys():
        if key not in object_names:
            data['damping'].pop(key, None)

    addtodsph_button.setEnabled(True)
    if len(selection) > 0:
        if len(selection) > 1:
            # Multiple objects selected
            addtodsph_button.setText(__("Add all possible objects to DSPH Simulation"))
            object_property_table.hide()
            addtodsph_button.show()
            removefromdsph_button.hide()
            damping_config_button.hide()
            pass
        else:
            # One object selected
            if selection[0].Name == "Case_Limits" or "_internal_" in selection[0].Name:
                object_property_table.hide()
                addtodsph_button.hide()
                removefromdsph_button.hide()
                damping_config_button.hide()
            elif "dampingzone" in selection[0].Name.lower() and selection[0].Name in data['damping'].keys():
                object_property_table.hide()
                addtodsph_button.hide()
                removefromdsph_button.hide()
                damping_config_button.show()
            elif selection[0].Name in data['simobjects'].keys():
                # Show properties on table
                object_property_table.show()
                addtodsph_button.hide()
                removefromdsph_button.show()
                damping_config_button.hide()

                # MK config
                mkgroup_prop.setRange(0, 240)
                to_change = object_property_table.cellWidget(1, 1)
                to_change.setValue(data['simobjects'][selection[0].Name][0])

                # type config
                to_change = object_property_table.cellWidget(0, 1)
                if selection[0].TypeId in temp_data['supported_types']:
                    # Supported object
                    to_change.setEnabled(True)
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        to_change.setCurrentIndex(0)
                        mkgroup_prop.setRange(0, 10)
                        mkgroup_label.setText(
                            "&nbsp;&nbsp;&nbsp;" + __("MKFluid") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>"
                        )
                    elif data['simobjects'][selection[0].Name][1].lower() == "bound":
                        to_change.setCurrentIndex(1)
                        mkgroup_prop.setRange(0, 240)
                        mkgroup_label.setText(
                            "&nbsp;&nbsp;&nbsp;" + __("MKBound") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>"
                        )
                elif "part" in selection[0].TypeId.lower() or "mesh" in selection[0].TypeId.lower() or (
                        selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower()):
                    # Is an object that will be exported to STL
                    to_change.setEnabled(True)
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        to_change.setCurrentIndex(0)
                        mkgroup_prop.setRange(0, 10)
                        mkgroup_label.setText(
                            "&nbsp;&nbsp;&nbsp;" + __("MKFluid") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>"
                        )
                    elif data['simobjects'][selection[0].Name][1].lower() == "bound":
                        to_change.setCurrentIndex(1)
                        mkgroup_prop.setRange(0, 240)
                        mkgroup_label.setText(
                            "&nbsp;&nbsp;&nbsp;" + __("MKBound") + " <a href='http://design.sphysics.org/wiki/doku.php?id=concepts'>?</a>"
                        )
                else:
                    # Everything else
                    to_change.setCurrentIndex(1)
                    to_change.setEnabled(False)

                # fill mode config
                to_change = object_property_table.cellWidget(2, 1)
                if selection[0].TypeId in temp_data['supported_types']:
                    # Object is a supported type. Fill with its type and enable selector.
                    to_change.setEnabled(True)
                    if data['simobjects'][selection[0].Name][2].lower() == "full":
                        to_change.setCurrentIndex(0)
                    elif data['simobjects'][selection[0].Name][2].lower() == "solid":
                        to_change.setCurrentIndex(1)
                    elif data['simobjects'][selection[0].Name][2].lower() == "face":
                        to_change.setCurrentIndex(2)
                    elif data['simobjects'][selection[0].Name][2].lower() == "wire":
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
                to_change = object_property_table.cellWidget(3, 1)
                if selection[0].TypeId in temp_data['supported_types'] or (selection[0].TypeId == "App::DocumentObjectGroup"
                                                                           and "fillbox" in selection[0].Name.lower()):
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        to_change.setEnabled(False)
                    else:
                        to_change.setEnabled(True)

                # initials restrictions
                to_change = object_property_table.cellWidget(4, 1)
                if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                    to_change.setEnabled(True)
                else:
                    to_change.setEnabled(False)

                # motion restrictions
                to_change = object_property_table.cellWidget(5, 1)
                if selection[0].TypeId in temp_data['supported_types'] or "Mesh::Feature" in str(selection[0].TypeId) or \
                        (selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower()):
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        to_change.setEnabled(False)
                    else:
                        to_change.setEnabled(True)

            else:
                if selection[0].InList == list():
                    # Show button to add to simulation
                    addtodsph_button.setText(__("Add to DSPH Simulation"))
                    object_property_table.hide()
                    addtodsph_button.show()
                    removefromdsph_button.hide()
                    damping_config_button.hide()
                else:
                    addtodsph_button.setText(__("Can't add this object to the simulation"))
                    object_property_table.hide()
                    addtodsph_button.show()
                    addtodsph_button.setEnabled(False)
                    removefromdsph_button.hide()
                    damping_config_button.hide()
    else:
        object_property_table.hide()
        addtodsph_button.hide()
        removefromdsph_button.hide()
        damping_config_button.hide()

    # Update dsph objects list
    objectlist_table.clear()
    objectlist_table.setEnabled(True)
    if len(data['export_order']) == 0:
        data['export_order'] = list(data['simobjects'].keys())

    # Substract one that represent case limits object
    if "Case_Limits" in data['export_order']:
        data['export_order'].remove('Case_Limits')

    objectlist_table.setRowCount(len(data['export_order']))
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
        # objectlist_table.setCellWidget(current_row, 0, QtGui.QLabel("   " + context_object.Label))
        target_widget = dsphwidgets.ObjectOrderWidget(
            index=current_row,
            object_mk=data['simobjects'][context_object.Name][0],
            mktype=data['simobjects'][context_object.Name][1],
            object_name=context_object.Label
        )

        target_widget.up.connect(on_up_objectorder)
        target_widget.down.connect(on_down_objectorder)

        if current_row is 0:
            target_widget.disable_up()
        if (current_row + 1) is len(data['export_order']):
            target_widget.disable_down()

        objectlist_table.setCellWidget(current_row, 0, target_widget)

        current_row += 1
    for each in objects_with_parent:
        try:
            data['simobjects'].pop(each, None)
        except ValueError:
            # Not in list, probably because now is part of a compound object
            pass
        data['export_order'].remove(each)
    properties_scaff_widget.adjustSize()
    properties_widget.adjustSize()


# Subscribe the trees to the item selection change function. This helps FreeCAD notify DesignSPHysics for the
# deleted and changed objects to get updated correctly.
for item in trees:
    item.itemSelectionChanged.connect(on_tree_item_selection_change)


# Watch if no object is selected and prevent fillbox rotations
def selection_monitor():
    time.sleep(2.0)
    while True:
        # ensure everything is fine when objects are not selected
        try:
            if len(FreeCADGui.Selection.getSelection()) == 0:
                object_property_table.hide()
                addtodsph_button.hide()
                removefromdsph_button.hide()
                damping_config_button.hide()
        except AttributeError:
            # No object is selected so the selection has no length. Ignore it
            pass
        try:
            # watch fillbox rotations and prevent them
            for o in FreeCAD.getDocument("DSPH_Case").Objects:
                if o.TypeId == "App::DocumentObjectGroup" and "fillbox" in o.Name.lower():
                    for subelem in o.OutList:
                        if subelem.Placement.Rotation.Angle != 0.0:
                            subelem.Placement.Rotation.Angle = 0.0
                            utils.error(__("Can't change rotation!"))
                if "case_limits" in o.Name.lower():
                    if o.Placement.Rotation.Angle != 0.0:
                        o.Placement.Rotation.Angle = 0.0
                        utils.error(__("Can't change rotation!"))
                    if not data['3dmode'] and o.Width.Value != utils.WIDTH_2D:
                        o.Width.Value = utils.WIDTH_2D
                        utils.error(__("Can't change width if the case is in 2D Mode!"))

            # Prevent some view properties of Case Limits to be changed
            case_limits_obj = guiutils.get_fc_view_object("Case_Limits")
            if case_limits_obj is not None:
                if case_limits_obj.DisplayMode != "Wireframe":
                    case_limits_obj.DisplayMode = "Wireframe"
                if case_limits_obj.LineColor != (1.00, 0.00, 0.00):
                    case_limits_obj.LineColor = (1.00, 0.00, 0.00)
                if case_limits_obj.Selectable:
                    case_limits_obj.Selectable = False

            for gn in data["damping"]:
                damping_group = FreeCAD.ActiveDocument.getObject(gn)
                data["damping"][gn].overlimit = damping_group.OutList[1].Length.Value

        except (NameError, AttributeError):
            # DSPH Case not opened, disable things
            guiutils.widget_state_config(widget_state_elements, "no case")
            time.sleep(2.0)
            continue
        time.sleep(0.5)


# Launch a monitor thread that ensures some things are not changed.
monitor_thread = threading.Thread(target=selection_monitor)
monitor_thread.start()

FreeCADGui.activateWorkbench("PartWorkbench")
utils.log(__("Loading data is done."))
