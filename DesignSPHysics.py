#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''
Initializes a complete interface with DualSPHysics suite related operations.

It allows an user to create DualSPHysics compatible cases, automating a bunch of things needed to use them.

More info in http://design.sphysics.org/
'''


from mod.dataobjects.relaxation_zone_file import RelaxationZoneFile
from mod.dataobjects.ml_piston_2d import MLPiston2D
from mod.dataobjects.ml_piston_1d import MLPiston1D
from mod.dataobjects.rotation_file_gen import RotationFileGen
from mod.dataobjects.file_gen import FileGen
from mod.dataobjects.special_movement import SpecialMovement
from mod.dataobjects.simulation_object import SimulationObject
from mod.dataobjects.case import Case
from mod.enums import ObjectType, ObjectFillMode, FreeCADDisplayMode, FreeCADObjectType
from mod.widgets.object_order_widget import ObjectOrderWidget
from mod.widgets.run_dialog import RunDialog
from mod.widgets.measure_tool_grid_dialog import MeasureToolGridDialog
from mod.widgets.info_dialog import InfoDialog
from mod.widgets.execution_parameters_dialog import ExecutionParametersDialog
from mod.widgets.setup_plugin_dialog import SetupPluginDialog
from mod.widgets.constants_dialog import ConstantsDialog
from mod.widgets.case_summary import CaseSummary
from mod.widgets.gencase_completed_dialog import GencaseCompletedDialog
from mod.widgets.mode_2d_config_dialog import Mode2DConfigDialog
from mod.widgets.run_additional_parameters_dialog import RunAdditionalParametersDialog
from mod.widgets.add_geo_dialog import AddGEODialog
from mod.widgets.special_options_selector_dialog import SpecialOptionsSelectorDialog
from mod.widgets.properties_dock_widget import PropertiesDockWidget
from mod.widgets.export_progress_dialog import ExportProgressDialog
from mod.widgets.object_list_table_widget import ObjectListTableWidget
from mod.constants import APP_NAME, PICKLE_PROTOCOL, WIDTH_2D, VERSION, CASE_LIMITS_OBJ_NAME, MAIN_WIDGET_INTERNAL_NAME
from mod.constants import FILLBOX_DEFAULT_LENGTH, FILLBOX_DEFAULT_RADIUS, CASE_LIMITS_2D_LABEL, CASE_LIMITS_3D_LABEL, PROP_WIDGET_INTERNAL_NAME
from mod.constants import DEFAULT_WORKBENCH
from mod.executable_tools import refocus_cwd
from mod.freecad_tools import valid_document_environment, get_fc_object, get_fc_view_object
from mod.freecad_tools import document_count, prompt_close_all_documents, create_dsph_document, get_fc_main_window, create_dsph_document_from_fcstd
from mod.utils import is_compatible_version, open_help, create_flowtool_boxes
from mod.stdout_tools import print_license, debug, error, log, warning, dump_to_disk
from mod.guiutils import widget_state_config,  get_icon, h_line_generator
from mod.dialog_tools import error_dialog, warning_dialog
from mod.translation_tools import __
from mod.xml import XMLExporter
import glob
import sys
import os
import time
import pickle
import threading
import traceback
import subprocess
import shutil
import uuid

import FreeCAD
import FreeCADGui

from PySide import QtGui, QtCore

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

data = {}  # TODO: Delete this

__author__ = "Andrés Vieira"
__copyright__ = "Copyright 2016-2017, DualSHPysics Team"
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

# TODO: Big Change: This should definitely be a custom class like DesignSPHysicsDock(QtGui.QDockWidget)
dsph_main_dock = QtGui.QDockWidget()  # DSPH main dock
# Scaffolding widget, only useful to apply to the dsph_dock widget
dsph_main_dock_scaff_widget = QtGui.QWidget()

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

# Creation of the DSPH Widget.
# Creates a widget with a series of layouts added, to apply to the DSPH dock at the end.
dsph_main_dock.setObjectName(MAIN_WIDGET_INTERNAL_NAME)
dsph_main_dock.setWindowTitle("{} {}".format(APP_NAME, str(__version__)))
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


def on_constants_button_pressed():
    ''' Opens constant definition window on button click. '''
    constants_window = ConstantsDialog()
    # Constant definition window behaviour and general composing
    constants_window.resize(600, 400)
    constants_window.exec_()


constants_button.clicked.connect(on_constants_button_pressed)
widget_state_elements['constants_button'] = constants_button

# Help button that opens a help URL for DesignSPHysics
help_button = QtGui.QPushButton("Help")
help_button.setToolTip(__("Push this button to open a browser with help\non how to use this tool."))
help_button.clicked.connect(open_help)

# Setup window button.
setup_button = QtGui.QPushButton(__("Setup\nPlugin"))
setup_button.setToolTip(__("Setup of the simulator executables"))


def on_setup_button_pressed():
    ''' Opens constant definition window on button click. '''
    setup_window = SetupPluginDialog()
    # Constant definition window behaviour and general composing
    setup_window.resize(600, 400)
    setup_window.exec_()


setup_button.clicked.connect(on_setup_button_pressed)

# Execution parameters button.
execparams_button = QtGui.QPushButton(__("Execution\nParameters"))
execparams_button.setToolTip(__("Change execution parameters, such as\ntime of simulation, viscosity, etc."))

# Opens execution parameters window on button click


def on_execparams_button_presed():
    ''' Opens a dialog to tweak the simulation's execution parameters '''
    execparams_window = ExecutionParametersDialog()
    # Execution parameters window behaviour and general composing
    execparams_window.resize(800, 600)
    execparams_window.exec_()


execparams_button.clicked.connect(on_execparams_button_presed)
widget_state_elements['execparams_button'] = execparams_button

# Logo. Made from a label. Labels can have image as well as text.
logo_label = QtGui.QLabel()
logo_label.setPixmap(get_icon(file_name="logo.png", return_only_path=True))


def on_dp_changed():
    ''' DP Introduction. Changes the dp at the moment the user changes the text. '''
    Case.instance().dp = float(dp_input.text())


# DP Introduction layout
dp_layout = QtGui.QHBoxLayout()
dp_label = QtGui.QLabel(__("Inter-particle distance: "))
dp_label.setToolTip(__("Lower DP to have more particles in the case."))
dp_input = QtGui.QLineEdit()
dp_input.setToolTip(__("Lower DP to have more particles in the case."))
dp_label2 = QtGui.QLabel(" meters")
dp_input.setMaxLength(10)
dp_input.setText(str(Case.instance().dp))
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
casecontrols_bt_newdoc.setToolTip(__("Creates a new case. \nThe opened documents will be closed."))
casecontrols_bt_newdoc.setIcon(get_icon("new.png"))
casecontrols_bt_newdoc.setIconSize(QtCore.QSize(28, 28))
casecontrols_menu_newdoc = QtGui.QMenu()
casecontrols_menu_newdoc.addAction(get_icon("new.png"), __("New"))
casecontrols_menu_newdoc.addAction(get_icon("new.png"), __("Import FreeCAD Document"))
casecontrols_bt_newdoc.setMenu(casecontrols_menu_newdoc)
casecontrols_menu_newdoc.resize(60, 60)

