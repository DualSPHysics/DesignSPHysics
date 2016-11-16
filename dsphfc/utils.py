#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""VisualSPHysics for FreeCAD Utils.

This file contains a collection of constants and
functions meant to use with VisualSPHysics for FreeCAD.

This module stores non-gui related operations, but
meant to use with FreeCAD.

"""

"""
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of VisualSPHysics for FreeCAD.

VisualSPHysics for FreeCAD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VisualSPHysics for FreeCAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VisualSPHysics for FreeCAD.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Andrés Vieira"
__copyright__ = "Copyright 2016, DualSHPysics Team"
__credits__ = ["Andrés Vieira", "Alejandro Jacobo Cabrera Crespo"]
__license__ = "GPL"
__version__ = "v0.1 BETA"
__maintainer__ = "Andrés Vieira"
__email__ = "anvieiravazquez@gmail.com"
__status__ = "Development"

import FreeCAD
import FreeCADGui
import Mesh
import sys
import os
import pickle
import threading
import math
import webbrowser
import traceback
import glob
import numpy
from PySide import QtGui, QtCore
from datetime import datetime
sys.path.append(FreeCAD.getUserAppDataDir() + "Macro/dsphfc")
import guiutils

#------ CONSTANTS DEFINITION ------
FREECAD_MIN_VERSION = "016"
APP_NAME = "VisualSPHysics for FreeCAD"
DEBUGGING = True
#------ END CONSTANTS DEFINITION ------
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
    print "[" + APP_NAME + "] " + str(message)

def warning(message):
    print "[" + APP_NAME + "] " + "[WARNING]" + ": " + str(message)

def error(message):
    print "[" + APP_NAME + "] " + "[ERROR]" + ": " + str(message)

def debug(message):
    if DEBUGGING:
        print "[" + APP_NAME + "] " + "[<<<<DEBUG>>>>]" + ": " + str(message) 

def check_executables(gencase_path, dsphysics_path, partvtk4_path):
    """ Checks the three needed executables for working with
        this software. Returns 4 values: 3 string paths and a boolean.
        If some path is not correct returns the respective
        empty string and False. """

    execs_correct = True
    #Tries to identify gencase
    if os.path.isfile(gencase_path):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start(gencase_path)
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "gencase" in output[0:15].lower():
            log("Found correct GenCase.")
        else:
            execs_correct = False
            gencase_path = ""
    else:
        execs_correct = False
        gencase_path = ""            

    #Tries to identify dualsphysics
    if os.path.isfile(dsphysics_path):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start(dsphysics_path)
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "dualsphysics" in output[0:20].lower():
            log("Found correct DualSPHysics.")
        else:
            execs_correct = False
            dsphysics_path = ""
    else:
        execs_correct = False
        dsphysics_path = ""            

    #Tries to identify partvtk4
    if os.path.isfile(partvtk4_path):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start(partvtk4_path)
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "partvtk4" in output[0:20].lower():
            log("Found correct PartVTK4.")
        else:
            execs_correct = False    
            partvtk4_path = ""
    else:
        execs_correct = False
        partvtk4_path = ""            

    #Spawn warning dialog and return paths.
    if not execs_correct:
        warning("One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries")
        guiutils.warning_dialog("One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries.")
    return gencase_path, dsphysics_path, partvtk4_path, execs_correct

