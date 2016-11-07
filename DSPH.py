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

import FreeCAD, FreeCADGui
import sys, os, pickle, threading, math, webbrowser, traceback, glob, numpy
from PySide import QtGui, QtCore
from datetime import datetime
from dsphfc import utils, guiutils

#Special vars
version = 'v0.11a'

utils.print_license()

#Version check. This script is only compatible with FreeCAD 0.16 or higher
is_compatible = utils.is_compatible_version()
if not is_compatible:
    raise EnvironmentError("This FreeCAD version is not compatible. Please update FreeCAD to version 0.16 or higher.")

#Main data structure
data = dict()
temp_data = dict()

#Establishing references for the different elements that the script will use later
fc_main_window = FreeCADGui.getMainWindow()
dsph_main_dock = QtGui.QDockWidget()
dsph_main_dock_scaff_widget = QtGui.QWidget() #Scaffolding widget, only useful to apply to the dsph_dock widget

#Executes the default data function the first time
default_data, default_temp_data = utils.get_default_data()
data.update(default_data)
temp_data.update(default_temp_data)

'''The script needs only one document open, called DSHP_Case.
This section tries to close all the current documents.'''
if len(FreeCAD.listDocuments().keys()) > 0:
    user_selection = guiutils.ok_cancel_dialog("DualSPHysics for FreeCAD", "To load this module you must close all current documents. Close all the documents?")
    if user_selection == QtGui.QMessageBox.Ok:
        #Close all current documents.
        print "DualSPHysics for FreeCAD: Closing all current documents"
        for doc in FreeCAD.listDocuments().keys():
            FreeCAD.closeDocument(doc)
    else:
        quit()

'''If the script is executed even when a previous DSHP Dock is created
it makes sure that it's deleted before'''
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, "DSPH Widget")
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

