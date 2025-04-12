#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Post Processing Widget """

# from PySide import QtGui
from PySide6 import QtWidgets

from mod.translation_tools import __
from mod.freecad_tools import get_fc_main_window

from mod.widgets.postprocessing.partvtk_dialog import PartVTKDialog
from mod.widgets.postprocessing.computeforces_dialog import ComputeForcesDialog
from mod.widgets.postprocessing.floatinginfo_dialog import FloatingInfoDialog
from mod.widgets.postprocessing.measuretool_dialog import MeasureToolDialog
from mod.widgets.postprocessing.isosurface_dialog import IsoSurfaceDialog
from mod.widgets.postprocessing.flowtool_dialog import FlowToolDialog


class DockPostProcessingWidget(QtWidgets.QWidget):
    """DesignSPHysics Dock Post Processing Widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Post processing section scaffolding
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QtWidgets.QLabel("<b>{}</b>".format(__("Post-processing")))
        self.title_label.setWordWrap(True)

        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()

        self.partvtk_button = QtWidgets.QPushButton(__("PartVTK"))
        self.computeforces_button = QtWidgets.QPushButton(__("ComputeForces"))
        self.isosurface_button = QtWidgets.QPushButton(__("IsoSurface"))
        self.floatinginfo_button = QtWidgets.QPushButton(__("FloatingInfo"))
        self.measuretool_button = QtWidgets.QPushButton(__("MeasureTool"))
        self.flowtool_button = QtWidgets.QPushButton(__("FlowTool"))

        self.partvtk_button.setToolTip(__("Opens the PartVTK tool."))
        self.computeforces_button.setToolTip(__("Opens the ComputeForces tool."))
        self.floatinginfo_button.setToolTip(__("Opens the FloatingInfo tool."))
        self.measuretool_button.setToolTip(__("Opens the MeasureTool tool."))
        self.isosurface_button.setToolTip(__("Opens the IsoSurface tool."))
        self.flowtool_button.setToolTip(__("Opens the FlowTool tool."))

        self.partvtk_button.clicked.connect(lambda: PartVTKDialog(self, parent=get_fc_main_window()))
        self.computeforces_button.clicked.connect(lambda: ComputeForcesDialog(self, parent=get_fc_main_window()))
        self.floatinginfo_button.clicked.connect(lambda: FloatingInfoDialog(self, parent=get_fc_main_window()))
        self.measuretool_button.clicked.connect(lambda: MeasureToolDialog(self, parent=get_fc_main_window()))
        self.isosurface_button.clicked.connect(lambda: IsoSurfaceDialog(self, parent=get_fc_main_window()))
        self.flowtool_button.clicked.connect(lambda: FlowToolDialog(self, parent=get_fc_main_window()))

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

    def adapt_to_export_start(self) -> None:
        """ Adapts the widget to post processing tool start. """
        self.setWindowTitle("<b>{} ({})</b>".format(__("Post-processing"), __("Exporting")))
        self.setEnabled(False)

    def adapt_to_export_finished(self) -> None:
        """ Adapts the widget to post processing tool finish. """
        self.setEnabled(True)
        self.setWindowTitle("<b>{}</b>".format(__("Post-processing")))
