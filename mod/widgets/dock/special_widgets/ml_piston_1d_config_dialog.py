#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics MLPiston1D Configuration Dialog. """

from PySide2 import QtWidgets

from mod.tools.translation_tools import __
from mod.tools.gui_tools import h_line_generator

from mod.dataobjects.case import Case
from mod.dataobjects.properties.ml_piston.ml_piston_1d import MLPiston1D
from mod.widgets.custom_widgets.size_input import SizeInput
from mod.widgets.custom_widgets.time_input import TimeInput
from mod.widgets.custom_widgets.value_input import ValueInput
from mod.widgets.custom_widgets.int_value_input import IntValueInput


class MLPiston1DConfigDialog(QtWidgets.QDialog):
    """ DesignSPHysics MLPiston1D Configuration Dialog. """

    def __init__(self, mk=None, mlpiston1d=None, parent=None):
        super().__init__(parent=parent)
        self.mk = mk
        self.temp_mlpiston1d = mlpiston1d if mlpiston1d is not None else MLPiston1D()
        self.mlpiston1d = mlpiston1d

        self.main_layout = QtWidgets.QVBoxLayout()
        self.data_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()

        self.mk_label = QtWidgets.QLabel(__("MK to use: {}").format(self.mk))

        self.filevelx_layout = QtWidgets.QHBoxLayout()
        self.filevelx_label = QtWidgets.QLabel(__("File with X velocity:"))
        self.filevelx_input = QtWidgets.QLineEdit()
        self.filevelx_browse = QtWidgets.QPushButton("...")

        for x in [self.filevelx_label, self.filevelx_input, self.filevelx_browse]:
            self.filevelx_layout.addWidget(x)

        self.incz_layout = QtWidgets.QHBoxLayout()
        self.incz_label = QtWidgets.QLabel(__("Z offset:"))
        self.incz_input = SizeInput()

        for x in [self.incz_label, self.incz_input]:
            self.incz_layout.addWidget(x)

        self.timedataini_layout = QtWidgets.QHBoxLayout()
        self.timedataini_label = QtWidgets.QLabel(__("Time offset:"))
        self.timedataini_input = TimeInput()

        for x in [self.timedataini_label, self.timedataini_input]:
            self.timedataini_layout.addWidget(x)

        self.smooth_layout = QtWidgets.QHBoxLayout()
        self.smooth_label = QtWidgets.QLabel(__("Smooth motion level:"))
        self.smooth_input = IntValueInput(min_val=0)

        for x in [self.smooth_label, self.smooth_input]:
            self.smooth_layout.addWidget(x)

        for x in [self.filevelx_layout, self.incz_layout, self.timedataini_layout, self.smooth_layout]:
            self.data_layout.addLayout(x)

        self.delete_button = QtWidgets.QPushButton(__("Delete piston configuration"))
        self.apply_button = QtWidgets.QPushButton(__("Apply this configuration"))
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
        self.temp_mlpiston1d.incz = self.incz_input.value()
        self.temp_mlpiston1d.timedataini = self.timedataini_input.value()
        self.temp_mlpiston1d.smooth = self.smooth_input.value()
        self.mlpiston1d = self.temp_mlpiston1d
        self.accept()

    def on_delete(self):
        """ Deletes the mlpiston1d """
        self.mlpiston1d = None
        self.reject()

    def fill_data(self):
        """ Fills the data for the dialog with the mlpiston1d information. """
        self.filevelx_input.setText(self.temp_mlpiston1d.filevelx)
        self.incz_input.setValue(self.temp_mlpiston1d.incz)
        self.timedataini_input.setValue(self.temp_mlpiston1d.timedataini)
        self.smooth_input.setValue(self.temp_mlpiston1d.smooth)

    def on_browse(self):
        """ Opens a file browser and sets the path for the file on the dialog. """
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, __("Open file"), Case.the().info.last_used_directory, "External velocity data (*.csv)")
        Case.the().info.update_last_used_directory(filename)
        self.filevelx_input.setText(filename)
