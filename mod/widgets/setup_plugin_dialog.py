#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Setup Plugin Dialog """

from PySide import QtGui

from mod.translation_tools import __
from mod.executable_tools import executable_contains_string
from mod.dialog_tools import error_dialog
from mod.file_tools import get_default_config_file

from mod.dataobjects.case import Case
from mod.dataobjects.application_settings import ApplicationSettings


class SetupPluginDialog(QtGui.QDialog):
    """ A configuration dialog to set up the DesignSPHysics plugin for FreeCAD. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("DesignSPHysics Setup")
        self.ok_button = QtGui.QPushButton("OK")
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.defaults_button = QtGui.QPushButton(__("Load defaults"))

        # GenCase path
        self.gencasepath_layout = QtGui.QHBoxLayout()
        self.gencasepath_label = QtGui.QLabel("GenCase Path: ")
        self.gencasepath_input = QtGui.QLineEdit()
        self.gencasepath_input.setText(Case.the().executable_paths.gencase)
        self.gencasepath_input.setPlaceholderText("Put GenCase path here")
        self.gencasepath_browse = QtGui.QPushButton("...")

        self.gencasepath_layout.addWidget(self.gencasepath_label)
        self.gencasepath_layout.addWidget(self.gencasepath_input)
        self.gencasepath_layout.addWidget(self.gencasepath_browse)

        # DualSPHyisics path
        self.dsphpath_layout = QtGui.QHBoxLayout()
        self.dsphpath_label = QtGui.QLabel("DualSPHysics Path: ")
        self.dsphpath_input = QtGui.QLineEdit()
        self.dsphpath_input.setText(Case.the().executable_paths.dsphysics)
        self.dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
        self.dsphpath_browse = QtGui.QPushButton("...")

        self.dsphpath_layout.addWidget(self.dsphpath_label)
        self.dsphpath_layout.addWidget(self.dsphpath_input)
        self.dsphpath_layout.addWidget(self.dsphpath_browse)

        # PartVTK4 path
        self.partvtk4path_layout = QtGui.QHBoxLayout()
        self.partvtk4path_label = QtGui.QLabel("PartVTK Path: ")
        self.partvtk4path_input = QtGui.QLineEdit()
        self.partvtk4path_input.setText(Case.the().executable_paths.partvtk4)
        self.partvtk4path_input.setPlaceholderText("Put PartVTK4 path here")
        self.partvtk4path_browse = QtGui.QPushButton("...")

        self.partvtk4path_layout.addWidget(self.partvtk4path_label)
        self.partvtk4path_layout.addWidget(self.partvtk4path_input)
        self.partvtk4path_layout.addWidget(self.partvtk4path_browse)

        # ComputeForces path
        self.computeforces_layout = QtGui.QHBoxLayout()
        self.computeforces_label = QtGui.QLabel("ComputeForces Path: ")
        self.computeforces_input = QtGui.QLineEdit()
        self.computeforces_input.setText(Case.the().executable_paths.computeforces)
        self.computeforces_input.setPlaceholderText("Put ComputeForces path here")
        self.computeforces_browse = QtGui.QPushButton("...")

        self.computeforces_layout.addWidget(self.computeforces_label)
        self.computeforces_layout.addWidget(self.computeforces_input)
        self.computeforces_layout.addWidget(self.computeforces_browse)

        # FloatingInfo path
        self.floatinginfo_layout = QtGui.QHBoxLayout()
        self.floatinginfo_label = QtGui.QLabel("FloatingInfo Path: ")
        self.floatinginfo_input = QtGui.QLineEdit()
        self.floatinginfo_input.setText(Case.the().executable_paths.floatinginfo)
        self.floatinginfo_input.setPlaceholderText("Put FloatingInfo path here")
        self.floatinginfo_browse = QtGui.QPushButton("...")

        self.floatinginfo_layout.addWidget(self.floatinginfo_label)
        self.floatinginfo_layout.addWidget(self.floatinginfo_input)
        self.floatinginfo_layout.addWidget(self.floatinginfo_browse)

        # MeasureTool path
        self.measuretool_layout = QtGui.QHBoxLayout()
        self.measuretool_label = QtGui.QLabel("MeasureTool Path: ")
        self.measuretool_input = QtGui.QLineEdit()
        self.measuretool_input.setText(Case.the().executable_paths.measuretool)
        self.measuretool_input.setPlaceholderText("Put MeasureTool path here")
        self.measuretool_browse = QtGui.QPushButton("...")

        self.measuretool_layout.addWidget(self.measuretool_label)
        self.measuretool_layout.addWidget(self.measuretool_input)
        self.measuretool_layout.addWidget(self.measuretool_browse)

        # IsoSurface path
        self.isosurface_layout = QtGui.QHBoxLayout()
        self.isosurface_label = QtGui.QLabel("IsoSurface Path: ")
        self.isosurface_input = QtGui.QLineEdit()
        self.isosurface_input.setText(Case.the().executable_paths.isosurface)
        self.isosurface_input.setPlaceholderText("Put IsoSurface path here")
        self.isosurface_browse = QtGui.QPushButton("...")

        self.isosurface_layout.addWidget(self.isosurface_label)
        self.isosurface_layout.addWidget(self.isosurface_input)
        self.isosurface_layout.addWidget(self.isosurface_browse)

        # BoundaryVTK path
        self.boundaryvtk_layout = QtGui.QHBoxLayout()
        self.boundaryvtk_label = QtGui.QLabel("BoundaryVTK Path: ")
        self.boundaryvtk_input = QtGui.QLineEdit()
        self.boundaryvtk_input.setText(Case.the().executable_paths.boundaryvtk)
        self.boundaryvtk_input.setPlaceholderText("Put BoundaryVTK path here")
        self.boundaryvtk_browse = QtGui.QPushButton("...")

        self.boundaryvtk_layout.addWidget(self.boundaryvtk_label)
        self.boundaryvtk_layout.addWidget(self.boundaryvtk_input)
        self.boundaryvtk_layout.addWidget(self.boundaryvtk_browse)

        # FlowTool path
        self.flowtool_layout = QtGui.QHBoxLayout()
        self.flowtool_label = QtGui.QLabel("FlowTool Path: ")
        self.flowtool_input = QtGui.QLineEdit()
        self.flowtool_input.setText(Case.the().executable_paths.flowtool)
        self.flowtool_input.setPlaceholderText("Put FlowTool path here")
        self.flowtool_browse = QtGui.QPushButton("...")

        self.flowtool_layout.addWidget(self.flowtool_label)
        self.flowtool_layout.addWidget(self.flowtool_input)
        self.flowtool_layout.addWidget(self.flowtool_browse)

        # ParaView path
        self.paraview_layout = QtGui.QHBoxLayout()
        self.paraview_label = QtGui.QLabel("ParaView Path: ")
        self.paraview_input = QtGui.QLineEdit()
        self.paraview_input.setText(Case.the().executable_paths.paraview)
        self.paraview_input.setPlaceholderText("Put ParaView path here")
        self.paraview_browse = QtGui.QPushButton("...")

        self.paraview_layout.addWidget(self.paraview_label)
        self.paraview_layout.addWidget(self.paraview_input)
        self.paraview_layout.addWidget(self.paraview_browse)

        self.defaults_button.clicked.connect(self.on_set_defaults)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.gencasepath_browse.clicked.connect(lambda: self.browse("GenCase", self.gencasepath_input))
        self.dsphpath_browse.clicked.connect(lambda: self.browse("DualSPHysics", self.dsphpath_input))
        self.partvtk4path_browse.clicked.connect(lambda: self.browse("PartVTK4", self.partvtk4path_input))
        self.computeforces_browse.clicked.connect(lambda: self.browse("ComputeForces", self.computeforces_input))
        self.floatinginfo_browse.clicked.connect(lambda: self.browse("FloatingInfo", self.floatinginfo_input))
        self.measuretool_browse.clicked.connect(lambda: self.browse("MeasureTool", self.measuretool_input))
        self.boundaryvtk_browse.clicked.connect(lambda: self.browse("BoundaryVTK", self.boundaryvtk_input))
        self.flowtool_browse.clicked.connect(lambda: self.browse("FlowTool", self.flowtool_input))
        self.isosurface_browse.clicked.connect(lambda: self.browse("IsoSurface", self.isosurface_input))
        self.paraview_browse.clicked.connect(self.on_paraview_browse)

        # Executables definition and composition.
        self.executables_layout = QtGui.QVBoxLayout()
        self.executables_layout.addLayout(self.gencasepath_layout)
        self.executables_layout.addLayout(self.dsphpath_layout)
        self.executables_layout.addLayout(self.partvtk4path_layout)
        self.executables_layout.addLayout(self.computeforces_layout)
        self.executables_layout.addLayout(self.floatinginfo_layout)
        self.executables_layout.addLayout(self.measuretool_layout)
        self.executables_layout.addLayout(self.isosurface_layout)
        self.executables_layout.addLayout(self.boundaryvtk_layout)
        self.executables_layout.addLayout(self.flowtool_layout)
        self.executables_layout.addLayout(self.paraview_layout)
        self.executables_layout.addStretch(1)

        # General settings
        self.settings_layout = QtGui.QFormLayout()

        self.use_debug_check = QtGui.QCheckBox(__("Show debug messages"))
        self.use_debug_check.setChecked(ApplicationSettings.the().debug_enabled)
        self.use_verbose_check = QtGui.QCheckBox(__("Show verbose log messages"))
        self.use_verbose_check.setChecked(ApplicationSettings.the().verbose_enabled)
        self.use_version_check = QtGui.QCheckBox(__("Look for updates at startup"))
        self.use_version_check.setChecked(ApplicationSettings.the().notify_on_outdated_version_enabled)
        self.force_moordyn_support_check = QtGui.QCheckBox("Force MoorDyn Support")
        self.force_moordyn_support_check.setChecked(ApplicationSettings.the().force_moordyn_support_enabled)
        self.settings_layout.addRow(self.use_debug_check)
        self.settings_layout.addRow(self.use_verbose_check)
        self.settings_layout.addRow(self.use_version_check)
        self.settings_layout.addRow(self.force_moordyn_support_check)

        # Tab widget composition
        self.tab_widget = QtGui.QTabWidget()

        self.executable_setup_widget = QtGui.QWidget()
        self.executable_setup_widget.setLayout(self.executables_layout)

        self.settings_setup_widget = QtGui.QWidget()
        self.settings_setup_widget.setLayout(self.settings_layout)

        self.tab_widget.addTab(self.executable_setup_widget, "Executables")
        self.tab_widget.addTab(self.settings_setup_widget, "Settings")

        # Button layout definition
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addWidget(self.defaults_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.ok_button.setFocus()

        self.resize(600, 400)
        self.exec_()

    def on_ok(self):
        """ Dumps the data from the dialog onto the main case data structure. """
        Case.the().executable_paths.gencase = self.gencasepath_input.text()
        Case.the().executable_paths.dsphysics = self.dsphpath_input.text()
        Case.the().executable_paths.partvtk4 = self.partvtk4path_input.text()
        Case.the().executable_paths.computeforces = self.computeforces_input.text()
        Case.the().executable_paths.floatinginfo = self.floatinginfo_input.text()
        Case.the().executable_paths.measuretool = self.measuretool_input.text()
        Case.the().executable_paths.isosurface = self.isosurface_input.text()
        Case.the().executable_paths.boundaryvtk = self.boundaryvtk_input.text()
        Case.the().executable_paths.flowtool = self.flowtool_input.text()
        Case.the().executable_paths.paraview = self.paraview_input.text()
        Case.the().executable_paths.check_and_filter()

        ApplicationSettings.the().debug_enabled = self.use_debug_check.isChecked()
        ApplicationSettings.the().verbose_enabled = self.use_verbose_check.isChecked()
        ApplicationSettings.the().notify_on_outdated_version_enabled = self.use_version_check.isChecked()
        ApplicationSettings.the().force_moordyn_support_enabled = self.force_moordyn_support_check.isChecked()
        ApplicationSettings.the().persist()
        self.accept()

    def on_set_defaults(self):
        """ Set the executable paths on the dialog to the defaults ones. """
        default_config: dict = get_default_config_file()
        self.gencasepath_input.setText(default_config["gencase"])
        self.dsphpath_input.setText(default_config["dsphysics"])
        self.partvtk4path_input.setText(default_config["partvtk4"])
        self.computeforces_input.setText(default_config["computeforces"])
        self.floatinginfo_input.setText(default_config["floatinginfo"])
        self.measuretool_input.setText(default_config["measuretool"])
        self.isosurface_input.setText(default_config["isosurface"])
        self.boundaryvtk_input.setText(default_config["boundaryvtk"])
        self.flowtool_input.setText(default_config["flowtool"])
        self.use_debug_check.setChecked(True)
        self.use_verbose_check.setChecked(True)
        self.use_version_check.setChecked(True)

    def on_cancel(self):
        """ Closes the dialog rejecting it. """
        self.reject()

    def browse(self, app_name, input_prop) -> None:
        """ Opens a file browser to check for the provided app name. """
        file_name, _ = QtGui.QFileDialog().getOpenFileName(self, __("Select {} path").format(app_name), Case.the().info.last_used_directory)
        Case.the().info.update_last_used_directory(file_name)

        self.ok_button.setFocus()

        if not file_name:
            return

        if executable_contains_string(file_name, app_name):
            input_prop.setText(file_name)
        else:
            error_dialog(__("Can't recognize {} in the selected executable.").format(app_name))

    def on_paraview_browse(self):
        """ Opens a file dialog to select a paraview executable. """
        file_name, _ = QtGui.QFileDialog().getOpenFileName(self, "Select ParaView path", Case.the().info.last_used_directory)
        if file_name:
            self.paraview_input.setText(file_name)
