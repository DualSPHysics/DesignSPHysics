#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Utils.

This file contains a collection of constants and
functions meant to use with DesignSPHysics.

This module stores non-gui related operations, but
meant to use with FreeCAD.

'''

import math
import pickle
import json
import shutil
import re

from sys import platform
from datetime import datetime
from traceback import print_exc
from glob import glob
from os import path, chdir, makedirs, remove

import FreeCAD
import FreeCADGui
import Mesh
import Fem
from femmesh.femmesh2mesh import femmesh_2_mesh

from mod.stdout_tools import log, warning, error, debug
from mod.translation_tools import __
from mod.xml import XMLExporter
from mod.dialog_tools import error_dialog
from mod.executable_tools import refocus_cwd
from mod.freecad_tools import document_count, prompt_close_all_documents

from mod.enums import FreeCADObjectType
from mod.constants import APP_NAME
from mod.constants import VERSION, PICKLE_PROTOCOL, DIVIDER


from mod.dataobjects.flow_tool_box import FlowToolBox
from mod.dataobjects.acceleration_input import AccelerationInput
from mod.dataobjects.movement import Movement
from mod.dataobjects.rect_motion import RectMotion
from mod.dataobjects.wait_motion import WaitMotion
from mod.dataobjects.acc_rect_motion import AccRectMotion
from mod.dataobjects.rot_motion import RotMotion
from mod.dataobjects.acc_rot_motion import AccRotMotion
from mod.dataobjects.acc_cir_motion import AccCirMotion
from mod.dataobjects.rot_sinu_motion import RotSinuMotion
from mod.dataobjects.cir_sinu_motion import CirSinuMotion
from mod.dataobjects.rect_sinu_motion import RectSinuMotion
from mod.dataobjects.special_movement import SpecialMovement
from mod.dataobjects.file_gen import FileGen
from mod.dataobjects.rotation_file_gen import RotationFileGen
from mod.dataobjects.regular_piston_wave_gen import RegularPistonWaveGen
from mod.dataobjects.irregular_piston_wave_gen import IrregularPistonWaveGen
from mod.dataobjects.regular_flap_wave_gen import RegularFlapWaveGen
from mod.dataobjects.irregular_flap_wave_gen import IrregularFlapWaveGen
from mod.dataobjects.ml_piston_1d import MLPiston1D
from mod.dataobjects.ml_piston_2d import MLPiston2D
from mod.dataobjects.relaxation_zone_regular import RelaxationZoneRegular
from mod.dataobjects.relaxation_zone_irregular import RelaxationZoneIrregular
from mod.dataobjects.relaxation_zone_uniform import RelaxationZoneUniform
from mod.dataobjects.relaxation_zone_file import RelaxationZoneFile


def get_total_exported_parts_from_disk(out_folder_path) -> int:
    ''' Gets the integer for the part with largest number on the out folder. '''
    return int(re.search("Part_(.*).bi4", glob("{}/Part_*.bi4".format(out_folder_path))).group(1))


def load_case(load_path: str) -> "Case":
    ''' Loads a case from the given folder and returns its Case data. '''
    refocus_cwd()
    project_folder_path = path.dirname(load_path)
    freecad_document_file_path = path.abspath("{}/DSPH_Case.FCStd".format(project_folder_path))

    if not path.isfile(freecad_document_file_path):
        error_dialog(__("DSPH_Case.FCStd file could not be found. Please check if the project was moved or the file was renamed."))
        return None

    if document_count() and not prompt_close_all_documents():
        return None

    FreeCAD.open(project_folder_path + "/DSPH_Case.FCStd")

    with open(load_path, 'rb') as load_picklefile:
        try:
            return pickle.load(load_picklefile)
        except AttributeError:
            error_dialog(__("There was an error opening the case. Case Data file seems to be corrupted."))
            return None


def save_case(save_name: str, case: "Case") -> None:
    ''' Saves a case to disk in the given path. '''
    project_name = save_name.split('/')[-1]
    case.path = save_name
    case.name = project_name

    if not path.exists(save_name):
        makedirs(save_name)

    if not path.exists("{}/{}_out".format(save_name, project_name)):
        makedirs("{}/{}_out".format(save_name, project_name))

    # Copy files from movements and change its paths to be inside the project.
    for _, mkproperties in case.mkbasedproperties.items():
        for movement in mkproperties.movements:
            if isinstance(movement, SpecialMovement):
                if isinstance(movement.generator, FileGen) or isinstance(movement.generator, RotationFileGen):
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
    if isinstance(case.relaxation_zone, RelaxationZoneFile):
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

    case.info.needs_to_run_gencase = False

    # Save data array on disk. It is saved as a binary file with Pickle.
    try:
        with open(save_name + "/casedata.dsphdata", 'wb') as picklefile:
            pickle.dump(case, picklefile, PICKLE_PROTOCOL)
    except Exception:
        print_exc()
        error_dialog(__("There was a problem saving the DSPH information file (casedata.dsphdata)."))

    refocus_cwd()


def get_default_config_file():
    ''' Gets the default-config.json from disk '''
    current_script_folder = path.dirname(path.realpath(__file__))
    with open('{}/../default-config.json'.format(current_script_folder)) as data_file:
        loaded_data = json.load(data_file)

    if "win" in platform:
        to_ret = loaded_data["windows"]
    elif "linux" in platform:
        to_ret = loaded_data["linux"]

    return to_ret


def get_saved_config_file() -> str:
    ''' Returns the path of the configuration file saved in the FreeCAD user directory. '''
    return "{datadir}/designsphysics-{version}.data".format(datadir=FreeCAD.getUserAppDataDir(), version=VERSION)


def get_designsphysics_path() -> str:
    ''' Returns the module base path. '''
    return "{}/../".format(path.dirname(path.abspath(__file__)))


def import_geo(filename=None, scale_x=1, scale_y=1, scale_z=1, name=None, autofill=False, case=None):
    ''' Opens a GEO file, preprocesses it and saves it
    int temp files to load with FreeCAD. '''
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

    case.get_simulation_object(name).autofill = autofill


def create_flowtool_boxes(file_path: str, boxes: list):
    ''' Creates a file with flowtool box information '''
    with open(file_path, 'w') as f:
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


# FIXME: Implement this in the new structure and delete this. This only remains here as documentation on how it works right now
def get_default_data():
    ''' A stub method to provide documentation for a refactor. '''

    data = dict()
    temp_data = dict()

    # CHRONO objects
    data['chrono_objects'] = list()
    data['link_spheric'] = list()
    data['link_linearspring'] = list()
    data['link_hinge'] = list()
    data['link_pointline'] = list()
    data['csv_intervals_check'] = False
    data['scale_scheme_check'] = False
    data['collisiondp_check'] = False
    data['csv_intervals'] = 0.0
    data['scale_scheme'] = 0.0
    data['collisiondp'] = 0.0
    data['modelnormal_check'] = 0
    data['modelnormal_print'] = "original"

    return data, temp_data


# FIXME: This should not exist. Saving it only as a documentation for the refactor
def dump_to_xml(data, save_name):
    ''' Saves all of the data in the opened case
        to disk. Generates a GenCase compatible XML. '''
    # Saves all the data in XML format.
    log("Saving data in " + data["project_path"] + ".")
    FreeCAD.ActiveDocument.saveAs(save_name + "/DSPH_Case.FCStd")
    FreeCADGui.SendMsgToActiveView("Save")
    f = open(save_name + "/" + save_name.split('/')[-1] + "_Def.xml", 'w', encoding='utf-8')
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    f.write('<!-- Case name: {} -->\n'.format(data["project_name"]))
    f.write('<case app="{} v{}" date="{}">\n'.format(APP_NAME, VERSION, datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
    f.write('\t<casedef>\n')
    f.write('\t\t<constantsdef>\n')
    f.write('\t\t\t<lattice bound="' + str(data['lattice_bound']) + '" fluid="' + str(data['lattice_fluid']) + '" />\n')
    f.write(
        '\t\t\t<gravity x="' + str(data['gravity'][0]) +
        '" y="' + str(data['gravity'][1]) +
        '" z="' + str(data['gravity'][2]) +
        '" comment="Gravitational acceleration" units_comment="m/s^2" />\n'
    )
    f.write('\t\t\t<rhop0 value="' + str(data['rhop0']) + '" comment="Reference density of the fluid" units_comment="kg/m^3" />\n')
    f.write(
        '\t\t\t<hswl value="' +
        str(data['hswl']) +
        '" auto="' +
        str(data['hswl_auto']).lower() +
        '" comment="Maximum still water level to calculate speedofsound using coefsound" units_comment="metres (m)"  />\n'
    )
    f.write('\t\t\t<gamma value="' + str(data['gamma']) + '" comment="Polytropic constant for water used in the state equation" />\n')
    f.write(
        '\t\t\t<speedsystem value="' +
        str(data['speedsystem']) +
        '" auto="' +
        str(data['speedsystem_auto']).lower() +
        '" comment="Maximum system speed (by default the dam-break propagation is used)" />\n'
    )
    f.write('\t\t\t<coefsound value="' + str(data['coefsound']) + '" comment="Coefficient to multiply speedsystem" />\n')
    f.write(
        '\t\t\t<speedsound value="' +
        str(data['speedsound']) +
        '" auto="' +
        str(data['speedsound_auto']).lower() +
        '" comment="Speed of sound to use in the simulation (by default speedofsound=coefsound*speedsystem)" />\n'
    )
    f.write(
        '\t\t\t<coefh value="' + str(data['coefh']) +
        '" comment="Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D)" />\n')
    f.write('\t\t\t<cflnumber value="' + str(data['cflnumber']) + '" comment="Coefficient to multiply dt" />\n')
    f.write('\t\t\t<h value="' + str(data['h']) + '" auto="' + str(data['h_auto']).lower() + '" units_comment="metres (m)" />\n')
    f.write('\t\t\t<b value="' + str(data['b']) + '" auto="' + str(data['b_auto']).lower() + '" units_comment="metres (m)" />\n')
    f.write('\t\t\t<massbound value="' + str(data['massbound']) + '" auto="' + str(data['massbound_auto']).lower() + '" units_comment="kg" />\n')
    f.write('\t\t\t<massfluid value="' + str(data['massfluid']) + '" auto="' + str(data['massfluid_auto']).lower() + '" units_comment="kg" />\n')
    f.write('\t\t</constantsdef>\n')
    f.write('\t\t<mkconfig boundcount="240" fluidcount="10">\n')
    f.write('\t\t</mkconfig>\n')
    f.write('\t\t<geometry>\n')
    f.write('\t\t\t<definition dp="' + str(data['dp']) + '" comment="Initial inter-particle distance" units_comment="metres (m)">\n')
    min_point = FreeCAD.ActiveDocument.getObject("Case_Limits").Placement.Base
    max_point = FreeCAD.ActiveDocument.getObject("Case_Limits")
    f.write('\t\t\t\t<pointmin x="' + str((min_point.x / DIVIDER)) + '" y="' + str((min_point.y / DIVIDER)) + '" z="' + str((min_point.z / DIVIDER)) + '" />\n')
    if data['3dmode']:
        f.write(
            '\t\t\t\t<pointmax x="' +
            str((min_point.x / DIVIDER + max_point.Length.Value / DIVIDER)) + '" y="' +
            str((min_point.y / DIVIDER + max_point.Width.Value / DIVIDER)) + '" z="' +
            str((min_point.z / DIVIDER + max_point.Height.Value / DIVIDER)) + '" />\n'
        )
    else:
        f.write(
            '\t\t\t\t<pointmax x="' +
            str((min_point.x / DIVIDER + max_point.Length.Value / DIVIDER)) + '" y="' +
            str((min_point.y / DIVIDER)) + '" z="' +
            str((min_point.z / DIVIDER + max_point.Height.Value / DIVIDER)) + '" />\n'
        )
    f.write('\t\t\t</definition>\n')
    f.write('\t\t\t<commands>\n')
    f.write('\t\t\t\t<mainlist>\n')
    f.write('\t\t\t\t\t<setshapemode>dp | bound</setshapemode>\n')
    # Export in strict order
    for key in data["export_order"]:
        name = key
        valuelist = data["simobjects"][name]
        o = FreeCAD.ActiveDocument.getObject(name)
        # Ignores case limits
        if name != "Case_Limits":
            # Sets MKfluid or bound depending on object properties and resets
            # the matrix
            if valuelist[1].lower() == "fluid":
                f.write('\t\t\t\t\t<setmkfluid mk="' + str(valuelist[0]) + '"/>\n')
            elif valuelist[1].lower() == "bound":
                f.write('\t\t\t\t\t<setmkbound mk="' + str(valuelist[0]) + '"/>\n')
            f.write('\t\t\t\t\t<setdrawmode mode="' + valuelist[2].lower() + '"/>\n')
            # Exports supported objects in a xml parametric mode.
            # If special objects are found, exported in an specific manner (p.e FillBox)
            # The rest of the things are exported in STL format.
            if o.TypeId == FreeCADObjectType.BOX:
                if math.degrees(o.Placement.Rotation.Angle) != 0:
                    if (abs(o.Placement.Base.x) + abs(o.Placement.Base.y) + abs(o.Placement.Base.z)) != 0:
                        f.write(
                            '\t\t\t\t\t<move x="' +
                            str(o.Placement.Base.x / DIVIDER) + '" y="' +
                            str(o.Placement.Base.y / DIVIDER) + '" z="' +
                            str(o.Placement.Base.z / DIVIDER) + '" />\n'
                        )
                    f.write(
                        '\t\t\t\t\t<rotate ang="' +
                        str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' +
                        str(-o.Placement.Rotation.Axis.x) + '" y="' +
                        str(-o.Placement.Rotation.Axis.y) + '" z="' +
                        str(-o.Placement.Rotation.Axis.z) + '" />\n'
                    )

                f.write('\t\t\t\t\t<drawbox objname="{}">\n'.format(o.Label))
                if (str(valuelist[0]), o.Label) in data['faces'].keys():
                    f.write('\t\t\t\t\t\t<boxfill>{}</boxfill>\n'.format(str(data['faces'][str(valuelist[0]), o.Label]
                                                                             .face_print)))
                else:
                    f.write('\t\t\t\t\t\t<boxfill>solid</boxfill>\n')

                if math.degrees(o.Placement.Rotation.Angle) == 0:
                    f.write('\t\t\t\t\t\t<point x="' +
                            str(o.Placement.Base.x / DIVIDER) + '" y="' +
                            str(o.Placement.Base.y / DIVIDER) + '" z="' +
                            str(o.Placement.Base.z / DIVIDER) + '" />\n')
                else:
                    f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')

                f.write(
                    '\t\t\t\t\t\t<size x="' +
                    str(o.Length.Value / DIVIDER) + '" y="' +
                    str(o.Width.Value / DIVIDER) + '" z="' +
                    str(o.Height.Value / DIVIDER) + '" />\n'
                )
                f.write('\t\t\t\t\t</drawbox>\n')
                if math.degrees(o.Placement.Rotation.Angle) != 0:
                    f.write('\t\t\t\t\t<matrixreset />\n')
            elif o.TypeId == FreeCADObjectType.SPHERE:
                if (abs(o.Placement.Base.x) + abs(o.Placement.Base.y) + abs(o.Placement.Base.z)) != 0:
                    f.write(
                        '\t\t\t\t\t<move x="' +
                        str(o.Placement.Base.x / DIVIDER) + '" y="' +
                        str(o.Placement.Base.y / DIVIDER) + '" z="' +
                        str(o.Placement.Base.z / DIVIDER) + '" />\n'
                    )
                if math.degrees(o.Placement.Rotation.Angle) != 0:
                    f.write(
                        '\t\t\t\t\t<rotate ang="' +
                        str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' +
                        str(-o.Placement.Rotation.Axis.x) + '" y="' +
                        str(-o.Placement.Rotation.Axis.y) + '" z="' +
                        str(-o.Placement.Rotation.Axis.z) + '" />\n'
                    )
                f.write('\t\t\t\t\t<drawsphere radius="' + str(o.Radius.Value / DIVIDER) + '"  objname="{}">\n'.format(o.Label))
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t</drawsphere>\n')
            elif o.TypeId == FreeCADObjectType.CYLINDER:
                if (abs(o.Placement.Base.x) + abs(o.Placement.Base.y) + abs(o.Placement.Base.z)) != 0:
                    f.write(
                        '\t\t\t\t\t<move x="' +
                        str(o.Placement.Base.x / DIVIDER) + '" y="' +
                        str(o.Placement.Base.y / DIVIDER) + '" z="' +
                        str(o.Placement.Base.z / DIVIDER) + '" />\n'
                    )
                if math.degrees(o.Placement.Rotation.Angle) != 0:
                    f.write(
                        '\t\t\t\t\t<rotate ang="' +
                        str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' +
                        str(-o.Placement.Rotation.Axis.x) + '" y="' +
                        str(-o.Placement.Rotation.Axis.y) + '" z="' +
                        str(-o.Placement.Rotation.Axis.z) + '" />\n'
                    )
                f.write('\t\t\t\t\t<drawcylinder radius="' + str(o.Radius.Value / DIVIDER) + '" objname="{}">\n'.format(o.Label))
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="' + str((0 + o.Height.Value) / DIVIDER) + '" />\n')
                f.write('\t\t\t\t\t</drawcylinder>\n')
            else:
                # Watch if it is a fillbox group
                if o.TypeId == FreeCADObjectType.FOLDER and "fillbox" in o.Name.lower():
                    filllimits = None
                    fillpoint = None
                    for element in o.OutList:
                        if "filllimit" in element.Name.lower():
                            filllimits = element
                        elif "fillpoint" in element.Name.lower():
                            fillpoint = element
                    if filllimits and fillpoint:
                        if (abs(filllimits.Placement.Base.x) + abs(filllimits.Placement.Base.y) + abs(filllimits.Placement.Base.z)) != 0:
                            f.write(
                                '\t\t\t\t\t<move x="' +
                                str(filllimits.Placement.Base.x / DIVIDER) + '" y="' +
                                str(filllimits.Placement.Base.y / DIVIDER) + '" z="' +
                                str(filllimits.Placement.Base.z / DIVIDER) + '" />\n'
                            )
                        if math.degrees(filllimits.Placement.Rotation.Angle) != 0:
                            f.write(
                                '\t\t\t\t\t<rotate ang="' +
                                str(math.degrees(filllimits.Placement.Rotation.Angle)) + '" x="' +
                                str(-filllimits.Placement.Rotation.Axis.x) + '" y="' +
                                str(-filllimits.Placement.Rotation.Axis.y) + '" z="' +
                                str(-filllimits.Placement.Rotation.Axis.z) + '" />\n'
                            )
                        f.write(
                            '\t\t\t\t\t<fillbox x="' +
                            str((fillpoint.Placement.Base.x - filllimits.Placement.Base.x) / DIVIDER) + '" y="' +
                            str((fillpoint.Placement.Base.y - filllimits.Placement.Base.y) / DIVIDER) + '" z="' +
                            str((fillpoint.Placement.Base.z - filllimits.Placement.Base.z) / DIVIDER) + '" objname="{}">\n'.format(o.Label)
                        )
                        f.write('\t\t\t\t\t\t<modefill>void</modefill>\n')
                        f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                        f.write(
                            '\t\t\t\t\t\t<size x="' +
                            str(filllimits.Length.Value / DIVIDER) + '" y="' +
                            str(filllimits.Width.Value / DIVIDER) + '" z="' +
                            str(filllimits.Height.Value / DIVIDER) + '" />\n'
                        )
                        f.write('\t\t\t\t\t</fillbox>\n')
                    else:
                        # Something went wrong, one of the needed objects is not
                        # in the fillbox group
                        error("Limits or point missing in a fillbox group. Ignoring it")
                        continue
                else:
                    # Not a xml parametric object.  Needs exporting
                    __objs__ = list()
                    __objs__.append(o)
                    # TODO: Convert to STL or maintain original format?
                    stl_file_path = save_name + "/" + o.Name + ".stl"
                    Mesh.export(__objs__, stl_file_path)
                    relative_file_path = path.relpath(
                        stl_file_path,
                        path.dirname(path.abspath(stl_file_path))
                    )
                    autofill_enabled = str(data["geo_autofill"][o.Name] if o.Name in data["geo_autofill"].keys() else False).lower()
                    f.write('\t\t\t\t\t<drawfilestl file="{}" objname="{}" autofill="{}">\n'.format(relative_file_path, o.Label, autofill_enabled))
                    f.write('\t\t\t\t\t\t<drawscale x="0.001" y="0.001" z="0.001" />\n')
                    f.write('\t\t\t\t\t</drawfilestl>\n')
                    del __objs__
    f.write('\t\t\t\t\t<shapeout file="" />\n')
    f.write('\t\t\t\t</mainlist>\n')
    f.write('\t\t\t</commands>\n')
    f.write('\t\t</geometry>\n')
    # Writes initials
    if len(data["initials_mks"].keys()) > 0:
        f.write('\t\t<initials>\n')
        for key, value in data["initials_mks"].items():
            f.write(
                '\t\t\t<velocity mkfluid="' +
                str(key) + '" x="' +
                str(value.force[0]) + '" y="' +
                str(value.force[1]) + '" z="' +
                str(value.force[2]) + '"/>\n'
            )
        f.write('\t\t</initials>\n')
    # Writes floatings
    if len(data["floating_mks"].keys()) > 0:
        f.write('\t\t<floatings>\n')
        for key, value in data["floating_mks"].items():
            if value.mass_density_type == 0:
                # is massbody
                f.write('\t\t\t<floating mkbound="' + str(key) + '">\n')
                f.write('\t\t\t\t<massbody value="' + str(value.mass_density_value) + '" />\n')
            else:
                # is rhopbody
                f.write('\t\t\t<floating mkbound="' + str(key) + '" rhopbody="' + str(value.mass_density_value) + '">\n')
            if len(value.gravity_center) != 0:
                f.write(
                    '\t\t\t\t<center x="' +
                    str(value.gravity_center[0]) + '" y="' +
                    str(value.gravity_center[1]) + '" z="' +
                    str(value.gravity_center[2]) + '" />\n'
                )
            if len(value.inertia) != 0:
                f.write(
                    '\t\t\t\t<inertia x="' +
                    str(value.inertia[0]) + '" y="' +
                    str(value.inertia[1]) + '" z="' +
                    str(value.inertia[2]) + '" />\n'
                )
            if len(value.initial_linear_velocity) != 0:
                f.write(
                    '\t\t\t\t<linearvelini x="' +
                    str(value.initial_linear_velocity[0]) + '" y="' +
                    str(value.initial_linear_velocity[1]) + '" z="' +
                    str(value.initial_linear_velocity[2]) + '" units_comment="m/s" />\n'
                )
            if len(value.initial_angular_velocity) != 0:
                f.write(
                    '\t\t\t\t<angularvelini x="' +
                    str(value.initial_angular_velocity[0]) + '" y="' +
                    str(value.initial_angular_velocity[1]) + '" z="' +
                    str(value.initial_angular_velocity[2]) + '" units_comment="rad/s" />\n'
                )
            if len(value.translation_restriction) != 0:
                f.write(
                    '\t\t\t\t<translation x="' +
                    str(value.translation_restriction[0]) + '" y="' +
                    str(value.translation_restriction[1]) + '" z="' +
                    str(value.translation_restriction[2]) + '" comment="Use 0 for translation restriction in the movement '
                    '(default=(1,1,1))" />\n'
                )
            if len(value.rotation_restriction) != 0:
                f.write(
                    '\t\t\t\t<rotation x="' +
                    str(value.rotation_restriction[0]) + '" y="' +
                    str(value.rotation_restriction[1]) + '" z="' +
                    str(value.rotation_restriction[2]) + '" comment="Use 0 for rotation restriction in the movement'
                                                         ' (default=(1,1,1))" />\n'
                )
            if value.material != "":
                f.write(
                    '\t\t\t\t<material name="' + str(value.material) + '"/>\n'
                )
            f.write('\t\t\t</floating>\n')
        f.write('\t\t</floatings>\n')

    # Writes motions
    if len(data["motion_mks"]) > 0 or len(data['mlayerpistons'].keys()) > 0:
        f.write('\t\t<motion>\n')
        mov_counter = 1
        for key, value in data['mlayerpistons'].items():
            f.write('\t\t\t<objreal ref="' + str(key) + '">\n')
            f.write('\t\t\t\t<begin mov="{}" start="0"/>\n'.format(mov_counter))
            f.write('\t\t\t\t<mvnull id="{}" />\n'.format(mov_counter))
            f.write('\t\t\t</objreal>\n')
            mov_counter += 1

        for key, value in data["motion_mks"].items():
            f.write('\t\t\t<objreal ref="' + str(key) + '">\n')
            mot_counter = 1
            for movement in value:
                if movement not in data["global_movements"]:
                    continue
                f.write('\t\t\t\t<!-- Movement Name: {} -->\n'.format(movement.name))
                f.write('\t\t\t\t<begin mov="{}" start="0"/>\n'.format(mot_counter))
                first_series_motion = mot_counter
                if isinstance(movement, Movement):
                    for motion_index, motion in enumerate(movement.motion_list):
                        if isinstance(motion, RectMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrect id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrect id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrect id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<vel x="{}" y="{}" z="{}"/>\n'.format(
                                motion.velocity[0], motion.velocity[1], motion.velocity[2]))
                            f.write('\t\t\t\t</mvrect>\n')
                        elif isinstance(motion, WaitMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                if movement.loop:
                                    f.write('\t\t\t\t<wait id="{}" duration="{}" next="{}"/>\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write(
                                        '\t\t\t\t<wait id="{}" duration="{}"/>\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<wait id="{}" duration="{}" next="{}"/>\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))
                        elif isinstance(motion, AccRectMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrectace id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrectace id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrectace id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<vel x="{}" y="{}" z="{}"/>\n'.format(
                                motion.velocity[0], motion.velocity[1], motion.velocity[2]))
                            f.write('\t\t\t\t\t<ace x="{}" y="{}" z="{}"/>\n'.format(
                                motion.acceleration[0], motion.acceleration[1], motion.acceleration[2]))
                            f.write('\t\t\t\t</mvrectace>\n')
                        elif isinstance(motion, RotMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrot id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrot id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrot id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write(
                                '\t\t\t\t\t<vel ang="{}"/>\n'.format(motion.ang_vel))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvrot>\n')
                        elif isinstance(motion, AccRotMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrotace id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrotace id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrotace id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<ace ang="{}"/>\n'.format(motion.ang_acc))
                            f.write('\t\t\t\t\t<velini ang="{}"/>\n'.format(motion.ang_vel))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvrotace>\n')
                        elif isinstance(motion, AccCirMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvcirace id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvcirace id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvcirace id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<ace ang="{}"/>\n'.format(motion.ang_acc))
                            f.write('\t\t\t\t\t<velini ang="{}"/>\n'.format(motion.ang_vel))
                            f.write('\t\t\t\t\t<ref x="{}" y="{}" z="{}"/>\n'.format(
                                motion.reference[0], motion.reference[1], motion.reference[2]))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvcirace>\n')
                        elif isinstance(motion, RotSinuMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write(
                                        '\t\t\t\t<mvrotsinu id="{}" duration="{}" anglesunits="radians" next="{}" >\n'.format(
                                            mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrotsinu id="{}" duration="{}" anglesunits="radians">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write(
                                    '\t\t\t\t<mvrotsinu id="{}" duration="{}" anglesunits="radians" next="{}">\n'.format(
                                        mot_counter, motion.duration, mot_counter + 1))

                            f.write(
                                '\t\t\t\t\t<freq v="{}"/>\n'.format(motion.freq))
                            f.write(
                                '\t\t\t\t\t<ampl v="{}"/>\n'.format(motion.ampl))
                            f.write(
                                '\t\t\t\t\t<phase v="{}"/>\n'.format(motion.phase))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvrotsinu>\n')
                        elif isinstance(motion, CirSinuMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvcirsinu id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvcirsinu id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvcirsinu id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write(
                                '\t\t\t\t\t<freq v="{}"/>\n'.format(motion.freq))
                            f.write(
                                '\t\t\t\t\t<ampl v="{}"/>\n'.format(motion.ampl))
                            f.write(
                                '\t\t\t\t\t<phase v="{}"/>\n'.format(motion.phase))
                            f.write('\t\t\t\t\t<ref x="{}" y="{}" z="{}"/>\n'.format(
                                motion.reference[0], motion.reference[1], motion.reference[2]))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(
                                motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvcirsinu>\n')
                        elif isinstance(motion, RectSinuMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrectsinu id="{}" duration="{}" next="{}">\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrectsinu id="{}" duration="{}">\n'.format(
                                        mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrectsinu id="{}" duration="{}" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<freq x="{}" y="{}" z="{}"/>\n'.format(
                                motion.freq[0], motion.freq[1], motion.freq[2]))
                            f.write('\t\t\t\t\t<ampl x="{}" y="{}" z="{}"/>\n'.format(
                                motion.ampl[0], motion.ampl[1], motion.ampl[2]))
                            f.write('\t\t\t\t\t<phase x="{}" y="{}" z="{}"/>\n'.format(
                                motion.phase[0], motion.phase[1], motion.phase[2]))
                            f.write('\t\t\t\t</mvrectsinu>\n')

                        mot_counter += 1
                elif isinstance(movement, SpecialMovement):
                    if isinstance(movement.generator, FileGen):
                        f.write('\t\t\t\t<mvfile id="{}" duration="{}">\n '.format(
                            mov_counter, movement.generator.duration))
                        f.write('\t\t\t\t\t<file name="{}" fields="{}" fieldtime="{}" '
                                'fieldx="{}" fieldy="{}" />\n '.format(movement.generator.filename,
                                                                       movement.generator.fields,
                                                                       movement.generator.fieldtime,
                                                                       movement.generator.fieldx,
                                                                       movement.generator.fieldy))
                        f.write('\t\t\t\t</mvfile>\n ')
                    elif isinstance(movement.generator, RotationFileGen):
                        f.write('\t\t\t\t<mvrotfile id="{}" duration="{}" anglesunits="{}">\n '.format(mov_counter,
                                                                                                       movement.generator.duration,
                                                                                                       movement.generator.anglesunits))
                        f.write(
                            '\t\t\t\t\t<file name="{}" />\n '.format(movement.generator.filename))
                        f.write(
                            '\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}" />\n '.format(*movement.generator.axisp1))
                        f.write(
                            '\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}" />\n '.format(*movement.generator.axisp2))
                        f.write('\t\t\t\t</mvrotfile>\n ')
                    else:
                        f.write(
                            '\t\t\t\t<mvnull id="{}" />\n'.format(mov_counter))

                mov_counter += 1
            f.write('\t\t\t</objreal>\n')
        f.write('\t\t</motion>\n')
    f.write('\t</casedef>\n')
    f.write('\t<execution>\n')

    f.write('\t\t<special>\n')

    # Acceleration Input
    if data['accinput'].enabled:
        f.write('\t\t\t<accinputs>\n')
        for aid in data['accinput'].acclist:
            f.write('\t\t\t\t<!-- Input label: {} -->\n'.format(aid.label))
            f.write('\t\t\t\t<accinput>\n')
            f.write('\t\t\t\t\t<mkfluid value="{}" comment="Mk-Fluid of selected particles" />\n'.format(aid.mkfluid))
            f.write(
                '\t\t\t\t\t<acccentre x="{}" y="{}" z="{}" comment="Center of acceleration" />\n'.format(*aid.acccentre))
            f.write(
                '\t\t\t\t\t<globalgravity value="{}" comment="Global gravity enabled (1) or disabled (0)" />\n'.format(
                    "1" if aid.globalgravity else "0"
                )
            )
            f.write('\t\t\t\t\t<datafile value="{}" comment="File with acceleration data" />\n'.format(aid.datafile))
            f.write('\t\t\t\t</accinput>\n')
        f.write('\t\t\t</accinputs>\n')

    # Damping support
    if len(data['damping']) > 0:
        f.write('\t\t\t<damping>\n')
        for objname, damping_object in data["damping"].items():
            fc_obj = FreeCAD.ActiveDocument.getObject(objname)
            if fc_obj is not None and damping_object.enabled:
                f.write('\t\t\t\t<dampingzone>\n')
                f.write(
                    '\t\t\t\t\t<limitmin x="{}" y="{}" z="{}" />\n'.format(
                        str(fc_obj.OutList[0].Start[0] / DIVIDER),
                        str(fc_obj.OutList[0].Start[1] / DIVIDER),
                        str(fc_obj.OutList[0].Start[2] / DIVIDER)
                    ))
                f.write(
                    '\t\t\t\t\t<limitmax x="{}" y="{}" z="{}" />\n'.format(
                        str(fc_obj.OutList[0].End[0] / DIVIDER),
                        str(fc_obj.OutList[0].End[1] / DIVIDER),
                        str(fc_obj.OutList[0].End[2] / DIVIDER)
                    ))
                f.write(
                    '\t\t\t\t\t<overlimit value="{}" />\n'.format(damping_object.overlimit))
                f.write(
                    '\t\t\t\t\t<redumax value="{}" />\n'.format(damping_object.redumax))
                f.write('\t\t\t\t</dampingzone>\n')
        f.write('\t\t\t</damping>\n')

    # Chrono objects
    if len(data['chrono_objects']) > 0 or data['csv_intervals_check'] or data['scale_scheme_check'] \
            or data['collisiondp_check']:
        f.write('\t\t\t<chrono>\n')
        if data['csv_intervals_check'] and data['csv_intervals'] != "":
            f.write(
                '\t\t\t\t<savedata value="{}" comment="Saves CSV with data exchange for each time interval '
                '(0=all steps)" />\n'.format(data['csv_intervals'])
            )
        if data['scale_scheme_check'] and data['scale_scheme'] != "":
            f.write(
                '\t\t\t\t<schemescale value="{}" comment="Scale used to create the initial scheme of Chrono objects '
                '(default=1)" />\n'.format(data['scale_scheme'])
            )
        if data['collisiondp_check'] and data['collisiondp'] != "":
            f.write(
                '\t\t\t\t<collisiondp value="{}" comment="Allowed collision overlap according Dp (default=0.5)" '
                '/>\n'.format(data['collisiondp'])
            )
        for chrono_element in data['chrono_objects']:
            if chrono_element[3] == 1:
                if chrono_element[4] == 0:
                    data['modelnormal_print'] = "original"
                elif chrono_element[4] == 1:
                    data['modelnormal_print'] = "invert"
                elif chrono_element[4] == 2:
                    data['modelnormal_print'] = "twoface"
                f.write(
                    '\t\t\t\t<{} id="{}" mkbound="{}" modelfile="AutoActual" modelnormal="{}"/>\n'.format(
                        chrono_element[5], str(chrono_element[1]), str(chrono_element[2]), data['modelnormal_print'])
                )
            else:
                f.write(
                    '\t\t\t\t<{} id="{}" mkbound="{}"/>\n'.format(chrono_element[5],
                                                                  str(chrono_element[1]), str(chrono_element[2]))
                )

        for ll in data['link_linearspring']:
            if ll[1] != "" and ll[2] != "":
                f.write(
                    '\t\t\t\t<link_linearspring idbody1="{}" idbody2="{}">\n'.format(str(ll[1]), str(ll[2]))
                )
                f.write(
                    '\t\t\t\t\t<point_fb1 x="{}" y="{}" z="{}" comment="Point in body 1" />\n'.format(ll[3][0],
                                                                                                      ll[3][1],
                                                                                                      ll[3][2])
                )
                f.write(
                    '\t\t\t\t\t<point_fb2 x="{}" y="{}" z="{}" comment="Point in body 2" />\n'.format(ll[4][0],
                                                                                                      ll[4][1],
                                                                                                      ll[4][2])
                )
                f.write(
                    '\t\t\t\t\t<stiffness value="{}" comment="Stiffness [N/m]" />\n'.format(ll[5])
                )
                f.write(
                    '\t\t\t\t\t<damping value="{}" comment="Damping [-]" />\n'.format(ll[6])
                )
                f.write(
                    '\t\t\t\t\t<rest_length value="{}" comment="Spring equilibrium length [m]" />\n'.format(ll[7])
                )
                f.write('\t\t\t\t\t<savevtk>\n')
                f.write(
                    '\t\t\t\t\t\t<nside value="{}" comment="number of sections for each revolution. 0=not saved, '
                    '1=line (default=16)" />\n'.format(ll[8][0])
                )
                f.write(
                    '\t\t\t\t\t\t<radius value="{}" comment="spring radius (default=3)" />\n'.format(ll[8][1])
                )
                f.write(
                    '\t\t\t\t\t\t<length value="{}" comment="length for each revolution (default=1)" />'
                    '\n'.format(ll[8][2])
                )
                f.write('\t\t\t\t\t</savevtk>\n')
                f.write('\t\t\t\t</link_linearspring>\n')

        for lh in data['link_hinge']:
            if lh[1] != "" and lh[2] != "":
                f.write(
                    '\t\t\t\t<link_hinge idbody1="{}" idbody2="{}">\n'.format(str(lh[1]), str(lh[2]))
                )
                f.write(
                    '\t\t\t\t\t<rotpoint x="{}" y="{}" z="{}" comment="Point for rotation" />\n'.format(lh[3][0],
                                                                                                        lh[3][1],
                                                                                                        lh[3][2])
                )
                f.write(
                    '\t\t\t\t\t<rotvector x="{}" y="{}" z="{}" comment="Vector direction for rotation" />'
                    '\n'.format(lh[4][0], lh[4][1], lh[4][2])
                )
                f.write(
                    '\t\t\t\t\t<stiffness value="{}" comment="Torsional stiffness [N/rad]" />\n'.format(lh[5])
                )
                f.write(
                    '\t\t\t\t\t<damping   value="{}" comment="Torsional damping [-]" />\n'.format(lh[6])
                )
                f.write('\t\t\t\t</link_hinge>\n')
        for ls in data['link_spheric']:
            if ls[1] != "":
                if ls[2] != "":
                    f.write(
                        '\t\t\t\t<link_spheric idbody1="{}" idbody2="{}">\n'.format(str(ls[1]), str(ls[2]))
                    )
                else:
                    f.write(
                        '\t\t\t\t<link_spheric idbody1="{}">\n'.format(str(ls[1]))
                    )

                f.write(
                    '\t\t\t\t\t<rotpoint x="{}" y="{}" z="{}" comment="Point for rotation" />\n'.format(ls[3][0],
                                                                                                        ls[3][1],
                                                                                                        ls[3][2])
                )
                f.write(
                    '\t\t\t\t\t<stiffness value="{}" comment="Torsional stiffness [N/rad]" />\n'.format(ls[4])
                )
                f.write(
                    '\t\t\t\t\t<damping value="{}" comment="Torsional damping [-]" />\n'.format(ls[5])
                )
                f.write('\t\t\t\t</link_spheric>\n')
        for lp in data['link_pointline']:
            if lp[1] != "":
                f.write('\t\t\t\t<link_pointline idbody1="{}">\n'.format(str(lp[1])))
                f.write(
                    '\t\t\t\t\t<slidingvector x="{}" y="{}" z="{}" comment="Vector direction for sliding axis" />'
                    '\n'.format(lp[2][0], lp[2][1], lp[2][2])
                )
                f.write(
                    '\t\t\t\t\t<rotpoint x="{}" y="{}" z="{}" comment="Point for rotation" />\n'.format(lp[3][0],
                                                                                                        lp[3][1],
                                                                                                        lp[3][2])
                )
                f.write(
                    '\t\t\t\t\t<rotvector x="{}" y="{}" z="{}" comment="Vector direction for rotation, use (0,0,0) for '
                    'spheric joint (default=(0,0,0))" />\n'.format(lp[4][0], lp[4][1], lp[4][2])
                )
                f.write(
                    '\t\t\t\t\t<rotvector2 x="{}" y="{}" z="{}" comment="Second vector to avoid rotation '
                    '(default=(0,0,0))" />\n'.format(lp[5][0], lp[5][1], lp[5][2])
                )
                f.write('\t\t\t\t\t<stiffness value="{}" comment="Torsional stiffness [N/rad]" />\n'.format(lp[6]))
                f.write('\t\t\t\t\t<damping value="{}" comment="Torsional damping [-]" />\n'.format(lp[7]))
                f.write('\t\t\t\t</link_pointline>\n')
        f.write('\t\t\t</chrono>\n')

    # Inlet/Outlet objects
    if len(data['inlet_zone']) > 0:
        f.write('\t\t\t<inout reuseids="{}" resizetime="{}">\n'.format(str(data['inlet_object'][0]).lower(), float(data['inlet_object'][1])))
        f.write('\t\t\t\t<userefilling value="{}" comment="Use advanced refilling algorithm but slower. It is necessary when outflow becomes inflow (default=false)" />\n'.format(str(data['inlet_object'][2]).lower()))
        f.write('\t\t\t\t<determlimit value="{}" comment="Use 1e-3 for first_order or 1e+3 for zeroth_order (default=1e+3)" />\n'.format(str(data['inlet_object'][3]).lower()))
        for target_zone in data['inlet_zone']:
            f.write('\t\t\t\t<inoutzone>\n')
            f.write('\t\t\t\t\t<convertfluid value="{}" comment="Converts fluid in inlet/outlet area (default=true)" />\n'.format(str(target_zone[1]).lower()))
            f.write('\t\t\t\t\t<layers value="{}" comment="Number of inlet/outlet particle layers" />\n'.format(int(target_zone[2])))
            if target_zone[3][0] == "zone2d":
                f.write('\t\t\t\t\t<zone2d comment="Input zone for 2-D simulations">\n')
                f.write('\t\t\t\t\t\t<particles mkfluid="{}" direction="{}" />\n'.format(int(target_zone[3][1]), str(target_zone[3][2]).lower()))
                f.write('\t\t\t\t\t</zone2d>\n')
            else:
                f.write('\t\t\t\t\t<zone3d comment="">\n')
                f.write('\t\t\t\t\t</zone3d>\n')
            f.write('\t\t\t\t\t<imposevelocity mode="{}" comment="Imposed velocity 0:fixed value, 1:variable value, 2:Extrapolated velocity, 3:Interpolated velocity (default=0)">\n'.format(int(target_zone[4][0])))
            if target_zone[4][0] == 0:
                f.write('\t\t\t\t\t\t<velocity v="{}" comment="Uniform velocity" units_comment="m/s" />\n'.format(float(target_zone[4][1])))
            f.write('\t\t\t\t\t</imposevelocity>\n')
            f.write('\t\t\t\t\t<imposerhop mode="{}" comment="Outlet rhop 0:Imposed fixed value, 1:Hydrostatic, 2:Extrapolated from ghost nodes (default=0)" />\n'.format(int(target_zone[5][0])))
            f.write('\t\t\t\t\t<imposezsurf mode="{}" comment="Inlet Z-surface 0:Imposed fixed value, 1:Imposed variable value, 2:Calculated from fluid domain (default=0)">\n'.format(int(target_zone[6][0])))
            if target_zone[6][0] == 0 or target_zone[6][0] == 2:
                f.write('\t\t\t\t\t\t<zbottom value="{}" comment="Bottom level of water (used for Hydrostatic option)" units_comment="m" />\n'.format(float(target_zone[6][1])))
                f.write('\t\t\t\t\t\t<zsurf value="{}" comment="Characteristic inlet Z-surface (used for Hydrostatic option)" units_comment="m" />\n'.format(float(target_zone[6][2])))
            f.write('\t\t\t\t\t</imposezsurf>\n')
            f.write('\t\t\t\t</inoutzone>\n')
        f.write('\t\t\t</inout>\n')

    # A counter for special movements. Controls when and how to open/close tags
    written_movements_counter = 0
    for mk, motlist in data["motion_mks"].items():
        # Check if object has motion enabled but no motions selected
        if len(motlist) < 1:
            continue
        if isinstance(motlist[0], SpecialMovement):
            mot = motlist[0].generator
            if isinstance(mot, FileGen) or isinstance(mot, RotationFileGen):
                continue

            # Open tags only for the first movement
            if written_movements_counter == 0:
                f.write('\t\t\t<wavepaddles>\n')

            if isinstance(mot, RegularPistonWaveGen):
                f.write('\t\t\t\t<piston>\n')
                f.write('\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write(
                    '\t\t\t\t\t<waveorder value="{}" ' 'comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(
                        mot.wave_order))
                f.write(
                    '\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(mot.start))
                f.write(
                    '\t\t\t\t\t<duration value="{}" ' 'comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                        mot.duration))
                f.write(
                    '\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(mot.depth))
                f.write(
                    '\t\t\t\t\t<pistondir x="{}" y="{}" z="{}" ' 'comment="Movement direction (def=(1,0,0))" />\n'.format(
                        *mot.piston_dir))
                f.write(
                    '\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(mot.wave_height))
                f.write(
                    '\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(mot.wave_period))
                f.write(
                    '\t\t\t\t\t<phase value="{}" ' 'comment="Initial wave phase in function of PI (def=0)" />\n'.format(
                        mot.phase))
                f.write(
                    '\t\t\t\t\t<ramp value="{}" comment="Periods of ramp (def=0)" />\n'.format(mot.ramp))
                f.write('\t\t\t\t\t<savemotion periods="{}" periodsteps="{}" xpos="{}" zpos="{}" '
                        'comment="Saves motion data. xpos and zpos are optional. '
                        'zpos=-depth of the measuring point" />\n'.format(mot.disksave_periods,
                                                                          mot.disksave_periodsteps, mot.disksave_xpos,
                                                                          mot.disksave_zpos))
                if mot.awas.enabled:
                    f.write('\t\t\t\t\t<awas_zsurf>\n')
                    f.write(
                        '\t\t\t\t\t\t<startawas value="{}" comment="Time to start AWAS correction (def=ramp*waveperiod)" />\n'.format(
                            float(mot.awas.startawas)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<swl value="{}" comment="Still water level (free-surface water)" />\n'.format(
                            float(mot.awas.swl)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<elevation value="{}" comment="Order wave to calculate elevation 1:1st order, 2:2nd order (def=2)" />\n'.format(
                            int(mot.awas.elevation)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugex valueh="{}" comment="Position in X from piston to measure free-surface water (def=5*Dp)" />\n'.format(
                            float(mot.awas.gaugex)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugey value="{}" comment="Position in Y to measure free-surface water" />\n'.format(
                            float(mot.awas.gaugey)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugezmin value="{}" comment="Minimum position in Z to measure free-surface water, it must be in water (def=domain limits)" />\n'.format(
                            float(mot.awas.gaugezmin)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugezmax value="{}" comment="Maximum position in Z to measure free-surface water (def=domain limits)" />\n'.format(
                            float(mot.awas.gaugezmax)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugedp value="{}" comment="Resolution to measure free-surface water, it uses Dp*gaugedp (def=0.1)" />\n'.format(
                            float(mot.awas.gaugedp)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<coefmasslimit value="{}" comment="Coefficient to calculate mass of free-surface (def=0.5 on 3D and 0.4 on 2D)" />\n'.format(
                            float(mot.awas.coefmasslimit)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<savedata value="{}" comment="Saves CSV with information 1:by part, 2:more info 3:by step (def=0)" />\n'.format(
                            int(mot.awas.savedata)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<limitace value="{}" comment="Factor to limit maximum value of acceleration, with 0 disabled (def=2)" />\n'.format(
                            float(mot.awas.limitace)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<{}correction coefstroke="{}" coefperiod="{}" powerfunc="{}" comment="Drift correction configuration (def=no applied)" />\n'.format(
                            "" if mot.awas.correction.enabled else "_",
                            float(mot.awas.correction.coefstroke),
                            float(mot.awas.correction.coefperiod),
                            float(mot.awas.correction.powerfunc)
                        ))
                    f.write('\t\t\t\t\t</awas_zsurf>\n')
                f.write('\t\t\t\t</piston>\n')
                written_movements_counter += 1

            elif isinstance(mot, IrregularPistonWaveGen):
                f.write('\t\t\t\t<piston_spectrum>\n')
                f.write(
                    '\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write(
                    '\t\t\t\t\t<waveorder value="{}" ' 'comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(
                        mot.wave_order))
                f.write(
                    '\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(mot.start))
                f.write(
                    '\t\t\t\t\t<duration value="{}" ' 'comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                        mot.duration))
                f.write(
                    '\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(mot.depth))
                # f.write(
                #     '\t\t\t\t\t<fixeddepth value="{}" ' 'comment="Fluid depth without paddle (def=0)" />\n'.format(
                #         mot.fixed_depth))
                f.write(
                    '\t\t\t\t\t<pistondir x="{}" y="{}" z="{}" ' 'comment="Movement direction (def=(1,0,0))" />\n'.format(
                        *mot.piston_dir))
                f.write('\t\t\t\t\t<spectrum value="{}" '
                        'comment="Spectrum type: jonswap,pierson-moskowitz" />\n'.format(
                            ['jonswap', 'pierson-moskowitz'][mot.spectrum]))
                f.write('\t\t\t\t\t<discretization value="{}" '
                        'comment="Spectrum discretization: regular,random,stretched,cosstretched '
                        '(def=stretched)" />\n'.format(
                            ['regular', 'random', 'stretched', 'cosstretched'][mot.discretization]))
                f.write(
                    '\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(mot.wave_height))
                f.write(
                    '\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(mot.wave_period))
                f.write(
                    '\t\t\t\t\t<peakcoef value="{}" comment="Peak enhancement coefficient (def=3.3)" />\n'.format(
                        mot.peak_coef))
                f.write(
                    '\t\t\t\t\t<waves value="{}" ' 'comment="Number of waves to create irregular waves (def=50)" />\n'.format(
                        mot.waves))
                f.write(
                    '\t\t\t\t\t<randomseed value="{}" ' 'comment="Random seed to initialize a pseudorandom number generator" />\n'.format(
                        mot.randomseed))
                f.write(
                    '\t\t\t\t\t<serieini value="{}" autofit="{}" '
                    'comment="Initial time in irregular wave serie (default=0 and autofit=false)" />\n'.format(
                        mot.serieini, str(mot.serieini_autofit).lower()
                    )
                )
                f.write(
                    '\t\t\t\t\t<ramptime value="{}" comment="Time of ramp (def=0)" />\n'.format(mot.ramptime))
                f.write('\t\t\t\t\t<savemotion time="{}" timedt="{}" xpos="{}" zpos="{}" '
                        'comment="Saves motion data. xpos and zpos are optional. '
                        'zpos=-depth of the measuring point" />\n'.format(mot.savemotion_time, mot.savemotion_timedt,
                                                                          mot.savemotion_xpos, mot.savemotion_zpos))
                f.write('\t\t\t\t\t<saveserie timemin="{}" timemax="{}" timedt="{}" xpos="{}"'
                        ' comment="Saves serie data (optional)" />\n'.format(mot.saveserie_timemin,
                                                                             mot.saveserie_timemax,
                                                                             mot.saveserie_timedt,
                                                                             mot.saveserie_xpos))
                f.write('\t\t\t\t\t<saveseriewaves timemin="{}" timemax="{}" xpos="{}" '
                        'comment="Saves serie heights" />\n'.format(mot.saveseriewaves_timemin,
                                                                    mot.saveseriewaves_timemax,
                                                                    mot.saveseriewaves_xpos))
                if mot.awas.enabled:
                    f.write('\t\t\t\t\t<awas_zsurf>\n')
                    f.write(
                        '\t\t\t\t\t\t<startawas value="{}" comment="Time to start AWAS correction (def=ramp*waveperiod)" />\n'.format(
                            float(mot.awas.startawas)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<swl value="{}" comment="Still water level (free-surface water)" />\n'.format(
                            float(mot.awas.swl)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<elevation value="{}" comment="Order wave to calculate elevation 1:1st order, 2:2nd order (def=2)" />\n'.format(
                            int(mot.awas.elevation)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugex valueh="{}" comment="Position in X from piston to measure free-surface water (def=5*Dp)" />\n'.format(
                            float(mot.awas.gaugex)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugey value="{}" comment="Position in Y to measure free-surface water" />\n'.format(
                            float(mot.awas.gaugey)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugezmin value="{}" comment="Minimum position in Z to measure free-surface water, it must be in water (def=domain limits)" />\n'.format(
                            float(mot.awas.gaugezmin)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugezmax value="{}" comment="Maximum position in Z to measure free-surface water (def=domain limits)" />\n'.format(
                            float(mot.awas.gaugezmax)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<gaugedp value="{}" comment="Resolution to measure free-surface water, it uses Dp*gaugedp (def=0.1)" />\n'.format(
                            float(mot.awas.gaugedp)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<coefmasslimit value="{}" comment="Coefficient to calculate mass of free-surface (def=0.5 on 3D and 0.4 on 2D)" />\n'.format(
                            float(mot.awas.coefmasslimit)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<savedata value="{}" comment="Saves CSV with information 1:by part, 2:more info 3:by step (def=0)" />\n'.format(
                            int(mot.awas.savedata)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<limitace value="{}" comment="Factor to limit maximum value of acceleration, with 0 disabled (def=2)" />\n'.format(
                            float(mot.awas.limitace)
                        ))
                    f.write(
                        '\t\t\t\t\t\t<{}correction coefstroke="{}" coefperiod="{}" powerfunc="{}" comment="Drift correction configuration (def=no applied)" />\n'.format(
                            "" if mot.awas.correction.enabled else "_",
                            float(mot.awas.correction.coefstroke),
                            float(mot.awas.correction.coefperiod),
                            float(mot.awas.correction.powerfunc)
                        ))
                    f.write('\t\t\t\t\t</awas_zsurf>\n')
                f.write('\t\t\t\t</piston_spectrum>\n')
                written_movements_counter += 1

            elif isinstance(mot, RegularFlapWaveGen):
                f.write('\t\t\t\t<flap>\n')
                f.write(
                    '\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write(
                    '\t\t\t\t\t<waveorder value="{}" ' 'comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(
                        mot.wave_order))
                f.write(
                    '\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(mot.start))
                f.write(
                    '\t\t\t\t\t<duration value="{}" ' 'comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                        mot.duration))
                f.write(
                    '\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(mot.depth))
                f.write(
                    '\t\t\t\t\t<variabledraft value="{}" comment="Position of the wavemaker hinge (above the bottom <0; below the bottom >0) (default=0)" />\n'.format(
                        mot.variable_draft))
                f.write(
                    '\t\t\t\t\t<flapaxis0 x="{}" y="{}" z="{}" comment="Point 0 of axis rotation" />\n'.format(
                        mot.flapaxis0[0], mot.flapaxis0[1], mot.flapaxis0[2]))
                f.write(
                    '\t\t\t\t\t<flapaxis1 x="{}" y="{}" z="{}" comment="Point 1 of axis rotation" />\n'.format(
                        mot.flapaxis1[0], mot.flapaxis1[1], mot.flapaxis1[2]))
                f.write(
                    '\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(mot.wave_height))
                f.write(
                    '\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(mot.wave_period))
                f.write(
                    '\t\t\t\t\t<phase value="{}" ' 'comment="Initial wave phase in function of PI (def=0)" />\n'.format(
                        mot.phase))
                f.write(
                    '\t\t\t\t\t<ramp value="{}" comment="Periods of ramp (def=0)" />\n'.format(mot.ramp))
                f.write('\t\t\t\t\t<savemotion periods="{}" periodsteps="{}" xpos="{}" zpos="{}" '
                        'comment="Saves motion data. xpos and zpos are optional. '
                        'zpos=-depth of the measuring point" />\n'.format(mot.disksave_periods,
                                                                          mot.disksave_periodsteps, mot.disksave_xpos,
                                                                          mot.disksave_zpos))
                f.write('\t\t\t\t</flap>\n')
                written_movements_counter += 1

            elif isinstance(mot, IrregularFlapWaveGen):
                f.write('\t\t\t\t<flap_spectrum>\n')
                f.write(
                    '\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write(
                    '\t\t\t\t\t<waveorder value="{}" ' 'comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(
                        mot.wave_order))
                f.write(
                    '\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(mot.start))
                f.write(
                    '\t\t\t\t\t<duration value="{}" ' 'comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                        mot.duration))
                f.write(
                    '\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(mot.depth))
                # f.write(
                #     '\t\t\t\t\t<fixeddepth value="{}" ' 'comment="Fluid depth without paddle (def=0)" />\n'.format(
                #         mot.fixed_depth))
                f.write(
                    '\t\t\t\t\t<variabledraft value="{}" comment="Position of the wavemaker hinge (above the bottom <0; below the bottom >0) (default=0)" />\n'.format(
                        mot.variable_draft))
                f.write(
                    '\t\t\t\t\t<flapaxis0 x="{}" y="{}" z="{}" comment="Point 0 of axis rotation" />\n'.format(
                        mot.flapaxis0[0], mot.flapaxis0[1], mot.flapaxis0[2]))
                f.write(
                    '\t\t\t\t\t<flapaxis1 x="{}" y="{}" z="{}" comment="Point 1 of axis rotation" />\n'.format(
                        mot.flapaxis1[0], mot.flapaxis1[1], mot.flapaxis1[2]))
                f.write('\t\t\t\t\t<spectrum value="{}" '
                        'comment="Spectrum type: jonswap,pierson-moskowitz" />\n'.format(
                            ['jonswap', 'pierson-moskowitz'][mot.spectrum]))
                f.write('\t\t\t\t\t<discretization value="{}" '
                        'comment="Spectrum discretization: regular,random,stretched,cosstretched '
                        '(def=stretched)" />\n'.format(
                            ['regular', 'random', 'stretched', 'cosstretched'][mot.discretization]))
                f.write(
                    '\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(mot.wave_height))
                f.write(
                    '\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(mot.wave_period))
                f.write(
                    '\t\t\t\t\t<peakcoef value="{}" comment="Peak enhancement coefficient (def=3.3)" />\n'.format(
                        mot.peak_coef))
                f.write(
                    '\t\t\t\t\t<waves value="{}" ' 'comment="Number of waves to create irregular waves (def=50)" />\n'.format(
                        mot.waves))
                f.write(
                    '\t\t\t\t\t<randomseed value="{}" ' 'comment="Random seed to initialize a pseudorandom number generator" />\n'.format(
                        mot.randomseed))
                f.write(
                    '\t\t\t\t\t<serieini value="{}" autofit="{}" '
                    'comment="Initial time in irregular wave serie (default=0 and autofit=false)" />\n'.format(
                        mot.serieini, str(mot.serieini_autofit).lower()
                    )
                )
                f.write(
                    '\t\t\t\t\t<ramptime value="{}" comment="Time of ramp (def=0)" />\n'.format(mot.ramptime))
                f.write('\t\t\t\t\t<savemotion time="{}" timedt="{}" xpos="{}" zpos="{}" '
                        'comment="Saves motion data. xpos and zpos are optional. '
                        'zpos=-depth of the measuring point" />\n'.format(mot.savemotion_time, mot.savemotion_timedt,
                                                                          mot.savemotion_xpos, mot.savemotion_zpos))
                f.write('\t\t\t\t\t<saveserie timemin="{}" timemax="{}" timedt="{}" xpos="{}"'
                        ' comment="Saves serie data (optional)" />\n'.format(mot.saveserie_timemin,
                                                                             mot.saveserie_timemax,
                                                                             mot.saveserie_timedt,
                                                                             mot.saveserie_xpos))
                f.write('\t\t\t\t\t<saveseriewaves timemin="{}" timemax="{}" xpos="{}" '
                        'comment="Saves serie heights" />\n'.format(mot.saveseriewaves_timemin,
                                                                    mot.saveseriewaves_timemax,
                                                                    mot.saveseriewaves_xpos))
                f.write('\t\t\t\t</flap_spectrum>\n')
                written_movements_counter += 1

    # Close tags only if at least one movement was written.
    if written_movements_counter > 0:
        f.write('\t\t\t</wavepaddles>\n')

    if len(data['mlayerpistons'].keys()) > 0:
        f.write('\t\t\t<mlayerpistons>\n')
        for mk, pistonobject in data['mlayerpistons'].items():
            if isinstance(pistonobject, MLPiston1D):
                f.write('\t\t\t\t<piston1d>\n')
                f.write('\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write('\t\t\t\t\t<filevelx value="{}" comment="File name with X velocity" />\n'.format(
                    pistonobject.filevelx))
                f.write('\t\t\t\t\t<incz value="{}" comment="Z offset (def=0)" />\n'.format(pistonobject.incz))
                f.write('\t\t\t\t\t<timedataini value="{}" comment="Time offset (def=0)" />\n'.format(
                    pistonobject.timedataini))
                f.write('\t\t\t\t\t<smooth value="{}" comment="Smooth motion level (def=0)" />\n'.format(
                    pistonobject.smooth))
                f.write('\t\t\t\t</piston1d>\n')
            if isinstance(pistonobject, MLPiston2D):
                f.write('\t\t\t\t<piston2d>\n')
                f.write('\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write('\t\t\t\t\t<incz value="{}" comment="Z offset (def=0)" />\n'.format(pistonobject.incz))
                f.write('\t\t\t\t\t<smoothz value="{}" comment="Smooth motion level (def=0)" />\n'.format(
                    pistonobject.smoothz))
                f.write('\t\t\t\t\t<smoothy value="{}" comment="Smooth motion level (def=0)" />\n'.format(
                    pistonobject.smoothy))
                for veldata in pistonobject.veldata:
                    f.write('\t\t\t\t\t<veldata>\n')
                    f.write('\t\t\t\t\t\t<filevelx value="{}" comment="File name with X velocity" />\n'.format(
                        veldata.filevelx))
                    f.write('\t\t\t\t\t\t<posy value="{}" comment="Position Y of data" />\n'.format(veldata.posy))
                    f.write('\t\t\t\t\t\t<timedataini value="{}" comment="Time offset (def=0)" />\n'.format(
                        veldata.timedataini))
                    f.write('\t\t\t\t\t</veldata>\n')

                f.write('\t\t\t\t</piston2d>\n')
        f.write('\t\t\t</mlayerpistons>\n')

    if data['relaxationzone'] is not None:
        f.write('\t\t\t<relaxationzones>\n')
        rzobject = data['relaxationzone']
        if isinstance(rzobject, RelaxationZoneRegular):
            f.write('\t\t\t\t<rzwaves_regular>\n')
            f.write('\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(rzobject.start))
            f.write(
                '\t\t\t\t\t<duration value="{}" comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                    rzobject.duration))
            f.write(
                '\t\t\t\t\t<waveorder value="{}" comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(
                    rzobject.waveorder))
            f.write('\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(rzobject.waveheight))
            f.write('\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(rzobject.waveperiod))
            f.write('\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(rzobject.depth))
            f.write('\t\t\t\t\t<swl value="{}" comment="Still water level (free-surface water)" />\n'.format(
                rzobject.swl))
            f.write(
                '\t\t\t\t\t<center x="{}" y="{}" z="{}" comment="Central point of application" />\n'.format(
                    *rzobject.center))
            f.write('\t\t\t\t\t<width value="{}" comment="Width for generation" />\n'.format(rzobject.width))
            f.write('\t\t\t\t\t<phase value="{}" comment="Initial wave phase in function of PI (def=0)" />\n'.format(
                rzobject.phase))
            f.write('\t\t\t\t\t<ramp value="{}" comment="Periods of ramp (def=0)" />\n'.format(rzobject.ramp))
            f.write(
                '\t\t\t\t\t<savemotion periods="{}" periodsteps="{}" xpos="{}" zpos="{}" comment="Saves motion data. xpos and zpos are optional. zpos=-depth of the measuring point" />\n'.format(
                    rzobject.savemotion_periods, rzobject.savemotion_periodsteps, rzobject.savemotion_xpos,
                    rzobject.savemotion_zpos))
            f.write(
                '\t\t\t\t\t<coefdir x="{}" y="{}" z="{}" comment="Coefficients for each direction (default=(1,0,0))" />\n'.format(
                    *rzobject.coefdir))
            f.write(
                '\t\t\t\t\t<coefdt value="{}" comment="Multiplies by dt value in the calculation (using 0 is not applied) (default=1000)" />\n'.format(
                    rzobject.coefdt))
            f.write(
                '\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in function for velocity (def. psi=0.9, beta=1)" />\n'.format(
                    rzobject.function_psi, rzobject.function_beta))
            f.write(
                '\t\t\t\t\t<driftcorrection value="{}" comment="Coefficient of drift correction applied in velocity X. 0:Disabled, 1:Full correction (def=0)" />\n'.format(
                    rzobject.driftcorrection))
            f.write('\t\t\t\t</rzwaves_regular>\n')
        if isinstance(rzobject, RelaxationZoneFile):
            f.write('\t\t\t\t<rzwaves_external_1d>\n')
            f.write('\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(rzobject.start))
            f.write(
                '\t\t\t\t\t<duration value="{}" comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                    rzobject.duration))
            f.write('\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(rzobject.depth))
            f.write('\t\t\t\t\t<swl value="{}" comment="Still water level (free-surface water)" />\n'.format(
                rzobject.swl))
            f.write('\t\t\t\t\t<filesvel value="{}" comment="Main name of files with velocity to use" />\n'.format(rzobject.filesvel))
            f.write('\t\t\t\t\t<filesvelx initial="{}" count="{}" comment="First file and count to use" />\n'.format(rzobject.filesvelx_initial,
                                                                                                                     rzobject.filesvelx_count))
            f.write('\t\t\t\t\t<usevelz value="{}" comment="Use velocity in Z or not (def=false)" />\n'.format("true" if rzobject.usevelz else "false"))
            f.write('\t\t\t\t\t<movedata x="{}" y="{}" z="{}" comment="Movement of data in CSV files" />\n'.format(*rzobject.movedata))
            f.write('\t\t\t\t\t<dpz valuedp="{}" comment="Distance between key points in Z (def=2)" />\n'.format(rzobject.dpz))
            f.write('\t\t\t\t\t<smooth value="{}" comment="Smooth motion level (def=0)" />\n'.format(rzobject.smooth))
            f.write(
                '\t\t\t\t\t<center x="{}" y="{}" z="{}" comment="Central point of application" />\n'.format(
                    *rzobject.center))
            f.write('\t\t\t\t\t<width value="{}" comment="Width for generation" />\n'.format(rzobject.width))
            f.write(
                '\t\t\t\t\t<coefdir x="{}" y="{}" z="{}" comment="Coefficients for each direction (default=(1,0,0))" />\n'.format(
                    *rzobject.coefdir))
            f.write(
                '\t\t\t\t\t<coefdt value="{}" comment="Multiplies by dt value in the calculation (using 0 is not applied) (default=1000)" />\n'.format(
                    rzobject.coefdt))
            f.write(
                '\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in function for velocity (def. psi=0.9, beta=1)" />\n'.format(
                    rzobject.function_psi, rzobject.function_beta))
            f.write(
                '\t\t\t\t\t<driftcorrection value="{}" comment="Coefficient of drift correction applied in velocity X. 0:Disabled, 1:Full correction (def=0)" />\n'.format(
                    rzobject.driftcorrection))
            f.write(
                '\t\t\t\t\t<driftinitialramp value="{}" comment="Ignore waves from external data in initial seconds (def=0)" />\n'.format(
                    rzobject.driftinitialramp))
            f.write('\t\t\t\t</rzwaves_external_1d>\n')
        if isinstance(rzobject, RelaxationZoneIrregular):
            f.write('\t\t\t\t<rzwaves_spectrum>\n')
            f.write('\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(rzobject.start))
            f.write(
                '\t\t\t\t\t<duration value="{}" comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(
                    rzobject.duration))
            f.write('\t\t\t\t\t<peakcoef value="{}" comment="Peak enhancement coefficient (default=3.3)" />\n'.format(
                rzobject.peakcoef))
            f.write('\t\t\t\t\t<spectrum value="{}" comment="Spectrum type: jonswap,pierson-moskowitz" />\n'.format(
                ["jonswap", "pierson-moskowitz"][rzobject.spectrum]
            ))
            f.write(
                '\t\t\t\t\t<discretization value="{}" comment="Spectrum discretization: regular,random,stretched,cosstretched (default=stretched)" />\n'.format(
                    ["regular", "random", "stretched", "cosstretched"][rzobject.discretization]
                ))
            f.write(
                '\t\t\t\t\t<waveorder value="{}" comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(
                    rzobject.waveorder))
            f.write('\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(rzobject.waveheight))
            f.write('\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(rzobject.waveperiod))
            f.write(
                '\t\t\t\t\t<waves value="{}" comment="Number of waves to create irregular waves (default=50)" />\n'.format(
                    rzobject.waves))
            f.write(
                '\t\t\t\t\t<randomseed value="{}" comment="Random seed to initialize a pseudorandom number generator" />\n'.format(
                    rzobject.randomseed))
            f.write('\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(rzobject.depth))
            f.write('\t\t\t\t\t<swl value="{}" comment="Still water level (free-surface water)" />\n'.format(
                rzobject.swl))
            f.write(
                '\t\t\t\t\t<center x="{}" y="{}" z="{}" comment="Central point of application" />\n'.format(
                    *rzobject.center))
            f.write('\t\t\t\t\t<width value="{}" comment="Width for generation" />\n'.format(rzobject.width))
            f.write('\t\t\t\t\t<ramptime value="{}" comment="Time of initial ramp (default=0)" />\n'.format(
                rzobject.ramptime))
            f.write(
                '\t\t\t\t\t<serieini value="{}" comment="Initial time in irregular wave serie (default=0)" />\n'.format(
                    rzobject.serieini))
            f.write(
                '\t\t\t\t\t<savemotion time="{}" timedt="{}" xpos="{}" zpos="{}" comment="Saves motion data. xpos and zpos are optional. zpos=-depth of the measuring point" />\n'.format(
                    rzobject.savemotion_time, rzobject.savemotion_timedt, rzobject.savemotion_xpos,
                    rzobject.savemotion_zpos))
            f.write(
                '\t\t\t\t\t<saveserie timemin="{}" timemax="{}" timedt="{}" xpos="{}" comment="Saves serie data (optional)" />\n'.format(
                    rzobject.saveserie_timemin, rzobject.saveserie_timemax, rzobject.saveserie_timedt,
                    rzobject.saveserie_xpos))
            f.write(
                '\t\t\t\t\t<saveseriewaves timemin="{}" timemax="{}" xpos="{}" comment="Saves serie heights" />\n'.format(
                    rzobject.saveseriewaves_timemin, rzobject.saveseriewaves_timemax, rzobject.saveseriewaves_xpos))
            f.write(
                '\t\t\t\t\t<coefdir x="{}" y="{}" z="{}" comment="Coefficients for each direction (default=(1,0,0))" />\n'.format(
                    *rzobject.coefdir))
            f.write(
                '\t\t\t\t\t<coefdt value="{}" comment="Multiplies by dt value in the calculation (using 0 is not applied) (default=1000)" />\n'.format(
                    rzobject.coefdt))
            f.write(
                '\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in function for velocity (def. psi=0.9, beta=1)" />\n'.format(
                    rzobject.function_psi, rzobject.function_beta))
            f.write(
                '\t\t\t\t\t<driftcorrection value="{}" comment="Coefficient of drift correction applied in velocity X. 0:Disabled, 1:Full correction (def=0)" />\n'.format(
                    rzobject.driftcorrection))
            f.write('\t\t\t\t</rzwaves_spectrum>\n')
        if isinstance(rzobject, RelaxationZoneUniform):
            f.write('\t\t\t\t<rzwaves_uniform>\n')
            f.write('\t\t\t\t\t<start value="{}" comment="Start time (default=0)" />\n'.format(str(rzobject.start)))
            f.write('\t\t\t\t\t<duration value="{}" comment="Duration, Zero is the end of simulation (default=0)" />\n'.format(str(rzobject.duration)))
            f.write('\t\t\t\t\t<domainbox>\n')
            f.write('\t\t\t\t\t\t<point x="{}" y="{}" z="{}" />\n'.format(*rzobject.domainbox_point))
            f.write('\t\t\t\t\t\t<size x="{}" y="{}" z="{}" />\n'.format(*rzobject.domainbox_size))
            f.write('\t\t\t\t\t\t<direction x="{}" y="{}" z="{}" />\n'.format(*rzobject.domainbox_direction))
            f.write('\t\t\t\t\t\t<rotateaxis angle="{}" anglesunits="degrees">\n'.format(str(rzobject.domainbox_rotateaxis_angle)))
            f.write('\t\t\t\t\t\t\t<point1 x="{}" y="{}" z="{}" />\n'.format(*rzobject.domainbox_rotateaxis_point1))
            f.write('\t\t\t\t\t\t\t<point2 x="{}" y="{}" z="{}" />\n'.format(*rzobject.domainbox_rotateaxis_point2))
            f.write('\t\t\t\t\t\t</rotateaxis>\n')
            f.write('\t\t\t\t\t</domainbox>\n')
            if rzobject.use_velocity:
                f.write('\t\t\t\t\t<velocity value="{}" comment="Velocity to impose (it is ignored when velocitytimes is defined)" />\n'.format(str(rzobject.velocity)))
            else:
                f.write('\t\t\t\t\t<velocitytimes comment="Uniform velocity in time">\n')
                for tv in rzobject.velocity_times:
                    f.write('\t\t\t\t\t\t<timevalue time="{}" v="{}" />\n'.format(str(tv[0]), str(tv[1])))
                f.write('\t\t\t\t\t</velocitytimes>\n')
            f.write('\t\t\t\t\t<coefdt value="{}" comment="Multiplies by dt value in the calculation (using 0 is not applied) (default=1000)" />\n'.format(str(rzobject.coefdt)))
            f.write('\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in function for velocity (def. psi=0.9, beta=1)" />\n'.format(str(rzobject.function_psi), str(rzobject.function_beta)))
            f.write('\t\t\t\t</rzwaves_uniform>\n')
        f.write('\t\t\t</relaxationzones>\n')

    f.write('\t\t</special>\n')

    f.write('\t\t<parameters>\n')
    # Writes parameters as user introduced
    f.write('\t\t\t<parameter key="PosDouble" value="' + str(
        data['posdouble']) + '" comment="Precision in particle interaction '
                             '0:Simple, 1:Double, 2:Uses and saves double (default=0)" />\n')
    f.write('\t\t\t<parameter key="StepAlgorithm" value="' +
            str(data['stepalgorithm']) + '" comment="Step Algorithm 1:Verlet, 2:Symplectic (default=1)" />\n')
    f.write('\t\t\t<parameter key="VerletSteps" value="' + str(data['verletsteps']) +
            '" comment="Verlet only: Number of steps to apply Euler timestepping (default=40)" />\n')
    f.write('\t\t\t<parameter key="Kernel" value="' +
            str(data['kernel']) + '" comment="Interaction Kernel 1:Cubic Spline, 2:Wendland (default=2)" />\n')
    f.write('\t\t\t<parameter key="ViscoTreatment" value="' + str(data['viscotreatment']) +
            '" comment="Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)" />\n')
    f.write('\t\t\t<parameter key="Visco" value="' + str(
        data['visco']) + '" comment="Viscosity value" /> % Note alpha can depend on the resolution. '
                         'A value of 0.01 is recommended for near irrotational flows.\n')
    f.write('\t\t\t<parameter key="ViscoBoundFactor" value="' + str(data['viscoboundfactor']) +
            '" comment="Multiply viscosity value with boundary (default=1)" />\n')
    f.write('\t\t\t<parameter key="DeltaSPH" value="' + str(data['deltasph']) +
            '" comment="DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0)" />\n')
    f.write('\t\t\t<parameter key="Shifting" value="' + str(data['shifting']) +
            '" comment="Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0)" />\n')
    f.write('\t\t\t<parameter key="ShiftCoef" value="' +
            str(data['shiftcoef']) + '" comment="Coefficient for shifting computation (default=-2)" />\n')
    f.write('\t\t\t<parameter key="ShiftTFS" value="' + str(data['shifttfs']) +
            '" comment="Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0)" />\n')
    f.write('\t\t\t<parameter key="RigidAlgorithm" value="' +
            str(data['rigidalgorithm']) + '" comment="Rigid Algorithm 1:SPH, 2:DEM, 3:CHRONO (default=1)" />\n')
    f.write('\t\t\t<parameter key="FtPause" value="' + str(
        data['ftpause']) + '" comment="Time to freeze the floatings at simulation start'
                           ' (warmup) (default=0)" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="CoefDtMin" value="' + str(data['coefdtmin']) +
            '" comment="Coefficient to calculate minimum time step dtmin=coefdtmin*h/speedsound (default=0.05)" />\n')
    if data["dtini_auto"]:
        comment = "#"
    else:
        comment = ""
    f.write('\t\t\t<parameter key="' + comment + 'DtIni" value="' + str(data['dtini']) +
            '" comment="Initial time step (default=h/speedsound)" units_comment="seconds" />\n')
    if data["dtmin_auto"]:
        comment = "#"
    else:
        comment = ""
    f.write('\t\t\t<parameter key="' + comment + 'DtMin" value="' + str(data['dtmin']) +
            '" comment="Minimum time step (default=coefdtmin*h/speedsound)" units_comment="seconds" />\n')
    # f.write('\t\t\t<parameter key="#DtFixed" value="'+str(data['dtfixed'])+'"
    # comment="Dt values are loaded from file (default=disabled)" />\n')
    f.write('\t\t\t<parameter key="DtAllParticles" value="' + str(data['dtallparticles']) +
            '" comment="Velocity of particles used to calculate DT. 1:All, 0:Only fluid/floating (default=0)" />\n')
    f.write('\t\t\t<parameter key="TimeMax" value="' +
            str(data['timemax']) + '" comment="Time of simulation" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="TimeOut" value="' +
            str(data['timeout']) + '" comment="Time out data" units_comment="seconds" />\n')
    if not data['simdomain_chk'] and data['incz'] > 0:
        f.write('\t\t\t<parameter key="IncZ" value="' +
                str(data['incz']) + '" comment="Increase of Z+" units_comment="decimal" />\n')
    f.write('\t\t\t<parameter key="PartsOutMax" value="' + str(
        data['partsoutmax']) + '" comment="%/100 of fluid particles allowed to be excluded from domain '
                               '(default=1)" units_comment="decimal" />\n')
    f.write('\t\t\t<parameter key="RhopOutMin" value="' +
            str(data['rhopoutmin']) + '" comment="Minimum rhop valid (default=700)" units_comment="kg/m^3" />\n')
    f.write('\t\t\t<parameter key="RhopOutMax" value="' +
            str(data['rhopoutmax']) + '" comment="Maximum rhop valid (default=1300)" units_comment="kg/m^3" />\n')
    if data['period_x'][0]:
        if data['3dmode']:
            f.write('\t\t\t<parameter key="XPeriodicIncY" value="' +
                    str(data['period_x'][2]) + '"/>\n')
        f.write('\t\t\t<parameter key="XPeriodicIncZ" value="' +
                str(data['period_x'][3]) + '"/>\n')
    if data['period_y'][0] and data['3dmode']:
        f.write('\t\t\t<parameter key="YPeriodicIncX" value="' +
                str(data['period_y'][1]) + '"/>\n')
        f.write('\t\t\t<parameter key="YPeriodicIncZ" value="' +
                str(data['period_y'][3]) + '"/>\n')
    if data['period_z'][0]:
        f.write('\t\t\t<parameter key="ZPeriodicIncX" value="' +
                str(data['period_z'][1]) + '"/>\n')
        if data['3dmode']:
            f.write('\t\t\t<parameter key="ZPeriodicIncY" value="' +
                    str(data['period_z'][2]) + '"/>\n')
    if data['domainfixed'].enabled and not data['simdomain_chk']:
        f.write(
            '\t\t\t<parameter key="DomainFixedXmin" value="{}" comment="The domain is fixed in the specified limit (default=not applied)" units_comment="metres (m)" />\n'.format(
                data['domainfixed'].xmin))
        f.write(
            '\t\t\t<parameter key="DomainFixedXmax" value="{}" comment="The domain is fixed in the specified limit (default=not applied)" units_comment="metres (m)" />\n'.format(
                data['domainfixed'].xmax))
        f.write(
            '\t\t\t<parameter key="DomainFixedYmin" value="{}" comment="The domain is fixed in the specified limit (default=not applied)" units_comment="metres (m)" />\n'.format(
                data['domainfixed'].ymin))
        f.write(
            '\t\t\t<parameter key="DomainFixedYmax" value="{}" comment="The domain is fixed in the specified limit (default=not applied)" units_comment="metres (m)" />\n'.format(
                data['domainfixed'].ymax))
        f.write(
            '\t\t\t<parameter key="DomainFixedZmin" value="{}" comment="The domain is fixed in the specified limit (default=not applied)" units_comment="metres (m)" />\n'.format(
                data['domainfixed'].zmin))
        f.write(
            '\t\t\t<parameter key="DomainFixedZmax" value="{}" comment="The domain is fixed in the specified limit (default=not applied)" units_comment="metres (m)" />\n'.format(
                data['domainfixed'].zmax))
    if data['simdomain_chk']:
        f.write(
            '\t\t\t<simulationdomain comment="Defines domain of simulation (default=Uses minimum and maximum position of the generated particles)" >\n'
        )
        f.write(
            '\t\t\t\t<posmin x="{}" y="{}" z="{}" comment="e.g.: x=0.5, y=default-1, z=default-10%" />\n'.format(
                data['posminxml'][0], data['posminxml'][1], data['posminxml'][2]
            )
        )
        f.write(
            '\t\t\t\t<posmax x="{}" y="{}" z="{}"/>\n'.format(
                data['posmaxxml'][0], data['posmaxxml'][1], data['posmaxxml'][2]
            )
        )
        f.write(
            '\t\t\t</simulationdomain>\n'
        )

    f.write('\t\t</parameters>\n')
    f.write('\t</execution>\n')
    f.write('</case>\n')
    f.close()
