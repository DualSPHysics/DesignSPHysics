#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""Main DesignSPHysics Dock Widget """

from PySide import QtGui, QtCore

from mod.gui_tools import h_line_generator
from mod.freecad_tools import get_fc_main_window

from mod.constants import MAIN_WIDGET_INTERNAL_NAME, APP_NAME, VERSION

from mod.dataobjects.case import Case

from mod.widgets.dock.dock_logo_widget import DockLogoWidget
from mod.widgets.dock.dock_configuration_widget import DockConfigurationWidget
from mod.widgets.dock.dock_dp_widget import DockDPWidget
from mod.widgets.dock.dock_pre_processing_widget import DockPreProcessingWidget
from mod.widgets.dock.dock_simulation_widget import DockSimulationWidget
from mod.widgets.dock.dock_post_processing_widget import DockPostProcessingWidget
from mod.widgets.dock.dock_object_list_table_widget import DockObjectListTableWidget


class DesignSPHysicsDock(QtGui.QDockWidget):
    """ Main DesignSPHysics Dock, containing all the tools needed to manage cases. """

    need_refresh = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(MAIN_WIDGET_INTERNAL_NAME)
        self.setWindowTitle("{} {}".format(APP_NAME, str(VERSION)))

        self.root_widget = QtGui.QWidget()
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(5, 0, 5, 0)

        self.dock_logo_widget = DockLogoWidget(parent=get_fc_main_window())
        self.dock_configuration_widget = DockConfigurationWidget(parent=get_fc_main_window())
        self.dp_widget = DockDPWidget(parent=get_fc_main_window())
        self.pre_proccessing_widget = DockPreProcessingWidget(parent=get_fc_main_window())
        self.simulation_widget = DockSimulationWidget(parent=get_fc_main_window())
        self.post_processing_widget = DockPostProcessingWidget(parent=get_fc_main_window())
        self.object_list_widget = DockObjectListTableWidget(parent=get_fc_main_window())

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
        self.pre_proccessing_widget.force_pressed.connect(self.on_preprocessing_force_pressed)
        self.pre_proccessing_widget.need_refresh.connect(self.on_refresh)
        self.pre_proccessing_widget.update_dp.connect(self.on_signal_update_dp)
        self.pre_proccessing_widget.case_created.connect(self.adapt_to_new_case)
        self.pre_proccessing_widget.gencase_completed.connect(self.adapt_to_gencase_done)
        self.pre_proccessing_widget.simulation_completed.connect(self.adapt_to_simulation_done)
        self.simulation_widget.simulation_complete.connect(self.adapt_to_simulation_done)
        self.simulation_widget.simulation_started.connect(self.adapt_to_simulation_start)
        self.simulation_widget.simulation_cancelled.connect(self.adapt_to_simulation_cancel)

    def on_refresh(self):
        """ Reacts to a refresh signal emmited by the pre processing widget. """
        self.need_refresh.emit()
        self.dock_configuration_widget.update_case_name(Case.the().name)

    def on_signal_update_dp(self):
        """ Defines the behaviour on DP update request. """
        self.dp_widget.dp_input.setText(str(Case.the().dp))

    def refresh_object_list(self):
        """ Refreshes the objects shown in the object list widget. """
        self.object_list_widget.refresh()

    def adapt_to_no_case(self):
        """ Adapts the dock to an environment with no case created/opened. """
        self.dock_configuration_widget.adapt_to_no_case()
        self.dp_widget.setEnabled(False)
        self.pre_proccessing_widget.adapt_to_no_case()
        self.simulation_widget.setEnabled(False)
        self.post_processing_widget.setEnabled(False)
        self.object_list_widget.setEnabled(False)

    def adapt_to_new_case(self):
        """ Adapts the dock to an environment with a new case created or loaded. """
        self.dock_configuration_widget.adapt_to_new_case()
        self.dp_widget.setEnabled(True)
        self.pre_proccessing_widget.adapt_to_new_case()
        self.simulation_widget.setEnabled(False)
        self.post_processing_widget.setEnabled(False)
        self.object_list_widget.setEnabled(True)

    def adapt_to_gencase_done(self, state: bool) -> None:
        """ Adapts the dock to an environment depending on if GenCase was executed. """
        self.simulation_widget.setEnabled(state)

    def adapt_to_simulation_done(self, state: bool) -> None:
        """ Adapts the dock to an environment depending on if GenCase was executed. """
        self.post_processing_widget.setEnabled(state)

    def adapt_to_simulation_start(self):
        """ Adapts the dock to an environment in which a simulation has just started. """
        self.simulation_widget.setEnabled(False)

    def adapt_to_simulation_cancel(self):
        """ Adapts the dock to an environment in which a simulation has been canceled. """
        self.simulation_widget.setEnabled(True)
        self.post_processing_widget.setEnabled(Case.the().info.is_simulation_done)

    def on_preprocessing_force_pressed(self):
        """ Receives the force_pressed signal from th preprocessing widget and forcefully enables all widgets. """
        self.simulation_widget.setEnabled(True)
        self.post_processing_widget.setEnabled(True)
