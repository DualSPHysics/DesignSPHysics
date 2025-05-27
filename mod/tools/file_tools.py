#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Utils.

This file contains a collection of constants and
functions meant to use with DesignSPHysics.

This module stores non-gui related operations, but
meant to use with FreeCAD.

"""
import os.path
import json
import shutil
import re
import pickle
import sys

from sys import platform
from traceback import print_exc
from glob import glob
from os import path, chdir, makedirs
from pickle import UnpicklingError  # Import the specific error

import FreeCAD
import FreeCADGui
import Mesh
import Fem
from femmesh.femmesh2mesh import femmesh_2_mesh


from mod.dataobjects.inletoutlet.inlet_outlet_elevation_info import InletOutletElevationInfo
from mod.dataobjects.inletoutlet.inlet_outlet_velocity_info import InletOutletVelocityInfo
from mod.dataobjects.motion.path_file_gen import PathFileGen
from mod.dataobjects.motion.rotate_adv_file_gen import RotateAdvFileGen
from mod.functions import get_designsphysics_path, get_mod_path
from mod.tools.freecad_tools import manage_inlet_outlet_zones,manage_vres_bufferboxes, manage_gauges, manage_partfilters
from mod.tools.stdout_tools import error, debug, log
from mod.tools.translation_tools import __
from mod.xml.xml_exporter import XMLExporter
from mod.tools.dialog_tools import error_dialog, warning_dialog, WaitDialog
from mod.tools.executable_tools import refocus_cwd
from mod.tools.freecad_tools import document_count, prompt_close_all_documents, get_fc_object
from mod.enums import ObjectType, ObjectFillMode, InletOutletVelocityType, InletOutletZSurfMode
from mod.tools.pickle_tool import CustomUnpickler

from mod.constants import VERSION, PICKLE_PROTOCOL

from mod.dataobjects.motion.special_movement import SpecialMovement
from mod.dataobjects.motion.file_gen import FileGen
from mod.dataobjects.motion.rotation_file_gen import RotationFileGen
from mod.dataobjects.properties.ml_piston.ml_piston_1d import MLPiston1D
from mod.dataobjects.properties.ml_piston.ml_piston_2d import MLPiston2D
from mod.dataobjects.relaxation_zone.relaxation_zone_file import RelaxationZoneFile
from mod.dataobjects.properties.simulation_object import SimulationObject
from mod.dataobjects.properties.material_property import MaterialProperty


def get_total_exported_parts_from_disk(out_folder_path) -> int:
    """ Gets the integer for the part with largest number on the out folder. """
    files_glob = glob("{}/Part_*.bi4".format(out_folder_path))
    files_glob.sort()
    if files_glob:
        return int(re.search("Part_(.*).bi4", files_glob[-1]).group(1))
    else:
        return 0


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
    log("Trying to open FreeCAD file")
    FreeCAD.open(project_folder_path + "/DSPH_Case.FCStd")
   
    log("Trying to load pickle file")
    with open(load_path, "rb") as load_picklefile:
        log("pickle file open")
        try:

            loaded_data = CustomUnpickler(load_picklefile).load()
            log("Data loaded from pickle file")
            if not loaded_data.version:
                warning_dialog(__("The case data you are trying to load is older than version 0.6 and cannot be loaded."))
                prompt_close_all_documents(prompt=False)
                return None
            if loaded_data.version < VERSION:
                warning_dialog(__("The case data you are loading comes from a previous version ({}) of this software. They may be missing features or errors. Please check your setup carefully.").format(loaded_data.version))
            elif loaded_data.version > VERSION:
                warning_dialog(__("You are loading a case data from a future version ({}) of this software. You should upgrade DesignSPHysics as they may be errors using this file.").format(loaded_data.version))
            return loaded_data
       
        except EOFError:
            error_dialog(__("The case file appears to be incomplete or corrupted (unexpected end of file)."))
            return None

        except AttributeError as e:
            error_dialog(__("Missing data structure or class attribute during loading.\n\nDetails: {}").format(str(e)))
            return None

        except ImportError as e:
            error_dialog(__("Unable to import a required module or object while loading the case.\n\nDetails: {}").format(str(e)))
            return None

        except UnpicklingError as e:
            error_dialog(__("The file format is invalid or not a valid pickle file.\n\nDetails: {}").format(str(e)))
            return None

        except ValueError as e:
            error_dialog(__("The data in the file is in an unexpected format.\n\nDetails: {}").format(str(e)))
            return None

        except Exception as e:
            error_dialog(__("An unexpected error occurred while loading the case file.\n\nDetails: {}").format(str(e)))
            return None


   
def save_case(save_name: str, case: "Case") -> None:
    """ Saves a case to disk in the given path. """
    manage_inlet_outlet_zones(case.inlet_outlet.zones)
    manage_vres_bufferboxes(case.vres.bufferbox_list)
    manage_gauges(case.gauges.gauges_dict)
    manage_partfilters(case.outparts.filts)
    wait_dialog=WaitDialog("Case is saving. Please wait.")
    wait_dialog.show()
    project_name = save_name.split("/")[-1]

    case.path = save_name
    case.name = project_name

    if not path.exists(save_name):
        makedirs(save_name)

    if not path.exists("{}/{}_out".format(save_name, project_name)):
        makedirs("{}/{}_out".format(save_name, project_name))

    # Export complex objects to STL, copy imported object files to the case
    log("Saving geometries")
    wait_dialog.update_info("Saving geometries")
    for obj in case.get_all_complex_objects():
        if obj.is_loaded_geometry:
            filename=obj.filename.split("/")[-1] #TEST WINDOWS
            dest_name=f"{save_name}/{filename}"
            if not os.path.isfile(dest_name):
                orig_name = obj.origin_filename
                chdir(save_name)
                try:
                    #if os.sep=='\\':
                    #    orig_name=orig_name.replace('/','\\')
                    shutil.copy2(orig_name, dest_name)
                    obj.filename=filename
                except shutil.Error:
                    error(f"shutil.Error: {shutil.Error.strerror}")
                except IOError:
                    error("Unable to copy {} into {}".format(orig_name, dest_name))
        else:
            filename = f"{save_name}/{obj.name}.stl"
            object=get_fc_object(obj.name)
            pos=object.Placement.Base
            rotation=object.Placement.Rotation
            object.Placement.Base=[0,0,0]
            object.Placement.Rotation.Angle=0
            object.Placement.Rotation.Axis=FreeCAD.Vector(0,0,0)
            Mesh.export([object],filename)
            object.Placement.Base=pos
            object.Placement.Rotation=rotation
            obj.filename= f"{obj.name}.stl"
        obj.full_filename=filename

    # FIXME: Too many branches
    log("Saving other files")
    wait_dialog.update_info("Saving other files")
    save_extra_files(case,save_name)

    # Dumps all the case data to an XML file.
    wait_dialog.update_info("Saving XML file")
    log("Saving XML file")
    XMLExporter().save_to_disk(save_name, case)
    wait_dialog.update_info("Saving FreeCAD data file")
    log("Saving FreeCAD data file")
    case.version = VERSION
    # Save data array on disk. It is saved as a binary file with Pickle.
    try:
        with open(save_name + "/casedata.dsphdata", "wb") as picklefile:
            pickle.dump(case, picklefile, PICKLE_PROTOCOL)
    except Exception:
        print_exc()
        error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))
    log("End saving")
    wait_dialog.close_dialog()
    refocus_cwd()

def save_extra_files(case: "Case",save_name:str):
    # Copy files from movements and change its paths to be inside the project.
    project_name = save_name.split("/")[-1]
    for _, mkproperties in case.mkbasedproperties.items():
        for movement in mkproperties.movements:
            if isinstance(movement, SpecialMovement):
                if isinstance(movement.generator, (FileGen, RotationFileGen,RotateAdvFileGen,PathFileGen)):
                    filename = movement.generator.filename
                    log("Copying movement generator {} to {}".format(filename, save_name))

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
                        error("Unable to copy {} into {}".format(filename, save_name + "/" + project_name + "_out"))

    # Copy files from Acceleration input and change paths to be inside the project folder.
    for aid in case.acceleration_input.acclist:
        filename = aid.datafile
        log("Copying acceleration_input file '{}' to {}".format(filename, save_name + "/" + project_name + "_out"))

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
            log("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
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
                log("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
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
            log("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
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
    for zone in case.inlet_outlet.zones:
        veloc: InletOutletVelocityInfo = zone.velocity_info
        if veloc.velocity_type == InletOutletVelocityType.INTERPOLATED:
            filename = veloc.velocity_mesh_data.filepath
            log("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
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

                veloc.velocity_mesh_data.filepath = os.path.basename(veloc.velocity_mesh_data.filepath)
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))
        zsurf: InletOutletElevationInfo = zone.elevation_info
        if zsurf.zsurf_mode == InletOutletZSurfMode.MESHDATA:
            filename = zsurf.meshdata.file
            log("Copying {} to {}".format(filename, save_name + "/" + project_name + "_out"))
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

                zsurf.meshdata.file = os.path.basename(zsurf.meshdata.file)
            except shutil.Error:
                # Probably already copied the file.
                pass
            except IOError:
                error("Unable to copy {} into {}".format(filename, save_name))


def get_default_config_file():
    """ Gets the default-config.json from disk """

    with open("{}/default-config.json".format(get_designsphysics_path()), encoding="utf-8") as data_file:
        loaded_data = json.load(data_file)

    if "win" in platform:
        to_ret = loaded_data["windows"]
    elif "linux" in platform:
        to_ret = loaded_data["linux"]

    return to_ret


def get_saved_config_file() -> str:
    """ Returns the path of the configuration file saved in the FreeCAD user directory. """
    config_file= "{datadir}/designsphysics-executables-{version}.data".format(datadir=FreeCAD.getUserAppDataDir(), version=VERSION)
    return config_file



def import_geo(filename=None, scale_x=1, scale_y=1, scale_z=1, name=None, autofill=False, case=None,adm =False,
               adm_reverse=False,has_adm_maxdepth=False,adm_maxdepth=3.0,has_adm_mindepth=False,adm_mindepth=0.1,
               desired_mkbound=-1,draw_as_points:bool=False,decimate:bool=False,reduction:float=0.9):
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

    scale_matrix = FreeCAD.Matrix()
    #scale_matrix.scale(scale_x * 1000, scale_y * 1000, scale_z * 1000)
    internal_name = "external_{}".format(name).replace("-", "_")

    if file_type == ".vtk" or file_type == ".vtu" or file_type == ".vtp":
        scale_matrix.scale(scale_x * 1000, scale_y * 1000, scale_z * 1000)
        loaded_fem_mesh = Fem.read(filename)
        loaded_mesh=femmesh_2_mesh(loaded_fem_mesh)
        loaded_mesh = Mesh.Mesh(loaded_mesh)
    else:
        scale_matrix.scale(scale_x *1000, scale_y*1000, scale_z*1000 ) #TODO test with FreeCAD saved geo
        loaded_mesh = Mesh.read(filename)

    loaded_mesh.transform(scale_matrix)
    Mesh.show(loaded_mesh, internal_name)


    SimObj=SimulationObject(internal_name, -1, ObjectType.BOUND, ObjectFillMode.SOLID)
    if not FreeCAD.ActiveDocument.getObject(SimObj.name):  #If there is no object with the same name in FreeCAD
        case.remove_tmp_object(SimObj.name)                 #Remove the tmpp object (why?))
        warning_dialog("Error loading object")
        return


    FreeCADGui.SendMsgToActiveView("ViewFit")
   
    # Add the geometry to the temporal object list. The mk must be defined when adding to the DSPH simulation (By default: mk=-1) 
    case.add_tmp_object(SimulationObject(internal_name, desired_mkbound, ObjectType.BOUND, ObjectFillMode.SOLID))
    tmp_object:SimulationObject=case.get_tmp_object(internal_name)
    tmp_object.autofill = autofill
    tmp_object.scale_factor=[scale_x,scale_y,scale_z]
    tmp_object.filename=filename
    tmp_object.advdraw_enabled=adm
    tmp_object.advdraw_reverse=adm_reverse
    tmp_object.advdraw_mindepth_enabled=has_adm_mindepth
    tmp_object.advdraw_maxdepth_enabled=has_adm_maxdepth
    tmp_object.advdraw_mindepth=adm_mindepth
    tmp_object.advdraw_maxdepth=adm_maxdepth
    tmp_object.file_type=file_type[1:4]
    tmp_object.is_loaded_geometry=True
    tmp_object.origin_filename=filename
    fc_object=get_fc_object(internal_name)
    if fc_object:
        fc_object.Label = name
        if draw_as_points :
                FreeCADGui.ActiveDocument.getObject(internal_name).DisplayMode = u"Points"
        if decimate :
                newmesh=fc_object.Mesh.copy()
                newmesh.decimate(0.2,reduction)
                fc_object.Mesh=newmesh
        FreeCAD.ActiveDocument.recompute() #TEST
    else:
        warning_dialog("There has been some error while loading object")



def save_measuretool_point_list(case_path: str, filename:str,points: list) -> None:
    """ Creates a file with measuretool points information. """
    if points:
        with open(f"{case_path}{os.sep}{filename}", "w", encoding="utf-8") as f:
            f.write("POINTS\n")
            for curr_point in points:
                f.write("{}  {}  {}\n".format(*curr_point))
    else:
        raise RuntimeError("Attempting to save measuretool info with no points setup.")

def save_measuretool_point_grid(case_path: str, filename:str,grid: list) -> None:
    if grid:
        with open(f"{case_path}{os.sep}{filename}", "w", encoding="utf-8") as f:
            for curr_point in grid:
                f.write("POINTSLIST\n")
                f.write("{}  {}  {}\n{}  {}  {}\n{}  {}  {}\n".format(*curr_point))
    else:
        raise RuntimeError("Attempting to save measuretool info with no grid setup.")

def load_default_materials() -> list:
    """ Loads and returns a list with the default materials on the project root. """
    with open("{}/default-materials.json".format(get_designsphysics_path()), encoding="utf-8") as default_config:
        default_materials = json.load(default_config)

    to_ret = list()
    for element in default_materials:
        material: MaterialProperty = MaterialProperty()
        material.name = str(element["name"])
        material.young_modulus = float(element["Young_Modulus"]["value"])
        material.poisson_ratio = float(element["PoissonRatio"]["value"])
        material.restitution_coefficient = float(element["Restitution_Coefficient"]["value"])
        material.kfric = float(element["Kfric"]["value"])
        to_ret.append(material)

    return to_ret
