#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Post-Processing tools utilities. """
import os
import subprocess

from PySide2 import QtCore
from mod.tools.script_tools import generate_ext_script

from mod.tools.translation_tools import __
from mod.tools.dialog_tools import error_dialog, info_dialog, warning_dialog
from mod.tools.freecad_tools import get_fc_main_window
from mod.tools.file_tools import get_total_exported_parts_from_disk,  save_measuretool_point_list, \
    save_measuretool_point_grid
from mod.tools.executable_tools import ensure_process_is_executable_or_fail

from mod.widgets.dock.postprocessing.export_progress_dialog import ExportProgressDialog


def partvtk_export(options, case, post_processing_widget,generate_script) -> None:
    """ Export VTK button behaviour. Launches a process while disabling the button. """
    save_extension: str = {0: "vtk", 1: "csv", 2: "asc"}[options["save_mode"]]
    save_flag: str = {0: "-savevtk", 1: "-savecsv", 2: "-saveascii"}[options["save_mode"]]
    if generate_script:
        outfolder=case.get_out_folder_path(False)
    else:
        outfolder = case.get_out_folder_path()
        exported_parts: int = get_total_exported_parts_from_disk(case.get_out_data_folder_path())
        if not exported_parts:

            warning_dialog(f"Particle data file not found.({case.get_out_data_folder_path()}/Part_0000.bi4) You should make sure you have run your simulation first")
            return
        export_dialog = ExportProgressDialog(0, exported_parts, parent=None)
        export_dialog.show()

        case.info.current_output = ""


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
            subprocess.Popen([case.executable_paths.paraview, f"--data={case.get_out_folder_path()}part{os.sep}{options['file_name']}_..{save_extension}"], stdout=subprocess.PIPE)




    executable_parameters = ["-dirin {}".format(outfolder),
                             "{save_flag} {dirout}/part/{file_name}".format(save_flag=save_flag,
                                                                             dirout=outfolder,
                                                                             file_name=options["file_name"]),
                             "-onlytype:{save_types} {additional}".format(save_types=options["save_types"],
                                                                          additional=options[
                                                                              "additional_parameters"])]

    if generate_script:
        generate_ext_script("partvtk",executable_parameters,options["file_name"])
    else:

        export_dialog.on_cancel.connect(on_cancel)
        ensure_process_is_executable_or_fail(case.executable_paths.partvtk)
        export_process = QtCore.QProcess(get_fc_main_window())
        export_process.finished.connect(on_export_finished)
        export_process.readyReadStandardOutput.connect(on_stdout_ready)
        export_process.start(case.executable_paths.partvtk, executable_parameters)

def floatinginfo_export(options, case, post_processing_widget, generate_script) -> None:
    """ FloatingInfo tool export. """
    if generate_script:
        outfolder = f"{case.name}_out/"
        datafolder = outfolder + "data/"
    else:
        outfolder = case.get_out_folder_path()
        datafolder = case.get_out_data_folder_path()
        #post_processing_widget.adapt_to_export_start()

        if not os.path.exists(datafolder+os.sep+"Part_0000.bi4"):
            warning_dialog("Particle data file not found. You should make sure you have run your simulation first")
            return

        exported_parts: int = get_total_exported_parts_from_disk(case.get_out_data_folder_path())

        export_dialog = ExportProgressDialog(0, exported_parts, parent=None)
        export_dialog.show()

        case.info.current_output = ""

    # Build parameters
    executable_parameters = [f"-dirin {outfolder}",
                             f"-savedata {outfolder}floating/{options['filename']}"]

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

    if generate_script:
        generate_ext_script("floatinginfo",executable_parameters,options["filename"])
    else:
        export_dialog.on_cancel.connect(on_cancel)
        export_process = QtCore.QProcess(get_fc_main_window())
        export_process.finished.connect(on_export_finished)
        export_process.readyReadStandardOutput.connect(on_stdout_ready)
        ensure_process_is_executable_or_fail(case.executable_paths.floatinginfo)
        export_process.start(case.executable_paths.floatinginfo, executable_parameters)


