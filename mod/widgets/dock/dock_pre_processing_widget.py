#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Pre Processing Widget """
import shutil
from os import path, walk
from traceback import print_exc
import FreeCADGui


from PySide2 import QtCore, QtWidgets,QtGui
from PySide2.QtWidgets import QAction

from mod.appmode import AppMode
from mod.constants import CASE_LIMITS_OBJ_NAME, CASE_LIMITS_2D_LABEL, CASE_LIMITS_3D_LABEL, WIDTH_2D
from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.dialog_tools import error_dialog, warning_dialog, WaitDialog, info_dialog
from mod.tools.dialog_tools import ok_cancel_dialog
from mod.enums import SDPositionPropertyType
from mod.tools.executable_tools import refocus_cwd, ensure_process_is_executable_or_fail
from mod.tools.file_tools import save_case, load_case, save_extra_files
from mod.tools.freecad_tools import document_count, prompt_close_all_documents, create_dsph_document, \
    create_dsph_document_from_fcstd, add_fillbox_objects, add_case_limits_object, create_empty_document, \
    add_tree_structure, update_simulation_domain, add_simulation_domain
from mod.tools.freecad_tools import get_fc_main_window, valid_document_environment, save_current_freecad_document, \
    get_fc_object
from mod.functions import has_special_char, parse_ds_int
from mod.tools.gui_tools import get_icon
from mod.tools.script_tools import generate_ext_script
from mod.tools.stdout_tools import error, log, debug
from mod.tools.translation_tools import __
from mod.widgets.dock.dock_widgets.add_bathymetry_dialog import AddBathymetryDialog
from mod.widgets.dock.dock_widgets.add_geo_dialog import AddGeoDialog
from mod.widgets.dock.dock_widgets.case_summary import CaseSummary
from mod.widgets.dock.dock_widgets.gencase_completed_dialog import GencaseCompletedDialog
from mod.widgets.dock.dock_widgets.mode_2d_config_dialog import Mode2DConfigDialog
from mod.widgets.dock.special_widgets.special_options_selector_dialog import SpecialOptionsSelectorDialog


