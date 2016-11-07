# -*- coding: utf-8 -*-

'''
Copyright (C) 2016 - Andrés Vieira (anvieiravazquez@gmail.com)
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DualSPHysics for FreeCAD.

DualSPHysics for FreeCAD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DualSPHysics for FreeCAD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DualSPHysics for FreeCAD.  If not, see <http://www.gnu.org/licenses/>.
'''

import FreeCAD, FreeCADGui, os, guiutils, traceback, pickle, webbrowser
import guiutils
from PySide import QtGui, QtCore

#------ CONSTANTS DEFINITION ------
FREECAD_MIN_VERSION = "016"
#------ END CONSTANTS DEFINITION ------

def is_compatible_version():
    '''Checks if the current FreeCAD version is suitable
    for this macro.'''

    version_num = FreeCAD.Version()[0] + FreeCAD.Version()[1]
    if int(version_num) < int(FREECAD_MIN_VERSION):
        guiutils.warning_dialog("This version of FreeCAD is not supported!. Install version 0.16 or higher.")
        return False
    else:
        return True

def check_executables(gencase_path, dsphysics_path, partvtk4_path):
    '''Checks the three needed executables for working with
    this software. Returns 4 values: 3 string paths and a boolean.
    If some path is not correct returns the respective empty string and False.'''

    execs_correct = True
    #Tries to identify gencase
    if os.path.isfile(gencase_path):
        process = QtCore.QProcess(FreeCADGui.getMainWindow())
        process.start(gencase_path)
        process.waitForFinished()
        output = str(process.readAllStandardOutput())
        if "gencase" in output[0:15].lower():
            print "DualSPHysics for FreeCAD: Found correct GenCase."
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
            print "DualSPHysics for FreeCAD: Found correct DualSPHysics."
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
            print "DualSPHysics for FreeCAD: Found correct PartVTK4."
        else:
            execs_correct = False    
            partvtk4_path = ""
    else:
        execs_correct = False
        partvtk4_path = ""            

    #Spawn warning dialog and return paths.
    if not execs_correct:
        print "WARNING: One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries"
        guiutils.warning_dialog("One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries.")
    return gencase_path, dsphysics_path, partvtk4_path, execs_correct

def get_default_data():
    '''Sets default data at start of the macro.
    Returns data and temp_data dict with default values.
    If there is data saved on disk, tries to load it.'''

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
    
    '''Dictionary that defines floatings. 
    Keys are mks enabled (ONLY BOUNDS) and values are a list containing:
    {'mkbound': [massrhop, center, inertia, velini, omegaini]}
    massrhop = [selectedOption (index), value]
    center = [auto (bool), x,y,z]
    inertia = [auto (bool), x,y,z]
    velini = [auto (bool), x,y,z]
    omegaini = [auto (bool), x,y,z]'''
    data['floating_mks'] = dict()

    '''Dictionary that defines initials. 
    Keys are mks enabled (ONLY FLUIDS) and values are a list containing:
    {'mkfluid': [x, y, z]}'''
    data['initials_mks'] = dict()

    #Control data for enabling features
    data['gencase_done'] = False
    data['simulation_done'] = False

    #Simulation objects with its parameters. Without order.
    #format is: {'key': ['mk', 'type', 'fill']}
    data['simobjects'] = dict()

    #Keys of simobjects. Ordered.
    data['export_order'] = []

    #Temporal data dict to control execution features.
    temp_data['current_process'] = None
    temp_data['stored_selection'] = []
    temp_data['export_numparts'] = ""
    temp_data['total_export_parts'] = -1
    temp_data['supported_types'] = ["Part::Box", "Part::Sphere", "Part::Cylinder"]

    '''Try to load saved paths. This way the user does not need
    to introduce the software paths every time'''
    if os.path.isfile(FreeCAD.getUserAppDataDir()+'/dsph_data.dsphdata'):
        try:
            picklefile = open(FreeCAD.getUserAppDataDir()+'/dsph_data.dsphdata', 'rb')
            disk_data = pickle.load(picklefile)
            data['gencase_path'] = disk_data['gencase_path']
            data['dsphysics_path'] = disk_data['dsphysics_path']
            data['partvtk4_path'] = disk_data['partvtk4_path']
        except:
            traceback.print_exc()
            data['gencase_path'] = ""
            data['dsphysics_path'] = ""
            data['partvtk4_path'] = ""
    
        print "DualSPHysics for FreeCAD: Found data file. Loading data from disk."
        data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'], state = check_executables(data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'])
    else:
        data["project_path"] = "" 
        data["project_name"] = ""


    return data, temp_data

def get_first_mk_not_used(objtype, data):
    '''Checks simulation objects to find the first not used
    MK group.'''

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
    '''Opens a web browser with this software help.'''

    webbrowser.open("http://dual.sphysics.org/gui/wiki/")

def print_license():
    '''Prints this software license'''
    licpath = os.path.abspath(__file__).split("dsphfc")[0] + "LICENSE"
    if os.path.isfile(licpath):
        with open(licpath) as licfile:
            print licfile.read()
    else:
        raise EnvironmentError("LICENSE file could not be found. Are you sure you didn't delete it?")