#Creation of the DSPH Widget
dsph_main_dock.setObjectName("DSPH Widget")
dsph_main_dock.setWindowTitle("DualSPHysics for FreeCAD " + str(version))
#Main Widget layout. Vertical ordering
main_layout = QtGui.QVBoxLayout()
#Component layouts definition
logo_layout = QtGui.QHBoxLayout()
intro_layout = QtGui.QVBoxLayout()
#Components by layout
constants_label = QtGui.QLabel("\nConstant Definition and Execution Parameters: \nYou can modify values to customize the simulation. If not set, the parameters would be at default values.")
constants_label.setWordWrap(True)
constants_button = QtGui.QPushButton("Define Constants")
constants_button.setToolTip("Use this button to define case constants,\nsuch as lattice, gravity or fluid reference density.")
constants_button.clicked.connect(lambda: guiutils.def_constants_window(data))
help_button = QtGui.QPushButton("Help")
help_button.setToolTip("Push this button to open a browser with help\non how to use this tool.")
help_button.clicked.connect(utils.open_help)
setup_button = QtGui.QPushButton("Setup Plugin")
setup_button.setToolTip("Setup of the simulator executables")
setup_button.clicked.connect(lambda: guiutils.def_setup_window(data))
execparams_button = QtGui.QPushButton("Execution Parameters")
execparams_button.setToolTip("Change execution parameters, such as\ntime of simulation, viscosity, etc.")
execparams_button.clicked.connect(lambda: guiutils.def_execparams_window(data))
constants_separator = QtGui.QFrame()
constants_separator.setFrameStyle(QtGui.QFrame.HLine)
crucialvars_separator = QtGui.QFrame()
crucialvars_separator.setFrameStyle(QtGui.QFrame.HLine)
#Logo layout related operations
logo_label = QtGui.QLabel()
logo_label.setPixmap(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/logo.png")
#DP introduction
def on_dp_changed():
    data['dp'] = float(dp_input.text())
dp_layout = QtGui.QHBoxLayout()
dp_label = QtGui.QLabel("Inter-particle distance: ")
dp_label.setToolTip("Lower DP to have more particles in the case.\nUpper it to ease times of simulation.\nNote that more DP implies more quality in the final result.")
dp_input = QtGui.QLineEdit()
dp_input.setToolTip("Lower DP to have more particles in the case.\nUpper it to ease times of simulation.\nNote that more DP implies more quality in the final result.")
dp_label2 = QtGui.QLabel(" meters")
dp_input.setMaxLength(10)
dp_input.setText(str(data["dp"]))
dp_input.textChanged.connect(on_dp_changed)
dp_validator = QtGui.QDoubleValidator(0.0, 100, 8, dp_input)
dp_input.setValidator(dp_validator)
dp_layout.addWidget(dp_label)
dp_layout.addWidget(dp_input)
dp_layout.addWidget(dp_label2)
#Case control part
cc_layout = QtGui.QVBoxLayout()
cclabel_layout = QtGui.QHBoxLayout()
ccfilebuttons_layout = QtGui.QHBoxLayout()
ccaddbuttons_layout = QtGui.QHBoxLayout()
casecontrols_label = QtGui.QLabel("Use these controls to define the Case you want to simulate.")
casecontrols_bt_newdoc = QtGui.QPushButton("  New Case")
casecontrols_bt_newdoc.setToolTip("Creates a new case. \nThe current documents opened will be closed.")
casecontrols_bt_newdoc.setIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/new.png"));
casecontrols_bt_newdoc.setIconSize(QtCore.QSize(28,28));
casecontrols_bt_savedoc = QtGui.QPushButton("  Save Case")
casecontrols_bt_savedoc.setToolTip("Saves the case and executes GenCase over.\nIf GenCase fails or is not set up, only the case\nwill be saved.")
casecontrols_bt_savedoc.setIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/save.png"));
casecontrols_bt_savedoc.setIconSize(QtCore.QSize(28,28));
casecontrols_bt_loaddoc = QtGui.QPushButton("  Load Case")
casecontrols_bt_loaddoc.setToolTip("Loads a case from disk. All the current documents\nwill be closed.")
casecontrols_bt_loaddoc.setIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Macro/DSPH_Images/load.png"));
casecontrols_bt_loaddoc.setIconSize(QtCore.QSize(28,28));
casecontrols_bt_addfillbox = QtGui.QPushButton("Add fillbox")
casecontrols_bt_addfillbox.setToolTip("Adds a FillBox. A FillBox is able to fill an empty space\nwithin limits of geometry and a maximum bounding\nbox placed by the user.")
casecontrols_bt_addfillbox.setEnabled(False)
casecontrols_bt_addstl = QtGui.QPushButton("Import STL")
casecontrols_bt_addstl.setToolTip("Imports a STL with postprocessing. This way you can set the scale of the imported object.")
casecontrols_bt_addstl.setEnabled(False)

def on_new_case():
    '''Defines what happens when new case is clicked. Closes all documents
    if possible and creates a FreeCAD document with Case Limits object.'''
    if len(FreeCAD.listDocuments().keys()) > 0:
        newConfirmDialog = QtGui.QMessageBox()
        newConfirmDialog.setText("DualSPHysics for FreeCAD")
        newConfirmDialog.setInformativeText("To make a new case you must close all the open documents. Close all the documents?")
        newConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        newConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
        openCDRet = newConfirmDialog.exec_()

        if openCDRet == QtGui.QMessageBox.Ok:
            print "DualSPHysics for FreeCAD: New File. Closing all documents..."
            for doc in FreeCAD.listDocuments().keys():
                FreeCAD.closeDocument(doc)
        else:
            return

    FreeCAD.newDocument("DSPH_Case")
    FreeCAD.setActiveDocument("DSPH_Case")
    FreeCAD.ActiveDocument=FreeCAD.getDocument("DSPH_Case")
    Gui.ActiveDocument=Gui.getDocument("DSPH_Case")
    Gui.activateWorkbench("PartWorkbench")
    Gui.activeDocument().activeView().viewAxonometric()
    FreeCAD.ActiveDocument.addObject("Part::Box","Case_Limits")
    FreeCAD.ActiveDocument.getObject("Case_Limits").Label = "Case_Limits"
    FreeCAD.ActiveDocument.getObject("Case_Limits").Length = '15 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Width = '15 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Height = '15 mm'
    FreeCAD.ActiveDocument.getObject("Case_Limits").Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    Gui.ActiveDocument.getObject("Case_Limits").DisplayMode = "Wireframe"
    Gui.ActiveDocument.getObject("Case_Limits").LineColor = (1.00,0.00,0.00)
    Gui.ActiveDocument.getObject("Case_Limits").LineWidth = 2.00
    Gui.ActiveDocument.getObject("Case_Limits").Selectable = False
    FreeCAD.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")
    default_data, default_temp_data = utils.get_default_data()
    data.update(default_data)
    temp_data.update(default_temp_data)
    constants_button.setEnabled(True)
    execparams_button.setEnabled(True)
    casecontrols_bt_savedoc.setEnabled(True)
    dp_input.setEnabled(True)
    ex_selector_combo.setEnabled(False)
    ex_button.setEnabled(False)
    ex_additional.setEnabled(False)
    export_button.setEnabled(False)
    exportopts_button.setEnabled(False)
    casecontrols_bt_addfillbox.setEnabled(True)
    casecontrols_bt_addstl.setEnabled(True)
    data['simobjects']['Case_Limits'] = ["mkspecial", "typespecial", "fillspecial"]
    on_tree_item_selection_change()

def on_save_case():
    '''Defines what happens when save case button is clicked.
    Saves a freecad scene definition, a dump of dsph data useful for this macro
    and tries to generate a case with gencase.'''
    #Watch if save path is available. Prompt the user if not.
    if (data["project_path"] == "") and (data["project_name"] == ""):
        saveName, _ = QtGui.QFileDialog.getSaveFileName(dsph_main_dock, "Save Case", QtCore.QDir.homePath())
    else:
        saveName = data["project_path"]
    if saveName != '' :
        if not os.path.exists(saveName):
            os.makedirs(saveName)
        data["project_path"] = saveName
        data["project_name"] = saveName.split('/')[-1]
        
        #Watch if folder already exists or create it
        if not os.path.exists(saveName+"/"+saveName.split('/')[-1]+ "_Out"):
            os.makedirs(saveName+"/"+saveName.split('/')[-1]+ "_Out")

        #Saves all the data in XML format.
        print "DualSPHysics for FreeCAD: Saving data in " + data["project_path"] + "."
        FreeCAD.getDocument("DSPH_Case").saveAs(saveName+"/DSPH_Case.FCStd")
        Gui.SendMsgToActiveView("Save")
        f = open(saveName+"/" + saveName.split('/')[-1]+ "_Def.xml", 'w')
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        f.write('<case app="' + data["project_name"] + '" date="' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + '">\n')
        f.write('\t<casedef>\n')
        f.write('\t\t<constantsdef>\n')
        f.write('\t\t\t<lattice bound="'+str(data['lattice_bound'])+'" fluid="'+str(data['lattice_fluid'])+'" />\n')
        f.write('\t\t\t<gravity x="'+str(data['gravity'][0])+'" y="'+str(data['gravity'][1])+'" z="'+str(data['gravity'][2])+'" comment="Gravitational acceleration" units_comment="m/s^2" />\n')
        f.write('\t\t\t<rhop0 value="'+str(data['rhop0'])+'" comment="Reference density of the fluid" units_comment="kg/m^3" />\n')
        f.write('\t\t\t<hswl value="'+str(data['hswl'])+'" auto="'+str(data['hswl_auto']).lower()+'" comment="Maximum still water level to calculate speedofsound using coefsound" units_comment="metres (m)"  />\n')
        f.write('\t\t\t<gamma value="'+str(data['gamma'])+'" comment="Polytropic constant for water used in the state equation" />\n')
        f.write('\t\t\t<speedsystem value="'+str(data['speedsystem'])+'" auto="'+str(data['speedsystem_auto']).lower()+'" comment="Maximum system speed (by default the dam-break propagation is used)" />\n')
        f.write('\t\t\t<coefsound value="'+str(data['coefsound'])+'" comment="Coefficient to multiply speedsystem" />\n')
        f.write('\t\t\t<speedsound value="'+str(data['speedsound'])+'" auto="'+str(data['speedsound_auto']).lower()+'" comment="Speed of sound to use in the simulation (by default speedofsound=coefsound*speedsystem)" />\n')
        f.write('\t\t\t<coefh value="'+str(data['coefh'])+'" comment="Coefficient to calculate the smoothing length (h=coefh*sqrt(3*dp^2) in 3D)" />\n')
        f.write('\t\t\t<cflnumber value="'+str(data['cflnumber'])+'" comment="Coefficient to multiply dt" />\n')
        f.write('\t\t\t<h value="'+str(data['h'])+'" auto="'+str(data['h_auto']).lower()+'" units_comment="metres (m)" />\n')
        f.write('\t\t\t<b value="'+str(data['b'])+'" auto="'+str(data['b_auto']).lower()+'" units_comment="metres (m)" />\n')
        f.write('\t\t\t<massbound value="'+str(data['massbound'])+'" auto="'+str(data['massbound_auto']).lower()+'" units_comment="kg" />\n')
        f.write('\t\t\t<massfluid value="'+str(data['massfluid'])+'" auto="'+str(data['massfluid_auto']).lower()+'" units_comment="kg" />\n')
        f.write('\t\t</constantsdef>\n')
        f.write('\t\t<mkconfig boundcount="240" fluidcount="10">\n')
        f.write('\t\t</mkconfig>\n')
        f.write('\t\t<geometry>\n')
        f.write('\t\t\t<definition dp="'+str(data['dp'])+'" comment="Initial inter-particle distance" units_comment="metres (m)">\n')
        min_point = FreeCAD.ActiveDocument.getObject("Case_Limits").Placement.Base
        max_point = FreeCAD.ActiveDocument.getObject("Case_Limits")
        f.write('\t\t\t\t<pointmin x="'+str(min_point.x / 1000)+'" y="'+str(min_point.y / 1000)+'" z="'+str(min_point.z / 1000)+'" />\n')
        f.write('\t\t\t\t<pointmax x="'+str(min_point.x / 1000 + max_point.Length.Value / 1000)+'" y="'+str(min_point.y / 1000 + max_point.Width.Value / 1000)+'" z="'+str(min_point.z / 1000 + max_point.Height.Value / 1000)+'" />\n')
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
                #Sets MKfluid or bound depending on object properties and resets the matrix
                f.write('\t\t\t\t\t<matrixreset />\n')
                if valuelist[1].lower() == "fluid":
                    f.write('\t\t\t\t\t<setmkfluid mk="'+str(valuelist[0])+'"/>\n')
                elif valuelist[1].lower() == "bound":
                    f.write('\t\t\t\t\t<setmkbound mk="'+str(valuelist[0])+'"/>\n')
                f.write('\t\t\t\t\t<setdrawmode mode="'+valuelist[2].lower()+'"/>\n')
                ''' Exports supported objects in a xml parametric mode.
                If specal objects are found, exported in an specific manner (p.e FillBox)
                The rest of the things are exported in STL format.'''
                if o.TypeId == "Part::Box":
                    f.write('\t\t\t\t\t<move x="'+str(o.Placement.Base.x / 1000)+'" y="'+str(o.Placement.Base.y / 1000)+'" z="'+str(o.Placement.Base.z / 1000)+'" />\n')
                    f.write('\t\t\t\t\t<rotate ang="'+str(math.degrees(o.Placement.Rotation.Angle))+'" x="'+str(-o.Placement.Rotation.Axis.x)+'" y="'+str(-o.Placement.Rotation.Axis.y)+'" z="'+str(-o.Placement.Rotation.Axis.z)+'" />\n')
                    f.write('\t\t\t\t\t<drawbox>\n')
                    f.write('\t\t\t\t\t\t<boxfill>solid</boxfill>\n')
                    f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                    f.write('\t\t\t\t\t\t<size x="'+str(o.Length.Value / 1000)+'" y="'+str(o.Width.Value / 1000)+'" z="'+str(o.Height.Value / 1000)+'" />\n')
                    f.write('\t\t\t\t\t</drawbox>\n')
                elif o.TypeId == "Part::Sphere":
                    f.write('\t\t\t\t\t<move x="'+str(o.Placement.Base.x / 1000)+'" y="'+str(o.Placement.Base.y / 1000)+'" z="'+str(o.Placement.Base.z / 1000)+'" />\n')
                    f.write('\t\t\t\t\t<rotate ang="'+str(math.degrees(o.Placement.Rotation.Angle))+'" x="'+str(-o.Placement.Rotation.Axis.x)+'" y="'+str(-o.Placement.Rotation.Axis.y)+'" z="'+str(-o.Placement.Rotation.Axis.z)+'" />\n')
                    f.write('\t\t\t\t\t<drawsphere radius="'+str(o.Radius.Value / 1000)+'">\n')
                    f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                    f.write('\t\t\t\t\t</drawsphere>\n')
                elif o.TypeId == "Part::Cylinder":
                    f.write('\t\t\t\t\t<move x="'+str(o.Placement.Base.x / 1000)+'" y="'+str(o.Placement.Base.y / 1000)+'" z="'+str(o.Placement.Base.z / 1000)+'" />\n')
                    f.write('\t\t\t\t\t<rotate ang="'+str(math.degrees(o.Placement.Rotation.Angle))+'" x="'+str(-o.Placement.Rotation.Axis.x)+'" y="'+str(-o.Placement.Rotation.Axis.y)+'" z="'+str(-o.Placement.Rotation.Axis.z)+'" />\n')
                    f.write('\t\t\t\t\t<drawcylinder radius="'+str(o.Radius.Value / 1000)+'">\n')
                    f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                    f.write('\t\t\t\t\t\t<point x="0" y="0" z="'+str((0 + o.Height.Value) / 1000)+'" />\n')
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
                            f.write('\t\t\t\t\t<move x="'+str(filllimits.Placement.Base.x / 1000)+'" y="'+str(filllimits.Placement.Base.y / 1000)+'" z="'+str(filllimits.Placement.Base.z / 1000)+'" />\n')
                            f.write('\t\t\t\t\t<rotate ang="'+str(math.degrees(filllimits.Placement.Rotation.Angle))+'" x="'+str(-filllimits.Placement.Rotation.Axis.x)+'" y="'+str(-filllimits.Placement.Rotation.Axis.y)+'" z="'+str(-filllimits.Placement.Rotation.Axis.z)+'" />\n')
                            f.write('\t\t\t\t\t<fillbox x="'+str((fillpoint.Placement.Base.x - filllimits.Placement.Base.x) / 1000)+'" y="'+str((fillpoint.Placement.Base.y - filllimits.Placement.Base.y) / 1000)+'" z="'+str((fillpoint.Placement.Base.z - filllimits.Placement.Base.z) / 1000)+'">\n')
                            f.write('\t\t\t\t\t\t<modefill>void</modefill>\n')
                            f.write('\t\t\t\t\t\t<point x="0" y="0" z="0" />\n')
                            f.write('\t\t\t\t\t\t<size x="'+str(filllimits.Length.Value / 1000)+'" y="'+str(filllimits.Width.Value / 1000)+'" z="'+str(filllimits.Height.Value / 1000)+'" />\n')
                            f.write('\t\t\t\t\t\t<matrixreset />\n')
                            f.write('\t\t\t\t\t</fillbox>\n')
                        else:
                            #Something went wrong, one of the needed objects is not in the fillbox group
                            print "ERROR: Limits or point missing in a fillbox group. Ignoring it"
                            continue
                    else:
                        #Not a xml parametric object. Needs exporting
                        __objs__=[]
                        __objs__.append(o)
                        Mesh.export(__objs__,saveName + "/" + o.Name + ".stl")
                        f.write('\t\t\t\t\t<drawfilestl file="'+ o.Name + ".stl"+'" >\n')
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
                f.write('\t\t\t<velocity mkfluid="' + str(key) + '" x="' +str(value[0])+ '" y="' +str(value[1])+ '" z="' +str(value[2])+ '"/>\n')
            f.write('\t\t</initials>\n')
        #Writes floatings
        if len(data["floating_mks"].keys()) > 0:
            f.write('\t\t<floatings>\n')
            for key, value in data["floating_mks"].iteritems():
                if value[0][0] == 0:
                    #is massbody
                    f.write('\t\t\t<floating mkbound="'+str(key)+'">\n')
                    f.write('\t\t\t\t<massbody value="'+str(value[0][1])+'" />\n')
                else:
                    #is rhopbody
                    f.write('\t\t\t<floating mkbound="'+str(key)+'" rhopbody="'+str(value[0][1])+'">\n')
                if not value[1][0]:
                    f.write('\t\t\t\t<center x="'+str(value[1][1])+'" y="'+str(value[1][2])+'" z="'+str(value[1][3])+'" />\n')
                if not value[2][0]:
                    f.write('\t\t\t\t<inertia x="'+str(value[2][1])+'" y="'+str(value[2][2])+'" z="'+str(value[2][3])+'" />\n')
                if not value[3][0]:
                    f.write('\t\t\t\t<velini x="'+str(value[3][1])+'" y="'+str(value[3][2])+'" z="'+str(value[3][3])+'" />\n')
                if not value[4][0]:
                    f.write('\t\t\t\t<omegaini x="'+str(value[4][1])+'" y="'+str(value[4][2])+'" z="'+str(value[4][3])+'" />\n')
                f.write('\t\t\t</floating>\n')
            f.write('\t\t</floatings>\n')
        f.write('\t</casedef>\n')
        f.write('\t<execution>\n')
        f.write('\t\t<parameters>\n')
        #Writes parameters as user introduced
        f.write('\t\t\t<parameter key="PosDouble" value="'+str(data['posdouble'])+'" comment="Precision in particle interaction 0:Simple, 1:Double, 2:Uses and saves double (default=0)" />\n')
        f.write('\t\t\t<parameter key="StepAlgorithm" value="'+str(data['stepalgorithm'])+'" comment="Step Algorithm 1:Verlet, 2:Symplectic (default=1)" />\n')
        f.write('\t\t\t<parameter key="VerletSteps" value="'+str(data['verletsteps'])+'" comment="Verlet only: Number of steps to apply Euler timestepping (default=40)" />\n')
        f.write('\t\t\t<parameter key="Kernel" value="'+str(data['kernel'])+'" comment="Interaction Kernel 1:Cubic Spline, 2:Wendland (default=2)" />\n')
        f.write('\t\t\t<parameter key="ViscoTreatment" value="'+str(data['viscotreatment'])+'" comment="Viscosity formulation 1:Artificial, 2:Laminar+SPS (default=1)" />\n')
        f.write('\t\t\t<parameter key="Visco" value="'+str(data['visco'])+'" comment="Viscosity value" /> % Note alpha can depend on the resolution. A value of 0.01 is recommended for near irrotational flows.\n')
        f.write('\t\t\t<parameter key="ViscoBoundFactor" value="'+str(data['viscoboundfactor'])+'" comment="Multiply viscosity value with boundary (default=1)" />\n')
        f.write('\t\t\t<parameter key="DeltaSPH" value="'+str(data['deltasph'])+'" comment="DeltaSPH value, 0.1 is the typical value, with 0 disabled (default=0)" />\n')
        f.write('\t\t\t<parameter key="#Shifting" value="'+str(data['shifting'])+'" comment="Shifting mode 0:None, 1:Ignore bound, 2:Ignore fixed, 3:Full (default=0)" />\n')
        f.write('\t\t\t<parameter key="#ShiftCoef" value="'+str(data['shiftcoef'])+'" comment="Coefficient for shifting computation (default=-2)" />\n')
        f.write('\t\t\t<parameter key="#ShiftTFS" value="'+str(data['shifttfs'])+'" comment="Threshold to detect free surface. Typically 1.5 for 2D and 2.75 for 3D (default=0)" />\n')
        f.write('\t\t\t<parameter key="RigidAlgorithm" value="'+str(data['rigidalgorithm'])+'" comment="Rigid Algorithm 1:SPH, 2:DEM (default=1)" />\n')
        f.write('\t\t\t<parameter key="FtPause" value="'+str(data['ftpause'])+'" comment="Time to freeze the floatings at simulation start (warmup) (default=0)" units_comment="seconds" />\n')
        f.write('\t\t\t<parameter key="CoefDtMin" value="'+str(data['coefdtmin'])+'" comment="Coefficient to calculate minimum time step dtmin=coefdtmin*h/speedsound (default=0.05)" />\n')
        comment = ""
        if data["dtini_auto"]:
            comment = "#"
        else:
            comment = ""
        f.write('\t\t\t<parameter key="'+comment+'DtIni" value="'+str(data['dtini'])+'" comment="Initial time step (default=h/speedsound)" units_comment="seconds" />\n')
        comment = ""
        if data["dtmin_auto"]:
            comment = "#"
        else:
            comment = ""
        f.write('\t\t\t<parameter key="'+comment+'DtMin" value="'+str(data['dtmin'])+'" comment="Minimum time step (default=coefdtmin*h/speedsound)" units_comment="seconds" />\n')
        #f.write('\t\t\t<parameter key="#DtFixed" value="'+str(data['dtfixed'])+'" comment="Dt values are loaded from file (default=disabled)" />\n')
        f.write('\t\t\t<parameter key="DtAllParticles" value="'+str(data['dtallparticles'])+'" comment="Velocity of particles used to calculate DT. 1:All, 0:Only fluid/floating (default=0)" />\n')
        f.write('\t\t\t<parameter key="TimeMax" value="'+str(data['timemax'])+'" comment="Time of simulation" units_comment="seconds" />\n')
        f.write('\t\t\t<parameter key="TimeOut" value="'+str(data['timeout'])+'" comment="Time out data" units_comment="seconds" />\n')
        f.write('\t\t\t<parameter key="IncZ" value="'+str(data['incz'])+'" comment="Increase of Z+" units_comment="decimal" />\n')
        f.write('\t\t\t<parameter key="PartsOutMax" value="'+str(data['partsoutmax'])+'" comment="%/100 of fluid particles allowed to be excluded from domain (default=1)" units_comment="decimal" />\n')
        f.write('\t\t\t<parameter key="RhopOutMin" value="'+str(data['rhopoutmin'])+'" comment="Minimum rhop valid (default=700)" units_comment="kg/m^3" />\n')
        f.write('\t\t\t<parameter key="RhopOutMax" value="'+str(data['rhopoutmax'])+'" comment="Maximum rhop valid (default=1300)" units_comment="kg/m^3" />\n')
        f.write('\t\t</parameters>\n')
        f.write('\t</execution>\n')
        f.write('</case>\n')
        f.close()

        #GENERATE BAT TO EXECUTE EASELY
        if (data["gencase_path"] == "") or (data["dsphysics_path"] == "") or (data["partvtk4_path"] == ""):
            print "WARNING: Can't create executable bat file! One or more of the paths in plugin setup is not set"
        else:
            bat_file = open(saveName+"/run.bat", 'w')
            print "Creating " + saveName+"/run.bat"
            bat_file.write("@echo off\n")
            bat_file.write('echo "------- Autoexported by DualSPHysics for FreeCAD -------"\n')
            bat_file.write('echo "This script executes GenCase for the case saved, that generates output files in the *_Out dir. Then, executes a simulation on CPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."\n')
            bat_file.write('pause\n')
            bat_file.write('"'+data["gencase_path"]+'" '+ saveName+"/" + saveName.split('/')[-1]+ "_Def " + saveName+"/"+saveName.split('/')[-1]+ "_Out/" + saveName.split('/')[-1] + ' -save:+all' +'\n')
            bat_file.write('"'+data["dsphysics_path"]+'" '+ saveName+"/"+saveName.split('/')[-1]+ "_Out/" + saveName.split('/')[-1] + ' ' + saveName+"/"+saveName.split('/')[-1]+ "_Out" + ' -svres -cpu' +'\n')
            bat_file.write('"'+data["partvtk4_path"]+'" -dirin '+ saveName+"/"+saveName.split('/')[-1]+ "_Out -savevtk " + saveName+"/"+saveName.split('/')[-1]+ "_Out/PartAll" +'\n')
            bat_file.write('echo "------- Execution complete. If results were not the exepected ones check for errors. Make sure your case has a correct DP specification. -------"\n')
            bat_file.write('pause\n')
            bat_file.close()

            bat_file = open(saveName+"/run.sh", 'w')
            print "Creating " + saveName+"/run.sh"
            bat_file.write('echo "------- Autoexported by DualSPHysics for FreeCAD -------"\n')
            bat_file.write('echo "This script executes GenCase for the case saved, that generates output files in the *_Out dir. Then, executes a simulation on CPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."\n')
            bat_file.write('read -rsp $"Press any key to continue..." -n 1 key\n')
            bat_file.write('"'+data["gencase_path"]+'" '+ saveName+"/" + saveName.split('/')[-1]+ "_Def " + saveName+"/"+saveName.split('/')[-1]+ "_Out/" + saveName.split('/')[-1] + ' -save:+all' +'\n')
            bat_file.write('"'+data["dsphysics_path"]+'" '+ saveName+"/"+saveName.split('/')[-1]+ "_Out/" + saveName.split('/')[-1] + ' ' + saveName+"/"+saveName.split('/')[-1]+ "_Out" + ' -svres -cpu' +'\n')
            bat_file.write('"'+data["partvtk4_path"]+'" -dirin '+ saveName+"/"+saveName.split('/')[-1]+ "_Out -savevtk " + saveName+"/"+saveName.split('/')[-1]+ "_Out/PartAll" +'\n')
            bat_file.write('echo "------- Execution complete. If results were not the exepected ones check for errors. Make sure your case has a correct DP specification. -------"\n')
            bat_file.write('read -rsp $"Press any key to continue..." -n 1 key\n')
            bat_file.close()

        
        data["gencase_done"] = False
        #Use gencase if possible to generate the case final definition
        if data["gencase_path"] != "":
            os.chdir(data["project_path"])
            process = QtCore.QProcess(fc_main_window)
            process.start(data["gencase_path"], [data["project_path"]+"/"+data["project_name"]+"_Def", data["project_path"]+"/"+data["project_name"]+"_Out/"+data["project_name"], "-save:+all"])
            process.waitForFinished()
            output = str(process.readAllStandardOutput())
            errorInGenCase = False
            if str(process.exitCode()) == "0":
                try:
                    total_particles_text = output[output.index("Total particles: "):output.index(" (bound=")]
                    total_particles = int(total_particles_text[total_particles_text.index(": ") + 2:])
                    data['total_particles'] = total_particles

                    print "Total number of particles exported: " + str(total_particles)
                    if total_particles < 300:
                        print "WARNING: Are you sure all the parameters are set right? The number of particles is very low (" + str(total_particles) + "). Lower the DP to increase number of particles"
                    elif total_particles > 200000:
                        print "WARNING: Number of particles is pretty high (" + str(total_particles) + ") and it could take a lot of time to simulate."
                    data["gencase_done"] = True
                    ex_selector_combo.setEnabled(True)
                    ex_button.setEnabled(True)
                    ex_additional.setEnabled(True)
                    gencase_infosave_dialog = QtGui.QMessageBox()
                    gencase_infosave_dialog.setText("Gencase exported " + str(total_particles) + " particles. Press View Details to check the output.\n")
                    gencase_infosave_dialog.setDetailedText(output.split("================================")[1])
                    gencase_infosave_dialog.setIcon(QtGui.QMessageBox.Information)
                    gencase_infosave_dialog.exec_()
                except ValueError as e:
                    errorInGenCase = True

            if str(process.exitCode()) != "0" or errorInGenCase:
                #Multiple causes
                gencase_out_file = open(data["project_path"] + "/" + data["project_name"] + "_Out/" + data["project_name"] + ".out", "rb")
                gencase_failed_dialog = QtGui.QMessageBox()
                gencase_failed_dialog.setText("Error executing gencase. Did you add objects to the case?. Another reason could be memory issues. View details for more info.")
                gencase_failed_dialog.setDetailedText(gencase_out_file.read().split("================================")[1])
                gencase_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
                gencase_failed_dialog.exec_()
                print "WARNING: GenCase Failed. Probably because nothing is in the scene."

        #Save data array on disk
        picklefile = open(saveName+"/casedata.dsphdata", 'wb')
        pickle.dump(data, picklefile)        

    else:
        print "DualSPHysics for FreeCAD: Saving cancelled."

def on_load_case():
    '''Defines loading case mechanism.
    Load points to a dsphdata custom file, that stores all the relevant info.
    If FCStd file is not found the project is considered corrupt.'''
    loadName, _ = QtGui.QFileDialog.getOpenFileName(dsph_main_dock, "Load Case", QtCore.QDir.homePath(), "casedata.dsphdata")
    if loadName == "":
        #User pressed cancel. No path is selected.
        return
    load_project_name = loadName.split("/")[-2]
    load_path_project_folder = "/".join(loadName.split("/")[:-1])
    if not os.path.isfile(load_path_project_folder + "/DSPH_Case.FCStd"):
        guiutils.warning_dialog("DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting.")
        print "ERROR: DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."
        return

    #Tries to close all documents
    if len(FreeCAD.listDocuments().keys()) > 0:
        loadConfirmDialog = QtGui.QMessageBox()
        loadConfirmDialog.setText("DualSPHysics for FreeCAD")
        loadConfirmDialog.setInformativeText("To load a case you must close all the open documents. Close all the documents?")
        loadConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        loadConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
        loadCDRet = loadConfirmDialog.exec_()

        if loadCDRet == QtGui.QMessageBox.Ok:
            print "DualSPHysics for FreeCAD: Load File. Closing all documents..."
            for doc in FreeCAD.listDocuments().keys():
                FreeCAD.closeDocument(doc)
        else:
            return
    
    #Opens the case freecad document
    FreeCAD.open(load_path_project_folder + "/DSPH_Case.FCStd")    

    #Loads own file and sets data and button behaviour
    load_picklefile = open(loadName, 'rb')
    load_disk_data = pickle.load(load_picklefile)    
    global data
    data.update(load_disk_data)
    global dp_input
    dp_input.setText(str(data['dp']))

    data["project_path"] = load_path_project_folder
    data["project_name"] = load_path_project_folder.split("/")[-1]
    constants_button.setEnabled(True)
    execparams_button.setEnabled(True)
    casecontrols_bt_savedoc.setEnabled(True)
    dp_input.setEnabled(True)
    if data["gencase_done"]:
        ex_selector_combo.setEnabled(True)
        ex_button.setEnabled(True)
        ex_additional.setEnabled(True)
    else:
        ex_selector_combo.setEnabled(False)
        ex_button.setEnabled(False)
        ex_additional.setEnabled(True)
    
    if data["simulation_done"]:    
        export_button.setEnabled(True)
        exportopts_button.setEnabled(True)
    else:
        export_button.setEnabled(False)
        exportopts_button.setEnabled(False)
    casecontrols_bt_addfillbox.setEnabled(True)
    casecontrols_bt_addstl.setEnabled(True)

    os.chdir(data["project_path"])
    data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'], correct_execs = utils.check_executables(data['gencase_path'], data['dsphysics_path'], data['partvtk4_path'])
    if not correct_execs:
        ex_selector_combo.setEnabled(False)
        ex_button.setEnabled(False)
        ex_additional.setEnabled(False)
        export_button.setEnabled(False)
        exportopts_button.setEnabled(False)

    on_tree_item_selection_change()

def on_add_fillbox():
    '''Add fillbox group. It consists
    in a group with 2 objects inside: a point and a box.
    The point represents the fill seed and the box sets
    the bounds for the filling'''
    fillbox_gp = FreeCAD.getDocument("DSPH_Case").addObject("App::DocumentObjectGroup","FillBox")
    fillbox_point = FreeCAD.ActiveDocument.addObject("Part::Sphere","FillPoint")
    fillbox_limits = FreeCAD.ActiveDocument.addObject("Part::Box","FillLimit")
    fillbox_limits.ViewObject.DisplayMode = "Wireframe"
    fillbox_limits.ViewObject.LineColor = (0.00,0.78,1.00)
    fillbox_point.Radius.Value = 0.2
    fillbox_point.Placement.Base = FreeCAD.Vector(5,5,5)
    fillbox_point.ViewObject.ShapeColor = (0.00,0.00,0.00)
    fillbox_gp.addObject(fillbox_limits)
    fillbox_gp.addObject(fillbox_point)
    FreeCAD.ActiveDocument.recompute()
    Gui.SendMsgToActiveView("ViewFit")

def on_add_stl():
    '''Add STL file. Opens a file opener and allows
    the user to set parameters for the import process'''
    #For now disabled
    filedialog = QtGui.QFileDialog()
    fileName, _ = filedialog.getOpenFileName(fc_main_window, "Select STL to import", QtCore.QDir.homePath(), "STL Files (*.stl)")
    stl_mesh = mesh.Mesh.from_file(fileName)

#Connect case control buttons
casecontrols_bt_newdoc.clicked.connect(on_new_case)
casecontrols_bt_savedoc.clicked.connect(on_save_case)
casecontrols_bt_loaddoc.clicked.connect(on_load_case)
casecontrols_bt_addfillbox.clicked.connect(on_add_fillbox)
casecontrols_bt_addstl.clicked.connect(on_add_stl)

#Defines case control scaffolding
cclabel_layout.addWidget(casecontrols_label)
ccfilebuttons_layout.addWidget(casecontrols_bt_newdoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_savedoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_loaddoc)
ccaddbuttons_layout.addWidget(casecontrols_bt_addfillbox)
#TODO: Add custom STL Import
#ccaddbuttons_layout.addWidget(casecontrols_bt_addstl)
cc_layout.addLayout(cclabel_layout)
cc_layout.addLayout(ccfilebuttons_layout)
cc_layout.addLayout(ccaddbuttons_layout)
cc_separator = QtGui.QFrame()
cc_separator.setFrameStyle(QtGui.QFrame.HLine)

#Defines run window dialog
run_dialog = QtGui.QDialog(None, QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint)
run_watcher = QtCore.QFileSystemWatcher()

run_dialog.setModal(False)
run_dialog.setWindowTitle("DualSPHysics Simulation: 0%")
run_dialog.setFixedSize(550,273)
run_dialog_layout = QtGui.QVBoxLayout()

run_group = QtGui.QGroupBox("Simulation Data")
run_group_layout = QtGui.QVBoxLayout()
run_group_label_case = QtGui.QLabel("Case Name: ")
run_group_label_proc = QtGui.QLabel("Simulation processor: ")
run_group_label_part = QtGui.QLabel("Number of particles: ")
run_group_label_partsout = QtGui.QLabel("Total particles out of case: ")
run_group_label_eta = QtGui.QLabel(run_dialog)
run_group_label_eta.setText("Estimated time of completion: Calculating...")
run_group_layout.addWidget(run_group_label_case)
run_group_layout.addWidget(run_group_label_proc)
run_group_layout.addWidget(run_group_label_part)
run_group_layout.addWidget(run_group_label_partsout)
run_group_layout.addWidget(run_group_label_eta)
run_group_layout.addStretch(1)
run_group.setLayout(run_group_layout)

run_progbar_layout = QtGui.QHBoxLayout()
run_progbar_bar = QtGui.QProgressBar()
run_progbar_bar.setRange(0, 100)
run_progbar_bar.setTextVisible(False)
run_progbar_layout.addWidget(run_progbar_bar)

run_button_layout = QtGui.QHBoxLayout()
run_button_cancel = QtGui.QPushButton("Cancel Simulation")
run_button_layout.addStretch(1)
run_button_layout.addWidget(run_button_cancel)

run_dialog_layout.addWidget(run_group)
run_dialog_layout.addLayout(run_progbar_layout)
run_dialog_layout.addLayout(run_button_layout)

run_dialog.setLayout(run_dialog_layout)

def on_ex_simulate():
    '''Defines what happens on simulation button press.
    It shows the run window and starts a background process
    with dualsphysics running. Updates the window with useful info.'''
    run_progbar_bar.setValue(0)
    data["simulation_done"] = False
    ex_button.setEnabled(False)
    ex_additional.setEnabled(False)
    export_button.setEnabled(False)
    exportopts_button.setEnabled(False)
    run_button_cancel.setText("Cancel Simulation")
    ex_selector_combo.setEnabled(False)
    run_dialog.setWindowTitle("DualSPHysics Simulation: 0%")
    run_group_label_case.setText("Case Name: " + data['project_name'])
    run_group_label_proc.setText("Simulation processor: " + str(ex_selector_combo.currentText()))
    run_group_label_part.setText("Number of particles: " + str(data['total_particles']))
    run_group_label_partsout.setText("Total particles out of case: 0")
    
    def on_cancel():
        print "DualSPHysics for FreeCAD: Stopping simulation"
        if temp_data["current_process"] != None :
            temp_data["current_process"].kill()

        run_dialog.hide()
        ex_selector_combo.setEnabled(True)
        ex_button.setEnabled(True)
        ex_additional.setEnabled(True)

    run_button_cancel.clicked.connect(on_cancel)

    #Launch simulation and watch filesystem to monitor simulation
    filelist = [ f for f in os.listdir(data["project_path"]+"/"+data["project_name"]+"_Out/") if f.startswith("Part") ]
    for f in filelist:
        os.remove(data["project_path"]+"/"+data["project_name"]+"_Out/" + f)
    
    def on_dsph_sim_finished(exitCode):
        output = temp_data["current_process"].readAllStandardOutput()
        run_watcher.removePath(data["project_path"]+"/"+data["project_name"]+"_Out/")
        run_dialog.setWindowTitle("DualSPHysics Simulation: Complete")
        run_progbar_bar.setValue(100)
        run_button_cancel.setText("Close")
        if exitCode == 0:
            data["simulation_done"] = True
            export_button.setEnabled(True)
            exportopts_button.setEnabled(True)
        else:
            if "exception" in str(output).lower():
                print "ERROR: Exception in execution."
                run_dialog.setWindowTitle("DualSPHysics Simulation: Error")
                run_progbar_bar.setValue(0)
                run_dialog.hide()
                ex_selector_combo.setEnabled(True)
                ex_button.setEnabled(True)
                ex_additional.setEnabled(True)
                execution_error_dialog = QtGui.QMessageBox()
                execution_error_dialog.setText("There was an error in execution. Make sure you set the parameters right (and they exist). Also, make sure that your computer has the right hardware to simulate. Check the details for more information.")
                execution_error_dialog.setDetailedText(str(output).split("================================")[1])
                execution_error_dialog.setIcon(QtGui.QMessageBox.Critical)
                execution_error_dialog.exec_()

    #Launches a QProcess in background
    process = QtCore.QProcess(run_dialog)
    process.finished.connect(on_dsph_sim_finished)
    temp_data["current_process"] = process
    static_params_exe = [data["project_path"]+"/"+data["project_name"]+"_Out/" + data["project_name"], data["project_path"]+"/"+data["project_name"]+"_Out/", "-svres", "-" + str(ex_selector_combo.currentText()).lower()]
    if len(data["additional_parameters"]) < 2:
        additional_params_ex = []
    else:
        additional_params_ex = data["additional_parameters"].split(" ")
    final_params_ex = static_params_exe + additional_params_ex
    temp_data["current_process"].start(data["dsphysics_path"], final_params_ex)
    
    def on_fs_change(path):
        try:
            run_file = open(data["project_path"]+"/"+data["project_name"]+"_Out/Run.out", "r")
            run_file_data = run_file.readlines()
            run_file.close()
        except Exception as e:
            print e

        #Set percentage scale based on timemax
        for l in run_file_data:
            if data["timemax"] == -1:
                if "TimeMax=" in l:
                    data["timemax"] = float(l.split("=")[1])

        if "Part_" in run_file_data[-1]:
            last_line_parttime = run_file_data[-1].split(".")
            if "Part_" in last_line_parttime[0]:
                current_value = (float(last_line_parttime[0].split(" ")[-1] + "." + last_line_parttime[1][:2]) * float(100)) / float(data["timemax"])
                run_progbar_bar.setValue(current_value)
                run_dialog.setWindowTitle("DualSPHysics Simulation: " +str(format(current_value, ".2f"))+ "%")
                
            last_line_time = run_file_data[-1].split("  ")[-1]
            if ("===" not in last_line_time) and ("CellDiv" not in last_line_time) and ("memory" not in last_line_time) and ("-" in last_line_time):
                #update time field
                try:
                    run_group_label_eta.setText("Estimated time of completion: " + last_line_time)
                except RuntimeError:
                    run_group_label_eta.setText("Estimated time of completion: Calculating..." )
                    pass
        elif "Particles out:" in run_file_data[-1]:
            totalpartsout = int(run_file_data[-1].split("(total: ")[1].split(")")[0])
            data["total_particles_out"] = totalpartsout
            run_group_label_partsout.setText("Total particles out of case: " + str(data['total_particles_out']))
        run_file = None


    run_watcher.addPath(data["project_path"]+"/"+data["project_name"]+"_Out/")
    run_watcher.directoryChanged.connect(on_fs_change)
    if temp_data["current_process"].state() == QtCore.QProcess.NotRunning:
        #Probably error happened.
        run_watcher.removePath(data["project_path"]+"/"+data["project_name"]+"_Out/")

        temp_data["current_process"] = ""
        exec_not_correct_dialog = QtGui.QMessageBox()
        exec_not_correct_dialog.setText("Error on simulation start. Is the path of DualSPHysics correctly placed?")
        exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Critical)
        exec_not_correct_dialog.exec_()
    else:
        run_dialog.show()

