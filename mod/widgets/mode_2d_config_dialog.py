#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" 2D Mode Configuration Dialog. """

# from PySide import QtGui
from PySide6 import QtWidgets

from mod.translation_tools import __
from mod.dialog_tools import error_dialog


class Mode2DConfigDialog(QtWidgets.QDialog):
    """ A dialog to configure features of going into 2D mode. """

    def __init__(self, case_limits_y_value: float, parent=None):
        super().__init__(parent=parent)

        self.stored_y_value = 0.0

        self.setWindowTitle(__("Set Y position"))

        self.ok_button = QtWidgets.QPushButton(__("OK"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

        self.y2d_button_layout = QtWidgets.QHBoxLayout()
        self.y2d_button_layout.addStretch(1)
        self.y2d_button_layout.addWidget(self.ok_button)
        self.y2d_button_layout.addWidget(self.cancel_button)

        self.y_pos_intro_layout = QtWidgets.QHBoxLayout()
        self.y_pos_intro_label = QtWidgets.QLabel(__("New Y position (mm): "))
        self.y2_pos_input = QtWidgets.QLineEdit()
        self.y2_pos_input.setText(str(case_limits_y_value))
        self.y_pos_intro_layout.addWidget(self.y_pos_intro_label)
        self.y_pos_intro_layout.addWidget(self.y2_pos_input)

        self.y_pos_2d_layout = QtWidgets.QVBoxLayout()
        self.y_pos_2d_layout.addLayout(self.y_pos_intro_layout)
        self.y_pos_2d_layout.addStretch(1)
        self.y_pos_2d_layout.addLayout(self.y2d_button_layout)

        self.setLayout(self.y_pos_2d_layout)
        self.exit_status: QtWidgets.QDialog.DialogCode = self.exec_()

    def on_ok(self):
        """ Tries to convert the current case to 2D mode while saving the 3D mode data. """
        try:
            self.stored_y_value = float(self.y2_pos_input.text())
        except ValueError:
            error_dialog(__("The Y position that was inserted is not valid."))
        self.accept()

    def on_cancel(self):
        """ Cancels the dialog not saving anything. """
        self.reject()
