#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Post-Processing tools utilities. '''

import glob
import subprocess

from PySide import QtCore

from mod.translation_tools import __
from mod.stdout_tools import log, debug
from mod.dialog_tools import error_dialog
from mod.freecad_tools import get_fc_main_window

from mod.dataobjects.case import Case

from mod.widgets.info_dialog import InfoDialog
from mod.widgets.export_progress_dialog import ExportProgressDialog


def partvtk_export(export_parameters, post_processing_widget) -> None:
    ''' Export VTK button behaviour.
    Launches a process while disabling the button. '''
    post_processing_widget.adapt_to_export_start()

    export_dialog = ExportProgressDialog()

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()

        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    export_dialog.on_cancel.connect(on_cancel)

    # PartVTK export finish handler
    def on_export_finished(exit_code):

        post_processing_widget.adapt_to_export_finished()

        export_dialog.accept()

        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("PartVTK finished successfully"),
                detailed_text=Case.instance().info.current_output
            )
        else:
            error_dialog(
                __("There was an error on the post-processing. Show details to view the errors."),
                detailed_text=Case.instance().info.current_output
            )

        # Bit of code that tries to open ParaView if the option was selected.
        if export_parameters['open_paraview']:
            formats = {0: "vtk", 1: "csv", 2: "asc"}
            subprocess.Popen(
                [
                    Case.instance().executable_paths.paraview,
                    "--data={}\\{}_..{}".format(Case.instance().path + '\\' + Case.instance().name + '_out',
                                                export_parameters['file_name'], formats[export_parameters['save_mode']])
                ],
                stdout=subprocess.PIPE)

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)

    # Set save mode according to the dropdown menu
    save_mode = '-savevtk '
    if export_parameters['save_mode'] == 0:
        save_mode = '-savevtk '
    elif export_parameters['save_mode'] == 1:
        save_mode = '-savecsv '
    elif export_parameters['save_mode'] == 2:
        save_mode = '-saveascii '

    # Build parameters
    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        save_mode + Case.instance().path + '/' + Case.instance().name +
        '_out/' + export_parameters['file_name'],
        '-onlytype:' + export_parameters['save_types'] +
        " " + export_parameters['additional_parameters']
    ]

    debug("Going to execute: {} {}".format(Case.instance().executable_paths.partvtk4, " ".join(static_params_exp)))

    # Start process
    export_process.start(Case.instance().executable_paths.partvtk4, static_params_exp)
    Case.instance().info.current_export_process = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split(
                "{}_".format(export_parameters['file_name']))[1]
            if export_parameters['save_mode'] == 0:
                current_part = int(current_part.split(".vtk")[0])
            elif export_parameters['save_mode'] == 1:
                current_part = int(current_part.split(".csv")[0])
            elif export_parameters['save_mode'] == 2:
                current_part = int(current_part.split(".asc")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def floatinginfo_export(export_parameters, post_processing_widget) -> None:
    ''' FloatingInfo tool export. '''
    post_processing_widget.adapt_to_export_start()

    export_dialog = ExportProgressDialog()

    # Find total export parts
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()

        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    export_dialog.on_cancel.connect(on_cancel)

    def on_export_finished(exit_code):

        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("FloatingInfo finished successfully"),
                detailed_text=Case.instance().info.current_output)
        else:
            error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)

    static_params_exp = [
        '-dirin ' + Case.instance().path + '/' + Case.instance().name +
        '_out/', '-savemotion',
        '-savedata ' + Case.instance().path + '/' + Case.instance().name + '_out/' +
        export_parameters['filename'], export_parameters['additional_parameters']
    ]

    if export_parameters['onlyprocess']:
        static_params_exp.append('-onlymk:' + export_parameters['onlyprocess'])

    export_process.start(Case.instance().executable_paths.floatinginfo, static_params_exp)
    Case.instance().info.current_export_process = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("Part_")[1].split("  ")[0]
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def computeforces_export(export_parameters, post_processing_widget) -> None:
    ''' ComputeForces tool export. '''
    post_processing_widget.adapt_to_export_start()

    export_dialog = ExportProgressDialog()

    # Find total export parts
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()

        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    export_dialog.on_cancel.connect(on_cancel)

    def on_export_finished(exit_code):

        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("ComputeForces finished successfully."),
                detailed_text=Case.instance().info.current_output
            )
        else:
            error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)

    save_mode = '-savevtk '
    if export_parameters['save_mode'] == 0:
        save_mode = '-savevtk '
    elif export_parameters['save_mode'] == 1:
        save_mode = '-savecsv '
    elif export_parameters['save_mode'] == 2:
        save_mode = '-saveascii '

    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        '-filexml ' + Case.instance().path + '/' +
        Case.instance().name + '_out/' + Case.instance().name + '.xml',
        save_mode + Case.instance().path + '/' + Case.instance().name + '_out/' +
        export_parameters['filename'], export_parameters['additional_parameters']
    ]

    if export_parameters['onlyprocess']:
        static_params_exp.append(export_parameters['onlyprocess_tag'] + export_parameters['onlyprocess'])

    export_process.start(Case.instance().executable_paths.computeforces, static_params_exp)
    Case.instance().info.current_export_process = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("Part_")[1].split(".bi4")[0]
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(
        on_stdout_ready)


