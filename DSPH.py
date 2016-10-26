# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from datetime import datetime
import os, sys, pickle, threading, math, webbrowser

#Special vars
version = 'v0.10a'

print "Loading DualSPHysics for FreeCAD..."
print "-----------------------------------"
print "DualSPHysics for FreeCAD is a free macro/module for FreeCAD created to make case definition for DualSPHysics easier."
print "EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo"
print "School of Mechanical, Aerospace and Civil Engineering, University of Manchester."
print "Developed by Andrés Vieira."
print "-----------------------------------"

#Version check. This script is only compatible with FreeCAD 0.16 or higher
version_num = FreeCAD.Version()[0] + FreeCAD.Version()[1]
if int(version_num) < int("016"):
	exec_not_correct_dialog = QtGui.QMessageBox()
	exec_not_correct_dialog.setText("This version of FreeCAD is not supported!. Install version 0.16 or higher.")
	exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Warning)
	exec_not_correct_dialog.exec_()
	exit(1)

#Main data structure
data = dict()
temp_data = dict()

#Establishing references for the different elements that the script will use later
app = QtGui.qApp
mw = FreeCADGui.getMainWindow()
dsph_dock = QtGui.QDockWidget()
scaff_widget = QtGui.QWidget() #Scaffolding widget, only useful to apply to the dsph_dock widget

#Check executables and see if they are the correct ones
def check_executables():
	execs_correct = True
	if os.path.isfile(data["gencase_path"]):
		process = QtCore.QProcess(mw)
		process.start(data["gencase_path"])
		process.waitForFinished()
		output = str(process.readAllStandardOutput())
		if "gencase" in output[0:15].lower():
			print "DualSPHysics for FreeCAD: Found correct GenCase."
		else:
			execs_correct = False
			data["gencase_path"] = ""
	else:
		execs_correct = False
		data["gencase_path"] = ""			

	if os.path.isfile(data["dsphysics_path"]):
		process = QtCore.QProcess(mw)
		process.start(data["dsphysics_path"])
		process.waitForFinished()
		output = str(process.readAllStandardOutput())
		if "dualsphysics" in output[0:20].lower():
			print "DualSPHysics for FreeCAD: Found correct DualSPHysics."
		else:
			execs_correct = False
			data["dsphysics_path"] = ""
	else:
		execs_correct = False
		data["dsphysics_path"] = ""			

	if os.path.isfile(data["partvtk4_path"]):
		process = QtCore.QProcess(mw)
		process.start(data["partvtk4_path"])
		process.waitForFinished()
		output = str(process.readAllStandardOutput())
		if "partvtk4" in output[0:20].lower():
			print "DualSPHysics for FreeCAD: Found correct PartVTK4."
		else:
			execs_correct = False	
			data["partvtk4_path"] = ""
	else:
		execs_correct = False
		data["partvtk4_path"] = ""			

	if not execs_correct:
		print "WARNING: One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries"
		exec_not_correct_dialog = QtGui.QMessageBox()
		exec_not_correct_dialog.setText("One or more of the executables in the setup is not correct. Check plugin setup to fix missing binaries.")
		exec_not_correct_dialog.setIcon(QtGui.QMessageBox.Warning)
		exec_not_correct_dialog.exec_()
	return execs_correct

def set_default_data():
	'''Sets default data at start of the macro.'''
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
	
	'''Dictionary that defines floatings. 
	Keys are mks enabled (ONLY BOUNDS) and values are a list containing:
	{'mkbound': [massrhop, center, inertia, velini, omegaini]}
	massrhop = [selectedOption (index), value]
	center = [auto (bool), x,y,z]
	inertia = [auto (bool), x,y,z]
	velini = [auto (bool), x,y,z]
	omegaini = [auto (bool), x,y,z]'''
	data['floating_mks'] = dict()

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
	temp_data['supported_types'] = ["Part::Box", "Part::Sphere", "Part::Cylinder"]

	'''Try to load saved paths. This way the user does not need
	to introduce the software paths every time'''
	if os.path.isfile(App.getUserAppDataDir()+'/dsph_data.dsphdata'):
		try:
			picklefile = open(App.	DataDir()+'/dsph_data.dsphdata', 'rb')
			disk_data = pickle.load(picklefile)
			data['gencase_path'] = disk_data['gencase_path']
			data['dsphysics_path'] = disk_data['dsphysics_path']
			data['partvtk4_path'] = disk_data['partvtk4_path']
		except:
			data['gencase_path'] = ""
			data['dsphysics_path'] = ""
			data['partvtk4_path'] = ""
	
		print "DualSPHysics for FreeCAD: Found data file. Loading data from disk."
		check_executables()
	else:
		data["project_path"] = "" 
		data["project_name"] = ""

#Executes the default data function the first time
set_default_data()


'''The script needs only one document open, called DSHP_Case.
This section tries to close all the current documents.'''
if len(App.listDocuments().keys()) > 0:
	#Close all current documents.
	openConfirmDialog = QtGui.QMessageBox()
	openConfirmDialog.setText("DualSPHysics for FreeCAD")
	openConfirmDialog.setInformativeText("To load this module you must close all current documents. Close all the documents?")
	openConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
	openConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
	openCDRet = openConfirmDialog.exec_()

	if openCDRet == QtGui.QMessageBox.Ok:
		print "DualSPHysics for FreeCAD: Closing all current documents"
		for doc in App.listDocuments().keys():
			App.closeDocument(doc)
	else:
		quit()

def get_first_mk_not_used(type):
	if type == "fluid":
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

#If the script is executed even when a previous DSHP Dock is created
# it makes sure that it's deleted before
previous_dock = mw.findChild(QtGui.QDockWidget, "DSPH Widget")
if previous_dock:
	previous_dock.setParent(None)
	previous_dock = None

#Creation of the DSPH Widget
dsph_dock.setObjectName("DSPH Widget")
dsph_dock.setWindowTitle("DualSPHysics for FreeCAD " + str(version))

