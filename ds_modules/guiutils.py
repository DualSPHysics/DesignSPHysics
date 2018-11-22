#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""DesignSPHysics GUI Utils.

This module stores functionality useful for GUI
operations in DesignSPHysics.

"""

import FreeCAD
import FreeCADGui
import pickle
import sys
import os
import utils
import constants
import subprocess
from sys import platform

reload(sys)
sys.setdefaultencoding('utf-8')

from PySide import QtGui, QtCore
from execution_parameters import *

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


def h_line_generator():
    """ Generates an horizontal line that can be used as a separator."""
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.HLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def v_line_generator():
    """ Generates a vertical line that can be used as a separator"""
    to_ret = QtGui.QFrame()
    to_ret.setFrameShape(QtGui.QFrame.VLine)
    to_ret.setFrameShadow(QtGui.QFrame.Sunken)
    return to_ret


def warning_dialog(warn_text, detailed_text=None):
    """Spawns a warning dialog with the text and details passed."""

    warning_messagebox = QtGui.QMessageBox()
    warning_messagebox.setText(str(warn_text))
    warning_messagebox.setIcon(QtGui.QMessageBox.Warning)
    if detailed_text is not None:
        warning_messagebox.setDetailedText(str(detailed_text))
    warning_messagebox.exec_()


def error_dialog(error_text, detailed_text=None):
    """Spawns an error dialog with the text and details passed."""

    error_messagebox = QtGui.QMessageBox()
    error_messagebox.setText(error_text)
    error_messagebox.setIcon(QtGui.QMessageBox.Critical)
    if detailed_text is not None:
        error_messagebox.setDetailedText(str(detailed_text))
    error_messagebox.exec_()


def info_dialog(info_text, detailed_text=None):
    """Spawns an info dialog with the text and details passed."""

    info_messagebox = QtGui.QMessageBox()
    info_messagebox.setText(info_text)
    info_messagebox.setIcon(QtGui.QMessageBox.Information)
    if detailed_text is not None:
        info_messagebox.setDetailedText(str(detailed_text))
    info_messagebox.exec_()


def ok_cancel_dialog(title, text):
    """Spawns an okay/cancel dialog with the title and text passed"""

    open_confirm_dialog = QtGui.QMessageBox()
    open_confirm_dialog.setWindowTitle(title)
    open_confirm_dialog.setText(text)
    open_confirm_dialog.setStandardButtons(QtGui.QMessageBox.Ok |
                                           QtGui.QMessageBox.Cancel)
    open_confirm_dialog.setDefaultButton(QtGui.QMessageBox.Ok)
    return open_confirm_dialog.exec_()


def get_icon(file_name, return_only_path=False):
    """ Returns a QIcon to use with DesignSPHysics.
    Retrieves a file with filename (like image.png) from the images folder. """
    file_to_load = os.path.dirname(os.path.abspath(__file__)) + "/../images/{}".format(file_name)
    if os.path.isfile(file_to_load):
        return file_to_load if return_only_path else QtGui.QIcon(file_to_load)
    else:
        raise IOError("File {} not found in images folder".format(file_name))


def get_fc_main_window():
    """ Returns FreeCAD main window. """
    return FreeCADGui.getMainWindow()


def def_setup_window(data):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    # TODO: This should be implemented as a custom class like SetupDialog(QtGui.QDialog)

    # Creates a dialog and 2 main buttons
    setup_window = QtGui.QDialog()
    setup_window.setWindowTitle("DSPH Setup")
    ok_button = QtGui.QPushButton("Ok")
    cancel_button = QtGui.QPushButton("Cancel")

    # GenCase path
    gencasepath_layout = QtGui.QHBoxLayout()
    gencasepath_label = QtGui.QLabel("GenCase Path: ")
    gencasepath_input = QtGui.QLineEdit()
    gencasepath_input.setText(data["gencase_path"])
    gencasepath_input.setPlaceholderText("Put GenCase path here")
    gencasepath_browse = QtGui.QPushButton("...")

    gencasepath_layout.addWidget(gencasepath_label)
    gencasepath_layout.addWidget(gencasepath_input)
    gencasepath_layout.addWidget(gencasepath_browse)

    # DualSPHyisics path
    dsphpath_layout = QtGui.QHBoxLayout()
    dsphpath_label = QtGui.QLabel("DualSPHysics Path: ")
    dsphpath_input = QtGui.QLineEdit()
    dsphpath_input.setText(data["dsphysics_path"])
    dsphpath_input.setPlaceholderText("Put DualSPHysics path here")
    dsphpath_browse = QtGui.QPushButton("...")

    dsphpath_layout.addWidget(dsphpath_label)
    dsphpath_layout.addWidget(dsphpath_input)
    dsphpath_layout.addWidget(dsphpath_browse)

    # PartVTK4 path
    partvtk4path_layout = QtGui.QHBoxLayout()
    partvtk4path_label = QtGui.QLabel("PartVTK Path: ")
    partvtk4path_input = QtGui.QLineEdit()
    partvtk4path_input.setText(data["partvtk4_path"])
    partvtk4path_input.setPlaceholderText("Put PartVTK4 path here")
    partvtk4path_browse = QtGui.QPushButton("...")

    partvtk4path_layout.addWidget(partvtk4path_label)
    partvtk4path_layout.addWidget(partvtk4path_input)
    partvtk4path_layout.addWidget(partvtk4path_browse)

    # ComputeForces path
    computeforces_layout = QtGui.QHBoxLayout()
    computeforces_label = QtGui.QLabel("ComputeForces Path: ")
    computeforces_input = QtGui.QLineEdit()
    try:
        computeforces_input.setText(data["computeforces_path"])
    except KeyError:
        computeforces_input.setText("")
    computeforces_input.setPlaceholderText("Put ComputeForces path here")
    computeforces_browse = QtGui.QPushButton("...")

    computeforces_layout.addWidget(computeforces_label)
    computeforces_layout.addWidget(computeforces_input)
    computeforces_layout.addWidget(computeforces_browse)

    # FloatingInfo path
    floatinginfo_layout = QtGui.QHBoxLayout()
    floatinginfo_label = QtGui.QLabel("FloatingInfo Path: ")
    floatinginfo_input = QtGui.QLineEdit()
    try:
        floatinginfo_input.setText(data["floatinginfo_path"])
    except KeyError:
        floatinginfo_input.setText("")
    floatinginfo_input.setPlaceholderText("Put FloatingInfo path here")
    floatinginfo_browse = QtGui.QPushButton("...")

    floatinginfo_layout.addWidget(floatinginfo_label)
    floatinginfo_layout.addWidget(floatinginfo_input)
    floatinginfo_layout.addWidget(floatinginfo_browse)

    # MeasureTool path
    measuretool_layout = QtGui.QHBoxLayout()
    measuretool_label = QtGui.QLabel("MeasureTool Path: ")
    measuretool_input = QtGui.QLineEdit()
    try:
        measuretool_input.setText(data["measuretool_path"])
    except KeyError:
        measuretool_input.setText("")
    measuretool_input.setPlaceholderText("Put MeasureTool path here")
    measuretool_browse = QtGui.QPushButton("...")

    measuretool_layout.addWidget(measuretool_label)
    measuretool_layout.addWidget(measuretool_input)
    measuretool_layout.addWidget(measuretool_browse)

    # IsoSurface path
    isosurface_layout = QtGui.QHBoxLayout()
    isosurface_label = QtGui.QLabel("IsoSurface Path: ")
    isosurface_input = QtGui.QLineEdit()
    try:
        isosurface_input.setText(data["isosurface_path"])
    except KeyError:
        isosurface_input.setText("")
    isosurface_input.setPlaceholderText("Put IsoSurface path here")
    isosurface_browse = QtGui.QPushButton("...")

    isosurface_layout.addWidget(isosurface_label)
    isosurface_layout.addWidget(isosurface_input)
    isosurface_layout.addWidget(isosurface_browse)

    # BoundaryVTK path
    boundaryvtk_layout = QtGui.QHBoxLayout()
    boundaryvtk_label = QtGui.QLabel("BoundaryVTK Path: ")
    boundaryvtk_input = QtGui.QLineEdit()
    try:
        boundaryvtk_input.setText(data["boundaryvtk_path"])
    except KeyError:
        boundaryvtk_input.setText("")
    boundaryvtk_input.setPlaceholderText("Put BoundaryVTK path here")
    boundaryvtk_browse = QtGui.QPushButton("...")

    boundaryvtk_layout.addWidget(boundaryvtk_label)
    boundaryvtk_layout.addWidget(boundaryvtk_input)
    boundaryvtk_layout.addWidget(boundaryvtk_browse)

    # FlowTool path
    flowtool_layout = QtGui.QHBoxLayout()
    flowtool_label = QtGui.QLabel("FlowTool Path: ")
    flowtool_input = QtGui.QLineEdit()
    try:
        flowtool_input.setText(data["flowtool_path"])
    except KeyError:
        flowtool_input.setText("")
    flowtool_input.setPlaceholderText("Put FlowTool path here")
    flowtool_browse = QtGui.QPushButton("...")

    flowtool_layout.addWidget(flowtool_label)
    flowtool_layout.addWidget(flowtool_input)
    flowtool_layout.addWidget(flowtool_browse)

    # ParaView path
    paraview_layout = QtGui.QHBoxLayout()
    paraview_label = QtGui.QLabel("ParaView Path: ")
    paraview_input = QtGui.QLineEdit()
    try:
        paraview_input.setText(data["paraview_path"])
    except KeyError:
        paraview_input.setText("")
    paraview_input.setPlaceholderText("Put ParaView path here")
    paraview_browse = QtGui.QPushButton("...")

    paraview_layout.addWidget(paraview_label)
    paraview_layout.addWidget(paraview_input)
    paraview_layout.addWidget(paraview_browse)

    # ------------ Button behaviour definition --------------
    def on_ok():
        data['gencase_path'] = gencasepath_input.text()
        data['dsphysics_path'] = dsphpath_input.text()
        data['partvtk4_path'] = partvtk4path_input.text()
        data['computeforces_path'] = computeforces_input.text()
        data['floatinginfo_path'] = floatinginfo_input.text()
        data['measuretool_path'] = measuretool_input.text()
        data['isosurface_path'] = isosurface_input.text()
        data['boundaryvtk_path'] = boundaryvtk_input.text()
        data['flowtool_path'] = flowtool_input.text()
        data['paraview_path'] = paraview_input.text()
        data_to_merge, state = utils.check_executables(data)
        data.update(data_to_merge)
        with open(FreeCAD.getUserAppDataDir() + '/dsph_data-{}.dsphdata'.format(utils.VERSION),
                  'wb') as picklefile:
            pickle.dump(data, picklefile, utils.PICKLE_PROTOCOL)
        utils.log("Setup changed. Saved to " + FreeCAD.getUserAppDataDir() +
                  '/dsph_data-{}.dsphdata'.format(utils.VERSION))
        setup_window.accept()

    def on_cancel():
        utils.log("Setup not changed")
        setup_window.reject()

    def on_gencase_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select GenCase path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed gencase
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "gencase" in output[0:15].lower():
                gencasepath_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize GenCase in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize GenCase in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_dualsphysics_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select DualSPHysics path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed dualsphysics
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            if platform == "linux" or platform == "linux2":
                os.environ["LD_LIBRARY_PATH"] = "{}/".format(
                    "/".join(file_name.split("/")[:-1]))
                process.start('"{}"'.format(file_name))
            else:
                process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())
            if "dualsphysics" in output[0:20].lower():
                dsphpath_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize DualSPHysics in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize DualSPHysics in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_partvtk4_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select PartVTK4 path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed dualsphysics
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "partvtk4" in output[0:20].lower():
                partvtk4path_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize PartVTK4 in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize PartVTK4 in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_computeforces_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select ComputeForces path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed computeforces
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "computeforces" in output[0:22].lower():
                computeforces_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize ComputeForces in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize ComputeForces in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_floatinginfo_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select FloatingInfo path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed floatinginfo
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "floatinginfo" in output[0:22].lower():
                floatinginfo_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize FloatingInfo in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize FloatingInfo in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_measuretool_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select MeasureTool path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "measuretool" in output[0:22].lower():
                measuretool_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize MeasureTool in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize MeasureTool in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_isosurface_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select IsoSurface path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "isosurface" in output[0:22].lower():
                isosurface_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize IsoSurface in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize IsoSurface in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_boundaryvtk_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select BoundaryVTK path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "boundaryvtk" in output[0:22].lower():
                boundaryvtk_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize BoundaryVTK in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize BoundaryVTK in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_flowtool_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select FlowTool path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            # Verify if exe is indeed measuretool
            process = QtCore.QProcess(FreeCADGui.getMainWindow())
            process.start('"{}"'.format(file_name))
            process.waitForFinished()
            output = str(process.readAllStandardOutput())

            if "flowtool" in output[0:22].lower():
                flowtool_input.setText(file_name)
            else:
                utils.error(
                    "I can't recognize FlowTool in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it"
                )
                warning_dialog(
                    "I can't recognize FlowTool in that executable.! "
                    "Check that the file corresponds with the appropriate tool and that you have permissions to execute it",
                    detailed_text="If you're working with GNU/Linux, you can give permissions to an executable from the terminal "
                                  "with: chmod +x /path/to/the/executable"
                )

    def on_paraview_browse():
        filedialog = QtGui.QFileDialog()
        # noinspection PyArgumentList
        file_name, _ = filedialog.getOpenFileName(setup_window,
                                                  "Select ParaView path",
                                                  QtCore.QDir.homePath())
        if file_name != "":
            paraview_input.setText(file_name)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    gencasepath_browse.clicked.connect(on_gencase_browse)
    dsphpath_browse.clicked.connect(on_dualsphysics_browse)
    partvtk4path_browse.clicked.connect(on_partvtk4_browse)
    computeforces_browse.clicked.connect(on_computeforces_browse)
    floatinginfo_browse.clicked.connect(on_floatinginfo_browse)
    measuretool_browse.clicked.connect(on_measuretool_browse)
    boundaryvtk_browse.clicked.connect(on_boundaryvtk_browse)
    flowtool_browse.clicked.connect(on_flowtool_browse)
    isosurface_browse.clicked.connect(on_isosurface_browse)
    paraview_browse.clicked.connect(on_paraview_browse)

    # Button layout definition
    stp_button_layout = QtGui.QHBoxLayout()
    stp_button_layout.addStretch(1)
    stp_button_layout.addWidget(ok_button)
    stp_button_layout.addWidget(cancel_button)

    # START Main layout definition and composition.
    stp_main_layout = QtGui.QVBoxLayout()
    stp_main_layout.addLayout(gencasepath_layout)
    stp_main_layout.addLayout(dsphpath_layout)
    stp_main_layout.addLayout(partvtk4path_layout)
    stp_main_layout.addLayout(computeforces_layout)
    stp_main_layout.addLayout(floatinginfo_layout)
    stp_main_layout.addLayout(measuretool_layout)
    stp_main_layout.addLayout(isosurface_layout)
    stp_main_layout.addLayout(boundaryvtk_layout)
    stp_main_layout.addLayout(flowtool_layout)
    stp_main_layout.addLayout(paraview_layout)
    stp_main_layout.addStretch(1)

    stp_groupbox = QtGui.QGroupBox("Setup parameters")
    stp_groupbox.setLayout(stp_main_layout)
    setup_window_layout = QtGui.QVBoxLayout()
    setup_window_layout.addWidget(stp_groupbox)
    setup_window_layout.addLayout(stp_button_layout)
    setup_window.setLayout(setup_window_layout)
    # END Main layout definition and composition.

    setup_window.resize(600, 400)
    setup_window.exec_()


def damping_config_window(data, object_key):
    """Defines the setup window.
    Modifies data dictionary passed as parameter."""

    # TODO: This should be implemented as a custom class like DampingConfigDialog(QtGui.QDialog)

    # Creates a dialog and 2 main buttons
    damping_window = QtGui.QDialog()
    damping_window.setWindowTitle("Damping configuration")
    ok_button = QtGui.QPushButton("Save")
    cancel_button = QtGui.QPushButton("Cancel")

    main_layout = QtGui.QVBoxLayout()

    enabled_checkbox = QtGui.QCheckBox("Enabled")

    main_groupbox = QtGui.QGroupBox("Damping parameters")
    main_groupbox_layout = QtGui.QVBoxLayout()

    limitmin_layout = QtGui.QHBoxLayout()
    limitmin_label = QtGui.QLabel("Limit Min. (X, Y, Z) (m): ")
    limitmin_input_x = QtGui.QLineEdit()
    limitmin_input_y = QtGui.QLineEdit()
    limitmin_input_z = QtGui.QLineEdit()
    [limitmin_layout.addWidget(x) for x in [limitmin_label, limitmin_input_x, limitmin_input_y, limitmin_input_z]]

    limitmax_layout = QtGui.QHBoxLayout()
    limitmax_label = QtGui.QLabel("Limit Max. (X, Y, Z) (m): ")
    limitmax_input_x = QtGui.QLineEdit()
    limitmax_input_y = QtGui.QLineEdit()
    limitmax_input_z = QtGui.QLineEdit()
    [limitmax_layout.addWidget(x) for x in [limitmax_label, limitmax_input_x, limitmax_input_y, limitmax_input_z]]

    overlimit_layout = QtGui.QHBoxLayout()
    overlimit_label = QtGui.QLabel("Overlimit (m): ")
    overlimit_input = QtGui.QLineEdit()
    [overlimit_layout.addWidget(x) for x in [overlimit_label, overlimit_input]]

    redumax_layout = QtGui.QHBoxLayout()
    redumax_label = QtGui.QLabel("Redumax: ")
    redumax_input = QtGui.QLineEdit()
    [redumax_layout.addWidget(x) for x in [redumax_label, redumax_input]]

    main_groupbox_layout.addLayout(limitmin_layout)
    main_groupbox_layout.addLayout(limitmax_layout)
    main_groupbox_layout.addLayout(overlimit_layout)
    main_groupbox_layout.addLayout(redumax_layout)

    main_groupbox.setLayout(main_groupbox_layout)

    button_layout = QtGui.QHBoxLayout()
    button_layout.addStretch(1)
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)

    main_layout.addWidget(enabled_checkbox)
    main_layout.addWidget(main_groupbox)
    main_layout.addLayout(button_layout)

    damping_window.setLayout(main_layout)

    # Window logic
    def on_ok():
        data["damping"][object_key].enabled = enabled_checkbox.isChecked()
        data["damping"][object_key].overlimit = float(overlimit_input.text())
        data["damping"][object_key].redumax = float(redumax_input.text())
        damping_group = FreeCAD.ActiveDocument.getObject(object_key)
        damping_group.OutList[0].Start = (float(limitmin_input_x.text()) * 1000,
                                          float(limitmin_input_y.text()) * 1000,
                                          float(limitmin_input_z.text()) * 1000)
        damping_group.OutList[0].End = (float(limitmax_input_x.text()) * 1000,
                                        float(limitmax_input_y.text()) * 1000,
                                        float(limitmax_input_z.text()) * 1000)
        damping_group.OutList[1].Start = damping_group.OutList[0].End

        overlimit_vector = FreeCAD.Vector(*damping_group.OutList[0].End) - FreeCAD.Vector(*damping_group.OutList[0].Start)
        overlimit_vector.normalize()
        overlimit_vector = overlimit_vector * data["damping"][object_key].overlimit * 1000
        overlimit_vector = overlimit_vector + FreeCAD.Vector(*damping_group.OutList[0].End)

        damping_group.OutList[1].End = (overlimit_vector.x, overlimit_vector.y, overlimit_vector.z)
        FreeCAD.ActiveDocument.recompute()
        damping_window.accept()

    def on_cancel():
        damping_window.reject()

    def on_enable_chk(state):
        if state == QtCore.Qt.Checked:
            main_groupbox.setEnabled(True)
        else:
            main_groupbox.setEnabled(False)

    def on_value_change():
        [x.setText(x.text().replace(",", ".")) for x in
         [overlimit_input, redumax_input, limitmin_input_x, limitmin_input_y, limitmin_input_z, limitmax_input_x,
          limitmax_input_y, limitmax_input_z]]

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)
    enabled_checkbox.stateChanged.connect(on_enable_chk)
    [x.textChanged.connect(on_value_change) for x in [overlimit_input, redumax_input]]

    # Fill fields with case data
    enabled_checkbox.setChecked(data["damping"][object_key].enabled)
    group = FreeCAD.ActiveDocument.getObject(object_key)
    limitmin_input_x.setText(str(group.OutList[0].Start[0] / 1000))
    limitmin_input_y.setText(str(group.OutList[0].Start[1] / 1000))
    limitmin_input_z.setText(str(group.OutList[0].Start[2] / 1000))
    limitmax_input_x.setText(str(group.OutList[0].End[0] / 1000))
    limitmax_input_y.setText(str(group.OutList[0].End[1] / 1000))
    limitmax_input_z.setText(str(group.OutList[0].End[2] / 1000))
    overlimit_input.setText(str(group.OutList[1].Length.Value / 1000))
    redumax_input.setText(str(data["damping"][object_key].redumax))
    redumax_input.setText(str(data["damping"][object_key].redumax))
    on_enable_chk(
        QtCore.Qt.Checked if data["damping"][object_key].enabled else QtCore.Qt.Unchecked)

    damping_window.exec_()


def widget_state_config(widgets, config):
    """ Takes an widget dictionary and a config string to
        enable and disable certain widgets base on a case. """
    if config == "no case":
        widgets["casecontrols_bt_savedoc"].setEnabled(False)
        widgets["rungencase_bt"].setEnabled(False)
        widgets["constants_button"].setEnabled(False)
        widgets["execparams_button"].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(False)
        widgets["casecontrols_bt_addstl"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
        widgets["objectlist_table"].setEnabled(False)
        widgets["dp_input"].setEnabled(False)
        widgets["summary_bt"].setEnabled(False)
        widgets["toggle3dbutton"].setEnabled(False)
        widgets["dampingbutton"].setEnabled(False)
    elif config == "new case":
        widgets["constants_button"].setEnabled(True)
        widgets["execparams_button"].setEnabled(True)
        widgets["casecontrols_bt_savedoc"].setEnabled(True)
        widgets["rungencase_bt"].setEnabled(True)
        widgets["dp_input"].setEnabled(True)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addstl"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["dampingbutton"].setEnabled(True)
    elif config == "gencase done":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
    elif config == "gencase not done":
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
    elif config == "load base":
        widgets["constants_button"].setEnabled(True)
        widgets["execparams_button"].setEnabled(True)
        widgets["casecontrols_bt_savedoc"].setEnabled(True)
        widgets["rungencase_bt"].setEnabled(True)
        widgets["dp_input"].setEnabled(True)
        widgets["casecontrols_bt_addfillbox"].setEnabled(True)
        widgets["casecontrols_bt_addstl"].setEnabled(True)
        widgets["summary_bt"].setEnabled(True)
        widgets["toggle3dbutton"].setEnabled(True)
        widgets["dampingbutton"].setEnabled(True)
    elif config == "simulation done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "simulation not done":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "execs not correct":
        widgets["ex_selector_combo"].setEnabled(False)
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
    elif config == "sim start":
        widgets["ex_button"].setEnabled(False)
        widgets["ex_additional"].setEnabled(False)
        widgets["ex_selector_combo"].setEnabled(False)
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim cancel":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
        # Post-proccessing is enabled on cancel, to evaluate only currently exported parts
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "sim error":
        widgets["ex_selector_combo"].setEnabled(True)
        widgets["ex_button"].setEnabled(True)
        widgets["ex_additional"].setEnabled(True)
    elif config == "export start":
        widgets['post_proc_partvtk_button'].setEnabled(False)
        widgets['post_proc_computeforces_button'].setEnabled(False)
        widgets['post_proc_floatinginfo_button'].setEnabled(False)
        widgets['post_proc_measuretool_button'].setEnabled(False)
        widgets['post_proc_isosurface_button'].setEnabled(False)
        widgets['post_proc_boundaryvtk_button'].setEnabled(False)
        widgets['post_proc_flowtool_button'].setEnabled(False)
    elif config == "export cancel":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)
    elif config == "export finished":
        widgets['post_proc_partvtk_button'].setEnabled(True)
        widgets['post_proc_computeforces_button'].setEnabled(True)
        widgets['post_proc_floatinginfo_button'].setEnabled(True)
        widgets['post_proc_measuretool_button'].setEnabled(True)
        widgets['post_proc_isosurface_button'].setEnabled(True)
        widgets['post_proc_boundaryvtk_button'].setEnabled(True)
        widgets['post_proc_flowtool_button'].setEnabled(True)


def case_summary(orig_data):
    """ Displays a dialog with a summary of the current opened case. """

    # TODO: This should be implemented as a custom class like CaseSummary(QtGui.QDialog)

    if not utils.valid_document_environment():
        return

    # Data copy to avoid referencing issues
    data = dict(orig_data)

    # Preprocess data to show in data copy
    data['gravity'] = "({}, {}, {})".format(*data['gravity'])
    if data['project_name'] == "":
        data['project_name'] = "<i>{}</i>".format(utils.__("Not yet saved"))

    if data['project_path'] == "":
        data['project_path'] = "<i>{}</i>".format(utils.__("Not yet saved"))

    for k in ['gencase_path', 'dsphysics_path', 'partvtk4_path']:
        if data[k] == "":
            data[k] = "<i>{}</i>".format(
                utils.__("Executable not correctly set"))

    data['stepalgorithm'] = {
        '1': 'Verlet',
        '2': 'Symplectic'
    }[str(data['stepalgorithm'])]
    data['project_mode'] = '3D' if data['3dmode'] else '2D'

    data['incz'] = float(data['incz']) * 100
    data['partsoutmax'] = float(data['partsoutmax']) * 100

    # Setting certain values to automatic
    for x in [
        'hswl', 'speedsystem', 'speedsound', 'h', 'b', 'massfluid',
        'massbound'
    ]:
        data[x] = '<u>Automatic</u>' if data[x + '_auto'] else data[x]

    # region Formatting objects info
    data['objects_info'] = ""
    if len(data['simobjects']) > 1:
        data['objects_info'] += "<ul>"
        # data['simobjects'] is a dict with format
        # {'key': ['mk', 'type', 'fill']} where key is an internal name.
        for key, value in data['simobjects'].iteritems():
            if key.lower() == 'case_limits':
                continue
            fc_object = utils.get_fc_object(key)
            is_floating = utils.__('Yes') if str(
                value[0]) in data['floating_mks'].keys() else utils.__('No')
            is_floating = utils.__('No') if value[
                                                1].lower() == "fluid" else is_floating
            has_initials = utils.__('Yes') if str(
                value[0]) in data['initials_mks'].keys() else utils.__('No')
            has_initials = utils.__('No') if value[
                                                 1].lower() == "bound" else has_initials
            real_mk = value[0] + 11 if value[
                                           1].lower() == "bound" else value[0] + 1
            data['objects_info'] += "<li><b>{label}</b> (<i>{iname}</i>): <br/>" \
                                    "Type: {type} (MK{type}: <b>{mk}</b> ; MK: <b>{real_mk}</b>)<br/>" \
                                    "Fill mode: {fillmode}<br/>" \
                                    "Floating: {floats}<br/>" \
                                    "Initials: {initials}</li><br/>".format(label=fc_object.Label, iname=key,
                                                                            type=value[1].title(), mk=value[0],
                                                                            real_mk=str(
                                                                                real_mk),
                                                                            fillmode=value[2].title(
                                                                            ),
                                                                            floats=is_floating,
                                                                            initials=has_initials)
        data['objects_info'] += "</ul>"
    else:
        data['objects_info'] += utils.__(
            "No objects were added to the simulation yet.")
    # endregion Formatting objects info

    # region Formatting movement info
    data['movement_info'] = ""
    if len(data['simobjects']) > 1:
        data['movement_info'] += "<ul>"
        for mov in data['global_movements']:
            try:
                movtype = mov.type
            except AttributeError:
                movtype = mov.__class__.__name__

            mklist = list()
            for key, value in data['motion_mks'].iteritems():
                if mov in value:
                    mklist.append(str(key))

            data['movement_info'] += "<li>{movtype} <u>{movname}</u><br/>" \
                                     "Applied to MKBound: {mklist}</li><br/>".format(
                movtype=movtype, movname=mov.name, mklist=', '.join(mklist))

        data['movement_info'] += "</ul>"
    else:
        data['movement_info'] += "No movements were defined in this case."

    # Create a string with MK used (of each type)
    data['mkboundused'] = list()
    data['mkfluidused'] = list()
    for element in data['simobjects'].values():
        if element[1].lower() == 'bound':
            data['mkboundused'].append(str(element[0]))
        elif element[1].lower() == 'fluid':
            data['mkfluidused'].append(str(element[0]))

    data['mkboundused'] = ", ".join(
        data['mkboundused']) if len(data['mkboundused']) > 0 else "None"
    data['mkfluidused'] = ", ".join(
        data['mkfluidused']) if len(data['mkfluidused']) > 0 else "None"

    data['last_number_particles'] = data['last_number_particles'] if data['last_number_particles'] >= 0 else "GenCase wasn't executed"

    # endregion Formatting movement info

    # Dialog creation and template filling
    main_window = QtGui.QDialog()
    main_layout = QtGui.QVBoxLayout()
    info = QtGui.QTextEdit()

    lib_folder = os.path.dirname(os.path.realpath(__file__))

    try:
        with open("{}/templates/case_summary_template.html".format(lib_folder),
                  "r") as input_template:
            info_text = input_template.read().format(**data)
    except:
        error_dialog(
            "An error occurred trying to load the template file and format it.")
        return

    info.setText(info_text)
    info.setReadOnly(True)

    main_layout.addWidget(info)
    main_window.setLayout(main_layout)
    main_window.setModal(True)
    main_window.setMinimumSize(500, 650)
    main_window.exec_()


def get_fc_view_object(internal_name):
    """ Returns a FreeCADGui View provider object by a name. """
    return FreeCADGui.getDocument("DSPH_Case").getObject(internal_name)


def gencase_completed_dialog(particle_count=0, detail_text="No details", data=dict(), temp_data=dict()):
    """ Creates a gencase save dialog with different options, like
    open the results with paraview, show details or dismiss. """

    # TODO: This should be implemented as a custom class like GenCaseCompleteDialog(QtGui.QDialog)

    # Window Creation
    window = QtGui.QDialog()
    window.setWindowModality(QtCore.Qt.NonModal)
    window.setWindowTitle(utils.__("Save & GenCase"))

    # Main Layout creation
    main_layout = QtGui.QVBoxLayout()

    # Main Layout elements
    info_message = QtGui.QLabel(
        utils.__("Gencase exported {} particles.\nPress \"Details\" to check the output").format(
            str(particle_count)))

    button_layout = QtGui.QHBoxLayout()
    bt_open_with_paraview = QtGui.QPushButton(utils.__("Open with Paraview"))
    temp_data['widget_saver'] = QtGui.QMenu()
    temp_data['widget_saver'].addAction("{}_MkCells.vtk".format(data['project_name']))
    temp_data['widget_saver'].addAction("{}_All.vtk".format(data['project_name']))
    temp_data['widget_saver'].addAction("{}_Fluid.vtk".format(data['project_name']))
    temp_data['widget_saver'].addAction("{}_Bound.vtk".format(data['project_name']))
    bt_open_with_paraview.setMenu(temp_data['widget_saver'])
    bt_details = QtGui.QPushButton(utils.__("Details"))
    bt_ok = QtGui.QPushButton(utils.__("Ok"))
    button_layout.addWidget(bt_open_with_paraview)
    button_layout.addWidget(bt_details)
    button_layout.addWidget(bt_ok)

    # Details popup window
    detail_text_dialog = QtGui.QDialog()
    detail_text_dialog.setModal(False)
    detail_text_dialog_layout = QtGui.QVBoxLayout()

    detail_text_area = QtGui.QTextEdit()
    detail_text_area.setText(detail_text)

    detail_text_dialog_layout.addWidget(detail_text_area)
    detail_text_dialog.setLayout(detail_text_dialog_layout)

    # Main Layout scaffolding
    main_layout.addWidget(info_message)
    main_layout.addLayout(button_layout)

    # Window logic
    detail_text_dialog.hide()

    if len(data["paraview_path"]) > 1:
        bt_open_with_paraview.show()
    else:
        bt_open_with_paraview.hide()

    def on_ok():
        detail_text_dialog.hide()
        window.accept()

    def on_view_details():
        if detail_text_dialog.isVisible():
            detail_text_dialog.hide()
        else:
            detail_text_dialog.show()
            detail_text_dialog.move(
                window.x() - detail_text_dialog.width() - 15,
                window.y() - abs(window.height() - detail_text_dialog.height()) / 2)

    def on_open_paraview_menu(action):
        try:
            subprocess.Popen(
                [
                    data['paraview_path'],
                    "--data={}\\{}".format(
                        data['project_path'] + '\\' +
                        data['project_name'] + '_out',
                        action.text()
                    )
                ],
                stdout=subprocess.PIPE)
            detail_text_dialog.hide()
            window.accept()
        except:
            error_dialog(
                "ERROR! \nCheck the ParaView executable path, it may have been saved from previously opened case!")
            return

    bt_ok.clicked.connect(on_ok)
    bt_details.clicked.connect(on_view_details)
    temp_data['widget_saver'].triggered.connect(on_open_paraview_menu)

    # Window scaffolding and execution
    window.setLayout(main_layout)
    window.show()