def on_additional_parameters():
    additional_parameters_window = QtGui.QDialog()
    additional_parameters_window.setWindowTitle("Additional parameters")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    def on_ok():
        data['additional_parameters'] = export_params.text()
        additional_parameters_window.accept()

    def on_cancel():
        additional_parameters_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    #Button layout definition    
    eo_button_layout = QtGui.QHBoxLayout()
    eo_button_layout.addStretch(1)
    eo_button_layout.addWidget(ok_button)
    eo_button_layout.addWidget(cancel_button)

    paramintro_layout = QtGui.QHBoxLayout()
    paramintro_label = QtGui.QLabel("Additional Parameters: ")
    export_params = QtGui.QLineEdit()
    export_params.setText(data["additional_parameters"])
    paramintro_layout.addWidget(paramintro_label)
    paramintro_layout.addWidget(export_params)

    additional_parameters_layout = QtGui.QVBoxLayout()
    additional_parameters_layout.addLayout(paramintro_layout)
    additional_parameters_layout.addStretch(1)
    additional_parameters_layout.addLayout(eo_button_layout)

    additional_parameters_window.setFixedSize(600,110)
    additional_parameters_window.setLayout(additional_parameters_layout)    
    additional_parameters_window.exec_()

#Execution section scaffolding
ex_layout = QtGui.QVBoxLayout()
ex_label = QtGui.QLabel("This is the simulation group. Use this controls to simulate the case in which you are working. Remember that, depending on the number of particles generated it could take some time.")
ex_label.setWordWrap(True)
ex_selector_layout = QtGui.QHBoxLayout()
ex_selector_label = QtGui.QLabel("Select where to simulate:")
ex_selector_combo = QtGui.QComboBox()
ex_selector_combo.addItem("CPU")
ex_selector_combo.addItem("GPU")
ex_selector_layout.addWidget(ex_selector_label)
ex_selector_layout.addWidget(ex_selector_combo)
ex_button = QtGui.QPushButton("Simulate Case")
ex_button.setToolTip("Starts the case simulation. From the simulation\nwindow you can see the current progress and\nuseful information.")
ex_button.clicked.connect(on_ex_simulate)
ex_additional = QtGui.QPushButton("Additional parameters")
ex_additional.setToolTip("Sets simulation additional parameters for execution.")
ex_additional.clicked.connect(on_additional_parameters)
ex_button_layout = QtGui.QHBoxLayout()
ex_button_layout.addWidget(ex_button)
ex_button_layout.addWidget(ex_additional)
ex_layout.addWidget(ex_label)
ex_layout.addLayout(ex_selector_layout)
ex_layout.addLayout(ex_button_layout)