# Save Case button and dropdown
casecontrols_bt_savedoc = QtGui.QToolButton()
casecontrols_bt_savedoc.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
casecontrols_bt_savedoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
casecontrols_bt_savedoc.setText("  {}".format(__("Save\n  Case")))
casecontrols_bt_savedoc.setToolTip(__("Saves the case."))
casecontrols_bt_savedoc.setIcon(get_icon("save.png"))
casecontrols_bt_savedoc.setIconSize(QtCore.QSize(28, 28))
casecontrols_menu_savemenu = QtGui.QMenu()
# casecontrols_menu_savemenu.addAction(get_icon("save.png"), __("Save and run GenCase"))
casecontrols_menu_savemenu.addAction(get_icon("save.png"), __("Save as..."))
casecontrols_bt_savedoc.setMenu(casecontrols_menu_savemenu)
widget_state_elements['casecontrols_bt_savedoc'] = casecontrols_bt_savedoc

# Load Case button
casecontrols_bt_loaddoc = QtGui.QToolButton()
casecontrols_bt_loaddoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
casecontrols_bt_loaddoc.setText("  {}".format(__("Load\n  Case")))
casecontrols_bt_loaddoc.setToolTip(__("Loads a case from disk. All the current documents\nwill be closed."))
casecontrols_bt_loaddoc.setIcon(get_icon("load.png"))
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
rungencase_bt.setIcon(get_icon("run_gencase.png"))
rungencase_bt.setIconSize(QtCore.QSize(12, 12))
widget_state_elements['rungencase_bt'] = rungencase_bt


def on_new_case(prompt=True):
    ''' Defines what happens when new case is clicked. Closes all documents
        if possible and creates a FreeCAD document with Case Limits object. '''

    # Closes all documents as there can only be one open.
    if document_count() > 0:
        new_case_success = prompt_close_all_documents(prompt)
        if not new_case_success:
            return

    # Creates a new document and merges default data to the current data structure.
    Case.instance().reset()
    create_dsph_document()
    widget_state_config(widget_state_elements, "new case")
    Case.instance().add_object(SimulationObject(CASE_LIMITS_OBJ_NAME, -1, ObjectType.SPECIAL, ObjectFillMode.SPECIAL))
    dp_input.setText(str(Case.instance().dp))

    # Forces call to item selection change function so all changes are taken into account
    on_tree_item_selection_change()


def on_new_from_freecad_document(prompt=True):
    ''' Creates a new case based on an existing FreeCAD document.
    This is specially useful for CAD users that want to use existing geometry for DesignSPHysics. '''
    file_name, _ = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), "Select document to import", QtCore.QDir.homePath())

    if document_count() > 0:
        new_case_success = prompt_close_all_documents(prompt)
        if not new_case_success:
            return

    # Creates a new document and merges default data to the current data structure.
    Case.instance().reset()
    create_dsph_document_from_fcstd(file_name)
    widget_state_config(widget_state_elements, "new case")
    Case.instance().add_object_to_sim(SimulationObject(CASE_LIMITS_OBJ_NAME, -1, ObjectType.SPECIAL, ObjectFillMode.SPECIAL))
    dp_input.setText(Case.instance().dp)

    # Forces call to item selection change function so all changes are taken into account
    on_tree_item_selection_change()


def on_save_case(save_as=None):
    ''' Defines what happens when save case button is clicked.
    Saves a freecad scene definition, and a dump of dsph data for the case.'''
    # Watch if save path is available.  Prompt the user if not.
    if (Case.instance().was_not_saved()) or save_as:
        # noinspection PyArgumentList
        save_name, _ = QtGui.QFileDialog.getSaveFileName(dsph_main_dock, __("Save Case"), QtCore.QDir.homePath())
    else:
        save_name = Case.instance().path

    # Check if there is any path, a blank one meant the user cancelled the save file dialog
    if save_name != '':
        project_name = save_name.split('/')[-1]
        # Watch if folder already exists or create it
        if not os.path.exists(save_name):
            os.makedirs(save_name)
        Case.instance().path = save_name
        Case.instance().name = project_name

        # Create out folder for the case
        if not os.path.exists("{}/{}_out".format(save_name, project_name)):
            os.makedirs("{}/{}_out".format(save_name, project_name))

        # Copy files from movements and change its paths to be inside the project.
        for _, mkproperties in Case.instance().mkbasedproperties.items():
            for movement in mkproperties.movements:
                if isinstance(movement, SpecialMovement):
                    if isinstance(movement.generator, FileGen) or isinstance(movement.generator, RotationFileGen):
                        filename = movement.generator.filename
                        debug("Copying {} to {}".format(filename, save_name))

                        # Change directory to de case one, so if file path is already relative it copies it to the
                        # out folder
                        os.chdir(save_name)

                        try:
                            # Copy to project root
                            shutil.copy2(filename, save_name)
                        except shutil.Error:
                            # Probably already copied the file.
                            pass
                        except IOError:
                            error("Unable to copy {} into {}".format(filename, save_name))

                        try:
                            # Copy to project out folder
                            shutil.copy2(filename, save_name + "/" + project_name + "_out")

                            movement.generator.filename = "{}".format(filename.split("/")[-1])
                        except shutil.Error:
                            # Probably already copied the file.
                            pass
                        except IOError:
                            error("Unable to copy {} into {}".format(filename, save_name))

        # Copy files from Acceleration input and change paths to be inside the project folder.
        for aid in Case.instance().acceleration_input.acclist:
            filename = aid.datafile
            debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))

            # Change directory to de case one, so if file path is already relative it copies it to the
            # out folder
            os.chdir(save_name)

            try:
                # Copy to project root
                shutil.copy2(filename, save_name)
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))

            try:
                # Copy to project out folder
                shutil.copy2(filename, save_name + "/" + project_name + "_out")

                aid.datafile = filename.split("/")[-1]

            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))

        # Copy files from pistons and change paths to be inside the project folder.
        for _, mkproperties in Case.instance().mkbasedproperties.items():
            if isinstance(mkproperties.mlayerpiston, MLPiston1D):
                filename = mkproperties.mlayerpiston.filevelx
                debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                # Change directory to de case one, so if file path is already relative it copies it to the
                # out folder
                os.chdir(save_name)

                try:
                    # Copy to project root
                    shutil.copy2(filename, save_name)
                except shutil.Error:
                    # Probably already copied the file.
                    pass
                except IOError:
                    error("Unable to copy {} into {}".format(filename, save_name))

                try:
                    # Copy to project out folder
                    shutil.copy2(filename, save_name + "/" + project_name + "_out")

                    mkproperties.mlayerpiston.filevelx = filename.split("/")[-1]
                except shutil.Error:
                    # Probably already copied the file.
                    pass
                except IOError:
                    error("Unable to copy {} into {}".format(filename, save_name))

            if isinstance(mkproperties.mlayerpiston, MLPiston2D):
                veldata = mkproperties.mlayerpiston.veldata
                for v in veldata:
                    filename = v.filevelx
                    debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                    # Change directory to de case one, so if file path is already relative it copies it to the
                    # out folder
                    os.chdir(save_name)

                    try:
                        # Copy to project root
                        shutil.copy2(filename, save_name)
                    except shutil.Error:
                        # Probably already copied the file.
                        pass
                    except IOError:
                        error("Unable to copy {} into {}".format(filename, save_name))

                    try:
                        # Copy to project out folder
                        shutil.copy2(filename, save_name + "/" + project_name + "_out")

                        v.filevelx = filename.split("/")[-1]
                    except shutil.Error:
                        # Probably already copied the file.
                        pass
                    except IOError:
                        error("Unable to copy {} into {}".format(filename, save_name))

        # Copies files needed for RelaxationZones into the project folder and changes data paths to relative ones.
        if isinstance(Case.instance().relaxation_zone, RelaxationZoneFile):
            # Need to copy the abc_x*_y*.csv file series to the out folder
            filename = Case.instance().relaxation_zone.filesvel

            # Change directory to de case one, so if file path is already relative it copies it to the
            # out folder
            os.chdir(save_name)

            for f in glob.glob("{}*".format(filename)):
                debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                try:
                    # Copy to project root
                    shutil.copy2(f, save_name)
                except shutil.Error:
                    # Probably already copied the file.
                    pass
                except IOError:
                    error("Unable to copy {} into {}".format(filename, save_name))

                try:
                    # Copy to project out folder
                    shutil.copy2(f, save_name + "/" + project_name + "_out")

                    Case.instance().relaxation_zone.filesvel = filename.split("/")[-1]
                except shutil.Error:
                    # Probably already copied the file.
                    pass
                except IOError:
                    error("Unable to copy {} into {}".format(filename, save_name))

        # Dumps all the case data to an XML file.
        XMLExporter().save_to_disk(save_name)

        Case.instance().info.needs_to_run_gencase = False

        # Save data array on disk. It is saved as a binary file with Pickle.
        try:
            with open(save_name + "/casedata.dsphdata", 'wb') as picklefile:
                pickle.dump(Case.instance(), picklefile, PICKLE_PROTOCOL)
        except Exception:
            traceback.print_exc()
            error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))

        refocus_cwd()
    else:
        log(__("Saving cancelled."))