def get_default_data():
    """ Sets default data at start of the macro.
        Returns data and temp_data dict with default values.
        If there is data saved on disk, tries to load it."""

    data = dict()
    temp_data = dict()

    #Data relative to constant definition
    data['lattice_bound'] = 1
    data['lattice_fluid'] = 1
    data['gravity'] = [0,0,-9.81]
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
    data['dp'] = 0.0005

    #Data relative to execution parameters
    data['posdouble'] = 1    
    data['stepalgorithm'] = 1    
    data['verletsteps'] = 40    
    data['kernel'] = 2    
    data['viscotreatment'] = 1    
    data['visco'] = 0.01    
    data['viscoboundfactor'] = 1    
    data['deltasph'] = 0    
    data['shifting'] = 0    
    data['shiftcoef'] = -2    
    data['shifttfs'] = 1.5
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

    #Stores paths to executables
    data['gencase_path'] = ""
    data['dsphysics_path'] = ""
    data['partvtk4_path'] = ""

    #Stores project path and name for future script needs
    data['project_path'] = ""
    data['project_name'] = "" 
    data['total_particles'] = -1
    data['total_particles_out'] = 0
    data['additional_parameters'] = ""
    data['export_options'] = ""
    data["mkboundused"] = []
    data["mkfluidused"] = []
    
    """ Dictionary that defines floatings. 
        Keys are mks enabled (ONLY BOUNDS) and values are a list containing:
        {'mkbound': [massrhop, center, inertia, velini, omegaini]}
        massrhop = [selectedOption (index), value]
        center = [auto (bool), x,y,z]
        inertia = [auto (bool), x,y,z]
        velini = [auto (bool), x,y,z]
        omegaini = [auto (bool), x,y,z]"""
    data['floating_mks'] = dict()

    """Dictionary that defines initials. 
    Keys are mks enabled (ONLY FLUIDS) and values are a list containing:
    {'mkfluid': [x, y, z]}"""
    data['initials_mks'] = dict()

    #Control data for enabling features
    data['gencase_done'] = False
    data['simulation_done'] = False

    #Simulation objects with its parameters.  Without order.
    #format is: {'key': ['mk', 'type', 'fill']}
    data['simobjects'] = dict()

    #Keys of simobjects.  Ordered.
    data['export_order'] = []

    #Temporal data dict to control execution features.
    temp_data['current_process'] = None
    temp_data['stored_selection'] = []
    temp_data['export_numparts'] = ""
    temp_data['total_export_parts'] = -1
    temp_data['supported_types'] = ["Part::Box", "Part::Sphere", "Part::Cylinder"]

    """ Try to load saved paths. This way the user does not need
        to introduce the software paths every time"""
    if os.path.isfile(FreeCAD.getUserAppDataDir() + '/dsph_data.dsphdata'):
        try:
            picklefile = open(FreeCAD.getUserAppDataDir() + '/dsph_data.dsphdata', 'rb')
            disk_data = pickle.load(picklefile)
            data['gencase_path'] = disk_data['gencase_path']
            data['dsphysics_path'] = disk_data['dsphysics_path']
            data['partvtk4_path'] = disk_data['partvtk4_path']
        except:
            traceback.print_exc()
            data['gencase_path'] = ""
            data['dsphysics_path'] = ""
            data['partvtk4_path'] = ""
    
        log("Found data file. Loading data from disk.")
        data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'], state = check_executables(data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'])
    else:
        data["project_path"] = "" 
        data["project_name"] = ""


    return data, temp_data

def get_first_mk_not_used(objtype, data):
    """ Checks simulation objects to find the first not used
        MK group. """

    if objtype == "fluid":
        endval = 10
        mkset = set()
        for key,value in data["simobjects"].iteritems():
            if value[1].lower() == "fluid":
                mkset.add(value[0])
    else:
        endval = 240
        mkset = set()
        for key,value in data["simobjects"].iteritems():
            if value[1].lower() == "bound":
                mkset.add(value[0])
    for i in range(0, endval):
        if i not in mkset:
            return i

def open_help():
    """ Opens a web browser with this software help. """

    webbrowser.open("http://dual.sphysics.org/gui/wiki/")

def print_license():
    """ Prints this software license. """
    licpath = os.path.abspath(__file__).split("dsphfc")[0] + "LICENSE"
    if os.path.isfile(licpath):
        with open(licpath) as licfile:
            print licfile.read()
    else:
        raise EnvironmentError("LICENSE file could not be found. Are you sure you didn't delete it?")

def prompt_close_all_documents():
    """ Shows a dialog to close all the current documents.
        If accepted, close all the current documents, 
        else stops the script execution. """
    user_selection = guiutils.ok_cancel_dialog(APP_NAME, "To load this module you must close all current documents. Close all the documents?")
    if user_selection == QtGui.QMessageBox.Ok:
        #Close all current documents.
        log("Closing all current documents")
        for doc in FreeCAD.listDocuments().keys():
            FreeCAD.closeDocument(doc)
        return True
    else:
        return False

def document_count():
    """ Returns an integer representing the number of
        current opened documents in FreeCAD. """
    return len(FreeCAD.listDocuments().keys())

