#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Movement Timeline Placeholder Widget """

from PySide import QtGui

from mod.translation_tools import __


class MovementTimelinePlaceholder(QtGui.QWidget):
    """ A placeholder for the movement timeline table. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.placeholder_layout = QtGui.QHBoxLayout()
        self.placeholder_text = QtGui.QLabel("<i>{}</i>".format(__("Select or create a movement to edit its properties")))

        self.placeholder_layout.addStretch(0.5)
        self.placeholder_layout.addWidget(self.placeholder_text)
        self.placeholder_layout.addStretch(0.5)

        self.main_layout.addStretch(0.5)
        self.main_layout.addLayout(self.placeholder_layout)
        self.main_layout.addStretch(0.5)

        self.setLayout(self.main_layout)
