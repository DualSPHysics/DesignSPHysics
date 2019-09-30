#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''Main DesignSPHysics Dock Widget '''

from PySide import QtGui

from mod.gui_tools import h_line_generator, widget_state_config

from mod.constants import MAIN_WIDGET_INTERNAL_NAME, APP_NAME

from mod.widgets.dock_logo_widget import DockLogoWidget
from mod.widgets.dock_configuration_widget import DockConfigurationWidget
from mod.widgets.dock_dp_widget import DockDPWidget
from mod.widgets.dock_pre_processing_widget import DockPreProcessingWidget
from mod.widgets.dock_simulation_widget import DockSimulationWidget
from mod.widgets.dock_post_processing_widget import DockPostProcessingWidget
from mod.widgets.dock_object_list_table_widget import DockObjectListTableWidget

# FIXME: Replace this when refactored
widget_state_elements = {}


class DesignSPHysicsDock(QtGui.QDockWidget):
    ''' Main DesignSPHysics Dock, containing all the tools needed to manage cases. '''

    def __init__(self, version):
        super().__init__()

        self.setObjectName(MAIN_WIDGET_INTERNAL_NAME)
        self.setWindowTitle("{} {}".format(APP_NAME, str(version)))

        self.root_widget = QtGui.QWidget()
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(5, 0, 5, 0)

        self.dock_logo_widget = DockLogoWidget()
        self.dock_configuration_widget = DockConfigurationWidget()
        self.dp_widget = DockDPWidget()
        self.pre_proccessing_widget = DockPreProcessingWidget()
        self.simulation_widget = DockSimulationWidget()
        self.post_processing_widget = DockPostProcessingWidget()
        self.dock_object_list_table_widget = DockObjectListTableWidget()

        self.main_layout.addWidget(self.dock_logo_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.dp_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.pre_proccessing_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.simulation_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.post_processing_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.dock_object_list_table_widget)

        widget_state_config(widget_state_elements, "no case")

        self.root_widget.setLayout(self.main_layout)
        self.setWidget(self.root_widget)