def create_dsph_document():
    """ Creates a new DSPH compatible document in FreeCAD.
        It includes the case limits and a compatible name. """
    FreeCAD.newDocument("DSPH_Case")
    FreeCAD.setActiveDocument("DSPH_Case")
    FreeCAD.ActiveDocument = FreeCAD.getDocument("DSPH_Case")
    FreeCADGui.ActiveDocument = FreeCADGui.getDocument("DSPH_Case")
    FreeCADGui.activateWorkbench("PartWorkbench")
    FreeCADGui.activeDocument().activeView().viewAxonometric()
    FreeCAD.ActiveDocument.addObject("Part::Box","Case_Limits")
    FreeCAD.ActiveDocument.getObject("Case_Limits").Label = "Case_Limits"
    FreeCAD.ActiveDocument.getObject("Case_Limits").Length = '15 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Width = '15 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Height = '15 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCADGui.ActiveDocument.getObject("Case_Limits").DisplayMode = "Wireframe"
    FreeCADGui.ActiveDocument.getObject("Case_Limits").LineColor = (1.00,0.00,0.00)
    FreeCADGui.ActiveDocument.getObject("Case_Limits").LineWidth = 2.00
    FreeCADGui.ActiveDocument.getObject("Case_Limits").Selectable = False
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")