def def_constants_window():
	'''Defines the constants window creation and functonality'''
	#Creates a dialog and 2 main buttons
	constants_window = QtGui.QDialog()
	constants_window.setWindowTitle("DSPH Constant definition")
	ok_button = QtGui.QPushButton("Ok")
	cancel_button = QtGui.QPushButton("Cancel")

	#Lattice for boundaries layout and components
	lattice_layout = QtGui.QHBoxLayout()
	lattice_label = QtGui.QLabel("Lattice for Boundaries: ")
	lattice_input = QtGui.QLineEdit()
	lattice_input.setMaxLength(1)	
	lattice_validator = QtGui.QIntValidator(1, 2, lattice_input)
	lattice_input.setText(str(data['lattice_bound']))
	lattice_input.setValidator(lattice_validator)
	lattice_label2 = QtGui.QLabel("units")

	lattice_layout.addWidget(lattice_label)
	lattice_layout.addWidget(lattice_input)
	lattice_layout.addWidget(lattice_label2)

	#Lattice for fluids layout and components
	lattice2_layout = QtGui.QHBoxLayout()
	lattice2_label = QtGui.QLabel("Lattice for Fluids: ")
	lattice2_input = QtGui.QLineEdit()
	lattice2_input.setMaxLength(1)	
	lattice2_validator = QtGui.QIntValidator(1, 2, lattice2_input)
	lattice2_input.setText(str(data['lattice_bound']))
	lattice2_input.setValidator(lattice2_validator)
	lattice2_label2 = QtGui.QLabel("units")

	lattice2_layout.addWidget(lattice2_label)
	lattice2_layout.addWidget(lattice2_input)
	lattice2_layout.addWidget(lattice2_label2)

	#Gravity
	gravity_layout = QtGui.QHBoxLayout()
	gravity_label = QtGui.QLabel("Gravity [X, Y, Z]: ")
	
	gravityx_input = QtGui.QLineEdit()
	gravityx_input.setMaxLength(10)	
	gravityx_validator = QtGui.QDoubleValidator(-200, 200, 8, gravityx_input)
	gravityx_input.setText(str(data['gravity'][0]))
	gravityx_input.setValidator(gravityx_validator)

	gravityy_input = QtGui.QLineEdit()
	gravityy_input.setMaxLength(10)	
	gravityy_validator = QtGui.QDoubleValidator(-200, 200, 8, gravityy_input)
	gravityy_input.setText(str(data['gravity'][1]))
	gravityy_input.setValidator(gravityy_validator)

	gravityz_input = QtGui.QLineEdit()
	gravityz_input.setMaxLength(10)	
	gravityz_validator = QtGui.QDoubleValidator(-200, 200, 8, gravityz_input)
	gravityz_input.setText(str(data['gravity'][2]))
	gravityz_input.setValidator(gravityz_validator)
	
	gravity_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

	gravity_layout.addWidget(gravity_label)
	gravity_layout.addWidget(gravityx_input) #For X
	gravity_layout.addWidget(gravityy_input) #For Y
	gravity_layout.addWidget(gravityz_input) #For Z
	gravity_layout.addWidget(gravity_label2)
	
	#Reference density of the fluid: layout and components
	rhop0_layout = QtGui.QHBoxLayout()
	rhop0_label = QtGui.QLabel("Fluid reference density: ")
	rhop0_input = QtGui.QLineEdit()
	rhop0_input.setMaxLength(10)	
	rhop0_validator = QtGui.QIntValidator(0, 10000, rhop0_input)
	rhop0_input.setText(str(data['rhop0']))
	rhop0_input.setValidator(rhop0_validator)
	rhop0_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3<span>")

	rhop0_layout.addWidget(rhop0_label)
	rhop0_layout.addWidget(rhop0_input)
	rhop0_layout.addWidget(rhop0_label2)

	#Maximum still water lavel to calc. spdofsound using coefsound: layout and components
	hswlauto_layout = QtGui.QHBoxLayout()
	hswlauto_chk = QtGui.QCheckBox("Auto HSWL ")
	if data['hswl_auto']:
		hswlauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		hswlauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_hswlauto_check(): #Controls if user selected auto HSWL or not enabling/disablen HSWL custom value introduction
		if hswlauto_chk.isChecked():
			hswl_input.setEnabled(False)
		else:
			hswl_input.setEnabled(True)

	hswlauto_chk.toggled.connect(on_hswlauto_check)
	hswlauto_layout.addWidget(hswlauto_chk)

	hswl_layout = QtGui.QHBoxLayout()
	hswl_label = QtGui.QLabel("HSWL: ")
	hswl_input = QtGui.QLineEdit()
	hswl_input.setMaxLength(10)	
	hswl_validator = QtGui.QIntValidator(0, 10000, hswl_input)
	hswl_input.setText(str(data['hswl']))
	hswl_input.setValidator(hswl_validator)
	hswl_label2 = QtGui.QLabel("metres")

	hswl_layout.addWidget(hswl_label)
	hswl_layout.addWidget(hswl_input)
	hswl_layout.addWidget(hswl_label2)

	#Manually trigger check for the first time
	on_hswlauto_check()

	#gamma: layout and components
	gamma_layout = QtGui.QHBoxLayout()
	gamma_label = QtGui.QLabel("Gamma: ")
	gamma_input = QtGui.QLineEdit()
	gamma_input.setMaxLength(3)	
	gamma_validator = QtGui.QIntValidator(0, 999, gamma_input)
	gamma_input.setText(str(data['gamma']))
	gamma_input.setValidator(gamma_validator)
	gamma_label2 = QtGui.QLabel("units")

	gamma_layout.addWidget(gamma_label)
	gamma_layout.addWidget(gamma_input)
	gamma_layout.addWidget(gamma_label2)

	#Speedsystem: layout and components
	speedsystemauto_layout = QtGui.QHBoxLayout()
	speedsystemauto_chk = QtGui.QCheckBox("Auto Speedsystem ")
	if data['speedsystem_auto']:
		speedsystemauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		speedsystemauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_speedsystemauto_check(): #Controls if user selected auto speedsystem or not enabling/disablen speedsystem custom value introduction
		if speedsystemauto_chk.isChecked():
			speedsystem_input.setEnabled(False)
		else:
			speedsystem_input.setEnabled(True)

	speedsystemauto_chk.toggled.connect(on_speedsystemauto_check)
	speedsystemauto_layout.addWidget(speedsystemauto_chk)

	speedsystem_layout = QtGui.QHBoxLayout()
	speedsystem_label = QtGui.QLabel("Speedsystem: ")
	speedsystem_input = QtGui.QLineEdit()
	speedsystem_input.setMaxLength(10)	
	speedsystem_validator = QtGui.QIntValidator(0, 10000, speedsystem_input)
	speedsystem_input.setText(str(data['speedsystem']))
	speedsystem_input.setValidator(speedsystem_validator)
	speedsystem_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

	speedsystem_layout.addWidget(speedsystem_label)
	speedsystem_layout.addWidget(speedsystem_input)
	speedsystem_layout.addWidget(speedsystem_label2)

	#Manually trigger check for the first time
	on_speedsystemauto_check()

	#coefsound: layout and components
	coefsound_layout = QtGui.QHBoxLayout()
	coefsound_label = QtGui.QLabel("Coefsound: ")
	coefsound_input = QtGui.QLineEdit()
	coefsound_input.setMaxLength(3)	
	coefsound_validator = QtGui.QIntValidator(0, 999, coefsound_input)
	coefsound_input.setText(str(data['coefsound']))
	coefsound_input.setValidator(coefsound_validator)
	coefsound_label2 = QtGui.QLabel("units")

	coefsound_layout.addWidget(coefsound_label)
	coefsound_layout.addWidget(coefsound_input)
	coefsound_layout.addWidget(coefsound_label2)

	#Speedsound: layout and components
	speedsoundauto_layout = QtGui.QHBoxLayout()
	speedsoundauto_chk = QtGui.QCheckBox("Auto Speedsound ")
	if data['speedsound_auto']:
		speedsoundauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		speedsoundauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_speedsoundauto_check(): #Controls if user selected auto speedsound or not enabling/disablen speedsound custom value introduction
		if speedsoundauto_chk.isChecked():
			speedsound_input.setEnabled(False)
		else:
			speedsound_input.setEnabled(True)

	speedsoundauto_chk.toggled.connect(on_speedsoundauto_check)
	speedsoundauto_layout.addWidget(speedsoundauto_chk)

	speedsound_layout = QtGui.QHBoxLayout()
	speedsound_label = QtGui.QLabel("Speedsound: ")
	speedsound_input = QtGui.QLineEdit()
	speedsound_input.setMaxLength(10)	
	speedsound_validator = QtGui.QIntValidator(0, 10000, speedsound_input)
	speedsound_input.setText(str(data['speedsound']))
	speedsound_input.setValidator(speedsound_validator)
	speedsound_label2 = QtGui.QLabel("m/s<span style='vertical-align:super'>2</span>")

	speedsound_layout.addWidget(speedsound_label)
	speedsound_layout.addWidget(speedsound_input)
	speedsound_layout.addWidget(speedsound_label2)

	#Manually trigger check for the first time
	on_speedsoundauto_check()

	#coefh: layout and components
	coefh_layout = QtGui.QHBoxLayout()
	coefh_label = QtGui.QLabel("CoefH: ")
	coefh_input = QtGui.QLineEdit()
	coefh_input.setMaxLength(10)	
	coefh_validator = QtGui.QDoubleValidator(0, 10, 8, coefh_input)
	coefh_input.setText(str(data['coefh']))
	coefh_input.setValidator(coefh_validator)
	coefh_label2 = QtGui.QLabel("units")

	coefh_layout.addWidget(coefh_label)
	coefh_layout.addWidget(coefh_input)
	coefh_layout.addWidget(coefh_label2)

	#cflnumber: layout and components
	cflnumber_layout = QtGui.QHBoxLayout()
	cflnumber_label = QtGui.QLabel("cflnumber: ")
	cflnumber_input = QtGui.QLineEdit()
	cflnumber_input.setMaxLength(10)	
	cflnumber_validator = QtGui.QDoubleValidator(0, 10, 8, coefh_input)
	cflnumber_input.setText(str(data['cflnumber']))
	cflnumber_input.setValidator(cflnumber_validator)
	cflnumber_label2 = QtGui.QLabel("units")

	cflnumber_layout.addWidget(cflnumber_label)
	cflnumber_layout.addWidget(cflnumber_input)
	cflnumber_layout.addWidget(cflnumber_label2)

	#h: layout and components
	hauto_layout = QtGui.QHBoxLayout()
	hauto_chk = QtGui.QCheckBox("Auto Smoothing length ")
	if data['h_auto']:
		hauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		hauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_hauto_check(): #Controls if user selected auto h or not enabling/disablen h custom value introduction
		if hauto_chk.isChecked():
			h_input.setEnabled(False)
		else:
			h_input.setEnabled(True)

	hauto_chk.toggled.connect(on_hauto_check)
	hauto_layout.addWidget(hauto_chk)

	h_layout = QtGui.QHBoxLayout()
	h_label = QtGui.QLabel("Smoothing Length: ")
	h_input = QtGui.QLineEdit()
	h_input.setMaxLength(10)	
	h_validator = QtGui.QDoubleValidator(0, 100, 8, h_input)
	h_input.setText(str(data['h']))
	h_input.setValidator(h_validator)
	h_label2 = QtGui.QLabel("metres")

	h_layout.addWidget(h_label)
	h_layout.addWidget(h_input)
	h_layout.addWidget(h_label2)

	#Manually trigger check for the first time
	on_hauto_check()

	#b: layout and components
	bauto_layout = QtGui.QHBoxLayout()
	bauto_chk = QtGui.QCheckBox("Auto b constant for EOS ")
	if data['b_auto']:
		bauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		bauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_bauto_check(): #Controls if user selected auto b or not enabling/disablen b custom value introduction
		if bauto_chk.isChecked():
			b_input.setEnabled(False)
		else:
			b_input.setEnabled(True)

	bauto_chk.toggled.connect(on_bauto_check)
	bauto_layout.addWidget(bauto_chk)

	b_layout = QtGui.QHBoxLayout()
	b_label = QtGui.QLabel("B constant: ")
	b_input = QtGui.QLineEdit()
	b_input.setMaxLength(10)	
	b_validator = QtGui.QDoubleValidator(0, 100, 8, b_input)
	b_input.setText(str(data['b']))
	b_input.setValidator(b_validator)
	b_label2 = QtGui.QLabel("metres")

	b_layout.addWidget(b_label)
	b_layout.addWidget(b_input)
	b_layout.addWidget(b_label2)

	#Manually trigger check for the first time
	on_bauto_check()


	#------------ Button behaviour definition --------------
	def on_ok():
		data['lattice_bound'] = lattice_input.text()
		data['lattice_fluid'] = lattice2_input.text()
		data['gravity'] = [gravityx_input.text(), gravityy_input.text(), gravityz_input.text()]
		data['rhop0'] = rhop0_input.text()
		data['hswl'] = hswl_input.text()
		data['hswl_auto'] = hswlauto_chk.isChecked()
		data['gamma'] = gamma_input.text()
		data['speedsystem'] = speedsystem_input.text()
		data['speedsystem_auto'] = speedsystemauto_chk.isChecked()
		data['coefsound'] = coefsound_input.text()
		data['speedsound'] = speedsound_input.text()
		data['speedsound_auto'] = speedsoundauto_chk.isChecked()
		data['coefh'] = coefh_input.text()
		data['cflnumber'] = cflnumber_input.text()
		data['h'] = h_input.text()
		data['h_auto'] = hauto_chk.isChecked()
		data['b'] = b_input.text()
		data['b_auto'] = bauto_chk.isChecked()
		print "DualSPHysics for FreeCAD: Constants changed"
		constants_window.accept()

	def on_cancel():
		print "DualSPHysics for FreeCAD: Constants not changed"
		constants_window.reject()

	ok_button.clicked.connect(on_ok)
	cancel_button.clicked.connect(on_cancel)
	#Button layout definition	
	cw_button_layout = QtGui.QHBoxLayout()
	cw_button_layout.addStretch(1)
	cw_button_layout.addWidget(ok_button)
	cw_button_layout.addWidget(cancel_button)

	#START Main layout definition and composition.
	cw_main_layout = QtGui.QVBoxLayout()
	
	cw_main_layout.addLayout(lattice_layout)
	cw_main_layout.addLayout(lattice2_layout)
	cw_main_layout.addLayout(gravity_layout)
	cw_main_layout.addLayout(rhop0_layout)
	cw_main_layout.addLayout(hswlauto_layout)
	cw_main_layout.addLayout(hswl_layout)
	cw_main_layout.addLayout(gamma_layout)
	cw_main_layout.addLayout(speedsystemauto_layout)
	cw_main_layout.addLayout(speedsystem_layout)
	cw_main_layout.addLayout(coefsound_layout)
	cw_main_layout.addLayout(speedsoundauto_layout)
	cw_main_layout.addLayout(speedsound_layout)
	cw_main_layout.addLayout(coefh_layout)
	cw_main_layout.addLayout(cflnumber_layout)
	cw_main_layout.addLayout(hauto_layout)
	cw_main_layout.addLayout(h_layout)
	cw_main_layout.addLayout(bauto_layout)
	cw_main_layout.addLayout(b_layout)

	cw_main_layout.addStretch(1)


	cw_groupbox = QtGui.QGroupBox("Case constants")
	cw_groupbox.setLayout(cw_main_layout)
	constants_window_layout = QtGui.QVBoxLayout()
	constants_window_layout.addWidget(cw_groupbox)	
	constants_window_layout.addLayout(cw_button_layout)
	constants_window.setLayout(constants_window_layout)
	#END Main layout definition and composition.

	#Constant definition window behaviour and general composing
	constants_window.resize(600,400)
	ret_val = constants_window.exec_()	