def computeforces_export(options, case, post_processing_widget,generate_script) -> None:
    """ ComputeForces tool export. """

    if generate_script:
        outfolder=case.get_out_folder_path(False)
        datafolder = case.get_out_data_folder_path(False)
    else:
        outfolder = case.get_out_folder_path()
        datafolder = case.get_out_data_folder_path()
        if not os.path.exists(datafolder+os.sep+"Part_0000.bi4"):
            warning_dialog("Particle data file not found. You should make sure you have run your simulation first")
            return

    save_flag: str = {0: "-savevtk", 1: "-savecsv", 2: "-saveascii"}[options["save_mode"]]

    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_data_folder_path())


    executable_parameters = ["-dirin {}".format(outfolder),
                             "-filexml {out_path}forces/{case_name}.xml".format(out_path=outfolder, case_name=case.name),
                             "{save_flag} {out_path}forces/{file_name}".format(save_flag=save_flag, out_path=outfolder, file_name=options["filename"])]

    if options["onlyprocess"]:
        executable_parameters.append("{}{}".format(options["onlyprocess_tag"], options["onlyprocess"]))

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    if not generate_script:
        #post_processing_widget.adapt_to_export_start()
        export_dialog = ExportProgressDialog(0, exported_parts, parent=None)
        export_dialog.show()

        case.info.current_output = ""

    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part = int(current_output.split("Part_")[1].split(".bi4")[0])
        except(IndexError,ValueError):
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

    if generate_script:
        generate_ext_script("computeforces",executable_parameters,options["filename"])
    else:
        export_dialog.on_cancel.connect(on_cancel)
        export_process = QtCore.QProcess(get_fc_main_window())
        export_process.finished.connect(on_export_finished)
        export_process.readyReadStandardOutput.connect(on_stdout_ready)
        ensure_process_is_executable_or_fail(case.executable_paths.computeforces)
        export_process.start(case.executable_paths.computeforces, executable_parameters)


def measuretool_export(options, case, post_processing_widget,generate_script) -> None:
    """ MeasureTool tool export. """
    save_flag: str = {0: "-savevtk", 1: "-savecsv", 2: "-saveascii"}[options["save_mode"]]
    exported_parts: int = get_total_exported_parts_from_disk(case.get_out_data_folder_path())
    points_file = options["points_file"]
    if generate_script:
        outfolder=case.get_out_folder_path(False)
        datafolder = case.get_out_data_folder_path(False)
        casepath=""
    else:
        outfolder = case.get_out_folder_path()
        datafolder = case.get_out_data_folder_path()
        casepath=case.path+os.sep
        if not os.path.exists(datafolder+os.sep+"Part_0000.bi4"):
            warning_dialog("Particle data file not found. You should make sure you have run your simulation first")
            return
        export_dialog = ExportProgressDialog(0, exported_parts, parent=None)
        export_dialog.show()
        case.info.current_output = ""


    #Generate the corresponding txt file (Always or only when running in local?)
    if options["points_source"]==0: #Points list
        save_measuretool_point_list(case.path, points_file,case.post_processing_settings.measuretool_points)
    elif options["points_source"]==1: #Points grid
        save_measuretool_point_grid(case.path, points_file, case.post_processing_settings.measuretool_grid)



    executable_parameters = ["-dirin {out_path}".format(out_path=outfolder),
                             "-filexml {out_path}{case_name}.xml".format(out_path=outfolder, case_name=case.name),
                             "{save_flag} {out_path}measure/{file_name}".format(save_flag=save_flag, out_path=outfolder, file_name=options["filename"]),
                             "-points {case_path}{points_file}".format(case_path=casepath,points_file=points_file) if options["points_source"]<3
                                else "-pointsgeo {case_path}{mesh_file}".format(case_path=casepath,mesh_file=points_file),
                             "-vars:{save_vars}".format(save_vars=options["save_vars"]),
                             "-height" if options["calculate_water_elevation"] else "",
                             "-flow:{units}".format(units=options["water_flow_units"]) if options["calculate_water_flow"] else "",
                             "-trackmk:{mk}".format(mk=options["follow_mk_number"]) if options["follow_mk_enable"] else ""]

    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])

    def on_stdout_ready():
        """ Updates the export dialog on every stdout available from the process. """
        current_output = str(export_process.readAllStandardOutput().data(), encoding='utf-8')
        case.info.current_output += current_output
        try:
            current_part_str=  current_output.split("/Part_")[1].split(".bi4")[0]
            if current_part_str.startswith("Head"):
                current_part = export_dialog.get_value()
            else:
                current_part=int(current_part_str)
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

    if generate_script:
        generate_ext_script("measuretool",executable_parameters,options["filename"])
    else:
        export_dialog.on_cancel.connect(on_cancel)
        export_process = QtCore.QProcess(get_fc_main_window())
        export_process.finished.connect(on_export_finished)
        export_process.readyReadStandardOutput.connect(on_stdout_ready)
        ensure_process_is_executable_or_fail(case.executable_paths.measuretool)
        export_process.start(case.executable_paths.measuretool, executable_parameters)


