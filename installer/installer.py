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

print "Copyright (C) 2016 - Andrés Vieira"
print "EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo"

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
    description_label = QtGui.QLabel('DualSPHysics for FreeCAD is a macro made for FreeCAD that allows the user to design case environments to use with DualSPHyisics.')
    description_label.setWordWrap(True)
    description_label.setAlignment(QtCore.Qt.AlignCenter)
    credits_label = QtGui.QLabel("DualSPHysics team.\nDeveloped by Andrés Vieira (Universidade de Vigo).\n")
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
            try:
                if os.path.isdir("./resource/DSPH_Images") and os.path.isfile("./resource/DSPH.py"):

                    #Set the directory depending on the system.
                    if 'windows' in system.lower():
                        dest_folder = os.getenv('APPDATA') + '/FreeCAD/Macro'
                    elif 'linux' in system.lower():
                        dest_folder = os.path.expanduser('~') + '/.FreeCAD/Macro'
                    else:
                        #Operating system not supported
                        install_button.setText('ERROR :(')
                        install_failed_dialog = QtGui.QMessageBox()
                        install_failed_dialog.setText("DualSPHysics for FreeCAD encountered an error while installing. Click on view details for more info.")
                        install_failed_dialog.setDetailedText("Operating system not supported: " + str(system))
                        install_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
                        install_failed_dialog.exec_()
                        sys.exit(1)

                    #Try to remove previous files
                    if not os.path.isdir(dest_folder):
                        os.makedirs(dest_folder)
                    try:
                        os.remove(dest_folder + 'DSPH.py')
                    except OSError as e:
                        #File does not exists. Ignoring
                        pass
                    try:
                        os.remove(dest_folder + 'LICENSE')
                    except OSError as e:
                        #File does not exists. Ignoring
                        pass
                    try:
                        shutil.rmtree(dest_folder + '/DSPH_Images')
                    except OSError as e:
                        #Directory does not exists. Ignoring
                        pass
                    try:
                        shutil.rmtree(dest_folder + '/dsphfc')
                    except OSError as e:
                        #Directory does not exists. Ignoring
                        pass

                    #Copy new files
                    shutil.copy("./resource/DSPH.py" , dest_folder)
                    shutil.copy("./resource/LICENSE" , dest_folder)
                    shutil.copytree("./resource/DSPH_Images" , dest_folder + '/DSPH_Images')
                    shutil.copytree("./resource/dsphfc" , dest_folder + '/dsphfc')

                    #Installation completed
                    install_button.setText('Installed!')
                    install_success_dialog = QtGui.QMessageBox()
                    install_success_dialog.setText("DualSPHysics for FreeCAD installed correctly.")
                    install_success_dialog.setIcon(QtGui.QMessageBox.Information)
                    install_success_dialog.exec_()
                    sys.exit(0)
                else:
                    raise Exception('DSPH_Images or DSPH.py are not in the resource folder.')
            except Exception as e:
                #Something failed, show error
                install_button.setText('ERROR :(')
                install_failed_dialog = QtGui.QMessageBox()
                install_failed_dialog.setText("DualSPHysics for FreeCAD encountered an error while installing. Click on view details for more info.")
                install_failed_dialog.setDetailedText("Exception " + str(e.__class__.__name__) + " encountered.\nError message: " + str(e))
                install_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
                install_failed_dialog.exec_()
                sys.exit(0)

        
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