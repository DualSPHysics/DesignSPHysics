#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics GenCase Completed Dialog. """

import subprocess

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.dialog_tools import error_dialog
from mod.gui_tools import h_line_generator

from mod.dataobjects.case import Case


class GencaseCompletedDialog(QtGui.QDialog):
    """ Gencase Save Dialog with different options, like open the results
        with paraview, show details, or dismiss. """

    DETAILS_MIN_WIDTH: int = 600
    DIALOG_IS_MODAL: bool = False

    def __init__(self, particle_count=0, detail_text="No details", cmd_string="", parent=None):
        super().__init__(parent=parent)

        # Window Creation
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setWindowTitle(__("Save & GenCase"))
        self.setMinimumSize(400, 100)

        # Main Layout creation
        self.main_layout = QtGui.QVBoxLayout()

        # Main Layout elements
        self.info_message = QtGui.QLabel(__(
            "Gencase exported <b>{}</b> particles.<br/>"
            "Press the <i>Details</i> button to check the output."
        ).format(str(particle_count)))

        self.button_layout = QtGui.QHBoxLayout()

        self.bt_open_with_paraview = QtGui.QPushButton(__("Open with Paraview"))

        self.open_menu = QtGui.QMenu()
        self.open_menu.addAction("{}_MkCells.vtk".format(Case.the().name))
        self.open_menu.addAction("{}_All.vtk".format(Case.the().name))
        self.open_menu.addAction("{}_Fluid.vtk".format(Case.the().name))
        self.open_menu.addAction("{}_Bound.vtk".format(Case.the().name))

        self.bt_open_with_paraview.setMenu(self.open_menu)

        self.bt_details = QtGui.QPushButton(__("Details"))
        self.bt_ok = QtGui.QPushButton(__("OK"))

        self.button_layout.addWidget(self.bt_open_with_paraview)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.bt_details)
        self.button_layout.addWidget(self.bt_ok)

        # Details widget
        self.detail_text_widget = QtGui.QWidget()
        self.detail_text_widget.setContentsMargins(0, 0, 0, 0)
        self.detail_text_widget_layout = QtGui.QVBoxLayout()
        self.detail_text_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.detail_text_area = QtGui.QTextEdit()
        self.detail_text_area.setText("<b>{}:</b> <tt>{}</tt><br><pre>{}</pre>".format(__("The executed command line was"), cmd_string, detail_text))

        self.detail_text_widget_layout.addWidget(h_line_generator())
        self.detail_text_widget_layout.addWidget(self.detail_text_area)
        self.detail_text_widget.setLayout(self.detail_text_widget_layout)

        # Main Layout scaffolding
        self.main_layout.addWidget(self.info_message)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.detail_text_widget)

        # Window logic
        self.detail_text_widget.hide()

        if Case.the().executable_paths.paraview:
            self.bt_open_with_paraview.show()
        else:
            self.bt_open_with_paraview.hide()

        self.bt_ok.clicked.connect(self.on_ok)
        self.bt_details.clicked.connect(self.on_view_details)
        self.open_menu.triggered.connect(self.on_open_paraview_menu)

        # Window scaffolding and execution
        self.setLayout(self.main_layout)
        self.setMinimumWidth(self.DETAILS_MIN_WIDTH)

    def on_ok(self):
        """ Hides the detail panel and closes the window. """
        self.accept()

    def on_view_details(self):
        """ Toggles the visibility of the detail pane. """
        self.detail_text_widget.setVisible(not self.detail_text_widget.isVisible())
        self.adjustSize()

    def on_open_paraview_menu(self, action):
        """ Tries to open Paraview with the selected option. """
        try:
            subprocess.Popen([Case.the().executable_paths.paraview, "--data={}\\{}".format(Case.the().path + "\\" + Case.the().name + "_out", action.text())], stdout=subprocess.PIPE)
            self.accept()
        except FileNotFoundError:
            error_dialog("There was an error executing paraview. Make sure the path for the paraview executable is set in the DesignSPHyisics configuration and that the executable is a correct paraview one.")