def def_execparams_window():
	'''Defines the execution parameters window'''
	#Creates a dialog and 2 main buttons
	execparams_window = QtGui.QDialog()
	execparams_window.setWindowTitle("DSPH Execution Parameters")
	ok_button = QtGui.QPushButton("Ok")
	cancel_button = QtGui.QPushButton("Cancel")

	#Precision in particle interaction
	posdouble_layout = QtGui.QHBoxLayout()
	posdouble_label = QtGui.QLabel("Precision in particle interaction: ")
	posdouble_input = QtGui.QLineEdit()
	posdouble_input.setMaxLength(1)	
	posdouble_validator = QtGui.QIntValidator(0, 2, posdouble_input)
	posdouble_input.setText(str(data['posdouble']))
	posdouble_input.setValidator(posdouble_validator)
	posdouble_label2 = QtGui.QLabel("[0,2]")

	posdouble_layout.addWidget(posdouble_label)
	posdouble_layout.addWidget(posdouble_input)
	posdouble_layout.addWidget(posdouble_label2)

	#Step Algorithm
	stepalgorithm_layout = QtGui.QHBoxLayout()
	stepalgorithm_label = QtGui.QLabel("Step Algorithm: ")
	stepalgorithm_input = QtGui.QLineEdit()
	stepalgorithm_input.setMaxLength(1)	
	stepalgorithm_validator = QtGui.QIntValidator(0, 2, stepalgorithm_input)
	stepalgorithm_input.setText(str(data['stepalgorithm']))
	stepalgorithm_input.setValidator(stepalgorithm_validator)
	stepalgorithm_label2 = QtGui.QLabel("[1,2]")

	stepalgorithm_layout.addWidget(stepalgorithm_label)
	stepalgorithm_layout.addWidget(stepalgorithm_input)
	stepalgorithm_layout.addWidget(stepalgorithm_label2)

	#Verlet steps
	verletsteps_layout = QtGui.QHBoxLayout()
	verletsteps_label = QtGui.QLabel("Verlet Steps: ")
	verletsteps_input = QtGui.QLineEdit()
	verletsteps_input.setMaxLength(4)	
	verletsteps_validator = QtGui.QIntValidator(0, 9999, verletsteps_input)
	verletsteps_input.setText(str(data['verletsteps']))
	verletsteps_input.setValidator(verletsteps_validator)

	verletsteps_layout.addWidget(verletsteps_label)
	verletsteps_layout.addWidget(verletsteps_input)

	#Kernel
	kernel_layout = QtGui.QHBoxLayout()
	kernel_label = QtGui.QLabel("Interaction kernel: ")
	kernel_input = QtGui.QLineEdit()
	kernel_input.setMaxLength(1)	
	kernel_validator = QtGui.QIntValidator(0, 2, kernel_input)
	kernel_input.setText(str(data['kernel']))
	kernel_input.setValidator(kernel_validator)
	kernel_label2 = QtGui.QLabel("[1,2]")

	kernel_layout.addWidget(kernel_label)
	kernel_layout.addWidget(kernel_input)
	kernel_layout.addWidget(kernel_label2)

	#Viscosity formulation
	def on_viscotreatment_change():
		if viscotreatment_input.text() == "1":
			visco_input.setText("0.01")
			
		elif viscotreatment_input.text() == "2":			
			visco_input.setText("0.000001")


	viscotreatment_layout = QtGui.QHBoxLayout()
	viscotreatment_label = QtGui.QLabel("Viscosity Formulation: ")
	viscotreatment_input = QtGui.QLineEdit()
	viscotreatment_input.setMaxLength(1)	
	viscotreatment_validator = QtGui.QIntValidator(0, 2, viscotreatment_input)
	viscotreatment_input.setText(str(data['viscotreatment']))
	viscotreatment_input.setValidator(viscotreatment_validator)
	viscotreatment_input.textChanged.connect(on_viscotreatment_change)
	viscotreatment_label2 = QtGui.QLabel("[1,2]")

	viscotreatment_layout.addWidget(viscotreatment_label)
	viscotreatment_layout.addWidget(viscotreatment_input)
	viscotreatment_layout.addWidget(viscotreatment_label2)

	#Viscosity value
	visco_layout = QtGui.QHBoxLayout()
	visco_label = QtGui.QLabel("Viscosity value: ")
	visco_input = QtGui.QLineEdit()
	visco_input.setMaxLength(10)	
	visco_input.setText(str(data['visco']))

	visco_layout.addWidget(visco_label)
	visco_layout.addWidget(visco_input)

	#Viscosity with boundary
	viscoboundfactor_layout = QtGui.QHBoxLayout()
	viscoboundfactor_label = QtGui.QLabel("Viscosity with boundary: ")
	viscoboundfactor_input = QtGui.QLineEdit()
	viscoboundfactor_input.setMaxLength(10)	
	viscoboundfactor_input.setText(str(data['viscoboundfactor']))

	viscoboundfactor_layout.addWidget(viscoboundfactor_label)
	viscoboundfactor_layout.addWidget(viscoboundfactor_input)

	#DeltaSPH value
	deltasph_layout = QtGui.QHBoxLayout()
	deltasph_label = QtGui.QLabel("DeltaSPH value: ")
	deltasph_input = QtGui.QLineEdit()
	deltasph_input.setMaxLength(10)	
	deltasph_input.setText(str(data['deltasph']))

	deltasph_layout.addWidget(deltasph_label)
	deltasph_layout.addWidget(deltasph_input)

	#Shifting mode
	shifting_layout = QtGui.QHBoxLayout()
	shifting_label = QtGui.QLabel("Shifting mode: ")
	shifting_input = QtGui.QLineEdit()
	shifting_input.setMaxLength(1)	
	shifting_validator = QtGui.QIntValidator(1, 3, shifting_input)
	shifting_input.setText(str(data['shifting']))
	shifting_input.setValidator(shifting_validator)
	shifting_label2 = QtGui.QLabel("[1,3]")

	shifting_layout.addWidget(shifting_label)
	shifting_layout.addWidget(shifting_input)
	shifting_layout.addWidget(shifting_label2)	

	#Coefficient for shifting
	shiftcoef_layout = QtGui.QHBoxLayout()
	shiftcoef_label = QtGui.QLabel("Coefficient for shifting: ")
	shiftcoef_input = QtGui.QLineEdit()
	shiftcoef_input.setMaxLength(10)	
	shiftcoef_input.setText(str(data['shiftcoef']))

	shiftcoef_layout.addWidget(shiftcoef_label)
	shiftcoef_layout.addWidget(shiftcoef_input)

	#Free surface detection threshold
	shifttfs_layout = QtGui.QHBoxLayout()
	shifttfs_label = QtGui.QLabel("Free surface detection threshold: ")
	shifttfs_input = QtGui.QLineEdit()
	shifttfs_input.setMaxLength(10)	
	shifttfs_input.setText(str(data['shifttfs']))

	shifttfs_layout.addWidget(shifttfs_label)
	shifttfs_layout.addWidget(shifttfs_input)

	#Rigid algorithm
	rigidalgorithm_layout = QtGui.QHBoxLayout()
	rigidalgorithm_label = QtGui.QLabel("Rigid algorithm: ")
	rigidalgorithm_input = QtGui.QLineEdit()
	rigidalgorithm_input.setMaxLength(1)	
	rigidalgorithm_validator = QtGui.QIntValidator(1, 2, rigidalgorithm_input)
	rigidalgorithm_input.setText(str(data['rigidalgorithm']))
	rigidalgorithm_input.setValidator(rigidalgorithm_validator)
	rigidalgorithm_label2 = QtGui.QLabel("[1,2]")

	rigidalgorithm_layout.addWidget(rigidalgorithm_label)
	rigidalgorithm_layout.addWidget(rigidalgorithm_input)
	rigidalgorithm_layout.addWidget(rigidalgorithm_label2)

	#Sim start freeze time
	ftpause_layout = QtGui.QHBoxLayout()
	ftpause_label = QtGui.QLabel("Sim start freeze time: ")
	ftpause_input = QtGui.QLineEdit()
	ftpause_input.setMaxLength(10)	
	ftpause_input.setText(str(data['ftpause']))
	ftpause_label2 = QtGui.QLabel("seconds")

	ftpause_layout.addWidget(ftpause_label)
	ftpause_layout.addWidget(ftpause_input)
	ftpause_layout.addWidget(ftpause_label2)


	#Coefficient to calculate DT
	coefdtmin_layout = QtGui.QHBoxLayout()
	coefdtmin_label = QtGui.QLabel("Coefficient to calculate DT: ")
	coefdtmin_input = QtGui.QLineEdit()
	coefdtmin_input.setMaxLength(10)	
	coefdtmin_input.setText(str(data['coefdtmin']))

	coefdtmin_layout.addWidget(coefdtmin_label)
	coefdtmin_layout.addWidget(coefdtmin_input)

	#Initial time step
	dtiniauto_layout = QtGui.QHBoxLayout()
	dtiniauto_chk = QtGui.QCheckBox("Initial time step auto")
	if data['dtini_auto']:
		dtiniauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		dtiniauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_dtiniauto_check(): #Controls if user selected auto b or not enabling/disablen b custom value introduction
		if dtiniauto_chk.isChecked():
			dtini_input.setEnabled(False)
		else:
			dtini_input.setEnabled(True)

	dtiniauto_chk.toggled.connect(on_dtiniauto_check)
	dtiniauto_layout.addWidget(dtiniauto_chk)

	dtini_layout = QtGui.QHBoxLayout()
	dtini_label = QtGui.QLabel("Initial time step: ")
	dtini_input = QtGui.QLineEdit()
	dtini_input.setMaxLength(10)	
	dtini_input.setText(str(data['dtini']))
	dtini_label2 = QtGui.QLabel("seconds")

	dtini_layout.addWidget(dtini_label)
	dtini_layout.addWidget(dtini_input)
	dtini_layout.addWidget(dtini_label2)

	on_dtiniauto_check()

	#Minimium time step
	dtminauto_layout = QtGui.QHBoxLayout()
	dtminauto_chk = QtGui.QCheckBox("Minimum time step: ")
	if data['dtmin_auto']:
		dtminauto_chk.setCheckState(QtCore.Qt.Checked)
	else:
		dtminauto_chk.setCheckState(QtCore.Qt.Unchecked)

	def on_dtminauto_check(): #Controls if user selected auto b or not enabling/disablen b custom value introduction
		if dtminauto_chk.isChecked():
			dtmin_input.setEnabled(False)
		else:
			dtmin_input.setEnabled(True)

	dtminauto_chk.toggled.connect(on_dtminauto_check)
	dtminauto_layout.addWidget(dtminauto_chk)
	dtmin_layout = QtGui.QHBoxLayout()
	dtmin_label = QtGui.QLabel("Minimium time step: ")
	dtmin_input = QtGui.QLineEdit()
	dtmin_input.setMaxLength(10)	
	dtmin_input.setText(str(data['dtmin']))
	dtmin_label2 = QtGui.QLabel("seconds")

	dtmin_layout.addWidget(dtmin_label)
	dtmin_layout.addWidget(dtmin_input)
	dtmin_layout.addWidget(dtmin_label2)

	on_dtminauto_check()

	#Fixed DT file
	dtfixed_layout = QtGui.QHBoxLayout()
	dtfixed_label = QtGui.QLabel("Fixed DT file: ")
	dtfixed_input = QtGui.QLineEdit()
	dtfixed_input.setText(str(data['dtfixed']))
	dtfixed_label2 = QtGui.QLabel("file")

	dtfixed_layout.addWidget(dtfixed_label)
	dtfixed_layout.addWidget(dtfixed_input)
	dtfixed_layout.addWidget(dtfixed_label2)

	#Velocity of particles
	dtallparticles_layout = QtGui.QHBoxLayout()
	dtallparticles_label = QtGui.QLabel("Velocity of particles: ")
	dtallparticles_input = QtGui.QLineEdit()
	dtallparticles_input.setMaxLength(1)	
	dtallparticles_validator = QtGui.QIntValidator(0, 1, dtallparticles_input)
	dtallparticles_input.setText(str(data['dtallparticles']))
	dtallparticles_input.setValidator(dtallparticles_validator)
	dtallparticles_label2 = QtGui.QLabel("[0,1]")

	dtallparticles_layout.addWidget(dtallparticles_label)
	dtallparticles_layout.addWidget(dtallparticles_input)
	dtallparticles_layout.addWidget(dtallparticles_label2)		

	#Time of simulation
	timemax_layout = QtGui.QHBoxLayout()
	timemax_label = QtGui.QLabel("Time of simulation: ")
	timemax_input = QtGui.QLineEdit()
	timemax_input.setMaxLength(10)	
	timemax_input.setText(str(data['timemax']))
	timemax_label2 = QtGui.QLabel("seconds")

	timemax_layout.addWidget(timemax_label)
	timemax_layout.addWidget(timemax_input)
	timemax_layout.addWidget(timemax_label2)

	#Time out data
	timeout_layout = QtGui.QHBoxLayout()
	timeout_label = QtGui.QLabel("Time out data: ")
	timeout_input = QtGui.QLineEdit()
	timeout_input.setMaxLength(10)	
	timeout_input.setText(str(data['timeout']))
	timeout_label2 = QtGui.QLabel("seconds")

	timeout_layout.addWidget(timeout_label)
	timeout_layout.addWidget(timeout_input)
	timeout_layout.addWidget(timeout_label2)

	#Increase of Z+
	incz_layout = QtGui.QHBoxLayout()
	incz_label = QtGui.QLabel("Increase of Z+: ")
	incz_input = QtGui.QLineEdit()
	incz_input.setMaxLength(10)	
	incz_input.setText(str(data['incz']))

	incz_layout.addWidget(incz_label)
	incz_layout.addWidget(incz_input)

	#Max parts out allowed
	partsoutmax_layout = QtGui.QHBoxLayout()
	partsoutmax_label = QtGui.QLabel("Max parts out allowed: ")
	partsoutmax_input = QtGui.QLineEdit()
	partsoutmax_input.setMaxLength(10)	
	partsoutmax_input.setText(str(data['partsoutmax']))

	partsoutmax_layout.addWidget(partsoutmax_label)
	partsoutmax_layout.addWidget(partsoutmax_input)

	#Minimum rhop valid
	rhopoutmin_layout = QtGui.QHBoxLayout()
	rhopoutmin_label = QtGui.QLabel("Minimum rhop valid: ")
	rhopoutmin_input = QtGui.QLineEdit()
	rhopoutmin_input.setMaxLength(10)	
	rhopoutmin_input.setText(str(data['rhopoutmin']))
	rhopoutmin_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")

	rhopoutmin_layout.addWidget(rhopoutmin_label)
	rhopoutmin_layout.addWidget(rhopoutmin_input)
	rhopoutmin_layout.addWidget(rhopoutmin_label2)

	#Maximum rhop valid
	rhopoutmax_layout = QtGui.QHBoxLayout()
	rhopoutmax_label = QtGui.QLabel("Maximum rhop valid: ")
	rhopoutmax_input = QtGui.QLineEdit()
	rhopoutmax_input.setMaxLength(10)	
	rhopoutmax_input.setText(str(data['rhopoutmax']))
	rhopoutmax_label2 = QtGui.QLabel("kg/m<span style='vertical-align:super'>3</span>")

	rhopoutmax_layout.addWidget(rhopoutmax_label)
	rhopoutmax_layout.addWidget(rhopoutmax_input)
	rhopoutmax_layout.addWidget(rhopoutmax_label2)	

	#------------ Button behaviour definition --------------
	def on_ok():
		data['posdouble'] = posdouble_input.text()
		data['stepalgorithm'] = stepalgorithm_input.text()
		data['verletsteps'] = verletsteps_input.text()
		data['kernel'] = kernel_input.text()
		data['viscotreatment'] = viscotreatment_input.text()
		data['visco'] = visco_input.text()
		data['viscoboundfactor'] = viscoboundfactor_input.text()
		data['deltasph'] = deltasph_input.text()
		data['shifting'] = shifting_input.text()
		data['shiftcoef'] = shiftcoef_input.text()
		data['shifttfs'] = shifttfs_input.text()
		data['rigidalgorithm'] = rigidalgorithm_input.text()
		data['ftpause'] = ftpause_input.text()
		data['coefdtmin'] = coefdtmin_input.text()
		data['dtini'] = dtini_input.text()
		data['dtini_auto'] = dtiniauto_chk.isChecked()
		data['dtmin'] = dtmin_input.text()
		data['dtmin_auto'] = dtminauto_chk.isChecked()
		data['dtfixed'] = dtfixed_input.text()
		data['dtallparticles'] = dtallparticles_input.text()
		data['timemax'] = timemax_input.text()
		data['timeout'] = timeout_input.text()
		data['incz'] = incz_input.text()
		data['partsoutmax'] = partsoutmax_input.text()
		data['rhopoutmin'] = rhopoutmin_input.text()
		data['rhopoutmax'] = rhopoutmax_input.text()
		print "DualSPHysics for FreeCAD: Execution Parameters changed"
		execparams_window.accept()

	def on_cancel():
		print "DualSPHysics for FreeCAD: Execution Parameters not changed"
		execparams_window.reject()

	ok_button.clicked.connect(on_ok)
	cancel_button.clicked.connect(on_cancel)
	#Button layout definition	
	ep_button_layout = QtGui.QHBoxLayout()
	ep_button_layout.addStretch(1)
	ep_button_layout.addWidget(ok_button)
	ep_button_layout.addWidget(cancel_button)

	#START Main layout definition and composition.
	ep_main_layout = QtGui.QVBoxLayout()
	
	ep_main_layout.addLayout(posdouble_layout)
	ep_main_layout.addLayout(stepalgorithm_layout)
	ep_main_layout.addLayout(verletsteps_layout)
	ep_main_layout.addLayout(kernel_layout)
	ep_main_layout.addLayout(viscotreatment_layout)
	ep_main_layout.addLayout(visco_layout)
	ep_main_layout.addLayout(viscoboundfactor_layout)
	ep_main_layout.addLayout(deltasph_layout)
	ep_main_layout.addLayout(shifting_layout)
	ep_main_layout.addLayout(shiftcoef_layout)
	ep_main_layout.addLayout(shifttfs_layout)
	ep_main_layout.addLayout(rigidalgorithm_layout)
	ep_main_layout.addLayout(ftpause_layout)
	ep_main_layout.addLayout(coefdtmin_layout)
	ep_main_layout.addLayout(dtiniauto_layout)
	ep_main_layout.addLayout(dtini_layout)
	ep_main_layout.addLayout(dtminauto_layout)
	ep_main_layout.addLayout(dtmin_layout)
	ep_main_layout.addLayout(dtallparticles_layout)
	ep_main_layout.addLayout(timemax_layout)
	ep_main_layout.addLayout(timeout_layout)
	ep_main_layout.addLayout(incz_layout)
	ep_main_layout.addLayout(partsoutmax_layout)
	ep_main_layout.addLayout(rhopoutmin_layout)
	ep_main_layout.addLayout(rhopoutmax_layout)

	ep_main_layout.addStretch(1)

	ep_groupbox = QtGui.QGroupBox("Execution Parameters")
	ep_groupbox.setLayout(ep_main_layout)
	execparams_window_layout = QtGui.QVBoxLayout()
	execparams_window_layout.addWidget(ep_groupbox)	
	execparams_window_layout.addLayout(ep_button_layout)
	execparams_window.setLayout(execparams_window_layout)
	#END Main layout definition and composition.

	execparams_window.resize(600,400)
	ret_val = execparams_window.exec_()