def on_save_with_gencase():
    ''' Saves data into disk and uses GenCase to generate the case files.'''

    # Check if the project is saved, if no shows the following message
    if Case.instance().path == '':
        # Warning window about save_case
        gencase_warning_dialog = QtGui.QMessageBox()
        gencase_warning_dialog.setWindowTitle(__("Warning!"))
        gencase_warning_dialog.setText(__("You need save first!"))
        gencase_warning_dialog.setIcon(QtGui.QMessageBox.Warning)
        gencase_warning_dialog.exec_()

    # Save Case as usual so all the data needed for GenCase is on disk
    on_save_case()
    # Ensure the current working directory is the DesignSPHysics directory
    refocus_cwd()

    # Use gencase if possible to generate the case final definition
    Case.instance().info.is_gencase_done = False
    if Case.instance().executable_paths.gencase != "":
        # Tries to spawn a process with GenCase to generate the case

        process = QtCore.QProcess(fc_main_window)

        if "./" in Case.instance().executable_paths.gencase:
            gencase_full_path = os.getcwd() + "/" + Case.instance().executable_paths.gencase
        else:
            gencase_full_path = Case.instance().executable_paths.gencase

        process.setWorkingDirectory(Case.instance().path)
        process.start(gencase_full_path, [
            Case.instance().path + '/' + Case.instance().name + '_Def', Case.instance().path +
            '/' + Case.instance().name + '_out/' + Case.instance().name,
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
                Case.instance().info.particle_number = total_particles
                log(__("Total number of particles exported: ") + str(total_particles))
                if total_particles < 300:
                    warning(__("Are you sure all the parameters are set right? The number of particles is very low ({}). "
                               "Lower the DP to increase number of particles").format(str(total_particles)))
                elif total_particles > 200000:
                    warning(__("Number of particles is pretty high ({}) "
                               "and it could take a lot of time to simulate.").format(str(total_particles)))
                Case.instance().info.is_gencase_done = True
                widget_state_config(widget_state_elements, "gencase done")
                Case.instance().info.previous_particle_number = int(total_particles)
                gencase_completed_dialog = GencaseCompletedDialog(particle_count=total_particles, detail_text=output.split("================================")[1])
                gencase_completed_dialog.show()
            except ValueError:
                # Not an expected result. GenCase had a not handled error
                error_in_gen_case = True

    # Check if there is any path, a blank one meant the user cancelled the save file dialog
    if Case.instance().path != '':
        # If for some reason GenCase failed
        if str(process.exitCode()) != "0" or error_in_gen_case:
            try:
                # Multiple possible causes. Let the user know
                gencase_out_file = open(Case.instance().path + '/' + Case.instance().name + '_out/' + Case.instance().name + ".out", "r")
                gencase_failed_dialog = QtGui.QMessageBox()
                gencase_failed_dialog.setText(__("Error executing GenCase. Did you add objects to the case?. "
                                                 "Another reason could be memory issues. View details for more info."))
                gencase_failed_dialog.setDetailedText(gencase_out_file.read().split("================================")[1])
                gencase_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
                gencase_out_file.close()
                gencase_failed_dialog.exec_()
                warning(__("GenCase Failed."))
            except:
                warning_dialog(
                    "I can't recognize GenCase in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +R 755 /path/to/the/executable"
                )

        # Save results again so all the data is updated if something changes.
        on_save_case()
    else:
        log(__("Saving cancelled."))

    Case.instance().info.needs_to_run_gencase = True


def on_newdoc_menu(action):
    ''' Handles the new document button and its dropdown items. '''
    if __("New") in action.text():
        on_new_case()
    if __("Import FreeCAD Document") in action.text():
        on_new_from_freecad_document()


def on_save_menu(action):
    ''' Handles the save button and its dropdown items. '''
    if __("Save as...") in action.text():
        on_save_case(save_as=True)


def on_load_button():
    ''' Defines load case button behaviour. This is made so errors can be detected and handled. '''
    try:
        on_load_case()
    except ImportError:
        error_dialog(__("There was an error loading the case"),
                     __("The case you are trying to load has some data that DesignSPHysics could not"
                        " load.\n\nDid you make the case in a previous version?"))
        on_new_case(prompt=False)


def on_load_case():
    '''Defines loading case mechanism.
    Load points to a dsphdata custom file, that stores all the relevant info.
    If FCStd file is not found the project is considered corrupt.'''
    # noinspection PyArgumentList
    load_name, _ = QtGui.QFileDialog.getOpenFileName(dsph_main_dock, __("Load Case"), QtCore.QDir.homePath(), "casedata.dsphdata")
    if load_name == "":
        # User pressed cancel.  No path is selected.
        return

    # Check if FCStd file is in there.
    load_path_project_folder = "/".join(load_name.split("/")[:-1])
    if not os.path.isfile(load_path_project_folder + "/DSPH_Case.FCStd"):
        error_dialog(__("DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."))
        error(__("DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."))
        return

    # Tries to close all documents
    if document_count() > 0:
        load_success = prompt_close_all_documents()
        if not load_success:
            return

    # Opens the case freecad document
    FreeCAD.open(load_path_project_folder + "/DSPH_Case.FCStd")

    # Loads own file and sets data and button behaviour
    global dp_input
    try:
        # Previous versions of DesignSPHysics saved the data on disk in an ASCII way (pickle protocol 0), so sometimes
        # due to OS changes files would be corrupted. Now it is saved in binary mode so that wouldn't happen. This bit
        # of code is to open files which have an error (or corrupted binary files!).
        with open(load_name, 'rb') as load_picklefile:
            try:
                load_disk_data = pickle.load(load_picklefile)
            except AttributeError:
                error_dialog(__("There was an error trying to load the case. This can be due to the project being "
                                "from another version or an error while saving the case."))
                on_new_case(prompt=False)
                return

        # Remove exec paths from loaded data if user have already correct ones.
        already_correct = Case.instance().executable_paths.check_and_filter()
        if already_correct:
            for x in ['gencase_path', 'dsphysics_path', 'partvtk4_path', 'floatinginfo_path', 'computeforces_path', 'measuretool_path', 'isosurface_path', 'boundaryvtk_path']:
                load_disk_data.pop(x, None)

        # Update data structure with disk loaded one
        data.update(load_disk_data)  # TODO: Update mechanism for new data
    except (EOFError, ValueError):
        error_dialog(
            __("There was an error importing the case  You probably need to set them again."
               "\n\n"
               "This could be caused due to file corruption, "
               "caused by operating system based line endings or ends-of-file, or other related aspects."))

    # Fill some data
    dp_input.setText(str(Case.instance().dp))

    Case.instance().path = load_path_project_folder
    Case.instance().name = load_path_project_folder.split("/")[-1]

    # Adapt widget state to case info
    widget_state_config(widget_state_elements, "load base")
    if Case.instance().info.is_gencase_done:
        widget_state_config(widget_state_elements, "gencase done")
    else:
        widget_state_config(widget_state_elements, "gencase not done")

    if Case.instance().info.is_simulation_done:
        widget_state_config(widget_state_elements, "simulation done")
    else:
        widget_state_config(widget_state_elements, "simulation not done")

    # Check executable paths
    refocus_cwd()
    correct_execs = Case.instance().executable_paths.check_and_filter()
    if not correct_execs:
        widget_state_config(widget_state_elements, "execs not correct")

    # Update FreeCAD case state
    on_tree_item_selection_change()


def on_add_fillbox():
    ''' Add fillbox group. It consists in a group with 2 objects inside: a point and a box.
    The point represents the fill seed and the box sets the bounds for the filling. '''

    fillbox_gp = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.FOLDER, "FillBox")
    fillbox_point = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.SPHERE, "FillPoint")
    fillbox_limits = FreeCAD.ActiveDocument.addObject(FreeCADObjectType.BOX, "FillLimit")
    fillbox_limits.Length = FILLBOX_DEFAULT_LENGTH
    fillbox_limits.Width = FILLBOX_DEFAULT_LENGTH
    fillbox_limits.Height = FILLBOX_DEFAULT_LENGTH
    fillbox_limits.ViewObject.DisplayMode = FreeCADDisplayMode.WIREFRAME
    fillbox_limits.ViewObject.LineColor = (0.00, 0.78, 1.00)
    fillbox_point.Radius.Value = FILLBOX_DEFAULT_RADIUS
    fillbox_point.Placement.Base = FreeCAD.Vector(500, 500, 500)
    fillbox_point.ViewObject.ShapeColor = (0.00, 0.00, 0.00)
    fillbox_gp.addObject(fillbox_limits)
    fillbox_gp.addObject(fillbox_point)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def on_add_geo():
    ''' Add STL file. Opens a file opener and allows the user to set parameters for the import process '''

    file_name = QtGui.QFileDialog().getOpenFileName(fc_main_window, __("Select GEO to import"), QtCore.QDir.homePath(), "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk)")

    if not file_name:
        return

    add_geo_dialog = AddGEODialog(file_name)
    add_geo_dialog.exec_()