ex_separator = QtGui.QFrame()
ex_separator.setFrameStyle(QtGui.QFrame.HLine)

#Defines export window dialog
export_dialog = QtGui.QDialog(None, QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint)

export_dialog.setModal(False)
export_dialog.setWindowTitle("Export to VTK: 0%")
export_dialog.setFixedSize(550,143)
export_dialog_layout = QtGui.QVBoxLayout()

export_progbar_layout = QtGui.QHBoxLayout()
export_progbar_bar = QtGui.QProgressBar()
export_progbar_bar.setRange(0, 100)
export_progbar_bar.setTextVisible(False)
export_progbar_layout.addWidget(export_progbar_bar)

export_button_layout = QtGui.QHBoxLayout()
export_button_cancel = QtGui.QPushButton("Cancel Exporting")
export_button_layout.addStretch(1)
export_button_layout.addWidget(export_button_cancel)

export_dialog_layout.addLayout(export_progbar_layout)
export_dialog_layout.addLayout(export_button_layout)

export_dialog.setLayout(export_dialog_layout)

def on_export():
    '''Export VTK button behaviour.
    Launches a process while disabling the button.'''
    temp_data["export_button"].setEnabled(False)
    temp_data["exportopts_button"].setEnabled(False)
    temp_data["export_button"].setText("Exporting...")

    #Find total export parts
    partfiles =  glob.glob(data["project_path"]+"/"+data["project_name"]+"_Out/" + "Part_*.bi4")
    for filename in partfiles:
        temp_data["total_export_parts"] = max(int(filename.split("Part_")[1].split(".bi4")[0]), temp_data["total_export_parts"])
    export_progbar_bar.setRange(0, temp_data["total_export_parts"])
    export_progbar_bar.setValue(0)

    export_dialog.show()

    def on_cancel():
        print "DualSPHysics for FreeCAD: Stopping export"
        if temp_data["current_export_process"] != None :
            temp_data["current_export_process"].kill()
        temp_data["export_button"].setText("Export data to VTK")
        temp_data["export_button"].setEnabled(True)
        temp_data["exportopts_button"].setEnabled(True)
        export_dialog.hide()

    export_button_cancel.clicked.connect(on_cancel)

    def on_export_finished(exitCode):
        temp_data["export_button"].setText("Export data to VTK")
        temp_data["export_button"].setEnabled(True)
        temp_data["exportopts_button"].setEnabled(True)
        export_dialog.hide()

    export_process = QtCore.QProcess(dsph_main_dock)
    export_process.finished.connect(on_export_finished)
    static_params_exp = ["-dirin "+data["project_path"]+"/"+data["project_name"]+"_Out/", "-savevtk "+data["project_path"]+"/"+data["project_name"]+"_Out/PartAll"]
    if len(data["export_options"]) < 2:
        additional_params_exp = []
    else:
        additional_params_exp = data["additional_parameters"].split(" ")

    final_params_exp = static_params_exp + additional_params_exp
    export_process.start(data["partvtk4_path"], final_params_exp)
    temp_data["current_export_process"] = export_process

    def on_stdout_ready():
        #update progress bar
        current_output = str(temp_data["current_export_process"].readAllStandardOutput())
        current_part = int(current_output.split("PartAll_")[1].split(".vtk")[0])
        export_progbar_bar.setValue(current_part)
        export_dialog.setWindowTitle("Export to VTK: " + str(current_part) + "/" + str(temp_data["total_export_parts"]))


    temp_data["current_export_process"].readyReadStandardOutput.connect(on_stdout_ready)

