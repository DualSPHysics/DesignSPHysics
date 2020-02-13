#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Pre Processing Widget """

from os import path
from traceback import print_exc

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import error, debug
from mod.dialog_tools import error_dialog, warning_dialog
from mod.executable_tools import refocus_cwd
from mod.file_tools import save_case, load_case
from mod.freecad_tools import document_count, prompt_close_all_documents, create_dsph_document, create_dsph_document_from_fcstd, add_fillbox_objects
from mod.freecad_tools import get_fc_main_window, valid_document_environment, save_current_freecad_document, get_fc_object

from mod.constants import CASE_LIMITS_OBJ_NAME, CASE_LIMITS_2D_LABEL, CASE_LIMITS_3D_LABEL
from mod.enums import ObjectType, ObjectFillMode

from mod.widgets.add_geo_dialog import AddGEODialog
from mod.widgets.special_options_selector_dialog import SpecialOptionsSelectorDialog
from mod.widgets.gencase_completed_dialog import GencaseCompletedDialog
from mod.widgets.mode_2d_config_dialog import Mode2DConfigDialog
from mod.widgets.case_summary import CaseSummary

from mod.dataobjects.case import Case
from mod.dataobjects.simulation_object import SimulationObject


class DockPreProcessingWidget(QtGui.QWidget):
    """DesignSPHysics Dock Pre Processing Widget """

    need_refresh = QtCore.Signal()
    update_dp = QtCore.Signal()
    case_created = QtCore.Signal()
    gencase_completed = QtCore.Signal(bool)
    simulation_completed = QtCore.Signal(bool)
    force_pressed = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label_layout = QtGui.QHBoxLayout()
        self.first_row_layout = QtGui.QHBoxLayout()
        self.second_row_layout = QtGui.QHBoxLayout()
        self.third_row_layout = QtGui.QHBoxLayout()
        self.fourth_row_layout = QtGui.QHBoxLayout()

        self.casecontrols_label = QtGui.QLabel("<b>{}</b>".format(__("Pre-processing")))
        self.force_button = QtGui.QPushButton(__("Force Enable Panels"))
        self.force_button.setStyleSheet("font-size: 8px; max-height: 10px; padding-bottom: 0; padding-top: 0; padding-left:2px; padding-right: 2px")

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

        self.force_button.clicked.connect(self.on_force_button)
        self.new_case_button.clicked.connect(lambda: self.on_new_case(True))
        self.save_button.clicked.connect(self.on_save_case)
        self.gencase_button.clicked.connect(self.on_execute_gencase)
        self.new_case_menu.triggered.connect(self.on_newdoc_menu)
        self.save_menu.triggered.connect(self.on_save_menu)
        self.load_button.clicked.connect(self.on_load_button)
        self.add_fillbox_button.clicked.connect(self.on_add_fillbox)
        self.add_geometry_button.clicked.connect(self.on_add_geo)
        self.import_xml_button.clicked.connect(lambda: error_dialog("XML Import is not available in this version."))
        self.case_summary_button.clicked.connect(CaseSummary)
        self.toggle_2d_mode_button.clicked.connect(self.on_2d_toggle)
        self.special_button.clicked.connect(SpecialOptionsSelectorDialog)

        self.label_layout.addWidget(self.casecontrols_label)
        self.label_layout.addStretch(1)
        self.label_layout.addWidget(self.force_button)
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
        """ Defines what happens when new case is clicked. Closes all documents
            if possible and creates a FreeCAD document with Case Limits object. """
        if document_count() and not prompt_close_all_documents(prompt):
            return

        create_dsph_document()
        Case.the().reset()
        Case.the().add_object(SimulationObject(CASE_LIMITS_OBJ_NAME, -1, ObjectType.SPECIAL, ObjectFillMode.SPECIAL))

        self.case_created.emit()
        self.update_dp.emit()
        self.need_refresh.emit()

    def on_new_from_freecad_document(self, prompt=True):
        """ Creates a new case based on an existing FreeCAD document.
        This is specially useful for CAD users that want to use existing geometry for DesignSPHysics. """
        file_name, _ = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), "Select document to import", Case.the().info.last_used_directory)
        Case.the().info.update_last_used_directory(file_name)
        if file_name and document_count() and not prompt_close_all_documents(prompt):
            return

        create_dsph_document_from_fcstd(file_name)
        Case.the().reset()
        Case.the().add_object_to_sim(SimulationObject(CASE_LIMITS_OBJ_NAME, -1, ObjectType.SPECIAL, ObjectFillMode.SPECIAL))

        self.update_dp.emit()
        self.case_created.emit()
        self.need_refresh.emit()

    def on_save_case(self, save_as=None):
        """ Defines what happens when save case button is clicked.
        Saves a freecad scene definition, and a dump of dsph data for the case."""
        self.need_refresh.emit()
        if Case.the().was_not_saved() or save_as:
            save_name, _ = QtGui.QFileDialog.getSaveFileName(self, __("Save Case"), Case.the().info.last_used_directory)
            Case.the().info.update_last_used_directory(save_name)
        else:
            save_name = Case.the().path

        if not save_name:
            return

        Case.the().info.needs_to_run_gencase = True
        save_case(save_name, Case.the())
        save_current_freecad_document(Case.the().path)
        if Case.the().has_materials() and Case.the().execution_parameters.rigidalgorithm not in (2, 3):
            warning_dialog(
                __("Properties and Material information wasn't written. See details for more info."),
                __("The case being saved has some properties/materials defined in one of its MKs.\n"
                   "However, the solid-solid interaction on the execution parameters must be set to DEM or CHRONO for this feature to work.")
            )

    def on_execute_gencase(self):
        """ Saves data into disk and uses GenCase to generate the case files."""
        self.on_save_case()
        if not Case.the().executable_paths.gencase:
            warning_dialog(__("GenCase executable is not set."))
            return

        gencase_full_path = path.abspath(Case.the().executable_paths.gencase)
        arguments = ["{path}/{name}_Def".format(path=Case.the().path, name=Case.the().name),
                     "{path}/{name}_out/{name}".format(path=Case.the().path, name=Case.the().name),
                     "-save:+all"]
        cmd_string = "{} {}".format(gencase_full_path, " ".join(arguments))

        refocus_cwd()
        process = QtCore.QProcess(get_fc_main_window())
        process.setWorkingDirectory(Case.the().path)
        process.start(gencase_full_path, arguments)
        debug("Executing -> {}".format(cmd_string))
        process.waitForFinished()

        output = str(process.readAllStandardOutput().data(), encoding='utf-8')

        if process.exitCode():
            Case.the().info.is_gencase_done = False
            error_dialog(__("Error executing GenCase. Did you add objects to the case?. Another reason could be memory issues. View details for more info."), output)
        else:
            try:
                total_particles_text = output[output.index("Total particles: "):output.index(" (bound=")]
                total_particles = int(total_particles_text[total_particles_text.index(": ") + 2:])
                Case.the().info.particle_number = total_particles
                GencaseCompletedDialog(particle_count=total_particles, detail_text=output, cmd_string=cmd_string, parent=get_fc_main_window()).show()
                Case.the().info.is_gencase_done = True
                self.on_save_case()
                Case.the().info.needs_to_run_gencase = False
            except ValueError:
                print_exc()
                Case.the().info.is_gencase_done = False
                Case.the().info.needs_to_run_gencase = True

        # Refresh widget enable/disable status as GenCase finishes
        self.gencase_completed.emit(Case.the().info.is_gencase_done)

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

        load_path, _ = QtGui.QFileDialog.getOpenFileName(self, __("Load Case"), Case.the().info.last_used_directory, "casedata.dsphdata")
        Case.the().info.update_last_used_directory(load_path)

        if load_path == "":
            return

        disk_data: Case = load_case(load_path)
        if not disk_data:
            return

        try:
            Case.update_from_disk(disk_data)
            self.update_dp.emit()
        except (EOFError, ValueError):
            error_dialog(__("There was an error importing the case  You probably need to set them again.\n\n"
                            "This could be caused due to file corruption, caused by operating system based line endings or ends-of-file, or other related aspects."))

        # User may have changed the name of the folder/project
        Case.the().path = path.dirname(load_path)
        Case.the().name = Case.the().path.split("/")[-1]

        # Adapt widget state to case info
        self.case_created.emit()
        self.gencase_completed.emit(Case.the().info.is_gencase_done)
        self.simulation_completed.emit(Case.the().info.is_simulation_done)
        self.need_refresh.emit()

        Case.the().executable_paths.check_and_filter()
        Case.the().info.update_last_used_directory(load_path)

    def on_add_fillbox(self):
        """ Add fillbox group. It consists in a group with 2 objects inside: a point and a box.
        The point represents the fill seed and the box sets the bounds for the filling. """
        add_fillbox_objects()

    def on_add_geo(self):
        """ Add STL file. Opens a file opener and allows the user to set parameters for the import process """
        self.need_refresh.emit()

        file_name, _ = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select GEO to import"), Case.the().info.last_used_directory, "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk)")
        Case.the().info.update_last_used_directory(file_name)
        if not file_name:
            return
        AddGEODialog(file_name, parent=get_fc_main_window())

    def on_2d_toggle(self):
        """ Handles Toggle 3D/2D Button. Changes the Case Limits object accordingly. """
        if not valid_document_environment():
            error("Not a valid case environment")
            return

        fc_object = get_fc_object(CASE_LIMITS_OBJ_NAME)

        if Case.the().mode3d:
            # 3D to 2D
            Case.the().info.last_3d_width = fc_object.Width.Value
            config_dialog = Mode2DConfigDialog(fc_object.Placement.Base.y, parent=get_fc_main_window())
            if config_dialog.exit_status == QtGui.QDialog.Rejected:
                return
            fc_object.Placement.Base.y = float(config_dialog.stored_y_value)
            fc_object.Label = CASE_LIMITS_2D_LABEL
            Case.the().mode3d = not Case.the().mode3d
        else:
            # 2D to 3D
            Case.the().mode3d = not Case.the().mode3d
            fc_object.Width = Case.the().info.last_3d_width if Case.the().info.last_3d_width > 0.0 else fc_object.Length
            fc_object.Label = CASE_LIMITS_3D_LABEL

    def adapt_to_no_case(self):
        """ Adapts the widget to an environment with no case opened. """
        for x in [self.save_button, self.add_fillbox_button, self.add_geometry_button, self.import_xml_button,
                  self.case_summary_button, self.toggle_2d_mode_button, self.special_button, self.gencase_button, self.force_button]:
            x.setEnabled(False)

    def adapt_to_new_case(self):
        """ Adapts the widget to an environment when a case is opened. """
        for x in [self.save_button, self.add_fillbox_button, self.add_geometry_button, self.import_xml_button,
                  self.case_summary_button, self.toggle_2d_mode_button, self.special_button, self.gencase_button, self.force_button]:
            x.setEnabled(True)

    def on_force_button(self):
        """ Triggers a signal implying that the force button was pressed. """
        self.force_pressed.emit()
