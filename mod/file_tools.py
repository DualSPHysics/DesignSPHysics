#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Utils.

This file contains a collection of constants and
functions meant to use with DesignSPHysics.

This module stores non-gui related operations, but
meant to use with FreeCAD.

"""

import pickle
import json
import shutil
import re

from sys import platform
from traceback import print_exc
from glob import glob
from os import path, chdir, makedirs

import FreeCAD
import FreeCADGui
import Mesh
import Fem
from femmesh.femmesh2mesh import femmesh_2_mesh

from mod.stdout_tools import error, debug
from mod.translation_tools import __
from mod.xml.xml_exporter import XMLExporter
from mod.dialog_tools import error_dialog, warning_dialog
from mod.executable_tools import refocus_cwd
from mod.freecad_tools import document_count, prompt_close_all_documents, get_fc_object
from mod.enums import ObjectType, ObjectFillMode

from mod.constants import VERSION, PICKLE_PROTOCOL

from mod.dataobjects.flow_tool_box import FlowToolBox
from mod.dataobjects.motion.special_movement import SpecialMovement
from mod.dataobjects.motion.file_gen import FileGen
from mod.dataobjects.motion.rotation_file_gen import RotationFileGen
from mod.dataobjects.ml_piston_1d import MLPiston1D
from mod.dataobjects.ml_piston_2d import MLPiston2D
from mod.dataobjects.relaxation_zone_file import RelaxationZoneFile
from mod.dataobjects.simulation_object import SimulationObject


def get_total_exported_parts_from_disk(out_folder_path) -> int:
    """ Gets the integer for the part with largest number on the out folder. """
    files_glob = glob("{}/Part_*.bi4".format(out_folder_path))
    files_glob.sort()
    return int(re.search("Part_(.*).bi4", files_glob[-1]).group(1))


def load_case(load_path: str) -> "Case":
    """ Loads a case from the given folder and returns its Case data. """
    refocus_cwd()
    project_folder_path = path.dirname(load_path)
    freecad_document_file_path = path.abspath("{}/DSPH_Case.FCStd".format(project_folder_path))

    if not path.isfile(freecad_document_file_path):
        error_dialog(__("DSPH_Case.FCStd file could not be found. Please check if the project was moved or the file was renamed."))
        return None

    if document_count() and not prompt_close_all_documents():
        return None

    FreeCAD.open(project_folder_path + "/DSPH_Case.FCStd")

    with open(load_path, "rb") as load_picklefile:
        try:
            loaded_data = pickle.load(load_picklefile)
            if not loaded_data.version:
                warning_dialog(__("The case data you're trying to load is older than version 0.6 and cannot be loaded."))
                prompt_close_all_documents(prompt=False)
                return None
            if loaded_data.version < VERSION:
                warning_dialog(__("The case data you are loading is from a previous version ({}) of this software. They may be missing features or errors.").format(loaded_data.version))
            elif loaded_data.version > VERSION:
                warning_dialog(__("You're loading a case data from a future version ({}) of this software. You should upgrade DesignSPHysics as they may be errors using this file.").format(loaded_data.version))

            return loaded_data
        except AttributeError:
            error_dialog(__("There was an error opening the case. Case Data file seems to be corrupted."))
            return None


def save_case(save_name: str, case: "Case") -> None:
    """ Saves a case to disk in the given path. """
    project_name = save_name.split("/")[-1]
    case.path = save_name
    case.name = project_name

    if not path.exists(save_name):
        makedirs(save_name)

    if not path.exists("{}/{}_out".format(save_name, project_name)):
        makedirs("{}/{}_out".format(save_name, project_name))

    # Export all complex objects to STL
    for obj in case.get_all_complex_objects():
        Mesh.export([get_fc_object(obj.name)], "{}/{}.stl".format(save_name, obj.name))

    # FIXME: Too many branches

    # Copy files from movements and change its paths to be inside the project.
    for _, mkproperties in case.mkbasedproperties.items():
        for movement in mkproperties.movements:
            if isinstance(movement, SpecialMovement):
                if isinstance(movement.generator, (FileGen, RotationFileGen)):
                    filename = movement.generator.filename
                    debug("Copying {} to {}".format(filename, save_name))

                    # Change directory to de case one, so if file path is already relative it copies it to the
                    # out folder
                    chdir(save_name)

                    try:
                        # Copy to project root
                        shutil.copy2(filename, save_name)
                    except shutil.Error:
                        # Probably already copied the file.
                        pass
                    except IOError:
                        error("Unable to copy {} into {}".format(filename, save_name))

                    try:
                        # Copy to project out folder
                        shutil.copy2(filename, save_name + "/" + project_name + "_out")

                        movement.generator.filename = "{}".format(filename.split("/")[-1])
                    except shutil.Error:
                        # Probably already copied the file.
                        pass
                    except IOError:
                        error("Unable to copy {} into {}".format(filename, save_name))

    # Copy files from Acceleration input and change paths to be inside the project folder.
    for aid in case.acceleration_input.acclist:
        filename = aid.datafile
        debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))

        # Change directory to de case one, so if file path is already relative it copies it to the
        # out folder
        chdir(save_name)

        try:
            # Copy to project root
            shutil.copy2(filename, save_name)
        except shutil.Error:
            # Probably already copied the file.
            pass
        except IOError:
            error("Unable to copy {} into {}".format(filename, save_name))

        try:
            # Copy to project out folder
            shutil.copy2(filename, save_name + "/" + project_name + "_out")

            aid.datafile = filename.split("/")[-1]

        except shutil.Error:
            # Probably already copied the file.
            pass
        except IOError:
            error("Unable to copy {} into {}".format(filename, save_name))

    # Copy files from pistons and change paths to be inside the project folder.
    for _, mkproperties in case.mkbasedproperties.items():
        if isinstance(mkproperties.mlayerpiston, MLPiston1D):
            filename = mkproperties.mlayerpiston.filevelx
            debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
            # Change directory to de case one, so if file path is already relative it copies it to the
            # out folder
            chdir(save_name)

            try:
                # Copy to project root
                shutil.copy2(filename, save_name)
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))

            try:
                # Copy to project out folder
                shutil.copy2(filename, save_name + "/" + project_name + "_out")

                mkproperties.mlayerpiston.filevelx = filename.split("/")[-1]
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))

        if isinstance(mkproperties.mlayerpiston, MLPiston2D):
            veldata = mkproperties.mlayerpiston.veldata
            for v in veldata:
                filename = v.filevelx
                debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
                # Change directory to de case one, so if file path is already relative it copies it to the
                # out folder
                chdir(save_name)

                try:
                    # Copy to project root
                    shutil.copy2(filename, save_name)
                except shutil.Error:
                    # Probably already copied the file.
                    pass
                except IOError:
                    error("Unable to copy {} into {}".format(filename, save_name))

                try:
                    # Copy to project out folder
                    shutil.copy2(filename, save_name + "/" + project_name + "_out")

                    v.filevelx = filename.split("/")[-1]
                except shutil.Error:
                    # Probably already copied the file.
                    pass
                except IOError:
                    error("Unable to copy {} into {}".format(filename, save_name))

    # Copies files needed for RelaxationZones into the project folder and changes data paths to relative ones.
    if isinstance(case.relaxation_zone, RelaxationZoneFile) and case.relaxation_zone.filesvel:
        # Need to copy the abc_x*_y*.csv file series to the out folder
        filename = case.relaxation_zone.filesvel

        # Change directory to de case one, so if file path is already relative it copies it to the
        # out folder
        chdir(save_name)

        for f in glob("{}*".format(filename)):
            debug("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
            try:
                # Copy to project root
                shutil.copy2(f, save_name)
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))

            try:
                # Copy to project out folder
                shutil.copy2(f, save_name + "/" + project_name + "_out")

                case.relaxation_zone.filesvel = filename.split("/")[-1]
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))

    # Dumps all the case data to an XML file.
    XMLExporter().save_to_disk(save_name, case)

    case.version = VERSION
    # Save data array on disk. It is saved as a binary file with Pickle.
    try:
        with open(save_name + "/casedata.dsphdata", "wb") as picklefile:
            pickle.dump(case, picklefile, PICKLE_PROTOCOL)
    except Exception:
        print_exc()
        error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))

    refocus_cwd()


def get_default_config_file():
    """ Gets the default-config.json from disk """
    current_script_folder = path.dirname(path.realpath(__file__))
    with open("{}/../default-config.json".format(current_script_folder)) as data_file:
        loaded_data = json.load(data_file)

    if "win" in platform:
        to_ret = loaded_data["windows"]
    elif "linux" in platform:
        to_ret = loaded_data["linux"]

    return to_ret


def get_saved_config_file() -> str:
    """ Returns the path of the configuration file saved in the FreeCAD user directory. """
    return "{datadir}/designsphysics-{version}.data".format(datadir=FreeCAD.getUserAppDataDir(), version=VERSION)


def get_designsphysics_path() -> str:
    """ Returns the module base path. """
    return "{}/../".format(path.dirname(path.abspath(__file__)))


def import_geo(filename=None, scale_x=1, scale_y=1, scale_z=1, name=None, autofill=False, case=None):
    """ Opens a GEO file, preprocesses it and saves it
    int temp files to load with FreeCAD. """
    if case is None:
        raise RuntimeError("Case parameter must be populated")

    file_type = ".{}".format(filename.split(".")[-1]).lower()

    if scale_x <= 0:
        scale_x = 1
    if scale_y <= 0:
        scale_y = 1
    if scale_z <= 0:
        scale_z = 1

    # TODO: Adapt to VTL (FEM lib, convert to other format)
    if file_type == ".vtk":
        loaded_mesh = Mesh.Mesh(femmesh_2_mesh(Fem.read(filename)))
    else:
        loaded_mesh = Mesh.read(filename)

    scale_matrix = FreeCAD.Matrix()
    scale_matrix.scale(scale_x, scale_y, scale_z)
    loaded_mesh.transform(scale_matrix)
    Mesh.show(loaded_mesh, name)
    FreeCADGui.SendMsgToActiveView("ViewFit")

    case.add_object(SimulationObject(name, case.get_first_mk_not_used(ObjectType.BOUND), ObjectType.BOUND, ObjectFillMode.SOLID))
    case.get_simulation_object(name).autofill = autofill


def create_flowtool_boxes(file_path: str, boxes: list):
    """ Creates a file with flowtool box information """
    with open(file_path, "w") as f:
        box: FlowToolBox = None
        for box in boxes:
            f.write("BOX @{}\n".format(box.name))
            f.write("{} {} {}\n".format(*box.point1))
            f.write("{} {} {}\n".format(*box.point2))
            f.write("{} {} {}\n".format(*box.point3))
            f.write("{} {} {}\n".format(*box.point4))
            f.write("{} {} {}\n".format(*box.point5))
            f.write("{} {} {}\n".format(*box.point6))
            f.write("{} {} {}\n".format(*box.point7))
            f.write("{} {} {}\n".format(*box.point8))
            f.write("\n")


def save_measuretool_info(case_path: str, points: list, grid: list) -> None:
    """ Creates a file with measuretool points/grid information.
        One of the parameters must be an empty list while the other must contain data. """
    if points:
        with open("{}/points.txt".format(case_path), "w") as f:
            f.write("POINTS\n")
            for curr_point in points:
                f.write("{}  {}  {}\n".format(*curr_point))
    elif grid:
        with open("{}/points.txt".format(case_path), "w") as f:
            for curr_point in grid:
                f.write("POINTSLIST\n")
                f.write("{}  {}  {}\n{}  {}  {}\n{}  {}  {}\n".format(*curr_point))
    else:
        raise RuntimeError("Attempting to save measuretool info with no points or grid setup.")
