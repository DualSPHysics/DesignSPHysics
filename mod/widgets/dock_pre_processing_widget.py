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
from mod.gui_tools import get_icon
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

# FIXME: Delete this when refactored
data = {}


def on_tree_item_selection_change():
    pass


class DockPreProcessingWidget(QtGui.QWidget):
    '''DesignSPHysics Dock Pre Processing Widget '''

    update_dp = QtCore.Signal()
    case_created = QtCore.Signal()
    gencase_completed = QtCore.Signal(bool)
    simulation_completed = QtCore.Signal(bool)

    def __init__(self):
        super().__init__()

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label_layout = QtGui.QHBoxLayout()
        self.first_row_layout = QtGui.QHBoxLayout()
        self.second_row_layout = QtGui.QHBoxLayout()
        self.third_row_layout = QtGui.QHBoxLayout()
        self.fourth_row_layout = QtGui.QHBoxLayout()

        self.casecontrols_label = QtGui.QLabel("<b>{}</b>".format(__("Pre-processing")))

        self.new_case_button = QtGui.QToolButton()
        self.new_case_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.new_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.new_case_button.setText("  {}".format(__("New\n  Case")))
        self.new_case_button.setToolTip(__("Creates a new case. \nThe opened documents will be closed."))
        self.new_case_button.setIcon(get_icon("new.png"))
        self.new_case_button.setIconSize(QtCore.QSize(28, 28))

        self.new_case_menu = QtGui.QMenu()
        self.new_case_menu.addAction(get_icon("new.png"), __("New"))
        self.new_case_menu.addAction(get_icon("new.png"), __("Import FreeCAD Document"))

        self.new_case_button.setMenu(self.new_case_menu)
        self.new_case_menu.resize(60, 60)

        self.save_button = QtGui.QToolButton()
        self.save_button.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.save_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_button.setText("  {}".format(__("Save\n  Case")))
        self.save_button.setToolTip(__("Saves the case."))
        self.save_button.setIcon(get_icon("save.png"))
        self.save_button.setIconSize(QtCore.QSize(28, 28))
        self.save_menu = QtGui.QMenu()
        self.save_menu.addAction(get_icon("save.png"), __("Save as..."))
        self.save_button.setMenu(self.save_menu)

        self.load_button = QtGui.QToolButton()
        self.load_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.load_button.setText("  {}".format(__("Load\n  Case")))
        self.load_button.setToolTip(__("Loads a case from disk. All the current documents\nwill be closed."))
        self.load_button.setIcon(get_icon("load.png"))
        self.load_button.setIconSize(QtCore.QSize(28, 28))

        self.add_fillbox_button = QtGui.QPushButton(__("Add fillbox"))
        self.add_fillbox_button.setToolTip(__("Adds a FillBox. A FillBox is able to fill an empty space\nwithin limits of geometry and a maximum bounding\nbox placed by the user."))

        self.add_geometry_button = QtGui.QPushButton("Import GEO")
        self.add_geometry_button.setToolTip(__("Imports a GEO object with postprocessing. This way you can set the scale of the imported object."))

        self.import_xml_button = QtGui.QPushButton(__("Import XML"))
        self.import_xml_button.setToolTip(__("Imports an already created XML case from disk."))

        self.case_summary_button = QtGui.QPushButton(__("Case summary"))
        self.case_summary_button.setToolTip(__("Shows a complete case summary with objects, configurations and settings in a brief view."))

        self.toggle_2d_mode_button = QtGui.QPushButton(__("Change 3D/2D"))
        self.toggle_2d_mode_button.setToolTip(__("Changes the case mode between 2D and 3D mode, switching the Case Limits between a plane or a cube"))

        self.special_button = QtGui.QPushButton(__("Special"))
        self.special_button.setToolTip(__("Special actions for the case."))

        self.gencase_button = QtGui.QPushButton(__("Run GenCase"))
        self.gencase_button.setStyleSheet("QPushButton {font-weight: bold; }")
        self.gencase_button.setToolTip(__("This pre-processing tool creates the initial state of the particles (position, velocity and density) and defines the different SPH parameters for the simulation."))
        self.gencase_button.setIcon(get_icon("run_gencase.png"))
        self.gencase_button.setIconSize(QtCore.QSize(12, 12))

        self.new_case_button.clicked.connect(self.on_new_case)
        self.save_button.clicked.connect(self.on_save_case)
        self.gencase_button.clicked.connect(self.on_save_with_gencase)
        self.new_case_menu.triggered.connect(self.on_newdoc_menu)
        self.save_menu.triggered.connect(self.on_save_menu)
        self.load_button.clicked.connect(self.on_load_button)
        self.add_fillbox_button.clicked.connect(self.on_add_fillbox)
        self.add_geometry_button.clicked.connect(self.on_add_geo)
        self.case_summary_button.clicked.connect(CaseSummary)
        self.toggle_2d_mode_button.clicked.connect(self.on_2d_toggle)
        self.special_button.clicked.connect(SpecialOptionsSelectorDialog)

        self.label_layout.addWidget(self.casecontrols_label)
        self.first_row_layout.addWidget(self.new_case_button)
        self.first_row_layout.addWidget(self.save_button)
        self.first_row_layout.addWidget(self.load_button)
        self.second_row_layout.addWidget(self.case_summary_button)
        self.second_row_layout.addWidget(self.toggle_2d_mode_button)
        self.third_row_layout.addWidget(self.add_fillbox_button)
        self.third_row_layout.addWidget(self.add_geometry_button)
        self.third_row_layout.addWidget(self.import_xml_button)
        self.fourth_row_layout.addWidget(self.special_button)
        self.fourth_row_layout.addWidget(self.gencase_button)

        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addLayout(self.first_row_layout)
        self.main_layout.addLayout(self.third_row_layout)
        self.main_layout.addLayout(self.second_row_layout)
        self.main_layout.addLayout(self.fourth_row_layout)

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
        Case.instance().add_object(SimulationObject(CASE_LIMITS_OBJ_NAME, -1, ObjectType.SPECIAL, ObjectFillMode.SPECIAL))

        self.case_created.emit()
        self.update_dp.emit()

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
        Case.instance().add_object_to_sim(SimulationObject(CASE_LIMITS_OBJ_NAME, -1, ObjectType.SPECIAL, ObjectFillMode.SPECIAL))

        self.update_dp.emit()
        self.case_created.emit()

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
                    self.gencase_completed.emit(True)

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
        self.case_created.emit()
        self.gencase_completed.emit(Case.instance().info.is_gencase_done)
        self.simulation_completed.emit(Case.instance().info.is_simulation_done)

        # Check executable paths
        refocus_cwd()
        correct_execs = Case.instance().executable_paths.check_and_filter()

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

    def adapt_to_no_case(self):
        ''' Adapts the widget to an environment with no case opened. '''
        for x in [self.save_button, self.add_fillbox_button, self.add_geometry_button, self.import_xml_button,
                  self.case_summary_button, self.toggle_2d_mode_button, self.special_button, self.gencase_button]:
            x.setEnabled(False)

    def adapt_to_new_case(self):
        ''' Adapts the widget to an environment when a case is opened. '''
        for x in [self.save_button, self.add_fillbox_button, self.add_geometry_button, self.import_xml_button,
                  self.case_summary_button, self.toggle_2d_mode_button, self.special_button, self.gencase_button]:
            x.setEnabled(True)