def dump_to_xml(data, save_name):
    """ Saves all of the data in the opened case
        to disk. Generates a GenCase compatible XML. """
    #Saves all the data in XML format.
    log("Saving data in " + data["project_path"] + ".")
    FreeCAD.getDocument("DSPH_Case").saveAs(save_name + "/DSPH_Case.FCStd")
    FreeCADGui.SendMsgToActiveView("Save")
    f = open(save_name + "/" + save_name.split('/')[-1] + "_Def.xml", 'w')
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    f.write('<case app="' + data["project_name"] + '" date="' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + '">\n')
    f.write('\t<casedef>\n')
    f.write('\t\t<constantsdef>\n')
    f.write('\t\t\t<lattice bound="' + str(data['lattice_bound']) + '" fluid="' + str(data['lattice_fluid']) + '" />\n')
    f.write('\t\t\t<gravity x="' + str(data['gravity'][0]) + '" y="' + str(data['gravity'][1]) + '" z="' + str(data['gravity'][2]) + '" comment="Gravitational acceleration" units_comment="m/s^2" />\n')
    f.write('\t\t\t<rhop0 value="' + str(data['rhop0']) + '" comment="Reference density of the fluid" units_comment="kg/m^3" />\n')
    f.write('\t\t\t<hswl value="' + str(data['hswl']) + '" auto="' + str(data['hswl_auto']).lower() + '" comment="Maximum still water level to calculate speedofsound using coefsound" units_comment="metres (m)"  />\n')
    f.write('\t\t\t<gamma value="' + str(data['gamma']) + '" comment="Polytropic constant for water used in the state equation" />\n')
    f.write('\t\t\t<speedsystem value="' + str(data['speedsystem']) + '" auto="' + str(data['speedsystem_auto']).lower() + '" comment="Maximum system speed (by default the dam-break propagation is used)" />\n')
    f.write('\t\t\t<coefsound value="' + str(data['coefsound']) + '" comment="Coefficient to multiply speedsystem" />\n')
    f.write('\t\t\t<speedsound value="' + str(data['speedsound']) + '" auto="' + str(data['speedsound_auto']).lower() + '" comment="Speed of sound to use in the simulation (by default speedofsound=coefsound*speedsystem)" />\n')
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
    f.write('\t\t\t\t<pointmin x="' + str((min_point.x / 1000) - (data['dp'] * 10)) + '" y="' + str((min_point.y / 1000) - (data['dp'] * 10)) + '" z="' + str((min_point.z / 1000) - (data['dp'] * 10)) + '" />\n')
    f.write('\t\t\t\t<pointmax x="' + str((min_point.x / 1000 + max_point.Length.Value / 1000) + (data['dp'] * 10)) + '" y="' + str((min_point.y / 1000 + max_point.Width.Value / 1000) + (data['dp'] * 10)) + '" z="' + str((min_point.z / 1000 + max_point.Height.Value / 1000) + (data['dp']) * 10) + '" />\n')
    f.write('\t\t\t</definition>\n')
    f.write('\t\t\t<commands>\n')
    f.write('\t\t\t\t<mainlist>\n')
    #Export in strict order
    for key in data["export_order"]:
        name = key
        valuelist = data["simobjects"][name]
        o = FreeCAD.getDocument("DSPH_Case").getObject(name)
        #Ignores case limits
        if (name != "Case_Limits"):
            #Sets MKfluid or bound depending on object properties and resets
            #the matrix
            f.write('\t\t\t\t\t<matrixreset />\n')
            if valuelist[1].lower() == "fluid":
                f.write('\t\t\t\t\t<setmkfluid mk="' + str(valuelist[0]) + '"/>\n')
            elif valuelist[1].lower() == "bound":
                f.write('\t\t\t\t\t<setmkbound mk="' + str(valuelist[0]) + '"/>\n')
            f.write('\t\t\t\t\t<setdrawmode mode="' + valuelist[2].lower() + '"/>\n')
            """ Exports supported objects in a xml parametric mode.
            If specal objects are found, exported in an specific manner (p.e FillBox)
            The rest of the things are exported in STL format."""
            if o.TypeId == "Part::Box":
                f.write('\t\t\t\t\t<move x="' + str(o.Placement.Base.x / 1000) + '" y="' + str(o.Placement.Base.y / 1000) + '" z="' + str(o.Placement.Base.z / 1000) + '" />\n')
                f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' + str(-o.Placement.Rotation.Axis.x) + '" y="' + str(-o.Placement.Rotation.Axis.y) + '" z="' + str(-o.Placement.Rotation.Axis.z) + '" />\n')
                f.write('\t\t\t\t\t<drawbox>\n')
                f.write('\t\t\t\t\t\t<boxfill>solid</boxfill>\n')
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t\t<size x="' + str(o.Length.Value / 1000) + '" y="' + str(o.Width.Value / 1000) + '" z="' + str(o.Height.Value / 1000) + '" />\n')
                f.write('\t\t\t\t\t</drawbox>\n')
            elif o.TypeId == "Part::Sphere":
                f.write('\t\t\t\t\t<move x="' + str(o.Placement.Base.x / 1000) + '" y="' + str(o.Placement.Base.y / 1000) + '" z="' + str(o.Placement.Base.z / 1000) + '" />\n')
                f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' + str(-o.Placement.Rotation.Axis.x) + '" y="' + str(-o.Placement.Rotation.Axis.y) + '" z="' + str(-o.Placement.Rotation.Axis.z) + '" />\n')
                f.write('\t\t\t\t\t<drawsphere radius="' + str(o.Radius.Value / 1000) + '">\n')
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t</drawsphere>\n')
            elif o.TypeId == "Part::Cylinder":
                f.write('\t\t\t\t\t<move x="' + str(o.Placement.Base.x / 1000) + '" y="' + str(o.Placement.Base.y / 1000) + '" z="' + str(o.Placement.Base.z / 1000) + '" />\n')
                f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(o.Placement.Rotation.Angle)) + '" x="' + str(-o.Placement.Rotation.Axis.x) + '" y="' + str(-o.Placement.Rotation.Axis.y) + '" z="' + str(-o.Placement.Rotation.Axis.z) + '" />\n')
                f.write('\t\t\t\t\t<drawcylinder radius="' + str(o.Radius.Value / 1000) + '">\n')
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                f.write('\t\t\t\t\t\t<point x="0" y="0" z="' + str((0 + o.Height.Value) / 1000) + '" />\n')
                f.write('\t\t\t\t\t</drawcylinder>\n')
            else:
                #Watch if it is a fillbox group
                if o.TypeId == "App::DocumentObjectGroup" and "fillbox" in o.Name.lower():
                    filllimits = None
                    fillpoint = None
                    for element in o.OutList:
                        if "filllimit" in element.Name.lower():
                            filllimits = element
                        elif "fillpoint" in element.Name.lower():
                            fillpoint = element
                    if filllimits and fillpoint:
                        f.write('\t\t\t\t\t<move x="' + str(filllimits.Placement.Base.x / 1000) + '" y="' + str(filllimits.Placement.Base.y / 1000) + '" z="' + str(filllimits.Placement.Base.z / 1000) + '" />\n')
                        f.write('\t\t\t\t\t<rotate ang="' + str(math.degrees(filllimits.Placement.Rotation.Angle)) + '" x="' + str(-filllimits.Placement.Rotation.Axis.x) + '" y="' + str(-filllimits.Placement.Rotation.Axis.y) + '" z="' + str(-filllimits.Placement.Rotation.Axis.z) + '" />\n')
                        f.write('\t\t\t\t\t<fillbox x="' + str((fillpoint.Placement.Base.x - filllimits.Placement.Base.x) / 1000) + '" y="' + str((fillpoint.Placement.Base.y - filllimits.Placement.Base.y) / 1000) + '" z="' + str((fillpoint.Placement.Base.z - filllimits.Placement.Base.z) / 1000) + '">\n')
                        f.write('\t\t\t\t\t\t<modefill>void</modefill>\n')
                        f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                        f.write('\t\t\t\t\t\t<size x="' + str(filllimits.Length.Value / 1000) + '" y="' + str(filllimits.Width.Value / 1000) + '" z="' + str(filllimits.Height.Value / 1000) + '" />\n')
                        f.write('\t\t\t\t\t\t<matrixreset />\n')
                        f.write('\t\t\t\t\t</fillbox>\n')
                    else:
                        #Something went wrong, one of the needed objects is not
                        #in the fillbox group
                        error("Limits or point missing in a fillbox group. Ignoring it")
                        continue
                else:
                    #Not a xml parametric object.  Needs exporting
                    __objs__ = []
                    __objs__.append(o)
                    Mesh.export(__objs__,save_name + "/" + o.Name + ".stl")
                    f.write('\t\t\t\t\t<drawfilestl file="' + o.Name + ".stl" + '" >\n')
                    f.write('\t\t\t\t\t\t<drawscale x="0.001" y="0.001" z="0.001" />\n')
                    f.write('\t\t\t\t\t</drawfilestl>\n')
                    del __objs__
    f.write('\t\t\t\t</mainlist>\n')
    f.write('\t\t\t</commands>\n')
    f.write('\t\t</geometry>\n')
    #Writes initials
    if len(data["initials_mks"].keys()) > 0:
        f.write('\t\t<initials>\n')
        for key, value in data["initials_mks"].iteritems():
            f.write('\t\t\t<velocity mkfluid="' + str(key) + '" x="' + str(value[0]) + '" y="' + str(value[1]) + '" z="' + str(value[2]) + '"/>\n')
        f.write('\t\t</initials>\n')
    #Writes floatings
    if len(data["floating_mks"].keys()) > 0:
        f.write('\t\t<floatings>\n')
        for key, value in data["floating_mks"].iteritems():
            if value[0][0] == 0:
                #is massbody
                f.write('\t\t\t<floating mkbound="' + str(key) + '">\n')
                f.write('\t\t\t\t<massbody value="' + str(value[0][1]) + '" />\n')
            else:
                #is rhopbody
                f.write('\t\t\t<floating mkbound="' + str(key) + '" rhopbody="' + str(value[0][1]) + '">\n')
            if not value[1][0]:
                f.write('\t\t\t\t<center x="' + str(value[1][1]) + '" y="' + str(value[1][2]) + '" z="' + str(value[1][3]) + '" />\n')
            if not value[2][0]:
                f.write('\t\t\t\t<inertia x="' + str(value[2][1]) + '" y="' + str(value[2][2]) + '" z="' + str(value[2][3]) + '" />\n')
            if not value[3][0]:
                f.write('\t\t\t\t<velini x="' + str(value[3][1]) + '" y="' + str(value[3][2]) + '" z="' + str(value[3][3]) + '" />\n')
            if not value[4][0]:
                f.write('\t\t\t\t<omegaini x="' + str(value[4][1]) + '" y="' + str(value[4][2]) + '" z="' + str(value[4][3]) + '" />\n')
            f.write('\t\t\t</floating>\n')
        f.write('\t\t</floatings>\n')
    f.write('\t</casedef>\n')
    f.write('\t<execution>\n')
    f.write('\t\t<parameters>\n')
    #Writes parameters as user introduced
    f.write('\t\t\t<parameter key="PosDouble" value="' + str(data['posdouble']) + '" comment="Precision in particle interaction 0:Simple, 1:Double, 2:Uses and saves double (default=0)" />\n')
    f.write('\t\t\t<parameter key="StepAlgorithm" value="' + str(data['stepalgorithm']) + '" comment="Step Algorithm 1:Verlet, 2:Symplectic (default=1)" />\n')
    f.write('\t\t\t<parameter key="VerletSteps" value="' + str(data['verletsteps']) + '" comment="Verlet only: Number of steps to apply Euler timestepping (default=40)" />\n')
    f.write('\t\t\t<parameter key="Kernel" value="' + str(data['kernel']) + '" comment="Interaction Kernel 1:Cubic Spline, 2:Wendland (default=2)" />\n')
    f.write('\t\t\t<parameter key="ViscoTreatment" value="' + str(data['viscotreatment']) + '" comment="Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)" />\n')
    f.write('\t\t\t<parameter key="Visco" value="' + str(data['visco']) + '" comment="Viscosity value" /> % Note alpha can depend on the resolution. A value of 0.01 is recommended for near irrotational flows.\n')
    f.write('\t\t\t<parameter key="ViscoBoundFactor" value="' + str(data['viscoboundfactor']) + '" comment="Multiply viscosity value with boundary (default=1)" />\n')
    f.write('\t\t\t<parameter key="DeltaSPH" value="' + str(data['deltasph']) + '" comment="DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0)" />\n')
    f.write('\t\t\t<parameter key="#Shifting" value="' + str(data['shifting']) + '" comment="Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0)" />\n')
    f.write('\t\t\t<parameter key="#ShiftCoef" value="' + str(data['shiftcoef']) + '" comment="Coefficient for shifting computation (default=-2)" />\n')
    f.write('\t\t\t<parameter key="#ShiftTFS" value="' + str(data['shifttfs']) + '" comment="Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0)" />\n')
    f.write('\t\t\t<parameter key="RigidAlgorithm" value="' + str(data['rigidalgorithm']) + '" comment="Rigid Algorithm 1:SPH, 2:DEM (default=1)" />\n')
    f.write('\t\t\t<parameter key="FtPause" value="' + str(data['ftpause']) + '" comment="Time to freeze the floatings at simulation start (warmup) (default=0)" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="CoefDtMin" value="' + str(data['coefdtmin']) + '" comment="Coefficient to calculate minimum time step dtmin=coefdtmin*h/speedsound (default=0.05)" />\n')
    comment = ""
    if data["dtini_auto"]:
        comment = "#"
    else:
        comment = ""
    f.write('\t\t\t<parameter key="' + comment + 'DtIni" value="' + str(data['dtini']) + '" comment="Initial time step (default=h/speedsound)" units_comment="seconds" />\n')
    comment = ""
    if data["dtmin_auto"]:
        comment = "#"
    else:
        comment = ""
    f.write('\t\t\t<parameter key="' + comment + 'DtMin" value="' + str(data['dtmin']) + '" comment="Minimum time step (default=coefdtmin*h/speedsound)" units_comment="seconds" />\n')
    #f.write('\t\t\t<parameter key="#DtFixed" value="'+str(data['dtfixed'])+'"
    #comment="Dt values are loaded from file (default=disabled)" />\n')
    f.write('\t\t\t<parameter key="DtAllParticles" value="' + str(data['dtallparticles']) + '" comment="Velocity of particles used to calculate DT. 1:All, 0:Only fluid/floating (default=0)" />\n')
    f.write('\t\t\t<parameter key="TimeMax" value="' + str(data['timemax']) + '" comment="Time of simulation" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="TimeOut" value="' + str(data['timeout']) + '" comment="Time out data" units_comment="seconds" />\n')
    f.write('\t\t\t<parameter key="IncZ" value="' + str(data['incz']) + '" comment="Increase of Z+" units_comment="decimal" />\n')
    f.write('\t\t\t<parameter key="PartsOutMax" value="' + str(data['partsoutmax']) + '" comment="%/100 of fluid particles allowed to be excluded from domain (default=1)" units_comment="decimal" />\n')
    f.write('\t\t\t<parameter key="RhopOutMin" value="' + str(data['rhopoutmin']) + '" comment="Minimum rhop valid (default=700)" units_comment="kg/m^3" />\n')
    f.write('\t\t\t<parameter key="RhopOutMax" value="' + str(data['rhopoutmax']) + '" comment="Maximum rhop valid (default=1300)" units_comment="kg/m^3" />\n')
    f.write('\t\t</parameters>\n')
    f.write('\t</execution>\n')
    f.write('</case>\n')
    f.close()