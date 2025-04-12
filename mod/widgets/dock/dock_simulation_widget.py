#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Execution Widget """

import os
from sys import platform

# from PySide import QtGui, QtCore
from PySide6 import QtCore, QtWidgets

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.freecad_tools import get_fc_main_window
from mod.stdout_tools import log
from mod.dialog_tools import error_dialog, warning_dialog
from mod.executable_tools import refocus_cwd, ensure_process_is_executable_or_fail
from mod.file_tools import save_case

from mod.dataobjects.case import Case

from mod.widgets.run_dialog import RunDialog
from mod.widgets.run_additional_parameters_dialog import RunAdditionalParametersDialog


class DockSimulationWidget(QtWidgets.QWidget):
    """DesignSPHysics Dock Execution Widget """

    simulation_complete = QtCore.Signal(bool)
    simulation_started = QtCore.Signal()
    simulation_cancelled = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Execution section scaffolding
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QtWidgets.QLabel("<b>" + __("Simulation control") + "</b> ")
        self.title_label.setWordWrap(True)

        # Combobox for processor selection
        self.device_selector = QtWidgets.QComboBox()
        self.device_selector.addItem("CPU")
        self.device_selector.addItem("GPU")

        # Simulate case button
        self.execute_button = QtWidgets.QPushButton(__("Run"))
        self.execute_button.setStyleSheet("QPushButton {font-weight: bold; }")
        self.execute_button.setToolTip(__("Starts the case simulation. From the simulation\n"
                                          "window you can see the current progress and\n"
                                          "useful information."))
        self.execute_button.setIcon(get_icon("run.png"))
        self.execute_button.setIconSize(QtCore.QSize(12, 12))
        self.execute_button.clicked.connect(self.on_ex_simulate)

        # Additional parameters button
        self.additional_parameters_button = QtWidgets.QPushButton(__("Additional parameters"))
        self.additional_parameters_button.setToolTip(__("Sets simulation additional parameters for execution."))
        self.additional_parameters_button.clicked.connect(self.on_additional_parameters)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.execute_button)
        self.button_layout.addWidget(self.device_selector)
        self.button_layout.addWidget(self.additional_parameters_button)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def on_ex_simulate(self):
        """ Defines what happens on simulation button press.
            It shows the run window and starts a background process with dualsphysics running. Updates the window with useful info."""

        refocus_cwd()

        if Case.the().info.needs_to_run_gencase:
            # Warning window about save_case
            warning_dialog("You should run GenCase again. Otherwise, the obtained results may not be as expected")

        static_params_exe = [Case.the().get_out_xml_file_path(),
                             Case.the().get_out_folder_path(),
                             "-{device}".format(device=self.device_selector.currentText().lower()),
                             "-svres"]

        additional_parameters = list()
        if Case.the().info.run_additional_parameters:
            additional_parameters = Case.the().info.run_additional_parameters.split(" ")

        final_params_ex = static_params_exe + additional_parameters
        cmd_string = "{} {}".format(Case.the().executable_paths.dsphysics, " ".join(final_params_ex))

        run_dialog = RunDialog(case_name=Case.the().name, processor=self.device_selector.currentText(), number_of_particles=Case.the().info.particle_number, cmd_string=cmd_string, parent=get_fc_main_window())
        run_dialog.set_value(0)
        run_dialog.run_update(0, 0, None)
        Case.the().info.is_simulation_done = False

        run_fs_watcher = QtCore.QFileSystemWatcher()

        self.simulation_started.emit()

        # Cancel button handler
        def on_cancel():
            log(__("Stopping simulation"))
            if process:
                process.kill()
            run_dialog.hide_all()
            Case.the().info.is_simulation_done = True
            self.simulation_cancelled.emit()

        run_dialog.cancelled.connect(on_cancel)

        # Launch simulation and watch filesystem to monitor simulation
        filelist = [f for f in os.listdir(Case.the().path + "/" + Case.the().name + "_out/") if f.startswith("Part")]
        for f in filelist:
            os.remove(Case.the().path + "/" + Case.the().name + "_out/" + f)

        def on_dsph_sim_finished(exit_code):
            """ Simulation finish handler. Defines what happens when the process finishes."""

            # Reads output from the .out file and completes the progress bar
            output = ""
            with open(Case.the().path + "/" + Case.the().name + "_out/Run.out", "r", encoding="utf-8") as run_file:
                output = "".join(run_file.readlines())

            run_dialog.set_detail_text(str(output))
            run_dialog.run_complete()

            run_fs_watcher.removePath(Case.the().path + "/" + Case.the().name + "_out/")

            if exit_code == 0:
                # Simulation went correctly
                Case.the().info.is_simulation_done = True
                Case.the().info.needs_to_run_gencase = False
                self.simulation_complete.emit(True)
            else:
                # In case of an error
                Case.the().info.needs_to_run_gencase = True
                if "exception" in str(output).lower():
                    log("There was an error on the execution. Opening an error dialog for that.")
                    run_dialog.hide()
                    self.simulation_complete.emit(False)
                    error_dialog(__("An error occurred during execution. Make sure that parameters exist and are properly defined. "
                                    "You can also check your execution device (update the driver of your GPU). Read the details for more information."), str(output))
            if not save_case(Case.the().path, Case.the()):
                return

        # Launches a QProcess in background
        process = QtCore.QProcess(get_fc_main_window())
        process.finished.connect(on_dsph_sim_finished)

        ensure_process_is_executable_or_fail(Case.the().executable_paths.dsphysics)
        if platform in ("linux", "linux2"):
            os.environ["LD_LIBRARY_PATH"] = os.path.dirname(Case.the().executable_paths.dsphysics)
        process.start(Case.the().executable_paths.dsphysics, final_params_ex)

        def on_fs_change():
            """ Executed each time the filesystem changes. This updates the percentage of the simulation and its details."""
            run_file_data = ""
            with open(Case.the().path + "/" + Case.the().name + "_out/Run.out", "r", encoding="utf-8") as run_file:
                run_file_data = run_file.readlines()

            # Fill details window
            run_dialog.set_detail_text("".join(run_file_data))

            # Set percentage scale based on timemax
            for l in run_file_data:
                if Case.the().execution_parameters.timemax == -1:
                    if "TimeMax=" in l:
                        Case.the().execution_parameters.timemax = float(l.split("=")[1])

            current_value: float = 0.0
            totalpartsout: int = 0
            last_estimated_time = None

            # Update execution metrics
            last_part_lines = list(filter(lambda x: "Part_" in x and "stored" not in x and "      " in x, run_file_data))
            if last_part_lines:
                current_value = (float(last_part_lines[-1].split(None)[1]) * float(100)) / float(Case.the().execution_parameters.timemax)
            else:
                current_value = None

            # Update particles out
            last_particles_out_lines = list(filter(lambda x: "total out: " in x, run_file_data))
            if last_particles_out_lines:
                totalpartsout = int(last_particles_out_lines[-1].split("(total out: ")[1].split(")")[0])

            try:
                last_estimated_time = str(" ".join(last_part_lines[-1].split(None)[-2:]))
            except IndexError:
                last_estimated_time = None

            # Update run dialog
            run_dialog.run_update(current_value, totalpartsout, last_estimated_time)

        # Set filesystem watcher to the out directory.
        run_fs_watcher.addPath(Case.the().path + "/" + Case.the().name + "_out/")
        run_fs_watcher.directoryChanged.connect(on_fs_change)

        # Handle error on simulation start
        if process.state() == QtCore.QProcess.NotRunning:
            # Probably error happened.
            run_fs_watcher.removePath(Case.the().path + "/" + Case.the().name + "_out/")
            process = None
            error_dialog("Error on simulation start. Check that the DualSPHysics executable is correctly set.")
        else:
            run_dialog.show()

    def on_additional_parameters(self):
        """ Handles additional parameters button for execution """
        RunAdditionalParametersDialog(parent=get_fc_main_window())