def measuretool_export(export_parameters, post_processing_widget) -> None:
    ''' MeasureTool tool export. '''
    post_processing_widget.adapt_to_export_start()

    export_dialog = ExportProgressDialog()

    # Find total export parts
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()

        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    export_dialog.on_cancel.connect(on_cancel)

    def on_export_finished(exit_code):

        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("MeasureTool finished successfully."),
                detailed_text=Case.instance().info.current_output
            )
        else:
            error_dialog(
                __("There was an error on the post-processing. Press the details button to see the error"),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)

    save_mode = '-savecsv '
    if export_parameters['save_mode'] == 0:
        save_mode = '-savevtk '
    elif export_parameters['save_mode'] == 1:
        save_mode = '-savecsv '
    elif export_parameters['save_mode'] == 2:
        save_mode = '-saveascii '

    # Save points to disk to later use them as parameter
    if len(Case.instance().info.measuretool_points) > len(Case.instance().info.measuretool_grid):
        # Save points
        with open(Case.instance().path + '/' + 'points.txt', 'w') as f:
            f.write("POINTS\n")
            for curr_point in Case.instance().info.measuretool_points:
                f.write("{}  {}  {}\n".format(*curr_point))
    else:
        # Save grid
        with open(Case.instance().path + '/' + 'points.txt', 'w') as f:
            for curr_point in Case.instance().info.measuretool_grid:
                f.write("POINTSLIST\n")
                f.write("{}  {}  {}\n{}  {}  {}\n{}  {}  {}\n".format(*curr_point))

    calculate_height = '-height' if export_parameters['calculate_water_elevation'] else ''

    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        '-filexml ' + Case.instance().path + '/' +
        Case.instance().name + '_out/' + Case.instance().name + '.xml',
        save_mode + Case.instance().path + '/' +
        Case.instance().name + '_out/' + export_parameters['filename'],
        '-points ' + Case.instance().path + '/points.txt', '-vars:' +
        export_parameters['save_vars'], calculate_height,
        export_parameters['additional_parameters']
    ]

    export_process.start(Case.instance().executable_paths.measuretool, static_params_exp)
    Case.instance().info.current_export_process = export_process

    def on_stdout_ready():
        # update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("/Part_")[1].split(".bi4")[0]
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(int(current_part))
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def isosurface_export(export_parameters, post_processing_widget) -> None:
    ''' Export IsoSurface button behaviour.
    Launches a process while disabling the button. '''
    post_processing_widget.adapt_to_export_start()

    export_dialog = ExportProgressDialog()

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()

        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    export_dialog.on_cancel.connect(on_cancel)

    # IsoSurface export finish handler
    def on_export_finished(exit_code):

        post_processing_widget.adapt_to_export_finished()

        export_dialog.accept()

        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("IsoSurface finished successfully."),
                detailed_text=Case.instance().info.current_output)
        else:
            error_dialog(
                __("There was an error on the post-processing."),
                detailed_text=Case.instance().info.current_output
            )

        # Bit of code that tries to open ParaView if the option was selected.
        if export_parameters['open_paraview']:
            subprocess.Popen(
                [Case.instance().executable_paths.paraview, "--data={}\\{}_..{}".format(
                    Case.instance().path + '\\' + Case.instance().name + '_out',
                    export_parameters['file_name'], "vtk")],
                stdout=subprocess.PIPE)

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)

    # Build parameters
    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        export_parameters["surface_or_slice"] + " " + Case.instance().path + '/' +
        Case.instance().name + '_out/' + export_parameters['file_name'] +
        " " + export_parameters['additional_parameters']
    ]

    # Start process
    export_process.start(Case.instance().executable_paths.isosurface, static_params_exp)
    Case.instance().info.current_export_process = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(export_parameters['file_name']))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)