def on_summary():
    ''' Handles Case Summary button '''
    case_summary_dialog = CaseSummary()
    case_summary_dialog.exec_()


def on_2d_toggle():
    ''' Handles Toggle 3D/2D Button. Changes the Case Limits object accordingly. '''
    if valid_document_environment():
        if Case.instance().mode3d:
            # Change to 2D

            Mode2DConfigDialog().exec_()

            # Toggle 3D Mode and change name
            Case.instance().mode3d = not Case.instance().mode3d
            get_fc_object(CASE_LIMITS_OBJ_NAME).Label = CASE_LIMITS_3D_LABEL if Case.instance().mode3d else CASE_LIMITS_2D_LABEL
        else:
            # Toggle 3D Mode and change name
            Case.instance().mode3d = not Case.instance().mode3d

            # Try to restore original Width.
            if Case.instance().info.last_3d_width > 0.0:
                get_fc_object(CASE_LIMITS_OBJ_NAME).Width = Case.instance().info.last_3d_width
            else:
                get_fc_object(CASE_LIMITS_OBJ_NAME).Width = get_fc_object(CASE_LIMITS_OBJ_NAME).Length

            get_fc_view_object(CASE_LIMITS_OBJ_NAME).DisplayMode = FreeCADDisplayMode.WIREFRAME
            get_fc_view_object(CASE_LIMITS_OBJ_NAME).ShapeColor = (0.80, 0.80, 0.80)
            get_fc_view_object(CASE_LIMITS_OBJ_NAME).Transparency = 0

            get_fc_object(CASE_LIMITS_OBJ_NAME).Label = CASE_LIMITS_3D_LABEL if Case.instance().mode3d else CASE_LIMITS_2D_LABEL
    else:
        error("Not a valid case environment")


def on_special_button():
    ''' Spawns a dialog with special options. This is only a selector '''

    SpecialOptionsSelectorDialog().exec_()


