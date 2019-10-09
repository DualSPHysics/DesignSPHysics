#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Setup Plugin Dialog """

from PySide import QtGui

from mod.translation_tools import __
from mod.executable_tools import executable_contains_string
from mod.dialog_tools import warning_dialog, error_dialog
from mod.file_tools import get_designsphysics_path

from mod.dataobjects.case import Case


class SetupPluginDialog(QtGui.QDialog):

    def __init__(self):
        super(SetupPluginDialog, self).__init__()

        self.setWindowTitle("DesignSPHysics Setup")
        self.ok_button = QtGui.QPushButton("Ok")
        self.cancel_button = QtGui.QPushButton("Cancel")

        # GenCase path
        self.gencasepath_layout = QtGui.QHBoxLayout()
        self.gencasepath_label = QtGui.QLabel("GenCase Path: ")
        self.gencasepath_input = QtGui.QLineEdit()
        self.gencasepath_input.setText(Case.instance().executable_paths.gencase)
        self.gencasepath_input.setPlaceholderText("Put GenCase path here")
        self.gencasepath_browse = QtGui.QPushButton("...")

        self.gencasepath_layout.addWidget(self.gencasepath_label)
        self.gencasepath_layout.addWidget(self.gencasepath_input)
        self.gencasepath_layout.addWidget(self.gencasepath_browse)

        # DualSPHyisics path
        self.dsphpath_layout = QtGui.QHBoxLayout()
        self.dsphpath_label = QtGui.QLabel("DualSPHysics Path: ")
        self.dsphpath_input = QtGui.QLineEdit()
        self.dsphpath_input.setText(Case.instance().executable_paths.dsphysics)
        self.dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
        self.dsphpath_browse = QtGui.QPushButton("...")

        self.dsphpath_layout.addWidget(self.dsphpath_label)
        self.dsphpath_layout.addWidget(self.dsphpath_input)
        self.dsphpath_layout.addWidget(self.dsphpath_browse)

        # PartVTK4 path
        self.partvtk4path_layout = QtGui.QHBoxLayout()
        self.partvtk4path_label = QtGui.QLabel("PartVTK Path: ")
        self.partvtk4path_input = QtGui.QLineEdit()
        self.partvtk4path_input.setText(Case.instance().executable_paths.partvtk4)
        self.partvtk4path_input.setPlaceholderText("Put PartVTK4 path here")
        self.partvtk4path_browse = QtGui.QPushButton("...")

        self.partvtk4path_layout.addWidget(self.partvtk4path_label)
        self.partvtk4path_layout.addWidget(self.partvtk4path_input)
        self.partvtk4path_layout.addWidget(self.partvtk4path_browse)

        # ComputeForces path
        self.computeforces_layout = QtGui.QHBoxLayout()
        self.computeforces_label = QtGui.QLabel("ComputeForces Path: ")
        self.computeforces_input = QtGui.QLineEdit()
        self.computeforces_input.setText(Case.instance().executable_paths.computeforces)
        self.computeforces_input.setPlaceholderText("Put ComputeForces path here")
        self.computeforces_browse = QtGui.QPushButton("...")

        self.computeforces_layout.addWidget(self.computeforces_label)
        self.computeforces_layout.addWidget(self.computeforces_input)
        self.computeforces_layout.addWidget(self.computeforces_browse)

        # FloatingInfo path
        self.floatinginfo_layout = QtGui.QHBoxLayout()
        self.floatinginfo_label = QtGui.QLabel("FloatingInfo Path: ")
        self.floatinginfo_input = QtGui.QLineEdit()
        self.floatinginfo_input.setText(Case.instance().executable_paths.floatinginfo)
        self.floatinginfo_input.setPlaceholderText("Put FloatingInfo path here")
        self.floatinginfo_browse = QtGui.QPushButton("...")

        self.floatinginfo_layout.addWidget(self.floatinginfo_label)
        self.floatinginfo_layout.addWidget(self.floatinginfo_input)
        self.floatinginfo_layout.addWidget(self.floatinginfo_browse)

        # MeasureTool path
        self.measuretool_layout = QtGui.QHBoxLayout()
        self.measuretool_label = QtGui.QLabel("MeasureTool Path: ")
        self.measuretool_input = QtGui.QLineEdit()
        self.measuretool_input.setText(Case.instance().executable_paths.measuretool)
        self.measuretool_input.setPlaceholderText("Put MeasureTool path here")
        self.measuretool_browse = QtGui.QPushButton("...")

        self.measuretool_layout.addWidget(self.measuretool_label)
        self.measuretool_layout.addWidget(self.measuretool_input)
        self.measuretool_layout.addWidget(self.measuretool_browse)

        # IsoSurface path
        self.isosurface_layout = QtGui.QHBoxLayout()
        self.isosurface_label = QtGui.QLabel("IsoSurface Path: ")
        self.isosurface_input = QtGui.QLineEdit()
        self.isosurface_input.setText(Case.instance().executable_paths.isosurface)
        self.isosurface_input.setPlaceholderText("Put IsoSurface path here")
        self.isosurface_browse = QtGui.QPushButton("...")

        self.isosurface_layout.addWidget(self.isosurface_label)
        self.isosurface_layout.addWidget(self.isosurface_input)
        self.isosurface_layout.addWidget(self.isosurface_browse)

        # BoundaryVTK path
        self.boundaryvtk_layout = QtGui.QHBoxLayout()
        self.boundaryvtk_label = QtGui.QLabel("BoundaryVTK Path: ")
        self.boundaryvtk_input = QtGui.QLineEdit()
        self.boundaryvtk_input.setText(Case.instance().executable_paths.boundaryvtk)
        self.boundaryvtk_input.setPlaceholderText("Put BoundaryVTK path here")
        self.boundaryvtk_browse = QtGui.QPushButton("...")

        self.boundaryvtk_layout.addWidget(self.boundaryvtk_label)
        self.boundaryvtk_layout.addWidget(self.boundaryvtk_input)
        self.boundaryvtk_layout.addWidget(self.boundaryvtk_browse)

        # FlowTool path
        self.flowtool_layout = QtGui.QHBoxLayout()
        self.flowtool_label = QtGui.QLabel("FlowTool Path: ")
        self.flowtool_input = QtGui.QLineEdit()
        self.flowtool_input.setText(Case.instance().executable_paths.flowtool)
        self.flowtool_input.setPlaceholderText("Put FlowTool path here")
        self.flowtool_browse = QtGui.QPushButton("...")

        self.flowtool_layout.addWidget(self.flowtool_label)
        self.flowtool_layout.addWidget(self.flowtool_input)
        self.flowtool_layout.addWidget(self.flowtool_browse)

        # ParaView path
        self.paraview_layout = QtGui.QHBoxLayout()
        self.paraview_label = QtGui.QLabel("ParaView Path: ")
        self.paraview_input = QtGui.QLineEdit()
        self.paraview_input.setText(Case.instance().executable_paths.paraview)
        self.paraview_input.setPlaceholderText("Put ParaView path here")
        self.paraview_browse = QtGui.QPushButton("...")

        self.paraview_layout.addWidget(self.paraview_label)
        self.paraview_layout.addWidget(self.paraview_input)
        self.paraview_layout.addWidget(self.paraview_browse)

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

        # Button layout definition
        self.stp_button_layout = QtGui.QHBoxLayout()
        self.stp_button_layout.addStretch(1)
        self.stp_button_layout.addWidget(self.ok_button)
        self.stp_button_layout.addWidget(self.cancel_button)

        # START Main layout definition and composition.
        self.stp_main_layout = QtGui.QVBoxLayout()
        self.stp_main_layout.addLayout(self.gencasepath_layout)
        self.stp_main_layout.addLayout(self.dsphpath_layout)
        self.stp_main_layout.addLayout(self.partvtk4path_layout)
        self.stp_main_layout.addLayout(self.computeforces_layout)
        self.stp_main_layout.addLayout(self.floatinginfo_layout)
        self.stp_main_layout.addLayout(self.measuretool_layout)
        self.stp_main_layout.addLayout(self.isosurface_layout)
        self.stp_main_layout.addLayout(self.boundaryvtk_layout)
        self.stp_main_layout.addLayout(self.flowtool_layout)
        self.stp_main_layout.addLayout(self.paraview_layout)
        self.stp_main_layout.addStretch(1)

        self.stp_groupbox = QtGui.QGroupBox("Setup parameters")
        self.stp_groupbox.setLayout(self.stp_main_layout)
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.addWidget(self.stp_groupbox)
        self.main_layout.addLayout(self.stp_button_layout)
        self.setLayout(self.main_layout)
        # END Main layout definition and composition.

        self.resize(600, 400)
        self.exec_()

    def on_ok(self):
        Case.instance().executable_paths.gencase = self.gencasepath_input.text()
        Case.instance().executable_paths.dsphysics = self.dsphpath_input.text()
        Case.instance().executable_paths.partvtk4 = self.partvtk4path_input.text()
        Case.instance().executable_paths.computeforces = self.computeforces_input.text()
        Case.instance().executable_paths.floatinginfo = self.floatinginfo_input.text()
        Case.instance().executable_paths.measuretool = self.measuretool_input.text()
        Case.instance().executable_paths.isosurface = self.isosurface_input.text()
        Case.instance().executable_paths.boundaryvtk = self.boundaryvtk_input.text()
        Case.instance().executable_paths.flowtool = self.flowtool_input.text()
        Case.instance().executable_paths.paraview = self.paraview_input.text()
        if not Case.instance().executable_paths.check_and_filter():
            warning_dialog(__("One or more of the specified executables are not correct."),
                           __("Make sure all executable have execution permissions set (specially on GNU/Linux) and try to set the configuration again."))
        self.accept()

    def on_cancel(self):
        self.reject()

    def browse(self, app_name, input_prop) -> None:
        """ Generic browse method for other to wrap. """
        file_name, _ = QtGui.QFileDialog().getOpenFileName(self, __("Select {} path").format(app_name), get_designsphysics_path())
        if not file_name:
            return

        if executable_contains_string(file_name, app_name):
            input_prop.setText(file_name)
        else:
            error_dialog(__("Can't recognize {} in the selected executable.").format(app_name))

    def on_paraview_browse(self):
        file_name, _ = QtGui.QFileDialog().getOpenFileName(self, "Select ParaView path", get_designsphysics_path())
        if file_name:
            self.paraview_input.setText(file_name)
