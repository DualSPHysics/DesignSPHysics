#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Dock Execution Widget """

import os
import re
from sys import platform

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QAction

from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.dialog_tools import error_dialog, warning_dialog, info_dialog
from mod.tools.executable_tools import refocus_cwd, ensure_process_is_executable_or_fail
from mod.tools.freecad_tools import get_fc_main_window
from mod.functions import parse_ds_int
from mod.tools.gui_tools import get_icon
from mod.tools.script_tools import generate_ext_script
from mod.tools.stdout_tools import log, debug
from mod.tools.translation_tools import __
from mod.widgets.dock.dock_widgets.run_additional_parameters_dialog import RunAdditionalParametersDialog
from mod.widgets.dock.dock_widgets.run_dialog import RunDialog


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
        #self.device_selector.addItem("Generate script (CPU)")
        #self.device_selector.addItem("Generate script (GPU)")

        #self.executable_selector = QtWidgets.QComboBox()
        #self.executable_selector.addItem("Standard")
        #self.executable_selector.addItem("VRes")

        # Simulate case button
        self.execute_button = QtWidgets.QPushButton()
        self.execute_button.setStyleSheet("QPushButton {font-weight: bold; }")
        self.execute_button.setToolTip(__("Starts the case simulation. From the simulation\n"
                                          "window you can see the current progress and\n"
                                          "useful information."))
        self.execute_button.setIcon(get_icon("run.png"))
        self.execute_button.setIconSize(QtCore.QSize(14, 14))


        self.execute_button.setText("  {}".format(__("Run")))
