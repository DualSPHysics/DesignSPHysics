#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Dock Execution Widget '''

import os

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import log, error
from mod.dialog_tools import error_dialog, warning_dialog

from mod.dataobjects.case import Case

from mod.widgets.run_dialog import RunDialog
from mod.widgets.run_additional_parameters_dialog import RunAdditionalParametersDialog


class DockSimulationWidget(QtGui.QWidget):
    '''DesignSPHysics Dock Execution Widget '''

    def __init__(self):
        super().__init__()

        # Execution section scaffolding
        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QtGui.QLabel("<b>" + __("Simulation control") + "</b> ")
        self.title_label.setWordWrap(True)

        # Combobox for processor selection
        self.device_selector = QtGui.QComboBox()
        self.device_selector.addItem("CPU")
        self.device_selector.addItem("GPU")

        # Simulate case button
        self.execute_button = QtGui.QPushButton(__("Run"))
        self.execute_button.setStyleSheet("QPushButton {font-weight: bold; }")
        self.execute_button.setToolTip(__("Starts the case simulation. From the simulation\n"
                                          "window you can see the current progress and\n"
                                          "useful information."))
        self.execute_button.setIcon(get_icon("run.png"))
        self.execute_button.setIconSize(QtCore.QSize(12, 12))
        self.execute_button.clicked.connect(self.on_ex_simulate)

        # Additional parameters button
        self.additional_parameters_button = QtGui.QPushButton(__("Additional parameters"))
        self.additional_parameters_button.setToolTip("__(Sets simulation additional parameters for execution.)")
        self.additional_parameters_button.clicked.connect(self.on_additional_parameters)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addWidget(self.execute_button)
        self.button_layout.addWidget(self.device_selector)
        self.button_layout.addWidget(self.additional_parameters_button)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def on_ex_simulate(self):
        ''' Defines what happens on simulation button press.
            It shows the run window and starts a background process with dualsphysics running. Updates the window with useful info.'''

        if not Case.instance().info.needs_to_run_gencase:
            # Warning window about save_case
            warning_dialog("You should run GenCase again. Otherwise, the obtained results may not be as expected")

        run_dialog = RunDialog(Case.instance().name, self.device_selector.currentText(), Case.instance().info.particle_number)
        run_dialog.set_value(0)
        run_dialog.run_update(0, 0, None)

        run_fs_watcher = QtCore.QFileSystemWatcher()

        Case.instance().info.is_simulation_done = False
        # FIXME: When simulation starts we should disable some widgets to prevent the user messing up the execution

        # Cancel button handler
        def on_cancel():
            log(__("Stopping simulation"))
            if Case.instance().info.current_process:
                Case.instance().info.current_process.kill()
            run_dialog.hide_all()
            Case.instance().info.is_simulation_done = False
            # FIXME: Enable/Disable widgets accordingly when we cancel a simulation

        run_dialog.cancelled.connect(on_cancel)
        run_dialog.run_button_details.clicked.connect(run_dialog.toggle_run_details)

        # Launch simulation and watch filesystem to monitor simulation
        filelist = [f for f in os.listdir(Case.instance().path + '/' + Case.instance().name + "_out/") if f.startswith("Part")]
        for f in filelist:
            os.remove(Case.instance().path + '/' + Case.instance().name + "_out/" + f)

        def on_dsph_sim_finished(exit_code):
            ''' Simulation finish handler. Defines what happens when the process finishes.'''

            # Reads output and completes the progress bar
            output = Case.instance().info.current_process.readAllStandardOutput()
            run_dialog.set_detail_text(str(output))
            run_dialog.run_complete()

            run_fs_watcher.removePath(Case.instance().path + '/' + Case.instance().name + "_out/")

            if exit_code == 0:
                # Simulation went correctly
                Case.instance().info.is_simulation_done = True
                # FIXME: Enable/Disable appropriate widgets when simulation completes correctly
            else:
                # In case of an error
                if "exception" in str(output).lower():
                    error(__("Exception in execution."))
                    run_dialog.hide()

                    # FIXME: Enable/Disable widgets accordingly when a simulation exits with errors.
                    error_dialog(__("An error occurred during execution. Make sure that parameters exist and are properly defined. "
                                    "You can also check your execution device (update the driver of your GPU). Read the details for more information."),
                                 str(output).split("================================")[1])

        # Launches a QProcess in background
        process = QtCore.QProcess(run_dialog)
        process.finished.connect(on_dsph_sim_finished)

        Case.instance().info.current_process = process

        static_params_exe = [Case.instance().get_out_xml_file_path(),
                             Case.instance().get_out_folder_path(),
                             "-{device}".format(device=self.device_selector.currentText().lower()),
                             "-svres"]

        additional_parameters = list()
        if Case.instance().info.run_additional_parameters:
            additional_parameters = Case.instance().info.run_additional_parameters.split(" ")

        final_params_ex = static_params_exe + additional_parameters
        Case.instance().info.current_process.start(Case.instance().executable_paths.dsphysics, final_params_ex)

        def on_fs_change():
            ''' Executed each time the filesystem changes. This updates the percentage of the simulation and its details.'''
            run_file_data = ''
            try:
                with open(Case.instance().path + '/' + Case.instance().name + "_out/Run.out", "r") as run_file:
                    run_file_data = run_file.readlines()
            except Exception:
                pass

            # Fill details window
            run_dialog.set_detail_text("".join(run_file_data))

            # Set percentage scale based on timemax
            for l in run_file_data:
                if Case.instance().execution_parameters.timemax == -1:
                    if "TimeMax=" in l:
                        Case.instance().execution_parameters.timemax = float(l.split("=")[1])

            # Update execution metrics
            last_part_lines = list(filter(lambda x: "Part_" in x and "stored" not in x and "      " in x, run_file_data))
            if last_part_lines:
                current_value = (float(last_part_lines[-1].split("      ")[1]) * float(100)) / float(Case.instance().execution_parameters.timemax)

            # Update particles out
            last_particles_out_lines = list(filter(lambda x: "(total: " in x and "Particles out:" in x, run_file_data))
            if last_particles_out_lines:
                totalpartsout = int(last_particles_out_lines[-1].split("(total: ")[1].split(")")[0])
                Case.instance().info.particles_out = totalpartsout

            # Update run dialog
            run_dialog.run_update(current_value, Case.instance().info.particles_out, str(last_part_lines[-1].split("  ")[-1]))

        # Set filesystem watcher to the out directory.
        run_fs_watcher.addPath(Case.instance().path + '/' + Case.instance().name + "_out/")
        run_fs_watcher.directoryChanged.connect(on_fs_change)

        Case.instance().info.needs_to_run_gencase = False

        # Handle error on simulation start
        if Case.instance().info.current_process.state() == QtCore.QProcess.NotRunning:
            # Probably error happened.
            run_fs_watcher.removePath(Case.instance().path + '/' + Case.instance().name + "_out/")
            Case.instance().info.current_process = None
            error_dialog("Error on simulation start. Check that the DualSPHysics executable is correctly set.")
        else:
            run_dialog.show()

    def on_additional_parameters(self):
        ''' Handles additional parameters button for execution '''
        RunAdditionalParametersDialog()