class DockPreProcessingWidget(QtWidgets.QWidget):
    """DesignSPHysics Dock Pre Processing Widget """

    need_refresh = QtCore.Signal()
    update_dp = QtCore.Signal()
    case_created = QtCore.Signal()
    gencase_completed = QtCore.Signal(bool)
    simulation_completed = QtCore.Signal(bool)
    force_pressed = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label_layout = QtWidgets.QHBoxLayout()
        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout = QtWidgets.QHBoxLayout()
        self.fourth_row_layout = QtWidgets.QHBoxLayout()
        self.fifth_row_layout = QtWidgets.QHBoxLayout()

        self.casecontrols_label = QtWidgets.QLabel("<b>{}</b>".format(__("Pre-processing")))
        #self.force_button = QtWidgets.QPushButton(__("Force Enable Panels"))
        #self.force_button.setStyleSheet("font-size: 8px; max-height: 10px; padding-bottom: 0; padding-top: 0; padding-left:2px; padding-right: 2px")

        self.new_case_button = QtWidgets.QToolButton()
        self.new_case_button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.new_case_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.new_case_button.setText("  {}".format(__("New Case")))
        self.new_case_button.setToolTip(__("Creates a new case. \nThe opened documents will be closed."))
        self.new_case_button.setIcon(QtGui.QIcon.fromTheme("document-new", get_icon("new.png")))
        self.new_case_button.setIconSize(QtCore.QSize(28, 28))
        self.new_case_button.setFixedHeight(24)

        self.new_case_menu = QtWidgets.QMenu()
        self.new_case_menu.addAction(QtGui.QIcon.fromTheme("document-new", get_icon("new.png")), __("New"))
        #self.new_case_menu.addAction(QtGui.QIcon.fromTheme("document-new", get_icon("new.png")), __("Import FreeCAD Document"))

        self.new_case_button.setMenu(self.new_case_menu)
        self.new_case_menu.resize(60, 60)

        self.save_button = QtWidgets.QToolButton()
        self.save_button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.save_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.save_button.setText("  {}".format(__("Save")))
        self.save_button.setToolTip(__("Saves the case."))
        self.save_button.setIcon(QtGui.QIcon.fromTheme("document-save", get_icon("save.png")))
        self.save_button.setIconSize(QtCore.QSize(28, 28))
        self.save_menu = QtWidgets.QMenu()
        self.save_menu.addAction(QtGui.QIcon.fromTheme("document-save-as", get_icon("save.png")), __("Save as..."))
        self.save_button.setMenu(self.save_menu)
        self.save_button.setFixedHeight(24)

        self.load_button = QtWidgets.QToolButton()
        self.load_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.load_button.setText("  {}".format(__("Load")))
        self.load_button.setToolTip(__("Loads a case from disk. All the current documents\nwill be closed."))
        self.load_button.setIcon(QtGui.QIcon.fromTheme("document-open", get_icon("load.png")))
        self.load_button.setIconSize(QtCore.QSize(28, 28))
        self.load_button.setFixedHeight(24)

        self.add_fillbox_button = QtWidgets.QPushButton(__("Add fillbox"))
        self.add_fillbox_button.setToolTip(__("Adds a FillBox. A FillBox is able to fill an empty space\nwithin limits of geometry and a maximum bounding\nbox placed by the user."))
        self.add_fillbox_button.setIcon(QtGui.QIcon.fromTheme("list-add"))

        self.add_geometry_button = QtWidgets.QPushButton("Import GEO")
        self.add_geometry_button.setToolTip(__("Imports a GEO object with postprocessing. This way you can set the scale of the imported object."))
        self.add_geometry_button.setIcon(QtGui.QIcon.fromTheme("list-add"))

        self.case_summary_button = QtWidgets.QPushButton(__("Case summary"))
        self.case_summary_button.setToolTip(__("Shows a complete case summary with objects, configurations and settings in a brief view."))
        self.case_summary_button.setIcon(QtGui.QIcon.fromTheme("document-properties"))

        self.toggle_2d_mode_button = QtWidgets.QPushButton(__("Change 3D/2D"))
        self.toggle_2d_mode_button.setToolTip(__("Changes the case mode between 2D and 3D mode, switching the Case Limits between a plane or a cube"))
        self.toggle_2d_mode_button.setIcon(QtGui.QIcon.fromTheme("object-flip-horizontal"))

        self.special_button = QtWidgets.QPushButton(__("Special"))
        self.special_button.setToolTip(__("Special actions for the case."))
        self.special_button.setIcon(QtGui.QIcon.fromTheme("window-new"))

        self.gencase_button = QtWidgets.QPushButton() #QToolButton
        self.gencase_button.setToolTip(__("This pre-processing tool creates the initial state of the particles (position, velocity and density) and defines the different SPH parameters for the simulation."))
        self.gencase_button.setIcon(get_icon("run_gencase.png"))
        self.gencase_button.setIconSize(QtCore.QSize(12, 12))
        self.gencase_button.setText("  {}".format(__("Gencase")))
        self.gencase_button.setIcon(get_icon("run_gencase.png"))
        self.gencase_menu = QtWidgets.QMenu()
        self.action_run_gencase=QAction( __("Local Run"))
        self.action_run_gencase.setIcon(get_icon("run_gencase.png"))
        self.action_generate_gencase_script = QAction(__("Generate_script"))
        self.action_generate_gencase_script.setIcon(get_icon("save.png"))
        self.gencase_menu.addActions([self.action_run_gencase,self.action_generate_gencase_script])
        self.gencase_button.setMenu(self.gencase_menu)
        self.gencase_menu.aboutToShow.connect(self.update_gencase_menu)
        #self.gencase_button.setFixedHeight(24)
        #self.gencase_button.setFixedWidth(180)


        self.new_case_button.clicked.connect(lambda: self.on_new_case(True))
        self.save_button.clicked.connect(self.on_save_case)
        self.gencase_menu.triggered.connect(self.on_gencase_menu)
        self.new_case_menu.triggered.connect(self.on_newdoc_menu)
        self.save_menu.triggered.connect(self.on_save_menu)
        self.load_button.clicked.connect(self.on_load_button)
        self.add_fillbox_button.clicked.connect(self.on_add_fillbox)
        self.add_geometry_button.clicked.connect(self.on_add_geo)
        self.case_summary_button.clicked.connect(CaseSummary)
        self.toggle_2d_mode_button.clicked.connect(self.on_2d_toggle)
        self.special_button.clicked.connect(SpecialOptionsSelectorDialog)

        self.label_layout.addWidget(self.casecontrols_label)
        self.label_layout.addStretch(1)
        self.first_row_layout.addWidget(self.new_case_button)
        self.first_row_layout.addWidget(self.save_button)
        self.first_row_layout.addWidget(self.load_button)
        self.second_row_layout.addWidget(self.add_fillbox_button)
        self.second_row_layout.addWidget(self.add_geometry_button)
        self.third_row_layout.addWidget(self.case_summary_button)
        self.third_row_layout.addWidget(self.toggle_2d_mode_button)
        self.fourth_row_layout.addWidget(self.special_button)
        self.fourth_row_layout.addWidget(self.gencase_button)

        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addLayout(self.first_row_layout)
        self.main_layout.addLayout(self.second_row_layout)
        self.main_layout.addLayout(self.third_row_layout)
        self.main_layout.addLayout(self.fourth_row_layout)

        self.setLayout(self.main_layout)

    def on_new_case(self, prompt=True):
        """ Defines what happens when new case is clicked. Closes all documents
            if possible and creates a FreeCAD document with Case Limits object. """
        if document_count() and not prompt_close_all_documents(prompt):
            return

        create_dsph_document()
        Case.the().reset()

        self.case_created.emit()
        self.update_dp.emit()
        self.need_refresh.emit()

    def on_new_from_freecad_document(self, prompt=True):
        """ Creates a new case based on an existing FreeCAD document.
        This is specially useful for CAD users that want to use existing geometry for DesignSPHysics. """
        file_name, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), "Select document to import", Case.the().info.last_used_directory)

        Case.the().info.update_last_used_directory(file_name)
        if file_name and document_count() and not prompt_close_all_documents(prompt):
            return
        if file_name:
            create_dsph_document_from_fcstd(file_name)
            Case.the().reset()

            self.update_dp.emit()
            self.case_created.emit()
            self.need_refresh.emit()

    def on_save_case(self, save_as=None):
        """ Defines what happens when save case button is clicked.
        Saves a freecad scene definition, and a dump of dsph data for the case."""
        # Check if case limits have been removed and add them back
        CaseLimits = get_fc_object(CASE_LIMITS_OBJ_NAME)
        if not CaseLimits:
            warning_dialog("No case limits object have been found. Default case limits will be created",
                           detailed_text=None)
            add_case_limits_object()
            if not Case.the().mode3d:
                self.on_2d_toggle()

        if Case.the().was_not_saved() or save_as:
            save_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, __("Save Case"), Case.the().info.last_used_directory)
            Case.the().info.update_last_used_directory(save_name)
        else:
            save_name = Case.the().path

        if not save_name:
            return

        Case.the().info.recommends_to_run_gencase = True

        if has_special_char(save_name):
            error_dialog(__("There was an error saving the case.\nSpaces or special characters cannot be included in path to save the case."))
            return
        
        save_case(save_name, Case.the())

        save_current_freecad_document(Case.the().path)
        if Case.the().has_materials() and Case.the().execution_parameters.rigidalgorithm not in (2, 3):
            warning_dialog(
                __("Properties and Material information was not written. See details for more info."),
                __("The case being saved has some properties/materials defined in one of its MKs.\n"
                   "However, the solid-solid interaction on the execution parameters must be set to DEM or CHRONO for this feature to work.")
            )
        self.need_refresh.emit()

    def update_gencase_menu(self):
        if (ApplicationSettings.the().basic_visualization):
            if self.gencase_menu.actions():
                self.gencase_menu.clear()
            self.on_gencase_menu(self.action_run_gencase)
        else:
            if not self.gencase_menu.actions():
                self.gencase_menu.addActions([self.action_run_gencase,self.action_generate_gencase_script])

    def on_gencase_menu(self, action):
        """ Handles the new document button and its dropdown items. """
        if __("Local Run") in action.text():
            self.on_execute_gencase()
        if __("Generate script") in action.text():
            self.on_generate_gencase_script()

    def on_execute_gencase(self):
        """ Saves data into disk and uses GenCase to generate the case files."""
        wait_dialog = WaitDialog("Gencase is running.please wait")
        wait_dialog.show()
        if not Case.the().path:
            error_dialog(__("The case must be saved before running GenCase."))
            self.on_save_case()
        
        if not Case.the().path:
            return

        if not Case.the().executable_paths.gencase:
            warning_dialog(__("GenCase executable is not set."))
            return



        gencase_full_path = path.abspath(Case.the().executable_paths.gencase)
        arguments = ["{path}/{name}_Def".format(path=Case.the().path, name=Case.the().name),
                     "{path}/{name}_out/{name}".format(path=Case.the().path, name=Case.the().name),
                     "-save:+all"]
        cmd_string = "{} {}".format(gencase_full_path, " ".join(arguments))

        # Check if the case was already generated
        dirout=str("{path}/{name}_out/".format(path=Case.the().path, name=Case.the().name))
        gencasefile=str("{dirout}/{name}.out".format(dirout=dirout, name=Case.the().name))
        if path.exists(gencasefile):
            execute_gencase=ok_cancel_dialog(__("Remove the Case output data"),__("This action will remove the data generated before.\n\nPress Ok to remove and run GenCase.\nPress Cancel to exit and keep the data."))
            # Decision dialog to remove data before running GenCase
            if execute_gencase == QtWidgets.QMessageBox.Cancel:
                return
            else:
                # Remove some folders before execute GenCase
                try:
                    self.delete_sub_folder(dirout,"Vtk")
                    self.delete_root_folder(dirout)
                except PermissionError:
                    warning_dialog("Output folder cannot be deleted.", "Close all open files in output folder before running gencase")
                    return
            
        refocus_cwd()
        process = QtCore.QProcess(get_fc_main_window())
        process.setWorkingDirectory(Case.the().path)
        try:
            ensure_process_is_executable_or_fail(gencase_full_path)
        except RuntimeError:
            wait_dialog.close_dialog()
            error_dialog("GenCase executable is invalid, does not have execution permissions or it's path is incorrect")
            return
        process.start(gencase_full_path, arguments)
        log("Executing -> {}".format(cmd_string))


        def on_gencase_finished(exit_code):
            try:
                output = str(process.readAllStandardOutput().data(), encoding='utf-8')
            except UnicodeDecodeError:
                output = str(process.readAllStandardOutput().data(), encoding='latin1')

            if exit_code:
                error_dialog(
                    f"Error executing GenCase: {exit_code}",
                    output)
            else:
                try:
                    total_particles_text = output[output.index("Total particles: "):output.index(" (bound=")]
                    total_particles = parse_ds_int(total_particles_text[total_particles_text.index(": ") + 2:])
                    Case.the().info.particle_number = total_particles
                    GencaseCompletedDialog(particle_count=total_particles, detail_text=output, cmd_string=cmd_string,
                                           parent=get_fc_main_window()).show()
                    save_name = Case.the().path
                    save_extra_files(Case.the(),save_name)
                    Case.the().info.recommends_to_run_gencase = False

                    particle_limits_text = output[output.index("Particle limits:"):output.index("Time of execution")]
                    manage_simulation_domain(particle_limits_text)


                except ValueError:
                    print_exc()
                    Case.the().info.recommends_to_run_gencase = True

            # Refresh widget enable/disable status as GenCase finishes
            wait_dialog.close_dialog()
        process.finished.connect(on_gencase_finished)

    def on_generate_gencase_script(self):
        """ Generates custom script for running gencase externally"""
        if not Case.the().path:
            error_dialog(__("The case must be saved before generating gencase script."))
            self.on_save_case()

        if not Case.the().path:
            return


        arguments = ["{name}_Def".format(name=Case.the().name),
                     "{name}_out/{name}".format(name=Case.the().name),
                     "-save:+all"]

        generate_ext_script("gencase",arguments,"")


    def delete_sub_folder(self,output_folder,endwith):
        """ Deletes sub folders that end with a desired string. """
        for subir, dirs, files in walk(output_folder):
            for dir in dirs:
                if dir.endswith(endwith):
                    shutil.rmtree(str("{}/{}".format(output_folder,dir)))
    
    def delete_root_folder(self,output_folder):
        """ Deletes sub folders that end with a desired string. """
        if path.isdir(output_folder):
            shutil.rmtree(str("{}".format(output_folder)))

    def on_newdoc_menu(self, action):
        """ Handles the new document button and its dropdown items. """
        if __("New") in action.text():
            self.on_new_case()
        if __("Import FreeCAD Document") in action.text():
            self.on_new_from_freecad_document()

    def on_save_menu(self, action):
        """ Handles the save button and its dropdown items. """
        if __("Save as...") in action.text():
            self.on_save_case(save_as=True)

    def on_load_button(self):
        """ Defines load case button behaviour. This is made so errors can be detected and handled. """
        try:
            self.on_load_case()
        except ImportError:
            error_dialog(__("There was an error loading the case"),
                         __("The case you are trying to load has some data that DesignSPHysics could not load.\n\nDid you make the case in a previous version?"))
            self.on_new_case(prompt=False)

    def on_load_case(self):
        """Defines loading case mechanism. Load points to a dsphdata custom file, that stores all the relevant info.
           If FCStd file is not found the project is considered corrupt."""

        load_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, __("Load Case"), Case.the().info.last_used_directory, "casedata.dsphdata")
        #load_path=load_path.replace("/",os.sep)
        Case.the().info.update_last_used_directory(load_path)

        if load_path == "":
            return
        log("Trying to load case from disk")
        disk_data: Case = load_case(load_path)
        if not disk_data:
            create_empty_document()
            return

        try:
            Case.update_from_disk(disk_data)
            self.update_dp.emit()
        except (EOFError, ValueError):
            error_dialog(__("There was an error importing the case. You probably need to set them again.\n\n"
                            "This could be caused due to file corruption, caused by operating system based line endings or ends-of-file, or other related aspects."))

        # User may have changed the name of the folder/project
        Case.the().path = path.dirname(load_path)
        #Case.the().name = Case.the().path.split("/")[-1] TODO CHECK THIS
        #On Case folder changed, change path but not name
        #So xml and output folder is still valid

        # Adapt widget state to case info
        self.case_created.emit()
        self.need_refresh.emit()
        Case.the().executable_paths.check_and_filter()
        Case.the().info.update_last_used_directory(load_path)
        AppMode.set_3d_mode(Case.the().mode3d)
        add_case_limits_object()
        add_tree_structure()

    def on_add_fillbox(self):
        """ Add fillbox group. It consists in a group with 2 objects inside: a point and a box.
        The point represents the fill seed and the box sets the bounds for the filling. """
        add_fillbox_objects()

    def on_add_geo(self):
        """ Add Geometry File (STL,PLY,VTK,VTU,XYZ) Opens a file opener and allows the user to set parameters for the import process """
        self.need_refresh.emit()

        file_name, _ = QtWidgets.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select GEO to import"), Case.the().info.last_used_directory, "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk);;XYZ Files (*.xyz);;VTU Files (*.vtu);;VTM Files(*.vtm)")
        Case.the().info.update_last_used_directory(file_name)
        if not file_name:
            return
        if "xyz" in file_name.lower()[-4:]:
            AddBathymetryDialog(file_name, parent=None).exec_()
        else:
            AddGeoDialog(file_name, parent=None).exec_()

    def on_2d_toggle(self):
        """ Handles Toggle 3D/2D Button. Changes the Case Limits object accordingly. """
        if not valid_document_environment():
            error("Not a valid case environment")
            return

        fc_object = get_fc_object(CASE_LIMITS_OBJ_NAME)
        
        if Case.the().mode3d:
            # 3D to 2D
            Case.the().info.last_3d_width = fc_object.Width.Value
            config_dialog = Mode2DConfigDialog(fc_object.Placement.Base.y, parent=None)
            if config_dialog.exit_status == QtWidgets.QDialog.Rejected:
                return
            fc_object.Placement.Base.y = float(config_dialog.stored_y_value)
            fc_object.Label = CASE_LIMITS_2D_LABEL
            Case.the().mode3d = False
            fc_object.Width.Value=WIDTH_2D
            FreeCADGui.activeDocument().activeView().viewFront()
        else:
            # 2D to 3D
            Case.the().mode3d = True
            fc_object.Width = Case.the().info.last_3d_width if Case.the().info.last_3d_width > 0.0 else fc_object.Length
            fc_object.Label = CASE_LIMITS_3D_LABEL
            FreeCADGui.activeDocument().activeView().viewIsometric()
       
        # Updates mode
        if (AppMode.is_3d() != Case.the().mode3d):
            AppMode.set_3d_mode(Case.the().mode3d)
            add_simulation_domain()

    def adapt_to_no_case(self):
        """ Adapts the widget to an environment with no case opened. """
        for x in [self.save_button, self.add_fillbox_button, self.add_geometry_button,
                  self.case_summary_button, self.toggle_2d_mode_button, self.special_button, self.gencase_button]:
            x.setEnabled(False)

    def adapt_to_new_case(self):
        """ Adapts the widget to an environment when a case is opened. """
        for x in [self.save_button, self.add_fillbox_button, self.add_geometry_button,
                  self.case_summary_button, self.toggle_2d_mode_button, self.special_button, self.gencase_button]:
            x.setEnabled(True)

        #if Case.the().custom_script_file: #Case
        #    pass
            #self.custom_script_button.setEnabled(True)

