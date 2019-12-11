#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Movement Actions Widget. """

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon


class MovementActions(QtGui.QWidget):
    """ A set of movement actions (use and delete) with its custom signals"""
    delete = QtCore.Signal(int)
    use = QtCore.Signal(int, bool)
    loop = QtCore.Signal(int, bool)

    def __init__(self, index, use_checked, loop_checked, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.use_checkbox = QtGui.QCheckBox(__("Use"))
        self.use_checkbox.setChecked(use_checked)
        self.use_checkbox.stateChanged.connect(self.on_use)
        self.loop_checkbox = QtGui.QCheckBox(__("Loop"))
        self.loop_checkbox.setChecked(loop_checked)
        self.loop_checkbox.stateChanged.connect(self.on_loop)
        self.delete_button = QtGui.QPushButton(get_icon("trash.png"), None)
        self.delete_button.clicked.connect(self.on_delete)

        main_layout = QtGui.QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.addWidget(self.use_checkbox)
        main_layout.addWidget(self.loop_checkbox)
        main_layout.addWidget(self.delete_button)
        self.setLayout(main_layout)

    def on_delete(self):
        """ Emits a delete signal once the delete button is pressed. """
        self.delete.emit(self.index)

    def on_use(self):
        """ Emits a use signal with the checkbox state attached once the use checkbox is clicked. """
        self.use.emit(self.index, self.use_checkbox.isChecked())

    def on_loop(self):
        """ Emits a loop signal with the checkbox state attached once the checkbox is clicked. """
        self.loop.emit(self.index, self.loop_checkbox.isChecked())