def def_setup_window():
	'''Defines the setup window'''
	#Creates a dialog and 2 main buttons
	setup_window = QtGui.QDialog()
	setup_window.setWindowTitle("DSPH Setup")
	ok_button = QtGui.QPushButton("Ok")
	cancel_button = QtGui.QPushButton("Cancel")

	#GenCase path
	gencasepath_layout = QtGui.QHBoxLayout()
	gencasepath_label = QtGui.QLabel("GenCase Path: ")
	gencasepath_input = QtGui.QLineEdit()
	gencasepath_input.setText(data["gencase_path"])
	gencasepath_input.setPlaceholderText("Put GenCase path here")
	gencasepath_browse = QtGui.QPushButton("...")

	gencasepath_layout.addWidget(gencasepath_label)
	gencasepath_layout.addWidget(gencasepath_input)
	gencasepath_layout.addWidget(gencasepath_browse)

	#DualSPHyisics path
	dsphpath_layout = QtGui.QHBoxLayout()
	dsphpath_label = QtGui.QLabel("DualSPHysics Path: ")
	dsphpath_input = QtGui.QLineEdit()
	dsphpath_input.setText(data["dsphysics_path"])
	dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
	dsphpath_browse = QtGui.QPushButton("...")

	dsphpath_layout.addWidget(dsphpath_label)
	dsphpath_layout.addWidget(dsphpath_input)
	dsphpath_layout.addWidget(dsphpath_browse)

	#PartVTK4 path
	partvtk4path_layout = QtGui.QHBoxLayout()
	partvtk4path_label = QtGui.QLabel("PartVTK4 Path: ")
	partvtk4path_input = QtGui.QLineEdit()
	partvtk4path_input.setText(data["partvtk4_path"])
	partvtk4path_input.setPlaceholderText("Put PartVTK4 path here")
	partvtk4path_browse = QtGui.QPushButton("...")

	partvtk4path_layout.addWidget(partvtk4path_label)
	partvtk4path_layout.addWidget(partvtk4path_input)
	partvtk4path_layout.addWidget(partvtk4path_browse)


	#------------ Button behaviour definition --------------
	def on_ok():
		data['gencase_path'] = gencasepath_input.text()
		data['dsphysics_path'] = dsphpath_input.text()
		data['partvtk4_path'] = partvtk4path_input.text()
		picklefile = open(App.getUserAppDataDir()+'/dsph_data.dsphdata', 'wb')
		pickle.dump(data, picklefile)
		print "DualSPHysics for FreeCAD: Setup changed. Saved to "+App.getUserAppDataDir()+"/dsph_data.dsphdata"
		state = check_executables()
		if not state:
			ex_selector_combo.setEnabled(False)
			ex_button.setEnabled(False)
			ex_additional.setEnabled(False)
		setup_window.accept()

	def on_cancel():
		print "DualSPHysics for FreeCAD: Setup not changed"
		setup_window.reject()

	def on_gencase_browse():
		filedialog = QtGui.QFileDialog()
		fileName, _ = filedialog.getOpenFileName(setup_window, "Select GenCase path", QtCore.QDir.homePath())
		if fileName != "":
			#Verify if exe is indeed gencase
			process = QtCore.QProcess(mw)
			process.start(fileName)
			process.waitForFinished()
			output = str(process.readAllStandardOutput())

			if "gencase" in output[0:15].lower():
				gencasepath_input.setText(fileName)
			else:
				print "ERROR: I can't recognize GenCase in that exe!"

	def on_dualsphysics_browse():
		filedialog = QtGui.QFileDialog()
		fileName, _ = filedialog.getOpenFileName(setup_window, "Select DualSPHysics path", QtCore.QDir.homePath())
		if fileName != "":
			#Verify if exe is indeed dualsphysics
			process = QtCore.QProcess(mw)
			process.start(fileName)
			process.waitForFinished()
			output = str(process.readAllStandardOutput())

			if "dualsphysics" in output[0:20].lower():
				dsphpath_input.setText(fileName)
			else:
				print "ERROR: I can't recognize DualSPHysics in that exe!"

	def on_partvtk4_browse():
		filedialog = QtGui.QFileDialog()
		fileName, _ = filedialog.getOpenFileName(setup_window, "Select PartVTK4 path", QtCore.QDir.homePath())
		if fileName != "":
			#Verify if exe is indeed dualsphysics
			process = QtCore.QProcess(mw)
			process.start(fileName)
			process.waitForFinished()
			output = str(process.readAllStandardOutput())

			if "partvtk4" in output[0:20].lower():
				partvtk4path_input.setText(fileName)
			else:
				print "ERROR: I can't recognize PartVTK4 in that exe!"

	ok_button.clicked.connect(on_ok)
	cancel_button.clicked.connect(on_cancel)
	gencasepath_browse.clicked.connect(on_gencase_browse)
	dsphpath_browse.clicked.connect(on_dualsphysics_browse)
	partvtk4path_browse.clicked.connect(on_partvtk4_browse)
	#Button layout definition	
	stp_button_layout = QtGui.QHBoxLayout()
	stp_button_layout.addStretch(1)
	stp_button_layout.addWidget(ok_button)
	stp_button_layout.addWidget(cancel_button)

	#START Main layout definition and composition.
	stp_main_layout = QtGui.QVBoxLayout()
	stp_main_layout.addLayout(gencasepath_layout)
	stp_main_layout.addLayout(dsphpath_layout)
	stp_main_layout.addLayout(partvtk4path_layout)
	stp_main_layout.addStretch(1)

	stp_groupbox = QtGui.QGroupBox("Setup parameters")
	stp_groupbox.setLayout(stp_main_layout)
	setup_window_layout = QtGui.QVBoxLayout()
	setup_window_layout.addWidget(stp_groupbox)	
	setup_window_layout.addLayout(stp_button_layout)
	setup_window.setLayout(setup_window_layout)
	#END Main layout definition and composition.

	setup_window.resize(600,400)
	ret_val = setup_window.exec_()