def manage_simulation_domain(particle_limits_text : str):
    particles_limit_x = particle_limits_text.split(":")[2].split(" [")[0].split(" to ")
    particles_limit_y = particle_limits_text.split(":")[3].split(" [")[0].split(" to ")
    particles_limit_z = particle_limits_text.split(":")[4].split(" [")[0].split(" to ")
    particles_limit_min_x = float(particles_limit_x[0])
    particles_limit_max_x = float(particles_limit_x[1])
    particles_limit_min_y = float(particles_limit_y[0])
    particles_limit_max_y = float(particles_limit_y[1])
    particles_limit_min_z = float(particles_limit_z[0])
    particles_limit_max_z = float(particles_limit_z[1])
    sd = Case.the().domain
    #min_x
    if sd.posmin_x.type==SDPositionPropertyType.DEFAULT:
        min_x=particles_limit_min_x
    elif sd.posmin_x.type==SDPositionPropertyType.VALUE:
        min_x=sd.posmin_x.value
    elif sd.posmin_x.type==SDPositionPropertyType.DEFAULT_VALUE:
        min_x = particles_limit_min_x-sd.posmin_x.value
    else:
        min_x = particles_limit_min_x - sd.posmin_x.value*particles_limit_min_x / 100
    #min_y
    if sd.posmin_y.type == SDPositionPropertyType.DEFAULT:
        min_y = particles_limit_min_y
    elif sd.posmin_y.type == SDPositionPropertyType.VALUE:
        min_y = sd.posmin_y.value
    elif sd.posmin_y.type == SDPositionPropertyType.DEFAULT_VALUE:
        min_y = particles_limit_min_y - sd.posmin_y.value
    else:
        min_y = particles_limit_min_y - sd.posmin_y.value * particles_limit_min_y / 100
    #min_z
    if sd.posmin_z.type == SDPositionPropertyType.DEFAULT:
        min_z = particles_limit_min_z
    elif sd.posmin_z.type == SDPositionPropertyType.VALUE:
        min_z = sd.posmin_z.value
    elif sd.posmin_z.type == SDPositionPropertyType.DEFAULT_VALUE:
        min_z = particles_limit_min_z - sd.posmin_z.value
    else:
        min_z = particles_limit_min_z - sd.posmin_z.value * particles_limit_min_z / 100
    #MAX
    # max_x
    if sd.posmax_x.type == SDPositionPropertyType.DEFAULT:
        max_x = particles_limit_max_x
    elif sd.posmax_x.type == SDPositionPropertyType.VALUE:
        max_x = sd.posmax_x.value
    elif sd.posmax_x.type == SDPositionPropertyType.DEFAULT_VALUE:
        max_x = particles_limit_max_x + sd.posmax_x.value
    else:
        max_x = particles_limit_max_x + sd.posmax_x.value * particles_limit_max_x / 100
    # max_y
    if sd.posmax_y.type == SDPositionPropertyType.DEFAULT:
        max_y = particles_limit_max_y
    elif sd.posmax_y.type == SDPositionPropertyType.VALUE:
        max_y = sd.posmax_y.value
    elif sd.posmax_y.type == SDPositionPropertyType.DEFAULT_VALUE:
        max_y = particles_limit_max_y + sd.posmax_y.value
    else:
        max_y = particles_limit_max_y + sd.posmax_y.value * particles_limit_max_y / 100
    # max_z
    if sd.posmax_z.type == SDPositionPropertyType.DEFAULT:
        max_z = particles_limit_max_z
    elif sd.posmax_z.type == SDPositionPropertyType.VALUE:
        max_z = sd.posmax_z.value
    elif sd.posmax_z.type == SDPositionPropertyType.DEFAULT_VALUE:
        max_z = particles_limit_max_z + sd.posmax_z.value
    else:
        max_z = particles_limit_max_z + sd.posmax_z.value * particles_limit_max_z / 100
    
    update_simulation_domain(min_x,min_y,min_z,max_x,max_y,max_z)