#        self.execute_button.setFixedHeight(24)
        self.execute_menu = QtWidgets.QMenu()
        self.action_run = QAction(__("Local Run"))
        self.action_run.setIcon(get_icon("run.png"))
        self.action_generate_script = QAction(__("Generate_script"))
        self.action_generate_script.setIcon(get_icon("save.png"))
        self.execute_menu.addActions([self.action_run, self.action_generate_script])

        self.execute_button.setMenu(self.execute_menu)
        self.execute_menu.triggered.connect(self.on_simulate_menu)
        self.execute_menu.aboutToShow.connect(self.update_simulate_menu)



        # Additional parameters button
        self.additional_parameters_button = QtWidgets.QPushButton(__("Additional parameters"))
        self.additional_parameters_button.setToolTip(__("Sets simulation additional parameters for execution."))
        self.additional_parameters_button.clicked.connect(self.on_additional_parameters)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.execute_button)
        self.button_layout.addWidget(self.device_selector)
        #self.button_layout.addWidget(self.executable_selector)
        self.button_layout.addWidget(self.additional_parameters_button)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.button_layout)

        #self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.setLayout(self.main_layout)

    def update_simulate_menu(self):
        if (ApplicationSettings.the().basic_visualization):
            if self.execute_menu.actions():
                self.execute_menu.clear()
            self.on_simulate_menu(self.action_run)
        else:
            if not self.execute_menu.actions():
                self.execute_menu.addActions([self.action_run,self.action_generate_script])

    def on_simulate_menu(self,action):
        """ Handles the new document button and its dropdown items. """
        if __("Local Run") in action.text():
            self.on_ex_simulate()

        if __("Generate script") in action.text():
            self.on_ex_simulate(generate_script=True)

    def on_ex_simulate(self,generate_script=False):
        """ Defines what happens on simulation button press.
            It shows the run window and starts a background process with dualsphysics running. Updates the window with useful info."""

        refocus_cwd()
        if self.device_selector.currentIndex()==0:
            device="cpu"
        elif self.device_selector.currentIndex()==1:
            device = "gpu"

        #NOT WORKING IN WINDOWS 11
        if not Case.the().vres.active:
            xml_file = Case.the().get_out_xml_file_path()+".xml"
        else:
            xml_file = Case.the().get_out_xml_file_path() + "_vres00.xml"
        if not os.path.isfile(xml_file) and not generate_script:#Case.the().info.is_gencase_done and not generate_script:
            warning_dialog("Gencase output files not found. You should run GenCase before simulating",
                           Case.the().get_out_xml_file_path()+".xml not found")
            return

        if Case.the().info.recommends_to_run_gencase and not generate_script:
            # Warning window about save_case
            warning_dialog("You should run GenCase again. Otherwise, the obtained results may not be as expected")

        if not Case.the().vres.active:
            vres=False
            outdatadir=Case.the().path + "/" + Case.the().name + "_out/data/"
            static_params_exe = [Case.the().get_out_xml_file_path(),
                                 Case.the().get_out_folder_path(),
                                 f"-{device}",
                                 "-svres",
                                 "-dirdataout data"]
        else:
            vres=True
            outdatadir=Case.the().path + "/" + Case.the().name + "_out/data_vres00/"
            static_params_exe = [Case.the().get_out_xml_file_path(),
                                 Case.the().get_out_folder_path(),
                                 f"-{device}",
                                 "-svres",
                                 "-dirdataout data",
                                 "-vres"]


        additional_parameters = list()
        if Case.the().info.run_additional_parameters:
            additional_parameters = Case.the().info.run_additional_parameters.split(" ")

        final_params_ex = static_params_exe + additional_parameters
        cmd_string = "{} {}".format(Case.the().executable_paths.dsphysics, " ".join(final_params_ex))

        if generate_script:

            args=["{name}_out/{name}".format(name=Case.the().name),
             "{name}_out/".format(name=Case.the().name),
             f"-{device}",
             "-svres",
             "-dirdataout data"]

            if vres:
                args.append("-vres")
                generate_ext_script("simulate_vres",args,"")
            else:
                generate_ext_script("simulate", args, "")
            return

        run_dialog = RunDialog(case_name=Case.the().name, processor=self.device_selector.currentText(), number_of_particles=Case.the().info.particle_number, cmd_string=cmd_string, parent=None)
        run_dialog.set_value(0)
        run_dialog.run_update(0, 0, None)

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
            run_fs_watcher.removePath(outdatadir)

        run_dialog.cancelled.connect(on_cancel)

        # Launch simulation and watch filesystem to monitor simulation


        def on_dsph_sim_finished(exit_code):
            """ Simulation finish handler. Defines what happens when the process finishes."""
            log(f"Exit code: {exit_code}")
            # Reads output from the .out file and completes the progress bar
            output = ""
            with open(Case.the().path + "/" + Case.the().name + "_out/Run.out", "r", encoding="utf-8") as run_file:
                output = "".join(run_file.readlines())

            run_dialog.set_detail_text(str(output))
            run_dialog.run_complete()

            run_fs_watcher.removePath(outdatadir)

            if exit_code == 0:
                # Simulation went correctly
                Case.the().info.recommends_to_run_gencase = False
                self.simulation_complete.emit(True)
            else:
                # In case of an error
                Case.the().info.recommends_to_run_gencase = True
                if "exception" in str(output).lower():
                    log("There was an error on the execution. Opening an error dialog for that.")
                    run_dialog.hide()
                    self.simulation_complete.emit(False)
                    error_dialog(__("An error occurred during execution. Make sure that parameters exist and are properly defined. "
                                    "You can also check your execution device (update the driver of your GPU). Read the details for more information."), str(output))
                try:
                    error_output=str(output).split("Exception")[1].split("Text: ")[1].split("Finished")[0]
                    self.check_output_errors(error_output)
                except IndexError:
                    pass
            #if not save_case(Case.the().path, Case.the()):
            return


        # Launches a QProcess in background
        log("Starting simulation")
        log(f"Executing {cmd_string}")
        process = QtCore.QProcess(get_fc_main_window())
        process.finished.connect(on_dsph_sim_finished)

        if not vres:
            if platform in ("linux", "linux2"):
                os.environ["LD_LIBRARY_PATH"] = os.path.dirname(Case.the().executable_paths.dsphysics)
            if not os.path.exists(outdatadir):
                if os.path.exists(Case.the().path + "/" + Case.the().name + "_out/data_vres00/"):
                    warning_dialog("It looks like you are simulating a VRES case. Please select VRes in simulation control panel")
                    return 1
            else:
                filelist = [f for f in os.listdir(outdatadir) if
                            f.startswith("Part")]
                for f in filelist:
                    os.remove(outdatadir + f)
            ensure_process_is_executable_or_fail(Case.the().executable_paths.dsphysics)
            log(f"{Case.the().executable_paths.dsphysics} {final_params_ex}")
            process.start(Case.the().executable_paths.dsphysics, final_params_ex)
        else:
            if platform in ("linux", "linux2"):
                os.environ["LD_LIBRARY_PATH"] = os.path.dirname(Case.the().executable_paths.dsphysics)
            #if os.path.exists(Case.the().path + "/" + Case.the().name + "_out/data_vres00/"):
            #    warning_dialog(
            #        "It looks like you are simulating a VRES case. Please select VRes in simulation control panel")
            #    return 1
            dirlist = [d for d in os.listdir(Case.the().path + "/" + Case.the().name + "_out/") if
                        d.startswith("data")]
            for d in dirlist:
                filelist = [f for f in os.listdir(Case.the().path + "/" + Case.the().name + "_out/" + d) if
                            f.startswith("Part")]
                for f in filelist:
                    os.remove(Case.the().path + "/" + Case.the().name + "_out/" + d +os.sep+ f)
            ensure_process_is_executable_or_fail(Case.the().executable_paths.dsphysics)
            process.start(Case.the().executable_paths.dsphysics, final_params_ex)
        log("Simulation just started")

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
            last_part_lines = list(filter(lambda x: re.match('^[0-9]{4,}', x) and "stored" not in x and "      " in x, run_file_data))
            if last_part_lines:
                current_value = (float(last_part_lines[-1].split(None)[1]) * float(100)) / float(Case.the().execution_parameters.timemax)
            else:
                current_value = None

            # Update particles out
            last_particles_out_lines = list(filter(lambda x: "total out: " in x, run_file_data))
            if last_particles_out_lines:
                totalpartsout = parse_ds_int(last_particles_out_lines[-1].split("(total out: ")[1].split(")")[0])

            try:
                last_estimated_time = str(" ".join(last_part_lines[-1].split(None)[-2:]))
            except IndexError:
                last_estimated_time = None

            # Update run dialog
            run_dialog.run_update(current_value, totalpartsout, last_estimated_time)

        # Set filesystem watcher to the out directory.

        # Handle error on simulation start
        if process.state() == QtCore.QProcess.NotRunning:
            # Probably error happened.
            run_fs_watcher.removePath(outdatadir)
            process = None
            error_dialog("Error on simulation start. Check that the DualSPHysics executable is correctly set.")
        else:
            run_dialog.show()

        if not os.path.exists(outdatadir):
            os.mkdir(outdatadir)
        run_fs_watcher.addPath(outdatadir)
        run_fs_watcher.directoryChanged.connect(on_fs_change)

    def on_additional_parameters(self):
        """ Handles additional parameters button for execution """
        RunAdditionalParametersDialog(parent=None)

    def check_output_errors(self,text:str):
        errors={'The initial condition does not include any initial particle. ': "Please Add some particles to the geometry",
                 "Constant 'b' cannot be zero.": "Add fluid to the simulation or set HSWL or SpeedSystem Constants section",
                 "Point for inlet conditions with position": "Inlet is outside of domain. Move the inlet inside particle's domain or modify the comain size in 'Execution parameters'"}
        more_errors=False
        for e in errors.keys():
            if text.startswith(e):
                warning_dialog(errors[e])
            else:
                more_errors=True
        if more_errors:
            warning_dialog(text)