def on_exportopts():
    export_options_window = QtGui.QDialog()
    export_options_window.setWindowTitle("Export options")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    def on_ok():
        data['export_options'] = export_params.text()
        export_options_window.accept()

    def on_cancel():
        export_options_window.reject()

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    #Button layout definition    
    eo_button_layout = QtGui.QHBoxLayout()
    eo_button_layout.addStretch(1)
    eo_button_layout.addWidget(ok_button)
    eo_button_layout.addWidget(cancel_button)

    export_params_layout = QtGui.QHBoxLayout()
    export_params_label = QtGui.QLabel("Export parameters: ")
    export_params = QtGui.QLineEdit()
    export_params.setText(data["export_options"])
    export_params_layout.addWidget(export_params_label)
    export_params_layout.addWidget(export_params)

    export_options_layout = QtGui.QVBoxLayout()
    export_options_layout.addLayout(export_params_layout)
    export_options_layout.addStretch(1)
    export_options_layout.addLayout(eo_button_layout)

    export_options_window.setFixedSize(600,110)
    export_options_window.setLayout(export_options_layout)    
    export_options_window.exec_()

#Export to VTK section scaffolding
export_layout = QtGui.QVBoxLayout()
export_label = QtGui.QLabel("This is the export section. Once a simulation is made, you can export to VTK the files generated by DualSPHysics. Press the button below to export")
export_label.setWordWrap(True)
export_buttons_layout = QtGui.QHBoxLayout()
export_button = QtGui.QPushButton("Export data to VTK")
exportopts_button = QtGui.QPushButton("Options")
export_button.setToolTip("Exports the simulation data to VTK format.")
export_button.clicked.connect(on_export)
exportopts_button.clicked.connect(on_exportopts)
temp_data["export_button"] = export_button
temp_data["exportopts_button"] = exportopts_button
export_layout.addWidget(export_label)
export_buttons_layout.addWidget(export_button)
export_buttons_layout.addWidget(exportopts_button)
export_layout.addLayout(export_buttons_layout)

export_separator = QtGui.QFrame()
export_separator.setFrameStyle(QtGui.QFrame.HLine)

#Object list table scaffolding
objectlist_layout = QtGui.QVBoxLayout()
objectlist_label = QtGui.QLabel("Order of objects marked for case simulation:")
objectlist_label.setWordWrap(True)
objectlist_table = QtGui.QTableWidget(0,3)
objectlist_table.setToolTip("Press 'Move up' to move an object up in the hirearchy.\nPress 'Move down' to move an object down in the hirearchy.")
objectlist_table.setObjectName("DSPH Objects")
objectlist_table.verticalHeader().setVisible(False)
objectlist_table.setHorizontalHeaderLabels(["Object Name", "Order up", "Order down"])
objectlist_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
temp_data["objectlist_table"] = objectlist_table
objectlist_layout.addWidget(objectlist_label)
objectlist_layout.addWidget(objectlist_table)

objectlist_separator = QtGui.QFrame()
objectlist_separator.setFrameStyle(QtGui.QFrame.HLine)

#Layout adding and ordering
logo_layout.addStretch(0.5)
logo_layout.addWidget(logo_label)
logo_layout.addStretch(0.5)

#Adding things here and there
intro_layout.addWidget(constants_label)
constantsandsetup_layout = QtGui.QHBoxLayout()
constantsandsetup_layout.addWidget(constants_button)
constantsandsetup_layout.addWidget(help_button)
constantsandsetup_layout.addWidget(setup_button)
intro_layout.addLayout(constantsandsetup_layout)
intro_layout.addWidget(execparams_button)
intro_layout.addWidget(constants_separator)
main_layout.addLayout(logo_layout)
main_layout.addLayout(intro_layout)
main_layout.addLayout(dp_layout)
main_layout.addWidget(crucialvars_separator)
main_layout.addLayout(cc_layout)
main_layout.addWidget(cc_separator)
main_layout.addLayout(ex_layout)
main_layout.addWidget(ex_separator)
main_layout.addLayout(export_layout)
main_layout.addWidget(export_separator)
main_layout.addLayout(objectlist_layout)
main_layout.addWidget(objectlist_separator)
main_layout.addStretch(1)

#Default disabled widgets
constants_button.setEnabled(False)
execparams_button.setEnabled(False)
casecontrols_bt_savedoc.setEnabled(False)
dp_input.setEnabled(False)
ex_selector_combo.setEnabled(False)
ex_button.setEnabled(False)
ex_additional.setEnabled(False)
export_button.setEnabled(False)
exportopts_button.setEnabled(False)

'''You can't apply layouts to a QDockWidget, 
so creating a standard widget, applying the layouts, 
and then setting it as the QDockWidget'''
dsph_main_dock_scaff_widget.setLayout(main_layout)
dsph_main_dock.setWidget(dsph_main_dock_scaff_widget)

#And docking it at right side of screen
fc_main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea,dsph_main_dock)

