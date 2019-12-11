#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics MLPiston1D Configuration Dialog. """

from PySide import QtGui

from mod.translation_tools import __
from mod.gui_tools import h_line_generator

from mod.dataobjects.case import Case
from mod.dataobjects.ml_piston_1d import MLPiston1D


class MLPiston1DConfigDialog(QtGui.QDialog):
    """ DesignSPHysics MLPiston1D Configuration Dialog. """

    def __init__(self, mk=None, mlpiston1d=None, parent=None):
        super().__init__(parent=parent)
        self.mk = mk
        self.temp_mlpiston1d = mlpiston1d if mlpiston1d is not None else MLPiston1D()
        self.mlpiston1d = mlpiston1d

        self.main_layout = QtGui.QVBoxLayout()
        self.data_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()

        self.mk_label = QtGui.QLabel(__("MK to use: {}").format(self.mk))

        self.filevelx_layout = QtGui.QHBoxLayout()
        self.filevelx_label = QtGui.QLabel(__("File with X velocity:"))
        self.filevelx_input = QtGui.QLineEdit()
        self.filevelx_browse = QtGui.QPushButton("...")

        for x in [self.filevelx_label, self.filevelx_input, self.filevelx_browse]:
            self.filevelx_layout.addWidget(x)

        self.incz_layout = QtGui.QHBoxLayout()
        self.incz_label = QtGui.QLabel(__("Z offset (m):"))
        self.incz_input = QtGui.QLineEdit()

        for x in [self.incz_label, self.incz_input]:
            self.incz_layout.addWidget(x)

        self.timedataini_layout = QtGui.QHBoxLayout()
        self.timedataini_label = QtGui.QLabel(__("Time offset (s):"))
        self.timedataini_input = QtGui.QLineEdit()

        for x in [self.timedataini_label, self.timedataini_input]:
            self.timedataini_layout.addWidget(x)

        self.smooth_layout = QtGui.QHBoxLayout()
        self.smooth_label = QtGui.QLabel(__("Smooth motion level:"))
        self.smooth_input = QtGui.QLineEdit()

        for x in [self.smooth_label, self.smooth_input]:
            self.smooth_layout.addWidget(x)

        for x in [self.filevelx_layout, self.incz_layout, self.timedataini_layout, self.smooth_layout]:
            self.data_layout.addLayout(x)

        self.delete_button = QtGui.QPushButton(__("Delete piston configuration"))
        self.apply_button = QtGui.QPushButton(__("Apply this configuration"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.apply_button)

        self.main_layout.addWidget(self.mk_label)
        self.main_layout.addWidget(h_line_generator())
        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.button_layout)

        self.apply_button.clicked.connect(self.on_apply)
        self.delete_button.clicked.connect(self.on_delete)
        self.filevelx_browse.clicked.connect(self.on_browse)

        self.setLayout(self.main_layout)

        self.fill_data()
        self.exec_()

    def on_apply(self):
        """ Applies the currently introduced data on the selected mlpiston1d. """
        self.temp_mlpiston1d.filevelx = str(self.filevelx_input.text())
        self.temp_mlpiston1d.incz = float(self.incz_input.text())
        self.temp_mlpiston1d.timedataini = float(self.timedataini_input.text())
        self.temp_mlpiston1d.smooth = int(self.smooth_input.text())
        self.mlpiston1d = self.temp_mlpiston1d
        self.accept()

    def on_delete(self):
        """ Deletes the mlpiston1d """
        self.mlpiston1d = None
        self.reject()

    def fill_data(self):
        """ Fills the data for the dialog with the mlpiston1d information. """
        self.filevelx_input.setText(str(self.temp_mlpiston1d.filevelx))
        self.incz_input.setText(str(self.temp_mlpiston1d.incz))
        self.timedataini_input.setText(str(self.temp_mlpiston1d.timedataini))
        self.smooth_input.setText(str(self.temp_mlpiston1d.smooth))

    def on_browse(self):
        """ Opens a file browser and sets the path for the file on the dialog. """
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, __("Open file"), Case.the().info.last_used_directory, "External velocity data (*.csv)")
        Case.the().info.update_last_used_directory(filename)
        self.filevelx_input.setText(filename)