# Connect case control buttons to respective handlers
casecontrols_bt_newdoc.clicked.connect(on_new_case)
casecontrols_bt_savedoc.clicked.connect(on_save_case)
rungencase_bt.clicked.connect(on_save_with_gencase)
casecontrols_menu_newdoc.triggered.connect(on_newdoc_menu)
casecontrols_menu_savemenu.triggered.connect(on_save_menu)
casecontrols_bt_loaddoc.clicked.connect(on_load_button)
casecontrols_bt_addfillbox.clicked.connect(on_add_fillbox)
casecontrols_bt_addgeo.clicked.connect(on_add_geo)
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
    ''' Defines what happens on simulation button press.
    It shows the run window and starts a background process
    with dualsphysics running. Updates the window with useful info.'''

    if not Case.instance().info.needs_to_run_gencase:
        # Warning window about save_case
        run_warning_dialog = QtGui.QMessageBox()
        run_warning_dialog.setWindowTitle(__("Warning!"))
        run_warning_dialog.setText(__("It is necessary that you run Run GenCase again, otherwise, maybe the results obtained may not be as expected..."))
        run_warning_dialog.setIcon(QtGui.QMessageBox.Warning)
        run_warning_dialog.exec_()

    run_dialog = RunDialog()
    run_dialog.run_progbar_bar.setValue(0)
    Case.instance().info.is_simulation_done = False
    widget_state_config(widget_state_elements, "sim start")
    run_dialog.run_button_cancel.setText(__("Cancel Simulation"))
    run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
    run_dialog.run_group_label_case.setText(__("Case name: ") + Case.instance().name)
    run_dialog.run_group_label_proc.setText(__("Simulation processor: ") + str(ex_selector_combo.currentText()))
    run_dialog.run_group_label_part.setText(__("Number of particles: ") + str(Case.instance().info.particle_number))
    run_dialog.run_group_label_partsout.setText(__("Total particles out: ") + "0")
    run_dialog.run_group_label_eta.setText(__("Estimated time to complete simulation: ") + __("Calculating..."))

    # Cancel button handler
    def on_cancel():
        log(__("Stopping simulation"))
        if Case.instance().info.current_process:
            Case.instance().info.current_process.kill()
        run_dialog.hide()
        run_dialog.run_details.hide()
        Case.instance().info.is_simulation_done = False
        widget_state_config(widget_state_elements, "sim cancel")

    run_dialog.run_button_cancel.clicked.connect(on_cancel)

    def on_details():
        ''' Details button handler. Opens and closes the details pane on the execution window.'''
        if run_dialog.run_details.isVisible():
            debug('Hiding details pane on execution')
            run_dialog.run_details.hide()
        else:
            debug('Showing details pane on execution')
            run_dialog.run_details.show()
            run_dialog.run_details.move(run_dialog.x() - run_dialog.run_details.width() - 15, run_dialog.y())

    # Ensure run button has no connections
    try:
        run_dialog.run_button_details.clicked.disconnect()
    except RuntimeError:
        pass

    run_dialog.run_button_details.clicked.connect(on_details)

    # Launch simulation and watch filesystem to monitor simulation
    filelist = [f for f in os.listdir(Case.instance().path + '/' + Case.instance().name + "_out/") if f.startswith("Part")]
    for f in filelist:
        os.remove(Case.instance().path + '/' + Case.instance().name + "_out/" + f)

    def on_dsph_sim_finished(exit_code):
        ''' Simulation finish handler. Defines what happens when the process finishes.'''

        # Reads output and completes the progress bar
        output = Case.instance().info.current_process.readAllStandardOutput()
        run_dialog.run_details_text.setText(str(output))
        run_dialog.run_details_text.moveCursor(QtGui.QTextCursor.End)
        run_dialog.run_watcher.removePath(Case.instance().path + '/' + Case.instance().name + "_out/")
        run_dialog.setWindowTitle(__("DualSPHysics Simulation: Complete"))
        run_dialog.run_progbar_bar.setValue(100)
        run_dialog.run_button_cancel.setText(__("Close"))

        if exit_code == 0:
            # Simulation went correctly
            Case.instance().info.is_simulation_done = True
            widget_state_config(widget_state_elements, "sim finished")
        else:
            # In case of an error
            if "exception" in str(output).lower():
                error(__("Exception in execution."))
                run_dialog.setWindowTitle(__("DualSPHysics Simulation: Error"))
                run_dialog.run_progbar_bar.setValue(0)
                run_dialog.hide()
                widget_state_config(widget_state_elements, "sim error")
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
    Case.instance().info.current_process = process
    static_params_exe = [
        Case.instance().path + '/' + Case.instance().name + "_out/" +
        Case.instance().name, Case.instance().path +
        '/' + Case.instance().name + "_out/",
        "-svres", "-" + str(ex_selector_combo.currentText()).lower()
    ]

    additional_params_ex = list()
    if Case.instance().info.run_additional_parameters:
        additional_params_ex = Case.instance().info.run_additional_parameters.split(" ")

    final_params_ex = static_params_exe + additional_params_ex
    Case.instance().info.current_process.start(Case.instance().executable_paths.dsphysics, final_params_ex)

    def on_fs_change():
        ''' Executed each time the filesystem changes. This updates the percentage of the simulation and its details.'''
        run_file_data = ''
        try:
            with open(Case.instance().path + '/' + Case.instance().name + "_out/Run.out", "r") as run_file:
                run_file_data = run_file.readlines()
        except Exception:
            pass

        # Fill details window
        run_dialog.run_details_text.setText("".join(run_file_data))
        run_dialog.run_details_text.moveCursor(QtGui.QTextCursor.End)

        # Set percentage scale based on timemax
        for l in run_file_data:
            if Case.instance().execution_parameters.timemax == -1:
                if "TimeMax=" in l:
                    Case.instance().execution_parameters.timemax = float(l.split("=")[1])

        # Update execution metrics on GUI
        last_part_lines = list(filter(lambda x: "Part_" in x and "stored" not in x and "      " in x, run_file_data))
        if last_part_lines:
            current_value = (float(last_part_lines[-1].split("      ")[1]) * float(100)) / float(Case.instance().execution_parameters.timemax)
            run_dialog.run_progbar_bar.setValue(current_value)
            run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format(str(format(current_value, ".2f"))))
            run_dialog.run_group_label_eta.setText(__("Estimated time to complete simulation: ") + last_part_lines[-1].split("  ")[-1])

        # Update particles out on GUI
        last_particles_out_lines = list(filter(lambda x: "(total: " in x and "Particles out:" in x, run_file_data))
        if last_particles_out_lines:
            dump_to_disk("".join(last_particles_out_lines))
            totalpartsout = int(last_particles_out_lines[-1].split("(total: ")[1].split(")")[0])
            Case.instance().info.particles_out = totalpartsout
            run_dialog.run_group_label_partsout.setText(__("Total particles out: {}").format(str(Case.instance().info.particles_out)))

    # Set filesystem watcher to the out directory.
    run_dialog.run_watcher.addPath(Case.instance().path + '/' + Case.instance().name + "_out/")
    run_dialog.run_watcher.directoryChanged.connect(on_fs_change)

    Case.instance().info.needs_to_run_gencase = False

    # Handle error on simulation start
    if Case.instance().info.current_process.state() == QtCore.QProcess.NotRunning:
        # Probably error happened.
        run_dialog.run_watcher.removePath(Case.instance().path + '/' + Case.instance().name + "_out/")
        Case.instance().info.current_process = ""
        exec_not_correct_dialog = QtGui.QMessageBox()
        exec_not_correct_dialog.setText(__("Error on simulation start. Is the path of DualSPHysics correctly placed?"))
        exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Critical)
        exec_not_correct_dialog.exec_()
    else:
        run_dialog.show()


def on_additional_parameters():
    ''' Handles additional parameters button for execution '''
    RunAdditionalParametersDialog().exec_()


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
ex_button.setIcon(get_icon("run.png"))
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
export_dialog = ExportProgressDialog()