#------------------------ DSPH OBJECT PROPERTIES DOCK RELATED CODE ----------------------------
#Tries to find and close previous instances of the widget.
previous_dock = fc_main_window.findChild(QtGui.QDockWidget, "DSPH_Properties")
if previous_dock:
    previous_dock.setParent(None)
    previous_dock = None

#Creation of the widget and scaffolding
properties_widget = QtGui.QDockWidget()
properties_widget.setMinimumHeight(400)
properties_widget.setObjectName("DSPH_Properties")
properties_widget.setWindowTitle("DSPH Object Properties")
properties_scaff_widget = QtGui.QWidget() #Scaffolding widget, only useful to apply to the properties_dock widget

property_widget_layout = QtGui.QVBoxLayout()
property_table = QtGui.QTableWidget(5,2)
property_table.setHorizontalHeaderLabels(["Property Name", "Value"])
property_table.verticalHeader().setVisible(False)
property_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
addtodsph_button = QtGui.QPushButton("Add to DSPH Simulation")
addtodsph_button.setToolTip("Adds the current selection to\nthe case. Objects not included will not be exported.")
removefromdsph_button = QtGui.QPushButton("Remove from DSPH Simulation")
removefromdsph_button.setToolTip("Removes the current selection from the case.\nObjects not included in the case will not be exported.")
property_widget_layout.addWidget(property_table)
property_widget_layout.addWidget(addtodsph_button)
property_widget_layout.addWidget(removefromdsph_button)
properties_scaff_widget.setLayout(property_widget_layout)

properties_widget.setWidget(properties_scaff_widget)
propertylabel1 = QtGui.QLabel("   MK Group")
propertylabel1.setToolTip("Establishes the object group.")
propertylabel2 = QtGui.QLabel("   Type of object")
propertylabel2.setToolTip("Establishes the object type, fluid or bound")
propertylabel3 = QtGui.QLabel("   Fill mode")
propertylabel3.setToolTip("Sets fill mode.\nFull: generates filling and external mesh.\nSolid: generates only filling.\nFace: generates only external mesh.\nWire: generates only external mesh polygon edges.")
propertylabel4 = QtGui.QLabel("   Float state")
propertylabel4.setToolTip("Sets floating state for this object MK.")
propertylabel5 = QtGui.QLabel("   Initials")
propertylabel5.setToolTip("Sets initials options for this object")
propertylabel1.setAlignment(QtCore.Qt.AlignLeft)
propertylabel2.setAlignment(QtCore.Qt.AlignLeft)
propertylabel3.setAlignment(QtCore.Qt.AlignLeft)
propertylabel4.setAlignment(QtCore.Qt.AlignLeft)
propertylabel5.setAlignment(QtCore.Qt.AlignLeft)
property_table.setCellWidget(0,0, propertylabel1)
property_table.setCellWidget(1,0, propertylabel2)
property_table.setCellWidget(2,0, propertylabel3)
property_table.setCellWidget(3,0, propertylabel4)
property_table.setCellWidget(4,0, propertylabel5)

def property1_change(value):
    '''Defines what happens when MKGroup is changed.'''
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
    data['simobjects'][selection.Name][0] = value

def property2_change(index):
    '''Defines what happens when type of object is changed'''
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
    data['simobjects'][selection.Name][1] = property2.itemText(index)
    if "fillbox" in selection.Name.lower():
        return
    if property2.itemText(index).lower() == "bound":
        property1.setRange(0, 240)
        selectiongui.ShapeColor = (0.80,0.80,0.80)
        selectiongui.Transparency = 0
        property4.setEnabled(True)
        property5.setEnabled(False)
    elif property2.itemText(index).lower() == "fluid":
        property1.setRange(0, 10)
        selectiongui.ShapeColor = (0.00,0.45,1.00)
        selectiongui.Transparency = 30
        if str(str(data['simobjects'][selection.Name][0])) in data["floating_mks"].keys():
            data["floating_mks"].pop(str(data['simobjects'][selection.Name][0]), None)
        property4.setEnabled(False)
        property5.setEnabled(True)

def property3_change(index):
    '''Defines what happens when fill mode is changed'''
    selection = FreeCADGui.Selection.getSelection()[0]
    selectiongui = FreeCADGui.getDocument("DSPH_Case").getObject(selection.Name)
    data['simobjects'][selection.Name][2] = property3.itemText(index)
    if property3.itemText(index).lower() == "full":
        if property2.itemText(property2.currentIndex()).lower() == "fluid":
            selectiongui.Transparency = 30
        elif property2.itemText(property2.currentIndex()).lower() == "bound":
            selectiongui.Transparency = 0
    elif property3.itemText(index).lower() == "solid":
        if property2.itemText(property2.currentIndex()).lower() == "fluid":
            selectiongui.Transparency = 30
        elif property2.itemText(property2.currentIndex()).lower() == "bound":
            selectiongui.Transparency = 0
    elif property3.itemText(index).lower() == "face":
        selectiongui.Transparency = 80
    elif property3.itemText(index).lower() == "wire":
        selectiongui.Transparency = 85

