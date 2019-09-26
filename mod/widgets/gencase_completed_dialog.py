#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' DesignSPHysics GenCase Completed Dialog. '''

import subprocess

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.guiutils import error_dialog

from mod.dataobjects.case import Case


class GencaseCompletedDialog(QtGui.QDialog):
    ''' Gencase Save Dialog with different options, like open the results
        with paraview, show details, or dismiss. '''

    DETAILS_MIN_WIDTH: int = 650
    DIALOG_IS_MODAL: bool = False

    def __init__(self, particle_count=0, detail_text="No details"):
        super().__init__()

        # Window Creation
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setWindowTitle(__("Save & GenCase"))

        # Main Layout creation
        self.main_layout = QtGui.QVBoxLayout()

        # Main Layout elements
        self.info_message = QtGui.QLabel(__("Gencase exported {} particles.\nPress \"Details\" to check the output").format(str(particle_count)))

        self.button_layout = QtGui.QHBoxLayout()

        self.bt_open_with_paraview = QtGui.QPushButton(__("Open with Paraview"))

        self.open_menu = QtGui.QMenu()
        self.open_menu.addAction("{}_MkCells.vtk".format(Case.instance.name))
        self.open_menu.addAction("{}_All.vtk".format(Case.instance.name))
        self.open_menu.addAction("{}_Fluid.vtk".format(Case.instance.name))
        self.open_menu.addAction("{}_Bound.vtk".format(Case.instance.name))

        self.bt_open_with_paraview.setMenu(self.open_menu)

        self.bt_details = QtGui.QPushButton(__("Details"))
        self.bt_ok = QtGui.QPushButton(__("Ok"))

        self.button_layout.addWidget(self.bt_open_with_paraview)
        self.button_layout.addWidget(self.bt_details)
        self.button_layout.addWidget(self.bt_ok)

        # Details popup window
        self.detail_text_dialog = QtGui.QDialog()
        self.detail_text_dialog.setMinimumWidth(self.DETAILS_MIN_WIDTH)
        self.detail_text_dialog.setModal(self.DIALOG_IS_MODAL)
        self.detail_text_dialog_layout = QtGui.QVBoxLayout()

        self.detail_text_area = QtGui.QTextEdit()
        self.detail_text_area.setText(detail_text)

        self.detail_text_dialog_layout.addWidget(self.sdetail_text_area)
        self.detail_text_dialog.setLayout(self.detail_text_dialog_layout)

        # Main Layout scaffolding
        self.main_layout.addWidget(self.info_message)
        self.main_layout.addLayout(self.button_layout)

        # Window logic
        self.detail_text_dialog.hide()

        if Case.instance().executable_paths.paraview:
            self.bt_open_with_paraview.show()
        else:
            self.bt_open_with_paraview.hide()

        self.bt_ok.clicked.connect(self.on_ok)
        self.bt_details.clicked.connect(self.on_view_details)
        self.open_menu.triggered.connect(self.on_open_paraview_menu)

        # Window scaffolding and execution
        self.setLayout(self.main_layout)

    def on_ok(self):
        ''' Hides the detail panel and closes the window. '''
        self.detail_text_dialog.hide()
        self.accept()

    def on_view_details(self):
        ''' Toggles the visibility of the detail pane. '''
        if self.detail_text_dialog.isVisible():
            self.detail_text_dialog.hide()
        else:
            self.detail_text_dialog.show()
            self.detail_text_dialog.move(self.x() - self.detail_text_dialog.width() - 15, self.y() - abs(self.height() - self.detail_text_dialog.height()) / 2)

    def on_open_paraview_menu(self, action):
        ''' Tries to open Paraview with the selected option. '''
        try:
            subprocess.Popen([Case.instance().executable_paths.paraview, "--data={}\\{}".format(Case.instance().path + '\\' + Case.instance().name + '_out', action.text())], stdout=subprocess.PIPE)
            self.detail_text_dialog.hide()
            self.accept()
        except:
            error_dialog("There was an error executing paraview. Make sure the path for the paraview executable is set in the DesignSPHyisics configuration and that the executable is a correct paraview one.")
