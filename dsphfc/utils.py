#!/usr/bin/env python2.7
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
import Draft
import math
import os
import pickle
import random
import tempfile
import traceback
import webbrowser
import json
from sys import platform
from datetime import datetime

from PySide import QtGui, QtCore

import guiutils
import stl
from properties import *
"""
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
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
FREECAD_MIN_VERSION = "016"
APP_NAME = "DesignSPHysics"
DEBUGGING = True
DIVIDER = 1000
PICKLE_PROTOCOL = 1  # Binary mode
VERSION = "0.4.1711-09-workshop"
WIDTH_2D = 0.001
MAX_PARTICLE_WARNING = 2000000

# ------ END CONSTANTS DEFINITION ------


def is_compatible_version():
    """ Checks if the current FreeCAD version is suitable
        for this macro. """

    version_num = FreeCAD.Version()[0] + FreeCAD.Version()[1]
    if int(version_num) < int(FREECAD_MIN_VERSION):
        guiutils.warning_dialog("This version of FreeCAD is not supported!. Install version 0.16 or higher.")
        return False
    else:
        return True


def log(message):
    print "[" + APP_NAME + "] " + message.encode('utf-8')


def warning(message):
    print "[" + APP_NAME + "] " + "[WARNING]" + ": " + str(message)


def error(message):
    print "[" + APP_NAME + "] " + "[ERROR]" + ": " + str(message)


def debug(message):
    if DEBUGGING:
        print "[" + APP_NAME + "] " + "[<<<<DEBUG>>>>]" + ": " + str(message)


def __(text):
    """ Translation helper. Takes a string and tries to return its translation to the current FreeCAD locale.
    If the translation is missing or the file does not exists, return default english string. """

    # Get FreeCAD current language
    freecad_locale = FreeCADGui.getLocale().lower().replace(", ", "-").replace(" ", "-")
    # Find dsphfc directory
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
        with open(filename, "wb") as f:
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

    refocus_cwd()

    # Tries to identify gencase
    if os.path.isfile(data['gencase_path']):
        debug('Path FOUND for gencase')
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

    if not execs_correct:
        bundled_execs_present = are_executables_bundled()

        if bundled_execs_present:
            user_selection = guiutils.ok_cancel_dialog(APP_NAME, "One or more of the executables in the setup is not correct. \n"
                                                       "A DualSPHysics package was detected on your installation. Do you want \n"
                                                       "to load the default configuration?")
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
                warning("One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries")
                guiutils.warning_dialog("One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries.")
    return data, execs_correct


def are_executables_bundled():
    dsph_execs_path = os.path.dirname(os.path.realpath(__file__)) + "/../dualsphysics/EXECS/"
    return os.path.isdir(dsph_execs_path)


def float_list_to_float_property(floating_mks):
    to_ret = dict()
    for key, value in floating_mks.iteritems():
        if isinstance(value, list):
            # Is in old mode. Change to OOP
            fp = FloatProperty(mk=float(key), mass_density_type=int(value[0][0]), mass_density_value=float(value[0][1]))
            if not value[1][0]:  # Gravity center is not auto
                fp.gravity_center = value[1][1:]
            if not value[2][0]:  # Inertia is not auto
                fp.inertia = value[2][1:]
            if not value[3][0]:  # Initial linear velocity is not auto
                fp.initial_linear_velocity = value[3][1:]
            if not value[4][0]:  # Initial angular velocity is not auto
                fp.initial_angular_velocity = value[4][1:]

            to_ret[key] = fp
        else:
            # Is in OOP mode, appending
            to_ret[key] = value
    return to_ret


def initials_list_to_initials_property(initials_mks):
    to_ret = dict()
    for key, value in initials_mks.iteritems():
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

    data = dict()
    temp_data = dict()

    # Data relative to constant definition
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
    data['dp'] = 0.01

    # Data relative to execution parameters
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
    data['incz'] = 1
    data['partsoutmax'] = 1
    data['rhopoutmin'] = 700
    data['rhopoutmax'] = 1300

    # Periodicity data [enabled, x_inc, y_inc, z_inc]
    data['period_x'] = [False, 0.0, 0.0, 0.0]
    data['period_y'] = [False, 0.0, 0.0, 0.0]
    data['period_z'] = [False, 0.0, 0.0, 0.0]

    # Stores paths to executables
    data['gencase_path'] = ""
    data['dsphysics_path'] = ""
    data['partvtk4_path'] = ""
    data['floatinginfo_path'] = ""
    data['computeforces_path'] = ""
    data['measuretool_path'] = ""
    data['isosurface_path'] = ""
    data['boundaryvtk_path'] = ""
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
    data["mkboundused"] = []
    data["mkfluidused"] = []
    """ Dictionary that defines floatings.
        Structure: {mk: FloatProperty} """
    data['floating_mks'] = dict()
    """Dictionary that defines initials.
    Keys are mks enabled (ONLY FLUIDS) and values are a list containing:
    {'mkfluid': [x, y, z]}"""
    data['initials_mks'] = dict()

    # Control data for enabling features
    data['gencase_done'] = False
    data['simulation_done'] = False

    # Simulation objects with its parameters.  Without order.
    # format is: {'key': ['mk', 'type', 'fill']}
    data['simobjects'] = dict()

    # Keys of simobjects.  Ordered.
    data['export_order'] = []
    """ Global movement list.
    It stores all the movements created in this case. """
    data['global_movements'] = list()
    """ Global property list.
        It stores all the properties created in this case. """
    data['global_properties'] = list()
    """ Object movement mapping.
    Dictionary with a list of movements attached..
    {'mkgroup': [movement1, movement2, ...]} """
    data['motion_mks'] = dict()

    # Temporal data dict to control execution features.
    temp_data['current_process'] = None
    temp_data['stored_selection'] = []
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
                data['paraview_path'] = disk_data['paraview_path']

        except Exception:
            # traceback.print_exc()
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
            data['paraview_path'] = ""
            data.update(get_default_config_file())

        data, state = check_executables(data)
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
        for key, value in data["simobjects"].iteritems():
            if value[1].lower() == "fluid":
                mkset.add(value[0])
    else:
        endval = 240
        mkset = set()
        for key, value in data["simobjects"].iteritems():
            if value[1].lower() == "bound":
                mkset.add(value[0])
    for i in range(0, endval):
        if i not in mkset:
            return i


def open_help():
    """ Opens a web browser with this software help. """
    webbrowser.open("http://design.sphysics.org/wiki/")


def get_os():
    """ Returns the current operating system """
    return platform


def print_license():
    """ Prints this software license. """
    licpath = os.path.abspath(__file__).split("dsphfc")[0] + "LICENSE"
    if os.path.isfile(licpath):
        with open(licpath) as licfile:
            print licfile.read()
    else:
        raise EnvironmentError("LICENSE file could not be found. Are you sure you didn't delete it?")


def prompt_close_all_documents(prompt=True):
    """ Shows a dialog to close all the current documents.
        If accepted, close all the current documents and return True, else returns False. """
    if prompt:
        user_selection = guiutils.ok_cancel_dialog(APP_NAME, "To do this you must close all current documents. Close all the documents?")
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
    return True if document_count() is 1 and 'dsph_case' in FreeCAD.listDocuments().keys()[0].lower() else False


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


def dump_to_xml(data, save_name):
    """ Saves all of the data in the opened case
        to disk. Generates a GenCase compatible XML. """
    # Saves all the data in XML format.
    log("Saving data in " + data["project_path"] + ".")
    FreeCAD.getDocument("DSPH_Case").saveAs(save_name.encode('utf-8') + "/DSPH_Case.FCStd")
    FreeCADGui.SendMsgToActiveView("Save")
    f = open(save_name + "/" + save_name.split('/')[-1] + "_Def.xml", 'w')
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    f.write('<!-- Case name: {} -->\n'.format(data["project_name"].encode('utf-8')))
    f.write('<case app="{} v{}" date="{}">\n'.format(APP_NAME, VERSION, datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
    f.write('\t<casedef>\n')
    f.write('\t\t<constantsdef>\n')
    f.write('\t\t\t<lattice bound="' + str(data['lattice_bound']) + '" fluid="' + str(data['lattice_fluid']) + '" />\n')
    f.write('\t\t\t<gravity x="' + str(data['gravity'][0]) + '" y="' + str(data['gravity'][1]) + '" z="' + str(data['gravity'][2]) +
            '" comment="Gravitational acceleration" units_comment="m/s^2" />\n')
    f.write('\t\t\t<rhop0 value="' + str(data['rhop0']) + '" comment="Reference density of the fluid" units_comment="kg/m^3" />\n')
    f.write('\t\t\t<hswl value="' + str(data['hswl']) + '" auto="' + str(data['hswl_auto']).lower() +
            '" comment="Maximum still water level to calculate speedofsound using coefsound" '
            'units_comment="metres (m)"  />\n')
    f.write('\t\t\t<gamma value="' + str(data['gamma']) + '" comment="Polytropic constant for water used in the state equation" />\n')
    f.write('\t\t\t<speedsystem value="' + str(data['speedsystem']) + '" auto="' + str(data['speedsystem_auto']).lower() +
            '" comment="Maximum system speed (by default the dam-break propagation is used)" />\n')
    f.write('\t\t\t<coefsound value="' + str(data['coefsound']) + '" comment="Coefficient to multiply speedsystem" />\n')
    f.write('\t\t\t<speedsound value="' + str(data['speedsound']) + '" auto="' + str(data['speedsound_auto']).lower() +
            '" comment="Speed of sound to use in the simulation '
            '(by default speedofsound=coefsound*speedsystem)" />\n')
    f.write('\t\t\t<coefh value="' + str(data['coefh']) + '" comment="Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D)" />\n')
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
        f.write('\t\t\t\t<pointmax x="' + str((min_point.x / DIVIDER + max_point.Length.Value / DIVIDER)) + '" y="' + str(
            (min_point.y / DIVIDER + max_point.Width.Value / DIVIDER)) + '" z="' + str((min_point.z / DIVIDER + max_point.Height.Value / DIVIDER)) + '" />\n')
    else:
        f.write('\t\t\t\t<pointmax x="' + str((min_point.x / DIVIDER + max_point.Length.Value / DIVIDER)) + '" y="' + str((min_point.y / DIVIDER)) + '" z="' +
                str((min_point.z / DIVIDER + max_point.Height.Value / DIVIDER)) + '" />\n')
    f.write('\t\t\t</definition>\n')
    f.write('\t\t\t<commands>\n')
    f.write('\t\t\t\t<mainlist>\n')
    f.write('\t\t\t\t\t<setshapemode>dp | bound</setshapemode>\n')
    # Export in strict order
    for key in data["export_order"]:
        name = key
        valuelist = data["simobjects"][name]
        o = FreeCAD.getDocument("DSPH_Case").getObject(name)
        # Ignores case limits
        if name != "Case_Limits":
            # Sets MKfluid or bound depending on object properties and resets
            # the matrix
            f.write('\t\t\t\t\t<matrixreset />\n')
            if valuelist[1].lower() == "fluid":
                f.write('\t\t\t\t\t<setmkfluid mk="' + str(valuelist[0]) + '"/>\n')
            elif valuelist[1].lower() == "bound":
                f.write('\t\t\t\t\t<setmkbound mk="' + str(valuelist[0]) + '"/>\n')
            f.write('\t\t\t\t\t<setdrawmode mode="' + valuelist[2].lower() + '"/>\n')
            """ Exports supported objects in a xml parametric mode.
            If special objects are found, exported in an specific manner (p.e FillBox)
            The rest of the things are exported in STL format."""
            if o.TypeId == "Part::Box":
                f.write('\t\t\t\t\t<move x="' + str(o.Placement.Base.x / DIVIDER) + '" y="' + str(o.Placement.Base.y / DIVIDER) + '" z="' + str(
                    o.Placement.Base.z / DIVIDER) + '" />\n')
                f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' + str(-o.Placement.Rotation.Axis.x) + '" y="' +
                        str(-o.Placement.Rotation.Axis.y) + '" z="' + str(-o.Placement.Rotation.Axis.z) + '" />\n')
                f.write('\t\t\t\t\t<drawbox objname="{}">\n'.format(o.Label))
                f.write('\t\t\t\t\t\t<boxfill>solid</boxfill>\n')
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t\t<size x="' + str(o.Length.Value / DIVIDER) + '" y="' + str(o.Width.Value / DIVIDER) + '" z="' + str(
                    o.Height.Value / DIVIDER) + '" />\n')
                f.write('\t\t\t\t\t</drawbox>\n')
            elif o.TypeId == "Part::Sphere":
                f.write('\t\t\t\t\t<move x="' + str(o.Placement.Base.x / DIVIDER) + '" y="' + str(o.Placement.Base.y / DIVIDER) + '" z="' + str(
                    o.Placement.Base.z / DIVIDER) + '" />\n')
                f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' + str(-o.Placement.Rotation.Axis.x) + '" y="' +
                        str(-o.Placement.Rotation.Axis.y) + '" z="' + str(-o.Placement.Rotation.Axis.z) + '" />\n')
                f.write('\t\t\t\t\t<drawsphere radius="' + str(o.Radius.Value / DIVIDER) + '"  objname="{}">\n'.format(o.Label))
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t</drawsphere>\n')
            elif o.TypeId == "Part::Cylinder":
                f.write('\t\t\t\t\t<move x="' + str(o.Placement.Base.x / DIVIDER) + '" y="' + str(o.Placement.Base.y / DIVIDER) + '" z="' + str(
                    o.Placement.Base.z / DIVIDER) + '" />\n')
                f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' + str(-o.Placement.Rotation.Axis.x) + '" y="' +
                        str(-o.Placement.Rotation.Axis.y) + '" z="' + str(-o.Placement.Rotation.Axis.z) + '" />\n')
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
                        f.write('\t\t\t\t\t<move x="' + str(filllimits.Placement.Base.x / DIVIDER) + '" y="' + str(filllimits.Placement.Base.y / DIVIDER) +
                                '" z="' + str(filllimits.Placement.Base.z / DIVIDER) + '" />\n')
                        f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(
                            filllimits.Placement.Rotation.Angle)) + '" x="' + str(-filllimits.Placement.Rotation.Axis.x) + '" y="' +
                                str(-filllimits.Placement.Rotation.Axis.y) + '" z="' + str(-filllimits.Placement.Rotation.Axis.z) + '" />\n')
                        f.write('\t\t\t\t\t<fillbox x="' + str((fillpoint.Placement.Base.x - filllimits.Placement.Base.x) / DIVIDER) + '" y="' + str(
                            (fillpoint.Placement.Base.y - filllimits.Placement.Base.y) / DIVIDER) + '" z="' + str(
                                (fillpoint.Placement.Base.z - filllimits.Placement.Base.z) / DIVIDER) + '" objname="{}">\n'.format(o.Label))
                        f.write('\t\t\t\t\t\t<modefill>void</modefill>\n')
                        f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                        f.write('\t\t\t\t\t\t<size x="' + str(filllimits.Length.Value / DIVIDER) + '" y="' + str(filllimits.Width.Value / DIVIDER) + '" z="' +
                                str(filllimits.Height.Value / DIVIDER) + '" />\n')
                        f.write('\t\t\t\t\t\t<matrixreset />\n')
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
                    Mesh.export(__objs__, save_name + "/" + o.Name + ".stl")
                    f.write('\t\t\t\t\t<drawfilestl file="' + save_name + "/" +
                            o.Name + ".stl" + '" objname="{}">\n'.format(o.Label))
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
        for key, value in data["initials_mks"].iteritems():
            f.write('\t\t\t<velocity mkfluid="' + str(key) + '" x="' + str(value.force[0]) + '" y="' + str(value.force[1]) + '" z="' + str(value.force[2]) +
                    '"/>\n')
        f.write('\t\t</initials>\n')
    # Writes floatings
    if len(data["floating_mks"].keys()) > 0:
        f.write('\t\t<floatings>\n')
        for key, value in data["floating_mks"].iteritems():
            if value.mass_density_type == 0:
                # is massbody
                f.write('\t\t\t<floating mkbound="' + str(key) + '">\n')
                f.write('\t\t\t\t<massbody value="' + str(value.mass_density_value) + '" />\n')
            else:
                # is rhopbody
                f.write('\t\t\t<floating mkbound="' + str(key) + '" rhopbody="' + str(value.mass_density_value) + '">\n')
            if len(value.gravity_center) != 0:
                f.write('\t\t\t\t<center x="' + str(value.gravity_center[0]) + '" y="' + str(value.gravity_center[1]) + '" z="' + str(value.gravity_center[2]) +
                        '" />\n')
            if len(value.inertia) != 0:
                f.write('\t\t\t\t<inertia x="' + str(value.inertia[0]) + '" y="' + str(value.inertia[1]) + '" z="' + str(value.inertia[2]) + '" />\n')
            if len(value.initial_linear_velocity) != 0:
                f.write('\t\t\t\t<velini x="' + str(value.initial_linear_velocity[0]) + '" y="' + str(value.initial_linear_velocity[1]) + '" z="' + str(
                    value.initial_linear_velocity[2]) + '" />\n')
            if len(value.initial_angular_velocity) != 0:
                f.write('\t\t\t\t<omegaini x="' + str(value.initial_angular_velocity[0]) + '" y="' + str(value.initial_angular_velocity[1]) + '" z="' + str(
                    value.initial_angular_velocity[2]) + '" />\n')
            f.write('\t\t\t</floating>\n')
        f.write('\t\t</floatings>\n')

    # Writes motions
    if len(data["motion_mks"]) > 0:
        f.write('\t\t<motion>\n')
        for key, value in data["motion_mks"].iteritems():
            f.write('\t\t\t<objreal ref="' + str(key) + '">\n')
            mov_counter = 1
            mot_counter = 1
            for movement in value:
                f.write('\t\t\t\t<!-- Movement Name: {} -->\n'.format(movement.name))
                f.write('\t\t\t\t<begin mov="{}" start="0"/>\n'.format(mov_counter))
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
                                    f.write('\t\t\t\t<mvrect id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrect id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrect id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<vel x="{}" y="{}" z="{}"/>\n'.format(motion.velocity[0], motion.velocity[1], motion.velocity[2]))
                            f.write('\t\t\t\t</mvrect>\n')
                        elif isinstance(motion, WaitMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                if movement.loop:
                                    f.write('\t\t\t\t<wait id="{}" duration="{}" next="{}"/>\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<wait id="{}" duration="{}"/>\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<wait id="{}" duration="{}" next="{}"/>\n'.format(mot_counter, motion.duration, mot_counter + 1))
                        elif isinstance(motion, AccRectMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrectace id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrectace id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrectace id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<vel x="{}" y="{}" z="{}"/>\n'.format(motion.velocity[0], motion.velocity[1], motion.velocity[2]))
                            f.write('\t\t\t\t\t<ace x="{}" y="{}" z="{}"/>\n'.format(motion.acceleration[0], motion.acceleration[1], motion.acceleration[2]))
                            f.write('\t\t\t\t</mvrectace>\n')
                        elif isinstance(motion, RotMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrot id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrot id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrot id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<vel ang="{}"/>\n'.format(motion.ang_vel))
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
                                    f.write('\t\t\t\t<mvrotace id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrotace id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrotace id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<ace ang="{}"/>\n'.format(motion.ang_acc))
                            f.write('\t\t\t\t\t<velini ang="{}"/>\n'.format(motion.ang_vel))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvrotace>\n')
                        elif isinstance(motion, AccCirMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvcirace id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvcirace id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvcirace id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<ace ang="{}"/>\n'.format(motion.ang_acc))
                            f.write('\t\t\t\t\t<velini ang="{}"/>\n'.format(motion.ang_vel))
                            f.write('\t\t\t\t\t<ref x="{}" y="{}" z="{}"/>\n'.format(motion.reference[0], motion.reference[1], motion.reference[2]))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvcirace>\n')
                        elif isinstance(motion, RotSinuMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrotsinu id="{}" duration="{}" anglesunits="radians" next="{}" >\n'.format(
                                        mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrotsinu id="{}" duration="{}" anglesunits="radians">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrotsinu id="{}" duration="{}" anglesunits="radians" next="{}">\n'.format(
                                    mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<freq v="{}"/>\n'.format(motion.freq))
                            f.write('\t\t\t\t\t<ampl v="{}"/>\n'.format(motion.ampl))
                            f.write('\t\t\t\t\t<phase v="{}"/>\n'.format(motion.phase))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvrotsinu>\n')
                        elif isinstance(motion, CirSinuMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvcirsinu id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvcirsinu id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvcirsinu id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<freq v="{}"/>\n'.format(motion.freq))
                            f.write('\t\t\t\t\t<ampl v="{}"/>\n'.format(motion.ampl))
                            f.write('\t\t\t\t\t<phase v="{}"/>\n'.format(motion.phase))
                            f.write('\t\t\t\t\t<ref x="{}" y="{}" z="{}"/>\n'.format(motion.reference[0], motion.reference[1], motion.reference[2]))
                            f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}"/>\n'.format(motion.axis1[0], motion.axis1[1], motion.axis1[2]))
                            f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}"/>\n'.format(motion.axis2[0], motion.axis2[1], motion.axis2[2]))
                            f.write('\t\t\t\t</mvcirsinu>\n')
                        elif isinstance(motion, RectSinuMotion):
                            if motion_index is len(movement.motion_list) - 1:
                                try:
                                    is_looping = movement.loop
                                except AttributeError:
                                    is_looping = False
                                if is_looping:
                                    f.write('\t\t\t\t<mvrectsinu id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, first_series_motion))
                                else:
                                    f.write('\t\t\t\t<mvrectsinu id="{}" duration="{}">\n'.format(mot_counter, motion.duration))
                            else:
                                f.write('\t\t\t\t<mvrectsinu id="{}" duration="{}" next="{}">\n'.format(mot_counter, motion.duration, mot_counter + 1))

                            f.write('\t\t\t\t\t<freq x="{}" y="{}" z="{}"/>\n'.format(motion.freq[0], motion.freq[1], motion.freq[2]))
                            f.write('\t\t\t\t\t<ampl x="{}" y="{}" z="{}"/>\n'.format(motion.ampl[0], motion.ampl[1], motion.ampl[2]))
                            f.write('\t\t\t\t\t<phase x="{}" y="{}" z="{}"/>\n'.format(motion.phase[0], motion.phase[1], motion.phase[2]))
                            f.write('\t\t\t\t</mvrectsinu>\n')

                        mot_counter += 1
                elif isinstance(movement, SpecialMovement):
                    if isinstance(movement.generator, FileGen):
                        f.write('\t\t\t\t<mvfile id="{}" duration="{}">\n '.format(mov_counter, movement.generator.duration))
                        f.write('\t\t\t\t\t<file name="{}" fields="{}" fieldtime="{}" '
                                'fieldx="{}" fieldy="{}" />\n '.format(movement.generator.filename, movement.generator.fields, movement.generator.fieldtime,
                                                                       movement.generator.fieldx, movement.generator.fieldy))
                        f.write('\t\t\t\t</mvfile>\n ')
                    elif isinstance(movement.generator, RotationFileGen):
                        f.write('\t\t\t\t<mvrotfile id="{}" duration="{}" anglesunits="{}">\n '.format(mov_counter, movement.generator.duration,
                                                                                                       movement.generator.anglesunits))
                        f.write('\t\t\t\t\t<file name="{}" />\n '.format(movement.generator.filename))
                        f.write('\t\t\t\t\t<axisp1 x="{}" y="{}" z="{}" />\n '.format(*movement.generator.axisp1))
                        f.write('\t\t\t\t\t<axisp2 x="{}" y="{}" z="{}" />\n '.format(*movement.generator.axisp2))
                        f.write('\t\t\t\t</mvrotfile>\n ')
                    else:
                        f.write('\t\t\t\t<mvnull id="{}" />\n'.format(mov_counter))

                mov_counter += 1
            f.write('\t\t\t</objreal>\n')
        f.write('\t\t</motion>\n')
    f.write('\t</casedef>\n')
    f.write('\t<execution>\n')
    for mk, motlist in data["motion_mks"].iteritems():
        # Check if object has motion enabled but no motions selected
        if len(motlist) < 1:
            continue
        if isinstance(motlist[0], SpecialMovement):
            mot = motlist[0].generator
            if isinstance(mot, FileGen):
                continue
            f.write('\t\t\t<special>\n')
            f.write('\t\t\t\t<wavepaddles>\n')
            if isinstance(mot, RegularWaveGen):
                f.write('\t\t\t\t\t<piston>\n')
                f.write('\t\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write('\t\t\t\t\t\t<waveorder value="{}" ' 'comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(mot.wave_order))
                f.write('\t\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(mot.start))
                f.write('\t\t\t\t\t\t<duration value="{}" ' 'comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(mot.duration))
                f.write('\t\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(mot.depth))
                f.write('\t\t\t\t\t\t<pistondir x="{}" y="{}" z="{}" ' 'comment="Movement direction (def=(1,0,0))" />\n'.format(*mot.piston_dir))
                f.write('\t\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(mot.wave_height))
                f.write('\t\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(mot.wave_period))
                f.write('\t\t\t\t\t\t<phase value="{}" ' 'comment="Initial wave phase in function of PI (def=0)" />\n'.format(mot.phase))
                f.write('\t\t\t\t\t\t<ramp value="{}" comment="Periods of ramp (def=0)" />\n'.format(mot.ramp))
                f.write('\t\t\t\t\t\t<savemotion periods="{}" periodsteps="{}" xpos="{}" zpos="{}" '
                        'comment="Saves motion data. xpos and zpos are optional. '
                        'zpos=-depth of the measuring point" />\n'.format(mot.disksave_periods, mot.disksave_periodsteps, mot.disksave_xpos, mot.disksave_zpos))
                f.write('\t\t\t\t\t</piston>\n')
            elif isinstance(mot, IrregularWaveGen):
                f.write('\t\t\t\t\t<piston_spectrum>\n')
                f.write('\t\t\t\t\t\t<mkbound value="{}" comment="Mk-Bound of selected particles" />\n'.format(mk))
                f.write('\t\t\t\t\t\t<waveorder value="{}" ' 'comment="Order wave generation 1:1st order, 2:2nd order (def=1)" />\n'.format(mot.wave_order))
                f.write('\t\t\t\t\t\t<start value="{}" comment="Start time (def=0)" />\n'.format(mot.start))
                f.write('\t\t\t\t\t\t<duration value="{}" ' 'comment="Movement duration, Zero is the end of simulation (def=0)" />\n'.format(mot.duration))
                f.write('\t\t\t\t\t\t<depth value="{}" comment="Fluid depth (def=0)" />\n'.format(mot.depth))
                f.write('\t\t\t\t\t\t<fixeddepth value="{}" ' 'comment="Fluid depth without paddle (def=0)" />\n'.format(mot.fixed_depth))
                f.write('\t\t\t\t\t\t<pistondir x="{}" y="{}" z="{}" ' 'comment="Movement direction (def=(1,0,0))" />\n'.format(*mot.piston_dir))
                f.write('\t\t\t\t\t\t<spectrum value="{}" '
                        'comment="Spectrum type: jonswap,pierson-moskowitz" />\n'.format(['jonswap', 'pierson-moskowitz'][mot.spectrum]))
                f.write('\t\t\t\t\t\t<discretization value="{}" '
                        'comment="Spectrum discretization: regular,random,stretched,cosstretched '
                        '(def=stretched)" />\n'.format(['regular', 'random', 'stretched', 'cosstretched'][mot.discretization]))
                f.write('\t\t\t\t\t\t<waveheight value="{}" comment="Wave height" />\n'.format(mot.wave_height))
                f.write('\t\t\t\t\t\t<waveperiod value="{}" comment="Wave period" />\n'.format(mot.wave_period))
                f.write('\t\t\t\t\t\t<peakcoef value="{}" comment="Peak enhancement coefficient (def=3.3)" />\n'.format(mot.peak_coef))
                f.write('\t\t\t\t\t\t<waves value="{}" ' 'comment="Number of waves to create irregular waves (def=50)" />\n'.format(mot.waves))
                f.write('\t\t\t\t\t\t<randomseed value="{}" ' 'comment="Random seed to initialize a pseudorandom number generator" />\n'.format(mot.randomseed))
                f.write('\t\t\t\t\t\t<serieini value="{}" autofit="{}" '
                        'comment="Initial time in irregular wave serie (default=0 and autofit=false)" />\n'.format(
                            mot.serieini, str(mot.serieini_autofit).lower()))
                f.write('\t\t\t\t\t\t<ramptime value="{}" comment="Time of ramp (def=0)" />\n'.format(mot.ramptime))
                f.write('\t\t\t\t\t\t<savemotion time="{}" timedt="{}" xpos="{}" zpos="{}" '
                        'comment="Saves motion data. xpos and zpos are optional. '
                        'zpos=-depth of the measuring point" />\n'.format(mot.savemotion_time, mot.savemotion_timedt, mot.savemotion_xpos, mot.savemotion_zpos))
                f.write('\t\t\t\t\t\t<saveserie timemin="{}" timemax="{}" timedt="{}" xpos="{}"'
                        ' comment="Saves serie data (optional)" />\n'.format(mot.saveserie_timemin, mot.saveserie_timemax, mot.saveserie_timedt,
                                                                             mot.saveserie_xpos))
                f.write('\t\t\t\t\t\t<saveseriewaves timemin="{}" timemax="{}" xpos="{}" '
                        'comment="Saves serie heights" />\n'.format(mot.saveseriewaves_timemin, mot.saveseriewaves_timemax, mot.saveseriewaves_xpos))
                f.write('\t\t\t\t\t</piston_spectrum>\n')
            f.write('\t\t\t\t</wavepaddles>\n')
            f.write('\t\t\t</special>\n')
    f.write('\t\t<parameters>\n')
    # Writes parameters as user introduced
    f.write('\t\t\t<parameter key="PosDouble" value="' + str(data['posdouble']) + '" comment="Precision in particle interaction '
            '0:Simple, 1:Double, 2:Uses and saves double (default=0)" />\n')
    f.write('\t\t\t<parameter key="StepAlgorithm" value="' + str(data['stepalgorithm']) + '" comment="Step Algorithm 1:Verlet, 2:Symplectic (default=1)" />\n')
    f.write('\t\t\t<parameter key="VerletSteps" value="' + str(data['verletsteps']) +
            '" comment="Verlet only: Number of steps to apply Euler timestepping (default=40)" />\n')
    f.write('\t\t\t<parameter key="Kernel" value="' + str(data['kernel']) + '" comment="Interaction Kernel 1:Cubic Spline, 2:Wendland (default=2)" />\n')
    f.write('\t\t\t<parameter key="ViscoTreatment" value="' + str(data['viscotreatment']) +
            '" comment="Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)" />\n')
    f.write('\t\t\t<parameter key="Visco" value="' + str(data['visco']) + '" comment="Viscosity value" /> % Note alpha can depend on the resolution. '
            'A value of 0.01 is recommended for near irrotational flows.\n')
    f.write('\t\t\t<parameter key="ViscoBoundFactor" value="' + str(data['viscoboundfactor']) +
            '" comment="Multiply viscosity value with boundary (default=1)" />\n')
    f.write('\t\t\t<parameter key="DeltaSPH" value="' + str(data['deltasph']) +
            '" comment="DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0)" />\n')
    f.write('\t\t\t<parameter key="Shifting" value="' + str(data['shifting']) +
            '" comment="Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0)" />\n')
    f.write('\t\t\t<parameter key="ShiftCoef" value="' + str(data['shiftcoef']) + '" comment="Coefficient for shifting computation (default=-2)" />\n')
    f.write('\t\t\t<parameter key="ShiftTFS" value="' + str(data['shifttfs']) +
            '" comment="Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0)" />\n')
    f.write('\t\t\t<parameter key="RigidAlgorithm" value="' + str(data['rigidalgorithm']) + '" comment="Rigid Algorithm 1:SPH, 2:DEM (default=1)" />\n')
    f.write('\t\t\t<parameter key="FtPause" value="' + str(data['ftpause']) + '" comment="Time to freeze the floatings at simulation start'
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
    f.write('\t\t\t<parameter key="TimeMax" value="' + str(data['timemax']) + '" comment="Time of simulation" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="TimeOut" value="' + str(data['timeout']) + '" comment="Time out data" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="IncZ" value="' + str(data['incz']) + '" comment="Increase of Z+" units_comment="decimal" />\n')
    f.write('\t\t\t<parameter key="PartsOutMax" value="' + str(data['partsoutmax']) + '" comment="%/100 of fluid particles allowed to be excluded from domain '
            '(default=1)" units_comment="decimal" />\n')
    f.write('\t\t\t<parameter key="RhopOutMin" value="' + str(data['rhopoutmin']) + '" comment="Minimum rhop valid (default=700)" units_comment="kg/m^3" />\n')
    f.write('\t\t\t<parameter key="RhopOutMax" value="' + str(data['rhopoutmax']) + '" comment="Maximum rhop valid (default=1300)" units_comment="kg/m^3" />\n')
    if data['period_x'][0]:
        if data['3dmode']:
            f.write('\t\t\t<parameter key="XPeriodicIncY" value="' + str(data['period_x'][2]) + '"/>\n')
        f.write('\t\t\t<parameter key="XPeriodicIncZ" value="' + str(data['period_x'][3]) + '"/>\n')
    if data['period_y'][0] and data['3dmode']:
        f.write('\t\t\t<parameter key="YPeriodicIncX" value="' + str(data['period_y'][1]) + '"/>\n')
        f.write('\t\t\t<parameter key="YPeriodicIncZ" value="' + str(data['period_y'][3]) + '"/>\n')
    if data['period_z'][0]:
        f.write('\t\t\t<parameter key="ZPeriodicIncX" value="' + str(data['period_z'][1]) + '"/>\n')
        if data['3dmode']:
            f.write('\t\t\t<parameter key="ZPeriodicIncY" value="' + str(data['period_z'][2]) + '"/>\n')
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
            app_name=APP_NAME, case_name=case_name.encode('utf-8'), gcpath=gcpath, dsphpath=dsphpath, pvtkpath=pvtkpath, exec_params=exec_params)
    with open('{}/templates/template.sh'.format(lib_folder), 'r') as content_file:
        linux_template = content_file.read().format(
            app_name=APP_NAME,
            case_name=case_name.encode('utf-8'),
            gcpath=gcpath,
            dsphpath=dsphpath,
            pvtkpath=pvtkpath,
            exec_params=exec_params,
            lib_path=lib_path,
            name="name")

    with open(full_path + "/run.bat", 'w') as bat_file:
        log(__("Creating ") + full_path + "/run.bat")
        bat_file.write(win_template)
    with open(full_path + "/run.sh", 'w') as bat_file:
        log(__("Creating ") + full_path + "/run.sh")
        bat_file.write(linux_template)


def import_stl(filename=None, scale_x=1, scale_y=1, scale_z=1, name=None):
    """ Opens a STL file, preprocesses it and saves it
    int temp files to load with FreeCAD. """
    if scale_x <= 0:
        scale_x = 1
    if scale_y <= 0:
        scale_y = 1
    if scale_z <= 0:
        scale_z = 1

    if not filename:
        raise RuntimeError("STL Import: file cannot be None")
    try:
        target = stl.Mesh.from_file(filename)
    except Exception as e:
        raise e

    target.x *= scale_x
    target.y *= scale_y
    target.z *= scale_z
    if not name:
        temp_file_name = tempfile.gettempdir() + "/" + str(random.randrange(100, 1000, 1)) + ".stl"
    else:
        temp_file_name = tempfile.gettempdir() + "/" + name + ".stl"

    target.save(temp_file_name)

    Mesh.insert(temp_file_name, FreeCAD.activeDocument().Name)
    FreeCADGui.SendMsgToActiveView("ViewFit")


def get_fc_object(internal_name):
    """ Returns a FreeCAD internal object by a name. """
    return FreeCAD.getDocument("DSPH_Case").getObject(internal_name)
