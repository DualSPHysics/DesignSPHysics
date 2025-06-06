#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Setup Plugin Dialog """


from PySide2 import QtWidgets

from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.dialog_tools import error_dialog
from mod.tools.executable_tools import executable_contains_string
from mod.tools.file_tools import get_default_config_file
from mod.tools.freecad_tools import get_fc_main_window
from mod.tools.gui_tools import h_line_generator
from mod.tools.translation_tools import __
from mod.widgets.dock.dock_widgets.feature_support_dialog import FeatureSupportDialog


class SetupPluginDialog(QtWidgets.QDialog):
    """ A configuration dialog to set up the DesignSPHysics plugin for FreeCAD. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("DesignSPHysics Setup")
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.defaults_button = QtWidgets.QPushButton(__("Load defaults"))
        self.feature_support_button = QtWidgets.QPushButton(__("Feature support report"))

        # GenCase path
        self.gencasepath_layout = QtWidgets.QHBoxLayout()
        self.gencasepath_label = QtWidgets.QLabel("GenCase Path: ")
        self.gencasepath_input = QtWidgets.QLineEdit()
        self.gencasepath_input.setText(Case.the().executable_paths.gencase)
        self.gencasepath_input.setPlaceholderText("Put GenCase path here")
        self.gencasepath_browse = QtWidgets.QPushButton("...")

        self.gencasepath_layout.addWidget(self.gencasepath_label)
        self.gencasepath_layout.addWidget(self.gencasepath_input)
        self.gencasepath_layout.addWidget(self.gencasepath_browse)

        # DualSPHyisics path
        self.dsphpath_layout = QtWidgets.QHBoxLayout()
        self.dsphpath_label = QtWidgets.QLabel("DualSPHysics Path: ")
        self.dsphpath_input = QtWidgets.QLineEdit()
        self.dsphpath_input.setText(Case.the().executable_paths.dsphysics)
        self.dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
        self.dsphpath_browse = QtWidgets.QPushButton("...")

        self.dsphpath_layout.addWidget(self.dsphpath_label)
        self.dsphpath_layout.addWidget(self.dsphpath_input)
        self.dsphpath_layout.addWidget(self.dsphpath_browse)

        # PartVTK path
        self.partvtkpath_layout = QtWidgets.QHBoxLayout()
        self.partvtkpath_label = QtWidgets.QLabel("PartVTK Path: ")
        self.partvtkpath_input = QtWidgets.QLineEdit()
        self.partvtkpath_input.setText(Case.the().executable_paths.partvtk)
        self.partvtkpath_input.setPlaceholderText("Put PartVTK path here")
        self.partvtkpath_browse = QtWidgets.QPushButton("...")

        self.partvtkpath_layout.addWidget(self.partvtkpath_label)
        self.partvtkpath_layout.addWidget(self.partvtkpath_input)
        self.partvtkpath_layout.addWidget(self.partvtkpath_browse)

        # ComputeForces path
        self.computeforces_layout = QtWidgets.QHBoxLayout()
        self.computeforces_label = QtWidgets.QLabel("ComputeForces Path: ")
        self.computeforces_input = QtWidgets.QLineEdit()
        self.computeforces_input.setText(Case.the().executable_paths.computeforces)
        self.computeforces_input.setPlaceholderText("Put ComputeForces path here")
        self.computeforces_browse = QtWidgets.QPushButton("...")

        self.computeforces_layout.addWidget(self.computeforces_label)
        self.computeforces_layout.addWidget(self.computeforces_input)
        self.computeforces_layout.addWidget(self.computeforces_browse)

        # FloatingInfo path
        self.floatinginfo_layout = QtWidgets.QHBoxLayout()
        self.floatinginfo_label = QtWidgets.QLabel("FloatingInfo Path: ")
        self.floatinginfo_input = QtWidgets.QLineEdit()
        self.floatinginfo_input.setText(Case.the().executable_paths.floatinginfo)
        self.floatinginfo_input.setPlaceholderText("Put FloatingInfo path here")
        self.floatinginfo_browse = QtWidgets.QPushButton("...")

        self.floatinginfo_layout.addWidget(self.floatinginfo_label)
        self.floatinginfo_layout.addWidget(self.floatinginfo_input)
        self.floatinginfo_layout.addWidget(self.floatinginfo_browse)

        # MeasureTool path
        self.measuretool_layout = QtWidgets.QHBoxLayout()
        self.measuretool_label = QtWidgets.QLabel("MeasureTool Path: ")
        self.measuretool_input = QtWidgets.QLineEdit()
        self.measuretool_input.setText(Case.the().executable_paths.measuretool)
        self.measuretool_input.setPlaceholderText("Put MeasureTool path here")
        self.measuretool_browse = QtWidgets.QPushButton("...")

        self.measuretool_layout.addWidget(self.measuretool_label)
        self.measuretool_layout.addWidget(self.measuretool_input)
        self.measuretool_layout.addWidget(self.measuretool_browse)

        # IsoSurface path
        self.isosurface_layout = QtWidgets.QHBoxLayout()
        self.isosurface_label = QtWidgets.QLabel("IsoSurface Path: ")
        self.isosurface_input = QtWidgets.QLineEdit()
        self.isosurface_input.setText(Case.the().executable_paths.isosurface)
        self.isosurface_input.setPlaceholderText("Put IsoSurface path here")
        self.isosurface_browse = QtWidgets.QPushButton("...")

        self.isosurface_layout.addWidget(self.isosurface_label)
        self.isosurface_layout.addWidget(self.isosurface_input)
        self.isosurface_layout.addWidget(self.isosurface_browse)

        # BoundaryVTK path
        self.boundaryvtk_layout = QtWidgets.QHBoxLayout()
        self.boundaryvtk_label = QtWidgets.QLabel("BoundaryVTK Path: ")
        self.boundaryvtk_input = QtWidgets.QLineEdit()
        self.boundaryvtk_input.setText(Case.the().executable_paths.boundaryvtk)
        self.boundaryvtk_input.setPlaceholderText("Put BoundaryVTK path here")
        self.boundaryvtk_browse = QtWidgets.QPushButton("...")

        self.boundaryvtk_layout.addWidget(self.boundaryvtk_label)
        self.boundaryvtk_layout.addWidget(self.boundaryvtk_input)
        self.boundaryvtk_layout.addWidget(self.boundaryvtk_browse)

        # FlowTool path
        self.flowtool_layout = QtWidgets.QHBoxLayout()
        self.flowtool_label = QtWidgets.QLabel("FlowTool Path: ")
        self.flowtool_input = QtWidgets.QLineEdit()
        self.flowtool_input.setText(Case.the().executable_paths.flowtool)
        self.flowtool_input.setPlaceholderText("Put FlowTool path here")
        self.flowtool_browse = QtWidgets.QPushButton("...")

        self.flowtool_layout.addWidget(self.flowtool_label)
        self.flowtool_layout.addWidget(self.flowtool_input)
        self.flowtool_layout.addWidget(self.flowtool_browse)

        # BathymetryTool path
        self.bathymetrytool_layout = QtWidgets.QHBoxLayout()
        self.bathymetrytool_label = QtWidgets.QLabel("BathymetryTool Path: ")
        self.bathymetrytool_input = QtWidgets.QLineEdit()
        self.bathymetrytool_input.setText(Case.the().executable_paths.bathymetrytool)
        self.bathymetrytool_input.setPlaceholderText("Put BathymetryTool path here")
        self.bathymetrytool_browse = QtWidgets.QPushButton("...")

        self.bathymetrytool_layout.addWidget(self.bathymetrytool_label)
        self.bathymetrytool_layout.addWidget(self.bathymetrytool_input)
        self.bathymetrytool_layout.addWidget(self.bathymetrytool_browse)

        # ParaView path
        self.paraview_layout = QtWidgets.QHBoxLayout()
        self.paraview_label = QtWidgets.QLabel("ParaView Path: ")
        self.paraview_input = QtWidgets.QLineEdit()
        self.paraview_input.setText(Case.the().executable_paths.paraview)
        self.paraview_input.setPlaceholderText("Put ParaView path here")
        self.paraview_browse = QtWidgets.QPushButton("...")

        self.paraview_layout.addWidget(self.paraview_label)
        self.paraview_layout.addWidget(self.paraview_input)
        self.paraview_layout.addWidget(self.paraview_browse)

        # DualSPHyisics vres path
        # self.dsph_vrespath_layout = QtWidgets.QHBoxLayout()
        # self.dsph_vrespath_label = QtWidgets.QLabel("VRes Path: ")
        # self.dsph_vrespath_input = QtWidgets.QLineEdit()
        # self.dsph_vrespath_input.setText(Case.the().executable_paths.vres)
        # self.dsph_vrespath_input.setPlaceholderText("Put DualSPHysics path here")
        # self.dsph_vrespath_browse = QtWidgets.QPushButton("...")

        # self.dsph_vrespath_layout.addWidget(self.dsph_vrespath_label)
        # self.dsph_vrespath_layout.addWidget(self.dsph_vrespath_input)
        # self.dsph_vrespath_layout.addWidget(self.dsph_vrespath_browse)
        
        self.surfaces_stl_path_layout = QtWidgets.QHBoxLayout()
        self.surfaces_stl_path_label = QtWidgets.QLabel("SurfacesSTL Path: ")
        self.surfaces_stl_path_input = QtWidgets.QLineEdit()
        self.surfaces_stl_path_input.setText(Case.the().executable_paths.surfacesstl)
        self.surfaces_stl_path_input.setPlaceholderText("Put SurfacesSTL path here")
        self.surfaces_stl_path_browse = QtWidgets.QPushButton("...")

        self.surfaces_stl_path_layout.addWidget(self.surfaces_stl_path_label)
        self.surfaces_stl_path_layout.addWidget(self.surfaces_stl_path_input)
        self.surfaces_stl_path_layout.addWidget(self.surfaces_stl_path_browse)


        self.defaults_button.clicked.connect(self.on_set_defaults)
        self.feature_support_button.clicked.connect(self.on_feature_support)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.gencasepath_browse.clicked.connect(lambda: self.browse("GenCase", self.gencasepath_input))
        self.dsphpath_browse.clicked.connect(lambda: self.browse("DualSPHysics", self.dsphpath_input))
        self.partvtkpath_browse.clicked.connect(lambda: self.browse("PartVTK", self.partvtkpath_input))
        self.computeforces_browse.clicked.connect(lambda: self.browse("ComputeForces", self.computeforces_input))
        self.floatinginfo_browse.clicked.connect(lambda: self.browse("FloatingInfo", self.floatinginfo_input))
        self.measuretool_browse.clicked.connect(lambda: self.browse("MeasureTool", self.measuretool_input))
        self.boundaryvtk_browse.clicked.connect(lambda: self.browse("BoundaryVTK", self.boundaryvtk_input))
        self.flowtool_browse.clicked.connect(lambda: self.browse("FlowTool", self.flowtool_input))
        self.bathymetrytool_browse.clicked.connect(lambda: self.browse("Bathymetrytool", self.bathymetrytool_input))
        self.isosurface_browse.clicked.connect(lambda: self.browse("IsoSurface", self.isosurface_input))
        # self.dsph_vrespath_browse.clicked.connect(lambda: self.browse("DualSPHysics", self.dsph_vrespath_input))
        self.surfaces_stl_path_browse.clicked.connect(lambda: self.browse("SurfacesSTL", self.surfaces_stl_path_input))
        self.paraview_browse.clicked.connect(self.on_paraview_browse)

        # Executables definition and composition.
        self.executables_layout = QtWidgets.QVBoxLayout()
        self.executables_layout.addLayout(self.gencasepath_layout)
        self.executables_layout.addLayout(self.dsphpath_layout)
        self.executables_layout.addLayout(self.partvtkpath_layout)
        self.executables_layout.addLayout(self.computeforces_layout)
        self.executables_layout.addLayout(self.floatinginfo_layout)
        self.executables_layout.addLayout(self.measuretool_layout)
        self.executables_layout.addLayout(self.isosurface_layout)
        self.executables_layout.addLayout(self.boundaryvtk_layout)
        self.executables_layout.addLayout(self.flowtool_layout)
        self.executables_layout.addLayout(self.bathymetrytool_layout)
        self.executables_layout.addLayout(self.paraview_layout)
        # self.executables_layout.addLayout(self.dsph_vrespath_layout)
        self.executables_layout.addLayout(self.surfaces_stl_path_layout)


        self.executables_layout.addStretch(1)

        # General settings
        self.settings_layout = QtWidgets.QFormLayout()

        self.use_debug_check = QtWidgets.QCheckBox(__("Show debug messages"))
        self.use_debug_check.setChecked(ApplicationSettings.the().debug_enabled)
        self.use_verbose_check = QtWidgets.QCheckBox(__("Show verbose log messages"))
        self.use_verbose_check.setChecked(ApplicationSettings.the().verbose_enabled)
        self.use_version_check = QtWidgets.QCheckBox(__("Look for updates at startup"))
        self.use_version_check.setChecked(ApplicationSettings.the().notify_on_outdated_version_enabled)
        self.visualization_mode_label=QtWidgets.QLabel("Visualization mode")
        self.visualization_mode_combo = QtWidgets.QComboBox()
        self.visualization_mode_combo.addItems([__("Basic"),__("Advanced")])

        self.visualization_mode_combo.setCurrentIndex(0 if ApplicationSettings.the().basic_visualization else 1  )
        self.visualization_mode_layout=QtWidgets.QHBoxLayout()
        self.visualization_mode_layout.addWidget(self.visualization_mode_label)
        self.visualization_mode_layout.addWidget(self.visualization_mode_combo)
        self.settings_layout.addRow(self.use_debug_check)
        self.settings_layout.addRow(self.use_verbose_check)
        self.settings_layout.addRow(self.use_version_check)
        self.settings_layout.addRow(self.visualization_mode_layout)

        self.external_settings_label=QtWidgets.QLabel("External run settings")
        # DualSPHyisics path
        self.hpc_dsphpath_layout = QtWidgets.QHBoxLayout()
        self.hpc_dsphpath_label = QtWidgets.QLabel("External DualSPHysics Path: ")
        self.hpc_dsphpath_input = QtWidgets.QLineEdit()
        self.hpc_dsphpath_input.setText(ApplicationSettings.the().execs_path)
        self.hpc_dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
        self.hpc_dsphpath_layout.addWidget(self.hpc_dsphpath_label)
        self.hpc_dsphpath_layout.addWidget(self.hpc_dsphpath_input)

        # Custom script text
        self.custom_script_text_label = QtWidgets.QLabel("Custom script text: ")
        self.custom_script_text_input = QtWidgets.QTextEdit()
        self.custom_script_text_input.setText(ApplicationSettings.the().custom_script_text)
        self.custom_script_text_input.setPlaceholderText("Custom text to put on each script")


        self.os_select_layout=QtWidgets.QHBoxLayout()
        self.os_select_label=QtWidgets.QLabel(__("Operative system: "))
        self.os_select_combo=QtWidgets.QComboBox()
        self.os_select_combo.addItems(ApplicationSettings.the().os_available_list)
        self.os_select_combo.setCurrentIndex(ApplicationSettings.the().os_index)
        self.os_select_layout.addWidget(self.os_select_label)
        self.os_select_layout.addWidget(self.os_select_combo)


        self.settings_layout.addRow(h_line_generator())
        self.settings_layout.addRow(self.external_settings_label)
        self.settings_layout.addRow(self.hpc_dsphpath_layout)
        self.settings_layout.addRow(self.os_select_layout)
        self.settings_layout.addRow(self.custom_script_text_label)
        self.settings_layout.addRow(self.custom_script_text_input)


        # Tab widget composition
        self.tab_widget = QtWidgets.QTabWidget()

        self.executable_setup_widget = QtWidgets.QWidget()
        self.executable_setup_widget.setLayout(self.executables_layout)

        self.settings_setup_widget = QtWidgets.QWidget()
        self.settings_setup_widget.setLayout(self.settings_layout)

        self.tab_widget.addTab(self.executable_setup_widget, "Executables")
        self.tab_widget.addTab(self.settings_setup_widget, "Settings")

        # Button layout definition
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.defaults_button)
        self.button_layout.addWidget(self.feature_support_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.ok_button.setFocus()
        self.ok_button.setDefault(True)

        self.resize(600, 400)

    def on_ok(self):
        """ Dumps the data from the dialog onto the main case data structure. """
        Case.the().executable_paths.gencase = self.gencasepath_input.text()
        Case.the().executable_paths.dsphysics = self.dsphpath_input.text()
        Case.the().executable_paths.partvtk = self.partvtkpath_input.text()
        Case.the().executable_paths.computeforces = self.computeforces_input.text()
        Case.the().executable_paths.floatinginfo = self.floatinginfo_input.text()
        Case.the().executable_paths.measuretool = self.measuretool_input.text()
        Case.the().executable_paths.isosurface = self.isosurface_input.text()
        Case.the().executable_paths.boundaryvtk = self.boundaryvtk_input.text()
        Case.the().executable_paths.flowtool = self.flowtool_input.text()
        Case.the().executable_paths.bathymetrytool = self.bathymetrytool_input.text()
        Case.the().executable_paths.paraview = self.paraview_input.text()
        # Case.the().executable_paths.vres = self.dsphpath_input.text()
        Case.the().executable_paths.surfacesstl = self.surfaces_stl_path_input.text()
        Case.the().executable_paths.check_and_filter()

        ApplicationSettings.the().debug_enabled = self.use_debug_check.isChecked()
        ApplicationSettings.the().verbose_enabled = self.use_verbose_check.isChecked()
        ApplicationSettings.the().notify_on_outdated_version_enabled = self.use_version_check.isChecked()
        ApplicationSettings.the().basic_visualization = self.visualization_mode_combo.currentIndex()==0
        ApplicationSettings.the().execs_path=self.hpc_dsphpath_input.text()
        ApplicationSettings.the().custom_script_text = self.custom_script_text_input.toPlainText()
        ApplicationSettings.the().linux_os = self.os_select_combo.currentIndex()
        ApplicationSettings.the().persist()

        #Case.the().manager.update_properties()
        
        self.accept()

    def on_feature_support(self):
        """ Displays a dialog with the features currently supported by the currently configured executables. """
        current_executables = Case.the().executable_paths

        FeatureSupportDialog(current_executables).exec_()

    def on_set_defaults(self):
        """ Set the executable paths on the dialog to the defaults ones. """
        default_config: dict = get_default_config_file()
        self.gencasepath_input.setText(default_config["gencase"])
        self.dsphpath_input.setText(default_config["dsphysics"])
        self.partvtkpath_input.setText(default_config["partvtk"])
        self.computeforces_input.setText(default_config["computeforces"])
        self.floatinginfo_input.setText(default_config["floatinginfo"])
        self.measuretool_input.setText(default_config["measuretool"])
        self.isosurface_input.setText(default_config["isosurface"])
        self.boundaryvtk_input.setText(default_config["boundaryvtk"])
        self.flowtool_input.setText(default_config["flowtool"])
        self.bathymetrytool_input.setText(default_config["bathymetrytool"])
        # self.dsph_vrespath_input.setText(default_config["vres"])
        self.surfaces_stl_path_input.setText((default_config["surfacesstl"]))
        self.use_debug_check.setChecked(True)
        self.use_verbose_check.setChecked(True)
        self.use_version_check.setChecked(True)

    def on_cancel(self):
        """ Closes the dialog rejecting it. """
        self.reject()

    def browse(self, app_name, input_prop) -> None:
        """ Opens a file browser to check for the provided app name. """
        file_name, _ = QtWidgets.QFileDialog().getOpenFileName(self, __("Select {} path").format(app_name), Case.the().info.last_used_directory)
        Case.the().info.update_last_used_directory(file_name)

        self.ok_button.setFocus()

        if not file_name:
            return

        if executable_contains_string(file_name, app_name):
            input_prop.setText(file_name)
        else:
            error_dialog(__("{} in the selected executable cannot be recognised.").format(app_name))

    def on_paraview_browse(self):
        """ Opens a file dialog to select a paraview executable. """
        file_name, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Select ParaView path", Case.the().info.last_used_directory)
        if file_name:
            self.paraview_input.setText(file_name)
