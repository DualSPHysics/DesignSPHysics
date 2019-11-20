#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Body Configuration Dialog. """

from PySide import QtGui

from mod.translation_tools import __
from mod.gui_tools import h_line_generator

from mod.dataobjects.moorings.moordyn.moordyn_body import MoorDynBody


class MoorDynBodyConfigurationDialog(QtGui.QDialog):
    """ DesignSPHysics MoorDyn Body Configuration Dialog. """

    def __init__(self, body):
        super().__init__()
        self.body: MoorDynBody = body

        self.setWindowTitle(__("MoorDyn Body Configuration"))
        self.setMinimumWidth(440)
        self.root_layout: QtGui.QVBoxLayout = QtGui.QVBoxLayout()

        # Label
        self.reference_label: QtGui.QLable = QtGui.QLabel(__("Editing settings for reference (mkbound): <b>{}</b>").format(body.ref))

        # Depth value introduction
        self.depth_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.depth_label: QtGui.QLabel = QtGui.QLabel(__("Water depth: "))
        self.depth_enable_check: QtGui.QCheckBox = QtGui.QCheckBox(__("Override"))
        self.depth_value_line_edit: QtGui.QLineEdit = QtGui.QLineEdit()
        self.depth_layout.addWidget(self.depth_label)
        self.depth_layout.addStretch(1)
        self.depth_layout.addWidget(self.depth_enable_check)
        self.depth_layout.addWidget(self.depth_value_line_edit)

        # Bottom button row
        self.button_layout: QtGui.QHBoxLayout = QtGui.QHBoxLayout()
        self.ok_button: QtGui.QPushButton = QtGui.QPushButton(__("OK"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.ok_button)

        # Main layout composition
        self.root_layout.addWidget(self.reference_label)
        self.root_layout.addWidget(h_line_generator())
        self.root_layout.addLayout(self.depth_layout)
        self.root_layout.addStretch(1)
        self.root_layout.addLayout(self.button_layout)
        self.setLayout(self.root_layout)

        # Connections
        self.ok_button.clicked.connect(self._on_ok)
        self.depth_enable_check.stateChanged.connect(self._on_enable)

        self._fill_data()
        self.exec_()

    def _fill_data(self):
        # self.body.depth can be either False or a float value. Compensate for that.
        self.depth_value_line_edit.setText(str(self.body.depth) if self.body.depth else "")
        self.depth_value_line_edit.setEnabled(bool(self.body.depth))
        self.depth_enable_check.setChecked(bool(self.body.depth))

    def _on_ok(self):
        self.body.depth = float(self.depth_value_line_edit.text()) if self.depth_enable_check.isChecked() and self.depth_value_line_edit.text() else False
        self.accept()

    def _on_enable(self):
        self.depth_value_line_edit.setEnabled(self.depth_enable_check.isChecked())
