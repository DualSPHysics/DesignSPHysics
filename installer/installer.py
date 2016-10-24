# -*- coding: utf-8 -*-

import sys, threading, shutil, platform, os
from PySide import QtGui, QtCore

def dprint(string):
	print ">>>Debug: " + str(string)

def main():
	app = QtGui.QApplication(sys.argv)

	w = QtGui.QDialog()
	QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName('UTF-8'))
	w.setFixedSize(400, 500)

	w.setWindowFlags(QtCore.Qt.Dialog)
	w.setWindowTitle('DSPH for FreeCAD Installer')
	
	main_layout = QtGui.QVBoxLayout()
	main_layout.setContentsMargins(0,0,0,0)
	image_label = QtGui.QLabel()
	image_label.setPixmap("./resource/installer-image.png")
	
	install_layout = QtGui.QVBoxLayout()
	install_layout.setContentsMargins(10,10,10,10)
	description_label = QtGui.QLabel('DualSPHysics for FreeCAD is a macro made for FreeCAD that lets the user design case environments to use with DualSPHyisics.')
	description_label.setWordWrap(True)
	description_label.setAlignment(QtCore.Qt.AlignCenter)
	credits_label = QtGui.QLabel("EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo\nSchool of Mechanical, Aerospace and Civil Engineering, University of Manchester.\nDeveloped by Andrés Vieira.\n")
	credits_label.setWordWrap(True)
	credits_label.setAlignment(QtCore.Qt.AlignCenter)
	credits_label.setStyleSheet("font: 7pt;")
	install_button_layout = QtGui.QHBoxLayout()
	install_button = QtGui.QPushButton('Install')
	install_button_layout.addStretch(1)
	install_button_layout.addWidget(install_button)
	install_button_layout.addStretch(1)

	install_layout.addWidget(description_label)
	install_layout.addStretch(1)
	install_layout.addWidget(credits_label)
	install_layout.addLayout(install_button_layout)

	def on_install():
		def threadfunc():
			install_button.setEnabled(False)
			install_button.setText('Installing...')
			system = platform.system()
			dprint(system)
			if 'windows' in system.lower():
				dest_folder = os.getenv('APPDATA') + '/FreeCAD/Macro'
				if not os.path.isdir(dest_folder):
					os.makedirs(dest_folder)
				dprint(dest_folder)
				shutil.copy("./resource/DSPH.py" , dest_folder)
				shutil.copytree("./resource/DSPH_Images" , dest_folder + '/DSPH_Images')
			elif 'linux' in system.lower():
				dest_folder = os.path.expanduser('~') + '/.FreeCAD/Macro'
				if not os.path.isdir(dest_folder):
					os.makedirs(dest_folder)
				dprint(dest_folder)
				shutil.copy("./resource/DSPH.py" , dest_folder)
				shutil.copytree("./resource/DSPH_Images" , dest_folder + '/DSPH_Images')
			elif 'darwin' in system.lower():
				#TODO: OS X not supported. spawn dialog
				pass
			else:
				pass
			install_button.setText('Installed!')
		
		installthread = threading.Thread(target=threadfunc)
		installthread.start()

	install_button.clicked.connect(on_install)
	main_layout.addWidget(image_label)
	main_layout.addLayout(install_layout)
	w.setLayout(main_layout)
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()