def def_help():
	webbrowser.open("http://dual.sphysics.org/gui/wiki/")

#Main Widget layout. Vertical ordering
main_layout = QtGui.QVBoxLayout()

#Component layouts definition
logo_layout = QtGui.QHBoxLayout() #Maybe not, needs work
intro_layout = QtGui.QVBoxLayout()

#Components by layout
constants_label = QtGui.QLabel("\nConstant Definition and Execution Parameters: \nYou can modify values to customize the simulation. If not set, the parameters would be at default values.")
constants_label.setWordWrap(True)
constants_button = QtGui.QPushButton("Define Constants")
constants_button.setToolTip("Use this button to define case constants,\nsuch as lattice, gravity or fluid reference density.")
constants_button.clicked.connect(def_constants_window)
help_button = QtGui.QPushButton("Help")
help_button.setToolTip("Push this button to open a browser with help\non how to use this tool.")
help_button.clicked.connect(def_help)
setup_button = QtGui.QPushButton("Setup Plugin")
setup_button.setToolTip("Setup of the simulator executables")
setup_button.clicked.connect(def_setup_window)
execparams_button = QtGui.QPushButton("Execution Parameters")
execparams_button.setToolTip("Change execution parameters, such as\ntime of simulation, viscosity, etc.")
execparams_button.clicked.connect(def_execparams_window)
constants_separator = QtGui.QFrame()
constants_separator.setFrameStyle(QtGui.QFrame.HLine)

