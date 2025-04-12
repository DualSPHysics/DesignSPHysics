#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Post-Processing tools utilities. """

import subprocess

# from PySide import QtCore
from PySide6 import QtCore

from mod.translation_tools import __
from mod.dialog_tools import error_dialog, info_dialog
from mod.freecad_tools import get_fc_main_window
from mod.file_tools import get_total_exported_parts_from_disk, save_measuretool_info
from mod.executable_tools import ensure_process_is_executable_or_fail

from mod.widgets.postprocessing.export_progress_dialog import ExportProgressDialog


def partvtk_export(options, case, post_processing_widget) -> None:
    """ Export VTK button behaviour. Launches a process while disabling the button. """
    post_processing_widget.adapt_to_export_start()

    save_extension: str = {0: "vtk", 1: "csv", 2: "asc"}[options["save_mode"]]
    save_flag: str = {0: "-savevtk", 1: "-savecsv", 2: "-saveascii"}[options["save_mode"]]

    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_folder_path())

    export_dialog = ExportProgressDialog(0, exported_parts, parent=get_fc_main_window())
    export_dialog.show()

    case.info.current_output = ""

    # Build parameters
    executable_parameters = ["-dirin {}".format(case.get_out_folder_path()),
                             "{save_flag} {out_path}{file_name}".format(save_flag=save_flag, out_path=case.get_out_folder_path(), file_name=options["file_name"]),
                             "-onlytype:{save_types} {additional}".format(save_types=options["save_types"], additional=options["additional_parameters"])]

    # Information ready handler.
    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(options["file_name"]))[1]
            current_part = int(current_part.split(".{}".format(save_extension))[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.update_data(current_part)

    # Cancel button handler
    def on_cancel():
        """ Kills the process and cancels the export dialog. """
        export_process.kill()
        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    # PartVTK export finish handler
    def on_export_finished(exit_code):
        """ Closes and displays info/error about the process. """
        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        detailed_text = "The executed command line was: {} {}\n\n{}".format(case.executable_paths.partvtk, " ".join(executable_parameters), case.info.current_output)

        if not exit_code:
            info_dialog(info_text=__("PartVTK finished successfully"), detailed_text=detailed_text)
        else:
            error_dialog(__("There was an error on the post-processing. Show details to view the errors."), detailed_text=detailed_text)

        if options["open_paraview"]:
            subprocess.Popen([case.executable_paths.paraview, "--data={}\\{}_..{}".format(case.get_out_folder_path(), options["file_name"], save_extension)], stdout=subprocess.PIPE)

    export_dialog.on_cancel.connect(on_cancel)
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)
    export_process.readyReadStandardOutput.connect(on_stdout_ready)
    ensure_process_is_executable_or_fail(case.executable_paths.partvtk)
    export_process.start(case.executable_paths.partvtk, executable_parameters)


def floatinginfo_export(options, case, post_processing_widget) -> None:
    """ FloatingInfo tool export. """
    post_processing_widget.adapt_to_export_start()

    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_folder_path())

    export_dialog = ExportProgressDialog(0, exported_parts, parent=get_fc_main_window())
    export_dialog.show()

    case.info.current_output = ""

    # Build parameters
    executable_parameters = ["-dirin {}".format(case.get_out_folder_path()),
                             "-savedata {out_path}{file_name}".format(out_path=case.get_out_folder_path(), file_name=options["filename"])]


    if options["onlyprocess"]:
        executable_parameters.append("-onlymk:" + options["onlyprocess"])

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    def on_stdout_ready():
        """ Updates the export dialog on every stdout avasilable from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = int(current_output.split("Part_")[-1].split(".bi4")[0])
        except (IndexError, ValueError):
            current_part = export_dialog.get_value()
        export_dialog.update_data(current_part)

    def on_cancel():
        """ Kills the process and cancels the export dialog. """
        export_process.kill()
        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    def on_export_finished(exit_code):
        """ Closes and displays info/error about the process. """
        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        detailed_text = "The executed command line was: {} {}\n\n{}".format(case.executable_paths.floatinginfo, " ".join(executable_parameters), case.info.current_output)

        if not exit_code:
            info_dialog(info_text=__("FloatingInfo finished successfully"), detailed_text=detailed_text)
        else:
            error_dialog(__("There was an error on the post-processing. Show details to view the errors."), detailed_text=detailed_text)

    export_dialog.on_cancel.connect(on_cancel)
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)
    export_process.readyReadStandardOutput.connect(on_stdout_ready)
    ensure_process_is_executable_or_fail(case.executable_paths.floatinginfo)
    export_process.start(case.executable_paths.floatinginfo, executable_parameters)


def computeforces_export(options, case, post_processing_widget) -> None:
    """ ComputeForces tool export. """
    post_processing_widget.adapt_to_export_start()

    save_flag: str = {0: "-savevtk", 1: "-savecsv", 2: "-saveascii"}[options["save_mode"]]

    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_folder_path())

    export_dialog = ExportProgressDialog(0, exported_parts, parent=get_fc_main_window())
    export_dialog.show()

    case.info.current_output = ""

    executable_parameters = ["-dirin {}".format(case.get_out_folder_path()),
                             "-filexml {out_path}{case_name}.xml".format(out_path=case.get_out_folder_path(), case_name=case.name),
                             "{save_flag} {out_path}{file_name}".format(save_flag=save_flag, out_path=case.get_out_folder_path(), file_name=options["filename"])]

    if options["onlyprocess"]:
        executable_parameters.append("{}{}".format(options["onlyprocess_tag"], options["onlyprocess"]))

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = int(current_output.split("Part_")[1].split(".bi4")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.update_data(current_part)

    def on_cancel():
        """ Kills the process and cancels the export dialog. """
        export_process.kill()
        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    def on_export_finished(exit_code):
        """ Closes and displays info/error about the process. """
        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        detailed_text = "The executed command line was: {} {}\n\n{}".format(case.executable_paths.computeforces, " ".join(executable_parameters), case.info.current_output)

        if not exit_code:
            info_dialog(info_text=__("ComputeForces finished successfully"), detailed_text=detailed_text)
        else:
            error_dialog(__("There was an error on the post-processing. Show details to view the errors."), detailed_text=detailed_text)

    export_dialog.on_cancel.connect(on_cancel)
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)
    export_process.readyReadStandardOutput.connect(on_stdout_ready)
    ensure_process_is_executable_or_fail(case.executable_paths.computeforces)
    export_process.start(case.executable_paths.computeforces, executable_parameters)


def measuretool_export(options, case, post_processing_widget) -> None:
    """ MeasureTool tool export. """
    post_processing_widget.adapt_to_export_start()

    save_flag: str = {0: "-savevtk", 1: "-savecsv", 2: "-saveascii"}[options["save_mode"]]
    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_folder_path())

    export_dialog = ExportProgressDialog(0, exported_parts, parent=get_fc_main_window())
    export_dialog.show()

    case.info.current_output = ""

    save_measuretool_info(case.path, case.info.measuretool_points, case.info.measuretool_grid)

    executable_parameters = ["-dirin {out_path}".format(out_path=case.get_out_folder_path()),
                             "-filexml {out_path}{case_name}.xml".format(out_path=case.get_out_folder_path(), case_name=case.name),
                             "{save_flag} {out_path}{file_name}".format(save_flag=save_flag, out_path=case.get_out_folder_path(), file_name=options["filename"]),
                             "-points {case_path}/points.txt".format(case_path=case.path),
                             "-vars:{save_vars}".format(save_vars=options["save_vars"]),
                             "-height" if options["calculate_water_elevation"] else ""]

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = int(current_output.split("/Part_")[1].split(".bi4")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.update_data(current_part)

    def on_cancel():
        """ Kills the process and cancels the export dialog. """
        export_process.kill()
        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    def on_export_finished(exit_code):
        """ Closes and displays info/error about the process. """
        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        detailed_text = "The executed command line was: {} {}\n\n{}".format(case.executable_paths.measuretool, " ".join(executable_parameters), case.info.current_output)

        if not exit_code:
            info_dialog(info_text=__("MeasureTool finished successfully."), detailed_text=detailed_text)
        else:
            error_dialog(__("There was an error on the post-processing. Show details to view the errors."), detailed_text=detailed_text)

    export_dialog.on_cancel.connect(on_cancel)
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)
    export_process.readyReadStandardOutput.connect(on_stdout_ready)
    ensure_process_is_executable_or_fail(case.executable_paths.measuretool)
    export_process.start(case.executable_paths.measuretool, executable_parameters)


def isosurface_export(options, case, post_processing_widget) -> None:
    """ Export IsoSurface button behaviour. Launches a process while disabling the button. """
    post_processing_widget.adapt_to_export_start()

    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_folder_path())
    export_dialog = ExportProgressDialog(0, exported_parts, parent=get_fc_main_window())
    export_dialog.show()

    case.info.current_output = ""

    # Build parameters
    executable_parameters = ["-dirin {out_path}".format(out_path=case.get_out_folder_path()),
                             "{surface_or_slice} {out_path}{file_name}".format(surface_or_slice=options["surface_or_slice"], out_path=case.get_out_folder_path(), file_name=options["file_name"])]

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(options["file_name"]))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.update_data(current_part)

    def on_cancel():
        """ Kills the process and cancels the export dialog. """
        export_process.kill()
        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    def on_export_finished(exit_code):
        """ Closes and displays info/error about the process. """
        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        detailed_text = "The executed command line was: {} {}\n\n{}".format(case.executable_paths.isosurface, " ".join(executable_parameters), case.info.current_output)

        if not exit_code:
            info_dialog(info_text=__("IsoSurface finished successfully"), detailed_text=detailed_text)
        else:
            error_dialog(__("There was an error on the post-processing. Show details to view the errors."), detailed_text=detailed_text)

        if options["open_paraview"]:
            subprocess.Popen([case.executable_paths.paraview, "--data={}\\{}_..{}".format(case.path + "\\" + case.name + "_out", options["file_name"], "vtk")], stdout=subprocess.PIPE)

    export_dialog.on_cancel.connect(on_cancel)
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)
    export_process.readyReadStandardOutput.connect(on_stdout_ready)
    ensure_process_is_executable_or_fail(case.executable_paths.isosurface)
    export_process.start(case.executable_paths.isosurface, executable_parameters)


def flowtool_export(options, case, post_processing_widget) -> None:
    """ Export FlowTool button behaviour. Launches a process while disabling the button. """
    post_processing_widget.adapt_to_export_start()

    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_folder_path())
    export_dialog = ExportProgressDialog(0, exported_parts, parent=get_fc_main_window())
    export_dialog.show()

    case.info.current_output = ""

    executable_parameters = ["-dirin {}".format(case.get_out_folder_path()),
                             "-fileboxes {case_path}/fileboxes.txt".format(case_path=case.path),
                             "-savecsv {out_path}{file_name}.csv".format(out_path=case.get_out_folder_path(), file_name=options["csv_name"]),
                             "-savevtk {out_path}{file_name}.vtk".format(out_path=case.get_out_folder_path(), file_name=options["vtk_name"])]

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = current_output.split("{}_".format(options["vtk_name"]))[1]
            current_part = int(current_part.split(".vtk")[0])
        except IndexError:
            current_part = export_dialog.get_value()
        export_dialog.update_data(current_part)

    def on_cancel():
        """ Kills the process and cancels the export dialog. """
        export_process.kill()
        post_processing_widget.adapt_to_export_finished()
        export_dialog.reject()

    def on_export_finished(exit_code):
        """ Closes and displays info/error about the process. """
        post_processing_widget.adapt_to_export_finished()
        export_dialog.accept()
        detailed_text = "The executed command line was: {} {}\n\n{}".format(case.executable_paths.flowtool, " ".join(executable_parameters), case.info.current_output)

        if not exit_code:
            info_dialog(info_text=__("FlowTool finished successfully"), detailed_text=detailed_text)
        else:
            error_dialog(__("There was an error on the post-processing. Show details to view the errors."), detailed_text=detailed_text)

    export_dialog.on_cancel.connect(on_cancel)
    export_process = QtCore.QProcess(get_fc_main_window())
    export_process.finished.connect(on_export_finished)
    export_process.readyReadStandardOutput.connect(on_stdout_ready)
    ensure_process_is_executable_or_fail(case.executable_paths.flowtool)
    export_process.start(case.executable_paths.flowtool, executable_parameters)
