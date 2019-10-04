#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''Main DesignSPHysics Dock Widget '''

from PySide import QtGui, QtCore

from mod.gui_tools import h_line_generator

from mod.constants import MAIN_WIDGET_INTERNAL_NAME, APP_NAME, VERSION

from mod.dataobjects.case import Case

from mod.widgets.dock_logo_widget import DockLogoWidget
from mod.widgets.dock_configuration_widget import DockConfigurationWidget
from mod.widgets.dock_dp_widget import DockDPWidget
from mod.widgets.dock_pre_processing_widget import DockPreProcessingWidget
from mod.widgets.dock_simulation_widget import DockSimulationWidget
from mod.widgets.dock_post_processing_widget import DockPostProcessingWidget
from mod.widgets.dock_object_list_table_widget import DockObjectListTableWidget


class DesignSPHysicsDock(QtGui.QDockWidget):
    ''' Main DesignSPHysics Dock, containing all the tools needed to manage cases. '''

    need_refresh = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName(MAIN_WIDGET_INTERNAL_NAME)
        self.setWindowTitle("{} {}".format(APP_NAME, str(VERSION)))

        self.root_widget = QtGui.QWidget()
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(5, 0, 5, 0)

        self.dock_logo_widget = DockLogoWidget()
        self.dock_configuration_widget = DockConfigurationWidget()
        self.dp_widget = DockDPWidget()
        self.pre_proccessing_widget = DockPreProcessingWidget()
        self.simulation_widget = DockSimulationWidget()
        self.post_processing_widget = DockPostProcessingWidget()
        self.object_list_widget = DockObjectListTableWidget()

        self.main_layout.addWidget(self.dock_logo_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.dock_configuration_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.dp_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.pre_proccessing_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.simulation_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.post_processing_widget)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addWidget(self.object_list_widget)

        self.root_widget.setLayout(self.main_layout)
        self.setWidget(self.root_widget)

        self.adapt_to_no_case()

        # Signal handling
        self.pre_proccessing_widget.need_refresh.connect(self.need_refresh.emit)
        self.pre_proccessing_widget.update_dp.connect(self.on_signal_update_dp)
        self.pre_proccessing_widget.case_created.connect(self.adapt_to_new_case)
        self.pre_proccessing_widget.gencase_completed.connect(self.adapt_to_gencase_done)
        self.pre_proccessing_widget.simulation_completed.connect(self.adapt_to_simulation_done)
        self.simulation_widget.simulation_complete.connect(self.adapt_to_simulation_done)
        self.simulation_widget.simulation_started.connect(self.adapt_to_simulation_start)
        self.simulation_widget.simulation_cancelled.connect(self.adapt_to_simulation_cancel)

    def on_signal_update_dp(self):
        ''' Defines the behaviour on DP update request. '''
        self.dp_widget.dp_input.setText(str(Case.instance().dp))

    def refresh_object_list(self):
        ''' Refreshes the objects shown in the object list widget. '''
        self.object_list_widget.refresh()

    def adapt_to_no_case(self):
        ''' Adapts the dock to an environment with no case created/opened. '''
        self.dock_configuration_widget.adapt_to_no_case()
        self.dp_widget.setEnabled(False)
        self.pre_proccessing_widget.adapt_to_no_case()
        self.simulation_widget.setEnabled(False)
        self.post_processing_widget.setEnabled(False)
        self.object_list_widget.setEnabled(False)

    def adapt_to_new_case(self):
        ''' Adapts the dock to an environment with a new case created or loaded. '''
        self.dock_configuration_widget.adapt_to_new_case()
        self.dp_widget.setEnabled(True)
        self.pre_proccessing_widget.adapt_to_new_case()
        self.simulation_widget.setEnabled(False)
        self.post_processing_widget.setEnabled(False)
        self.object_list_widget.setEnabled(True)

    def adapt_to_gencase_done(self, state: bool) -> None:
        ''' Adapts the dock to an environment depending on if GenCase was executed. '''
        self.simulation_widget.setEnabled(state)

    def adapt_to_simulation_done(self, state: bool) -> None:
        ''' Adapts the dock to an environment depending on if GenCase was executed. '''
        self.post_processing_widget.setEnabled(state)

    def adapt_to_simulation_start(self):
        ''' Adapts the dock to an environment in which a simulation has just started. '''
        self.simulation_widget.setEnabled(False)

    def adapt_to_simulation_cancel(self):
        ''' Adapts the dock to an environment in which a simulation has been canceled. '''
        self.simulation_widget.setEnabled(True)