def property4_configure():
    '''Defines a window with floating properties.'''
    floatings_window = QtGui.QDialog()
    floatings_window.setWindowTitle("Floating configuration")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")
    target_mk = int(data["simobjects"][FreeCADGui.Selection.getSelection()[0].Name][0])
    def on_ok():
        guiutils.info_dialog("This will apply the floating properties to all objects with mkbound = " + str(target_mk))
        if is_floating_selector.currentIndex() == 1:
            #Floating false
            if str(target_mk) in data["floating_mks"].keys():
                data["floating_mks"].pop(str(target_mk), None)
        else:
            #Floating true
            #Structure: 'mk': [massrhop, center, inertia, velini, omegaini]
            data["floating_mks"][str(target_mk)] = [[floating_props_massrhop_selector.currentIndex(), float(floating_props_massrhop_input.text())],[floating_center_auto.isChecked(), float(floating_center_input_x.text()), float(floating_center_input_y.text()), float(floating_center_input_z.text())],[floating_inertia_auto.isChecked(), float(floating_inertia_input_x.text()), float(floating_inertia_input_y.text()), float(floating_inertia_input_z.text())],[floating_velini_auto.isChecked(), float(floating_velini_input_x.text()), float(floating_velini_input_y.text()), float(floating_velini_input_z.text())],[floating_omegaini_auto.isChecked(), float(floating_omegaini_input_x.text()), float(floating_omegaini_input_y.text()), float(floating_omegaini_input_z.text())]]

        floatings_window.accept()
    def on_cancel():
        floatings_window.reject()


    def on_floating_change(index):
        if index == 0:
            floating_props_group.setEnabled(True)
        else:
            floating_props_group.setEnabled(False)
    
    def on_massrhop_change(index):
        if index == 0:
            floating_props_massrhop_input.setText("0.0")
        else:
            floating_props_massrhop_input.setText("0.0")

    def on_gravity_auto():
        if floating_center_auto.isChecked():
            floating_center_input_x.setEnabled(False)
            floating_center_input_y.setEnabled(False)
            floating_center_input_z.setEnabled(False)
        else:
            floating_center_input_x.setEnabled(True)
            floating_center_input_y.setEnabled(True)
            floating_center_input_z.setEnabled(True)

    def on_inertia_auto():
        if floating_inertia_auto.isChecked():
            floating_inertia_input_x.setEnabled(False)
            floating_inertia_input_y.setEnabled(False)
            floating_inertia_input_z.setEnabled(False)
        else:
            floating_inertia_input_x.setEnabled(True)
            floating_inertia_input_y.setEnabled(True)
            floating_inertia_input_z.setEnabled(True)

    def on_velini_auto():
        if floating_velini_auto.isChecked():
            floating_velini_input_x.setEnabled(False)
            floating_velini_input_y.setEnabled(False)
            floating_velini_input_z.setEnabled(False)
        else:
            floating_velini_input_x.setEnabled(True)
            floating_velini_input_y.setEnabled(True)
            floating_velini_input_z.setEnabled(True)

    def on_omegaini_auto():
        if floating_omegaini_auto.isChecked():
            floating_omegaini_input_x.setEnabled(False)
            floating_omegaini_input_y.setEnabled(False)
            floating_omegaini_input_z.setEnabled(False)
        else:
            floating_omegaini_input_x.setEnabled(True)
            floating_omegaini_input_y.setEnabled(True)
            floating_omegaini_input_z.setEnabled(True)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    is_floating_layout = QtGui.QHBoxLayout()
    is_floating_label = QtGui.QLabel("Set floating: ")
    is_floating_label.setToolTip("Sets the current MKBound selected as floating.")
    is_floating_selector = QtGui.QComboBox()
    is_floating_selector.insertItems(0, ["True", "False"])
    is_floating_selector.currentIndexChanged.connect(on_floating_change)
    is_floating_targetlabel = QtGui.QLabel("Target MKBound: "+ str(target_mk))
    is_floating_layout.addWidget(is_floating_label)
    is_floating_layout.addWidget(is_floating_selector)
    is_floating_layout.addStretch(1)
    is_floating_layout.addWidget(is_floating_targetlabel)

    floating_props_group = QtGui.QGroupBox("Floating properties")
    floating_props_layout = QtGui.QVBoxLayout()
    floating_props_massrhop_layout = QtGui.QHBoxLayout()
    floating_props_massrhop_label = QtGui.QLabel("Mass/Density: ")
    floating_props_massrhop_label.setToolTip("Selects an mass/density calculation method and its value.")
    floating_props_massrhop_selector = QtGui.QComboBox()
    floating_props_massrhop_selector.insertItems(0, ["massbody", "rhopbody"])
    floating_props_massrhop_selector.currentIndexChanged.connect(on_massrhop_change)
    floating_props_massrhop_input = QtGui.QLineEdit()
    floating_props_massrhop_layout.addWidget(floating_props_massrhop_label)
    floating_props_massrhop_layout.addWidget(floating_props_massrhop_selector)
    floating_props_massrhop_layout.addWidget(floating_props_massrhop_input)
    
    floating_center_layout = QtGui.QHBoxLayout()
    floating_center_label = QtGui.QLabel("Gravity center: ")
    floating_center_label.setToolTip("Sets the mk group gravity center.")
    floating_center_label_x = QtGui.QLabel("X")
    floating_center_input_x = QtGui.QLineEdit()
    floating_center_label_y = QtGui.QLabel("Y")
    floating_center_input_y = QtGui.QLineEdit()
    floating_center_label_z = QtGui.QLabel("Z")
    floating_center_input_z = QtGui.QLineEdit()
    floating_center_auto = QtGui.QCheckBox("Auto ")
    floating_center_auto.toggled.connect(on_gravity_auto)
    floating_center_layout.addWidget(floating_center_label)
    floating_center_layout.addWidget(floating_center_label_x)
    floating_center_layout.addWidget(floating_center_input_x)
    floating_center_layout.addWidget(floating_center_label_y)
    floating_center_layout.addWidget(floating_center_input_y)
    floating_center_layout.addWidget(floating_center_label_z)
    floating_center_layout.addWidget(floating_center_input_z)
    floating_center_layout.addWidget(floating_center_auto)

    floating_inertia_layout = QtGui.QHBoxLayout()
    floating_inertia_label = QtGui.QLabel("Inertia: ")
    floating_inertia_label.setToolTip("Sets the mk group inertia.")
    floating_inertia_label_x = QtGui.QLabel("X")
    floating_inertia_input_x = QtGui.QLineEdit()
    floating_inertia_label_y = QtGui.QLabel("Y")
    floating_inertia_input_y = QtGui.QLineEdit()
    floating_inertia_label_z = QtGui.QLabel("Z")
    floating_inertia_input_z = QtGui.QLineEdit()
    floating_inertia_auto = QtGui.QCheckBox("Auto ")
    floating_inertia_auto.toggled.connect(on_inertia_auto)
    floating_inertia_layout.addWidget(floating_inertia_label)
    floating_inertia_layout.addWidget(floating_inertia_label_x)
    floating_inertia_layout.addWidget(floating_inertia_input_x)
    floating_inertia_layout.addWidget(floating_inertia_label_y)
    floating_inertia_layout.addWidget(floating_inertia_input_y)
    floating_inertia_layout.addWidget(floating_inertia_label_z)
    floating_inertia_layout.addWidget(floating_inertia_input_z)
    floating_inertia_layout.addWidget(floating_inertia_auto)

    floating_velini_layout = QtGui.QHBoxLayout()
    floating_velini_label = QtGui.QLabel("Initial linear velocity: ")
    floating_velini_label.setToolTip("Sets the mk group initial linear velocity")
    floating_velini_label_x = QtGui.QLabel("X")
    floating_velini_input_x = QtGui.QLineEdit()
    floating_velini_label_y = QtGui.QLabel("Y")
    floating_velini_input_y = QtGui.QLineEdit()
    floating_velini_label_z = QtGui.QLabel("Z")
    floating_velini_input_z = QtGui.QLineEdit()
    floating_velini_auto = QtGui.QCheckBox("Auto ")
    floating_velini_auto.toggled.connect(on_velini_auto)
    floating_velini_layout.addWidget(floating_velini_label)
    floating_velini_layout.addWidget(floating_velini_label_x)
    floating_velini_layout.addWidget(floating_velini_input_x)
    floating_velini_layout.addWidget(floating_velini_label_y)
    floating_velini_layout.addWidget(floating_velini_input_y)
    floating_velini_layout.addWidget(floating_velini_label_z)
    floating_velini_layout.addWidget(floating_velini_input_z)
    floating_velini_layout.addWidget(floating_velini_auto)

    floating_omegaini_layout = QtGui.QHBoxLayout()
    floating_omegaini_label = QtGui.QLabel("Initial angular velocity: ")
    floating_omegaini_label.setToolTip("Sets the mk group initial angular velocity")
    floating_omegaini_label_x = QtGui.QLabel("X")
    floating_omegaini_input_x = QtGui.QLineEdit()
    floating_omegaini_label_y = QtGui.QLabel("Y")
    floating_omegaini_input_y = QtGui.QLineEdit()
    floating_omegaini_label_z = QtGui.QLabel("Z")
    floating_omegaini_input_z = QtGui.QLineEdit()
    floating_omegaini_auto = QtGui.QCheckBox("Auto ")
    floating_omegaini_auto.toggled.connect(on_omegaini_auto)
    floating_omegaini_layout.addWidget(floating_omegaini_label)
    floating_omegaini_layout.addWidget(floating_omegaini_label_x)
    floating_omegaini_layout.addWidget(floating_omegaini_input_x)
    floating_omegaini_layout.addWidget(floating_omegaini_label_y)
    floating_omegaini_layout.addWidget(floating_omegaini_input_y)
    floating_omegaini_layout.addWidget(floating_omegaini_label_z)
    floating_omegaini_layout.addWidget(floating_omegaini_input_z)
    floating_omegaini_layout.addWidget(floating_omegaini_auto)

    floating_props_layout.addLayout(floating_props_massrhop_layout)
    floating_props_layout.addLayout(floating_center_layout)
    floating_props_layout.addLayout(floating_inertia_layout)
    floating_props_layout.addLayout(floating_velini_layout)
    floating_props_layout.addLayout(floating_omegaini_layout)
    floating_props_layout.addStretch(1)
    floating_props_group.setLayout(floating_props_layout)

    buttons_layout = QtGui.QHBoxLayout()
    buttons_layout.addStretch(1)
    buttons_layout.addWidget(ok_button)
    buttons_layout.addWidget(cancel_button)

    floatings_window_layout = QtGui.QVBoxLayout()
    floatings_window_layout.addLayout(is_floating_layout)
    floatings_window_layout.addWidget(floating_props_group)
    floatings_window_layout.addLayout(buttons_layout)

    floatings_window.setLayout(floatings_window_layout)

    if str(target_mk) in data["floating_mks"].keys():
        is_floating_selector.setCurrentIndex(0)
        on_floating_change(0)
        floating_props_group.setEnabled(True)
        floating_props_massrhop_selector.setCurrentIndex(data["floating_mks"][str(target_mk)][0][0])
        floating_props_massrhop_input.setText(str(data["floating_mks"][str(target_mk)][0][1]))
        floating_center_input_x.setText(str(data["floating_mks"][str(target_mk)][1][1]))
        floating_center_input_y.setText(str(data["floating_mks"][str(target_mk)][1][2]))
        floating_center_input_z.setText(str(data["floating_mks"][str(target_mk)][1][3]))
        floating_inertia_input_x.setText(str(data["floating_mks"][str(target_mk)][2][1]))
        floating_inertia_input_y.setText(str(data["floating_mks"][str(target_mk)][2][2]))
        floating_inertia_input_z.setText(str(data["floating_mks"][str(target_mk)][2][3]))
        floating_velini_input_x.setText(str(data["floating_mks"][str(target_mk)][3][1]))
        floating_velini_input_y.setText(str(data["floating_mks"][str(target_mk)][3][2]))
        floating_velini_input_z.setText(str(data["floating_mks"][str(target_mk)][3][3]))
        floating_omegaini_input_x.setText(str(data["floating_mks"][str(target_mk)][4][1]))
        floating_omegaini_input_y.setText(str(data["floating_mks"][str(target_mk)][4][2]))
        floating_omegaini_input_z.setText(str(data["floating_mks"][str(target_mk)][4][3]))
        floating_center_auto.setCheckState(QtCore.Qt.Checked if data["floating_mks"][str(target_mk)][1][0] else QtCore.Qt.Unchecked)
        floating_inertia_auto.setCheckState(QtCore.Qt.Checked if data["floating_mks"][str(target_mk)][2][0] else QtCore.Qt.Unchecked)
        floating_velini_auto.setCheckState(QtCore.Qt.Checked if data["floating_mks"][str(target_mk)][3][0] else QtCore.Qt.Unchecked)
        floating_omegaini_auto.setCheckState(QtCore.Qt.Checked if data["floating_mks"][str(target_mk)][4][0] else QtCore.Qt.Unchecked)
    else:
        is_floating_selector.setCurrentIndex(1)
        on_floating_change(1)
        floating_props_group.setEnabled(False)
        is_floating_selector.setCurrentIndex(1)
        floating_props_massrhop_selector.setCurrentIndex(0)
        floating_props_massrhop_input.setText("100")
        floating_center_input_x.setText("0")
        floating_center_input_y.setText("0")
        floating_center_input_z.setText("0")
        floating_inertia_input_x.setText("0")
        floating_inertia_input_y.setText("0")
        floating_inertia_input_z.setText("0")
        floating_velini_input_x.setText("0")
        floating_velini_input_y.setText("0")
        floating_velini_input_z.setText("0")
        floating_omegaini_input_x.setText("0")
        floating_omegaini_input_y.setText("0")
        floating_omegaini_input_z.setText("0")

        floating_center_auto.setCheckState(QtCore.Qt.Checked)
        floating_inertia_auto.setCheckState(QtCore.Qt.Checked)
        floating_velini_auto.setCheckState(QtCore.Qt.Checked)
        floating_omegaini_auto.setCheckState(QtCore.Qt.Checked)

    floatings_window.exec_()

def property5_configure():
    '''Defines a window with initials properties.'''
    initials_window = QtGui.QDialog()
    initials_window.setWindowTitle("Initials configuration")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")
    target_mk = int(data["simobjects"][FreeCADGui.Selection.getSelection()[0].Name][0])
    def on_ok():
        guiutils.info_dialog("This will apply the initials properties to all objects with mkbound = " + str(target_mk))
        if has_initials_selector.currentIndex() == 1:
            #Initials false
            if str(target_mk) in data["initials_mks"].keys():
                data["initials_mks"].pop(str(target_mk), None)
        else:
            #Initials true
            #Structure: {'mkfluid': [x, y, z]}
            data["initials_mks"][str(target_mk)] = [float(initials_vector_input_x.text()), float(initials_vector_input_y.text()), float(initials_vector_input_z.text())]
        initials_window.accept()

    def on_cancel():
        initials_window.reject()

    def on_initials_change(index):
        if index == 0:
            initials_props_group.setEnabled(True)
        else:
            initials_props_group.setEnabled(False)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    has_initials_layout = QtGui.QHBoxLayout()
    has_initials_label = QtGui.QLabel("Set initials: ")
    has_initials_label.setToolTip("Sets the current initial movement vector.")
    has_initials_selector = QtGui.QComboBox()
    has_initials_selector.insertItems(0, ["True", "False"])
    has_initials_selector.currentIndexChanged.connect(on_initials_change)
    has_initials_targetlabel = QtGui.QLabel("Target MKFluid: "+ str(target_mk))
    has_initials_layout.addWidget(has_initials_label)
    has_initials_layout.addWidget(has_initials_selector)
    has_initials_layout.addStretch(1)
    has_initials_layout.addWidget(has_initials_targetlabel)

    initials_props_group = QtGui.QGroupBox("Initials properties")
    initials_props_layout = QtGui.QVBoxLayout()
    
    initials_vector_layout = QtGui.QHBoxLayout()
    initials_vector_label = QtGui.QLabel("Movement vector: ")
    initials_vector_label.setToolTip("Sets the mk group movement vector.")
    initials_vector_label_x = QtGui.QLabel("X")
    initials_vector_input_x = QtGui.QLineEdit()
    initials_vector_label_y = QtGui.QLabel("Y")
    initials_vector_input_y = QtGui.QLineEdit()
    initials_vector_label_z = QtGui.QLabel("Z")
    initials_vector_input_z = QtGui.QLineEdit()
    initials_vector_layout.addWidget(initials_vector_label)
    initials_vector_layout.addWidget(initials_vector_label_x)
    initials_vector_layout.addWidget(initials_vector_input_x)
    initials_vector_layout.addWidget(initials_vector_label_y)
    initials_vector_layout.addWidget(initials_vector_input_y)
    initials_vector_layout.addWidget(initials_vector_label_z)
    initials_vector_layout.addWidget(initials_vector_input_z)

    initials_props_layout.addLayout(initials_vector_layout)
    initials_props_layout.addStretch(1)
    initials_props_group.setLayout(initials_props_layout)

    buttons_layout = QtGui.QHBoxLayout()
    buttons_layout.addStretch(1)
    buttons_layout.addWidget(ok_button)
    buttons_layout.addWidget(cancel_button)

    initials_window_layout = QtGui.QVBoxLayout()
    initials_window_layout.addLayout(has_initials_layout)
    initials_window_layout.addWidget(initials_props_group)
    initials_window_layout.addLayout(buttons_layout)

    initials_window.setLayout(initials_window_layout)

    if str(target_mk) in data["initials_mks"].keys():
        has_initials_selector.setCurrentIndex(0)
        on_initials_change(0)
        initials_props_group.setEnabled(True)
        initials_vector_input_x.setText(str(data["initials_mks"][str(target_mk)][0]))
        initials_vector_input_y.setText(str(data["initials_mks"][str(target_mk)][1]))
        initials_vector_input_z.setText(str(data["initials_mks"][str(target_mk)][2]))
    else:
        has_initials_selector.setCurrentIndex(1)
        on_initials_change(1)
        initials_props_group.setEnabled(False)
        has_initials_selector.setCurrentIndex(1)
        initials_vector_input_x.setText("0")
        initials_vector_input_y.setText("0")
        initials_vector_input_z.setText("0")
    
    initials_window.exec_()