crucialvars_separator = QtGui.QFrame()
crucialvars_separator.setFrameStyle(QtGui.QFrame.HLine)

#Logo layout related operations
logo_label = QtGui.QLabel()
logo_label.setPixmap(App.getUserAppDataDir() + "Macro/DSPH_Images/logo.png")

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
casecontrols_bt_newdoc.setIcon(QtGui.QIcon(App.getUserAppDataDir() + "Macro/DSPH_Images/new.png"));
casecontrols_bt_newdoc.setIconSize(QtCore.QSize(28,28));
casecontrols_bt_savedoc = QtGui.QPushButton("  Save Case")
casecontrols_bt_savedoc.setToolTip("Saves the case and executes GenCase over.\nIf GenCase fails or is not set up, only the case\nwill be saved.")
casecontrols_bt_savedoc.setIcon(QtGui.QIcon(App.getUserAppDataDir() + "Macro/DSPH_Images/save.png"));
casecontrols_bt_savedoc.setIconSize(QtCore.QSize(28,28));
casecontrols_bt_loaddoc = QtGui.QPushButton("  Load Case")
casecontrols_bt_loaddoc.setToolTip("Loads a case from disk. All the current documents\nwill be closed.")
casecontrols_bt_loaddoc.setIcon(QtGui.QIcon(App.getUserAppDataDir() + "Macro/DSPH_Images/load.png"));
casecontrols_bt_loaddoc.setIconSize(QtCore.QSize(28,28));

