#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Utils.

This file contains a collection of constants and
functions meant to use with DesignSPHysics.

This module stores non-gui related operations, but
meant to use with FreeCAD.

"""

import FreeCAD
import FreeCADGui
import Mesh
import Fem
import Draft
import math
import os
import pickle
import random
import tempfile
import traceback
import webbrowser
import json
import shutil
from sys import platform
from datetime import datetime
from femmesh.femmesh2mesh import femmesh_2_mesh

import sys

from PySide import QtGui, QtCore
from ds_modules import guiutils
from ds_modules import execution_parameters
from ds_modules import properties
from ds_modules.properties import *
from ds_modules.execution_parameters import *


"""
Copyright (C) 2019
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DesignSPHysics.

DesignSPHysics is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DesignSPHysics is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.
"""

# ------ CONSTANTS DEFINITION ------
FREECAD_MIN_VERSION = "018"
APP_NAME = "DesignSPHysics"
DEBUGGING = True
VERBOSE = True
DIVIDER = 1000
PICKLE_PROTOCOL = 1  # Binary mode
VERSION = "0.5.1.1907-29"
WIDTH_2D = 0.001
MAX_PARTICLE_WARNING = 2000000
HELP_WEBPAGE = "https://github.com/DualSPHysics/DesignSPHysics/wiki"
DISK_DUMP_FILE_NAME = "designsphysics-{}.log".format(VERSION)


# ------ END CONSTANTS DEFINITION ------

def is_compatible_version():
    """ Checks if the current FreeCAD version is suitable
        for this macro. """

    version_num = FreeCAD.Version()[0] + FreeCAD.Version()[1]
    if float(version_num) < float(FREECAD_MIN_VERSION):
        guiutils.warning_dialog("This version of FreeCAD is not supported!. Install version 0.17 or higher.")
        return False
    else:
        return True


def log(message):
    """ Prints a log in the default output."""
    if VERBOSE:
        print ("[" + APP_NAME + "]" + message)


def warning(message):
    """ Prints a warning in the default output. """
    if VERBOSE:
        print ("[" + APP_NAME + "] " + "[WARNING]" + ": " + str(message))


def error(message):
    """ Prints an error in the default output."""
    if VERBOSE:
        print ("[" + APP_NAME + "] " + "[ERROR]" + ": " + str(message))


def debug(message):
    """ Prints a debug message in the default output"""
    if DEBUGGING and VERBOSE:
        print ("[" + APP_NAME + "] " + "[<<<<DEBUG>>>>]" + ": " + str(message))

def dump_to_disk(text):
    """ Dumps text content into a file on disk """
    with open('/tmp/{}'.format(DISK_DUMP_FILE_NAME), 'w') as error_dump:
        error_dump.write(text)


def __(text):
    """ Translation helper. Takes a string and tries to return its translation to the current FreeCAD locale.
    If the translation is missing or the file does not exists, return default english string. """
    # Get FreeCAD current language
    freecad_locale = FreeCADGui.getLocale().lower().replace(", ", "-").replace(" ", "-")
    # Find ds_modules directory
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    # Open translation file and print the matching string, if it's defined.
    filename = "{utils_dir}/lang/{locale}.json".format(utils_dir=utils_dir, locale=freecad_locale)
    if not os.path.isfile(filename):
        filename = "{utils_dir}/lang/{locale}.json".format(utils_dir=utils_dir, locale="english")
    with open(filename, "rb") as f:
        translation = json.load(f)
    # Tries to return the translation. It it does not exist, creates it
    to_ret = translation.get(text, None)
    if not to_ret:
        translation[text] = text
        with open(filename, "w", encoding="utf8") as f:
            json.dump(translation, f, indent=4)
        return text
    else:
        return to_ret


def refocus_cwd():
    """ Ensures the current working directory is the DesignSPHysics folder """
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(utils_dir + "/..")


def check_executables(data):
    """ Checks the different executables used by DesignSPHysics. Returns the filtered data structure and a boolean
    stating if all went correctly. """
    execs_correct = True

    # Make sure the current working directory is the DesignSPHysics folder
    refocus_cwd()

    # Tries to identify gencase
    if os.path.isfile(data['gencase_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['gencase_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "gencase" in output.lower():
            log("Found correct GenCase.")
        else:
            debug('Execution of gencase did not find correct gencase')
            execs_correct = False
            data['gencase_path'] = ""
    else:
        debug('Path not found for gencase')
        execs_correct = False
        data['gencase_path'] = ""

    # Tries to identify dualsphysics
    if os.path.isfile(data['dsphysics_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        if platform == "linux" or platform == "linux2":
            os.environ["LD_LIBRARY_PATH"] = "/".join(data['dsphysics_path'].split("/")[:-1])
            process.start('"{}"'.format(data['dsphysics_path']))
        else:
            process.start('"{}"'.format(data['dsphysics_path']))

        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "dualsphysics" in output.lower():
            log("Found correct DualSPHysics.")
        else:
            execs_correct = False
            data['dsphysics_path'] = ""
    else:
        execs_correct = False
        data['dsphysics_path'] = ""

    # Tries to identify partvtk4
    if os.path.isfile(data['partvtk4_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['partvtk4_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "partvtk4" in output.lower():
            log("Found correct PartVTK4.")
        else:
            execs_correct = False
            data['partvtk4_path'] = ""
    else:
        execs_correct = False
        data['partvtk4_path'] = ""

    # Tries to identify computeforces
    if os.path.isfile(data['computeforces_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['computeforces_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "computeforces" in output.lower():
            log("Found correct ComputeForces.")
        else:
            execs_correct = False
            data['computeforces_path'] = ""
    else:
        execs_correct = False
        data['computeforces_path'] = ""

    # Tries to identify floatinginfo
    if os.path.isfile(data['floatinginfo_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['floatinginfo_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "floatinginfo" in output.lower():
            log("Found correct FloatingInfo.")
        else:
            execs_correct = False
            data['floatinginfo_path'] = ""
    else:
        execs_correct = False
        data['floatinginfo_path'] = ""

    # Tries to identify measuretool
    if os.path.isfile(data['measuretool_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['measuretool_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "measuretool" in output.lower():
            log("Found correct MeasureTool.")
        else:
            execs_correct = False
            data['measuretool_path'] = ""
    else:
        execs_correct = False
        data['measuretool_path'] = ""

    # Tries to identify isosurface
    if os.path.isfile(data['isosurface_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['isosurface_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "isosurface" in output.lower():
            log("Found correct IsoSurface.")
        else:
            execs_correct = False
            data['isosurface_path'] = ""
    else:
        execs_correct = False
        data['isosurface_path'] = ""

    # Tries to identify boundaryvtk
    if os.path.isfile(data['boundaryvtk_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['boundaryvtk_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "boundaryvtk" in output.lower():
            log("Found correct BoundaryVTK.")
        else:
            execs_correct = False
            data['boundaryvtk_path'] = ""
    else:
        execs_correct = False
        data['boundaryvtk_path'] = ""

    # Tries to identify flowtool
    if os.path.isfile(data['flowtool_path']):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start('"{}"'.format(data['flowtool_path']))
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "flowtool" in output.lower():
            log("Found correct FlowTool.")
        else:
            execs_correct = False
            data['flowtool_path'] = ""
    else:
        execs_correct = False
        data['flowtool_path'] = ""

    if not execs_correct:
        bundled_execs_present = are_executables_bundled()

        if bundled_execs_present:
            user_selection = guiutils.ok_cancel_dialog(APP_NAME,
                                                       "The path of some of the executables "
                                                       "in “Setup Plugin” is not correct.\n"
                                                       "DualSPHysics was detected. "
                                                       "Do you want to load the default configuration?")
            if user_selection == QtGui.QMessageBox.Ok:
                # Auto-fill executables.
                filled_data = get_default_config_file()
                data.update(filled_data)
                return data, execs_correct
            else:
                return data, execs_correct
        else:
            # Spawn warning dialog and return filtered data.
            if not execs_correct:
                warning("One or more of the executables in the setup is not correct. "
                        "Check plugin setup to fix missing binaries")
                ds_modules.guiutils.warning_dialog("One or more of the executables in the setup is not correct. "
                                        "Check plugin setup to fix missing binaries.")
    return data, execs_correct


def are_executables_bundled():
    """ Returns if the DualSPHysics executable directory exists"""
    dsph_execs_path = os.path.dirname(os.path.realpath(__file__)) + "/../dualsphysics/bin/"
    return os.path.isdir(dsph_execs_path)


def float_list_to_float_property(floating_mks):
    """ Transforms a float lists from an old case format to the new properties. """
    to_ret = dict()
    for key, value in floating_mks.items():
        if isinstance(value, list):
            # Is in old mode. Change to OOP
            fp = FloatProperty(
                mk=float(key),
                mass_density_type=int(value[0][0]),
                mass_density_value=float(value[0][1])
            )
            if not value[1][0]:  # Gravity center is not auto
                fp.gravity_center = value[1][1:]
            if not value[2][0]:  # Inertia is not auto
                fp.inertia = value[2][1:]
            if not value[3][0]:  # Initial linear velocity is not auto
                fp.initial_linear_velocity = value[3][1:]
            if not value[4][0]:  # Initial angular velocity is not auto
                fp.initial_angular_velocity = value[4][1:]

            to_ret[key] = fp

        # Adds the new element (empty) if not exists
        elif isinstance(value, object):
            try:
                translation = value.translation_restriction
            except AttributeError:
                translation = list()

            try:
                rotation = value.rotation_restriction
            except AttributeError:
                rotation = list()

            try:
                material = value.material
            except AttributeError:
                material = ""

            fp = FloatProperty(
                mk=float(key),
                mass_density_type=value.mass_density_type,
                mass_density_value=value.mass_density_value,
                gravity_center=value.gravity_center,
                inertia=value.inertia,
                initial_linear_velocity=value.initial_linear_velocity,
                initial_angular_velocity=value.initial_angular_velocity,
                translation_restriction=translation,
                rotation_restriction=rotation,
                material=material
            )

            to_ret[key] = fp

        else:
            # Is in OOP mode, appending
            to_ret[key] = value

    return to_ret


def initials_list_to_initials_property(initials_mks):
    """ Transforms initials lists to properties from old cases. """
    to_ret = dict()
    for key, value in initials_mks.items():
        if isinstance(value, list):
            # Is in old mode. Change to OOP
            ip = InitialsProperty(mk=int(key), force=value)
            to_ret[key] = ip
        else:
            # Is in OOP mode, appending
            to_ret[key] = value
    return to_ret


def get_maximum_particles(dp):
    """ Gets the maximum number of particles that can be in the Case Limits with the given DP """
    to_ret = get_fc_object('Case_Limits').Width.Value / (dp * 1000)
    to_ret *= get_fc_object('Case_Limits').Height.Value / (dp * 1000)
    to_ret *= get_fc_object('Case_Limits').Length.Value / (dp * 1000)

    return int(to_ret)


def get_default_data():
    """ Sets default data at start of the macro.
        Returns data and temp_data dict with default values.
        If there is data saved on disk, tries to load it. """

    # TODO: Big change. These should be data objects, not dict()
    data = dict()
    temp_data = dict()

    # Data relative to constant definition
    # TODO: These should be aggregated into an object like CaseConstants()
    data['lattice_bound'] = 1
    data['lattice_fluid'] = 1
    data['gravity'] = [0, 0, -9.81]
    data['rhop0'] = 1000
    data['hswl'] = 0
    data['hswl_auto'] = True
    data['gamma'] = 7
    data['speedsystem'] = 0
    data['speedsystem_auto'] = True
    data['coefsound'] = 20
    data['speedsound'] = 0
    data['speedsound_auto'] = True
    data['coefh'] = 1
    data['cflnumber'] = 0.2
    data['h'] = 0
    data['h_auto'] = True
    data['b'] = 0
    data['b_auto'] = True
    data['massbound'] = 0
    data['massbound_auto'] = True
    data['massfluid'] = 0
    data['massfluid_auto'] = True

    # TODO: This should be aggregated into an object like CaseGeometryDefinition()
    data['dp'] = 0.01

    # Data relative to execution parameters
    # TODO: These should be aggregated into an object like CaseExecutionParameters()
    data['posdouble'] = 0
    data['stepalgorithm'] = 1
    data['verletsteps'] = 40
    data['kernel'] = 2
    data['viscotreatment'] = 1
    data['visco'] = 0.01
    data['viscoboundfactor'] = 1
    data['deltasph'] = 0
    data['deltasph_en'] = 0
    data['shifting'] = 0
    data['shiftcoef'] = -2
    data['shifttfs'] = 0
    data['rigidalgorithm'] = 1
    data['ftpause'] = 0.0
    data['coefdtmin'] = 0.05
    data['dtini'] = 0.0001
    data['dtini_auto'] = True
    data['dtmin'] = 0.00001
    data['dtmin_auto'] = True
    data['dtfixed'] = "DtFixed.dat"
    data['dtallparticles'] = 0
    data['timemax'] = 1.5
    data['timeout'] = 0.01
    data['incz'] = 0
    data['partsoutmax'] = 1
    data['rhopoutmin'] = 700
    data['rhopoutmax'] = 1300
    data['domainfixed'] = execution_parameters.DomainFixedParameter(False, 0, 0, 0, 0, 0, 0)

    # Damping object dictionary: {'ObjectName': DampingObject}
    data['damping'] = dict()

    # Periodicity data [enabled, x_inc, y_inc, z_inc]
    data['period_x'] = [False, 0.0, 0.0, 0.0]
    data['period_y'] = [False, 0.0, 0.0, 0.0]
    data['period_z'] = [False, 0.0, 0.0, 0.0]

    # Simulation domain [0=default, x_value, 0=default, y_value, 0=default, z_value]
    data['simdomain_chk'] = False
    data['posmin'] = [0, 0.0, 0, 0.0, 0, 0.0]
    data['posminxml'] = ['', '', '']
    data['posmax'] = [0, 0.0, 0, 0.0, 0, 0.0]
    data['posmaxxml'] = ['', '', '']

    # Stores paths to executables
    # TODO: These should be aggregated into an object like ExecutablePaths()
    data['gencase_path'] = ""
    data['dsphysics_path'] = ""
    data['partvtk4_path'] = ""
    data['floatinginfo_path'] = ""
    data['computeforces_path'] = ""
    data['measuretool_path'] = ""
    data['isosurface_path'] = ""
    data['boundaryvtk_path'] = ""
    data['flowtool_path'] = ""
    data['paraview_path'] = ""

    # Case mode
    data['3dmode'] = True

    # Stores project path and name for future script needs
    data['project_path'] = ""
    data['project_name'] = ""
    data['total_particles'] = -1
    data['total_particles_out'] = 0
    data['additional_parameters'] = ""
    data['export_options'] = ""
    data['mkboundused'] = []
    data['mkfluidused'] = []

    # Dictionary that defines floatings.
    # Structure: {mk: FloatProperty}
    data['floating_mks'] = dict()

    # Dictionary that defines initials.
    # Keys are mks enabled (ONLY FLUIDS) and values are a list containing: {'mkfluid': InitialsProperty()}
    data['initials_mks'] = dict()

    # Control data for enabling features
    data['gencase_done'] = False
    data['simulation_done'] = False

    # Last generated number of particles
    data['last_number_particles'] = -1

    # Simulation objects with its parameters (Without order).
    # The format is: {'key': ['mk', 'type', 'fill']}
    data['simobjects'] = dict()

    # Keys of simobjects (Ordered).
    data['export_order'] = []

    # Global movement list.
    # It stores all the movements created in this case.
    data['global_movements'] = list()

    # Global property list.
    # It stores all the properties created in this case.
    data['global_properties'] = list()

    # Object movement mapping.
    # Dictionary with a list of movements attached. {'mkgroup': [movement1, movement2, ...]}
    data['motion_mks'] = dict()

    # Post-processing info
    # FlowTool Boxes: [ [id, "name", x1, x2,..., x8], ... ]
    # id is an UUID
    data['flowtool_boxes'] = list()

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

    # INLET/OUTLET objects
    #[id, convertfluid, layers, [zone2/3D, mk, direction], [velocity, value], [density, value], [elevation,zbottom, zsurf]]
    data['inlet_zone'] = list()
    #[reuseids, resizetime, userefilling, determlimit]
    data['inlet_object'] = [0, 0.5, 0, 0]

    # Faces objects
    data['faces'] = dict()

    # GEO autofill. {name: true/false}
    data['geo_autofill'] = dict()

    # Geometry original filetypes. Helps to write original filetype on gencase
    data["import_geo_filetypes"] = dict()

    # MultiLayer Pistons: {mk: MLPistonObject}
    data['mlayerpistons'] = dict()

    # Relaxation zones for the case. Can only set one. None means no RZ is set
    data['relaxationzone'] = None

    # Acceleration Input
    data['accinput'] = properties.AccelerationInput()

    # Temporal data dict to control execution features.
    temp_data['current_process'] = None
    temp_data['stored_selection'] = []
    temp_data['current_info_dialog'] = None
    temp_data['widget_saver'] = None
    temp_data['export_numparts'] = ""
    temp_data['total_export_parts'] = -1
    temp_data['measuretool_points'] = list()
    temp_data['measuretool_grid'] = list()
    temp_data['current_output'] = ""
    temp_data['supported_types'] = ["Part::Box", "Part::Sphere", "Part::Cylinder"]

    # Try to load saved paths. This way the user does not need
    # to introduce the software paths every time
    if os.path.isfile(FreeCAD.getUserAppDataDir() + '/dsph_data-{}.dsphdata'.format(VERSION)):
        try:
            with open(FreeCAD.getUserAppDataDir() + '/dsph_data-{}.dsphdata'.format(VERSION), 'rb') as picklefile:
                log("Found data file. Loading data from disk.")
                disk_data = pickle.load(picklefile)
                data['gencase_path'] = disk_data['gencase_path']
                data['dsphysics_path'] = disk_data['dsphysics_path']
                data['partvtk4_path'] = disk_data['partvtk4_path']
                data['computeforces_path'] = disk_data['computeforces_path']
                data['floatinginfo_path'] = disk_data['floatinginfo_path']
                data['measuretool_path'] = disk_data['measuretool_path']
                data['isosurface_path'] = disk_data['isosurface_path']
                data['boundaryvtk_path'] = disk_data['boundaryvtk_path']
                data['flowtool_path'] = disk_data['flowtool_path']
                data['paraview_path'] = disk_data['paraview_path']

        except Exception:
            warning(__("The main settings file is corrupted. Deleting..."))
            os.remove(picklefile.name)
            data['gencase_path'] = ""
            data['dsphysics_path'] = ""
            data['partvtk4_path'] = ""
            data['computeforces_path'] = ""
            data['floatinginfo_path'] = ""
            data['measuretool_path'] = ""
            data['isosurface_path'] = ""
            data['boundaryvtk_path'] = ""
            data['flowtool_path'] = ""
            data['paraview_path'] = ""
            data.update(get_default_config_file())

        data, state = check_executables(data)
        with open(FreeCAD.getUserAppDataDir() + '/dsph_data-{}.dsphdata'.format(VERSION), 'wb') as picklefile:
            pickle.dump(data, picklefile, PICKLE_PROTOCOL)
    else:
        # Settings file not created. Merging with default one inf default-config.json
        data["project_path"] = ""
        data["project_name"] = ""
        data.update(get_default_config_file())

    return data, temp_data


def get_default_config_file():
    """ Gets the default-config.json from disk """
    current_script_folder = os.path.dirname(os.path.realpath(__file__))
    with open('{}/../default-config.json'.format(current_script_folder)) as data_file:
        loaded_data = json.load(data_file)

    if "win" in get_os():
        to_ret = loaded_data["windows"]
    elif "linux" in get_os():
        to_ret = loaded_data["linux"]

    return to_ret


def get_first_mk_not_used(objtype, data):
    """ Checks simulation objects to find the first not used
        MK group. """

    if objtype == "fluid":
        endval = 10
        mkset = set()
        for key, value in data["simobjects"].items():
            if value[1].lower() == "fluid":
                mkset.add(value[0])
    else:
        endval = 240
        mkset = set()
        for key, value in data["simobjects"].items():
            if value[1].lower() == "bound":
                mkset.add(value[0])
    for i in range(0, endval):
        if i not in mkset:
            return i


def open_help():
    """ Opens a web browser with this software help. """
    webbrowser.open(HELP_WEBPAGE)


def get_os():
    """ Returns the current operating system """
    return platform


def print_license():
    """ Prints this software license. """
    licpath = "{}{}".format(os.path.abspath(__file__).split("ds_modules")[0], "LICENSE")
    if os.path.isfile(licpath):
        with open(licpath) as licfile:
            if VERBOSE:
                print (licfile.read())
    else:
        raise EnvironmentError(
            "LICENSE file could not be found. Are you sure you didn't delete it?")


def prompt_close_all_documents(prompt=True):
    """ Shows a dialog to close all the current documents.
        If accepted, close all the current documents and return True, else returns False. """
    if prompt:
        user_selection = guiutils.ok_cancel_dialog(
            APP_NAME, "All documents will be closed")
    if not prompt or user_selection == QtGui.QMessageBox.Ok:
        # Close all current documents.
        log("Closing all current documents")
        for doc in FreeCAD.listDocuments().keys():
            FreeCAD.closeDocument(doc)
        return True
    else:
        return False


def document_count():
    """ Returns an integer representing the number of current opened documents in FreeCAD. """
    return len(FreeCAD.listDocuments().keys())


def valid_document_environment():
    """ Returns a boolean if a correct document environment is found.
    A correct document environment is defined if only a DSPH_Case document is currently opened in FreeCAD. """
    return True if document_count() is 1 and 'dsph_case' in list(FreeCAD.listDocuments().keys())[0].lower() else False


def create_dsph_document():
    """ Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. """
    FreeCAD.newDocument("DSPH_Case")
    FreeCAD.setActiveDocument("DSPH_Case")
    FreeCAD.ActiveDocument = FreeCAD.getDocument("DSPH_Case")
    FreeCADGui.ActiveDocument = FreeCADGui.getDocument("DSPH_Case")
    FreeCADGui.activateWorkbench("PartWorkbench")
    FreeCADGui.activeDocument().activeView().viewAxonometric()
    FreeCAD.ActiveDocument.addObject("Part::Box", "Case_Limits")
    FreeCAD.ActiveDocument.getObject("Case_Limits").Label = "Case Limits (3D)"
    FreeCAD.ActiveDocument.getObject("Case_Limits").Length = '1000 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Width = '1000 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Height = '1000 mm'
    FreeCADGui.ActiveDocument.getObject("Case_Limits").DisplayMode = "Wireframe"
    FreeCADGui.ActiveDocument.getObject("Case_Limits").LineColor = (1.00, 0.00, 0.00)
    FreeCADGui.ActiveDocument.getObject("Case_Limits").LineWidth = 2.00
    FreeCADGui.ActiveDocument.getObject("Case_Limits").Selectable = False

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def create_dsph_document_from_fcstd(document_path):
    """ Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. """
    temp_document_path = tempfile.gettempdir() + "/" + "DSPH_Case.fcstd"
    shutil.copyfile(document_path, temp_document_path)
    FreeCAD.open(temp_document_path)
    FreeCAD.setActiveDocument("DSPH_Case")
    FreeCAD.ActiveDocument = FreeCAD.getDocument("DSPH_Case")
    FreeCADGui.ActiveDocument = FreeCADGui.getDocument("DSPH_Case")
    FreeCADGui.activateWorkbench("PartWorkbench")
    FreeCADGui.activeDocument().activeView().viewAxonometric()
    FreeCAD.ActiveDocument.addObject("Part::Box", "Case_Limits")
    FreeCAD.ActiveDocument.getObject("Case_Limits").Label = "Case Limits (3D)"
    FreeCAD.ActiveDocument.getObject("Case_Limits").Length = '1000 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Width = '1000 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Height = '1000 mm'
    FreeCADGui.ActiveDocument.getObject("Case_Limits").DisplayMode = "Wireframe"
    FreeCADGui.ActiveDocument.getObject("Case_Limits").LineColor = (1.00, 0.00, 0.00)
    FreeCADGui.ActiveDocument.getObject("Case_Limits").LineWidth = 2.00
    FreeCADGui.ActiveDocument.getObject("Case_Limits").Selectable = False

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


def dump_to_xml(data, save_name):
    """ Saves all of the data in the opened case
        to disk. Generates a GenCase compatible XML. """
    # Saves all the data in XML format.
    log("Saving data in " + data["project_path"] + ".")
    FreeCAD.getDocument("DSPH_Case").saveAs(save_name + "/DSPH_Case.FCStd")
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
    f.write('\t\t\t\t\t<setshapemode>actual | dp | bound</setshapemode>\n')
    # Export in strict order
    for key in data["export_order"]:
        name = key
        valuelist = data["simobjects"][name]
        o = FreeCAD.getDocument("DSPH_Case").getObject(name)
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
            if o.TypeId == "Part::Box":
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
            elif o.TypeId == "Part::Sphere":
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
            elif o.TypeId == "Part::Cylinder":
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
                if o.TypeId == "App::DocumentObjectGroup" and "fillbox" in o.Name.lower():
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
                    if o.Name in data["import_geo_filetypes"].keys():
                        if data["import_geo_filetypes"][o.Name] == ".stl":
                            stl_file_path = save_name + "/" + o.Name + ".stl"
                            Mesh.export(__objs__, stl_file_path)
                            relative_file_path = os.path.relpath(
                                stl_file_path,
                                os.path.dirname(os.path.abspath(stl_file_path))
                            )
                            autofill_enabled = str(data["geo_autofill"][o.Name] if o.Name in data["geo_autofill"].keys() else False).lower()
                            f.write('\t\t\t\t\t<drawfilestl file="{}" objname="{}" autofill="{}">\n'.format(relative_file_path, o.Label, autofill_enabled))
                            f.write('\t\t\t\t\t\t<drawscale x="0.001" y="0.001" z="0.001" />\n')
                            f.write('\t\t\t\t\t</drawfilestl>\n')
                        elif data["import_geo_filetypes"][o.Name] == ".ply":
                            ply_file_path = save_name + "/" + o.Name + ".ply"
                            Mesh.export(__objs__, ply_file_path)
                            relative_file_path = os.path.relpath(
                                ply_file_path,
                                os.path.dirname(os.path.abspath(ply_file_path))
                            )
                            autofill_enabled = str(data["geo_autofill"][o.Name] if o.Name in data["geo_autofill"].keys() else False).lower()
                            f.write('\t\t\t\t\t<drawfileply file="{}" objname="{}" autofill="{}">\n'.format(relative_file_path, o.Label, autofill_enabled))
                            f.write('\t\t\t\t\t\t<drawscale x="0.001" y="0.001" z="0.001" />\n')
                            f.write('\t\t\t\t\t</drawfileply>\n')
                        elif data["import_geo_filetypes"][o.Name] == ".vtk":
                            vtk_file_path = save_name + "/" + o.Name + ".vtk"
                            Fem.export(__objs__, vtk_file_path)
                            relative_file_path = os.path.relpath(
                                vtk_file_path,
                                os.path.dirname(os.path.abspath(vtk_file_path))
                            )
                            autofill_enabled = str(data["geo_autofill"][o.Name] if o.Name in data["geo_autofill"].keys() else False).lower()
                            f.write('\t\t\t\t\t<drawfilevtk file="{}" objname="{}" autofill="{}">\n'.format(relative_file_path, o.Label, autofill_enabled))
                            f.write('\t\t\t\t\t\t<drawscale x="0.001" y="0.001" z="0.001" />\n')
                            f.write('\t\t\t\t\t</drawfilevtk>\n')
                    else:
                        stl_file_path = save_name + "/" + o.Name + ".stl"
                        Mesh.export(__objs__, stl_file_path)
                        relative_file_path = os.path.relpath(
                            stl_file_path,
                            os.path.dirname(os.path.abspath(stl_file_path))
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
            if value.initials_type == 0:
                f.write('\t\t\t<velocity mkfluid="{}">\n'.format(value.mk))
                f.write('\t\t\t\t<direction x="{}" y="{}" z="{}" />\n'.format(*value.direction))
                f.write('\t\t\t\t<velocity v="{}" comment="Uniform profile velocity" units_comment="m/s" />\n'.format(value.v1))
                f.write('\t\t\t</velocity>\n')
            elif value.initials_type == 1:
                f.write('\t\t\t<velocity mkfluid="{}">\n'.format(value.mk))
                f.write('\t\t\t\t<direction x="{}" y="{}" z="{}" />\n'.format(*value.direction))
                f.write('\t\t\t\t<velocity2 v="{}" v2="{}" z="{}" z2="{}" comment="Linear profile velocity" units_comment="m/s" />\n'.format(value.v1, value.v2, value.z1, value.z2))
                f.write('\t\t\t</velocity>\n')
            elif value.initials_type == 2:
                f.write('\t\t\t<velocity mkfluid="{}">\n'.format(value.mk))
                f.write('\t\t\t\t<direction x="{}" y="{}" z="{}" />\n'.format(*value.direction))
                f.write('\t\t\t\t<velocity3 v="{}" v2="{}" v3="{}" z="{}" z2="{}" z3="{}" comment="Parabolic profile velocity" units_comment="m/s" />\n'.format(
                        value.v1, value.v2, value.v3, value.z1, value.z2, value.z3
                    ))
                f.write('\t\t\t</velocity>\n')
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
                elif isinstance(movement, properties.SpecialMovement):
                    if isinstance(movement.generator, properties.FileGen):
                        f.write('\t\t\t\t<mvfile id="{}" duration="{}">\n '.format(
                            mov_counter, movement.generator.duration))
                        f.write('\t\t\t\t\t<file name="{}" fields="{}" fieldtime="{}" '
                                'fieldx="{}" fieldy="{}" />\n '.format(movement.generator.filename,
                                                                       movement.generator.fields,
                                                                       movement.generator.fieldtime,
                                                                       movement.generator.fieldx,
                                                                       movement.generator.fieldy))
                        f.write('\t\t\t\t</mvfile>\n ')
                    elif isinstance(movement.generator, properties.RotationFileGen):
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
            if ll[1] != "":
                if ll[2] == "":
                    f.write(
                        '\t\t\t\t<link_linearspring idbody1="{}">\n'.format(str(ll[1]))
                    )
                else:
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
            if lh[1] != "":
                if lh[2] == "":
                    f.write(
                        '\t\t\t\t<link_hinge idbody1="{}">\n'.format(str(lh[1]))
                    )
                else:
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
                    '\t\t\t\t\t<damping   value="10" comment="Torsional damping [-]" />\n'.format(lh[6])
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
        if isinstance(motlist[0], properties.SpecialMovement):
            mot = motlist[0].generator
            if isinstance(mot, properties.FileGen) or isinstance(mot, properties.RotationFileGen):
                continue

            # Open tags only for the first movement
            if written_movements_counter == 0:
                f.write('\t\t\t<wavepaddles>\n')

            if isinstance(mot, properties.RegularPistonWaveGen):
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

            elif isinstance(mot, properties.IrregularPistonWaveGen):
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

            elif isinstance(mot, properties.RegularFlapWaveGen):
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

            elif isinstance(mot, properties.IrregularFlapWaveGen):
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
                '\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in funtion for velocity (def. psi=0.9, beta=1)" />\n'.format(
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
                '\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in funtion for velocity (def. psi=0.9, beta=1)" />\n'.format(
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
                '\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in funtion for velocity (def. psi=0.9, beta=1)" />\n'.format(
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
            f.write('\t\t\t\t\t<function psi="{}" beta="{}" comment="Coefficients in funtion for velocity (def. psi=0.9, beta=1)" />\n'.format(str(rzobject.function_psi), str(rzobject.function_beta)))
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
            '\t\t\t<simulationdomain comment="Defines domain of simulation (default=Uses minimun and maximum position of the generated particles)" >\n'
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
    else:
        f.write('\t\t\t<simulationdomain comment="Defines domain of simulation (default=Uses minimun and maximum position of the generated particles)">\n')
        f.write('\t\t\t\t<posmin x="default" y="default" z="default" comment="e.g.: x=0.5, y=default-1, z=default-10%" />\n')
        f.write('\t\t\t\t<posmax x="default" y="default" z="default + 50%" />\n')
        f.write('\t\t\t</simulationdomain>\n')


    f.write('\t\t</parameters>\n')
    f.write('\t</execution>\n')
    f.write('</case>\n')
    f.close()


def get_number_of_documents():
    """ Returns the number of documents currently
    opened in FreeCAD. """
    return len(FreeCAD.listDocuments())


def batch_generator(full_path, case_name, gcpath, dsphpath, pvtkpath, exec_params, lib_path):
    """ Loads a windows & linux template for batch files and saves them formatted to disk. """
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    with open('{}/templates/template.bat'.format(lib_folder), 'r') as content_file:
        win_template = content_file.read().format(
            app_name=APP_NAME, case_name=case_name, gcpath=gcpath, dsphpath=dsphpath, pvtkpath=pvtkpath,
            exec_params=exec_params)
    with open('{}/templates/template.sh'.format(lib_folder), 'r') as content_file:
        linux_template = content_file.read().format(
            app_name=APP_NAME,
            case_name=case_name,
            gcpath=gcpath,
            dsphpath=dsphpath,
            pvtkpath=pvtkpath,
            exec_params=exec_params,
            lib_path=lib_path,
            name="name"
        )

    with open(full_path + "/run.bat", 'w') as bat_file:
        log(__("Creating ") + full_path + "/run.bat")
        bat_file.write(win_template)
    with open(full_path + "/run.sh", 'w') as bat_file:
        log(__("Creating ") + full_path + "/run.sh")
        bat_file.write(linux_template)


def import_geo(filename=None, scale_x=1, scale_y=1, scale_z=1, name=None, autofill=False, data=None):
    """ Opens a GEO file, preprocesses it and saves it
    int temp files to load with FreeCAD. """
    if data == None:
        raise RuntimeError("Data parameter must be populated")
    length_filename = len(filename)
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

    data["geo_autofill"][name] = autofill
    data["import_geo_filetypes"][name] = str(file_type).lower()


def get_fc_object(internal_name):
    """ Returns a FreeCAD internal object by a name. """
    return FreeCAD.getDocument("DSPH_Case").getObject(internal_name)


def create_flowtool_boxes(path, boxes):
    """ Creates a file with flowtool box information """
    with open(path, 'w') as f:
        for box in boxes:
            f.write("BOX @{}\n".format(box[1]))
            f.write("{} {} {}\n".format(*box[2]))
            f.write("{} {} {}\n".format(*box[3]))
            f.write("{} {} {}\n".format(*box[4]))
            f.write("{} {} {}\n".format(*box[5]))
            f.write("{} {} {}\n".format(*box[6]))
            f.write("{} {} {}\n".format(*box[7]))
            f.write("{} {} {}\n".format(*box[8]))
            f.write("{} {} {}\n".format(*box[9]))
            f.write("\n")