def flowtool_export(export_parameters, post_processing_widget) -> None:
    ''' Export FlowTool button behaviour.
    Launches a process while disabling the button. '''
    post_processing_widget.adapt_to_export_start()

    export_dialog = ExportProgressDialog()

    # Find total export parts and adjust progress bar
    partfiles = glob.glob(Case.instance().path + '/' + Case.instance().name + "_out/" + "Part_*.bi4")
    for filename in partfiles:
        Case.instance().info.exported_parts = max(int(filename.split("Part_")[1].split(".bi4")[0]), Case.instance().info.exported_parts)
    export_dialog.set_range(0, Case.instance().info.exported_parts)
    export_dialog.set_value(0)

    export_dialog.show()

    # Cancel button handler
    def on_cancel():
        log(__("Stopping export"))
        if Case.instance().info.current_export_process is not None:
            Case.instance().info.current_export_process.kill()

        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    export_dialog.on_cancel.connect(on_cancel)

    # FlowTool export finish handler
    def on_export_finished(exit_code):

        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()

        if exit_code == 0:
            # Exported correctly
            Case.instance().info.current_info_dialog = InfoDialog(
                info_text=__("FlowTool finished successfully."),
                detailed_text=Case.instance().info.current_output)
        else:
            error_dialog(
                __("There was an error on the post-processing."),
                detailed_text=Case.instance().info.current_output
            )

    Case.instance().info.current_output = ""
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)

    # Build parameters
    static_params_exp = [
        '-dirin ' + Case.instance().path +
        '/' + Case.instance().name + '_out/',
        '-fileboxes ' + Case.instance().path + '/' + 'fileboxes.txt',
        '-savecsv ' + Case.instance().path + '/' + Case.instance().name +
        '_out/' + '{}.csv'.format(export_parameters['csv_name']),
        '-savevtk ' + Case.instance().path + '/' + Case.instance().name + '_out/' + '{}.vtk'.format(
            export_parameters['vtk_name']) +
        " " + export_parameters['additional_parameters']
    ]

    # Start process
    export_process.start(Case.instance().executable_paths.flowtool, static_params_exp)
    Case.instance().info.current_export_process = export_process

    # Information ready handler.
    def on_stdout_ready():
        # Update progress bar
        current_output = str(Case.instance().info.current_export_process.readAllStandardOutput())
        Case.instance().info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(export_parameters['vtk_name']))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.set_value(current_part)
        export_dialog.setWindowTitle(__("Exporting: ") + str(current_part) + "/" + str(Case.instance().info.exported_parts))

    Case.instance().info.current_export_process.readyReadStandardOutput.connect(on_stdout_ready)