def isosurface_export(options, case, post_processing_widget,generate_script) -> None:
    """ Export IsoSurface button behaviour. Launches a process while disabling the button. """
    if generate_script:
        outfolder=case.get_out_folder_path(False)
        datafolder = case.get_out_data_folder_path(False)
    else:
        outfolder = case.get_out_folder_path()
        datafolder = case.get_out_data_folder_path()
        if not os.path.exists(datafolder+os.sep+"Part_0000.bi4"):
            warning_dialog("Particle data file not found. You should make sure you have run your simulation first")
            return
        #post_processing_widget.adapt_to_export_start()

        exported_parts: int = get_total_exported_parts_from_disk(case.get_out_data_folder_path())
        export_dialog = ExportProgressDialog(0, exported_parts, parent=None)
        export_dialog.show()

        case.info.current_output = ""

    # Build parameters
    executable_parameters = ["-dirin {out_path}".format(out_path=outfolder),
                             "{surface_or_slice} {out_path}surface/{file_name}".format(surface_or_slice=options["surface_or_slice"], out_path=outfolder, file_name=options["file_name"])]

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

    if generate_script:
        generate_ext_script("isosurface", executable_parameters, options["file_name"])
    else:
        export_dialog.on_cancel.connect(on_cancel)
        export_process = QtCore.QProcess(get_fc_main_window())
        export_process.finished.connect(on_export_finished)
        export_process.readyReadStandardOutput.connect(on_stdout_ready)
        ensure_process_is_executable_or_fail(case.executable_paths.isosurface)
        export_process.start(case.executable_paths.isosurface, executable_parameters)


def flowtool_export(options, case, post_processing_widget,boxes_file:str,generate_script:bool,save_vtk:bool) -> None:
    """ Export FlowTool button behaviour. Launches a process while disabling the button. """
    if generate_script:
        outfolder=case.get_out_folder_path(False)
        datafolder = case.get_out_data_folder_path(False)
        casepath=""
    else:
        outfolder = case.get_out_folder_path()
        datafolder = case.get_out_data_folder_path()
        casepath=case.path+os.sep
        if not os.path.exists(datafolder+os.sep+"Part_0000.bi4"):
            warning_dialog("Particle data file not found. You should make sure you have run your simulation first")
            return

    executable_parameters = ["-dirin {}".format(outfolder),
                             "-fileboxes {case_path}{boxes_file}".format(case_path=casepath,
                                                                          boxes_file=boxes_file),
                             "-savecsv {out_path}flow/{file_name}.csv".format(out_path=outfolder,
                                                                              file_name=options["csv_name"])]
    if save_vtk:
        executable_parameters.append("-savevtk {out_path}flow/{file_name}.vtk".format(out_path=outfolder,
                                                                              file_name=options["vtk_name"]))


    if options["additional_parameters"]:
        executable_parameters.append(options["additional_parameters"])


    if generate_script:
        generate_ext_script("flowtool",executable_parameters,options["csv_name"])
        return
    else:
        exported_parts: int = get_total_exported_parts_from_disk(case.get_out_data_folder_path())
        export_dialog = ExportProgressDialog(0, exported_parts, parent=None)
        export_dialog.show()

        case.info.current_output = ""


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