def partvtk_export(export_parameters):
    ''' Export VTK button behaviour.
    Launches a process while disabling the button. '''
    widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_partvtk_button'].setText("Exporting...")

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()
            widget_state_elements['post_proc_partvtk_button'].setText(
                __("PartVTK"))
        widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_dialog.on_cancel.connect(on_cancel)

    # PartVTK export finish handler
    def on_export_finished(exit_code):
        widget_state_elements['post_proc_partvtk_button'].setText(__("PartVTK"))
        widget_state_config(widget_state_elements, "export finished")

        export_dialog.hide()

        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("PartVTK finished successfully"),
                detailed_text=Case.instance().info.current_output
            )
        else:
            error_dialog(
                __("There was an error on the post-processing. Show details to view the errors."),
                detailed_text=Case.instance().info.current_output
            )

        # Bit of code that tries to open ParaView if the option was selected.
        if export_parameters['open_paraview']:
            formats = {0: "vtk", 1: "csv", 2: "asc"}
            subprocess.Popen(
                [
                    Case.instance().executable_paths.paraview,
                    "--data={}\\{}_..{}".format(Case.instance().path + '\\' + Case.instance().name + '_out',
                                                export_parameters['file_name'], formats[export_parameters['save_mode']])
                ],
                stdout=subprocess.PIPE)

    Case.instance().info.current_output = ""
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
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        save_mode + Case.instance().path + '/' + Case.instance().name +
        '_out/' + export_parameters['file_name'],
        '-onlytype:' + export_parameters['save_types'] +
        " " + export_parameters['additional_parameters']
    ]

    debug("Going to execute: {} {}".format(Case.instance().executable_paths.partvtk4, " ".join(static_params_exp)))

    # Start process
    export_process.start(Case.instance().executable_paths.partvtk4, static_params_exp)
    Case.instance().info.current_export_process = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
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
            current_part = export_dialog.get_value()
        export_dialog.set_value(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def on_partvtk():
    ''' Opens a dialog with PartVTK exporting options '''
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
    for x in [pvtk_types_chk_all,
              pvtk_types_chk_bound,
              pvtk_types_chk_fluid,
              pvtk_types_chk_fixed,
              pvtk_types_chk_moving,
              pvtk_types_chk_floating]:
        pvtk_types_groupbox_layout.addWidget(x)

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
    pvtk_open_at_end.setEnabled(Case.instance().executable_paths.paraview != "")

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
        ''' Cancel button behaviour '''
        partvtk_tool_dialog.reject()

    def on_pvtk_export():
        ''' Export button behaviour '''
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

        if pvtk_file_name_text.text():
            export_parameters['file_name'] = pvtk_file_name_text.text()
        else:
            export_parameters['file_name'] = 'ExportedPart'

        if pvtk_parameters_text.text():
            export_parameters['additional_parameters'] = pvtk_parameters_text.text(
            )
        else:
            export_parameters['additional_parameters'] = ''

        partvtk_export(export_parameters)
        partvtk_tool_dialog.accept()

    def on_pvtk_type_all_change(state):
        ''' 'All' type selection handler '''
        if state == QtCore.Qt.Checked:
            for chk in [pvtk_types_chk_bound,
                        pvtk_types_chk_fluid,
                        pvtk_types_chk_fixed,
                        pvtk_types_chk_moving,
                        pvtk_types_chk_floating]:
                chk.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_bound_change(state):
        ''' 'Bound' type selection handler '''
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_fluid_change(state):
        ''' 'Fluid' type selection handler '''
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_fixed_change(state):
        ''' 'Fixed' type selection handler '''
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_moving_change(state):
        ''' 'Moving' type selection handler '''
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_type_floating_change(state):
        ''' 'Floating' type selection handler '''
        if state == QtCore.Qt.Checked:
            pvtk_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_pvtk_export_format_change(_):
        ''' Export format combobox handler'''
        if "vtk" in outformat_combobox.currentText().lower() and Case.instance().executable_paths.paraview != "":
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
    ''' FloatingInfo tool export. '''
    widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_floatinginfo_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()
            widget_state_elements['post_proc_floatinginfo_button'].setText(__("FloatingInfo"))
        widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_dialog.on_cancel.connect(on_cancel)

    def on_export_finished(exit_code):
        widget_state_elements['post_proc_floatinginfo_button'].setText(__("FloatingInfo"))
        widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()
        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("FloatingInfo finished successfully"),
                detailed_text=Case.instance().info.current_output)
        else:
            error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    static_params_exp = [
        '-dirin ' + Case.instance().path + '/' + Case.instance().name +
        '_out/', '-savemotion',
        '-savedata ' + Case.instance().path + '/' + Case.instance().name + '_out/' +
        export_parameters['filename'], export_parameters['additional_parameters']
    ]

    if export_parameters['onlyprocess']:
        static_params_exp.append('-onlymk:' + export_parameters['onlyprocess'])

    export_process.start(Case.instance().executable_paths.floatinginfo, static_params_exp)
    Case.instance().info.current_export_process = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("Part_")[1].split("  ")[0]
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def on_floatinginfo():
    ''' Opens a dialog with FloatingInfo exporting options '''
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
        ''' Cancel button behaviour.'''
        floatinfo_tool_dialog.reject()

    def on_finfo_export():
        ''' Export button behaviour.'''
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
    ''' ComputeForces tool export. '''
    widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_computeforces_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()
            widget_state_elements['post_proc_computeforces_button'].setText(__("ComputeForces"))
        widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_dialog.on_cancel.connect(on_cancel)

    def on_export_finished(exit_code):
        widget_state_elements['post_proc_computeforces_button'].setText(__("ComputeForces"))
        widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()
        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("ComputeForces finished successfully."),
                detailed_text=Case.instance().info.current_output
            )
        else:
            error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
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
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        '-filexml ' + Case.instance().path + '/' +
        Case.instance().name + '_out/' + Case.instance().name + '.xml',
        save_mode + Case.instance().path + '/' + Case.instance().name + '_out/' +
        export_parameters['filename'], export_parameters['additional_parameters']
    ]

    if export_parameters['onlyprocess']:
        static_params_exp.append(export_parameters['onlyprocess_tag'] + export_parameters['onlyprocess'])

    export_process.start(Case.instance().executable_paths.computeforces, static_params_exp)
    Case.instance().info.current_export_process = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("Part_")[1].split(".bi4")[0]
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(
        on_stdout_ready)