casecontrols_bt_addfillbox = QtGui.QPushButton("Add fillbox")
casecontrols_bt_addfillbox.setToolTip("Adds a FillBox. A FillBox is able to fill an empty space\nwithin limits of geometry and a maximum bounding\nbox placed by the user.")
casecontrols_bt_addfillbox.setEnabled(False)

def on_new_case():
	'''Defines what happens when new case is clicked. Closes all documents
	if possible and creates a FreeCAD document with Case Limits object.'''
	if len(App.listDocuments().keys()) > 0:
		newConfirmDialog = QtGui.QMessageBox()
		newConfirmDialog.setText("DualSPHysics for FreeCAD")
		newConfirmDialog.setInformativeText("To make a new case you must close all the open documents. Close all the documents?")
		newConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
		newConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
		openCDRet = newConfirmDialog.exec_()

		if openCDRet == QtGui.QMessageBox.Ok:
			print "DualSPHysics for FreeCAD: New File. Closing all documents..."
			for doc in App.listDocuments().keys():
				App.closeDocument(doc)
		else:
			return

	App.newDocument("DSPH_Case")
	App.setActiveDocument("DSPH_Case")
	App.ActiveDocument=App.getDocument("DSPH_Case")
	Gui.ActiveDocument=Gui.getDocument("DSPH_Case")
	Gui.activateWorkbench("PartWorkbench")
	Gui.activeDocument().activeView().viewAxonometric()
	App.ActiveDocument.addObject("Part::Box","Case_Limits")
	App.ActiveDocument.getObject("Case_Limits").Label = "Case_Limits"
	App.ActiveDocument.getObject("Case_Limits").Length = '15 mm'
	App.ActiveDocument.getObject("Case_Limits").Width = '15 mm'
	App.ActiveDocument.getObject("Case_Limits").Height = '15 mm'
	App.ActiveDocument.getObject("Case_Limits").Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
	Gui.ActiveDocument.getObject("Case_Limits").DisplayMode = "Wireframe"
	Gui.ActiveDocument.getObject("Case_Limits").LineColor = (1.00,0.00,0.00)
	Gui.ActiveDocument.getObject("Case_Limits").LineWidth = 2.00
	Gui.ActiveDocument.getObject("Case_Limits").Selectable = False
	App.ActiveDocument.recompute()
	Gui.SendMsgToActiveView("ViewFit")
	set_default_data()
	constants_button.setEnabled(True)
	execparams_button.setEnabled(True)
	casecontrols_bt_savedoc.setEnabled(True)
	dp_input.setEnabled(True)
	ex_selector_combo.setEnabled(False)
	ex_button.setEnabled(False)
	ex_additional.setEnabled(False)
	export_button.setEnabled(False)
	casecontrols_bt_addfillbox.setEnabled(True)
	data['simobjects']['Case_Limits'] = ["mkspecial", "typespecial", "fillspecial"]
	on_tree_item_selection_change()

def on_save_case():
	'''Defines what happens when save case button is clicked.
	Saves a freecad scene definition, a dump of dsph data useful for this macro
	and tries to generate a case with gencase.'''
	#Watch if save path is available. Prompt the user if not.
	if (data["project_path"] == "") and (data["project_name"] == ""):
		saveName, _ = QtGui.QFileDialog.getSaveFileName(dsph_dock, "Save Case", QtCore.QDir.homePath())
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
		App.getDocument("DSPH_Case").saveAs(saveName+"/DSPH_Case.FCStd")
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
		min_point = App.ActiveDocument.getObject("Case_Limits").Placement.Base
		max_point = App.ActiveDocument.getObject("Case_Limits")
		f.write('\t\t\t\t<pointmin x="'+str(min_point.x / 1000)+'" y="'+str(min_point.y / 1000)+'" z="'+str(min_point.z / 1000)+'" />\n')
		f.write('\t\t\t\t<pointmax x="'+str(min_point.x / 1000 + max_point.Length.Value / 1000)+'" y="'+str(min_point.y / 1000 + max_point.Width.Value / 1000)+'" z="'+str(min_point.z / 1000 + max_point.Height.Value / 1000)+'" />\n')
		f.write('\t\t\t</definition>\n')
		f.write('\t\t\t<commands>\n')
		f.write('\t\t\t\t<mainlist>\n')
		#Export in strict order
		for key in data["export_order"]:
			name = key
			valuelist = data["simobjects"][name]
			o = App.getDocument("DSPH_Case").getObject(name)
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
			process = QtCore.QProcess(mw)
			process.start(data["gencase_path"], [data["project_path"]+"/"+data["project_name"]+"_Def", data["project_path"]+"/"+data["project_name"]+"_Out/"+data["project_name"], "-save:+all"])
			process.waitForFinished()
			output = str(process.readAllStandardOutput())
			if str(process.exitCode()) == "0":
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
			else:
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
	loadName, _ = QtGui.QFileDialog.getOpenFileName(dsph_dock, "Load Case", QtCore.QDir.homePath(), "casedata.dsphdata")
	if loadName == "":
		#User pressed cancel. No path is selected.
		return
	load_project_name = loadName.split("/")[-2]
	load_path_project_folder = "/".join(loadName.split("/")[:-1])
	if not os.path.isfile(load_path_project_folder + "/DSPH_Case.FCStd"):
		#TODO: Needs dialog
		print "ERROR: DSPH_Case.FCStd file not found! Corrupt or moved project. Aborting."
		return

	#Tries to close all documents
	if len(App.listDocuments().keys()) > 0:
		loadConfirmDialog = QtGui.QMessageBox()
		loadConfirmDialog.setText("DualSPHysics for FreeCAD")
		loadConfirmDialog.setInformativeText("To load a case you must close all the open documents. Close all the documents?")
		loadConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
		loadConfirmDialog.setDefaultButton(QtGui.QMessageBox.Ok)
		loadCDRet = loadConfirmDialog.exec_()

		if loadCDRet == QtGui.QMessageBox.Ok:
			print "DualSPHysics for FreeCAD: Load File. Closing all documents..."
			for doc in App.listDocuments().keys():
				App.closeDocument(doc)
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
	else:
		export_button.setEnabled(False)
	casecontrols_bt_addfillbox.setEnabled(True)

	os.chdir(data["project_path"])
	correct_execs = check_executables()
	if not correct_execs:
		ex_selector_combo.setEnabled(False)
		ex_button.setEnabled(False)
		ex_additional.setEnabled(False)
		export_button.setEnabled(False)

	on_tree_item_selection_change()

