#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Information Dialog Details widget.'''

from PySide import QtGui

from mod.translation_tools import __

class InfoDialogDetails(QtGui.QDialog):
    ''' A popup dialog with a text box to show details.'''

    def __init__(self, text=None):
        super(InfoDialogDetails, self).__init__()
        self.setMinimumWidth(650)
        self.setModal(False)
        self.setWindowTitle(__("Details"))
        self.main_layout = QtGui.QVBoxLayout()

        self.details_text = QtGui.QTextEdit()
        self.details_text.setReadOnly(True)
        self.main_layout.addWidget(self.details_text)

        self.details_text.setText(text)

        self.setLayout(self.main_layout)