#Property change widgets
property1 = QtGui.QSpinBox()
property2 = QtGui.QComboBox()
property3 = QtGui.QComboBox()
property4 = QtGui.QPushButton("Configure")
property5 = QtGui.QPushButton("Configure")
property1.setRange(0, 240)
property2.insertItems(0, ["Fluid", "Bound"])
property3.insertItems(1, ["Full", "Solid", "Face", "Wire"])
property1.valueChanged.connect(property1_change)
property2.currentIndexChanged.connect(property2_change)
property3.currentIndexChanged.connect(property3_change)
property4.clicked.connect(property4_configure)
property5.clicked.connect(property5_configure)
property_table.setCellWidget(0,1, property1)
property_table.setCellWidget(1,1, property2)
property_table.setCellWidget(2,1, property3)
property_table.setCellWidget(3,1, property4)
property_table.setCellWidget(4,1, property5)

#Dock the widget to the left side of screen
fc_main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)

#By default all is hidden in the widget
property_table.hide()
addtodsph_button.hide()
removefromdsph_button.hide()

def add_object_to_sim():
    '''Defines what happens when "Add object to sim" button is presseed.
    Takes the selection of FreeCAD and watches what type of thing it is adding'''
    selection = FreeCADGui.Selection.getSelection()
    for item in selection:
        if item.Name == "Case_Limits":
            continue
        if len(item.InList) > 0:
            continue
        if item.Name not in data['simobjects'].keys():
            if "fillbox" in item.Name.lower():
                mktoput = utils.get_first_mk_not_used("fluid", data)
                if not mktoput:
                    mktoput = 0
                data['simobjects'][item.Name] = [mktoput, 'fluid', 'full']
                data["mkfluidused"].append(mktoput)
            else:
                mktoput = utils.get_first_mk_not_used("bound", data)
                if not mktoput:
                    mktoput = 0
                data['simobjects'][item.Name] = [mktoput, 'bound', 'full']
                data["mkboundused"].append(mktoput)
            data["export_order"].append(item.Name)
    on_tree_item_selection_change()

def remove_object_from_sim():
    '''Defines what happens when removing objects from
    the simulation'''
    selection = FreeCADGui.Selection.getSelection()
    for item in selection:
        if item.Name == "Case_Limits":
            continue
        if item.Name in data["export_order"]:
            data['export_order'].remove(item.Name)
        toRemove = data['simobjects'].pop(item.Name, None)
    on_tree_item_selection_change()

#Connects buttons to its functions
addtodsph_button.clicked.connect(add_object_to_sim)
removefromdsph_button.clicked.connect(remove_object_from_sim)

#Find treewidgets of freecad.
trees = []
for item in fc_main_window.findChildren(QtGui.QTreeWidget):
    if item.objectName() != "DSPH Objects":
        trees.append(item)

def on_tree_item_selection_change():
    selection = FreeCADGui.Selection.getSelection()
    objectNames = []
    for item in FreeCAD.getDocument("DSPH_Case").Objects:
        objectNames.append(item.Name)
    
    #Detect object deletion
    for key in data['simobjects'].keys():
        if key not in objectNames:
            data['simobjects'].pop(key, None)
            data["export_order"].remove(key)

    addtodsph_button.setEnabled(True)
    if len(selection) > 0:
        if len(selection) > 1:
            #Multiple objects selected
            addtodsph_button.setText("Add all possible to DSPH Simulation")
            property_table.hide()
            addtodsph_button.show()
            removefromdsph_button.hide()
            pass
        else:
            #One object selected
            if selection[0].Name == "Case_Limits":
                property_table.hide()
                addtodsph_button.hide()
                removefromdsph_button.hide()
                return
            if selection[0].Name in data['simobjects'].keys():
                #Show properties on table
                property_table.show()
                addtodsph_button.hide()
                removefromdsph_button.show()
                toChange = property_table.cellWidget(0,1)
                toChange.setValue(data['simobjects'][selection[0].Name][0])

                toChange = property_table.cellWidget(1,1)
                if selection[0].TypeId in temp_data["supported_types"]:
                    toChange.setEnabled(True)
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        toChange.setCurrentIndex(0)
                        property1.setRange(0, 10)
                        propertylabel1.setText("   MKFluid")
                    elif data['simobjects'][selection[0].Name][1].lower() == "bound":
                        toChange.setCurrentIndex(1)
                        property1.setRange(0, 240)
                        propertylabel1.setText("   MKBound")
                elif selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower():
                        toChange.setEnabled(False)
                        toChange.setCurrentIndex(0)
                else:
                    toChange.setCurrentIndex(1)
                    toChange.setEnabled(False)

                toChange = property_table.cellWidget(2,1)
                if selection[0].TypeId in temp_data["supported_types"]:
                    toChange.setEnabled(True)
                    if data['simobjects'][selection[0].Name][2].lower() == "full":
                        toChange.setCurrentIndex(0)
                    elif data['simobjects'][selection[0].Name][2].lower() == "solid":
                        toChange.setCurrentIndex(1)
                    elif data['simobjects'][selection[0].Name][2].lower() == "face":
                        toChange.setCurrentIndex(2)
                    elif data['simobjects'][selection[0].Name][2].lower() == "wire":
                        toChange.setCurrentIndex(3)
                else:
                    toChange.setCurrentIndex(0)
                    toChange.setEnabled(False)

                #float state config
                toChange = property_table.cellWidget(3,1)
                if selection[0].TypeId in temp_data["supported_types"]:
                    if data['simobjects'][selection[0].Name][1].lower() == "fluid":
                        toChange.setEnabled(False)
                    else:
                        toChange.setEnabled(True)

            else:
                if selection[0].InList == []:
                    #Show button to add to simulation
                    addtodsph_button.setText("Add to DSPH Simulation")
                    property_table.hide()
                    addtodsph_button.show()
                    removefromdsph_button.hide()
                else:
                    addtodsph_button.setText("Can't add this object to the simulation")
                    property_table.hide()
                    addtodsph_button.show()
                    addtodsph_button.setEnabled(False)
                    removefromdsph_button.hide()
    else:
        property_table.hide()
        addtodsph_button.hide()
        removefromdsph_button.hide()

    #Update dsph objects list
    objectlist_table.clear()
    objectlist_table.setEnabled(True)
    if len(data["export_order"]) == 0:
        data["export_order"] = data["simobjects"].keys()
    #Substract one that represent case limits object
    objectlist_table.setRowCount(len(data["export_order"]) - 1)
    objectlist_table.setHorizontalHeaderLabels(["Object Name", "Order up", "Order down"])
    currentRow = 0
    objectsWithParent = []
    for key in data["export_order"]:
        contextObject = FreeCAD.getDocument("DSPH_Case").getObject(key)
        if not contextObject:
            data["export_order"].remove(key)
            continue
        if contextObject.InList != []:
            objectsWithParent.append(contextObject.Name)
            continue
        if contextObject.Name == "Case_Limits":
            continue
        objectlist_table.setCellWidget(currentRow, 0, QtGui.QLabel("   " + contextObject.Label))
        up = QtGui.QLabel("   Move Up")
        up.setAlignment(QtCore.Qt.AlignLeft)
        up.setStyleSheet("QLabel { background-color : rgb(225,225,225); color : black; margin: 2px;} QLabel:hover { background-color : rgb(215,215,255); color : black; }")
        
        down = QtGui.QLabel("   Move Down")
        down.setAlignment(QtCore.Qt.AlignLeft)
        down.setStyleSheet("QLabel { background-color : rgb(225,225,225); color : black; margin: 2px;} QLabel:hover { background-color : rgb(215,215,255); color : black; }")

        if currentRow != 0:
            objectlist_table.setCellWidget(currentRow,1, up)
        if (currentRow + 2) != len(data["export_order"]):
            objectlist_table.setCellWidget(currentRow,2, down)

        currentRow += 1
    for each in objectsWithParent:
        try:
            data["simobjects"].pop(each, None)
        except ValueError as e:
            #Not in list, probably because now is part of a compound object
            pass
        data["export_order"].remove(each)

for item in trees:
    item.itemSelectionChanged.connect(on_tree_item_selection_change)

def on_cell_click(row, column):
    label_pressed = objectlist_table.cellWidget(row, column)
    #set in row + 1 to ignore case_limits (always first)
    object_pressed = FreeCAD.getDocument("DSPH_Case").getObject(data["simobjects"].keys()[row + 1])

    new_order = []
    if column == 1:
        #order up
        curr_elem = data["export_order"][row + 1]
        prev_elem = data["export_order"][row]

        data["export_order"].remove(curr_elem)

        for element in data["export_order"]:
            if element == prev_elem:
                new_order.append(curr_elem)
            new_order.append(element)

        data['export_order'] = new_order
    elif column == 2:
        #order down
        curr_elem = data["export_order"][row + 1]
        next_elem = data["export_order"][row + 2]

        data["export_order"].remove(curr_elem)

        for element in data["export_order"]:
            new_order.append(element)
            if element == next_elem:
                new_order.append(curr_elem)

        data['export_order'] = new_order
    else:
        #ignore
        pass
    on_tree_item_selection_change()

objectlist_table.cellClicked.connect(on_cell_click)

#Watch if no object is selected and prevent fillbox rotations
def selection_monitor():
    while True:
        #ensure everything is fine when objects are not selected
        if len(FreeCADGui.Selection.getSelection()) == 0:
            property_table.hide()
            addtodsph_button.hide()
            removefromdsph_button.hide()
        #watch fillbox rotations and prevent them
        try:
            for o in FreeCAD.getDocument("DSPH_Case").Objects:
                if o.TypeId == "App::DocumentObjectGroup" and "fillbox" in o.Name.lower():
                    for subelem in o.OutList:
                        if subelem.Placement.Rotation.Angle != 0.0:
                            subelem.Placement.Rotation.Angle = 0.0
                            print "ERROR: Can't change fillbox contents rotation!"
        except NameError as e:
            #DSPH Case not opened, disable things
            casecontrols_bt_savedoc.setEnabled(False)
            constants_button.setEnabled(False)
            execparams_button.setEnabled(False)
            casecontrols_bt_addfillbox.setEnabled(False)
            casecontrols_bt_addstl.setEnabled(False)
            ex_button.setEnabled(False)
            ex_additional.setEnabled(False)
            ex_selector_combo.setEnabled(False)
            export_button.setEnabled(False)
            exportopts_button.setEnabled(False)
            objectlist_table.setEnabled(False)
            threading._sleep(2)
            continue

        threading._sleep(0.5)

monitor_thread = threading.Thread(target=selection_monitor)
monitor_thread.start()

FreeCADGui.activateWorkbench("PartWorkbench")
print "DualSPHysics for FreeCAD: Done loading data."
