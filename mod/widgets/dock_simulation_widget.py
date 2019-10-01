#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Dock Execution Widget '''

import os

from PySide import QtGui, QtCore

from mod.translation_tools import __
from mod.gui_tools import get_icon, widget_state_config
from mod.stdout_tools import debug, log, error, dump_to_disk
from mod.dialog_tools import error_dialog, warning_dialog

from mod.dataobjects.case import Case

from mod.widgets.run_dialog import RunDialog
from mod.widgets.run_additional_parameters_dialog import RunAdditionalParametersDialog


# FIXME: Replace this when refactored
widget_state_elements = {}
data = {}


class DockSimulationWidget(QtGui.QWidget):
    '''DesignSPHysics Dock Execution Widget '''

    def __init__(self):
        super().__init__()

        # Execution section scaffolding
        self.main_layout = QtGui.QVBoxLayout()
        self.title_label = QtGui.QLabel("<b>" + __("Simulation control") + "</b> ")
        self.title_label.setWordWrap(True)

        # Combobox for processor selection
        self.device_selector = QtGui.QComboBox()
        self.device_selector.addItem("CPU")
        self.device_selector.addItem("GPU")

        widget_state_elements['ex_selector_combo'] = self.device_selector

        # Simulate case button
        self.execute_button = QtGui.QPushButton(__("Run"))
        self.execute_button.setStyleSheet("QPushButton {font-weight: bold; }")
        self.execute_button.setToolTip(__("Starts the case simulation. From the simulation\n"
                                          "window you can see the current progress and\n"
                                          "useful information."))
        self.execute_button.setIcon(get_icon("run.png"))
        self.execute_button.setIconSize(QtCore.QSize(12, 12))
        self.execute_button.clicked.connect(self.on_ex_simulate)

        widget_state_elements['ex_button'] = self.execute_button

        # Additional parameters button
        self.additional_parameters_button = QtGui.QPushButton(__("Additional parameters"))
        self.additional_parameters_button.setToolTip("__(Sets simulation additional parameters for execution.)")
        self.additional_parameters_button.clicked.connect(self.on_additional_parameters)

        widget_state_elements['ex_additional'] = self.additional_parameters_button

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

        # FIXME: RunDialog has a really weird way of constructing. Change this to be more modular
        run_dialog = RunDialog()
        run_dialog.run_progbar_bar.setValue(0)
        Case.instance().info.is_simulation_done = False
        widget_state_config(widget_state_elements, "sim start")
        run_dialog.run_button_cancel.setText(__("Cancel Simulation"))
        run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
        run_dialog.run_group_label_case.setText(__("Case name: ") + Case.instance().name)
        run_dialog.run_group_label_proc.setText(__("Simulation processor: ") + str(self.device_selector.currentText()))
        run_dialog.run_group_label_part.setText(__("Number of particles: ") + str(Case.instance().info.particle_number))
        run_dialog.run_group_label_partsout.setText(__("Total particles out: ") + "0")
        run_dialog.run_group_label_eta.setText(__("Estimated time to complete simulation: ") + __("Calculating..."))
        run_dialog.run_group_label_completed.setVisible(False)

        # Cancel button handler
        def on_cancel():
            log(__("Stopping simulation"))
            if Case.instance().info.current_process:
                Case.instance().info.current_process.kill()
            run_dialog.hide()
            run_dialog.run_details.hide()
            Case.instance().info.is_simulation_done = False
            widget_state_config(widget_state_elements, "sim cancel")

        run_dialog.run_button_cancel.clicked.connect(on_cancel)

        def on_details():
            ''' Details button handler. Opens and closes the details pane on the execution window.'''
            if run_dialog.run_details.isVisible():
                debug('Hiding details pane on execution')
                run_dialog.run_details.hide()
            else:
                debug('Showing details pane on execution')
                run_dialog.run_details.show()
                run_dialog.run_details.move(run_dialog.x() - run_dialog.run_details.width() - 15, run_dialog.y())

        # Ensure run button has no connections
        try:
            run_dialog.run_button_details.clicked.disconnect()
        except RuntimeError:
            pass

        run_dialog.run_button_details.clicked.connect(on_details)

        # Launch simulation and watch filesystem to monitor simulation
        filelist = [f for f in os.listdir(Case.instance().path + '/' + Case.instance().name + "_out/") if f.startswith("Part")]
        for f in filelist:
            os.remove(Case.instance().path + '/' + Case.instance().name + "_out/" + f)

        def on_dsph_sim_finished(exit_code):
            ''' Simulation finish handler. Defines what happens when the process finishes.'''

            # Reads output and completes the progress bar
            output = Case.instance().info.current_process.readAllStandardOutput()
            run_dialog.run_details_text.setText(str(output))
            run_dialog.run_details_text.moveCursor(QtGui.QTextCursor.End)
            run_dialog.run_watcher.removePath(Case.instance().path + '/' + Case.instance().name + "_out/")
            run_dialog.setWindowTitle(__("DualSPHysics Simulation: Complete"))
            run_dialog.run_progbar_bar.setValue(100)
            run_dialog.run_button_cancel.setText(__("Close"))
            run_dialog.run_group_label_completed.setVisible(True)

            if exit_code == 0:
                # Simulation went correctly
                Case.instance().info.is_simulation_done = True
                widget_state_config(widget_state_elements, "sim finished")
            else:
                # In case of an error
                if "exception" in str(output).lower():
                    error(__("Exception in execution."))
                    run_dialog.setWindowTitle(__("DualSPHysics Simulation: Error"))
                    run_dialog.run_progbar_bar.setValue(0)
                    run_dialog.hide()
                    widget_state_config(widget_state_elements, "sim error")
                    execution_error_dialog = QtGui.QMessageBox()
                    execution_error_dialog.setText(__("An error occurred during execution. Make sure that parameters exist and are properly defined. "
                                                      "You can also check your execution device (update the driver of your GPU). "
                                                      "Read the details for more information."))
                    execution_error_dialog.setDetailedText(str(output).split("================================")[1])
                    execution_error_dialog.setIcon(QtGui.QMessageBox.Critical)
                    execution_error_dialog.exec_()

        # Launches a QProcess in background
        process = QtCore.QProcess(run_dialog)
        process.finished.connect(on_dsph_sim_finished)
        Case.instance().info.current_process = process
        static_params_exe = [
            Case.instance().path + '/' + Case.instance().name + "_out/" +
            Case.instance().name, Case.instance().path +
            '/' + Case.instance().name + "_out/",
            "-svres", "-" + str(self.device_selector.currentText()).lower()
        ]

        additional_params_ex = list()
        if Case.instance().info.run_additional_parameters:
            additional_params_ex = Case.instance().info.run_additional_parameters.split(" ")

        final_params_ex = static_params_exe + additional_params_ex
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
            run_dialog.run_details_text.setText("".join(run_file_data))
            run_dialog.run_details_text.moveCursor(QtGui.QTextCursor.End)

            # Set percentage scale based on timemax
            for l in run_file_data:
                if Case.instance().execution_parameters.timemax == -1:
                    if "TimeMax=" in l:
                        Case.instance().execution_parameters.timemax = float(l.split("=")[1])

            # Update execution metrics on GUI
            last_part_lines = list(filter(lambda x: "Part_" in x and "stored" not in x and "      " in x, run_file_data))
            if last_part_lines:
                current_value = (float(last_part_lines[-1].split("      ")[1]) * float(100)) / float(Case.instance().execution_parameters.timemax)
                run_dialog.run_progbar_bar.setValue(current_value)
                run_dialog.setWindowTitle(__("DualSPHysics Simulation: {}%").format(str(format(current_value, ".2f"))))
                run_dialog.run_group_label_eta.setText(__("Estimated time to complete simulation: ") + last_part_lines[-1].split("  ")[-1])

            # Update particles out on GUI
            last_particles_out_lines = list(filter(lambda x: "(total: " in x and "Particles out:" in x, run_file_data))
            if last_particles_out_lines:
                dump_to_disk("".join(last_particles_out_lines))
                totalpartsout = int(last_particles_out_lines[-1].split("(total: ")[1].split(")")[0])
                Case.instance().info.particles_out = totalpartsout
                run_dialog.run_group_label_partsout.setText(__("Total particles out: {}").format(str(Case.instance().info.particles_out)))

        # Set filesystem watcher to the out directory.
        run_dialog.run_watcher.addPath(Case.instance().path + '/' + Case.instance().name + "_out/")
        run_dialog.run_watcher.directoryChanged.connect(on_fs_change)

        Case.instance().info.needs_to_run_gencase = False

        # Handle error on simulation start
        if Case.instance().info.current_process.state() == QtCore.QProcess.NotRunning:
            # Probably error happened.
            run_dialog.run_watcher.removePath(Case.instance().path + '/' + Case.instance().name + "_out/")
            Case.instance().info.current_process = None
            error_dialog("Error on simulation start. Check that the DualSPHysics executable is correctly set.")
        else:
            run_dialog.show()

    def on_additional_parameters(self):
        ''' Handles additional parameters button for execution '''
        RunAdditionalParametersDialog()
