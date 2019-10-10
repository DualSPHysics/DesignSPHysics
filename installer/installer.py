# -*- coding: utf-8 -*-
"""DesignSPHysics Installer.

This file spawns a Qt window that installs DSPH files
into FreeCAD's default Macro directory.

This script is meant to use with pyinstaller to generate
a simple standalone executable for release.

"""

import sys
import shutil
import platform
import os
import ctypes
from PySide import QtGui, QtCore

# Copyright (C) 2019
# EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo
#
# This file is part of DesignSPHysics.
#
# DesignSPHysics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DesignSPHysics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.

print("Copyright (C) 2016-2019")
print("EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo")


def dprint(string):
    """ Prints a debug message in the terminal window """
    print(">>>Debug: {}".format(str(string)))


def is_user_admin():
    """ Return True if user has admin privileges. """

    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        # Probably linux, admin not needed so true
        return True


def main():
    """ Main function of the installer. Initializes a window
        that enables the user to install the software. """

    app = QtGui.QApplication(sys.argv)

    w = QtGui.QDialog()
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("UTF-8"))

    w.setWindowFlags(QtCore.Qt.Dialog)
    w.setWindowTitle("DualSPHysics Installer")

    main_layout = QtGui.QVBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    image_label = QtGui.QLabel()
    image_label.setPixmap("./resource/installer-image.png")

    install_layout = QtGui.QVBoxLayout()
    install_layout.setContentsMargins(10, 10, 10, 10)
    description_label = QtGui.QLabel("DesignSPHysics is a macro made for FreeCAD that allows the user to design case environments to use with DualSPHyisics.")
    description_label.setWordWrap(True)
    description_label.setAlignment(QtCore.Qt.AlignCenter)
    credits_label = QtGui.QLabel("DualSPHysics team.\nDeveloped by Andrés Vieira (Universidade de Vigo).\n")
    credits_label.setWordWrap(True)
    credits_label.setAlignment(QtCore.Qt.AlignCenter)
    credits_label.setStyleSheet("font: 7pt;")
    install_button_layout = QtGui.QHBoxLayout()
    install_button = QtGui.QPushButton("Install")
    installopts_selector = QtGui.QComboBox()
    installopts_selector.addItems(["Complete (With DualSPHysics)", "DesignSPHysics only"])
    install_button_layout.addStretch(1)
    install_button_layout.addWidget(install_button)
    install_button_layout.addWidget(installopts_selector)
    install_button_layout.addStretch(1)

    install_layout.addWidget(description_label)
    install_layout.addStretch(1)
    install_layout.addWidget(credits_label)
    install_layout.addLayout(install_button_layout)

    def on_install():
        """ Defines what happens when install button
            is pressed. """
        install_button.setEnabled(False)
        install_button.setText("Installing...")
        system = platform.system()
        try:
            if os.path.isdir("./resource/images") and os.path.isfile("./resource/DesignSPHysics.py"):

                # Set the directory depending on the system.
                if "windows" in system.lower():
                    macro_dir = os.getenv("APPDATA") + "/FreeCAD/Macro"
                    fc_default_mod_dir = os.getenv(
                        "APPDATA") + "/FreeCAD/Mod"
                elif "linux" in system.lower():
                    macro_dir = os.path.expanduser("~") + "/.FreeCAD/Macro"
                    fc_default_mod_dir = os.path.expanduser("~") + "/.FreeCAD/Mod"
                else:
                    # Operating system not supported
                    install_button.setText("ERROR :(")
                    install_failed_dialog = QtGui.QMessageBox()
                    install_failed_dialog.setText("DesignSPHysics encountered an error while installing. " "Click on view details for more info.")
                    install_failed_dialog.setDetailedText("Operating system not supported: " + str(system))
                    install_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
                    install_failed_dialog.exec_()
                    sys.exit(1)

                # Try to remove files from previous and current versions
                if not os.path.isdir(macro_dir):
                    os.makedirs(macro_dir)
                if not os.path.isdir(fc_default_mod_dir):
                    os.makedirs(fc_default_mod_dir)
                try:
                    os.remove(macro_dir + "/DesignSPHysics.py")
                except OSError:
                    # File does not exists.  Ignoring
                    pass
                try:
                    os.remove(macro_dir + "/DSPH.py")
                except OSError:
                    # File does not exists.  Ignoring
                    pass
                try:
                    os.remove(macro_dir + "/default-config.json")
                except OSError:
                    # File does not exists.  Ignoring
                    pass
                try:
                    os.remove(macro_dir + "/LICENSE")
                except OSError:
                    # File does not exists.  Ignoring
                    pass
                try:
                    shutil.rmtree(macro_dir + "/images")
                except OSError:
                    # Directory does not exists.  Ignoring
                    pass
                try:
                    shutil.rmtree(macro_dir + "/mod")
                except OSError:
                    # Directory does not exists.  Ignoring
                    pass
                try:
                    shutil.rmtree(fc_default_mod_dir + "/DesignSPHysics")
                except OSError:
                    # Directory does not exists.  Ignoring
                    pass
                try:
                    os.remove(macro_dir + "/DesignSPHysics.FCMacro")
                except OSError:
                    # File does not exists.  Ignoring
                    pass

                # Create installation directory
                if not os.path.exists(fc_default_mod_dir + "/DesignSPHysics"):
                    os.mkdir(fc_default_mod_dir + "/DesignSPHysics")

                # Copy new files
                shutil.copy("./resource/DesignSPHysics.py", fc_default_mod_dir + "/DesignSPHysics")
                shutil.copy("./resource/LICENSE", fc_default_mod_dir + "/DesignSPHysics")
                shutil.copy("./resource/DesignSPHysics.FCMacro", macro_dir)
                shutil.copy("./resource/default-config.json", fc_default_mod_dir + "/DesignSPHysics")
                shutil.copytree("./resource/images", fc_default_mod_dir + "/DesignSPHysics" + "/images")
                shutil.copytree("./resource/mod", fc_default_mod_dir + "/DesignSPHysics" + "/mod")

                if installopts_selector.currentIndex() == 0:
                    try:
                        shutil.rmtree(fc_default_mod_dir + "/DesignSPHysics" + "/dualsphysics")
                    except OSError:
                        # Directory does not exists.  Ignoring
                        pass
                    shutil.copytree("./resource/dualsphysics", fc_default_mod_dir + "/DesignSPHysics" + "/dualsphysics")

                # Installation completed
                install_button.setText("Installed!")
                install_success_dialog = QtGui.QMessageBox()
                install_success_dialog.setText("DesignSPHysics installed correctly.")
                install_success_dialog.setIcon(QtGui.QMessageBox.Information)
                install_success_dialog.exec_()
                sys.exit(0)
                return
            else:
                raise Exception("images or DesignSPHysics.py are not in the resource folder.")
        except Exception as e:
            # Something failed, show error
            install_button.setText("ERROR :(")
            install_failed_dialog = QtGui.QMessageBox()
            install_failed_dialog.setText("DesignSPHysics encountered an error while installing. Click on view details for more info.")
            install_failed_dialog.setDetailedText("Exception " + str(e.__class__.__name__) + " encountered.\nError message: " + str(e))
            install_failed_dialog.setIcon(QtGui.QMessageBox.Critical)
            install_failed_dialog.exec_()
            return

    install_button.clicked.connect(on_install)
    main_layout.addWidget(image_label)
    main_layout.addLayout(install_layout)
    w.setLayout(main_layout)
    w.show()
    app.exec_()
    sys.exit(0)


if __name__ == "__main__":
    main()