def on_computeforces():
    ''' Opens a dialog with ComputeForces exporting options '''
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
        ''' Cancel button behaviour.'''
        compforces_tool_dialog.reject()

    def on_cfces_export():
        ''' Export button behaviour.'''
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
    ''' MeasureTool tool export. '''
    widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_measuretool_button'].setText("Exporting...")

    # Find total export parts
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()
            widget_state_elements['post_proc_measuretool_button'].setText(__("MeasureTool"))
        widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_dialog.on_cancel.connect(on_cancel)

    def on_export_finished(exit_code):
        widget_state_elements['post_proc_measuretool_button'].setText(__("MeasureTool"))
        widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()
        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("MeasureTool finished successfully."),
                detailed_text=Case.instance().info.current_output
            )
        else:
            error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
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
    if len(Case.instance().info.measuretool_points) > len(Case.instance().info.measuretool_grid):
        # Save points
        with open(Case.instance().path + '/' + 'points.txt', 'w') as f:
            f.write("POINTS\n")
            for curr_point in Case.instance().info.measuretool_points:
                f.write("{}  {}  {}\n".format(*curr_point))
    else:
        # Save grid
        with open(Case.instance().path + '/' + 'points.txt', 'w') as f:
            for curr_point in Case.instance().info.measuretool_grid:
                f.write("POINTSLIST\n")
                f.write("{}  {}  {}\n{}  {}  {}\n{}  {}  {}\n".format(*curr_point))

    calculate_height = '-height' if export_parameters['calculate_water_elevation'] else ''

    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        '-filexml ' + Case.instance().path + '/' +
        Case.instance().name + '_out/' + Case.instance().name + '.xml',
        save_mode + Case.instance().path + '/' +
        Case.instance().name + '_out/' + export_parameters['filename'],
        '-points ' + Case.instance().path + '/points.txt', '-vars:' +
        export_parameters['save_vars'], calculate_height,
        export_parameters['additional_parameters']
    ]

    export_process.start(Case.instance().executable_paths.measuretool, static_params_exp)
    Case.instance().info.current_export_process = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("/Part_")[1].split(".bi4")[0]
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def on_measuretool():
    ''' Opens a dialog with MeasureTool exporting options '''
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
    for x in [mtool_types_chk_all,
              mtool_types_chk_vel,
              mtool_types_chk_rhop,
              mtool_types_chk_press,
              mtool_types_chk_mass,
              mtool_types_chk_vol,
              mtool_types_chk_idp,
              mtool_types_chk_ace,
              mtool_types_chk_vor,
              mtool_types_chk_kcorr]:
        mtool_types_groupbox_layout.addWidget(x)

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
        ''' Cancel button behaviour.'''
        measuretool_tool_dialog.reject()

    def on_mtool_export():
        ''' Export button behaviour.'''
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

        if mtool_file_name_text.text():
            export_parameters['filename'] = mtool_file_name_text.text()
        else:
            export_parameters['filename'] = 'MeasurePart'

        if mtool_parameters_text.text():
            export_parameters['additional_parameters'] = mtool_parameters_text.text()
        else:
            export_parameters['additional_parameters'] = ''

        measuretool_export(export_parameters)
        measuretool_tool_dialog.accept()

    def on_mtool_measure_all_change(state):
        ''' 'All' checkbox behaviour'''
        if state == QtCore.Qt.Checked:
            for chk in [mtool_types_chk_vel,
                        mtool_types_chk_rhop,
                        mtool_types_chk_press,
                        mtool_types_chk_mass,
                        mtool_types_chk_vol,
                        mtool_types_chk_idp,
                        mtool_types_chk_ace,
                        mtool_types_chk_vor,
                        mtool_types_chk_kcorr]:
                chk.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_measure_single_change(state):
        ''' Behaviour for all checkboxes except 'All' '''
        if state == QtCore.Qt.Checked:
            mtool_types_chk_all.setCheckState(QtCore.Qt.Unchecked)

    def on_mtool_set_points():
        ''' Point list button behaviour.'''
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

        for i, point in enumerate(Case.instance().info.measuretool_points):
            mpoints_table.setItem(i, 0, QtGui.QTableWidgetItem(str(point[0])))
            mpoints_table.setItem(i, 1, QtGui.QTableWidgetItem(str(point[1])))
            mpoints_table.setItem(i, 2, QtGui.QTableWidgetItem(str(point[2])))

        def on_mpoints_accept():
            ''' MeasureTool points dialog accept button behaviour. '''
            Case.instance().info.measuretool_points = list()
            for mtool_row in range(0, mpoints_table.rowCount()):
                try:
                    current_point = [
                        float(mpoints_table.item(mtool_row, 0).text()),
                        float(mpoints_table.item(mtool_row, 1).text()),
                        float(mpoints_table.item(mtool_row, 2).text())
                    ]
                    Case.instance().info.measuretool_points.append(current_point)
                except (ValueError, AttributeError):
                    pass

            # Deletes the grid points (not compatible together)
            Case.instance().info.measuretool_grid = list()
            measurepoints_tool_dialog.accept()

        def on_mpoints_cancel():
            ''' MeasureTool points dialog cancel button behaviour. '''
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

        measuregrid_tool_dialog = MeasureToolGridDialog()
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
    ''' Export IsoSurface button behaviour.
    Launches a process while disabling the button. '''
    widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_isosurface_button'].setText("Exporting...")

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()
            widget_state_elements['post_proc_isosurface_button'].setText(__("IsoSurface"))
        widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_dialog.on_cancel.connect(on_cancel)

    # IsoSurface export finish handler
    def on_export_finished(exit_code):
        widget_state_elements['post_proc_isosurface_button'].setText(__("IsoSurface"))
        widget_state_config(widget_state_elements, "export finished")

        export_dialog.hide()

        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("IsoSurface finished successfully."),
                detailed_text=Case.instance().info.current_output)
        else:
            error_dialog(
                __("There was an error on the post-processing."),
                detailed_text=Case.instance().info.current_output
            )

        # Bit of code that tries to open ParaView if the option was selected.
        if export_parameters['open_paraview']:
            subprocess.Popen(
                [Case.instance().executable_paths.paraview, "--data={}\\{}_..{}".format(
                    Case.instance().path + '\\' + Case.instance().name + '_out',
                    export_parameters['file_name'], "vtk")],
                stdout=subprocess.PIPE)

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    # Build parameters
    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        export_parameters["surface_or_slice"] + " " + Case.instance().path + '/' +
        Case.instance().name + '_out/' + export_parameters['file_name'] +
        " " + export_parameters['additional_parameters']
    ]

    # Start process
    export_process.start(Case.instance().executable_paths.isosurface, static_params_exp)
    Case.instance().info.current_export_process = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(export_parameters['file_name']))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def on_isosurface():
    ''' Opens a dialog with IsoSurface exporting options '''
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
    isosfc_open_at_end.setEnabled(Case.instance().executable_paths.paraview != "")

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
        ''' IsoSurface dialog cancel button behaviour.'''
        isosurface_tool_dialog.reject()

    def on_isosfc_export():
        ''' IsoSurface dialog export button behaviour.'''
        export_parameters = dict()

        if "surface" in isosfc_selector.currentText().lower():
            export_parameters['surface_or_slice'] = '-saveiso'
        else:
            export_parameters['surface_or_slice'] = '-saveslice'

        if isosfc_file_name_text.text():
            export_parameters['file_name'] = isosfc_file_name_text.text()
        else:
            export_parameters['file_name'] = 'IsoFile'

        if isosfc_parameters_text.text():
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
    ''' Export FlowTool button behaviour.
    Launches a process while disabling the button. '''
    widget_state_config(widget_state_elements, "export start")
    widget_state_elements['post_proc_flowtool_button'].setText("Exporting...")

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()
            widget_state_elements['post_proc_flowtool_button'].setText(__("FlowTool"))
        widget_state_config(widget_state_elements, "export cancel")
        export_dialog.hide()

    export_dialog.on_cancel.connect(on_cancel)

    # FlowTool export finish handler
    def on_export_finished(exit_code):
        widget_state_elements['post_proc_flowtool_button'].setText(__("FlowTool"))
        widget_state_config(widget_state_elements, "export finished")
        export_dialog.hide()

        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("FlowTool finished successfully."),
                detailed_text=Case.instance().info.current_output)
        else:
            error_dialog(
                __("There was an error on the post-processing."),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)

    # Build parameters
    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        '-fileboxes ' + Case.instance().path + '/' + 'fileboxes.txt',
        '-savecsv ' + Case.instance().path + '/' + Case.instance().name +
        '_out/' + '{}.csv'.format(export_parameters['csv_name']),
        '-savevtk ' + Case.instance().path + '/' + Case.instance().name + '_out/' + '{}.vtk'.format(
            export_parameters['vtk_name']) +
        " " + export_parameters['additional_parameters']
    ]

    # Start process
    export_process.start(Case.instance().executable_paths.flowtool, static_params_exp)
    Case.instance().info.current_export_process = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(export_parameters['vtk_name']))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def on_flowtool():
    ''' Opens a dialog with FlowTool exporting options '''
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
        ''' Box edit button behaviour. Opens a dialog to edit the selected FlowTool Box'''
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
            error_dialog("There was an error opening the box to edit")
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
        box_edit_image.setPixmap(get_icon("flowtool_template.jpg", return_only_path=True))
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
            ''' FlowTool box edit ok behaviour.'''
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
            ''' FlowTool box edit cancel button behaviour.'''
            box_edit_dialog.reject()

        box_edit_button_ok.clicked.connect(on_ok)
        box_edit_button_cancel.clicked.connect(on_cancel)

        box_edit_dialog.exec_()

    def box_delete(box_id):
        ''' Box delete button behaviour. Tries to find the box for which the button was pressed and deletes it.'''
        box_to_remove = None
        for box in data['flowtool_boxes']:
            if box[0] == box_id:
                box_to_remove = box
        if box_to_remove is not None:
            data['flowtool_boxes'].remove(box_to_remove)
            refresh_boxlist()

    def refresh_boxlist():
        ''' Refreshes the FlowTool box list.'''
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
        ''' Adds a box to the data structure.'''
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
        ''' FlowTool cancel button behaviour.'''
        flowtool_tool_dialog.reject()

    def on_fltool_export():
        ''' FlowTool export button behaviour.'''
        export_parameters = dict()

        if fltool_csv_file_name_text.text():
            export_parameters['csv_name'] = fltool_csv_file_name_text.text()
        else:
            export_parameters['csv_name'] = '_ResultFlow'

        if fltool_vtk_file_name_text.text():
            export_parameters['vtk_name'] = fltool_vtk_file_name_text.text()
        else:
            export_parameters['vtk_name'] = 'Boxes'

        if fltool_parameters_text.text():
            export_parameters['additional_parameters'] = fltool_parameters_text.text()
        else:
            export_parameters['additional_parameters'] = ''

        create_flowtool_boxes(Case.instance().path + '/' + 'fileboxes.txt', data['flowtool_boxes'])

        flowtool_export(export_parameters)
        flowtool_tool_dialog.accept()

    fltool_addbox_button.clicked.connect(on_fltool_addbox)
    fltool_export_button.clicked.connect(on_fltool_export)
    fltool_cancel_button.clicked.connect(on_fltool_cancel)
    refresh_boxlist()
    flowtool_tool_dialog.exec_()


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
post_proc_flowtool_button = QtGui.QPushButton(__("FlowTool"))

