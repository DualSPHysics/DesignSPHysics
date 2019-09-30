#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
''' 2D Mode Configuration Dialog. '''

from PySide import QtGui

from mod.translation_tools import __
from mod.freecad_tools import get_fc_object, get_fc_view_object
from mod.dialog_tools import error_dialog
from mod.constants import WIDTH_2D
from mod.enums import FreeCADDisplayMode

from mod.dataobjects.case import Case


class Mode2DConfigDialog(QtGui.QDialog):
    ''' A dialog to configure features of going into 2D mode. '''

    def __init__(self):
        super().__init__()

        self.setWindowTitle(__("Set Y position"))

        self.ok_button = QtGui.QPushButton(__("Ok"))
        self.cancel_button = QtGui.QPushButton(__("Cancel"))

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.y2d_button_layout = QtGui.QHBoxLayout()
        self.y2d_button_layout.addStretch(1)
        self.y2d_button_layout.addWidget(self.ok_button)
        self.y2d_button_layout.addWidget(self.cancel_button)

        self.y_pos_intro_layout = QtGui.QHBoxLayout()
        self.y_pos_intro_label = QtGui.QLabel(__("New Y position (mm): "))
        self.y2_pos_input = QtGui.QLineEdit()
        self.y2_pos_input.setText(str(get_fc_object('Case_Limits').Placement.Base.y))
        self.y_pos_intro_layout.addWidget(self.y_pos_intro_label)
        self.y_pos_intro_layout.addWidget(self.y2_pos_input)

        self.y_pos_2d_layout = QtGui.QVBoxLayout()
        self.y_pos_2d_layout.addLayout(self.y_pos_intro_layout)
        self.y_pos_2d_layout.addStretch(1)
        self.y_pos_2d_layout.addLayout(self.y2d_button_layout)

        self.setLayout(self.y_pos_2d_layout)
        self.exec_()

    def on_ok(self):
        ''' Tries to convert the current case to 2D mode while saving the 3D mode data. '''
        Case.instance().info.last_3d_width = get_fc_object('Case_Limits').Width.Value

        try:
            get_fc_object('Case_Limits').Placement.Base.y = float(self.y2_pos_input.text())
        except ValueError:
            error_dialog(__("The Y position that was inserted is not valid."))

        get_fc_object('Case_Limits').Width.Value = WIDTH_2D
        get_fc_view_object('Case_Limits').DisplayMode = FreeCADDisplayMode.FLATLINES
        get_fc_view_object('Case_Limits').ShapeColor = (1.00, 0.00, 0.00)
        get_fc_view_object('Case_Limits').Transparency = 90

        self.accept()

    def on_cancel(self):
        ''' Cancels the dialog not saving anything. '''
        self.reject()
