#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Dock Post Processing Widget '''

from PySide import QtGui

from mod.translation_tools import __

from mod.widgets.partvtk_dialog import PartVTKDialog
from mod.widgets.computeforces_dialog import ComputeForcesDialog
from mod.widgets.floatinginfo_dialog import FloatingInfoDialog
from mod.widgets.measuretool_dialog import MeasureToolDialog
from mod.widgets.isosurface_dialog import IsoSurfaceDialog
from mod.widgets.flowtool_dialog import FlowToolDialog


# FIXME: Replace this when refactored
widget_state_elements = {}


class DockPostProcessingWidget(QtGui.QWidget):
    '''DesignSPHysics Dock Post Processing Widget '''

    def __init__(self):
        super().__init__()

        # Post processing section scaffolding
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QtGui.QLabel("<b>" + __("Post-processing") + "</b>")
        self.title_label.setWordWrap(True)

        self.first_row_layout = QtGui.QHBoxLayout()
        self.second_row_layout = QtGui.QHBoxLayout()

        self.partvtk_button = QtGui.QPushButton(__("PartVTK"))
        self.computeforces_button = QtGui.QPushButton(__("ComputeForces"))
        self.isosurface_button = QtGui.QPushButton(__("IsoSurface"))
        self.floatinginfo_button = QtGui.QPushButton(__("FloatingInfo"))
        self.measuretool_button = QtGui.QPushButton(__("MeasureTool"))
        self.flowtool_button = QtGui.QPushButton(__("FlowTool"))

        self.partvtk_button.setToolTip(__("Opens the PartVTK tool."))
        self.computeforces_button.setToolTip(__("Opens the ComputeForces tool."))
        self.floatinginfo_button.setToolTip(__("Opens the FloatingInfo tool."))
        self.measuretool_button.setToolTip(__("Opens the MeasureTool tool."))
        self.isosurface_button.setToolTip(__("Opens the IsoSurface tool."))
        self.flowtool_button.setToolTip(__("Opens the FlowTool tool."))

        widget_state_elements['post_proc_partvtk_button'] = self.partvtk_button
        widget_state_elements['post_proc_computeforces_button'] = self.computeforces_button
        widget_state_elements['post_proc_floatinginfo_button'] = self.floatinginfo_button
        widget_state_elements['post_proc_measuretool_button'] = self.measuretool_button
        widget_state_elements['post_proc_isosurface_button'] = self.isosurface_button
        widget_state_elements['post_proc_flowtool_button'] = self.flowtool_button

        self.partvtk_button.clicked.connect(PartVTKDialog)
        self.computeforces_button.clicked.connect(ComputeForcesDialog)
        self.floatinginfo_button.clicked.connect(FloatingInfoDialog)
        self.measuretool_button.clicked.connect(MeasureToolDialog)
        self.isosurface_button.clicked.connect(IsoSurfaceDialog)
        self.flowtool_button.clicked.connect(FlowToolDialog)

        self.main_layout.addWidget(self.title_label)
        self.first_row_layout.addWidget(self.partvtk_button)
        self.first_row_layout.addWidget(self.computeforces_button)
        self.first_row_layout.addWidget(self.isosurface_button)
        self.second_row_layout.addWidget(self.floatinginfo_button)
        self.second_row_layout.addWidget(self.measuretool_button)
        self.second_row_layout.addWidget(self.flowtool_button)

        self.main_layout.addLayout(self.first_row_layout)
        self.main_layout.addLayout(self.second_row_layout)

        self.setLayout(self.main_layout)