post_proc_partvtk_button.setToolTip(__("Opens the PartVTK tool."))
post_proc_computeforces_button.setToolTip(__("Opens the ComputeForces tool."))
post_proc_floatinginfo_button.setToolTip(__("Opens the FloatingInfo tool."))
post_proc_measuretool_button.setToolTip(__("Opens the MeasureTool tool."))
post_proc_isosurface_button.setToolTip(__("Opens the IsoSurface tool."))
post_proc_flowtool_button.setToolTip(__("Opens the FlowTool tool."))

widget_state_elements['post_proc_partvtk_button'] = post_proc_partvtk_button
widget_state_elements['post_proc_computeforces_button'] = post_proc_computeforces_button
widget_state_elements['post_proc_floatinginfo_button'] = post_proc_floatinginfo_button
widget_state_elements['post_proc_measuretool_button'] = post_proc_measuretool_button
widget_state_elements['post_proc_isosurface_button'] = post_proc_isosurface_button
widget_state_elements['post_proc_flowtool_button'] = post_proc_flowtool_button

post_proc_partvtk_button.clicked.connect(on_partvtk)
post_proc_computeforces_button.clicked.connect(on_computeforces)
post_proc_floatinginfo_button.clicked.connect(on_floatinginfo)
post_proc_measuretool_button.clicked.connect(on_measuretool)
post_proc_isosurface_button.clicked.connect(on_isosurface)
post_proc_flowtool_button.clicked.connect(on_flowtool)

export_layout.addWidget(export_label)
export_first_row_layout.addWidget(post_proc_partvtk_button)
export_first_row_layout.addWidget(post_proc_computeforces_button)
export_first_row_layout.addWidget(post_proc_isosurface_button)
export_second_row_layout.addWidget(post_proc_floatinginfo_button)
export_second_row_layout.addWidget(post_proc_measuretool_button)
export_second_row_layout.addWidget(post_proc_flowtool_button)
export_layout.addLayout(export_first_row_layout)
export_layout.addLayout(export_second_row_layout)

# Object list table scaffolding
object_list_table_widget = ObjectListTableWidget()
widget_state_elements['object_list_table_widget'] = object_list_table_widget
Case.instance().info.objectlist_table = object_list_table_widget

# called before objectlist_table


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
main_layout.addWidget(h_line_generator())
main_layout.addLayout(intro_layout)
main_layout.addWidget(h_line_generator())
main_layout.addLayout(dp_layout)
main_layout.addWidget(h_line_generator())
main_layout.addLayout(cc_layout)
main_layout.addWidget(h_line_generator())
main_layout.addLayout(ex_layout)
main_layout.addWidget(h_line_generator())
main_layout.addLayout(export_layout)
main_layout.addWidget(h_line_generator())
main_layout.addWidget(object_list_table_widget)

# Default disabled widgets
widget_state_config(widget_state_elements, "no case")

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
    object_list_table_widget.clear_table_contents()
    object_list_table_widget.set_table_enabled(True)

    object_list_table_widget.set_table_row_count(Case.instance().number_of_objects_in_simulation())
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

        object_list_table_widget.set_table_cell_widget(current_row, 0, target_widget)

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
