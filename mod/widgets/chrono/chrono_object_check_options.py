#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Chrono Object Check Options widget."""

from PySide import QtGui

from mod.translation_tools import __


class ChronoObjectCheckOptions(QtGui.QWidget):
    """ Widget shows check options for an object """

    def __init__(self, key, object_name="No name", object_mk=-1, mktype="bound", is_floating="", parent=None):
        super().__init__(parent=parent)

        self.key = key
        self.object_name = object_name
        self.object_mk = object_mk
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.mk_label = QtGui.QLabel(
            "<b>{}{}</b>".format(mktype[0].upper(), str(object_mk)))
        self.name_label = QtGui.QLabel(str(object_name))
        self.is_floating = is_floating
        self.object_check = QtGui.QCheckBox()
        self.geometry_check = QtGui.QCheckBox(__("Geometry"))
        self.modelnormal_input = QtGui.QComboBox()
        self.modelnormal_input.insertItems(0, ["Original", "Invert", "Two face"])

        self.main_layout.addWidget(self.object_check)
        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.geometry_check)
        self.main_layout.addWidget(self.modelnormal_input)

        self.setLayout(self.main_layout)
