#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Information Dialog widget. '''

from PySide import QtCore, QtGui

from mod.gui_tools import h_line_generator

from mod.widgets.info_dialog_details import InfoDialogDetails


class InfoDialog(QtGui.QDialog):
    ''' An information dialog with popup details and ok button.'''

    def __init__(self, info_text="", detailed_text=None):
        super(InfoDialog, self).__init__()
        self.setWindowModality(QtCore.Qt.NonModal)
        self.has_details = detailed_text is not None
        if self.has_details:
            self.details_dialog = InfoDialogDetails(detailed_text)
        self.main_layout = QtGui.QVBoxLayout()

        self.text = QtGui.QLabel(str(info_text))
        self.text.setWordWrap(True)

        if self.has_details:
            self.details_button = QtGui.QPushButton("Details")
        self.ok_button = QtGui.QPushButton("Ok")

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch(1)
        if self.has_details:
            self.button_layout.addWidget(self.details_button)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.text)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

        self.connections()
        self.show()

    def on_details_button(self):
        if self.details_dialog.isVisible():
            self.details_dialog.hide()
        else:
            self.details_dialog.show()
            self.details_dialog.move(
                self.x() - self.details_dialog.width() - 15,
                self.y() - abs(self.height() - self.details_dialog.height()) / 2)

    def on_ok_button(self):
        if self.has_details:
            self.details_dialog.hide()
        self.accept()

    def connections(self):
        if self.has_details:
            self.details_button.clicked.connect(self.on_details_button)
        self.ok_button.clicked.connect(self.on_ok_button)
