#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" DesignSPHysics MoorDyn Body Configuration Dialog. """

# from PySide import QtGui
from PySide6 import QtWidgets

from mod.translation_tools import __
from mod.gui_tools import h_line_generator

from mod.dataobjects.moorings.moordyn.moordyn_body import MoorDynBody


class MoorDynBodyConfigurationDialog(QtWidgets.QDialog):
    """ DesignSPHysics MoorDyn Body Configuration Dialog. """

    def __init__(self, body):
        super().__init__()
        self.body: MoorDynBody = body

        self.setWindowTitle(__("MoorDyn Body Configuration"))
        self.setMinimumWidth(440)
        self.root_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        # Label
        self.reference_label: QtWidgets.QLable = QtWidgets.QLabel(__("Editing settings for reference (mkbound): <b>{}</b>").format(body.ref))

        # Depth value introduction
        self.depth_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.depth_label: QtWidgets.QLabel = QtWidgets.QLabel(__("Water depth: "))
        self.depth_enable_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox(__("Override"))
        self.depth_value_line_edit: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.depth_layout.addWidget(self.depth_label)
        self.depth_layout.addStretch(1)
        self.depth_layout.addWidget(self.depth_enable_check)
        self.depth_layout.addWidget(self.depth_value_line_edit)

        # Bottom button row
        self.button_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.ok_button: QtWidgets.QPushButton = QtWidgets.QPushButton(__("OK"))
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
