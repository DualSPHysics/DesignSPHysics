#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Dock Pre Processing Widget '''

import os
import shutil
import glob
import pickle
from traceback import print_exc

import FreeCAD
import FreeCADGui

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon, widget_state_config
from mod.stdout_tools import debug, error, log, warning
from mod.dialog_tools import error_dialog, warning_dialog
from mod.executable_tools import refocus_cwd
from mod.freecad_tools import document_count, prompt_close_all_documents, create_dsph_document, create_dsph_document_from_fcstd, get_fc_main_window, valid_document_environment, get_fc_object, get_fc_view_object
from mod.xml import XMLExporter

from mod.constants import CASE_LIMITS_OBJ_NAME, PICKLE_PROTOCOL, FILLBOX_DEFAULT_LENGTH, FILLBOX_DEFAULT_RADIUS, CASE_LIMITS_3D_LABEL, CASE_LIMITS_2D_LABEL
from mod.enums import ObjectType, ObjectFillMode, FreeCADObjectType, FreeCADDisplayMode

from mod.widgets.gencase_completed_dialog import GencaseCompletedDialog
from mod.widgets.add_geo_dialog import AddGEODialog
from mod.widgets.case_summary import CaseSummary
from mod.widgets.mode_2d_config_dialog import Mode2DConfigDialog
from mod.widgets.special_options_selector_dialog import SpecialOptionsSelectorDialog

from mod.dataobjects.case import Case
from mod.dataobjects.simulation_object import SimulationObject
from mod.dataobjects.special_movement import SpecialMovement
from mod.dataobjects.file_gen import FileGen
from mod.dataobjects.rotation_file_gen import RotationFileGen
from mod.dataobjects.ml_piston_1d import MLPiston1D
from mod.dataobjects.ml_piston_2d import MLPiston2D
from mod.dataobjects.relaxation_zone_file import RelaxationZoneFile

# FIXME: Replace this when refactored
widget_state_elements = {}
data = {}


def on_tree_item_selection_change():
    pass


