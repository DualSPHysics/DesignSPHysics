#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Add STL Dialog. """

from PySide import QtCore, QtGui

from mod.file_tools import import_geo
from mod.translation_tools import __
from mod.dialog_tools import error_dialog
from mod.freecad_tools import get_fc_main_window

from mod.dataobjects.case import Case

class AddGEODialog(QtGui.QDialog):
    """ A dialog that shows option to import a geometry passed as parameter """

    IS_DIALOG_MODAL: bool = True

    def __init__(self, file_name):
        super().__init__()

        # Defines import stl dialog
        self.setModal(self.IS_DIALOG_MODAL)
        self.setWindowTitle(__("Import GEO"))
        self.geo_dialog_layout = QtGui.QVBoxLayout()
        self.geo_group = QtGui.QGroupBox(__("Import GEO options"))
        self.geo_group_layout = QtGui.QVBoxLayout()

        # STL File selection
        self.geo_file_layout = QtGui.QHBoxLayout()
        self.geo_file_label = QtGui.QLabel(__("GEO File: "))
        self.geo_file_path = QtGui.QLineEdit()
        self.geo_file_path.setText(file_name)
        self.geo_file_browse = QtGui.QPushButton(__("Browse"))

        for x in [self.geo_file_label, self.geo_file_path, self.geo_file_browse]:
            self.geo_file_layout.addWidget(x)
        # END STL File selection

        # Scaling factor
        self.geo_scaling_layout = QtGui.QHBoxLayout()
        self.geo_scaling_label = QtGui.QLabel(__("Scaling factor: "))
        self.geo_scaling_x_l = QtGui.QLabel("X: ")
        self.geo_scaling_x_e = QtGui.QLineEdit("1")
        self.geo_scaling_y_l = QtGui.QLabel("Y: ")
        self.geo_scaling_y_e = QtGui.QLineEdit("1")
        self.geo_scaling_z_l = QtGui.QLabel("Z: ")
        self.geo_scaling_z_e = QtGui.QLineEdit("1")

        for x in [self.geo_scaling_label,
                  self.geo_scaling_x_l,
                  self.geo_scaling_x_e,
                  self.geo_scaling_y_l,
                  self.geo_scaling_y_e,
                  self.geo_scaling_z_l,
                  self.geo_scaling_z_e, ]:
            self.geo_scaling_layout.addWidget(x)
        # END Scaling factor

        # Import object name
        self.geo_objname_layout = QtGui.QHBoxLayout()
        self.geo_objname_label = QtGui.QLabel(__("Import object name: "))
        self.geo_objname_text = QtGui.QLineEdit("ImportedGEO")
        for x in [self.geo_objname_label, self.geo_objname_text]:
            self.geo_objname_layout.addWidget(x)
        # End object name

        # Autofill
        self.geo_autofil_layout = QtGui.QHBoxLayout()
        self.geo_autofill_chck = QtGui.QCheckBox("Autofill")
        self.geo_autofil_layout.addWidget(self.geo_autofill_chck)

        if self.geo_autofill_chck.isChecked():
            self.geo_autofill_chck.setCheckState(QtCore.Qt.Checked)
        else:
            self.geo_autofill_chck.setCheckState(QtCore.Qt.Unchecked)
        # End autofill

        # Add component layouts to group layout
        for x in [self.geo_file_layout, self.geo_scaling_layout, self.geo_objname_layout, self.geo_autofil_layout]:
            self.geo_group_layout.addLayout(x)
        self.geo_group_layout.addStretch(1)
        self.geo_group.setLayout(self.geo_group_layout)

        # Create button layout
        self.geo_button_layout = QtGui.QHBoxLayout()
        self.geo_button_ok = QtGui.QPushButton(__("Import"))
        self.geo_button_cancel = QtGui.QPushButton(__("Cancel"))
        self.geo_button_cancel.clicked.connect(self.reject)
        self.geo_button_layout.addStretch(1)
        self.geo_button_layout.addWidget(self.geo_button_cancel)
        self.geo_button_layout.addWidget(self.geo_button_ok)

        # Compose main window layout
        self.geo_dialog_layout.addWidget(self.geo_group)
        self.geo_dialog_layout.addStretch(1)
        self.geo_dialog_layout.addLayout(self. geo_button_layout)

        self.setLayout(self.geo_dialog_layout)

        self.geo_button_cancel.clicked.connect(self.reject)
        self.geo_button_ok.clicked.connect(self.geo_ok_clicked)
        self.geo_file_browse.clicked.connect(self.geo_dialog_browse)

        self.exec_()

    def geo_ok_clicked(self):
        """ Defines ok button behaviour"""
        for geo_scaling_edit in [self.geo_scaling_x_e, self.geo_scaling_y_e, self.geo_scaling_z_e]:
            geo_scaling_edit.setText(geo_scaling_edit.text().replace(",", "."))
        try:
            import_geo(filename=str(self.geo_file_path.text()),
                       scale_x=float(self.geo_scaling_x_e.text()),
                       scale_y=float(self.geo_scaling_y_e.text()),
                       scale_z=float(self.geo_scaling_z_e.text()),
                       name=str(self.geo_objname_text.text()),
                       autofill=self.geo_autofill_chck.isChecked(),
                       case=Case.instance())

            self.accept()
        except ValueError:
            error_dialog(__("There was an error. Are you sure you wrote correct float values in the sacaling factor?"))

    def geo_dialog_browse(self):
        """ Defines the browse button behaviour."""
        file_name_temp, _ = QtGui.QFileDialog().getOpenFileName(get_fc_main_window(), __("Select GEO to import"), QtCore.QDir.homePath(), "STL Files (*.stl);;PLY Files (*.ply);;VTK Files (*.vtk)")
        self.geo_file_path.setText(file_name_temp)
        self.raise_()
        self.activateWindow()
