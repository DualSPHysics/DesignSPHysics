#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics MLPiston2D Configuration Dialog """

import glob
from os import path

from PySide import QtGui

from mod.translation_tools import __
from mod.gui_tools import h_line_generator
from mod.dialog_tools import error_dialog

from mod.dataobjects.case import Case
from mod.dataobjects.ml_piston_2d import MLPiston2D
from mod.dataobjects.ml_piston_2d_veldata import MLPiston2DVeldata


class MLPiston2DConfigDialog(QtGui.QDialog):
    """ A Dialog to configure an MLPiston2D configuration. """

    def __init__(self, mk=None, mlpiston2d=None, parent=None):
        super().__init__(parent=parent)
        self.mk = mk
        self.temp_mlpiston2d = mlpiston2d if mlpiston2d else MLPiston2D()
        self.mlpiston2d = mlpiston2d

        self.main_layout = QtGui.QVBoxLayout()
        self.data_layout = QtGui.QVBoxLayout()
        self.button_layout = QtGui.QHBoxLayout()

        self.mk_label = QtGui.QLabel(__("MK to use: {}").format(self.mk))

        self.incz_layout = QtGui.QHBoxLayout()
        self.incz_label = QtGui.QLabel(__("Z offset (m):"))
        self.incz_input = QtGui.QLineEdit()

        for x in [self.incz_label, self.incz_input]:
            self.incz_layout.addWidget(x)

        self.smooth_layout = QtGui.QHBoxLayout()
        self.smooth_label = QtGui.QLabel(__("Smooth motion level (Z, Y):"))
        self.smooth_z = QtGui.QLineEdit()
        self.smooth_y = QtGui.QLineEdit()

        for x in [self.smooth_label, self.smooth_z, self.smooth_y]:
            self.smooth_layout.addWidget(x)

        self.veldata_groupbox = QtGui.QGroupBox(__("Velocity data"))
        self.veldata_groupbox_layout = QtGui.QVBoxLayout()

        self.veldata_filevelx_layout = QtGui.QHBoxLayout()
        self.veldata_filevelx_label = QtGui.QLabel(__("File series"))
        self.veldata_filevelx_input = QtGui.QLineEdit()
        self.veldata_filevelx_browse = QtGui.QPushButton("...")
        for x in [self.veldata_filevelx_label, self.veldata_filevelx_input, self.veldata_filevelx_browse]:
            self.veldata_filevelx_layout.addWidget(x)

        self.veldata_files_label = QtGui.QLabel(__("No files selected"))

        self.veldata_posy_layout = QtGui.QHBoxLayout()
        self.veldata_posy_label = QtGui.QLabel(__("Y positions (separated by commas):"))
        self.veldata_posy_input = QtGui.QLineEdit()
        for x in [self.veldata_posy_label, self.veldata_posy_input]:
            self.veldata_posy_layout.addWidget(x)

        self.veldata_timedataini_layout = QtGui.QHBoxLayout()
        self.veldata_timedataini_label = QtGui.QLabel(__("Time offsets (separated by commas):"))
        self.veldata_timedataini_input = QtGui.QLineEdit()
        for x in [self.veldata_timedataini_label, self.veldata_timedataini_input]:
            self.veldata_timedataini_layout.addWidget(x)

        self.veldata_groupbox_layout.addLayout(self.veldata_filevelx_layout)
        self.veldata_groupbox_layout.addWidget(self.veldata_files_label)
        self.veldata_groupbox_layout.addLayout(self.veldata_posy_layout)
        self.veldata_groupbox_layout.addLayout(self.veldata_timedataini_layout)
        self.veldata_groupbox.setLayout(self.veldata_groupbox_layout)

        for x in [self.incz_layout, self.smooth_layout]:
            self.data_layout.addLayout(x)
        self.data_layout.addWidget(self.veldata_groupbox)

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
        self.veldata_filevelx_browse.clicked.connect(self.on_browse)

        self.setLayout(self.main_layout)

        self.fill_data()
        self.exec_()

    def on_apply(self):
        """ Applies the currently introduced MLPiston2D configuration to the data structure. """
        self.temp_mlpiston2d.incz = float(self.incz_input.text())
        self.temp_mlpiston2d.smoothz = int(self.smooth_z.text())
        self.temp_mlpiston2d.smoothy = int(self.smooth_y.text())
        list_posy = self.veldata_posy_input.text().split(",")
        list_timedataini = self.veldata_timedataini_input.text().split(",")
        if len(list_posy) != len(list_timedataini) or len(self.temp_mlpiston2d.veldata) != len(list_posy) or len(self.temp_mlpiston2d.veldata) != len(list_timedataini):
            error_dialog(__("Wrong number of Y positions or Time offsets. Introduce {} of them separated by commas").format(len(self.temp_mlpiston2d.veldata)))
            return
        for index, _ in enumerate(self.temp_mlpiston2d.veldata):
            self.temp_mlpiston2d.veldata[index].posy = list_posy[index]
            self.temp_mlpiston2d.veldata[index].timedataini = list_timedataini[index]

        self.mlpiston2d = self.temp_mlpiston2d
        self.accept()

    def on_delete(self):
        """ Deletes the MLPiston2D from the data structure. """
        self.mlpiston2d = None
        self.reject()

    def fill_data(self):
        """ Fills the data for this MLPiston2D into the dialog. """
        self.incz_input.setText(str(self.temp_mlpiston2d.incz))
        self.smooth_z.setText(str(self.temp_mlpiston2d.smoothz))
        self.smooth_y.setText(str(self.temp_mlpiston2d.smoothy))
        if self.temp_mlpiston2d.veldata:
            self.veldata_files_label.setText(__("The serie has {} files").format(len(self.temp_mlpiston2d.veldata)))
            self.veldata_filevelx_input.setText(self.temp_mlpiston2d.veldata[0].filevelx.split("_x")[0])
            self.veldata_posy_input.setText(",".join([str(x.posy) for x in self.temp_mlpiston2d.veldata]))
            self.veldata_timedataini_input.setText(",".join([str(x.timedataini) for x in self.temp_mlpiston2d.veldata]))
        else:
            self.veldata_files_label.setText(__("No files selected"))
            self.veldata_filevelx_input.setText("None")
            self.veldata_posy_input.setText("")
            self.veldata_timedataini_input.setText("")

    def on_browse(self):
        """ Opens a file browser to select the external velocity data, then parses it and fills the dialog with the information. """
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, __("Open a file from the serie"), Case.the().info.last_used_directory, "External velocity data (*_x*_y*.csv)")
        Case.the().info.update_last_used_directory(filename)
        if not filename:
            return

        basename: str = path.basename(filename)
        folder: str = path.dirname(filename)

        filename_filtered = "{}/{}".format(folder, basename.split("_x")[0])
        self.veldata_filevelx_input.setText(str(filename_filtered))
        serie_filenames = glob.glob("{}*.csv".format(filename_filtered))
        self.temp_mlpiston2d.veldata = list()
        for serie_filename in serie_filenames:
            serie_filename = serie_filename.replace("\\", "/")
            self.temp_mlpiston2d.veldata.append(MLPiston2DVeldata(serie_filename, 0, 0))
        self.veldata_files_label.setText(__("The serie has {} files").format(len(self.temp_mlpiston2d.veldata)))
        self.veldata_posy_input.setText(",".join([str(x.posy) for x in self.temp_mlpiston2d.veldata]))
        self.veldata_timedataini_input.setText(",".join([str(x.timedataini) for x in self.temp_mlpiston2d.veldata]))