def on_add_fillbox():
	'''Add fillbox group. It consists
	in a group with 2 objects inside: a point and a box.
	The point represents the fill seed and the box sets
	the bounds for the filling'''
	fillbox_gp = App.getDocument("DSPH_Case").addObject("App::DocumentObjectGroup","FillBox")
	fillbox_point = App.ActiveDocument.addObject("Part::Sphere","FillPoint")
	fillbox_limits = App.ActiveDocument.addObject("Part::Box","FillLimit")
	fillbox_limits.ViewObject.DisplayMode = "Wireframe"
	fillbox_limits.ViewObject.LineColor = (0.00,0.78,1.00)
	fillbox_point.Radius.Value = 0.2
	fillbox_point.Placement.Base = App.Vector(5,5,5)
	fillbox_point.ViewObject.ShapeColor = (0.00,0.00,0.00)
	fillbox_gp.addObject(fillbox_limits)
	fillbox_gp.addObject(fillbox_point)
	App.ActiveDocument.recompute()
	Gui.SendMsgToActiveView("ViewFit")

#Connect case control buttons
casecontrols_bt_newdoc.clicked.connect(on_new_case)
casecontrols_bt_savedoc.clicked.connect(on_save_case)
casecontrols_bt_loaddoc.clicked.connect(on_load_case)
casecontrols_bt_addfillbox.clicked.connect(on_add_fillbox)

#Defines case control scaffolding
cclabel_layout.addWidget(casecontrols_label)
ccfilebuttons_layout.addWidget(casecontrols_bt_newdoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_savedoc)
ccfilebuttons_layout.addWidget(casecontrols_bt_loaddoc)
ccaddbuttons_layout.addWidget(casecontrols_bt_addfillbox)
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
			last_line_parttime = run_file_data[-1].split("      ")
			if "Part_" in last_line_parttime[0]:
				current_value = (float(last_line_parttime[1]) * float(100)) / float(data["timemax"])
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
		data['additional_parameters'] = paramintro_input.text()
		additional_parameters_window.accept()

	def on_cancel():
		additional_parameters_window.reject()

	ok_button.clicked.connect(on_ok)
	cancel_button.clicked.connect(on_cancel)
	#Button layout definition	
	ap_button_layout = QtGui.QHBoxLayout()
	ap_button_layout.addStretch(1)
	ap_button_layout.addWidget(ok_button)
	ap_button_layout.addWidget(cancel_button)

	paramintro_layout = QtGui.QHBoxLayout()
	paramintro_label = QtGui.QLabel("Additional Parameters: ")
	paramintro_input = QtGui.QLineEdit()
	paramintro_input.setText(data["additional_parameters"])
	paramintro_layout.addWidget(paramintro_label)
	paramintro_layout.addWidget(paramintro_input)

	additional_parameters_layout = QtGui.QVBoxLayout()
	additional_parameters_layout.addLayout(paramintro_layout)
	additional_parameters_layout.addStretch(1)
	additional_parameters_layout.addLayout(ap_button_layout)

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

def on_export():
	'''Export VTK button behaviour.
	Launches a process while disabling the button.'''
	temp_data["export_button"].setEnabled(False)
	temp_data["export_button"].setText("Exporting...")

	def on_export_finished(exitCode):
		temp_data["export_button"].setText("Export data to VTK")
		temp_data["export_button"].setEnabled(True)

	export_process = QtCore.QProcess(dsph_dock)
	export_process.finished.connect(on_export_finished)
	export_process.start(data["partvtk4_path"], ["-dirin "+data["project_path"]+"/"+data["project_name"]+"_Out/", "-savevtk "+data["project_path"]+"/"+data["project_name"]+"_Out/PartAll"])

	temp_data["current_export_process"] = export_process

#Export to VTK section scaffolding
export_layout = QtGui.QVBoxLayout()
export_label = QtGui.QLabel("This is the export section. Once a simulation is made, you can export to VTK the files generated by DualSPHysics. Press the button below to export")
export_label.setWordWrap(True)
export_button = QtGui.QPushButton("Export data to VTK")
export_button.setToolTip("Exports the simulation data to VTK format.")
export_button.clicked.connect(on_export)
temp_data["export_button"] = export_button
export_layout.addWidget(export_label)
export_layout.addWidget(export_button)

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

'''You can't apply layouts to a QDockWidget, 
so creating a standard widget, applying the layouts, 
and then setting it as the QDockWidget'''
scaff_widget.setLayout(main_layout)
dsph_dock.setWidget(scaff_widget)

#And docking it at right side of screen
mw.addDockWidget(QtCore.Qt.RightDockWidgetArea,dsph_dock)

#------------------------ DSPH OBJECT PROPERTIES DOCK RELATED CODE ----------------------------
#Tries to find and close previous instances of the widget.
previous_dock = mw.findChild(QtGui.QDockWidget, "DSPH_Properties")
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
property_table = QtGui.QTableWidget(4,2)
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
propertylabel1.setAlignment(QtCore.Qt.AlignLeft)
propertylabel2.setAlignment(QtCore.Qt.AlignLeft)
propertylabel3.setAlignment(QtCore.Qt.AlignLeft)
propertylabel4.setAlignment(QtCore.Qt.AlignLeft)
property_table.setCellWidget(0,0, propertylabel1)
property_table.setCellWidget(1,0, propertylabel2)
property_table.setCellWidget(2,0, propertylabel3)
property_table.setCellWidget(3,0, propertylabel4)

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
	elif property2.itemText(index).lower() == "fluid":
		property1.setRange(0, 10)
		selectiongui.ShapeColor = (0.00,0.45,1.00)
		selectiongui.Transparency = 30

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
		#TODO: Warn the user of changing all of this mks
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


#Property change widgets
property1 = QtGui.QSpinBox()
property2 = QtGui.QComboBox()
property3 = QtGui.QComboBox()
property4 = QtGui.QPushButton("Configure")
property1.setRange(0, 240)
property2.insertItems(0, ["Fluid", "Bound"])
property3.insertItems(1, ["Full", "Solid", "Face", "Wire"])
property1.valueChanged.connect(property1_change)
property2.currentIndexChanged.connect(property2_change)
property3.currentIndexChanged.connect(property3_change)
property4.clicked.connect(property4_configure)
property_table.setCellWidget(0,1, property1)
property_table.setCellWidget(1,1, property2)
property_table.setCellWidget(2,1, property3)
property_table.setCellWidget(3,1, property4)

#Dock the widget to the left side of screen
mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, properties_widget)

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
				mktoput = get_first_mk_not_used("fluid")
				if not mktoput:
					mktoput = 0
				data['simobjects'][item.Name] = [mktoput, 'fluid', 'full']
				data["mkfluidused"].append(mktoput)
			else:
				mktoput = get_first_mk_not_used("bound")
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
for item in mw.findChildren(QtGui.QTreeWidget):
	if item.objectName() != "DSPH Objects":
		trees.append(item)

def up_clicked(row):
	print "to be implemented. Reorder up on element " + str(row)
	pass

def down_clicked(row):
	print "to be implemented. Reorder down on element " + str(row)
	pass

def on_tree_item_selection_change():
	selection = FreeCADGui.Selection.getSelection()
	objectNames = []
	for item in App.getDocument("DSPH_Case").Objects:
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
				else:
					if selection[0].TypeId == "App::DocumentObjectGroup" and "fillbox" in selection[0].Name.lower():
						toChange.setEnabled(True)
						if data['simobjects'][selection[0].Name][1].lower() == "fluid":
							toChange.setCurrentIndex(0)
							property1.setRange(0, 10)
						elif data['simobjects'][selection[0].Name][1].lower() == "bound":
							toChange.setCurrentIndex(1)
							property1.setRange(0, 240)
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
				pass
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
				pass
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
		contextObject = App.getDocument("DSPH_Case").getObject(key)
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
		toDeleteKey = data["simobjects"].values().index(each)
		data["simobjects"].pop(each, None)
		data["export_order"].remove(toDeleteKey)

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
			ex_button.setEnabled(False)
			ex_additional.setEnabled(False)
			ex_selector_combo.setEnabled(False)
			export_button.setEnabled(False)
			objectlist_table.setEnabled(False)
			threading._sleep(2)
			continue

		threading._sleep(0.5)

monitor_thread = threading.Thread(target=selection_monitor)
monitor_thread.start()

FreeCADGui.activateWorkbench("PartWorkbench")
print "DualSPHysics for FreeCAD: Done loading data."