class DockPreProcessingWidget(QtGui.QWidget):
    '''DesignSPHysics Dock Pre Processing Widget '''

    def __init__(self):
        super().__init__()

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.cclabel_layout = QtGui.QHBoxLayout()
        self.ccfilebuttons_layout = QtGui.QHBoxLayout()
        self.ccsecondrow_layout = QtGui.QHBoxLayout()
        self.ccthirdrow_layout = QtGui.QHBoxLayout()
        self.ccfourthrow_layout = QtGui.QHBoxLayout()
        self.casecontrols_label = QtGui.QLabel("<b>{}</b>".format(__("Pre-processing")))

        self.casecontrols_bt_newdoc = QtGui.QToolButton()
        self.casecontrols_bt_newdoc.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.casecontrols_bt_newdoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.casecontrols_bt_newdoc.setText("  {}".format(__("New\n  Case")))
        self.casecontrols_bt_newdoc.setToolTip(__("Creates a new case. \nThe opened documents will be closed."))
        self.casecontrols_bt_newdoc.setIcon(get_icon("new.png"))
        self.casecontrols_bt_newdoc.setIconSize(QtCore.QSize(28, 28))
        self.casecontrols_menu_newdoc = QtGui.QMenu()
        self.casecontrols_menu_newdoc.addAction(get_icon("new.png"), __("New"))
        self.casecontrols_menu_newdoc.addAction(get_icon("new.png"), __("Import FreeCAD Document"))
        self.casecontrols_bt_newdoc.setMenu(self.casecontrols_menu_newdoc)
        self.casecontrols_menu_newdoc.resize(60, 60)

        self.casecontrols_bt_savedoc = QtGui.QToolButton()
        self.casecontrols_bt_savedoc.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.casecontrols_bt_savedoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.casecontrols_bt_savedoc.setText("  {}".format(__("Save\n  Case")))
        self.casecontrols_bt_savedoc.setToolTip(__("Saves the case."))
        self.casecontrols_bt_savedoc.setIcon(get_icon("save.png"))
        self.casecontrols_bt_savedoc.setIconSize(QtCore.QSize(28, 28))
        self.casecontrols_menu_savemenu = QtGui.QMenu()
        self.casecontrols_menu_savemenu.addAction(get_icon("save.png"), __("Save as..."))
        self.casecontrols_bt_savedoc.setMenu(self.casecontrols_menu_savemenu)

        widget_state_elements['casecontrols_bt_savedoc'] = self.casecontrols_bt_savedoc

        self.casecontrols_bt_loaddoc = QtGui.QToolButton()
        self.casecontrols_bt_loaddoc.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.casecontrols_bt_loaddoc.setText("  {}".format(__("Load\n  Case")))
        self.casecontrols_bt_loaddoc.setToolTip(__("Loads a case from disk. All the current documents\nwill be closed."))
        self.casecontrols_bt_loaddoc.setIcon(get_icon("load.png"))
        self.casecontrols_bt_loaddoc.setIconSize(QtCore.QSize(28, 28))

        self.casecontrols_bt_addfillbox = QtGui.QPushButton(__("Add fillbox"))
        self.casecontrols_bt_addfillbox.setToolTip(__("Adds a FillBox. A FillBox is able to fill an empty space\nwithin limits of geometry and a maximum bounding\nbox placed by the user."))
        self.casecontrols_bt_addfillbox.setEnabled(False)

        widget_state_elements['casecontrols_bt_addfillbox'] = self.casecontrols_bt_addfillbox

        self.casecontrols_bt_addgeo = QtGui.QPushButton("Import GEO")
        self.casecontrols_bt_addgeo.setToolTip(__("Imports a GEO object with postprocessing. This way you can set the scale of the imported object."))
        self.casecontrols_bt_addgeo.setEnabled(False)

        widget_state_elements['casecontrols_bt_addgeo'] = self.casecontrols_bt_addgeo

        self.casecontrols_bt_importxml = QtGui.QPushButton(__("Import XML"))
        self.casecontrols_bt_importxml.setToolTip(__("Imports an already created XML case from disk."))
        self.casecontrols_bt_importxml.setEnabled(True)

        self.summary_bt = QtGui.QPushButton(__("Case summary"))
        self.summary_bt.setToolTip(__("Shows a complete case summary with objects, configurations and settings in a brief view."))
        self.summary_bt.setEnabled(False)

        widget_state_elements['summary_bt'] = self.summary_bt

        self.toggle3dbutton = QtGui.QPushButton(__("Change 3D/2D"))
        self.toggle3dbutton.setToolTip(__("Changes the case mode between 2D and 3D mode, switching the Case Limits between a plane or a cube"))

        widget_state_elements['toggle3dbutton'] = self.toggle3dbutton

        self.casecontrols_bt_special = QtGui.QPushButton(__("Special"))
        self.casecontrols_bt_special.setToolTip(__("Special actions for the case."))

        widget_state_elements['dampingbutton'] = self.casecontrols_bt_special

        self.rungencase_bt = QtGui.QPushButton(__("Run GenCase"))
        self.rungencase_bt.setStyleSheet("QPushButton {font-weight: bold; }")
        self.rungencase_bt.setToolTip(__("This pre-processing tool creates the initial state of the particles (position, velocity and density) and defines the different SPH parameters for the simulation."))
        self.rungencase_bt.setIcon(get_icon("run_gencase.png"))
        self.rungencase_bt.setIconSize(QtCore.QSize(12, 12))

        widget_state_elements['rungencase_bt'] = self.rungencase_bt

        self.casecontrols_bt_newdoc.clicked.connect(self.on_new_case)
        self.casecontrols_bt_savedoc.clicked.connect(self.on_save_case)
        self.rungencase_bt.clicked.connect(self.on_save_with_gencase)
        self.casecontrols_menu_newdoc.triggered.connect(self.on_newdoc_menu)
        self.casecontrols_menu_savemenu.triggered.connect(self.on_save_menu)
        self.casecontrols_bt_loaddoc.clicked.connect(self.on_load_button)
        self.casecontrols_bt_addfillbox.clicked.connect(self.on_add_fillbox)
        self.casecontrols_bt_addgeo.clicked.connect(self.on_add_geo)
        self.summary_bt.clicked.connect(CaseSummary)
        self.toggle3dbutton.clicked.connect(self.on_2d_toggle)
        self.casecontrols_bt_special.clicked.connect(SpecialOptionsSelectorDialog)

        self.cclabel_layout.addWidget(self.casecontrols_label)
        self.ccfilebuttons_layout.addWidget(self.casecontrols_bt_newdoc)
        self.ccfilebuttons_layout.addWidget(self.casecontrols_bt_savedoc)
        self.ccfilebuttons_layout.addWidget(self.casecontrols_bt_loaddoc)
        self.ccsecondrow_layout.addWidget(self.summary_bt)
        self.ccsecondrow_layout.addWidget(self.toggle3dbutton)
        self.ccthirdrow_layout.addWidget(self.casecontrols_bt_addfillbox)
        self.ccthirdrow_layout.addWidget(self.casecontrols_bt_addgeo)
        self.ccthirdrow_layout.addWidget(self.casecontrols_bt_importxml)
        self.ccfourthrow_layout.addWidget(self.casecontrols_bt_special)
        self.ccfourthrow_layout.addWidget(self.rungencase_bt)

        self.main_layout.addLayout(self.cclabel_layout)
        self.main_layout.addLayout(self.ccfilebuttons_layout)
        self.main_layout.addLayout(self.ccthirdrow_layout)
        self.main_layout.addLayout(self.ccsecondrow_layout)
        self.main_layout.addLayout(self.ccfourthrow_layout)

        self.setLayout(self.main_layout)

    def on_new_case(self, prompt=True):
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
        self.dp_input.setText(str(Case.instance().dp))

        # Forces call to item selection change function so all changes are taken into account
        # FIXME: this should not be here
        on_tree_item_selection_change()

    def on_new_from_freecad_document(self, prompt=True):
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
        self.dp_input.setText(Case.instance().dp)

        # Forces call to item selection change function so all changes are taken into account
        # FIXME: This should not be here
        on_tree_item_selection_change()

    def on_save_case(self, save_as=None):
        ''' Defines what happens when save case button is clicked.
        Saves a freecad scene definition, and a dump of dsph data for the case.'''
        # Watch if save path is available.  Prompt the user if not.
        if (Case.instance().was_not_saved()) or save_as:
            # noinspection PyArgumentList
            save_name, _ = QtGui.QFileDialog.getSaveFileName(self, __("Save Case"), QtCore.QDir.homePath())
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
                print_exc()
                error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))

            refocus_cwd()
        else:
            log(__("Saving cancelled."))

    def on_save_with_gencase(self):
        ''' Saves data into disk and uses GenCase to generate the case files.'''

        # Check if the project is saved, if no shows the following message
        if Case.instance().path == '':
            # Warning window about save_case
            warning_dialog("You need to save the case first.")

        # Save Case as usual so all the data needed for GenCase is on disk
        self.on_save_case()
        # Ensure the current working directory is the DesignSPHysics directory
        refocus_cwd()

        # Use gencase if possible to generate the case final definition
        Case.instance().info.is_gencase_done = False
        if Case.instance().executable_paths.gencase != "":
            # Tries to spawn a process with GenCase to generate the case

            process = QtCore.QProcess(get_fc_main_window())

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
            self.on_save_case()
        else:
            log(__("Saving cancelled."))

        Case.instance().info.needs_to_run_gencase = True

    def on_newdoc_menu(self, action):
        ''' Handles the new document button and its dropdown items. '''
        if __("New") in action.text():
            self.on_new_case()
        if __("Import FreeCAD Document") in action.text():
            self.on_new_from_freecad_document()

    def on_save_menu(self, action):
        ''' Handles the save button and its dropdown items. '''
        if __("Save as...") in action.text():
            self.on_save_case(save_as=True)

    def on_load_button(self):
        ''' Defines load case button behaviour. This is made so errors can be detected and handled. '''
        try:
            self.on_load_case()
        except ImportError:
            error_dialog(__("There was an error loading the case"),
                         __("The case you are trying to load has some data that DesignSPHysics could not"
                            " load.\n\nDid you make the case in a previous version?"))
            self.on_new_case(prompt=False)

    def on_load_case(self):
        '''Defines loading case mechanism.
        Load points to a dsphdata custom file, that stores all the relevant info.
        If FCStd file is not found the project is considered corrupt.'''
        # noinspection PyArgumentList
        load_name, _ = QtGui.QFileDialog.getOpenFileName(self, __("Load Case"), QtCore.QDir.homePath(), "casedata.dsphdata")
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
                    self.on_new_case(prompt=False)
                    return

            # Remove exec paths from loaded data if user have already correct ones.
            already_correct = Case.instance().executable_paths.check_and_filter()
            if already_correct:
                for x in ['gencase_path', 'dsphysics_path', 'partvtk4_path', 'floatinginfo_path', 'computeforces_path', 'measuretool_path', 'isosurface_path', 'boundaryvtk_path']:
                    load_disk_data.pop(x, None)

            # Update data structure with disk loaded one
            data.update(load_disk_data)  # TODO: Update mechanism for new data
        except (EOFError, ValueError):
            error_dialog(__("There was an error importing the case  You probably need to set them again.\n\n"
                            "This could be caused due to file corruption, "
                            "caused by operating system based line endings or ends-of-file, or other related aspects."))

        # Fill some data
        self.dp_input.setText(str(Case.instance().dp))

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
        # FIXME: This should not be here
        on_tree_item_selection_change()

    def on_add_fillbox(self):
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

    def on_add_geo(self):
        ''' Add STL file. Opens a file opener and allows the user to set parameters for the import process '''

        file_name = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select GEO to import"), QtCore.QDir.homePath(), "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk)")

        if not file_name:
            return

        add_geo_dialog = AddGEODialog(file_name)
        add_geo_dialog.exec_()

    def on_2d_toggle(self):
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
