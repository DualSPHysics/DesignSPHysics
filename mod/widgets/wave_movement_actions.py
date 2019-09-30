#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Wave Movement Actions Widget. '''

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon


class WaveMovementActions(QtGui.QWidget):
    ''' A set of wave movement actions (use and delete) with its custom signals'''
    delete = QtCore.Signal(int)
    use = QtCore.Signal(int, bool)

    def __init__(self, index, use_checked):
        super(WaveMovementActions, self).__init__()
        self.index = index
        self.use_checkbox = QtGui.QCheckBox(__("Use"))
        self.use_checkbox.setChecked(use_checked)
        self.use_checkbox.stateChanged.connect(self.on_use)
        self.delete_button = QtGui.QPushButton(get_icon("trash.png"), None)
        self.delete_button.clicked.connect(self.on_delete)
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QtGui.QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.addWidget(self.use_checkbox)
        main_layout.addWidget(self.delete_button)
        self.setLayout(main_layout)

    def on_delete(self):
        self.delete.emit(self.index)

    def on_use(self):
        self.use.emit(self.index, self.use_checkbox.isChecked())
